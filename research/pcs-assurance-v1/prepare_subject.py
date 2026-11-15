"""Copy a narrow pinned implementation allowlist into ignored SVB storage.

Never checks out or reads benchmark/dev/prospective/adjudication directories.
The repository object store is an opaque source cache, not a held-out study.
"""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2]
G=R/'results/local/pcs-assurance/subject.git';D=R/'results/local/pcs-assurance/subject'
SHA='bd6d88f71833e101fdb6b491df248f0ded0d6f75'
assert subprocess.check_output(['git','--git-dir='+str(G),'cat-file','-t',SHA],text=True).strip()=='commit'
paths=[]
for pkg in ['research/claimcheck_v1','research/claimcheck_v1_1']:
 names=subprocess.check_output(['git','--git-dir='+str(G),'ls-tree','--name-only',SHA+':'+pkg],text=True).splitlines()
 paths += [pkg+'/'+n for n in names if n.endswith('.py')]
paths += ['research/claimcheck_v1/formal/ClaimCheck.lean','research/claimcheck_v1/formal/ClaimCheck.lean.sha256',
 'research/claimcheck_assurance_v1/runner/claimcheck_kernel_runner_v2.py']
files={}
for path in paths:
 b=subprocess.check_output(['git','--git-dir='+str(G),'show',SHA+':'+path]);p=D/path;p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():assert p.read_bytes()==b
 else:p.write_bytes(b);p.chmod(0o444)
 files[path]=hashlib.sha256(b).hexdigest()
record={'repository':'Tommaso-R-Marena/proof-carrying-science','commit':SHA,'files':files,
 'prospective_or_benchmark_content_copied':False,'scope':'Pinned implementation export; original repositories never fetched into, checked out or edited.'}
(R/'research/pcs-assurance-v1/subject_identity.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
print('Exported',len(files),'implementation files; no prospective/dev/heldout data or results.')
