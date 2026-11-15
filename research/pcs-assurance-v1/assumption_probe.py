"""Post-hoc positive discrepancy control; independent convention explicitly admitted."""
from pathlib import Path
import copy,json
from sandbox import R,execute
D=Path(__file__).parent;sup=json.loads((D/'results/supplemental_probes.json').read_text())
x=copy.deepcopy(next(r['input'] for r in sup['rows'] if r['id']=='S02b'));x['id']='S02c'
x['source']=x['source'].replace('(SD','(sample SD');x['proposal']['quote']=x['source'];x['manifest']['sd_convention']='n-1'
w=R/'results/local/pcs-assurance/supplemental/S02c';w.mkdir(parents=True,exist_ok=False);(w/'input.json').write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
r=execute(w,['/usr/bin/python3','/worker.py']);records=json.loads((w/'bundle/records.json').read_text()) if (w/'bundle/records.json').exists() else []
(D/'results/assumption_probe.json').write_text(json.dumps({'kind':'post_hoc_meaningful_assumption_change_not_primary','input':x,'execution':r,'records':records},sort_keys=True,indent=2)+'\n')
print(r['returncode'],records[0]['outward']['verdict'] if records else None)
