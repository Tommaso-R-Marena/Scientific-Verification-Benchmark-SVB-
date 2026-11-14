"""Semantic software checks; illustrative examples are not scientific reviews."""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import json
import unittest
from svb.core import Invalid,LABELS,ACCEPT
from svb.taxonomy import relation_name,validate_assessment,false_acceptance_bounds,FIELDS
ROOT=Path(__file__).resolve().parents[1]

class Taxonomy(unittest.TestCase):
 def setUp(self):self.examples=json.loads((ROOT/'data/v0.4.0/taxonomy_examples.json').read_text())
 def test_reference_illustrations_validate_without_relabeling_old_cases(self):
  for x in self.examples:self.assertEqual(validate_assessment(x['assessment']),x['assessment'])
 def test_all_four_relations_and_unassessed_are_distinct(self):
  names={relation_name({'support':a,'opposition':b,'assessed':True}) for a in [False,True] for b in [False,True]}
  self.assertEqual(names,{'neither','support_only','opposition_only','both'})
  self.assertEqual(relation_name({'support':False,'opposition':False,'assessed':False}),'unassessed')
 def test_flags_are_booleans_and_unassessed_cannot_assert_support(self):
  for r in [{'support':1,'opposition':False,'assessed':True},{'support':True,'opposition':False,'assessed':False}]:
   with self.assertRaises(Invalid):relation_name(r)
 def test_passed_arithmetic_does_not_imply_target_support(self):
  x=next(e['assessment'] for e in self.examples if e['historical_case']=='CW02S')
  self.assertEqual(x['computational_check']['status'],'passed');self.assertEqual(relation_name(x['relation']),'neither')
 def test_source_fact_can_have_multiple_justification_types(self):
  x=self.examples[0]['assessment'];self.assertIn('computational',x['justification_types']);self.assertIn('observational',x['justification_types'])
 def test_strength_without_domain_rubric_or_false_documented_dispute_rejected(self):
  for change in ['strength','dispute','machine']:
   x=deepcopy(self.examples[0]['assessment'])
   if change=='strength':x['evidence_strength']['value']='high'
   if change=='dispute':x['research_dispute']['status']='documented'
   if change=='machine':x['computational_check']['status']='not_checked'
   with self.assertRaises(Invalid):validate_assessment(x)
 def test_structural_schema_matches_runtime_top_level_fields(self):
  s=json.loads((ROOT/'schemas/v0.4.0/evidence_assessment.schema.json').read_text())
  self.assertEqual(set(s['properties']),FIELDS);self.assertFalse(s['additionalProperties'])
 def test_all_nonempty_label_subsets_with_fixed_acceptance_membership_are_invariant(self):
  for n in range(1,7):
   for labels in combinations(LABELS,n):
    if len({l in ACCEPT for l in labels})==1:
     for pred in LABELS:
      r=false_acceptance_bounds(pred,list(labels));self.assertEqual(r['lower'],r['upper'])
 def test_cross_boundary_references_yield_bounds_not_new_gold(self):
  self.assertEqual(false_acceptance_bounds('empirically_supported',['empirically_supported','insufficient_evidence']),{'lower':0,'upper':1,'reference_unresolved':False})
  self.assertEqual(false_acceptance_bounds('refuted',['empirically_supported','insufficient_evidence'])['upper'],0)
 def test_empty_or_malformed_reference_is_not_safe_acceptance(self):
  self.assertIsNone(false_acceptance_bounds('empirically_supported',[])['lower'])
  with self.assertRaises(Invalid):false_acceptance_bounds('fixed by parser',['refuted'])
  with self.assertRaises(Invalid):false_acceptance_bounds('refuted',['unknown'])
if __name__=='__main__':unittest.main()
