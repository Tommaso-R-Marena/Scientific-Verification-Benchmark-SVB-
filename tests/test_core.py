from __future__ import annotations
import copy,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from svb.core import Invalid,calculate,load_dataset,validate_freeze,read,score,LABELS
from svb.baselines import public_item,predict
ROOT=Path(__file__).resolve().parents[1]
class CoreTests(unittest.TestCase):
    def test_all_references_recompute(self):
        tasks=load_dataset(ROOT)
        self.assertEqual(len(tasks),34)
        for t in tasks:
            self.assertEqual(calculate(t['checker'],ROOT)[0],t['reference']['label'])
    def test_public_baseline_view_cannot_access_label(self):
        for t in load_dataset(ROOT):
            v=public_item(t)
            self.assertNotIn('reference',v);self.assertNotIn('expected_response',v)
            self.assertNotIn('success_label',v['checker'])
    def test_rational_reference_forbids_empirical_promotion(self):
        p={'kind':'rational','operation':'sum','values':['1'],'claimed':'1','success_label':'empirically_supported'}
        with self.assertRaises(Invalid): calculate(p,ROOT)
    def test_no_known_paired_controls_cross_split(self):
        ts={t['id']:t for t in load_dataset(ROOT)}
        for a,b in [('C01','C03'),('B01','B02')]:
            self.assertEqual(ts[a]['split'],ts[b]['split']);self.assertEqual(ts[a]['family'],ts[b]['family'])
    def test_missing_bridge_conflicts_fail(self):
        p={'kind':'missing_bridge','available':['empirical'],'missing':['empirical'],'worlds':['a','b']}
        with self.assertRaises(Invalid):calculate(p,ROOT)
    def test_corruption_and_reference_label_mutation_fail(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'results') as temp:
            p=Path(temp);shutil.copytree(ROOT/'data',p/'data')
            (p/'data/iris.data').write_text('CORRUPT')
            with self.assertRaises(Invalid):load_dataset(p)
    def test_scaling_fraction_metamorphism(self):
        for n in range(1,20):
            p={'kind':'rational','operation':'ratio','values':[str(3*n),str(4*n)],'claimed':'3/4','success_label':'computationally_established'}
            self.assertEqual(calculate(p,ROOT)[0],'computationally_established')
    def test_confidence_brier_known_values(self):
        t=load_dataset(ROOT)[0];r={'id':t['id'],'status':'ok','label':'refuted','scopes':[], 'confidence':{k:float(k=='refuted') for k in LABELS},'reason':'wrong'}
        self.assertEqual(score([t],[r])['summary']['mean_brier_answered'],2)
    def test_manifest_and_cli_reject_incomplete_outputs(self):
        validate_freeze(ROOT)
        proc=subprocess.run([sys.executable,'-B','-m','svb.cli','--root',str(ROOT),'validate'],cwd=ROOT,capture_output=True,text=True,timeout=20)
        self.assertEqual(proc.returncode,0,proc.stderr)
        self.assertTrue(json.loads(proc.stdout)['validated'])
if __name__=='__main__':unittest.main()
