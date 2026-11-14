"""Post-hoc internal audit of historical results; no model inference or relabeling."""
from pathlib import Path
from collections import Counter,defaultdict
from decimal import Decimal
import csv,hashlib,json,math,subprocess
from svb.core import read,ACCEPT,LABELS
from svb.phase2 import public_id
from svb.taxonomy import false_acceptance_bounds
ROOT=Path(__file__).resolve().parents[1]
BASE='d832b6431c37871674d20ceb534e9b5fac797909'
MAIN='30f842e241b0a37ab5d24ef6537113d6bbbb4103'

def put(name,x):
 p=ROOT/'results/v0.4.0'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def rows(name):
 with (ROOT/'data/v0.3.0/sources'/name).open(newline='') as f:return list(csv.DictReader(f))
def rational(n,d=1):
 g=math.gcd(n,d);return f'{n//g}/{d//g}'
def eq_rational(got,expected):
 a,b=got.split('/');parts=expected.split('/');c,d=(parts+["1"])[:2] if len(parts)==1 else parts
 return int(a)*int(d)==int(c)*int(b)

def numerical():
 sleep=rows('sleep_extracted.csv');pairs=defaultdict(dict)
 for r in sleep:pairs[r['ID']][r['group']]=int(Decimal(r['extra'])*10)
 differences=[x['2']-x['1'] for x in pairs.values()];assert len(differences)==10
 chick=rows('chick_growth_extracted.csv');groups={k:[int(r['weight']) for r in chick if r['Time']=='21' and r['Diet']==k] for k in ('1','4')}
 d={r['Time']:int(Decimal(r['demand'])*10) for r in rows('oxygen_demand_extracted.csv')}
 values={'SL01P':rational(sum(differences),10*len(differences)),'SL01X':rational(sum(differences),10*len(differences)),
    'CW01P':rational(sum(groups['4'])*len(groups['1'])-sum(groups['1'])*len(groups['4']),len(groups['4'])*len(groups['1'])),
    'OD01P':rational(d['7']-d['1'],10000)}
 values['CW01X']=values['CW01P'];values['OD01X']=values['OD01P']
 cs={c['id']:c for c in read(ROOT/'data/v0.3.0/cases.json')}
 keys={'SL01P':'mean_difference_hours','SL01X':'mean_difference_hours','CW01P':'diet4_minus_diet1_g','CW01X':'diet4_minus_diet1_g','OD01P':'difference_g_per_L','OD01X':'difference_g_per_L'}
 for cid,v in values.items():assert eq_rational(v,cs[cid]['reference']['numeric_check']['expected'][keys[cid]])
 one={r['Time']:int(r['weight']) for r in chick if r['Chick']=='1'}
 assert (sum(v>0 for v in differences),sum(v==0 for v in differences),one['0'],one['21'],d['3']-d['4'])==(9,1,42,205,30)
 return {'audit_kind':'internal_independent_implementation_not_external_validation','method':'Read archived CSV, use integer tenths and integer cross-products; do not import the old source parser or numerical oracle. Decimal used only for exact scaling of stored decimals.',
   'calculated_rationals':values,'sleep_positive_pairs':9,'sleep_ties':1,'chick_day21_n':{k:len(v) for k,v in groups.items()},
   'chick_day21_sums_g':{k:sum(v) for k,v in groups.items()},'chick1_birth_and_day21_g':[one['0'],one['21']],
   'oxygen_day3_minus_day4_mg_L':3,'all_historical_numeric_comparisons_pass':True,
   'reference_errors_discovered':0,'scope_and_primary_measurement_validity_not_proved':True}

def sensitivity():
 r=read(ROOT/'results/v0.3.0/results.json');out=[]
 for model,x in r['models'].items():
  for mode,y in x['interfaces'].items():
   a=y['A_evidence'];rows_=a['rows'];nonaccept=[z for z in rows_ if z['reference'] not in ACCEPT]
   # Pure evidence-type multiplicity within the accepting set cannot change FA.
   for z in rows_:
    labels=list(ACCEPT) if z['reference'] in ACCEPT else [z['reference']]
    b=false_acceptance_bounds(z['predicted'],labels)
    assert b['lower']==b['upper']==int(z['false_accept'])
   out.append({'model':model,'mode':mode,'historical_nonaccept_reference_n':len(nonaccept),
       'historical_false_accepts':sum(z['false_accept'] for z in nonaccept),
       'unchanged_under_within_accepting_group_multiplicity':True,
       'false_accept_items':[z['id'] for z in nonaccept if z['false_accept']],
       'supported_reference_n':6,'accepted_supported_items':sum(z['reference'] in ACCEPT and z['predicted'] in ACCEPT for z in rows_),
       'scientific_references_externally_adjudicated':False})
 return {'kind':'post_hoc_class_membership_invariance_audit_not_rescoring','rows':out,
   'cross_acceptance_boundary':'If actual independent reviewers admit both accepting and nonaccepting references, the indicator is set-valued (0..1) for an accepting prediction. No definite false-accept rate is then identified without a resolution policy. Counts on fixed denominators or stratified definite/ambiguous counts are preferable to moving-denominator bounds.',
   'new_gold_created':False,'historical_scores_modified':False,'representative_model_ranking_justified':False}

def release():
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,text=True).splitlines()
 files=[];dups=defaultdict(list)
 for p in paths:
  b=subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT)
  h=hashlib.sha256(b).hexdigest();files.append({'path':p,'bytes':len(b),'sha256':h});dups[h].append(p)
 duplicate=[{'sha256':h,'paths':ps,'copies':len(ps),'bytes_per_copy':next(x['bytes'] for x in files if x['sha256']==h)} for h,ps in dups.items() if len(ps)>1]
 sizes=Counter()
 for f in files:sizes[f['path'].split('/')[0]]+=f['bytes']
 diff=subprocess.check_output(['git','diff','--numstat',MAIN,BASE],cwd=ROOT,text=True).splitlines()
 adds=dels=binaries=0
 for line in diff:
  a,d,_=line.split('\t',2)
  if a=='-':binaries+=1
  else:adds+=int(a);dels+=int(d)
 return {'audited_commit':BASE,'base_main':MAIN,'tracked_files':len(files),'tracked_bytes':sum(x['bytes'] for x in files),
   'PR_changed_files':len(diff),'PR_text_additions':adds,'PR_text_deletions':dels,'PR_binary_entries':binaries,
   'bytes_by_top_directory':dict(sizes),'largest_files':sorted(files,key=lambda x:x['bytes'],reverse=True)[:15],
   'exact_duplicate_groups':duplicate,'duplicate_excess_bytes':sum((x['copies']-1)*x['bytes_per_copy'] for x in duplicate),
   'zip_bytes_not_expanded_in_duplicate_totals':True,'core_dependencies':read(ROOT/'results/v0.3.0/evidence_ledger.json')['environment']['core_third_party_dependencies'],
   'recommendation':'Keep PR1 draft as provenance umbrella; request review in immutable phase/concern ranges or future stacked PRs using existing commits, without rewriting history or deleting frozen artifacts. New pilot uses a shared source ZIP rather than duplicating archives per stage.',
   'licenses_rechecked_by_notice_and_registry_only_not_legal_opinion':True}

def development():
 r=read(ROOT/'results/v0.3.0/development_qualification_all_candidates.json');out=[]
 for model,v in r.items():
  gs=v['groups']['unconstrained'];a={r['id']:r['verdict'] for r in gs['A_dev_standard']['rows']};b={r['id']:r['verdict'] for r in gs['A_dev_reverse']['rows']}
  def coarse(x):return 'accepting_group' if x in ACCEPT else x
  out.append({'model':model,'n':len(a),'exact_same_category':sum(a[k] is not None and a[k]==b[k] for k in a),
    'same_coarse_decision':sum(a[k] is not None and b[k] is not None and coarse(a[k])==coarse(b[k]) for k in a),
    'changed_within_accepting_group':sum(a[k]!=b[k] and a[k] in ACCEPT and b[k] in ACCEPT for k in a)})
 return {'kind':'post_hoc_development_diagnostic_not_requalification','historical_gate_unchanged':True,'rows':out,
   'interpretation':'Exact order consistency mixes verdict stability and evidence-type selection; coarse stability can conceal wrong evidence types. Neither metric retrospectively replaces the gate.'}

if __name__=='__main__':
 put('development_construct_audit.json',development());put('numerical_audit.json',numerical());put('false_acceptance_audit.json',sensitivity());put('release_audit.json',release())
 print('Historical numerical checks pass; acceptance-group invariance checked; release inventory recorded. No new model inference, human reviews or gold labels.')
