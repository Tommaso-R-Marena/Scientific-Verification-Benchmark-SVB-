"""Fresh local diagnostic execution with portable host paths; never overwrite results."""
import argparse,hashlib,json
from pathlib import Path
import sandbox
D=Path(__file__).parent
p=argparse.ArgumentParser();p.add_argument('--lean-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--ids',nargs='*',default=['S01']);a=p.parse_args()
sandbox.LEAN=a.lean_root.resolve()
identity=json.loads((D/'subject_identity.json').read_text())
for name,h in identity['files'].items():assert hashlib.sha256((sandbox.SUBJECT/name).read_bytes()).hexdigest()==h
out=a.output.resolve()
if out.exists() or not out.is_relative_to(sandbox.R/'results/local'):p.exit(2,'fresh output under results/local required\n')
cs={c['id']:c for c in json.loads((D/'cases.json').read_text())};assert set(a.ids)<=set(cs)
out.mkdir(parents=True)
for cid in a.ids:
 w=out/cid;w.mkdir();(w/'input.json').write_text(json.dumps(cs[cid]['input'],sort_keys=True,indent=2)+'\n')
 r=sandbox.execute(w,['/usr/bin/python3','/worker.py']);(w/'execution.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(cid,r['returncode'])
