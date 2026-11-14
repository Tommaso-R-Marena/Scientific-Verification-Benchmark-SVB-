"""Verify completed research artifact identity separately from scientific scoring."""
from pathlib import Path
import json,hashlib
from svb.core import canonical,digest,read,Invalid
from svb.phase2b import validate,write,run_records
R=Path(__file__).resolve().parents[1];validate(R)
plan=read(R/'data/v0.3.0/evaluation_plan.json');access=read(R/'results/v0.3.0/model_access.json');checks=[]
for model in plan['selected_models']:
 for mode,groups in plan['groups'].items():
  path=R/plan['run_files'][model][mode];meta=read(path.with_suffix('.run.json'))
  assert digest(path)==meta['output_sha256'],'unfinished or tampered raw record'
  assert meta['model_key']==model and meta['revision']==access['models'][model]['revision']
  assert meta['runner_sha256']==digest(R/'scripts/run_phase2b_model.py')
  assert meta['prompt_file_sha256']==plan['prompt_files'][mode]['sha256']
  assert bool(meta['constrained_a'])==(mode=='constrained')
  expected_prompts=run_records(R/plan['prompt_files'][mode]['path']);bykey={(p['id'],p['task'],p['condition']):p for p in expected_prompts}
  rows=run_records(path);assert len(rows)==len(bykey)==meta['selected_records']
  seen=set()
  for row in rows:
   key=row['id'],row['task'],row['condition'];assert key in bykey and key not in seen;seen.add(key)
   assert row['prompt_sha256']==hashlib.sha256(canonical(bykey[key])).hexdigest()
   assert row['model_key']==model and row['model_revision']==meta['revision']
   assert bool(row['constrained_a'])==(mode=='constrained' and row['task']=='A')
  checks.append({'model':model,'mode':mode,'records':len(rows),'raw_sha256':digest(path),'prompt_sha256':meta['prompt_file_sha256'],'identity_and_prompt_checks_passed':True,'generation_statuses':{s:sum(r['status']==s for r in rows) for s in sorted({r['status'] for r in rows})}})
write(R/'results/v0.3.0/run_integrity.json',{'checks':checks,'scientific_reference_validity_proved':False,'human_adjudication_completed':False})
print(json.dumps(checks,sort_keys=True,indent=2))
