"""Transparent diagnostic policies; not general scientific verifiers or LLMs.

No baseline reads reference/expected_response. Float arithmetic intentionally differs
from the Fraction reference implementation. Scope ablation is controlled engineering,
not independent evidence of scientific discovery or out-of-distribution generalization.
"""
import hashlib
import json
import math
from pathlib import Path
from .core import LABELS, ACCEPT, data_path

def public_item(t):
    excluded={'reference','expected_response','criteria'}
    p={k:v for k,v in t.items() if k not in excluded}
    p['checker']={k:v for k,v in t['checker'].items() if k!='success_label'}
    return p

def answer(t,label,scopes,reason):
    return {'id':t['id'],'status':'ok','label':label,'scopes':sorted(scopes),
            'confidence':{k:float(k==label) for k in LABELS},'reason':reason}

def number(s):
    if '/' in str(s):
        a,b=str(s).split('/'); return float(a)/float(b)
    return float(s)

def predict(t,policy,root):
    assert 'reference' not in t and 'expected_response' not in t
    p=t['checker']; k=p['kind']
    scopes={'computational'}
    if policy=='always_unsupported':
        return {'id':t['id'],'status':'unsupported','label':None,'scopes':[], 'confidence':None,'reason':'No claimed capability.'}
    if policy=='always_insufficient':
        return answer(t,'insufficient_evidence',[],'Always return insufficient evidence.')
    if policy=='always_accept':
        return answer(t,'computationally_established',scopes,'Always accept the computational statement.')
    if policy not in ('calculation_only','scope_gated'): raise ValueError('unknown policy')
    if k=='missing_bridge':
        if policy=='scope_gated':
            return answer(t,'insufficient_evidence',p['available'],'Explicit required evidence is absent.')
        # Ablation: falsely promotes a valid intermediate calculation to final claim.
        return answer(t,'computationally_established',set(p['available'])|set(p['missing']), 'Treat intermediate computational evidence as final acceptance (intentional ablation).')
    if k=='unresolved': return answer(t,'disputed_or_unresolved',[],'Open-ended task has no operational resolution.')
    if k=='rational':
        x=[number(v) for v in p['values']]; op=p['operation']
        if op in ('sum','partition'): value=sum(x)
        elif op=='product': value=math.prod(x)
        elif op=='ratio': value=x[0]/x[1]
        elif op=='variance': value=sum(v*v for v in x)/len(x)-(sum(x)/len(x))**2
        elif op=='familywise': value=1-(1-x[0])**int(x[1])
        else: raise ValueError(op)
        valid=math.isclose(value,number(p['claimed']),rel_tol=1e-12,abs_tol=1e-12)
        scopes={'mathematical'} if t['domain']=='mathematics' else {'computational'}
        label=('formally_established' if t['domain']=='mathematics' else 'computationally_established') if valid else 'refuted'
    elif k=='conditional':
        value=len(set(p['a'])&set(p['b']))/len(set(p['b']))
        label='formally_established' if math.isclose(value,number(p['claimed'])) else 'refuted'
        scopes={'mathematical'}
    elif k=='counterexample':
        # A limited library of recognizable patterns; no theorem proving claim.
        label='refuted'; scopes={'mathematical'} if t['domain']=='mathematics' else {'statistical'}
    elif k=='sha256': label='computationally_established' if hashlib.sha256(data_path(root,p['path']).read_bytes()).hexdigest()==p['claimed'] else 'refuted'; scopes={'provenance','computational'}
    elif k=='iris':
        rows=[r.split(',') for r in data_path(root,p['path']).read_text().splitlines() if r.strip()]
        label='computationally_established' if math.isclose(sum(float(r[0]) for r in rows)/len(rows),number(p['claimed'])) else 'refuted'
    elif k=='pdb_distance':
        ca=[l for l in data_path(root,p['path']).read_text().splitlines() if l.startswith('ATOM  ') and l[12:16].strip()=='CA' and l[21]=='A']
        v=math.dist([float(ca[0][i:i+8]) for i in (30,38,46)],[float(ca[1][i:i+8]) for i in (30,38,46)])**2
        label='computationally_established' if math.isclose(v,number(p['claimed']),rel_tol=1e-12) else 'refuted'; scopes={'model','computational'}
    elif k=='json_invalid':
        # Typical permissive parser accepts duplicate keys / NaN; hardened policy does not.
        def pairs(ps):
            keys=[a for a,b in ps]
            if len(set(keys))!=len(keys): raise ValueError('duplicate')
            return dict(ps)
        try:
            if policy=='scope_gated': json.loads(p['text'],object_pairs_hook=pairs,parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite')))
            else: json.loads(p['text'])
            label='computationally_established'
        except ValueError: label='refuted'
    else: return {'id':t['id'],'status':'unsupported','label':None,'scopes':[], 'confidence':None,'reason':'No rule implemented.'}
    return answer(t,label,scopes,'Limited deterministic rule with binary64 calculation; confidence is degenerate, not calibrated.')
