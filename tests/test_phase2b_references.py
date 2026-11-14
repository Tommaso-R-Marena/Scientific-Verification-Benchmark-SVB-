"""New study-family reference checks;no historical frozen artifact writes."""
from __future__ import annotations
from collections import Counter
from decimal import Decimal
from fractions import Fraction
import csv
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from svb.phase2b_references import source_rows,recompute,validate,verify_transformations

class PhaseIIbReferences(unittest.TestCase):
    def cases(self,root=ROOT):return json.loads((root/'data/v0.3.0/cases.json').read_text())

    def test_all_source_hashes_transformations_and_nine_numeric_witnesses(self):
        r=validate(ROOT)
        self.assertTrue(r['source_hashes_valid'])
        self.assertEqual(r['numeric_witnesses_checked'],9)
        self.assertEqual(r['transformations']['chick_growth']['rows'],578)
        self.assertFalse(r['original_laboratory_execution_verified'])
        self.assertFalse(r['external_human_adjudication'])

    def test_twelve_cases_six_pairs_three_new_studies(self):
        cases=self.cases()
        self.assertEqual(len(cases),12)
        self.assertEqual(Counter(c['family'] for c in cases),{'sleep':4,'chick_growth':4,'oxygen_demand':4})
        self.assertEqual(set(Counter(c['pair']['id'] for c in cases).values()),{2})
        self.assertEqual({c['split'] for c in cases},{'evaluation'})
        old=json.loads((ROOT/'data/v0.2.0/cases.json').read_text())
        self.assertFalse({c['family'] for c in cases}&{c['family'] for c in old})
        self.assertEqual(Counter(c['reference']['label'] for c in cases),{'computationally_established':3,'empirically_supported':3,'refuted':3,'insufficient_evidence':3})

    def test_source_documents_have_no_reference_metadata_or_missing_checklist(self):
        for c in self.cases():
            p=c['packet']
            self.assertEqual(set(p),{'question','claim','documents','methodology','assumptions'})
            self.assertEqual(c['reference']['status'],'provisional_author_adjudicated')
            text=json.dumps(p)
            for token in ('numeric_check','condition_labels','reasoning_requirements','insufficient_evidence','no clinical endpoints','No correlation matrix'):
                self.assertNotIn(token,text)
            self.assertTrue(set(c['reference']['evidence_ids'])<=set(d['id'] for d in p['documents']))

    def test_no_evidence_is_a_justification_reference_not_factual_memory(self):
        for c in self.cases():
            r=c['reference']
            self.assertEqual(r['condition_labels']['no_evidence'],'insufficient_evidence')
            self.assertEqual(r['condition_scopes']['no_evidence'],[])
            for condition in ('evidence','no_assumptions','verified_numbers','paraphrase'):
                self.assertEqual(r['condition_labels'][condition],r['label'])

    def test_official_license_not_inferred_from_project_license(self):
        reg=json.loads((ROOT/'data/v0.3.0/registry.json').read_text())
        for source in reg['sources'].values():
            self.assertEqual(source['license'],'GPL-2.0-or-later')
            self.assertIn('secondary',source['limitations'])
            self.assertIn('not independently obtained',source['limitations'])
            text=(ROOT/'data/v0.3.0/sources'/source['license_evidence'][0]).read_text()
            self.assertIn('Distributed under GPL 2 or later',text)
            self.assertIn(source['upstream_commit'],source['url'])

    def test_sleep_decimal_recalculation_from_raw_source(self):
        # Independent Decimal/lexical route verifies exact-Fraction parser output.
        raw=(ROOT/'data/v0.3.0/sources/sleep.R').read_text()
        literal=raw.split('extra = c(',1)[1].split(')',1)[0]
        x=[Decimal(v.strip()) for v in literal.split(',')]
        differences=[b-a for a,b in zip(x[:10],x[10:])]
        self.assertEqual(sum(differences),Decimal('15.8'))
        self.assertEqual(sum(differences)/10,Decimal('1.58'))
        self.assertEqual((sum(d>0 for d in differences),sum(d==0 for d in differences)),(9,1))
        self.assertEqual(recompute('sleep_paired_mean',ROOT)['mean_difference_hours'],'79/50')

    def test_chick_factor_codes_are_not_identifier_labels(self):
        rows=source_rows(ROOT)['chick_growth']
        # Source ordered factor begins code15,but its label is1.
        self.assertEqual(rows[0],{'weight':'42','Time':'0','Chick':'1','Diet':'1'})
        first=next(r for r in rows if r['Chick']=='1' and r['Time']=='21')
        self.assertEqual(first['weight'],'205')
        self.assertEqual(len({r['Chick'] for r in rows}),50)
        self.assertEqual(recompute('chick_one_growth',ROOT)['observed_gain_g'],'163')

    def test_chick_means_independent_grouped_integer_sums(self):
        # Work directly on simple source weight/time/diet vectors without source_rows.
        text=(ROOT/'data/v0.3.0/sources/ChickWeight.R').read_text()
        def literal(name):
            m=re.search(r'\b'+name+r'\s*=\s*(?:factor\()?c\(([^()]*)\)',text,re.S)
            return [int(x.strip()) for x in m[1].split(',')]
        w,t,d=literal('weight'),literal('Time'),literal('Diet')
        diet1=[v for v,age,diet in zip(w,t,d) if age==21 and diet==1]
        diet4=[v for v,age,diet in zip(w,t,d) if age==21 and diet==4]
        self.assertEqual((len(diet1),sum(diet1),len(diet4),sum(diet4)),(16,2844,9,2147))
        self.assertEqual(Fraction(sum(diet4),len(diet4))-Fraction(sum(diet1),len(diet1)),Fraction(2189,36))

    def test_bod_conversion_not_only_subtraction(self):
        x=recompute('oxygen_change',ROOT)
        self.assertEqual(x['difference_mg_per_L'],'23/2')
        self.assertEqual(x['difference_g_per_L'],'23/2000')
        self.assertEqual(Fraction(x['difference_mg_per_L'])/Fraction(x['difference_g_per_L']),1000)
        self.assertTrue(recompute('oxygen_nonmonotone',ROOT)['nonmonotone'])

    def test_wrong_numeric_reference_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'results/local') as temp:
            target=Path(temp);shutil.copytree(ROOT/'data/v0.3.0',target/'data/v0.3.0')
            p=target/'data/v0.3.0/cases.json';cs=json.loads(p.read_text())
            cs[0]['reference']['numeric_check']['expected']['mean_difference_hours']='79/25'
            p.write_text(json.dumps(cs))
            with self.assertRaisesRegex(ValueError,'numeric witness mismatch:SL01P'):validate(target)

    def test_source_cell_corruption_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'results/local') as temp:
            target=Path(temp);shutil.copytree(ROOT/'data/v0.3.0',target/'data/v0.3.0')
            p=target/'data/v0.3.0/sources/BOD.R';p.write_text(p.read_text().replace('19.8','29.8'))
            with self.assertRaisesRegex(ValueError,'source hash mismatch'):validate(target)

    def test_transform_corruption_detected_separately_from_hash(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'results/local') as temp:
            target=Path(temp);shutil.copytree(ROOT/'data/v0.3.0',target/'data/v0.3.0')
            p=target/'data/v0.3.0/sources/chick_growth_extracted.csv'
            p.write_text(p.read_text().replace('42,0,1,1','42,0,15,1',1))
            with self.assertRaisesRegex(ValueError,'source transformation mismatch:chick_growth'):verify_transformations(target)

if __name__=='__main__':unittest.main()
