"""Small supplemental packet reuses Phase III forms; no contacts or ratings."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[2];D=Path(__file__).parent
sys.path.insert(0,str(R/'src'));sys.path.insert(0,str(R/'scripts'))
from svb.adjudication import digest_json,validate_context
from build_phase3_pilot import blank_form
cs={c['id']:c for c in json.loads((D/'cases.json').read_text())};runs={r['id']:r for r in json.loads((D/'results/runs.json').read_text())}
sup=next(r for r in json.loads((D/'results/supplemental_probes.json').read_text())['rows'] if r['id']=='S05b')
context={'schema_version':'0.4.0-proposal','pilot_id':'svb-pcs-assurance-supplement-1','packets':[],'candidates':[]}
for i,cid in enumerate(['S01','S05b','S06','S08','P01','P02'],1):
 x=sup['input'] if cid=='S05b' else cs[cid]['input'];pid=f'PCS{i:02d}'
 docs=[{'id':'SENTENCE','source_id':cid,'title':'Authored diagnostic source sentence, not a paper quotation','text':x['source']},{'id':'TABLE','source_id':cid,'title':'Exact supplied CSV bytes','text':x['csv']},{'id':'MANIFEST','source_id':cid,'title':'Submitter-supplied vocabulary and byte pin; not an independent scientific authority','text':json.dumps(x['manifest'],sort_keys=True)}]
 if cid=='S06':docs.append({'id':'CUSTODY','source_id':cid,'title':'Synthetic construction provenance','text':'The supplied rows are juveniles. The sentence targets adults. This extra custody fact was not supplied to PCS and is not established by its receipt.'})
 packet={'packet_id':pid,'claim':x['source'],'question':'What do the exact computation, reading and scientific interpretation respectively establish? Challenge any unsupported target or category.','documents':docs,'methodology':'Separate finite arithmetic, literal source association, custody and empirical inference. Public-data sentences are SVB authored, not alleged errors in publications.','assumptions':['Displayed decimals are exact computational inputs, not physically exact measurements.']}
 context['packets'].append({'packet_id':pid,'packet_sha256':digest_json(packet),'packet':packet,'source_family':'public_oxygen' if cid.startswith('P') else 'synthetic_diagnostics'})
 rec=next(r for r in (sup['records'] if cid=='S05b' else runs[cid]['records']) if not r['auxiliary'])
 c={'candidate_id':f'RECEIPT{i:02d}','packet_id':pid,'raw_response':json.dumps(rec,sort_keys=True,indent=2),'generation_status':'actual_PCS_machine_receipt_not_model_prose'};c['candidate_sha256']=digest_json(c);context['candidates'].append(c)
validate_context(context);out=D/'review';out.mkdir(exist_ok=True)
for name,x in [('coordinator_context.json',context),('reference_packets.json',[p['packet'] for p in context['packets']]),('candidate_receipts.json',context['candidates']),('blank_reference_form.json',blank_form(context,'reference')),('blank_candidate_form.json',blank_form(context,'candidate'))]:
 (out/name).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
print('Prepared six supplementary packets; reused Phase III forms; no human reviews.')
