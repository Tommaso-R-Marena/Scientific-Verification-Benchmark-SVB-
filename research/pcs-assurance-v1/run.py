"""Execute the internally frozen diagnostic inputs against actual PCS in isolation."""
from pathlib import Path
import hashlib,json,sys,time
from sandbox import execute,R,LEAN,SUBJECT
D=Path(__file__).parent;OUT=D/'results';OUT.mkdir(exist_ok=True)
manifest=json.loads((D/'freeze.json').read_text())
for n,h in manifest.items():assert hashlib.sha256((D/n).read_bytes()).hexdigest()==h,n
cs=json.loads((D/'cases.json').read_text());runs=[]
for c in cs:
 work=R/'results/local/pcs-assurance/executions'/c['id']
 if work.exists():raise SystemExit('Refuse overwrite: preserve failed/missing executions explicitly.')
 work.mkdir(parents=True);(work/'input.json').write_text(json.dumps(c['input'],sort_keys=True,indent=2)+'\n')
 r=execute(work,['/usr/bin/python3','/worker.py'])
 (work/'execution.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
 rows=json.loads((work/'bundle/records.json').read_text()) if (work/'bundle/records.json').exists() else []
 primary=[x for x in rows if not x['auxiliary']]
 record={'id':c['id'],'returncode':r['returncode'],'timed_out':r['timed_out'],'seconds':r['seconds'],'status':'completed' if r['returncode']==0 and len(primary)==1 else 'execution_failure','tripwire_created':(work/'injected.txt').exists(),'records':rows,'execution_stdout':r['stdout'],'execution_stderr':r['stderr']}
 runs.append(record);(OUT/'runs.partial.json').write_text(json.dumps(runs,sort_keys=True,indent=2)+'\n')
 print(json.dumps({'id':c['id'],'status':record['status'],'seconds':r['seconds'],'math':primary[0]['mathematical']['status'] if primary else None,'outward':primary[0]['outward']['verdict'] if primary else None}),flush=True)
(OUT/'runs.json').write_text(json.dumps(runs,sort_keys=True,indent=2)+'\n')
