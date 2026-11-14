"""Immutable first freeze for the fresh-source IIb diagnostic comparison."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];out=R/'data/v0.3.0/manifest.json'
if out.exists():raise SystemExit('Refuse to overwrite a frozen protocol; preserve and version deviations.')
names=['src/svb/phase2b.py','scripts/run_phase2b_model.py','scripts/analyze_phase2b.py','scripts/run_phase2b_evaluation.py','src/svb/phase2b_references.py','results/v0.3.0/model_access.json','results/v0.3.0/development_qualification_all_candidates.json']
names += [str(p.relative_to(R)) for p in (R/'data/v0.3.0').rglob('*') if p.is_file() and 'review' not in p.parts]
m={'version':'0.3.0','state':'internally-frozen-public-diagnostic','external_human_reviews':0,'protected_holdout':False,'qualified_scientific_models':0,'files':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in sorted(set(names))}}
out.write_text(json.dumps(m,sort_keys=True,indent=2)+'\n');print(hashlib.sha256(out.read_bytes()).hexdigest())
