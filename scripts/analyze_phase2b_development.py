"""Development-only qualification; never reads new scientific case labels."""
from pathlib import Path
import argparse,json
from collections import Counter
from svb.core import loads
from svb.phase2 import public_id,admit_answer
from svb.phase2b import minimal_verdict
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if not a.output.resolve().is_relative_to(R):raise SystemExit('output must stay inside project')
controls=json.loads((R/'data/v0.3.0/development_controls.json').read_text());byid={public_id(c):c for c in controls};report={}
for model in ('qwen-0.5b','qwen-1.5b','qwen-3b'):
 modelrows={};allrows=[]
 for mode in ('unconstrained','constrained'):
  path=R/f'results/v0.3.0/development/{model}_{mode}.jsonl'
  if not path.exists():continue
  rows=[loads(l) for l in path.read_text().splitlines() if l.strip()];allrows+=rows;groups={}
  for r in rows:
   group=r['task']+'_'+r['condition'];entry={'id':r['id'],'status':r['status'],'format_valid':False,'verdict':None,'correct':False,'seconds':r.get('seconds')}
   if r['status']=='completed':
    try:
     if r['task']=='A':
      label=minimal_verdict(r['raw_text']);entry.update({'format_valid':True,'verdict':label,'correct':label==byid[r['id']]['reference']['label']})
     elif r['task']=='C':admit_answer(loads(r['raw_text']),byid[r['id']],'evidence');entry['format_valid']=True
     else:entry['format_valid']=bool(r['raw_text'].strip())
    except (ValueError,TypeError,KeyError):pass
   groups.setdefault(group,[]).append(entry)
  modelrows[mode]={g:{'n':len(rs),'format_valid':sum(r['format_valid'] for r in rs),'exact_correct':sum(r['correct'] for r in rs),'rows':rs} for g,rs in groups.items()}
 std=modelrows.get('unconstrained',{}).get('A_dev_standard',{'rows':[]});rev=modelrows.get('unconstrained',{}).get('A_dev_reverse',{'rows':[]})
 sm={r['id']:r for r in std['rows']};rm={r['id']:r for r in rev['rows']}
 consistent=sum(r['format_valid'] and rm.get(pid,{}).get('format_valid') and r['verdict']==rm[pid]['verdict'] for pid,r in sm.items())
 qualified=std.get('format_valid',0)>=5 and std.get('exact_correct',0)>=4 and consistent>=4
 report[model]={'groups':modelrows,'order_consistent':consistent,'order_pairs':6,'standard_development_thresholds_met':qualified,'observed_generation_seconds':sum(r.get('seconds',0) for r in allrows),'qualification_limit':'Author-defined instruction controls and two historical public cases, not independent scientific generalization; C historical rich-prompt differs from minimal A instruction bundle.'}
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:{'qualified':v['standard_development_thresholds_met'],'order_consistent':v['order_consistent'],'groups':{m:{g:{n:r[n] for n in ('n','format_valid','exact_correct')} for g,r in gs.items()} for m,gs in v['groups'].items()}} for k,v in report.items()},sort_keys=True,indent=2))
