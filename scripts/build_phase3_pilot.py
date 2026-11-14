"""Build a small answer-filtered pilot. No blinding or human review is asserted."""
from __future__ import annotations
import argparse
from copy import deepcopy
from pathlib import Path
import random
import sys
import json
from svb.core import read, canonical, Invalid
from svb.adjudication import VERSION, digest_json, digest_bytes, DECLARATION_KEYS, validate_context
from svb.phase2 import public_id
from build_phase2b_review import scientific_sources, deterministic_zip, json_bytes, packet

ROOT=Path(__file__).resolve().parents[1]


def blank_form(context, stage):
    declaration={k:None for k in DECLARATION_KEYS}
    declaration['conflicts']='';declaration['expertise_scope']=''
    judgments=[]
    items=context['packets'] if stage=='reference' else context['candidates']
    byid={p['packet_id']:p for p in context['packets']}
    for item in items:
        pid=item['packet_id'];j={'packet_id':pid,'packet_sha256':byid[pid]['packet_sha256'],
            'assessment_status':None,'reviewer_uncertainty':None,'rationale':'','citations':[]}
        if stage=='reference':
            j.update(legacy_labels=[],category_relation=None,evidence_relation=None,supported_scope='',missing_assumptions=[],
                uncertainty_explanation='',issues=[],proposed_disposition=None,proposed_revision=None)
        else:
            j.update(candidate_id=item['candidate_id'],candidate_sha256=item['candidate_sha256'],
                reasoning_validity=None,attribution_validity=None,scope_handling=None,uncertainty_handling=None)
        judgments.append(j)
    return {'schema_version':VERSION,'pilot_id':context['pilot_id'],'origin':None,'stage':stage,'round':1,
        'reviewer_code':None,'declaration':declaration,'prior_form_sha256':None,'tools_and_external_sources':[],'judgments':judgments}


def build(root=ROOT):
    selection=read(root/'data/v0.4.0/pilot_selection.json')
    all_cases=[*read(root/'data/v0.2.0/cases.json'),*read(root/'data/v0.3.0/cases.json')]
    byid={c['id']:c for c in all_cases};ids=selection['case_ids']
    if len(ids)!=12 or len(set(ids))!=len(ids) or not set(ids)<=set(byid):raise Invalid('invalid fixed pilot selection')
    chosen=[byid[c] for c in ids];random.Random(selection['packet_order_seed']).shuffle(chosen)
    context={'schema_version':VERSION,'pilot_id':selection['pilot_id'],'packets':[],'candidates':[]};mapping={};public_packets=[]
    for i,c in enumerate(chosen,1):
        pid=f'P{i:02d}';p=packet(c);p.pop('public_id');p={'packet_id':pid,**p};public_packets.append(p)
        context['packets'].append({'packet_id':pid,'packet_sha256':digest_json(p),'packet':p,'source_family':c['family']})
        mapping[public_id(c)]={'packet_id':pid,'case_id':c['id']}
    raw=[]
    for key in ('qwen-0.5b','qwen-1.5b'):
        p=root/f'results/v0.3.0/evaluation/{key}_unconstrained.jsonl'
        for r in p.read_text().splitlines():
            row=json.loads(r)
            if row['task']=='B' and row['condition']=='evidence' and row['id'] in mapping:
                raw.append({'packet_id':mapping[row['id']]['packet_id'],'raw_response':row['raw_text'],'generation_status':row['status']})
    if len(raw)!=12:raise Invalid('expected exactly twelve retained B candidates, no fixtures or repairs')
    random.Random(selection['packet_order_seed']+1).shuffle(raw)
    for i,c in enumerate(raw,1):
        c={'candidate_id':f'C{i:02d}',**c};c['candidate_sha256']=digest_json(c);context['candidates'].append(c)
    validate_context(context)
    source_ids={d['source_id'] for p in public_packets for d in p['documents']}
    registry,sources=scientific_sources([read(root/'data/v0.2.0/registry.json'),read(root/'data/v0.3.0/registry.json')],source_ids,root)
    source_files={**sources,'source_registry.json':json_bytes(registry)}
    source_zip=deterministic_zip(source_files);source_ref={'archive':'source_materials.zip','sha256':digest_bytes(source_zip),'required_for_both_review_stages':True,'archived_primary_methods_may_be_incomplete':True}
    guide=(root/'docs/phase-iii/reviewer_guide.md').read_bytes()
    common={'reviewer_guide.md':guide,'source_bundle.json':json_bytes(source_ref),'response_form.md':(root/'docs/phase-iii/response_form.md').read_bytes()}
    ref={**common,'packets.json':json_bytes(public_packets),'blank_response.json':json_bytes(blank_form(context,'reference'))}
    cand={**common,'packets.json':json_bytes(public_packets),'candidates.json':json_bytes(context['candidates']),'blank_response.json':json_bytes(blank_form(context,'candidate'))}
    for files in (ref,cand):
        files['manifest.json']=json_bytes({'schema_version':VERSION,'pilot_id':selection['pilot_id'],'human_reviews_completed':0,'actual_blinding_established':False,'protected_holdout':False,'files':{n:digest_bytes(b) for n,b in sorted(files.items())}})
    archives={'reference_review.zip':deterministic_zip(ref),'candidate_review.zip':deterministic_zip(cand),'source_materials.zip':source_zip}
    coordinator={'schema_version':VERSION,'pilot_id':selection['pilot_id'],'coordinator_attestation':None,'reference_round1_locked':False,'reviewers':[]}
    coordinator['reviewers']=[{'reviewer_code':None,'role':None,'human_origin_attested':None,'credentials_checked':None,'independence_checked':None,'consent_to_process':None,'reference_assignments':[],'candidate_assignments':[]}]
    return archives,context,coordinator,{'case_mapping':mapping,'review_status':'prepared_not_distributed','human_reviews_completed':0,'candidate_identity_policy':'No provider metadata exported; prose not redacted. Public files can reveal identity; coordinator must check cues and use neutral distribution paths.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'data/v0.4.0/pilot');a=p.parse_args()
    dest=a.output.resolve()
    if not dest.is_relative_to(ROOT) or dest.exists():p.exit(2,'new output directory inside SVB required; refusing overwrite\n')
    archives,context,registry,coord=build();dest.mkdir(parents=True)
    for name,b in archives.items():(dest/name).write_bytes(b)
    for name,value in [('coordinator_context.json',context),('registry_template.json',registry),('preparation_record.json',coord)]:
        (dest/name).write_bytes(json_bytes(value))
    manifest={'schema_version':VERSION,'human_reviews_completed':0,'reviewers_contacted':0,'reference_packets':12,'candidate_responses':12,
        'files':{p.name:digest_bytes(p.read_bytes()) for p in sorted(dest.iterdir())}}
    (dest/'manifest.json').write_bytes(json_bytes(manifest));print(json.dumps({'output':str(dest),'reference_packets':12,'raw_candidates':12,'human_reviews':0}))
if __name__=='__main__':main()
