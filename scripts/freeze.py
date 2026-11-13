"""Explicit first freeze only; immutable existing manifest refuses overwrite."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/manifest.json'
if p.exists(): raise SystemExit('Refusing overwrite: a revision requires new benchmark version and retained artifacts.')
files=['data/tasks.json','data/protocol.json','data/registry.json','data/1CRN.pdb','data/iris.data','data/iris.names','data/iris.zip','docs/reference_protocol.md','src/svb/core.py','src/svb/baselines.py','src/svb/cli.py']
m={'version':'0.1.0','state':'frozen-public','protected_holdout':False,'files':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files}}
p.write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')
print(hashlib.sha256(p.read_bytes()).hexdigest())
