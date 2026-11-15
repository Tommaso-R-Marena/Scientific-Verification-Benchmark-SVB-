"""Independent rational references and scope-aware descriptive replay; no PCS imports."""
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal
from collections import Counter,defaultdict
import csv,io,json
D=Path(__file__).parent

def reference(x,stat=None):
 s=x['proposal']['spec'];stat=stat or s['stat'];rs=list(csv.DictReader(io.StringIO(x['csv'])))
 for f in s.get('filter',[]):
  if f['kind']=='num':
   t=Q(f['value']);ops={'ge':lambda a:a>=t,'gt':lambda a:a>t,'eq':lambda a:a==t,'ne':lambda a:a!=t,'le':lambda a:a<=t,'lt':lambda a:a<t}
   rs=[r for r in rs if ops[f['cmp']](Q(r[f['column']]))]
  elif f['kind']=='text_eq':rs=[r for r in rs if r[f['column']]==f['value']]
  else:raise ValueError('reference implementation does not silently support this filter')
 if stat=='count':return Q(len(rs)),False
 ys=[Q(r[s['column']]) for r in rs];n=len(ys);mean=sum(ys,Q())/n
 if stat=='mean':return mean,False
 if stat=='sum':return sum(ys,Q()),False
 if stat in ('sd_sample','sd_pop','sem'):
  var=sum((y-mean)**2 for y in ys)/(n-1 if stat!='sd_pop' else n)
  return var/n if stat=='sem' else var,True
 raise ValueError('unsupported independent reference statistic')

def check_theorem(x,t):
 o=t['outcome'];value,sqrt=reference(x,t['statistic']);ex=o['exact'];actual=Q(int(ex['numerator']),int(ex['denominator']))
 s=x['proposal']['spec'];scale=Q(1,1000) if x['manifest']['columns'].get(s.get('column'),{}).get('unit')=='g' and s.get('reported_unit')=='kg' else Q(1)
 half=Q(10)**Decimal(s['reported']).as_tuple().exponent/2;reported=Q(s['reported']);lo,hi=reported-half,reported+half
 match=(hi>=0 and max(lo,Q())**2<=value*scale**2<=hi**2) if sqrt else abs(value*scale-reported)<=half
 return {'value_matches_independent_reference':actual==value,'verdict_matches_independent_reference':o['verdict']==('consistent' if match else 'inconsistent'),'exact':str(value),'sqrt':sqrt}

def analyze():
 cs=json.loads((D/'cases.json').read_text());runs={r['id']:r for r in json.loads((D/'results/runs.json').read_text())};rows=[]
 for c in cs:
  rr=runs.get(c['id']);p=next((r for r in rr['records'] if not r['auxiliary']),None) if rr else None
  invalid_reference=c['id']=='S02'
  checks=[] if not p else [check_theorem(c['input'],t) for t in p['mathematical']['theorems'] if t['outcome'].get('defined')]
  if checks:assert all(v['value_matches_independent_reference'] and v['verdict_matches_independent_reference'] for v in checks),c['id']
  verdict=p['outward']['verdict'] if p else None
  rows.append({'id':c['id'],'stratum':c['stratum'],'family':c['family'],'execution_status':rr['status'] if rr else 'missing',
   'math':p['mathematical']['status'] if p else None,'v1_result':p['v1_result'] if p else None,'v11_outward':verdict,
   'reference_status':'defective_reference_preserved' if invalid_reference else c['reference']['status'],
   'reading_binding_reference':c['reference']['reading_binding'],'scientific_reference':c['reference']['scientific_interpretation'],
   'scientific_output':p['scientific']['status'] if p else None,'independent_computational_checks':checks,
   'supported_confirmation':verdict=='CONFIRMATION' and c['reference']['reading_binding'] and not invalid_reference,
   'unsupported_reading_confirmation':verdict=='CONFIRMATION' and not c['reference']['reading_binding'] and not invalid_reference,
   'binding_supported_discrepancy':verdict=='DISCREPANCY_FOR_REVIEW' and c['reference']['reading_binding'] and not invalid_reference,
   'misleading_discrepancy':verdict=='DISCREPANCY_FOR_REVIEW' and not c['reference']['reading_binding'] and not invalid_reference,
   'seconds':rr['seconds'] if rr else None,'tripwire_created':rr['tripwire_created'] if rr else None})
 def agg(rs):
  return {'scheduled_n':len(rs),'reference_eligible_n':sum(r['reference_status']!='defective_reference_preserved' for r in rs),
   'execution_statuses':dict(Counter(r['execution_status'] for r in rs)),'math_statuses':dict(Counter(r['math'] for r in rs)),
   'outward_counts':dict(Counter(r['v11_outward'] for r in rs)),'v1_result_counts':dict(Counter(r['v1_result'] for r in rs)),
   **{k:sum(r[k] for r in rs) for k in ['supported_confirmation','unsupported_reading_confirmation','binding_supported_discrepancy','misleading_discrepancy']},
   'kernel_decided_primary_n':sum(bool(r['independent_computational_checks']) for r in rs),
   'primary_theorem_checks':sum(len(r['independent_computational_checks']) for r in rs),'scientific_not_assessed':sum(r['scientific_output']=='NOT_ASSESSED' for r in rs),
   'execution_seconds':sum(r['seconds'] or 0 for r in rs)}
 report={'kind':'frozen_development_diagnostic_not_prospective','primary':agg(rows),'by_stratum':{k:agg([r for r in rows if r['stratum']==k]) for k in sorted({r['stratum'] for r in rows})},
 'by_family':{k:agg([r for r in rows if r['family']==k]) for k in sorted({r['family'] for r in rows})},'rows':rows,
 'metamorphic':[{ 'id':c['id'],'parent':c['metamorphic_parent'],'mathematical_match_invariance':runs[c['id']]['records'][0]['mathematical']['status']==runs[c['metamorphic_parent']]['records'][0]['mathematical']['status']=='MATCH_PROVED'} for c in cs if 'metamorphic_parent' in c],
 'limits':['S02 is a preserved benchmark input/reference defect; excluded from reference-dependent judgments but retained in execution denominator18','Unsupported reading confirmation is not kernel unsoundness or proof of a paper error','Correct numerical confirmation does not assess the stronger scientific interpretation','No human reviews; public-data scope author-provisional','Auxiliary siblings are not independent primary cases','Few authored families and paired items are dependent; no population confidence/risk claim','V1 comparison uses v1 receipts in actual v1.1 run, not a newly executed separate v1 study']}
 return report
if __name__=='__main__':
 r=analyze();(D/'results/analysis.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r['primary'],indent=2))
