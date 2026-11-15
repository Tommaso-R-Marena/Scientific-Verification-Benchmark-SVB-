"""Reproduce a disclosed runner issue and check its existing proposed guard."""
from pathlib import Path
import json,hashlib,sys,shutil
from sandbox import R,execute,SUBJECT
D=Path(__file__).parent;work=R/'results/local/pcs-assurance/artifact-probes';work.mkdir(exist_ok=False)
checker=(SUBJECT/'research/claimcheck_v1/formal/ClaimCheck.lean').read_text()
data=b'x\n1\n2\n'
marker='\n-- ===== generated obligations (data numeral, claims, expected outcomes) =====\n'
tail=('open PCS.ClaimCheck\n\n'+f'def pcs_src : Source := ⟨0x{data.hex()}, {len(data)}⟩\n\n'
 'structure IndependentDecoy where\n  witness : Nat\n\n'
 'def pcs_c0 : IndependentDecoy := ⟨7⟩\n\n'
 'def run (_ : Source) (_ : IndependentDecoy) : Outcome := .checked .consistent (.rat ((314159 : Rat) / 1)) 2 0\n\n'
 'theorem pcs_claim_0 : run pcs_src pcs_c0 = .checked .consistent (.rat ((314159 : Rat) / 1)) 2 0 := by\n  rfl\n#print axioms pcs_claim_0\n\n')
(work/'forged.lean').write_text(checker+marker+tail)
original='/subject/research/claimcheck_v1_1/claimcheck_kernel_runner.py';v2='/subject/research/claimcheck_assurance_v1/runner/claimcheck_kernel_runner_v2.py'
genuine=next((R/'results/local/pcs-assurance/executions/S01/bundle/v1/obligations').glob('*.lean'));shutil.copyfile(genuine,work/'genuine.lean')
(work/'corrupt.lean').write_text('corrupt'+(work/'genuine.lean').read_text())
rows=[]
for tool,script in [('original_v11',original),('existing_candidate_v2',v2)]:
 for name in ['genuine','forged','corrupt']:
  out=f'{tool}_{name}.json';r=execute(work,['/usr/bin/python3',script,f'/work/{name}.lean','--lean','/lean/bin/lean','--out',f'/work/{out}'],timeout=90)
  raw=json.loads((work/out).read_text()) if (work/out).exists() else None
  rows.append({'tool':tool,'input':name,'execution':r,'report':raw,'input_sha256':hashlib.sha256((work/(name+'.lean')).read_bytes()).hexdigest()})
  print(tool,name,r['returncode'],None if raw is None else raw.get('accepted'),flush=True)
(D/'results/artifact_probes.json').write_text(json.dumps({'known_disclosed_issue_reproduction_not_new_discovery':True,'rows':rows},sort_keys=True,indent=2)+'\n')
