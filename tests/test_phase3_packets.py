"""Bounded pilot provenance and masking checks; no actual blinding claim."""
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
import zipfile
from svb.adjudication import validate_context,digest_bytes,digest_json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_phase3_pilot as pilot

class Pilot(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.archives,cls.context,cls.registry,cls.coord=pilot.build()
 def unpack(self,name):
  with zipfile.ZipFile(io.BytesIO(self.archives[name])) as z:return {n:z.read(n) for n in z.namelist()}
 def test_twelve_fixed_cases_five_families_no_humans(self):
  self.assertEqual(len(self.context['packets']),12);self.assertEqual(len({p['source_family'] for p in self.context['packets']}),5)
  self.assertEqual(self.coord['human_reviews_completed'],0);self.assertIsNone(self.registry['coordinator_attestation'])
 def test_context_hashes_and_candidate_identity_validate(self):validate_context(self.context)
 def test_reference_package_has_no_candidate_or_gold_fields(self):
  files=self.unpack('reference_review.zip');self.assertNotIn('candidates.json',files)
  packets=json.loads(files['packets.json'])
  for p in packets:
   self.assertEqual(set(p),{'packet_id','question','claim','documents','methodology','assumptions'})
   self.assertNotIn('public_id',p)
  self.assertNotIn('coordinator_context.json',files);self.assertNotIn('preparation_record.json',files)
 def test_candidate_raw_text_preserved_without_provider_envelope(self):
  files=self.unpack('candidate_review.zip');cs=json.loads(files['candidates.json'])
  source=[]
  for model in ['0.5b','1.5b']:
   source += [json.loads(s)['raw_text'] for s in (ROOT/f'results/v0.3.0/evaluation/qwen-{model}_unconstrained.jsonl').read_text().splitlines() if json.loads(s)['task']=='B']
  self.assertCountEqual([c['raw_response'] for c in cs],source)
  for c in cs:self.assertEqual(set(c),{'candidate_id','packet_id','candidate_sha256','raw_response','generation_status'})
 def test_source_bundle_is_hash_bound_and_licensed_sources_complete(self):
  ref=json.loads(self.unpack('reference_review.zip')['source_bundle.json'])
  self.assertEqual(ref['sha256'],digest_bytes(self.archives['source_materials.zip']))
  files=self.unpack('source_materials.zip');reg=json.loads(files['source_registry.json'])
  self.assertEqual(len(reg['sources']),5)
  for src in reg['sources'].values():
   self.assertIn('license',src)
   for a in src['artifacts']:self.assertEqual(digest_bytes(files[a['package_path']]),a['sha256'])
 def test_blank_forms_make_no_human_attestation_and_allow_category_challenge(self):
  f=json.loads(self.unpack('reference_review.zip')['blank_response.json'])
  self.assertIsNone(f['origin']);self.assertIsNone(f['declaration']['human_attestation'])
  self.assertTrue(all(j['category_relation'] is None and j['legacy_labels']==[] for j in f['judgments']))
 def test_build_is_byte_identical_on_repeat(self):
  again,_,_,_=pilot.build();self.assertEqual(self.archives,again)
 def test_each_package_manifest_binds_every_other_entry(self):
  for name in ['reference_review.zip','candidate_review.zip']:
   files=self.unpack(name);m=json.loads(files.pop('manifest.json'))
   self.assertFalse(m['actual_blinding_established']);self.assertEqual(m['human_reviews_completed'],0)
   self.assertEqual(m['files'],{k:digest_bytes(v) for k,v in files.items()})
if __name__=='__main__':unittest.main()
