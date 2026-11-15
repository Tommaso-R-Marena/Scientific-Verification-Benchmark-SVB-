"""Replay recorded diagnostics without importing/running PCS or assuming expert review."""
import importlib.util,json,sys,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'research/pcs-assurance-v1'
spec=importlib.util.spec_from_file_location('assurance_analysis',D/'analyze.py');A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
class Assurance(unittest.TestCase):
 def test_independent_primary_references_match_actual_theorems(self):
  r=A.analyze();self.assertEqual(r['primary']['primary_theorem_checks'],17);self.assertEqual(r['primary']['kernel_decided_primary_n'],16)
 def test_reference_defect_not_hidden_or_scored_as_subject_failure(self):
  r=A.analyze();self.assertEqual(r['primary']['scheduled_n'],18);self.assertEqual(r['primary']['reference_eligible_n'],17)
  self.assertEqual(next(x for x in r['rows'] if x['id']=='S02')['reference_status'],'defective_reference_preserved')
 def test_deferral_is_neither_scientific_acceptance_nor_execution_failure(self):
  r=A.analyze();self.assertEqual(r['primary']['execution_statuses'],{'completed':18});self.assertEqual(r['primary']['outward_counts']['REQUIRE_HUMAN_REVIEW'],9)
  self.assertEqual(r['primary']['scientific_not_assessed'],18)
 def test_metamorphic_arithmetic_preserved_and_no_injection_effect(self):
  r=A.analyze();self.assertTrue(all(x['mathematical_match_invariance'] for x in r['metamorphic']));self.assertFalse(any(x['tripwire_created'] for x in r['rows']))
 def test_scope_tradeoff_keeps_false_binding_visible(self):
  r=A.analyze()['primary'];self.assertEqual(r['supported_confirmation'],6);self.assertEqual(r['unsupported_reading_confirmation'],1)
 def test_known_proof_runner_forgery_and_existing_guard(self):
  rows=json.loads((D/'results/supplemental_probes.json').read_text())['rows']
  self.assertTrue(next(x['report']['accepted'] for x in rows if x['id']=='forgery_newline_original_v11'))
  self.assertFalse(next(x['report']['accepted'] for x in rows if x['id']=='forgery_newline_existing_candidate_v2'))
 def test_genuine_and_self_redigested_false_receipt_replays(self):
  rs=json.loads((D/'results/replay_probes.json').read_text());self.assertEqual([x['execution']['returncode'] for x in rs],[0,1])
  self.assertTrue(json.loads(rs[0]['execution']['stdout'])['proofs_rechecked_by_the_lean_kernel'])
 def test_explicit_convention_allows_positive_discrepancy_control(self):
  r=json.loads((D/'results/assumption_probe.json').read_text());self.assertEqual(r['records'][0]['outward']['verdict'],'DISCREPANCY_FOR_REVIEW')
 def test_scope_proof_actually_executed_without_axioms(self):
  r=json.loads((D/'results/scope_proof.json').read_text());self.assertEqual(r['returncode'],0);self.assertEqual(r['stdout'].count('does not depend on any axioms'),2)
 def test_supplemental_context_compatible_with_frozen_phase3_ingestion(self):
  from svb.adjudication import validate_context
  x=json.loads((D/'review/coordinator_context.json').read_text());p,c=validate_context(x);self.assertEqual((len(p),len(c)),(6,6))
  f=json.loads((D/'review/blank_reference_form.json').read_text());self.assertIsNone(f['origin']);self.assertIsNone(f['declaration']['human_attestation'])
if __name__=='__main__':unittest.main()
