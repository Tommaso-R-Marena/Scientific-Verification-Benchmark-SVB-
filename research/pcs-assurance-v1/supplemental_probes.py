"""Post-run construction audit. Preserve primary18; new inputs explicitly supplemental."""
from pathlib import Path
import copy,hashlib,json,shutil
from sandbox import R,SUBJECT,execute
D=Path(__file__).parent;cs=json.loads((D/'cases.json').read_text());rows=[]
# S02 accidentally left the old number in the proposal: preserve it as a benchmark defect.
a=copy.deepcopy(next(c for c in cs if c['id']=='S02'));a['input']['id']='S02b';a['input']['proposal']['spec']['reported']='105.25'
# days is outside the lexical unit recognizer. Isolate variable binding using supported g.
b=copy.deepcopy(next(c for c in cs if c['id']=='S05'));b['input']['id']='S05b'
b['input']['csv']=b['input']['csv'].replace('age_at_hatching','dry_mass').replace('age_at_sampling','wet_mass')
b['input']['source']='The mean wet mass was 104.25 g (SD 2.94 g, n = 4).'
b['input']['proposal']={'quote':b['input']['source'],'spec':{'stat':'mean','column':'dry_mass','reported':'104.25','reported_unit':'g'}}
b['input']['manifest']['columns']={'dry_mass':{'unit':'g','aliases':['wet mass']},'wet_mass':{'unit':'g','aliases':['fresh mass']}}
b['input']['manifest']['sha256']=hashlib.sha256(b['input']['csv'].encode()).hexdigest()
for c in [a,b]:
 work=R/'results/local/pcs-assurance/supplemental'/c['input']['id'];work.mkdir(parents=True,exist_ok=False)
 (work/'input.json').write_text(json.dumps(c['input'],sort_keys=True,indent=2)+'\n');r=execute(work,['/usr/bin/python3','/worker.py'])
 record=json.loads((work/'bundle/records.json').read_text()) if (work/'bundle/records.json').exists() else []
 rows.append({'id':c['input']['id'],'input':c['input'],'execution':r,'records':record})
 print(c['input']['id'],r['returncode'],record[0]['outward']['verdict'] if record else None,flush=True)
# Same semantic decoy theorem, with the newline syntax recognized by the old runner.
work=R/'results/local/pcs-assurance/supplemental/forgery-newline';work.mkdir(parents=True,exist_ok=False)
original=(R/'results/local/pcs-assurance/artifact-probes/forged.lean').read_text()
(work/'forged.lean').write_text(original.replace(':= by\n  rfl',':=\n  rfl'))
for name,path in [('original_v11','research/claimcheck_v1_1/claimcheck_kernel_runner.py'),('existing_candidate_v2','research/claimcheck_assurance_v1/runner/claimcheck_kernel_runner_v2.py')]:
 r=execute(work,['/usr/bin/python3','/subject/'+path,'/work/forged.lean','--out','/work/'+name+'.json'])
 report=json.loads((work/(name+'.json')).read_text());rows.append({'id':'forgery_newline_'+name,'execution':r,'report':report})
 print(name,report['accepted'],report.get('why_not'),flush=True)
(D/'results/supplemental_probes.json').write_text(json.dumps({'kind':'post_primary_diagnostic_construction_audit_not_primary_rescore','primary_results_preserved':True,
 'benchmark_reference_defect':'S02 quote changed to105.25 but typed spec remained104.25. Primary reference mismatch expectation is invalid; no mathematical verdict was established. Keep it as defective_reference stratum.',
 'S05_limitation':'days unit literal unrecognized by source gates; new wet/dry-mass input tests semantic alias binding with supported unit.',
 'forgery_variation':'Initial syntactically different forged theorem not parsed; separate newline variant matches old runner statement regex. Neither modifies PCS.', 'rows':rows},sort_keys=True,indent=2)+'\n')
