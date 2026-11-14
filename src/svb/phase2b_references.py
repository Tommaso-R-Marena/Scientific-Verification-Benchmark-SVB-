"""Source-record and exact arithmetic checks for SVB 0.3.0 fresh study families.

GPL R dataset snapshots are read as data;R code is never evaluated. Exact
arithmetic does not validate original laboratory work or author scope judgments.
"""
from __future__ import annotations
from collections import Counter
import csv
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]


def vector(text,name,wrapper=''):
    pat=r'\b'+re.escape(name)+r'\s*=\s*'+(re.escape(wrapper)+r'\(' if wrapper else '')+r'c\(([^()]*)\)'
    m=re.search(pat,text,re.S)
    if not m:raise ValueError('missing simple source vector:'+name)
    values=[x.strip() for x in m[1].split(',')]
    if any(not re.fullmatch(r'-?\d+(?:\.\d+)?',x) for x in values):raise ValueError('nonnumeric source vector')
    return values


def source_rows(root=ROOT):
    d=root/'data/v0.3.0/sources'
    sleep=(d/'sleep.R').read_text();extra=vector(sleep,'extra')
    if len(extra)!=20 or not re.search(r'group\s*=\s*gl\(2,\s*10\)',sleep) or not re.search(r'ID\s*=\s*factor\(rep.int\(1:10,\s*2\)\)',sleep):raise ValueError('unsupported sleep layout')
    sr=[{'ID':str(i%10+1),'group':str(i//10+1),'extra':v} for i,v in enumerate(extra)]
    chick=(d/'ChickWeight.R').read_text()
    arrays={name:vector(chick,name,wrapper) for name,wrapper in [('weight',''),('Time',''),('Chick','ordered'),('Diet','factor')]}
    # R ordered() stores integer codes plus explicit labels;codes are NOT IDs.
    m=re.search(r'Chick\s*=\s*ordered\(c\([^()]*\),\s*levels=1:50,\s*labels\s*=\s*c\(([^()]*)\)',chick,re.S)
    if not m:raise ValueError('unsupported Chick factor layout')
    labels=[s.strip().strip('"') for s in m[1].split(',')]
    if len(labels)!=50 or set(labels)!={str(i) for i in range(1,51)} or any(len(v)!=578 for v in arrays.values()):raise ValueError('invalid ChickWeight shape')
    cr=[{'weight':arrays['weight'][i],'Time':arrays['Time'][i],'Chick':labels[int(arrays['Chick'][i])-1],'Diet':arrays['Diet'][i]} for i in range(578)]
    bod=(d/'BOD.R').read_text();times=vector(bod,'Time');demand=vector(bod,'demand')
    if len(times)!=6 or len(demand)!=6:raise ValueError('BOD shape')
    br=[{'Time':t,'demand':v} for t,v in zip(times,demand)]
    return {'sleep':sr,'chick_growth':cr,'oxygen_demand':br}


def recompute(operation,root=ROOT):
    data=source_rows(root)
    if operation=='sleep_paired_mean':
        values={g:{r['ID']:Q(r['extra']) for r in data['sleep'] if r['group']==g} for g in ('1','2')}
        if set(values['1'])!=set(values['2']):raise ValueError('paired IDs differ')
        diffs=[values['2'][k]-values['1'][k] for k in values['1']]
        return {'pairs':len(diffs),'sum_difference_hours':str(sum(diffs,Q())),'mean_difference_hours':str(sum(diffs,Q())/len(diffs))}
    if operation=='sleep_signs':
        values={g:{r['ID']:Q(r['extra']) for r in data['sleep'] if r['group']==g} for g in ('1','2')}
        ds=[values['2'][k]-values['1'][k] for k in values['1']]
        return {'greater':sum(x>0 for x in ds),'equal':sum(x==0 for x in ds),'less':sum(x<0 for x in ds),'pairs':len(ds)}
    if operation=='chick_day21':
        out={}
        for diet in ('1','4'):
            xs=[Q(r['weight']) for r in data['chick_growth'] if r['Time']=='21' and r['Diet']==diet]
            out['diet'+diet+'_n']=len(xs);out['diet'+diet+'_mean_g']=str(sum(xs,Q())/len(xs))
        out['diet4_minus_diet1_g']=str(Q(out['diet4_mean_g'])-Q(out['diet1_mean_g']))
        return out
    if operation=='chick_one_growth':
        r={x['Time']:Q(x['weight']) for x in data['chick_growth'] if x['Chick']=='1'}
        return {'chick':'1','birth_g':str(r['0']),'day21_g':str(r['21']),'observed_gain_g':str(r['21']-r['0'])}
    if operation=='oxygen_change':
        r={x['Time']:Q(x['demand']) for x in data['oxygen_demand']}
        return {'day1_mg_per_L':str(r['1']),'day7_mg_per_L':str(r['7']),'difference_mg_per_L':str(r['7']-r['1']),'difference_g_per_L':str((r['7']-r['1'])/1000)}
    if operation=='oxygen_nonmonotone':
        r={x['Time']:Q(x['demand']) for x in data['oxygen_demand']}
        return {'day3_mg_per_L':str(r['3']),'day4_mg_per_L':str(r['4']),'drop_mg_per_L':str(r['3']-r['4']),'nonmonotone':any(Q(b['demand'])<Q(a['demand']) for a,b in zip(data['oxygen_demand'],data['oxygen_demand'][1:]))}
    raise ValueError('unknown exact operation:'+operation)


def verify_transformations(root=ROOT):
    d=root/'data/v0.3.0/sources';source=source_rows(root);out={}
    for name,raw in source.items():
        with (d/(name+'_extracted.csv')).open(newline='') as f:extracted=list(csv.DictReader(f))
        if extracted!=raw:raise ValueError('source transformation mismatch:'+name)
        out[name]={'rows':len(raw),'cells':len(raw)*len(raw[0])}
    return out


def validate(root=ROOT):
    d=root/'data/v0.3.0';registry=json.loads((d/'registry.json').read_text())
    for source in registry['sources'].values():
        for a in source['artifacts']:
            path=(root/a['path']).resolve()
            if not path.is_relative_to((d/'sources').resolve()):raise ValueError('source path escape')
            if hashlib.sha256(path.read_bytes()).hexdigest()!=a['sha256']:raise ValueError('source hash mismatch:'+a['path'])
    transformations=verify_transformations(root)
    cs=json.loads((d/'cases.json').read_text());checks=[]
    for c in cs:
        check=c['reference'].get('numeric_check')
        if check:
            got=recompute(check['operation'],root)
            if got!=check['expected']:raise ValueError('numeric witness mismatch:'+c['id'])
            checks.append({'id':c['id'],'operation':check['operation'],'result':got})
    return {'version':'0.3.0','source_hashes_valid':True,'numeric_witnesses_checked':len(checks),'checks':checks,'transformations':transformations,'original_laboratory_execution_verified':False,'external_human_adjudication':False}

if __name__=='__main__':print(json.dumps(validate(),indent=2,sort_keys=True))
