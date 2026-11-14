"""Score preselected model conditions; never alters or repairs generated answers."""
from pathlib import Path
import argparse,json
from svb.phase2 import validate,load_cases,public_id,model_records,score_responses,write,CONDITIONS
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('raw_jsonl',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
validate(R)
if not a.output.resolve().is_relative_to(R):raise SystemExit('Output must stay inside project')
cases=[c for c in load_cases(R) if c['split']=='evaluation']
report={'version':'0.2.0','reference_status':'provisional_author_adjudicated','conditions':{},'source_breakdowns':{},'limitations':['Public—not hidden evaluation','Single small public instruct model; no general AI claim','Reasoning validity not independently human reviewed','Condition-specific labels; withholding docs changes proper answer','Four-case assistance/assumption/paraphrase subsets not powered comparisons']}
for condition in CONDITIONS:
    selected=cases if condition in ('evidence','no_evidence') else cases[:4]
    records=model_records(a.raw_jsonl,condition)
    report['conditions'][condition]=score_responses(selected,records,condition)
    report['source_breakdowns'][condition]={}
    for family in sorted({c['family'] for c in selected}):
        cs=[c for c in selected if c['family']==family];ids={public_id(c) for c in cs}
        report['source_breakdowns'][condition][family]=score_responses(cs,[r for r in records if r['id'] in ids],condition)['summary']
write(a.output,report)
print(json.dumps({k:{'n':v['summary']['n'],'strict_correct':v['summary']['correct'],'coverage':v['summary']['coverage'],'statuses':v['summary']['raw_statuses'],'secondary_extracted':v['summary']['secondary_label_extracted_n'],'secondary_agree':v['summary']['secondary_label_agreement_correct']} for k,v in report['conditions'].items()},sort_keys=True,indent=2))
