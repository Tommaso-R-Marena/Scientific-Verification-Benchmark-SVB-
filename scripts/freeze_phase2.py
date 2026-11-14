"""First immutable Phase II freeze. Never overwrite a frozen manifest."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'data/v0.2.0/manifest.json'
if p.exists():raise SystemExit('Refusing to overwrite frozen manifest')
names=['src/svb/phase2.py','src/svb/phase2_numeric.py','src/svb/phase2_references.py','scripts/run_local_model.py','scripts/analyze_phase2.py','requirements-models.txt','results/v0.2.0/model_access.json']
names += [str(x.relative_to(R)) for x in (R/'data/v0.2.0').rglob('*') if x.is_file() and 'review' not in x.parts]
m={'version':'0.2.0','protected_holdout':False,'expert_review_completed':False,'reference_status':'provisional_author_adjudicated','files':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in sorted(set(names))}}
p.write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')
print(hashlib.sha256(p.read_bytes()).hexdigest())
