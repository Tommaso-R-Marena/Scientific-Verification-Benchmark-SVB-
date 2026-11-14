"""Phase II source admission,arithmetic,variant sufficiency and provenance tests."""
from __future__ import annotations
from copy import deepcopy
from collections import Counter
import csv
import gzip
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from svb.phase2_references import validate,recompute,verify_source_transformations
from svb.phase2 import load_cases,build_prompt,condition_reference,source_overlap

class PhaseIIReferenceTests(unittest.TestCase):
    def test_all_source_hashes_and_numeric_witnesses(self):
        result=validate(ROOT)
        self.assertEqual(result['numeric_witnesses_checked'],17)
        self.assertFalse(result['empirical_adequacy_mechanically_validated'])
        self.assertFalse(result['external_human_adjudication'])

    def test_pairs_and_source_splits(self):
        cs=load_cases(ROOT)
        self.assertEqual(len(cs),32)
        self.assertEqual(Counter(c['split'] for c in cs),{'dev':8,'evaluation':24})
        self.assertEqual(set(Counter(c['pair']['id'] for c in cs).values()),{2})
        self.assertEqual(source_overlap(cs)['cross_split_sources'],[])

    def test_numeric_comparisons_are_exact(self):
        self.assertEqual(recompute('puromycin_mean_011',ROOT)['difference'],'49/2')
        self.assertEqual(recompute('freesolv_residual',ROOT)['residual'],'-11/4')
        self.assertEqual(recompute('grass_mississippi_1000',ROOT),{'nonchilled':'158/5','chilled':'281/15'})
        self.assertEqual(recompute('grass_quebec_1000',ROOT),{'nonchilled':'259/6','chilled':'245/6'})

    def test_source_rows_not_independent_animals_or_plants(self):
        self.assertEqual(recompute('penguin_ids',ROOT),{'rows':344,'unique_id':190,'unique_study_id':344})
        self.assertEqual(recompute('grass_counts',ROOT),{'plants':12,'rows':84,'per_plant':7})
        self.assertEqual(recompute('puromycin_counts',ROOT),{'treated':12,'untreated':11})

    def test_default_uncertainty_not_measured_confidence(self):
        self.assertTrue(recompute('freesolv_default',ROOT)['default_note'])
        cs={c['id']:c for c in load_cases(ROOT)}
        self.assertEqual(cs['FS03S']['reference']['label'],'refuted')
        self.assertEqual(cs['CO02S']['reference']['label'],'refuted')

    def test_withheld_evidence_changes_justification_not_truth(self):
        for c in load_cases(ROOT):
            with self.subTest(case=c['id']):
                p=build_prompt(c,'no_evidence')
                user=json.loads(p['messages'][1]['content'])
                self.assertEqual(user['documents'],[])
                self.assertEqual(condition_reference(c,'no_evidence')['label'],'insufficient_evidence')
                self.assertEqual(condition_reference(c,'no_evidence')['scopes'],[])

    def test_public_prompt_excludes_reference_annotations(self):
        for c in load_cases(ROOT):
            p=json.loads(build_prompt(c,'evidence')['messages'][1]['content'])
            self.assertEqual(set(p),{'question','claim','documents','methodology','assumptions'})
            self.assertNotIn('numeric_check',json.dumps(p))
            self.assertNotIn('provisional_author_adjudicated',json.dumps(p))
        pu=next(c for c in load_cases(ROOT) if c['id']=='PU01N')
        fs=next(c for c in load_cases(ROOT) if c['id']=='FS01N')
        self.assertNotIn('no clinical endpoints',json.dumps(pu['packet']))
        self.assertNotIn('No correlation matrix',json.dumps(fs['packet']))

    def test_numeric_tool_note_does_not_add_an_adequacy_label(self):
        for c in load_cases(ROOT):
            if c['pair']['id'] in {'PU01','PU02'}:
                p=json.loads(build_prompt(c,'verified_numbers')['messages'][1]['content'])
                self.assertEqual(p['documents'][-1]['id'],'calculator')
                note=p['documents'][-1]['text']
                self.assertFalse(any(x in note for x in ('insufficient_evidence','empirically_supported','clinical','population')))

    def test_license_and_upstream_qualifications_preserved(self):
        r=json.loads((ROOT/'data/v0.2.0/registry.json').read_text())['sources']
        self.assertEqual(r['freesolv']['license'],'CC-BY-4.0')
        self.assertIn('original restrictions may apply',r['freesolv']['limitations'])
        self.assertEqual(r['puromycin']['license'],'GPL-2.0-or-later')
        self.assertIn('not obtained',r['puromycin']['limitations'])
        self.assertEqual(r['penguins']['license'],'CC0-1.0')

    def test_rejected_acquisitions_absent_from_registry(self):
        r=json.loads((ROOT/'data/v0.2.0/registry.json').read_text())
        paths={a['path'].split('/')[-1] for s in r['sources'].values() for a in s['artifacts']}
        self.assertFalse(paths&{'CO2.csv','CO2_plant.csv','nist_bio001.xml','nist_Cp.xml','pressure.R'})
        headers=(ROOT/'data/v0.2.0/sources/CO2_plants_extracted.csv').read_text().splitlines()[0]
        self.assertEqual(headers,'Plant,Type,Treatment,conc,uptake')

    def test_corrupt_numeric_reference_detected(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'results/local') as tmp:
            dest=Path(tmp);shutil.copytree(ROOT/'data/v0.2.0',dest/'data/v0.2.0')
            path=dest/'data/v0.2.0/cases.json';cases=json.loads(path.read_text())
            c=next(x for x in cases if x['id']=='CO03P')
            c['reference']['numeric_check']['expected']['chilled']='557/30'
            path.write_text(json.dumps(cases))
            with self.assertRaisesRegex(ValueError,'numeric witness mismatch:CO03P'):validate(dest)

    def test_corrupt_source_detected_even_with_plausible_values(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'results/local') as tmp:
            dest=Path(tmp);shutil.copytree(ROOT/'data/v0.2.0',dest/'data/v0.2.0')
            p=dest/'data/v0.2.0/sources/Puromycin_extracted.csv'
            p.write_text(p.read_text().replace('0.02,76,treated','0.02,77,treated'))
            with self.assertRaisesRegex(ValueError,'source hash mismatch'):validate(dest)

    def test_original_serialized_and_text_cells_match_extractions(self):
        out=verify_source_transformations(ROOT)
        self.assertEqual(out,{'Puromycin_cells':69,'CO2_numeric_cells':168,'FreeSolv_rows':6})

if __name__=='__main__':unittest.main()
