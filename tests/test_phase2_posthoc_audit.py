"""Diagnostic fixtures for the explicitly post-hoc attribution audit, not model runs."""
import json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from svb.phase2 import load_cases,public_id
ROOT=Path(__file__).resolve().parents[1]
class RawAttributionAudit(unittest.TestCase):
 def test_known_ids_and_unknown_ids_remain_distinct_without_probability_repair(self):
  c=next(c for c in load_cases(ROOT) if c['split']=='evaluation');doc=c['packet']['documents'][0]['id']
  rows=[]
  for condition,ids in [('evidence',[doc]),('no_evidence',['imaginary'])]:
   rows.append({'id':public_id(c),'condition':condition,'status':'completed','raw_text':json.dumps({'label':'formally_established','confidence':0.99,'evidence_ids':ids,'citations':[]})})
  with tempfile.TemporaryDirectory(dir=ROOT/'results') as d:
   p=Path(d);(p/'raw.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows))
   proc=subprocess.run([sys.executable,'-B','scripts/audit_phase2_outputs.py',str(p/'raw.jsonl'),'--output',str(p/'audit.json')],cwd=ROOT,capture_output=True,text=True,timeout=15)
   self.assertEqual(proc.returncode,0,proc.stderr);r=json.loads((p/'audit.json').read_text())
  self.assertEqual(r['conditions']['evidence']['nonsupplied_evidence_id_cases_among_parseable'],0)
  self.assertEqual(r['conditions']['no_evidence']['nonsupplied_evidence_id_cases_among_parseable'],1)
  self.assertEqual(r['conditions']['no_evidence']['scalar_confidence_cases'],1)
  self.assertIn('not a replacement',r['analysis'])
 def test_nonparseable_raw_output_is_not_silently_dropped(self):
  c=next(c for c in load_cases(ROOT) if c['split']=='evaluation')
  row={'id':public_id(c),'condition':'evidence','status':'completed','raw_text':'{"label":'}
  with tempfile.TemporaryDirectory(dir=ROOT/'results') as d:
   p=Path(d);(p/'raw.jsonl').write_text(json.dumps(row)+'\n')
   proc=subprocess.run([sys.executable,'-B','scripts/audit_phase2_outputs.py',str(p/'raw.jsonl'),'--output',str(p/'audit.json')],cwd=ROOT,capture_output=True,text=True,timeout=15)
   self.assertEqual(proc.returncode,0,proc.stderr);s=json.loads((p/'audit.json').read_text())['conditions']['evidence']
  self.assertEqual(s['observed_n'],1);self.assertEqual(s['parse_failures'],1);self.assertEqual(s['parseable_object_n'],0)
