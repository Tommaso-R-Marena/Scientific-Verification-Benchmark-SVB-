"""Frozen IIb replay: distinct minimal verdict/prose/rich tasks, no output repair."""
from pathlib import Path
import argparse,json
from svb.core import read,ACCEPT,Invalid
from svb.phase2 import public_id,packet_view,deterministic
from svb.phase2b import validate,load_cases,run_records,score_all,score_a,write
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
validate(R)
if not a.output.resolve().is_relative_to(R):raise Invalid('output must stay inside SVB')
cs=load_cases(R);byid={public_id(c):c for c in cs};plan=read(R/'data/v0.3.0/evaluation_plan.json')
report={'version':'0.3.0','reference_status':'provisional_author_adjudicated','models':{},'baselines':{},'limits':['New to SVB study families, public sources potentially present in pretraining','No protected/blinded or expert-adjudicated test','Coarse acceptance distinct from exact taxonomy agreement','B scientific quality awaits independent human review','A-vs-C is descriptive instruction-bundle comparison; constrained-vs-unconstrained A changes decoding only','Three study families do not justify iid population inference']}
for model in plan['selected_models']:
 output={'interfaces':{}}
 for mode,groups in plan['groups'].items():
  path=R/plan['run_files'][model][mode]
  rows=run_records(path) if path.exists() else []
  allowed={(pid,g['task'],g['condition']) for g in groups for pid in g['ids']}
  if any((r.get('id'),r.get('task'),r.get('condition')) not in allowed for r in rows):raise Invalid('foreign execution in model file')
  if any(bool(r.get('constrained_a',False))!=(mode=='constrained') for r in rows):raise Invalid('decoding intervention mismatch')
  result={}
  for g in groups:
   selected=[byid[i] for i in g['ids']];rs=[r for r in rows if r['task']==g['task'] and r['condition']==g['condition']]
   result[g['task']+'_'+g['condition']]=score_all(selected,rs,g['task'],g['condition'])
   if g['task']=='C':
    result['C_by_source_family']={family:score_all([c for c in selected if c['family']==family],[r for r in rs if byid[r['id']]['family']==family],'C',g['condition']) for family in sorted({c['family'] for c in selected})}
  output['interfaces'][mode]=result
 free=output['interfaces']['unconstrained'];con=output['interfaces']['constrained']
 for mode,results in output['interfaces'].items():
  ev={r['id']:r for r in results['A_evidence']['rows']};no={r['id']:r for r in results['A_no_evidence']['rows']}
  shifts=[]
  for pid,row in ev.items():
   if row['reference'] in ACCEPT:
    shifts.append({'id':pid,'evidence_prediction':row['predicted'],'no_evidence_prediction':no[pid]['predicted'],'correct_coarse_shift':row['predicted'] in ACCEPT and no[pid]['predicted']=='insufficient_evidence','both_admitted':row['status']=='admitted' and no[pid]['status']=='admitted'})
  output.setdefault('evidence_condition_shifts',{})[mode]={'support_reference_n':len(shifts),'correct_coarse_shifts':sum(r['correct_coarse_shift'] for r in shifts),'rows':shifts}
 matchedids=next(g['ids'] for g in plan['groups']['unconstrained'] if g['task']=='C');Arows=[r for r in free['A_evidence']['rows'] if r['id'] in matchedids];C=free['C_evidence']
 output['matched_A_C']={'n':len(matchedids),'A_admitted':sum(r['status']=='admitted' for r in Arows),'A_exact_correct':sum(r['exact_correct'] for r in Arows),'C_admitted':C['summary']['statuses'].get('ok',0),'C_exact_correct':C['summary']['correct'],'not_identified_causal_schema_effect':True,'reason':'Same source cases but historical rich instructions/order/length differ from rotated minimal A; do not attribute difference solely to schema.'}
 report['models'][model]=output
for name in ('numerical','evidence_aware'):
 for condition in ('evidence','no_evidence'):
  records=[]
  for c in cs:
   packet=packet_view(c)
   if condition=='no_evidence':packet['documents']=[]
   answer=deterministic(packet,name)
   unsupported=answer.get('status')=='unsupported'
   records.append({'id':public_id(c),'task':'A','condition':condition,'status':'unsupported' if unsupported else 'completed','raw_text':None if unsupported else answer['label']})
  report['baselines'][name+'_'+condition]=score_a(cs,records,condition)
write(a.output,report)
print(json.dumps({model:{mode:{group:{k:v.get('summary',{}).get(k) for k in ('n','admitted','exact_correct','false_accepts','nonaccept_reference_n')} for group,v in rs.items() if group.startswith('A_')} for mode,rs in info['interfaces'].items()} for model,info in report['models'].items()},sort_keys=True,indent=2))
