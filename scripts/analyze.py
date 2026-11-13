"""Post-hoc descriptive decomposition; never changes frozen labels or scores."""
from pathlib import Path
import json
from svb.core import read,load_dataset,score,validate_freeze
R=Path(__file__).resolve().parents[1]
validate_freeze(R)
tasks=[t for t in load_dataset(R) if t['split']=='evaluation']
a={x['id']:x for x in read(R/'results/core/calculation_only.responses.json')}
b={x['id']:x for x in read(R/'results/core/scope_gated.responses.json')}
results={}
for name,types in [('scope_gate_only',{'missing_bridge'}),('strict_json_only',{'json_invalid'}),('both',{'missing_bridge','json_invalid'})]:
    responses=[(b if t['checker']['kind'] in types else a)[t['id']] for t in tasks]
    results[name]=score(tasks,responses)['summary']
# Confidence is one-hot for all policies. Thresholding cannot create a meaningful curve.
rows={'analysis':'Post-hoc controlled hybrid ablation of frozen response artifacts, not new preregistered comparison',
      'hybrids':results,'risk_coverage_limitation':'One-hot policies have no confidence ranking; a smooth curve or calibration claim would be misleading.'}
(R/'results/ablations.json').write_text(json.dumps(rows,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:{'n':v['n'],'correct':v['correct'],'false_accept_count':v['false_accept_count']} for k,v in results.items()},sort_keys=True))
