"""Execute only the internally frozen local-model plan, sequentially and offline.

No evaluated-source references enter runner inputs; raw artifacts refuse overwrite.
This is known-model orchestration, not a sandbox for executable submissions.
"""
from pathlib import Path
import argparse,subprocess,sys,json
from svb.phase2b import validate
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--python',type=Path,default=R/'results/local/model-venv/bin/python');a=p.parse_args()
validate(R)
plan=json.loads((R/'data/v0.3.0/evaluation_plan.json').read_text())
for model in plan['selected_models']:
 for mode in ('unconstrained','constrained'):
  output=R/plan['run_files'][model][mode];output.parent.mkdir(parents=True,exist_ok=True)
  if output.exists():raise SystemExit('Refuse overwrite: preserve prior execution and explicitly plan a missing-request remainder.')
  cmd=[str(a.python),str(R/'scripts/run_phase2b_model.py'),'--model',model,'--prompts',str(R/plan['prompt_files'][mode]['path']),'--output',str(output),'--threads','4','--max-input-tokens','4096','--max-a','24','--max-b','128','--max-c','384']
  if mode=='constrained':cmd.append('--constrained-a')
  log=output.with_suffix('.execution.log')
  print(json.dumps({'starting':str(output.relative_to(R)),'model':model,'mode':mode}),flush=True)
  with log.open('x') as f:result=subprocess.run(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT,check=False)
  print(json.dumps({'finished':str(output.relative_to(R)),'process_returncode':result.returncode}),flush=True)
  if result.returncode:raise SystemExit(result.returncode)
