"""Pinned PCS API invocation inside the OS sandbox; no SVB references imported."""
import json,sys
from pathlib import Path
sys.path.insert(0,'/subject')
from research.claimcheck_v1_1.verify import verify,write_bundle_v11
p=Path('/work');x=json.loads((p/'input.json').read_text())
data=x['csv'].encode();out=p/'bundle'
r=verify([(x['id'],x['proposal'],'SVB diagnostic author; has seen data')],source_text=x['source'],source_meta={'name':'SVB authored diagnostic sentence, not a published-paper error claim'},
 data=data,manifest=x['manifest'],selection={'proposed_by':'SVB diagnostic author','saw_the_data':'yes'},run_lean=True,lean_timeout=180,
 keep_dir=out/'v1/obligations',workers=1,batch_size=4,find_siblings=True)
write_bundle_v11(out,r,source_text=x['source'],data=data,manifest=x['manifest'],source_name='source.txt',data_name='data.csv')
print(json.dumps({'records':len(r['records']),'primary':r['records'][0]['outward']['verdict']}))
