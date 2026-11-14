#!/usr/bin/env python3
"""Construct ONLY new SVB0.3.0 source-family packets before parent freeze.

Official R dataset snapshots are parsed as data,never executed. Historical0.1/0.2
files,models,evaluated repositories and environment configuration are untouched.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from svb.phase2b_references import source_rows
DEST=ROOT/'data/v0.3.0';SRC=DEST/'sources'
CASES=[]
CONDITIONS=('evidence','no_evidence','no_assumptions','verified_numbers','paraphrase')


def write_json(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
def table(rows,fields):
    out=io.StringIO();w=csv.writer(out,lineterminator='\n');w.writerow(fields)
    for r in rows:w.writerow([r[f] for f in fields])
    return out.getvalue()
def doc(ident,title,text,source):return {'id':ident,'title':title,'text':text,'source_id':source}

def add(ident,family,claim,documents,label,scopes,rationale,requirements,uncertainty,pair,role,kind,check=None):
    c={'id':ident,'family':family,'split':'evaluation','pair':{'id':pair,'role':role},
       'packet':{'question':'Which epistemic status is justified for this precise claim by the supplied scientific record?',
                 'claim':claim,'documents':documents,
                 'methodology':'Read the source description and recorded observations. Check any calculation using the stated units and experimental identifiers. Assess the precise target claim and explain its evidential basis.',
                 'assumptions':['For arithmetic, treat the displayed stored values as exact numerical inputs; this does not make the physical measurements exact.']},
       'reference':{'label':label,'scopes':scopes,'rationale':rationale,'evidence_ids':[d['id'] for d in documents],
                    'reasoning_requirements':requirements,'uncertainty':uncertainty,'status':'provisional_author_adjudicated','kind':kind,
                    'condition_labels':{k:('insufficient_evidence' if k=='no_evidence' else label) for k in CONDITIONS},
                    'condition_scopes':{k:([] if k=='no_evidence' else scopes) for k in CONDITIONS}}}
    if check:c['reference']['numeric_check']=check
    CASES.append(c)


def build():
    data=source_rows(ROOT)
    for name,rs in data.items():(SRC/(name+'_extracted.csv')).write_text(table(rs,list(rs[0])))
    sleepdoc=doc('SL-OBS','Recorded sleep prolongation observations',table(data['sleep'],['ID','group','extra']),'sleep')
    sleepmethod=doc('SL-METHOD','R datasets documentation of the historical sleep study',
      'The R datasets manual describes the sleep data as the effect of two soporific drugs: increase in hours of sleep compared with control on 10 patients. The column extra is the increase in hours; group identifies the drug and ID identifies the patient. The manual explicitly states that the group name may be misleading: these are measurements on 10 persons, not separate groups. The data have 20 observations. The source citations are Cushny and Peebles (1905) and Student (1908). This packet transcribes the public R dataset and its documentation.', 'sleep')
    su='Curated historical R transcription, not an independent replication of the original experiment. Full primary protocols, treatment ordering, washout, measurement error and population sampling were not independently reconstructed. Exact calculations establish properties of recorded observations only.'
    sleepcheck={'operation':'sleep_paired_mean','expected':{'pairs':10,'sum_difference_hours':'79/5','mean_difference_hours':'79/50'}}
    add('SL01P','sleep','Using patient ID to pair the recorded observations, the mean of drug 2 minus drug 1 sleep prolongation is 1.58 hours.',[sleepmethod,sleepdoc],
      'computationally_established',['computational'],'Ten within-ID differences sum to 15.8 hours, giving an arithmetic mean of 1.58 hours.',
      ['Pair records by patient ID rather than treating group labels as different persons.','Compute the mean within-patient difference with hours as the unit.'],su,'SL01','positive','exact',sleepcheck)
    add('SL01X','sleep','Using patient ID to pair the recorded observations, the mean of drug 2 minus drug 1 sleep prolongation is 3.16 hours.',[sleepmethod,sleepdoc],
      'refuted',[],'The recorded paired differences have mean 79/50 = 1.58 hours, contradicting the proposed 3.16-hour mean.',
      ['Compute the paired mean rather than accepting a plausible supplied number.','Identify the numerical contradiction without making a population-level treatment claim.'],su,'SL01','negative','exact',sleepcheck)
    signcheck={'operation':'sleep_signs','expected':{'greater':9,'equal':1,'less':0,'pairs':10}}
    add('SL02N','sleep','In every recorded patient pair, the sleep prolongation under drug 2 is at least as large as under drug 1.',[sleepmethod,sleepdoc],
      'empirically_supported',['empirical','computational'],'Nine recorded paired differences are positive and one is zero. No recorded patient has a negative drug-2-minus-drug-1 difference.',
      ['Check all 10 patient pairs.','Preserve the non-strict comparison and scope to recorded patients.'],su,'SL02','narrow','empirical_source_fact',signcheck)
    add('SL02S','sleep','The recorded patient comparisons establish that drug 2 will increase sleep more than drug 1 for every future patient.',[sleepmethod,sleepdoc],
      'insufficient_evidence',[],'A finite historical sample does not establish a strict benefit for every future patient; sampling, heterogeneity and applicability remain unestablished. One observed tie also prevents describing all recorded differences as strict increases, but it does not refute the separate universal future-patient target.',
      ['Identify the shift from a finite recorded sample to every future patient.','Explain why finite favorable observations do not establish a universal individual treatment response; do not claim the future outcome has been observed false.'],su,'SL02','stronger','interpretation')
    chickmethod=doc('CW-METHOD','R documentation of early chick growth observations',
      'The R ChickWeight dataset describes an experiment on early growth under four protein diets. Body weight is recorded in grams; Time is days since birth; Chick is a unique chick identifier; Diet identifies the experimental diet. Weights were measured at birth and every second day until day 20, and also at day 21. The complete curated table has 578 observations. The R source cites Crowder and Hand (1990), Example 5.3, pages 74–78, and Hand and Crowder (1996), Table A.2, page 172. Ordered factor labels identify chicks; factor ordering groups diets and orders final weights.', 'chick_growth')
    day21=[r for r in data['chick_growth'] if r['Time']=='21' and r['Diet'] in {'1','4'}]
    chick21=doc('CW-DAY21','Recorded day-21 weights for diets 1 and 4',table(day21,['Chick','Diet','Time','weight']),'chick_growth')
    cu='Curated textbook/R observations rather than verified original laboratory records. Missing follow-up and selection are not resolved by a complete-case sample mean. Full diet composition, assignment, husbandry, original uncertainty and laboratory protocol were not independently obtained. No population-level causal effect is established by the stored-number arithmetic.'
    chickcheck={'operation':'chick_day21','expected':{'diet1_n':16,'diet1_mean_g':'711/4','diet4_n':9,'diet4_mean_g':'2147/9','diet4_minus_diet1_g':'2189/36'}}
    add('CW01P','chick_growth','Among the supplied day-21 observations, the arithmetic mean weight for diet 4 exceeds that for diet 1 by exactly 2189/36 grams.',[chickmethod,chick21],
      'computationally_established',['computational'],'The 16 observed diet-1 weights have mean 711/4 g; the 9 observed diet-4 weights have mean 2147/9 g. Their difference is 2189/36 g.',
      ['Use only supplied day-21 observations and their unequal denominators.','Subtract the diet-1 mean from the diet-4 mean without treating arithmetic exactness as physical precision.'],cu,'CW01','positive','exact',chickcheck)
    add('CW01X','chick_growth','Among the supplied day-21 observations, the arithmetic mean weight for diet 4 is lower than that for diet 1.',[chickmethod,chick21],
      'refuted',[],'The recorded means are 2147/9 g for diet 4 and 711/4 g for diet 1; diet 4 is higher, so the target reverses the sample comparison.',
      ['Compute the two sample means with correct denominators.','Identify the reversed inequality, retaining the observed-sample scope.'],cu,'CW01','negative','exact',chickcheck)
    chickone=doc('CW-CHICK1','Recorded growth series for chick 1',table([r for r in data['chick_growth'] if r['Chick']=='1'],['Chick','Diet','Time','weight']),'chick_growth')
    gaincheck={'operation':'chick_one_growth','expected':{'chick':'1','birth_g':'42','day21_g':'205','observed_gain_g':'163'}}
    add('CW02N','chick_growth','The recorded body weight of chick 1 increased from 42 grams at birth to 205 grams on day 21 while it received diet 1.',[chickmethod,chickone],
      'empirically_supported',['empirical','computational'],'The supplied series records 42 g at Time 0 and 205 g at Time 21 for chick 1, whose Diet value is 1. This describes a within-chick observed change.',
      ['Match the same chick ID and the two measurement times.','Describe observed growth under diet 1 without assigning all growth causally to that diet.'],cu,'CW02','narrow','empirical_source_fact',gaincheck)
    add('CW02S','chick_growth','The growth series of chick 1 establishes that diet 1 caused exactly 163 grams of additional body weight compared with what this chick would have weighed without diet 1.',[chickmethod,chickone],
      'insufficient_evidence',[],'An observed within-chick change is not an observed counterfactual diet effect. Development with age and other husbandry conditions can accompany the same series; the unobserved alternative weight is not identified.',
      ['Distinguish a temporal gain of 163 g from a counterfactual causal contrast.','Identify the unobserved alternative-diet outcome or adequate causal design that would be needed, without asserting the treatment effect is zero.'],cu,'CW02','stronger','interpretation')
    boddoc=doc('OD-OBS','Recorded biochemical oxygen demand table',table(data['oxygen_demand'],['Time','demand']),'oxygen_demand')
    bodmethod=doc('OD-METHOD','R documentation of biochemical oxygen demand observations',
      'The R BOD dataset contains six observations of biochemical oxygen demand versus time in an evaluation of water quality. Time is the measurement time in days; demand is biochemical oxygen demand in mg/l. The R source attributes the data to Marske (1967), reproduced in Bates and Watts (1988), Appendix A1.4, page 270. The documentation illustrates fitting an asymptotic first-order curve to the recorded values.', 'oxygen_demand')
    ou='The small table is a curated historical transcription, not independently verified raw water-sample or laboratory records. No replicate structure, organism identification, experimental error model or physical mechanism is independently established here. Recorded nonmonotonicity alone need not be nonmonotonicity of an underlying latent process.'
    bodcheck={'operation':'oxygen_change','expected':{'day1_mg_per_L':'83/10','day7_mg_per_L':'99/5','difference_mg_per_L':'23/2','difference_g_per_L':'23/2000'}}
    add('OD01P','oxygen_demand','The recorded demand on day 7 minus the recorded demand on day 1 equals 0.0115 grams per litre.',[bodmethod,boddoc],
      'computationally_established',['computational'],'The stored difference is 19.8 - 8.3 = 11.5 mg/L. Dividing by 1000 gives 0.0115 g/L.',
      ['Subtract the two recorded values.','Convert milligrams to grams using 1000 mg = 1 g while retaining the per-litre denominator.'],ou,'OD01','positive','exact',bodcheck)
    add('OD01X','oxygen_demand','The recorded demand on day 7 minus the recorded demand on day 1 equals 11.5 grams per litre.',[bodmethod,boddoc],
      'refuted',[],'The difference is 11.5 mg/L, not 11.5 g/L. The target is 1000 times the stored difference expressed in g/L.',
      ['Check the original mg/L unit.','Identify the factor-1000 conversion error, not merely the subtraction.'],ou,'OD01','negative','exact',bodcheck)
    dropcheck={'operation':'oxygen_nonmonotone','expected':{'day3_mg_per_L':'19','day4_mg_per_L':'16','drop_mg_per_L':'3','nonmonotone':True}}
    add('OD02N','oxygen_demand','The recorded oxygen-demand values decrease between day 3 and day 4.',[bodmethod,boddoc],
      'empirically_supported',['empirical','computational'],'The table records 19 mg/L at day 3 and 16 mg/L at day 4, a decline in these observations.',
      ['Locate the two specified observations.','Limit the statement to the recorded data rather than a noiseless latent process or mechanism.'],ou,'OD02','narrow','empirical_source_fact',dropcheck)
    add('OD02S','oxygen_demand','The observed day-3 to day-4 decline uniquely establishes that the microorganisms in the water stopped aerobic respiration during that interval.',[bodmethod,boddoc],
      'insufficient_evidence',[],'A pair of demand readings does not uniquely identify microbial respiration or its cessation. Measurement variation, sampling and alternative processes remain compatible with the same recorded decline.',
      ['Distinguish a measured decrease from a unique biological mechanism.','Give at least one compatible alternative and avoid asserting that respiration actually ceased or certainly did not cease.'],ou,'OD02','stronger','interpretation')
    write_json(DEST/'cases.json',CASES)
    registry()
    dossier()


def registry():
    revision=json.loads((SRC/'R_revision.json').read_text())['commit']
    titles={'sleep':'Historical paired sleep-prolongation study','chick_growth':'Longitudinal early chick growth under protein diets','oxygen_demand':'Historical biochemical oxygen demand time series'}
    stems={'sleep':'sleep','chick_growth':'ChickWeight','oxygen_demand':'BOD'}
    citations={'sleep':['Cushny and Peebles (1905)','Student (1908), The probable error of a mean, Biometrika 6:1–25'],
               'chick_growth':['Crowder and Hand (1990), Analysis of Repeated Measures, Example 5.3, pages 74–78','Hand and Crowder (1996), Practical Longitudinal Data Analysis, Table A.2, page 172'],
               'oxygen_demand':['Marske (1967), as cited by the R BOD documentation','Bates and Watts (1988), Nonlinear Regression Analysis and Its Applications, Appendix A1.4, page 270']}
    sources={}
    for name,stem in stems.items():
        files=[stem+'.R',stem+'.Rd',name+'_extracted.csv','R_COPYING','r_datasets_DESCRIPTION.in','R_revision.json']
        sources[name]={'title':titles[name],'study_family':name,'source_type':'curated_historical_experimental_transcription','license':'GPL-2.0-or-later',
            'license_evidence':[stem+'.Rd','R_COPYING','r_datasets_DESCRIPTION.in'],
            'url':f'https://raw.githubusercontent.com/wch/r-source/{revision}/src/library/datasets/data/{stem}.R',
            'documentation_url':f'https://raw.githubusercontent.com/wch/r-source/{revision}/src/library/datasets/man/{stem}.Rd',
            'accessed':'2026-11-14','upstream_commit':revision,'original_source_citations':citations[name],'split':'evaluation',
            'transformation':'Parse only explicit numeric R vectors without evaluation; sleep grouping follows checked gl/rep.int declarations; Chick integer factor codes map through explicit source labels; write canonical CSV with decimal strings preserved.',
            'limitations':'The public R data and manuals are secondary scientific transcriptions. Original laboratory records and complete primary methods were not independently obtained. GPL source and documentation notices apply to these files rather than SVB Apache code license.',
            'artifacts':[{'path':'data/v0.3.0/sources/'+name,'sha256':hashlib.sha256((SRC/name).read_bytes()).hexdigest(),'bytes':(SRC/name).stat().st_size} for name in files]}
    write_json(DEST/'registry.json',{'version':'0.3.0','sources':sources,
        'adjudication':'provisional_author_adjudicated',
        'scope':'Three additional study families, all evaluation; historical v0.2.0 is development/historical context only. These public classic datasets are not secret, unseen-to-training or independently blinded.'})


def dossier():
    s='''# Phase IIb: additional source families for SVB0.3.0\n\nThis12-case extension contains six matched pairs from three scientific studies not used in SVB0.2.0. The studies are all public R datasets and may be familiar to pretrained systems. A new study-family split is not a hidden set, proof of training noncontamination, or blinded adjudication. The frozen0.2.0 release remains historical/development material; none of its files is changed.\n\n## Provenance,license and scientific limits\n\nOfficial R source commit95b95f1a200c97a9aa027fe020263d2493141526 is archived by content hash in the new registry. Each dataset’s manual explicitly says it is distributed under GPL2or later. COPYING and package DESCRIPTION are retained. These source/data files remain GPL2-or-later and are not relicensed as Apache. No primary laboratory dataset was manufactured, and no evaluated-system output informed labels.\n\n- **Sleep**:20records for10persons,paired across two soporific drugs; extra is hours of sleep increase compared with control. The manual warns group does not mean independent groups. Source citations Cushny and Peebles1905and Student1908are preserved;full primary treatment ordering,washout and sampling details were not independently reconstructed.\n- **ChickWeight**:578growth observations on50chicks,with recorded protein diet,age in days and body weight in grams. Sources Crowder and Hand1990and Hand and Crowder1996are textbook transcriptions cited by R. An important transformation is source integer factor-code→explicit chick-ID label mapping. Raw integer code15names chick1,not chick15. Day21diet1and4observed sample sizes differ16versus9;complete-case means do not establish survival-adjusted or population causal effects.\n- **BOD**:six recorded biochemical oxygen-demand values in mg/L versus days,attributed by R to Marske1967via Bates and Watts1988AppendixA1.4. Original water source,replication,organisms,error model and original methods are not independently verified. A nonmonotone observed segment does not uniquely establish a microbial mechanism.\n\nAll12labels are provisional author adjudications. Exact checks establish source-record and arithmetic properties;they do not validate laboratories,physical precision,clinical benefit,causal identification or population generalization. Narrow observed comparisons have empirical and computational allowed scopes;exact sample means and unit conversions use computationally_established. False numeric conclusions are refuted;unsupported causal/universal/mechanistic conclusions are insufficient_evidence.\n\n## Variant policy\n\nFor evidence,no_assumptions,verified_numbers and paraphrase,the legitimate source observations and method facts remain available,so the reference label is unchanged. Separate assumptions only remind the reader of stored-number arithmetic. With every evidence document removed,the packet contains neither observed values nor an independently admitted record:every no_evidence reference is insufficient_evidence with empty scopes. This applies to originally refuted claims too and measures justification conditional on admitted evidence,not factual memory. Labels,checks,pair roles and missing-evidence analyses are never model inputs. Source documents contain legitimate methods/data,not adjudicator-written absent-evidence checklists.\n\n## Dossiers\n\n'''
    for c in CASES:
        r=c['reference'];s+=f'### {c["id"]}: {r["label"]}\n\nTarget: {c["packet"]["claim"]}\n\nEvidence: '+', '.join(r['evidence_ids'])+';source family '+c['family']+'.\n\nReference: '+r['rationale']+'\n\nCriteria:\n\n'+''.join('- '+x+'\n' for x in r['reasoning_requirements'])+'\nLimitations: '+r['uncertainty']+'\n\n'
        if 'numeric_check' in r:s+='Exact witness: `'+json.dumps(r['numeric_check'],sort_keys=True)+'`.\n\n'
    s+='## Reproduction and review needs\n\nRun `PYTHONPATH=src python -m svb.phase2b_references` and the new `tests/test_phase2b_references.py` suite. Numeric witnesses are fixed independently of model responses and checked against source-derived tables. No external domain panel has adjudicated category boundaries. Reviewers should challenge the empirical-versus-computational label interpretation,the secondary nature of every source,classic-dataset contamination,small study-family count,complete-case chick selection,and authored strong-claim wording. No population performance conclusion follows from twelve cases.\n'
    (ROOT/'docs/phase-iib/new_sources.md').write_text(s)

if __name__=='__main__':build()
