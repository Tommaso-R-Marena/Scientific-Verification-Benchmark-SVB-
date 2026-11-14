"""Frozen-package qualification is distinct from scientific expert review."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from svb.core import Invalid
from svb.phase3 import validate
ROOT=Path(__file__).resolve().parents[1]

class Freeze(unittest.TestCase):
 def test_frozen_pilot_and_shared_source_integrity(self):
  r=validate(ROOT);self.assertEqual(r['reference_packets'],12)
  self.assertEqual(r['human_reviews_completed'],0);self.assertFalse(r['scientific_taxonomy_validated'])
 def test_corruption_and_manifest_path_escape_fail(self):
  m=json.loads((ROOT/'data/v0.4.0/manifest.json').read_text())
  with tempfile.TemporaryDirectory() as td:
   root=Path(td)
   for n in [*m['files'],'data/v0.4.0/manifest.json']:
    dest=root/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,dest)
   p=root/'data/v0.4.0/pilot/reference_review.zip';p.write_bytes(p.read_bytes()+b'corruption')
   with self.assertRaises(Invalid):validate(root)
   m['files']={'../escape':'0'*64};(root/'data/v0.4.0/manifest.json').write_text(json.dumps(m))
   with self.assertRaises(Invalid):validate(root)
if __name__=='__main__':unittest.main()
