"""Data admission/token constraint tests; no model dependency or inference."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('phase2b_runner',ROOT/'scripts/run_phase2b_model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Phase2bRunner(unittest.TestCase):
 @classmethod
 def setUpClass(cls):(ROOT/'results/local').mkdir(parents=True,exist_ok=True)
 def test_category_is_exact_without_fence_or_quote_repair(self):
  self.assertEqual(m.exact_category('  refuted\n'),'refuted')
  for s in ('"refuted"','```refuted```','Refuted','refuted because',''):
   with self.subTest(s=s):self.assertIsNone(m.exact_category(s))
 def test_six_category_trie_cannot_escape_or_stop_early(self):
  seqs=[[1,2],[1,3],[4],[5],[6,7],[6,8]];trie=m.CategoryTrie(seqs,99)
  self.assertEqual(trie.allowed([]),[1,4,5,6]);self.assertEqual(trie.allowed([1]),[2,3]);self.assertEqual(trie.allowed([4]),[99])
  with self.assertRaises(m.InputError):trie.allowed([8])
  self.assertNotIn(99,trie.allowed([1]))
 def test_duplicate_trie_paths_and_eos_inside_label_reject(self):
  with self.assertRaises(m.InputError):m.CategoryTrie([[1]]*6,99)
  with self.assertRaises(m.InputError):m.CategoryTrie([[i] for i in range(6)],0)
 def test_hidden_metadata_and_duplicate_prompts_reject(self):
  r={'id':'x','task':'A','condition':'dev','messages':[{'role':'user','content':'Assess evidence.'}]}
  with tempfile.TemporaryDirectory(dir=ROOT/'results/local') as d:
   p=Path(d)/'p';p.write_text(json.dumps(r)+'\n');self.assertEqual(m.load_prompts(p),[r])
   p.write_text(json.dumps(dict(r,reference='refuted'))+'\n')
   with self.assertRaises(m.InputError):m.load_prompts(p)
   p.write_text((json.dumps(r)+'\n')*2)
   with self.assertRaises(m.InputError):m.load_prompts(p)
 def test_duplicate_keys_and_nonfinite_reject(self):
  for s in ('{"x":0,"x":1}','{"x":NaN}','{"x":1e999}'):
   with self.assertRaises(m.InputError):m.loads(s)
 def test_task_enum_not_arbitrary_evaluation_command(self):
  r={'id':'x','task':'execute','condition':'dev','messages':[{'role':'user','content':'q'}]}
  with tempfile.TemporaryDirectory(dir=ROOT/'results/local') as d:
   p=Path(d)/'p';p.write_text(json.dumps(r)+'\n')
   with self.assertRaises(m.InputError):m.load_prompts(p)
if __name__=='__main__':unittest.main()
