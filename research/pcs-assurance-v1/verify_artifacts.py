"""Offline artifact identities, not scientific validation or fresh kernel execution."""
from pathlib import Path
import hashlib,json,zipfile
D=Path(__file__).parent
m=json.loads((D/'MANIFEST.json').read_text())
for name,h in m['files'].items():
 p=(D/name).resolve();assert p.is_relative_to(D.resolve()) and hashlib.sha256(p.read_bytes()).hexdigest()==h,name
index=json.loads((D/'archive_manifest.json').read_text())
with zipfile.ZipFile(D/'raw_executions.zip') as z:
 assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(index)
 for n,h in index.items():assert not Path(n).is_absolute() and '..' not in Path(n).parts and hashlib.sha256(z.read(n)).hexdigest()==h,n
print('PCS diagnostic artifact identity verified; no expert/scientific validity inferred.')
