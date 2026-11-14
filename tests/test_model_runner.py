"""Runner admission tests: no model dependency or inference needed."""
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('svb_local_runner',ROOT/'scripts/run_local_model.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class LocalModelAdmission(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  (ROOT/'results/local').mkdir(parents=True,exist_ok=True)
 def test_duplicate_or_nonfinite_json_is_rejected(self):
  for s in ('{"x":1,"x":2}','{"x":NaN}','{"x":1e999}'):
   with self.subTest(s=s),self.assertRaises(m.InputError):m.strict_loads(s)
 def test_prompts_are_allowlisted_data_not_reference_records(self):
  good={'id':'x','condition':'evidence','messages':[{'role':'user','content':'What follows from this observation?'}]}
  with tempfile.TemporaryDirectory(dir=ROOT/'results/local') as d:
   p=Path(d)/'p.jsonl';p.write_text(json.dumps(good)+'\n')
   self.assertEqual(m.load_prompts(p),[good])
   bad=dict(good,reference={'label':'refuted'});p.write_text(json.dumps(bad)+'\n')
   with self.assertRaises(m.InputError):m.load_prompts(p)
 def test_duplicate_conditions_reject_not_silently_replace(self):
  row={'id':'x','condition':'evidence','messages':[{'role':'user','content':'q'}]}
  with tempfile.TemporaryDirectory(dir=ROOT/'results/local') as d:
   p=Path(d)/'p.jsonl';p.write_text((json.dumps(row)+'\n')*2)
   with self.assertRaises(m.InputError):m.load_prompts(p)
 def test_assistant_exemplars_and_arbitrary_fields_rejected(self):
  row={'id':'x','condition':'evidence','messages':[{'role':'assistant','content':'the answer'}]}
  with tempfile.TemporaryDirectory(dir=ROOT/'results/local') as d:
   p=Path(d)/'p.jsonl';p.write_text(json.dumps(row)+'\n')
   with self.assertRaises(m.InputError):m.load_prompts(p)
 def test_output_confinement_and_no_overwrite(self):
  with self.assertRaises(m.InputError):m.inside_output(Path('/tmp/unapproved-model-output.jsonl'))
  with self.assertRaises(m.InputError):m.inside_output(ROOT/'README.md')
if __name__=='__main__':unittest.main()
