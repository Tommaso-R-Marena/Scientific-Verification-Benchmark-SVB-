"""SOFTWARE FIXTURES ONLY: no synthetic record represents a human review."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from svb.adjudication import (VERSION, Invalid, digest_json, validate_context, validate_submission,
    analyze, nominal_kappa, load_file)


def context():
    packets=[]
    for i in range(1,5):
        p={'packet_id':f'P{i:02d}','claim':'A fixed claim.', 'documents':[{'id':'DOC','text':'A measured value is 2.'}]}
        packets.append({'packet_id':p['packet_id'],'packet_sha256':digest_json(p),'packet':p,'source_family':'one_study'})
    c={'candidate_id':'C01','packet_id':'P01','raw_response':'This is an explicit SOFTWARE TEST FIXTURE.','generation_status':'completed'}
    c['candidate_sha256']=digest_json(c)
    return {'schema_version':VERSION,'pilot_id':'TEST_FIXTURE_ONLY','packets':packets,'candidates':[c]}


def registry(ctx):
    return {'schema_version':VERSION,'pilot_id':ctx['pilot_id'],'coordinator_attestation':True,
        'reference_round1_locked':False,'reviewers':[
        {'reviewer_code':c,'role':r,'human_origin_attested':True,'credentials_checked':True,'independence_checked':True,
         'consent_to_process':True,'reference_assignments':[p['packet_id'] for p in ctx['packets']], 'candidate_assignments':['C01']}
        for c,r in [('TEST_A','domain'),('TEST_B','methods')]]}


def form(ctx,code='TEST_A',labels=None):
    labels=labels or ['empirically_supported']*4
    js=[]
    for p,l in zip(ctx['packets'],labels):
        ls=[l] if isinstance(l,str) else l
        js.append({'packet_id':p['packet_id'],'packet_sha256':p['packet_sha256'],'assessment_status':'completed',
            'reviewer_uncertainty':'moderate','rationale':'SOFTWARE FIXTURE: exercise source checking.',
            'citations':[{'document_id':'DOC','locator':'sentence 1','quotation':'value is 2'}],
            'legacy_labels':ls,'category_relation':'single_defensible' if len(ls)==1 else 'simultaneously_applicable' if ls else 'none_fit',
            'evidence_relation':'support_only','supported_scope':'The supplied table only.','missing_assumptions':[],
            'uncertainty_explanation':'No measurement model given.','issues':[],'proposed_disposition':'retain','proposed_revision':None})
    return {'schema_version':VERSION,'pilot_id':ctx['pilot_id'],'origin':'software_test_fixture','stage':'reference','round':1,
        'reviewer_code':code,'prior_form_sha256':None,'tools_and_external_sources':[],
        'declaration':{'human_attestation':False,'independent_work':True,'saw_other_reviews':False,'source_exposure':'none',
           'author_label_exposure':'none','candidate_identity_exposure':'uncertain','conflicts':'TEST FIXTURE none','expertise_scope':'Software testing only.'},'judgments':js}


class Ingestion(unittest.TestCase):
    def setUp(self):self.ctx=context();self.reg=registry(self.ctx);self.f=form(self.ctx)
    def check(self,f=None):return validate_submission(f or self.f,self.reg,self.ctx,allow_test_fixtures=True)
    def rejected(self,mutate):
        f=deepcopy(self.f);mutate(f)
        with self.assertRaises(Invalid):self.check(f)
    def test_production_rejects_software_fixtures(self):
        with self.assertRaisesRegex(Invalid,'human-origin'):validate_submission(self.f,self.reg,self.ctx)
    def test_fixture_analysis_is_watermarked_zero_humans(self):
        r=analyze([self.f],self.reg,self.ctx,allow_test_fixtures=True)
        self.assertEqual(r['analysis_kind'],'SOFTWARE_FIXTURE_NOT_HUMAN_REVIEW');self.assertEqual(r['human_judgments_submitted'],0)
        self.assertFalse(r['automatic_gold_created'])
    def test_hash_bound_context_and_judgment(self):
        self.rejected(lambda f:f['judgments'][0].update(packet_sha256='0'*64))
        bad=deepcopy(self.ctx);bad['packets'][0]['packet']['claim']='changed'
        with self.assertRaises(Invalid):validate_context(bad)
    def test_duplicate_foreign_or_out_of_assignment_cases(self):
        self.rejected(lambda f:f['judgments'].append(deepcopy(f['judgments'][0])))
        self.rejected(lambda f:f['judgments'][0].update(packet_id='FOREIGN'))
        self.reg['reviewers'][0]['reference_assignments']=[]
        with self.assertRaises(Invalid):self.check()
    def test_citations_are_supplied_and_exact_when_quoted(self):
        self.rejected(lambda f:f['judgments'][0]['citations'][0].update(document_id='FABRICATED'))
        self.rejected(lambda f:f['judgments'][0]['citations'][0].update(quotation='value is 3'))
        self.rejected(lambda f:f['judgments'][0].update(citations=[]))
    def test_multiple_categories_and_none_fit_are_preserved(self):
        f=form(self.ctx,labels=[['computationally_established','empirically_supported'],[],'refuted','insufficient_evidence'])
        self.check(f)
        r=analyze([f],self.reg,self.ctx,allow_test_fixtures=True)
        self.assertEqual(r['validated_forms'][0]['judgments'][0]['legacy_labels'],f['judgments'][0]['legacy_labels'])
        self.assertEqual(r['validated_forms'][0]['judgments'][1]['category_relation'],'none_fit')
    def test_alternative_interpretations_distinct_from_simultaneous(self):
        f=form(self.ctx,labels=[['computationally_established','empirically_supported']]*4)
        f['judgments'][0]['category_relation']='alternative_interpretations';self.check(f)
        self.assertNotEqual(f['judgments'][0]['category_relation'],f['judgments'][1]['category_relation'])
    def test_inconsistent_sets_or_duplicate_labels_rejected(self):
        self.rejected(lambda f:f['judgments'][0].update(legacy_labels=['refuted','refuted']))
        self.rejected(lambda f:f['judgments'][0].update(category_relation='none_fit'))
        self.rejected(lambda f:f['judgments'][0].update(legacy_labels=['refuted','insufficient_evidence']))
    def test_missing_and_unassessable_distinct(self):
        f=deepcopy(self.f);f['judgments']=f['judgments'][:1]
        j=f['judgments'][0];j.update(assessment_status='unable_to_assess',legacy_labels=[],category_relation='not_assessable',evidence_relation='not_assessable',citations=[],proposed_disposition='unable_to_assess')
        r=analyze([f],self.reg,self.ctx,allow_test_fixtures=True)
        c=r['coverage'][0];self.assertEqual((c['assigned'],c['submitted'],c['completed'],c['unable_to_assess'],c['missing_assignments']),(8,1,0,1,7))
    def test_unassessable_cannot_carry_reference_verdict(self):
        self.rejected(lambda f:f['judgments'][0].update(assessment_status='unable_to_assess'))
    def test_reference_error_allegations_never_become_corrections(self):
        f=deepcopy(self.f);f['judgments'][0].update(issues=['reference_error_suspected','irreconcilable_interpretation'],proposed_disposition='reference_correction_proposed')
        r=analyze([f],self.reg,self.ctx,allow_test_fixtures=True);j=r['items'][0]
        self.assertEqual(j['reference_error_status'],'alleged_requires_independent_check');self.assertFalse(j['automatic_reference_revision'])
        self.assertTrue(j['irreconcilable_ambiguity_reported'])
    def test_unfounded_correction_disposition_rejected(self):
        self.rejected(lambda f:f['judgments'][0].update(proposed_disposition='reference_correction_proposed'))
    def test_registry_checks_consent_role_duplicates_and_identity(self):
        for k,value in [('consent_to_process',False),('human_origin_attested',None),('role','AI'),('reviewer_code','name@example.org')]:
            r=deepcopy(self.reg);r['reviewers'][0][k]=value
            with self.assertRaises(Invalid):validate_submission(self.f,r,self.ctx,allow_test_fixtures=True)
        r=deepcopy(self.reg);r['reviewers'].append(deepcopy(r['reviewers'][0]))
        with self.assertRaises(Invalid):analyze([],r,self.ctx)
    def test_first_round_cannot_be_post_discussion(self):
        self.rejected(lambda f:f['declaration'].update(saw_other_reviews=True))
        self.rejected(lambda f:f['declaration'].update(independent_work=False))
    def test_origin_and_human_attestation_must_match(self):
        self.rejected(lambda f:f['declaration'].update(human_attestation=True))
    def test_duplicate_forms_refused_instead_of_overwrite(self):
        with self.assertRaises(Invalid):analyze([self.f,self.f],self.reg,self.ctx,allow_test_fixtures=True)
    def test_linked_second_round_retains_first(self):
        f2=deepcopy(self.f);f2.update(round=2,prior_form_sha256=digest_json(self.f));f2['judgments'][0]['legacy_labels']=['refuted']
        f2['declaration'].update(independent_work=False,saw_other_reviews=True)
        r=analyze([self.f,f2],self.reg,self.ctx,allow_test_fixtures=True)
        self.assertEqual(len(r['validated_forms']),2);self.assertEqual(r['validated_forms'][0]['judgments'][0]['legacy_labels'],['empirically_supported'])
        f2['prior_form_sha256']='0'*64
        with self.assertRaises(Invalid):analyze([self.f,f2],self.reg,self.ctx,allow_test_fixtures=True)
    def test_round_two_cannot_introduce_new_cases_or_link_another_reviewer(self):
        f=deepcopy(self.f);f['judgments']=f['judgments'][:1]
        f2=deepcopy(self.f);f2.update(round=2,prior_form_sha256=digest_json(f))
        with self.assertRaises(Invalid):analyze([f,f2],self.reg,self.ctx,allow_test_fixtures=True)
        f2=deepcopy(f);f2.update(round=2,reviewer_code='TEST_B',prior_form_sha256=digest_json(f))
        with self.assertRaises(Invalid):analyze([f,f2],self.reg,self.ctx,allow_test_fixtures=True)
    def candidate(self):
        f=deepcopy(self.f);f['stage']='candidate';c=self.ctx['candidates'][0];j=f['judgments'][0]
        f['judgments']=[{k:j[k] for k in ('packet_id','packet_sha256','assessment_status','reviewer_uncertainty','rationale','citations')}]
        f['judgments'][0].update(candidate_id=c['candidate_id'],candidate_sha256=c['candidate_sha256'],reasoning_validity='invalid',attribution_validity='missing',scope_handling='inadequate',uncertainty_handling='inadequate')
        return f
    def test_candidate_ratings_require_reference_lock_and_raw_identity(self):
        f=self.candidate()
        with self.assertRaises(Invalid):self.check(f)
        self.reg['reference_round1_locked']=True;self.check(f)
        r=analyze([f],self.reg,self.ctx,allow_test_fixtures=True);self.assertEqual(r['coverage'][2]['completed'],1)
        f['judgments'][0]['candidate_sha256']='0'*64
        with self.assertRaises(Invalid):self.check(f)
    def test_partial_roles_are_reported_without_population_claims(self):
        r=analyze([self.f],self.reg,self.ctx,allow_test_fixtures=True)
        self.assertEqual(r['source_family_counts'],{'one_study':4});self.assertEqual(r['pairwise'][0]['joint_completed'],0)
        self.assertEqual(r['planned_reference_role_slots'],12)
        self.assertEqual(sum(x['unassigned_minimum_role_slots'] for x in r['registered_reference_role_coverage']),4)
    def test_json_duplicate_keys_nonfinite_or_oversize_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'review.json'
            for data in ['{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}']:
                p.write_text(data)
                with self.assertRaises(Invalid):load_file(p)
            p.write_bytes(b' '*(2*1024*1024+1))
            with self.assertRaises(Invalid):load_file(p)


class Agreement(unittest.TestCase):
    def test_kappa_matches_hand_calculation(self):
        # 3/4 agree; both marginals half each; (0.75-0.5)/(1-0.5)=0.5.
        r=nominal_kappa(['a','a','b','b'],['a','b','b','b'])
        # Marginals .5/.5 and .25/.75 still give Pe=.5.
        self.assertEqual(r['observed_agreement'],.75);self.assertEqual(r['expected_agreement'],.5);self.assertEqual(r['kappa'],.5)
    def test_degenerate_and_missing_kappa_are_null(self):
        self.assertIsNone(nominal_kappa([],[])['kappa']);self.assertIsNone(nominal_kappa(['a']*3,['a']*3)['kappa'])
        with self.assertRaises(Invalid):nominal_kappa(['a'],[])
    def test_disagreement_can_have_negative_kappa(self):
        self.assertEqual(nominal_kappa(['a','b'],['b','a'])['kappa'],-1)
    def test_set_agreement_singleton_selection_and_jaccard_denominators(self):
        ctx=context();reg=registry(ctx)
        a=form(ctx,labels=[['computationally_established','empirically_supported'],[],'refuted','refuted'])
        b=form(ctx,'TEST_B',labels=[['computationally_established'],[],'refuted','insufficient_evidence'])
        r=analyze([a,b],reg,ctx,allow_test_fixtures=True)['pairwise'][0]
        self.assertEqual(r['exact_set_agreement'],.5);self.assertEqual(r['jaccard_n'],3)
        self.assertEqual(r['mean_jaccard_nonempty_union'],.5);self.assertEqual(r['jaccard_empty_union_excluded'],1)
        self.assertEqual(r['singleton_only_legacy_kappa']['n'],2);self.assertEqual(r['singleton_selection_excluded'],2)

if __name__=='__main__':unittest.main()
