"""Post-hoc raw-JSON attribution audit, separate from frozen strict scoring.

This never upgrades malformed outputs or assigns human reasoning validity.
"""
from pathlib import Path
import argparse,json
from collections import Counter
from svb.core import loads,LABELS,ACCEPT,Invalid
from svb.phase2 import load_cases,public_id,build_prompt,condition_reference,validate,write
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('raw',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
validate(R)
if not a.output.resolve().is_relative_to(R):raise SystemExit('Output must stay in SVB')
cases={public_id(c):c for c in load_cases(R)}
rows=[];seen=set()
for line in a.raw.read_text().splitlines():
 if not line.strip():continue
 x=loads(line);key=x['id'],x['condition']
 if key in seen:raise Invalid('duplicate raw execution')
 seen.add(key);c=cases[x['id']];ref=condition_reference(c,x['condition']);obj=None;error=None
 try:
  obj=loads(x.get('raw_text') or '')
  if not isinstance(obj,dict):raise Invalid('not a JSON object')
 except (Invalid,TypeError) as exc:error=str(exc)
 docs=json.loads(build_prompt(c,x['condition'])['messages'][1]['content'])['documents'];docmap={d['id']:d['text'] for d in docs}
 badids=[];badquotes=[];label=None;scalar=None
 if isinstance(obj,dict):
  label=obj.get('label') if obj.get('label') in LABELS else None
  ev=obj.get('evidence_ids')
  if isinstance(ev,list) and all(isinstance(v,str) for v in ev):badids=sorted(set(ev)-set(docmap))
  for cite in obj.get('citations',[]) if isinstance(obj.get('citations',[]),list) else []:
   if isinstance(cite,dict) and isinstance(cite.get('document_id'),str) and isinstance(cite.get('quote'),str):
    if cite['document_id'] not in docmap:badids.append(cite['document_id'])
    elif cite['quote'] not in docmap[cite['document_id']]:badquotes.append(cite)
  if type(obj.get('confidence')) in (float,int):scalar=obj['confidence']
 rows.append({'id':x['id'],'condition':x['condition'],'raw_object_parseable':isinstance(obj,dict),'parse_error':error,
   'label':label,'reference':ref['label'],'nonaccept_reference':ref['label'] not in ACCEPT,
   'raw_label_false_accept':label in ACCEPT and ref['label'] not in ACCEPT,
   'nonsupplied_evidence_ids':sorted(set(badids)),'invalid_exact_quotes':badquotes,
   'scalar_confidence_as_textual_report_only':scalar,'reasoning_validity':'not_independently_human_adjudicated',
   'output_limit':x.get('output_reached_token_limit',False)})
summary={}
for condition in sorted({r['condition'] for r in rows}):
 rs=[r for r in rows if r['condition']==condition];parsed=[r for r in rs if r['raw_object_parseable']]
 summary[condition]={'observed_n':len(rs),'parseable_object_n':len(parsed),'parse_failures':len(rs)-len(parsed),
  'raw_label_counts':dict(Counter(r['label'] for r in parsed)),
  'raw_label_false_accept_candidates':sum(r['raw_label_false_accept'] for r in rs),
  'all_nonaccept_reference_n':sum(r['nonaccept_reference'] for r in rs),
  'nonsupplied_evidence_id_cases_among_parseable':sum(bool(r['nonsupplied_evidence_ids']) for r in parsed),
  'invalid_exact_quote_cases_among_parseable':sum(bool(r['invalid_exact_quotes']) for r in parsed),
  'output_limit_n':sum(r['output_limit'] for r in rs),
  'scalar_confidence_cases':sum(r['scalar_confidence_as_textual_report_only'] is not None for r in parsed)}
write(a.output,{'analysis':'Post-hoc descriptive raw-JSON audit; not a replacement for frozen strict model scoring',
 'limits':['Not independently human adjudicated','Unknown IDs are nonsupplied packet IDs, not automatically fabricated real publications','Exact quote presence does not establish entailment','Nonparseable outputs remain unassessable for full attribution; candidate counts are not primary admitted false accepts','Scalar confidence is not a valid six-class vector and is not recalibrated or repaired'],
 'conditions':summary,'rows':rows})
print(json.dumps(summary,sort_keys=True,indent=2))
