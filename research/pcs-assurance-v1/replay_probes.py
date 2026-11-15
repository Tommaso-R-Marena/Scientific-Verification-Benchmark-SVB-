"""Fresh independent replays, including self-redigested false outward receipt."""
from pathlib import Path
import copy,hashlib,json,shutil
from sandbox import R,SUBJECT,execute
D=Path(__file__).parent;checker=(SUBJECT/'research/claimcheck_v1/formal/ClaimCheck.lean.sha256').read_text().split()[0];rows=[]
for label,cid in [('genuine','S01'),('redigested_false_confirmation','S12')]:
 w=R/'results/local/pcs-assurance/replay'/label;w.mkdir(parents=True,exist_ok=False)
 shutil.copytree(R/f'results/local/pcs-assurance/executions/{cid}/bundle',w/'bundle')
 if label!='genuine':
  p=w/'bundle/records.json';rs=json.loads(p.read_text());r=next(r for r in rs if not r['auxiliary']);r['outward']['verdict']='CONFIRMATION'
  canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
  r['record_sha256']=hashlib.sha256(canonical({k:v for k,v in r.items() if k!='record_sha256'})).hexdigest();p.write_text(json.dumps(rs,sort_keys=True,indent=1)+'\n')
  i=w/'bundle/claimcheck_v1_1.json';x=json.loads(i.read_text());x['files']['records.json']=hashlib.sha256(p.read_bytes()).hexdigest();i.write_text(json.dumps(x,sort_keys=True,indent=1)+'\n')
 run=execute(w,['/usr/bin/python3','/subject/research/claimcheck_v1_1/replay_independent_v1_1.py','/work/bundle','--checker-sha256',checker,'--timeout','90'],timeout=150)
 rows.append({'probe':label,'execution':run});print(label,run['returncode'],run['stdout'][-220:],flush=True)
(D/'results/replay_probes.json').write_text(json.dumps(rows,sort_keys=True,indent=2)+'\n')
