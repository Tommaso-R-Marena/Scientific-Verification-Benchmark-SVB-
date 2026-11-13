"""Strict data-only ingestion, independent reference checks and explicit scoring."""
from __future__ import annotations
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

LABELS = ('formally_established', 'computationally_established', 'empirically_supported',
          'refuted', 'insufficient_evidence', 'disputed_or_unresolved')
ACCEPT = frozenset(LABELS[:3])
SCOPES = frozenset(('mathematical', 'computational', 'numerical', 'statistical',
                    'model', 'empirical', 'provenance', 'epistemic'))
MAX_BYTES = 2_000_000

class Invalid(ValueError):
    """Untrusted input failed admission; no partial scores are returned."""

def _pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise Invalid(f'duplicate JSON key: {k}')
        d[k] = v
    return d

def loads(s: str) -> Any:
    if len(s.encode()) > MAX_BYTES:
        raise Invalid('input too large')
    try:
        def finite_float(s):
            value=float(s)
            if not math.isfinite(value): raise Invalid('nonfinite JSON number')
            return value
        return json.loads(s, object_pairs_hook=_pairs, parse_float=finite_float,
                          parse_constant=lambda s: (_ for _ in ()).throw(Invalid('nonfinite JSON')))
    except (ValueError, RecursionError) as e:
        raise Invalid(str(e)) from e

def read(path: Path):
    if path.stat().st_size > MAX_BYTES:
        raise Invalid('input too large')
    return loads(path.read_text())

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def data_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or Path(name).is_absolute():
        raise Invalid('relative registered data path required')
    path = (root/name).resolve()
    if not path.is_relative_to((root/'data').resolve()):
        raise Invalid('data path escapes boundary')
    registry = read(root/'data/registry.json')
    source = next((s for s in registry['sources'].values() if s.get('path')==name), None)
    if source is None or digest(path)!=source.get('sha256'):
        raise Invalid('unregistered or corrupted evidence')
    return path

def _q(s) -> Q:
    if not isinstance(s, (str, int)) or isinstance(s, bool) or len(str(s)) > 100:
        raise Invalid('bounded rational required')
    try:
        q = Q(s)
    except (ValueError, ZeroDivisionError) as e:
        raise Invalid('invalid rational') from e
    return q

def calculate(p: dict, root: Path) -> tuple[str, dict]:
    """Answer from exact specifications/witnesses, never subject outputs or stored labels.

    Hand-reviewed scientific sufficiency is encoded as an explicit missing bridge,
    not inferred by a model and not described as mechanically established truth.
    """
    k = p['kind']
    if k == 'rational':
        if p['success_label'] not in ('formally_established','computationally_established'):
            raise Invalid('arithmetic cannot establish empirical support')
        x = [_q(a) for a in p['values']]
        op = p['operation']
        if op == 'sum': value = sum(x, Q())
        elif op == 'product': value = math.prod(x)
        elif op == 'ratio': value = x[0] / x[1]
        elif op == 'variance':
            mean = sum(x) / len(x)
            value = sum((v-mean)**2 for v in x) / len(x)
        elif op == 'familywise': value = 1 - (1-x[0])**int(x[1])
        elif op == 'partition': value = sum(x, Q())
        else: raise Invalid('unknown arithmetic operation')
        verdict = p['success_label'] if value == _q(p['claimed']) else 'refuted'
        return verdict, {'exact':str(value), 'claimed':p['claimed'], 'operation':op}
    if k == 'conditional':
        # Exhaustively enumerated equiprobable sample space.
        universe = set(p['universe']); a = set(p['a']); b = set(p['b'])
        if not a <= universe or not b <= universe or not b:
            raise Invalid('invalid conditional event')
        value = Q(len(a & b), len(b))
        return ('formally_established' if value == _q(p['claimed']) else 'refuted'), {'exact':str(value)}
    if k == 'counterexample':
        # Finite, exhaustive witnesses for supplied false mathematical statements.
        name = p['statement']
        if name == 'quantifier_swap':
            worlds = [-1,0,1]
            antecedent = all(any(x+y == 0 for y in worlds) for x in worlds)
            consequent = any(all(x+y == 0 for x in worlds) for y in worlds)
            assert antecedent and not consequent
            w = {'domain':worlds,'forall_exists':antecedent,'exists_forall':consequent}
        elif name == 'division_cancellation':
            assert Q(0)*Q(1) == Q(0)*Q(2) and Q(1) != Q(2)
            w = {'a':0,'b':1,'c':2}
        elif name == 'stationary_maximum':
            assert Q(1)**2 > Q(0)**2
            w = {'f':'x^2','domain':'[-1,1]','stationary':0,'better':1}
        elif name == 'invalid_proof_true_theorem':
            # Claim is validity of submitted division-by-zero proof, not 1+1=2.
            w = {'theorem_true':Q(1)+Q(1)==Q(2),'proof_step_denominator':0}
        elif name == 'independent_covariance':
            # X=Y, symmetric +/-1: Var(X+Y)=4, not 2.
            w = {'variance_actual':4,'variance_claimed':2,'covariance':1}
        else: raise Invalid('unknown witness')
        return 'refuted', w
    if k == 'missing_bridge':
        # Reviewed insufficient evidence, not a false-theorem verdict.
        if set(p['available']) & set(p['missing']):
            raise Invalid('contradictory admitted/missing evidence')
        if not p['missing'] or not p['worlds'] or len(p['worlds']) < 2:
            raise Invalid('insufficient evidence needs alternative-world explanation')
        return 'insufficient_evidence', {'missing':p['missing'],'worlds':p['worlds'],
                                        'adjudication':'reviewed scope judgment; not automated empirical discovery'}
    if k == 'sha256':
        actual = digest(data_path(root,p['path']))
        return ('computationally_established' if actual == p['claimed'] else 'refuted'), {'sha256':actual}
    if k == 'iris':
        rows = [r.split(',') for r in data_path(root,p['path']).read_text().splitlines() if r.strip()]
        value = sum(_q(r[0]) for r in rows)/len(rows)
        return ('computationally_established' if value==_q(p['claimed']) else 'refuted'), {'rows':len(rows),'sepal_length_mean_cm':str(value)}
    if k == 'pdb_distance':
        ca = [l for l in data_path(root,p['path']).read_text().splitlines()
              if l.startswith('ATOM  ') and l[12:16].strip()=='CA' and l[21]=='A']
        a,b = ca[:2]
        squared = sum((_q(a[i:i+8].strip())-_q(b[i:i+8].strip()))**2 for i in (30,38,46))
        return ('computationally_established' if squared==_q(p['claimed']) else 'refuted'), {'squared_distance_angstrom2':str(squared),'CA_count':len(ca)}
    if k == 'json_invalid':
        try: loads(p['text'])
        except Invalid: return 'refuted', {'rejected':True}
        return 'computationally_established', {'rejected':False}
    if k == 'unresolved':
        return 'disputed_or_unresolved', {'reason':p['reason'],'scored':False}
    raise Invalid(f'unknown checker: {k}')

def load_dataset(root: Path) -> list[dict]:
    items = read(root/'data/tasks.json')
    if not isinstance(items,list) or not items: raise Invalid('nonempty task list required')
    ids=set(); fingerprints=set(); families={}
    needed = {'id','domain','split','family','question','claim','assumptions','sources','reference',
              'checker','criteria','uncertainty','expected_response','limitations','severity','difficulty','scored'}
    for t in items:
        if not isinstance(t,dict) or set(t)!=needed: raise Invalid('task fields do not match schema')
        if t['id'] in ids: raise Invalid('duplicate item ID')
        ids.add(t['id'])
        fp=hashlib.sha256(canonical({'claim':t['claim'],'checker':t['checker']})).hexdigest()
        if fp in fingerprints: raise Invalid('duplicated example')
        fingerprints.add(fp)
        if t['split'] not in ('dev','evaluation'): raise Invalid('invalid split')
        old=families.setdefault(t['family'],t['split'])
        if old!=t['split']: raise Invalid('family leakage across splits')
        if t['domain'] not in ('mathematics','computation','statistics','biophysics','provenance','safety'): raise Invalid('unknown domain')
        if type(t['scored']) is not bool: raise Invalid('scored must be boolean')
        if t['reference']['label'] not in LABELS: raise Invalid('unknown label')
        if not set(t['reference']['scopes'])<=SCOPES: raise Invalid('unknown scope')
        if not all(t[f] for f in ('assumptions','sources','criteria','uncertainty','limitations')): raise Invalid('missing adjudication')
        for s in t['sources']:
            if s not in read(root/'data/registry.json')['sources']: raise Invalid('unregistered source')
        label,_ = calculate(t['checker'],root)
        if label!=t['reference']['label']: raise Invalid('reference label contradicts independent check: '+t['id'])
    return items

def validate_freeze(root:Path) -> dict:
    m=read(root/'data/manifest.json')
    if m['version']!='0.1.0': raise Invalid('unsupported manifest version')
    for name, expected in m['files'].items():
        p=root/name
        if not p.resolve().is_relative_to(root.resolve()): raise Invalid('path escape')
        if digest(p)!=expected: raise Invalid('frozen file hash mismatch: '+name)
    load_dataset(root)
    return m

def response(raw:dict) -> dict:
    if not isinstance(raw,dict): raise Invalid('response object required')
    required={'id','status','label','scopes','confidence','reason'}
    if set(raw)!=required: raise Invalid('response schema mismatch')
    if raw['status'] not in ('ok','unsupported','execution_error'): raise Invalid('unknown execution status')
    if not isinstance(raw['id'],str) or not isinstance(raw['reason'],str) or len(raw['reason'])>10000: raise Invalid('invalid text')
    if not isinstance(raw['scopes'],list) or len(set(raw['scopes']))!=len(raw['scopes']) or not set(raw['scopes'])<=SCOPES: raise Invalid('invalid scopes')
    if raw['status']!='ok':
        if raw['label'] is not None or raw['confidence'] is not None or raw['scopes']: raise Invalid('failed execution cannot assert a verdict')
    else:
        if raw['label'] not in LABELS: raise Invalid('unknown response label')
        c=raw['confidence']
        if not isinstance(c,dict) or set(c)!=set(LABELS): raise Invalid('full probability vector required')
        if any(type(v) not in (float,int) or not math.isfinite(v) or v<0 or v>1 for v in c.values()): raise Invalid('invalid confidence')
        if abs(sum(c.values())-1)>1e-9: raise Invalid('probabilities must sum to 1')
        if c[raw['label']] < max(c.values())-1e-12: raise Invalid('label must maximize probability')
    return raw

def wilson(successes:int,total:int) -> list[float]|None:
    if not total: return None
    z=1.959963984540054; phat=successes/total; den=1+z*z/total
    center=(phat+z*z/(2*total))/den
    radius=z*math.sqrt(phat*(1-phat)/total+z*z/(4*total*total))/den
    return [max(0.,center-radius),min(1.,center+radius)]

def score(items:list[dict], submitted:list[dict]) -> dict:
    if not isinstance(submitted,list): raise Invalid('submission array required')
    allowed={t['id'] for t in items}; responses={}
    for raw in submitted:
        r=response(raw)
        if r['id'] not in allowed: raise Invalid('unknown submitted ID')
        if r['id'] in responses: raise Invalid('duplicate submitted ID')
        responses[r['id']]=r
    rows=[]
    for t in items:
        r=responses.get(t['id']); status='missing' if r is None else r['status']
        correct=status=='ok' and r['label']==t['reference']['label']
        overclaim=status=='ok' and bool(set(r['scopes'])-set(t['reference']['scopes']))
        false_accept=status=='ok' and r['label'] in ACCEPT and t['reference']['label'] not in ACCEPT
        brier=None if status!='ok' else sum((r['confidence'][k]-int(k==t['reference']['label']))**2 for k in LABELS)
        rows.append({'id':t['id'],'domain':t['domain'],'scored':t['scored'],'status':status,
          'reference':t['reference']['label'],'predicted':None if r is None else r['label'],
          'correct':bool(correct),'false_accept':bool(false_accept),'scope_overclaim':bool(overclaim),
          'brier':brier,'severity':t['severity'],'difficulty':t['difficulty']})
    def aggregate(rs):
        n=len(rs); ok=[r for r in rs if r['status']=='ok']; c=sum(r['correct'] for r in rs)
        accepted=[r for r in rs if r['predicted'] in ACCEPT and r['status']=='ok']
        positives=[r for r in rs if r['reference'] in ACCEPT]
        negatives=[r for r in rs if r['reference'] not in ACCEPT]
        return {'n':n,'statuses':dict(Counter(r['status'] for r in rs)), 'correct':c,
          'accuracy_all':c/n if n else None,'accuracy_wilson95_descriptive':wilson(c,n),
          'coverage':len(ok)/n if n else None,'accuracy_answered':sum(r['correct'] for r in ok)/len(ok) if ok else None,
          'false_accept_count':sum(r['false_accept'] for r in rs),'nonaccept_reference_n':len(negatives),
          'false_accept_rate':sum(r['false_accept'] for r in negatives)/len(negatives) if negatives else None,
          'false_reject_count':sum(r['predicted']=='refuted' and r['status']=='ok' for r in positives),
          'accept_reference_n':len(positives),'accepted_n':len(accepted),
          'accepted_risk':sum(not r['correct'] or r['scope_overclaim'] for r in accepted)/len(accepted) if accepted else None,
          'correct_insufficient':sum(r['correct'] and r['reference']=='insufficient_evidence' for r in rs),
          'scope_overclaims':sum(r['scope_overclaim'] for r in rs),
          'mean_brier_answered':sum(r['brier'] for r in ok)/len(ok) if ok else None,
          'confusion':dict(Counter(r['reference']+' -> '+str(r['predicted'] if r['status']=='ok' else r['status']) for r in rs))}
    scored=[r for r in rows if r['scored']]
    return {'summary':aggregate(scored),'by_domain':{d:aggregate([r for r in scored if r['domain']==d]) for d in sorted({r['domain'] for r in rows})},
            'by_severity':{s:aggregate([r for r in scored if r['severity']==s]) for s in sorted({r['severity'] for r in scored})},
            'by_difficulty':{s:aggregate([r for r in scored if r['difficulty']==s]) for s in sorted({r['difficulty'] for r in scored})},
            'excluded_unresolved_n':len(rows)-len(scored),'rows':rows}
