"""Exact checks of Phase II source-record facts,not empirical adequacy or labels.

Independent of the evaluated subjects and model responses. These routines replay
registered source bytes and arithmetic; they cannot validate sampling assumptions,
original laboratory execution,causal/clinical interpretations or author judgments.
"""
from __future__ import annotations
import csv
import gzip
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import re
import struct

ROOT=Path(__file__).resolve().parents[2]

def rows(path):
    with path.open(newline='') as h:return list(csv.DictReader(h))
def mean(values):
    xs=[Q(str(x)) for x in values]
    if not xs:raise ValueError('empty measurement subset')
    return sum(xs,Q())/len(xs)
def ratio_text(x):return str(Q(x))

def source_measurements(root=ROOT):
    s=root/'data/v0.2.0/sources'
    peng=rows(s/'penguins_raw.csv')
    puro=rows(s/'Puromycin_extracted.csv')
    plant=rows(s/'CO2_plants_extracted.csv')
    free=rows(s/'freesolv_selected.csv')
    return peng,puro,plant,{r['name']:r for r in free}

def recompute(operation,root=ROOT):
    peng,puro,plant,free=source_measurements(root)
    if operation=='penguin_species_mass':
        result={}
        for name in ('Gentoo','Adelie'):
            vals=[Q(r['Body Mass (g)']) for r in peng if r['Species'].startswith(name) and r['Body Mass (g)']!='NA']
            result[name+'_n']=len(vals);result[name+'_sum_g']=str(sum(vals,Q()))
        result['gentoo_gt_adelie']=Q(result['Gentoo_sum_g'])/result['Gentoo_n']>Q(result['Adelie_sum_g'])/result['Adelie_n']
        return result
    if operation=='penguin_sex_mass':
        result={}
        for sex in ('MALE','FEMALE'):
            vals=[Q(r['Body Mass (g)']) for r in peng if r['Species'].startswith('Adelie') and r['Sex']==sex and r['Body Mass (g)']!='NA']
            result[sex+'_n']=len(vals);result[sex+'_sum_g']=str(sum(vals,Q()))
        return result
    if operation=='penguin_ids':
        return {'rows':len(peng),'unique_id':len({r['Individual ID'] for r in peng}),'unique_study_id':len({(r['studyName'],r['Individual ID']) for r in peng})}
    if operation=='holdout_fraction':
        # Primary article extract,not an independently rerun classifier.
        article=(root/'data/v0.2.0/sources/penguins_article.html').read_text()
        plain=re.sub('<[^>]+>',' ',article)
        if not re.search(r'39\s+out of\s+44',plain):raise ValueError('primary39/44source missing')
        return {'correct':39,'total':44,'percent_2dp':f'{100*39/44:.2f}'}
    if operation=='puromycin_mean_011':
        vals={state:mean([r['rate'] for r in puro if r['state']==state and Q(r['conc'])==Q('0.11')]) for state in ('treated','untreated')}
        return {'treated':str(vals['treated']),'untreated':str(vals['untreated']),'difference':str(vals['treated']-vals['untreated'])}
    if operation=='puromycin_high':
        return {state:[str(Q(r['rate'])) for r in puro if r['state']==state and Q(r['conc'])==Q('1.1')] for state in ('treated','untreated')}
    if operation=='puromycin_ratio':
        lo=mean([r['rate'] for r in puro if r['state']=='treated' and Q(r['conc'])==Q('0.02')]);hi=mean([r['rate'] for r in puro if r['state']=='treated' and Q(r['conc'])==Q('1.1')])
        return {'low':str(lo),'high':str(hi),'rate_ratio':str(hi/lo),'concentration_ratio':str(Q('1.1')/Q('0.02'))}
    if operation=='puromycin_counts':return dict(Counter(r['state'] for r in puro))
    if operation=='grass_qn1':
        lookup={r['conc']:Q(r['uptake']) for r in plant if r['Plant']=='Qn1'}
        return {'350':str(lookup['350']),'500':str(lookup['500']),'difference':str(lookup['500']-lookup['350'])}
    if operation=='grass_counts':
        counts=Counter(r['Plant'] for r in plant)
        if len(set(counts.values()))!=1:raise ValueError('unequal repeated measures')
        return {'plants':len(counts),'rows':len(plant),'per_plant':next(iter(counts.values()))}
    if operation in ('grass_mississippi_1000','grass_quebec_1000'):
        origin='Mississippi' if 'mississippi' in operation else 'Quebec'
        return {state:str(mean([r['uptake'] for r in plant if r['Type']==origin and r['Treatment']==state and Q(r['conc'])==1000])) for state in ('nonchilled','chilled')}
    if operation=='freesolv_values':
        a=Q(free['ethanol']['experimental_kcal_mol']);b=Q(free['methane']['experimental_kcal_mol'])
        return {'ethanol':str(a),'methane':str(b),'difference':str(a-b)}
    if operation=='freesolv_residual':
        c=free['triethylphosphate'];a=Q(c['calculated_kcal_mol']);b=Q(c['experimental_kcal_mol'])
        return {'compound':'triethylphosphate','calculated':str(a),'experimental':str(b),'residual':str(a-b)}
    if operation=='freesolv_default':
        c=free['methanol'];return {'compound':'methanol','uncertainty':str(Q(c['experimental_uncertainty_kcal_mol'])),'default_note':'assigned a default value' in c['notes']}
    if operation=='freesolv_equal':
        c=free['neopentane'];return {'compound':'neopentane','experimental':str(Q(c['experimental_kcal_mol'])),'calculated':str(Q(c['calculated_kcal_mol'])),'experimental_uncertainty':str(Q(c['experimental_uncertainty_kcal_mol'])),'calculated_uncertainty':str(Q(c['calculated_uncertainty_kcal_mol']))}
    raise ValueError('unknown operation:'+operation)

def verify_source_transformations(root=ROOT):
    s=root/'data/v0.2.0/sources'
    # Check extracted Puromycin cells against two named vectors in official R
    # source,never by evaluating that code.
    rsource=(s/'Puromycin.R').read_text()
    puro=rows(s/'Puromycin_extracted.csv')
    for field,variable in [('conc','conc'),('rate','vel')]:
        m=re.search(r'\b'+variable+r'\s*=\s*c\((.*?)\)',rsource,re.S)
        nums=[Q(t.strip()) for t in m[1].split(',')]
        if nums!=[Q(r[field]) for r in puro]:raise ValueError('Puromycin source cells changed')
    # BoundedRDX2 numeric-vector matching; compare all84raw IEEE754 records.
    raw=gzip.decompress((s/'CO2.rda').read_bytes());plant=rows(s/'CO2_plants_extracted.csv')
    tag=struct.pack('>ii',14,84);hits=[];offset=0
    while (offset:=raw.find(tag,offset))>=0:
        hits.append(struct.unpack('>84d',raw[offset+8:offset+680]));offset+=1
    if len(hits)!=2:raise ValueError('CO2 source vector count changed')
    for key,data in zip(('conc','uptake'),hits):
        if [float(r[key]) for r in plant]!=list(data):raise ValueError('CO2 numeric cells changed')
    # Check FreeSolv selected records against the exact published-reference rows
    # and reject use of records referencing unpublished measurements.
    original={}
    for line in (s/'freesolv_database.txt').read_text().splitlines():
        if line and not line.startswith('#'):
            cells=[v.strip() for v in line.split(';',9)];original[cells[0]]=cells
    for row in rows(s/'freesolv_selected.csv'):
        a=original[row['id']]
        if list(row.values())!=a:raise ValueError('FreeSolv selected row altered')
        if not row['experimental_reference'].startswith('10.'):raise ValueError('nonpublished source selected')
    return {'Puromycin_cells':len(puro)*3,'CO2_numeric_cells':len(plant)*2,'FreeSolv_rows':6}

def validate(root=ROOT):
    d=root/'data/v0.2.0';registry=json.loads((d/'registry.json').read_text());cases=json.loads((d/'cases.json').read_text())
    for source in registry['sources'].values():
        for a in source['artifacts']:
            p=(root/a['path']).resolve()
            if not p.is_relative_to((d/'sources').resolve()):raise ValueError('source path escape')
            if hashlib.sha256(p.read_bytes()).hexdigest()!=a['sha256']:raise ValueError('source hash mismatch:'+a['path'])
    transformation=verify_source_transformations(root)
    checked=[]
    for c in cases:
        check=c['reference'].get('numeric_check')
        if check:
            got=recompute(check['operation'],root)
            if got!=check['expected']:raise ValueError('numeric witness mismatch:'+c['id']+':'+repr(got))
            checked.append({'id':c['id'],'operation':check['operation'],'result':got})
    return {'source_hashes_valid':True,'numeric_witnesses_checked':len(checked),'transformations':transformation,'checks':checked,'empirical_adequacy_mechanically_validated':False,'external_human_adjudication':False}

if __name__=='__main__':print(json.dumps(validate(),indent=2,sort_keys=True))
