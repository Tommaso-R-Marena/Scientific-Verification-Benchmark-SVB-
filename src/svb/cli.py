from __future__ import annotations
import argparse
import csv
import json
import platform
import sys
from pathlib import Path
from .core import Invalid, LABELS, canonical, digest, read, load_dataset, validate_freeze, calculate, score
from .baselines import public_item,predict

def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n')

def experiment(root,output):
    manifest=validate_freeze(root)
    all_items=load_dataset(root)
    items=[t for t in all_items if t['split']=='evaluation']
    systems={}
    for policy in ('always_accept','always_insufficient','always_unsupported','calculation_only','scope_gated'):
        # Strict public view, deliberately excludes reference labels and explanations.
        responses=[predict(public_item(t),policy,root) for t in items]
        systems[policy]=score(items,responses)
        write(output/(policy+'.responses.json'),responses)
    report={'version':'0.1.0','protocol_sha256':digest(root/'data/protocol.json'),
        'manifest_sha256':digest(root/'data/manifest.json'),'python':platform.python_version(),
        'evaluation_n':len(items),'scored_evaluation_n':sum(t['scored'] for t in items),
        'limitations':['Public frozen labels, no protected holdout','Diagnostic hand-coded policies, not general AI systems','Author-adjudicated pilot; no external scientific expert qualification','Wilson intervals descriptive under hypothetical iid sampling only; purposive sample is not iid'],
        'baselines':systems}
    write(output/'baselines.json',report)
    with (output/'summary.csv').open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['policy','n','correct','accuracy_all','coverage','false_accept_count','scope_overclaims','mean_brier_answered'])
        for name,r in systems.items():
            s=r['summary'];w.writerow([name]+[s[k] for k in ('n','correct','accuracy_all','coverage','false_accept_count','scope_overclaims','mean_brier_answered')])
    # Standalone SVG, no plotting dependencies. All rows share same evaluation tasks.
    bars=[]
    for i,(name,r) in enumerate(systems.items()):
        y=42+i*45; accuracy=r['summary']['accuracy_all']
        bars.append(f'<text x="8" y="{y+17}">{name}</text><rect x="190" y="{y}" width="{accuracy*400:.2f}" height="25" fill="#3265a8"/><text x="{200+accuracy*400:.2f}" y="{y+17}">{accuracy:.3f}</text>')
    (output/'accuracy.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="720" height="320" role="img" aria-label="Diagnostic baseline accuracy"><style>text{font:14px sans-serif}</style><text x="8" y="20">SVB pilot: public authored controls, not AI generalization</text>'+''.join(bars)+'<text x="8" y="300">Missing/unsupported counted in total; open question excluded.</text></svg>\n')
    return report

def main():
    p=argparse.ArgumentParser(description='SVB data-only scientific verification pilot')
    p.add_argument('--root',type=Path,default=Path.cwd())
    s=p.add_subparsers(dest='command',required=True)
    s.add_parser('validate');s.add_parser('references');s.add_parser('export')
    e=s.add_parser('experiment');e.add_argument('--output',type=Path,default=Path('results/core'))
    e=s.add_parser('score');e.add_argument('submission',type=Path);e.add_argument('--output',type=Path,required=True)
    args=p.parse_args();root=args.root.resolve()
    try:
        validate_freeze(root);items=load_dataset(root)
        if args.command=='validate': print(json.dumps({'validated':True,'items':len(items),'manifest_sha256':digest(root/'data/manifest.json')}))
        elif args.command=='references':
            print(json.dumps([{'id':t['id'],'label':calculate(t['checker'],root)[0],'evidence':calculate(t['checker'],root)[1]} for t in items],sort_keys=True,indent=2))
        elif args.command=='export': print(json.dumps([public_item(t) for t in items],sort_keys=True,indent=2))
        elif args.command=='experiment':
            out=args.output.resolve()
            if not out.is_relative_to(root): raise Invalid('output must stay inside independent project')
            r=experiment(root,out)
            print(json.dumps({k:v['summary'] for k,v in r['baselines'].items()},sort_keys=True,indent=2))
        else:
            out=args.output.resolve()
            if not out.is_relative_to(root): raise Invalid('output must stay inside independent project')
            write(out,score([t for t in items if t['split']=='evaluation'],read(args.submission)))
    except (Invalid,OSError,KeyError,TypeError,ValueError,ZeroDivisionError) as e:
        print(json.dumps({'error':type(e).__name__,'message':str(e)}),file=sys.stderr)
        raise SystemExit(2)

if __name__=='__main__': main()
