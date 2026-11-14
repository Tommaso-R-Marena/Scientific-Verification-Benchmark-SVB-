#!/usr/bin/env python3
"""Construct author-adjudicated SVB 0.2 packets from pinned public source snapshots.

No evaluated-system outputs, API calls, or executable source evaluation occur.
This script writes only v0.2 files and its new dossier. Do not run after freeze
without a separately versioned dataset revision.
"""
from __future__ import annotations
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import struct
from fractions import Fraction as Q

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'data/v0.2.0'
SRC=DEST/'sources'
DATE='2026-11-14'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(p,obj): p.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
def table(rows,columns):
    out=io.StringIO();w=csv.writer(out,lineterminator='\n');w.writerow(columns)
    for row in rows:w.writerow([row[k] for k in columns])
    return out.getvalue()

def plant_rows():
    """Decode only known vector records from this pinned RDX2 data snapshot.

    It is not a general R serializer and never invokes R code. Vector tags,
    lengths, all level strings and concentration grid are checked explicitly.
    """
    b=gzip.decompress((SRC/'CO2.rda').read_bytes())
    if not b.startswith(b'RDX2\nX\n'): raise ValueError('unsupported R format')
    def vectors(flags,code):
        tag=struct.pack('>ii',flags,84);hits=[];start=0
        while (start:=b.find(tag,start))>=0:
            size=8 if code=='d' else 4
            hits.append(struct.unpack('>'+code*84,b[start+8:start+8+size*84]));start+=1
        return hits
    factors=vectors(781,'i');nums=vectors(14,'d')
    if len(factors)!=3 or len(nums)!=2:raise ValueError('unexpected vectors')
    levels=[['Qn1','Qn2','Qn3','Qc1','Qc3','Qc2','Mn3','Mn2','Mn1','Mc2','Mc3','Mc1'],['Quebec','Mississippi'],['nonchilled','chilled']]
    for ll in levels:
        for s in ll:
            if struct.pack('>ii',262153,len(s))+s.encode() not in b:raise ValueError('missing factor label')
    rows=[]
    for i in range(84):
        rows.append({'Plant':levels[0][factors[0][i]-1],'Type':levels[1][factors[1][i]-1],
                     'Treatment':levels[2][factors[2][i]-1],'conc':format(nums[0][i],'.12g'),'uptake':format(nums[1][i],'.12g')})
    if any([Q(r['conc']) for r in rows if r['Plant']==p]!=[95,175,250,350,500,675,1000] for p in levels[0]):raise ValueError('wrong concentration grid')
    return rows

def puro_rows():
    s=(SRC/'Puromycin.R').read_text()
    def vector(name):
        m=re.search(r'\b'+name+r'\s*=\s*c\((.*?)\)',s,re.S)
        if not m:raise ValueError(name)
        return [x.strip() for x in m[1].split(',')]
    conc=vector('conc');rate=vector('vel')
    if len(conc)!=23 or len(rate)!=23:raise ValueError('Puromycin shape')
    return [{'conc':c,'rate':r,'state':'treated' if i<12 else 'untreated'} for i,(c,r) in enumerate(zip(conc,rate))]

def freesolv_rows():
    fields=['id','smiles','name','experimental_kcal_mol','experimental_uncertainty_kcal_mol','calculated_kcal_mol','calculated_uncertainty_kcal_mol','experimental_reference','calculated_reference','notes']
    result=[]
    for s in (SRC/'freesolv_database.txt').read_text().splitlines():
        if not s.strip() or s.startswith('#'):continue
        vals=[x.strip() for x in s.split(';',9)]
        if len(vals)!=10:raise ValueError('FreeSolv format')
        result.append(dict(zip(fields,vals)))
    return result

def doc(ident,title,text,source):return {'id':ident,'title':title,'text':text,'source_id':source}

CASES=[]
DOSSIERS=[]
QUESTION='What epistemic status does the supplied evidence justify for this exact claim? Distinguish measured observations, calculations, assumptions, and stronger scientific interpretations.'

def case(ident,family,split,claim,documents,assumptions,label,scopes,rationale,requirements,uncertainty,kind,pair,role,numeric=None):
    c={'id':ident,'family':family,'split':split,
       'packet':{'question':QUESTION,'claim':claim,'documents':documents,
                 'methodology':'Read the supplied source excerpts and measurement tables. Check any arithmetic directly from the observations. Evaluate only the exact proposed claim; distinguish a failure of evidence from a contradiction.',
                 'assumptions':assumptions},
       'reference':{'label':label,'scopes':scopes,'rationale':rationale,'evidence_ids':[d['id'] for d in documents],
                    'reasoning_requirements':requirements,'uncertainty':uncertainty,'status':'provisional_author_adjudicated','kind':kind,
                    'condition_labels':{k:('insufficient_evidence' if k=='no_evidence' else label) for k in ('evidence','no_evidence','no_assumptions','verified_numbers','paraphrase')},
                    'condition_scopes':{k:([] if k=='no_evidence' else scopes) for k in ('evidence','no_evidence','no_assumptions','verified_numbers','paraphrase')}},
       'pair':{'id':pair,'role':role}}
    if numeric:c['reference']['numeric_check']=numeric
    CASES.append(c)
    DOSSIERS.append((ident,label,rationale,requirements,uncertainty,numeric))
    return c

def paired(ident,family,split,docs,assumptions,narrow,strong,label,scopes,rationale,requirements,uncertainty,numeric=None,strong_rationale=None,strong_requirements=None):
    case(ident+'N',family,split,narrow,docs,assumptions,label,scopes,rationale,requirements,uncertainty,'empirical_source_fact' if label=='empirically_supported' else 'exact',ident,'narrow',numeric)
    case(ident+'S',family,split,strong,docs,assumptions,'insufficient_evidence',[],strong_rationale or 'The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.',strong_requirements or ['Identify the exact scope extension.','Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.'],uncertainty,'interpretation',ident,'stronger')

def build():
    peng=list(csv.DictReader((SRC/'penguins_raw.csv').open()))
    puro=puro_rows();plants=plant_rows();free=freesolv_rows()
    (SRC/'Puromycin_extracted.csv').write_text(table(puro,['conc','rate','state']))
    (SRC/'CO2_plants_extracted.csv').write_text(table(plants,['Plant','Type','Treatment','conc','uptake']))
    chosen=[r for r in free if r['name'] in {'methane','methanol','ethanol','benzene','neopentane','triethylphosphate'}]
    if len(chosen)!=6:raise ValueError('missing FreeSolv examples')
    (SRC/'freesolv_selected.csv').write_text(table(chosen,list(chosen[0])))
    pcontext=doc('PG-METHOD','Palmer observational sampling and measurement context',
      'Gorman, Williams and Fraser (2014), PLOS ONE 9:e90081, DOI10.1371/journal.pone.0090081, and Palmer LTER dataset excerpts. Adult penguins were sampled at nests near Palmer Station during2007–2009; raw Stage values are Adult,1 Egg Stage. Body Mass(g), Species, Sex, Island and studyName are recorded fields. This is an observational breeding-season sample. Missing values are NA. The paper states body mass results are relevant to the egg-laying period and should not be considered representative of chick rearing or outside the breeding season.', 'penguins')
    punc='Field observations at the recorded breeding stage and sites; missingness, selection, year dependence and measurement errors are not resolved by an exact sample summary. Source record correctness is assumed; independent expert adjudication has not occurred.'
    ptable=doc('PG-MASS','Recorded species and body mass, all344 rows',table(peng,['Species','Body Mass (g)']),'penguins')
    paired('PG01','penguins','dev',[pcontext,ptable],['Use nonmissing recorded body masses and the arithmetic mean; do not impute NA.'],
      'For the nonmissing recorded observations, Gentoo penguins have a higher mean body mass than Adélie penguins.',
      'The observed species difference proves that moving an Adélie penguin to Biscoe Island would cause its mass to become that of a Gentoo penguin.',
      'empirically_supported',['empirical'],'The measured sample means are624350/123g for Gentoo and558800/151g for Adélie, so the stated descriptive comparison is supported.',
      ['Exclude the two NA body masses.','Compute the species-specific sample means and limit the comparison to these observations.'],punc,
      {'operation':'penguin_species_mass','expected':{'Gentoo_n':123,'Gentoo_sum_g':'624350','Adelie_n':151,'Adelie_sum_g':'558800','gentoo_gt_adelie':True}},
      'Species and islands were not randomized, and a cross-species association cannot identify an intervention on one individual. Genetic, sex, age, diet and other factors remain compatible explanations.',
      ['Identify the observational design and species-versus-intervention mismatch.','Do not call the descriptive species difference a measured causal effect of relocation.'])
    sexrows=[r for r in peng if r['Species'].startswith('Adelie') and r['Sex'] in {'MALE','FEMALE'}]
    sexdoc=doc('PG-SEX','Adélie records with identified sex',table(sexrows,['studyName','Sex','Body Mass (g)']),'penguins')
    paired('PG02','penguins','dev',[pcontext,sexdoc],['Describe only the records with identified sex and nonmissing body mass.'],
      'In these sex-identified Adélie observations, the male mean body mass exceeds the female mean body mass.',
      'These egg-laying-period observations establish the same male–female mass difference during every season throughout Antarctica.',
      'empirically_supported',['empirical'],'There are73 male masses summing295175g and73 female masses summing245925g; the observed means differ by49250/73g.',
      ['Compare sex-specific averages with their denominators.','Distinguish the observed conditional sample comparison from all-season extrapolation.'],punc,
      {'operation':'penguin_sex_mass','expected':{'MALE_n':73,'MALE_sum_g':'295175','FEMALE_n':73,'FEMALE_sum_g':'245925'}})
    iddoc=doc('PG-ID','Raw study and individual identifiers',table(peng,['studyName','Individual ID']),'penguins')
    paired('PG03','penguins','dev',[pcontext,iddoc],['Strings identify records only as documented; do not assume identifier stability across studies.'],
      'The supplied table has344 records,190 distinct Individual ID strings, and344 distinct(studyName,Individual ID) pairs.',
      'Repeated Individual ID strings across studies establish that these are repeated measurements of the same animals and allow individual growth rates to be inferred.',
      'computationally_established',['computational','provenance'],'Counting rows and exact strings establishes the stated table properties. The source packet does not establish a cross-study animal-linkage key.',
      ['Count records, unique ID strings and composite keys.','Do not confuse a repeated string with documented longitudinal identity.'],punc,
      {'operation':'penguin_ids','expected':{'rows':344,'unique_id':190,'unique_study_id':344}})
    holdout=doc('PG-HOLDOUT','Primary article held-out classification result',
      'Gorman etal.(2014) Results, Sex classification, states: "all supported models accurately predicted sex for39 out of44 individuals(88.64%,Table1)" for Adélie penguins at probability threshold0.50. Methods states that structural-size models were developed using a randomly chosen two-thirds subset and assessed on a one-third subset not included in developing the models. Reported denominators are44 Adélie,18 chinstrap and38 gentoo; the outcome is classification of sex in the study population, not disease, survival or clinical efficacy. Excerpt numerals are normalized with spacing; see archived primary article for the exact typography.', 'penguins_article')
    paired('PG04','penguins','dev',[pcontext,holdout],['Read the result as a reported held-out within-study classification result, not independently reproduced model performance.'],
      'The primary article reports39 correct classifications out of44 held-out Adélie individuals, approximately88.64%,under its stated sex-classification procedure.',
      'The reported held-out accuracy establishes88.64%classification accuracy for any future penguin population, species and seasonal stage.',
      'empirically_supported',['empirical'],'The primary article directly reports the held-out result and39/44 rounds to88.64%. This supports the precise reporting claim, not an independently replicated predictor.',
      ['Identify39/44 and the within-study held-out procedure.','Preserve the task(population sex classification)and reported-result qualification.'],punc,
      {'operation':'holdout_fraction','expected':{'correct':39,'total':44,'percent_2dp':'88.64'}})
    pudoc=doc('PU-DATA','Recorded Puromycin enzyme-reaction data',table(puro,['conc','rate','state']),'puromycin')
    puctx=doc('PU-METHOD','R source documentation of enzyme experiment',
      'R datasets Puromycin documents substrate concentration in ppm and instantaneous reaction rate in counts/min/min. It says counts per minute of radioactive product were measured as a function of substrate concentration, then initial reaction velocity was calculated. The experiment was conducted once with enzyme treated with Puromycin and once untreated. There are23 rows. Source: Treloar(1974), as reproduced in Bates and Watts(1988), AppendixA1.3; curated R source transcription.', 'puromycin')
    puunc='Curated transcription of a historical enzyme experiment; the original thesis and full laboratory protocol were not obtained. The two readings at many concentrations do not establish independent biological replication. No patient data, molecular binding assay or original measurement uncertainty is supplied.'
    paired('PU01','puromycin','evaluation',[puctx,pudoc],['Compare the reported readings only; preserve ppm and counts/min/min units.'],
      'At recorded concentration0.11ppm,the treated mean reaction rate is131counts/min/min and the untreated mean is106.5counts/min/min.',
      'The difference at0.11ppm establishes a precisely estimated population-average treatment effect across independent enzyme preparations.',
      'empirically_supported',['empirical'],'Treated readings123and139 average131; untreated98and115 average106.5. These are observed condition summaries, with no independent-preparation uncertainty estimate.',
      ['Compute the two means from the rows at0.11ppm.','Restrict the claim to these recorded enzyme observations.'],puunc,
      {'operation':'puromycin_mean_011','expected':{'treated':'131','untreated':'213/2','difference':'49/2'}})
    paired('PU02','puromycin','evaluation',[puctx,pudoc],['Compare only the recorded high-substrate observations.'],
      'At1.1ppm,the two treated rates are207and200counts/min/min,while the single untreated rate is160counts/min/min.',
      'The higher treated reaction rates establish that Puromycin improves patients’ health or survival.',
      'empirically_supported',['empirical'],'The table records the stated instantaneous rates; the outcomes are enzyme reaction counts, not clinical benefit.',
      ['Locate the three1.1ppm observations.','Retain the measured outcome and avoid clinical interpretation.'],puunc,
      {'operation':'puromycin_high','expected':{'treated':['207','200'],'untreated':['160']}})
    paired('PU03','puromycin','evaluation',[puctx,pudoc],['Compare treated means at the two stated concentrations; do not fit a model or infer molecular mechanisms.'],
      'For treated observations,increasing substrate from0.02to1.1ppm increases the recorded mean rate by less than the55-fold increase in concentration.',
      'The recorded sublinear rate increase uniquely establishes Michaelis–Menten binding kinetics and identifies the molecular binding mechanism.',
      'empirically_supported',['empirical'],'The means are61.5and203.5, giving rate ratio407/123,which is below55. Many kinetic mechanisms, assay effects or noise processes can yield a sublinear finite response.',
      ['Compute61.5and203.5from the treated rows.','Compare rate ratio407/123with substrate ratio55without interpreting the finite ratio as a mechanism proof.'],puunc,
      {'operation':'puromycin_ratio','expected':{'low':'123/2','high':'407/2','rate_ratio':'407/123','concentration_ratio':'55'}})
    case('PU04P','puromycin','evaluation','The table contains12treated rows and11untreated rows.',[puctx,pudoc],[],
      'computationally_established',['computational'],'Direct counting yields12and11rows; this is not a count of biological preparations.',['Count state labels.','Distinguish rows from independent experiments.'],puunc,'exact','PU04','positive',{'operation':'puromycin_counts','expected':{'treated':12,'untreated':11}})
    case('PU04X','puromycin','evaluation','The23rows constitute23independent biological experiments,as documented by this study.',[puctx,pudoc],[],
      'refuted',[],'The supplied method explicitly describes one treated and one untreated experiment with varying substrate concentration. It contradicts the claim that the study documents23independent biological experiments.',['Cite the once-treated/once-untreated protocol.','Do not equate concentration readings with independent biological replication.'],puunc,'interpretation','PU04','negative')
    codoc=doc('CO-DATA','Recorded grass-plant CO2 uptake data',table(plants,['Plant','Type','Treatment','conc','uptake']),'grass_co2')
    coctx=doc('CO-METHOD','R documentation of cold-tolerance experiment',
      'R datasets CO2:84observations from12grass plants(Echinochloa crus-galli),six from Quebec and six from Mississippi. Each plant was measured at seven recorded ambient concentration levels95,175,250,350,500,675,1000. Half the plants of each origin were chilled overnight. Plant is the experimental-unit identifier; successive concentrations are repeated observations of that plant. Uptake is documented in micromol per square metre per second. The R manual labels ambient concentration mL/L; the numeric source scale is preserved in this table. Source Potvin,Lechowicz and Tardif(1990),curated R transcription,formerly nlme.', 'grass_co2')
    counc='Twelve plants and repeated concentration observations; no independent experimental repetition or randomization protocol is supplied. The R concentration-unit label is preserved but not silently interpreted as ppm. Source transcription and original calibration uncertainties are not independently verified.'
    paired('CO01','grass_co2','evaluation',[coctx,codoc],['Compare Qn1 recorded uptake values directly,retaining source concentration codes.'],
      'For plantQn1,the recorded uptake at concentration code500is35.3,lower than37.2at code350.',
      'The observed decrease in Qn1 establishes a reproducible inhibitory CO2 effect above concentration350for this species.',
      'empirically_supported',['empirical'],'The within-plant measured values support the narrow statement. A single nonmonotone segment does not distinguish noise,adaptation,order effects or reproducible inhibition.',
      ['Locate both Qn1 rows and compare their uptake rates.','Avoid treating two sequential readings as independent causal evidence of inhibition.'],counc,
      {'operation':'grass_qn1','expected':{'350':'186/5','500':'353/10','difference':'-19/10'}})
    paired('CO02','grass_co2','evaluation',[coctx,codoc],['Count Plant identifiers and concentration observations separately.'],
      'The table has12distinct Plant identifiers and84rows,with seven recorded concentrations per plant.',
      'A comparison using all84rows as84independent plants is justified by the supplied repeated-observation design.',
      'computationally_established',['computational'],'There are12plant identifiers with seven rows each. Repeated measurements do not supply84independent plants.',
      ['Count12plant identifiers and seven rows per plant.','Identify the repeated-measures unit.'],counc,
      {'operation':'grass_counts','expected':{'plants':12,'rows':84,'per_plant':7}},
      'The design has12plants measured repeatedly; it does not justify84independent experimental units. A dependence-aware analysis or explicit covariance model would be required.',
      ['Name the plant as the experimental unit.','Explain why per-row independence is not supplied.'])
    # A contradiction is separately scored from evidence insufficiency.
    case('CO03P','grass_co2','evaluation','For the three Mississippi nonchilled plants at concentration code1000,the mean recorded uptake exceeds the mean of the three Mississippi chilled plants.',[coctx,codoc],[],
      'empirically_supported',['empirical'],'At code1000the nonchilled values are35.5,31.5,27.8(mean31.6);chilled values are21.9,14.4,19.9(mean281/15). The finite observed comparison holds.',['Use only Mississippi plants at code1000.','State the3-versus3plant denominators and limit to observed conditions.'],counc,'empirical_source_fact','CO03','positive',{'operation':'grass_mississippi_1000','expected':{'nonchilled':'158/5','chilled':'281/15'}})
    case('CO03X','grass_co2','evaluation','For the three Mississippi plants in each condition at concentration code1000,the chilled mean recorded uptake is greater than the nonchilled mean.',[coctx,codoc],[],
      'refuted',[],'This reverses the empirical table comparison:the chilled mean281/15is below158/5. This refutes the proposed sample comparison,not every possible cold-treatment effect.',['Compute both means.','Identify the reversed inequality without extrapolating to every plant.'],counc,'exact','CO03','negative',{'operation':'grass_mississippi_1000','expected':{'nonchilled':'158/5','chilled':'281/15'}})
    paired('CO04','grass_co2','evaluation',[coctx,codoc],['Analyze only Quebec plants and recorded concentration code1000.'],
      'At concentration code1000,the observed mean uptake of the three Quebec nonchilled plants exceeds that of the three Quebec chilled plants.',
      'The Quebec experiment establishes the same cold-treatment effect for all grass species under future field climates.',
      'empirically_supported',['empirical'],'Quebec nonchilled uptake values39.7,44.3,45.5 have mean259/6;chilled values38.7,42.4,41.4 have mean245/6. The sample comparison holds without population or ecosystem extrapolation.',
      ['Use3plants in each Quebec treatment condition at the same code.','Preserve the restricted species,source scale and measured outcome.'],counc,
      {'operation':'grass_quebec_1000','expected':{'nonchilled':'259/6','chilled':'245/6'}})
    fdoc=doc('FS-DATA','FreeSolv selected thermodynamic records',table(chosen,['id','name','experimental_kcal_mol','experimental_uncertainty_kcal_mol','calculated_kcal_mol','calculated_uncertainty_kcal_mol','experimental_reference','calculated_reference','notes']),'freesolv')
    fctx=doc('FS-METHOD','FreeSolv field definitions and provenance',
      'FreeSolv database.txt header labels experimental hydration free energy,experimental uncertainty,GAFF calculated hydration free energy and calculated uncertainty,all in kcal/mol. Hydration is transfer to water. Experimental_reference identifies the paper from which a value was taken; calculated_reference for these rows is10.1021/acs.jced.7b00104. Fields label different evidence types. The database notes mark some uncertainty values as assigned defaults when experimental uncertainty is unavailable.', 'freesolv')
    func='Public curated experimental/calculated thermodynamic records,not original laboratory raw measurements. Individual primary experimental papers and full transfer standard-state corrections are not independently replayed. Default uncertainties are not measured error bars. No protein-binding or temperature-series validation is supplied.'
    paired('FS01','freesolv','evaluation',[fctx,fdoc],['Interpret experimental and calculated columns according to the source header; use only the named published-reference entries.'],
      'FreeSolv reports experimental hydration free energy-5.00kcal/mol for ethanol and+2.00kcal/mol for methane,so the reported ethanol value is more negative.',
      'These hydration values prove that ethanol binds more tightly than methane to an arbitrary protein target.',
      'empirically_supported',['empirical'],'The two curator-reported experimental hydration values support their narrow ordering. Transfer to water is not a protein-ligand binding free energy.',
      ['Identify the experimental rather than calculated columns.','Preserve hydration-to-water scope and kcal/mol units.'],func,
      {'operation':'freesolv_values','expected':{'ethanol':'-5','methane':'2','difference':'-7'}})
    paired('FS02','freesolv','evaluation',[fctx,fdoc],['Calculate the signed residual as GAFF calculated minus experimental value.'],
      'For the FreeSolv triethylphosphate record,the signed GAFF hydration residual is-2.75kcal/mol(calculated minus experimental).',
      'This single residual proves that GAFF is inaccurate by exactly2.75kcal/mol for every protein-binding calculation.',
      'computationally_established',['computational'],'The source fields give-10.25-(-7.50)=-2.75kcal/mol. A calculation error for one hydration record does not identify all protein-binding errors.',
      ['Subtract-7.50from-10.25with the stated sign convention.','Do not generalize a single hydration residual to all compounds or binding calculations.'],func,
      {'operation':'freesolv_residual','expected':{'compound':'triethylphosphate','calculated':'-41/4','experimental':'-15/2','residual':'-11/4'}})
    paired('FS03','freesolv','evaluation',[fctx,fdoc],['Read each uncertainty note,not only the numeric uncertainty field.'],
      'The FreeSolv methanol record marks its0.60kcal/mol experimental-uncertainty field as an assigned default because experimental uncertainty is not presently available.',
      'The methanol0.60kcal/mol field is a measured95%confidence interval from independent replicate hydration experiments.',
      'computationally_established',['provenance'],'The record note explicitly says the experimental uncertainty is unavailable and a default was assigned. The numeric field alone does not provide a confidence level or replication design.',
      ['Read the default-assignment note.','Distinguish an assigned uncertainty convention from measured replicate-based uncertainty.'],func,
      {'operation':'freesolv_default','expected':{'compound':'methanol','uncertainty':'3/5','default_note':True}})
    paired('FS04','freesolv','evaluation',[fctx,fdoc],['Describe agreement of the two displayed rounded values only.'],
      'For neopentane,the displayed FreeSolv experimental and calculated hydration values both equal2.51kcal/mol.',
      'Equality of the two displayed neopentane values proves exact physical prediction with zero model discrepancy at every temperature.',
      'empirically_supported',['empirical'],'The source reports both values as2.51with experimental uncertainty0.60(default)and calculated uncertainty0.02. Displayed agreement is not zero uncertainty or validation over temperature.',
      ['Identify equality of the rounded displayed values.','Retain nonzero uncertainty and distinguish display equality from exact physical identity.'],func,
      {'operation':'freesolv_equal','expected':{'compound':'neopentane','experimental':'251/100','calculated':'251/100','experimental_uncertainty':'3/5','calculated_uncertainty':'1/50'}})
    # Negative evidence can refute a proposed evidential interpretation; this is
    # different from an unknown physical claim beyond the source scope.
    for c in CASES:
        if c['id'] in {'CO02S','FS03S'}:
            c['reference']['label']='refuted'
            c['reference']['kind']='interpretation'
            c['reference']['condition_labels']={k:('insufficient_evidence' if k=='no_evidence' else 'refuted') for k in ('evidence','no_evidence','no_assumptions','verified_numbers','paraphrase')}
            c['reference']['rationale']=('The supplied design explicitly has12plants measured7times,so treating84rows as84independent plants contradicts the documented experimental units.' if c['id']=='CO02S' else 'The source explicitly calls0.60an assigned default because experimental uncertainty is unavailable;this contradicts describing that field as a measured95%confidence interval.')
    def readable(text):
        # Normalize authored prose,never identifiers,DOIs or source table bytes.
        text=text.replace('plantQn1','plant Qn1').replace('Qn1,the','Qn1, the')
        protected={}
        def keep(m):
            token='PROTECTED'+chr(65+len(protected))+'TOKEN'
            protected[token]=m[0]
            return token
        text=re.sub(r'10\.\d{4,9}/[^ ,;()]+|\b(?:CO2|Qn[123]|Qc[123]|Mn[123]|Mc[123])\b',keep,text)
        text=re.sub(r'(?<=[a-zA-Z])(?=\d)|(?<=\d)(?=[a-zA-Z])',' ',text)
        text=re.sub(r'(?<=\d)(?=(?:ppm|kcal|counts|fold|rows|plants|records|correct|times|treated|untreated|independent|distinct|confidence|and|is|at|for|to|from|with)\b)', ' ',text)
        text=re.sub(r'\b(for|of|are|has|by|with|at|from|to|during|below|than|mean|values|records|contains|only|above)(?=\d)',r'\1 ',text)
        text=re.sub(r'(?<=,)(?=[A-Za-z0-9])', ' ',text)
        text=re.sub(r'(?<=[a-z%])(?=\()',' ',text)
        text=re.sub(r'(?<=\))(?=[A-Za-z])',' ',text)
        for token,original in protected.items():text=text.replace(token,original)
        return text
    for c in CASES:
        for k in ('question','claim','methodology'):c['packet'][k]=readable(c['packet'][k])
        c['packet']['assumptions']=[readable(t) for t in c['packet']['assumptions']]
        for d in c['packet']['documents']:
            if ',\n' not in d['text'] and '\n' not in d['text']:d['text']=readable(d['text'])
        c['reference']['rationale']=readable(c['reference']['rationale'])
        if c['reference']['label']=='empirically_supported' and c['reference'].get('numeric_check'):
            c['reference']['scopes']=sorted(set(c['reference']['scopes'])|{'computational'})
            for condition in c['reference']['condition_scopes']:
                if condition!='no_evidence':c['reference']['condition_scopes'][condition]=list(c['reference']['scopes'])
        pair=c['pair']['id']
        if pair=='PU01':
            c['verification_note']='Exact arithmetic on the recorded rows at 0.11 ppm: (123 + 139) / 2 = 131; (98 + 115) / 2 = 106.5; 131 - 106.5 = 24.5 counts/min/min.'
        elif pair=='PU02':
            c['verification_note']='Direct extraction at 1.1 ppm gives treated rates [207, 200] and untreated rates [160], in counts/min/min.'
    # Render dossiers from final corrected labels and rationales.
    for i,entry in enumerate(DOSSIERS):
        c=CASES[i]
        DOSSIERS[i]=(c['id'],c['reference']['label'],c['reference']['rationale'],c['reference']['reasoning_requirements'],c['reference']['uncertainty'],c['reference'].get('numeric_check'))
    write_json(DEST/'cases.json',CASES)
    write_registry()
    write_dossiers()

def write_registry():
    specs={
      'penguins':{'title':'Palmer LTER penguin field measurements,raw palmerpenguins distribution','source_type':'observational_field_measurements','license':'CC0-1.0','license_evidence':['penguins_LICENSE.md','penguins_README.md'],'url':'https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins_raw.csv','primary_doi':'10.1371/journal.pone.0090081','files':['penguins_raw.csv','penguins_LICENSE.md','penguins_README.md','penguins_revision.json'],'split':'dev','limitations':'Species-specific EDI data citations are in README.344records are not documented344unique animals across studies. License recommends investigator contact for publication; no publication undertaken.'},
      'penguins_article':{'title':'Gorman,Williams and Fraser2014 PLOS ONE primary article','source_type':'primary_article','license':'CC-BY-4.0','license_evidence':['penguins_article.html'],'url':'https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081','primary_doi':'10.1371/journal.pone.0090081','files':['penguins_article.html','penguins_primary.pdf'],'split':'dev','limitations':'Source-reported results; independent reconstruction of original classification not performed.'},
      'puromycin':{'title':'R datasets Puromycin:enzyme reaction velocity curated historical observations','source_type':'curated_experimental_transcription','license':'GPL-2.0-or-later','license_evidence':['Puromycin.Rd','R_COPYING','r_datasets_DESCRIPTION.in'],'url':'https://raw.githubusercontent.com/wch/r-source/trunk/src/library/datasets/data/Puromycin.R','original_source':'Treloar1974 experimental thesis via Bates and Watts1988,AppendixA1.3,p269','files':['Puromycin.R','Puromycin.Rd','Puromycin_extracted.csv','R_COPYING','r_datasets_DESCRIPTION.in','R_revision.json'],'split':'evaluation','limitations':'Original thesis and full methods not obtained. Data source file preserves GPL distribution and source attribution; source code/license texts remain GPL rather than SVB Apache.23readings are not23independent biological experiments.'},
      'grass_co2':{'title':'R datasets CO2:grass cold-tolerance experiment','source_type':'curated_experimental_transcription','license':'GPL-2.0-or-later','license_evidence':['CO2.Rd','R_COPYING','r_datasets_DESCRIPTION.in'],'url':'https://raw.githubusercontent.com/wch/r-source/trunk/src/library/datasets/data/CO2.rda','original_source':'Potvin,Lechowicz and Tardif1990,The statistical analysis of ecophysiological response curves obtained from experiments involving repeated measures,Ecology71:1389–1400','files':['CO2.rda','CO2.Rd','CO2_plants_extracted.csv','R_COPYING','r_datasets_DESCRIPTION.in','R_revision.json'],'split':'evaluation','limitations':'Original primary paper not obtained;12plants repeatedly measured7times. Preserve source numeric concentration scale; unit transcription not independently resolved. Extraction parses bounded vector records without executing R.'},
      'freesolv':{'title':'FreeSolv v0.52 experimental and calculated hydration free energy records','source_type':'curated_thermodynamic_database','license':'CC-BY-4.0','license_evidence':['freesolv_LICENSE','freesolv_README.md'],'url':'https://raw.githubusercontent.com/MobleyLab/FreeSolv/master/database.txt','dataset_doi':'10.5281/zenodo.1161245','paper_doi':'10.1021/acs.jced.7b00104','files':['freesolv_database.txt','freesolv_selected.csv','freesolv_LICENSE','freesolv_README.md','freesolv_revision.json'],'split':'evaluation','limitations':'Upstream README explicitly states CC-BY4only to extent authors can license data; original restrictions may apply. Selected entries cite published sources only; no unpublished-reference entry used. Original laboratory methods and standard-state corrections not independently verified. Assigned default uncertainties retain notes.'},
    }
    for source in specs.values():
        source['accessed']=DATE
        source['artifacts']=[{'path':'data/v0.2.0/sources/'+f,'sha256':sha(SRC/f),'bytes':(SRC/f).stat().st_size} for f in source.pop('files')]
    write_json(DEST/'registry.json',{'version':'0.2.0','sources':specs,'adjudication':'provisional_author_adjudicated','source_split_policy':'All packets derived from one source family stay together;penguin primary article and field data both dev;all3other scientific source families evaluation. No hidden set or external human validation claimed.'})

def write_dossiers():
    text='''# Phase II reference dossiers (SVB0.2.0)\n\nThese32cases form16paired scientific judgments from four source families. All references are provisional author adjudications,not external expert approvals. Numeric witnesses are independently recomputed from archived public source bytes by `src/svb/phase2_references.py`; those computations do not mechanically establish empirical adequacy or the hand-reviewed scope labels. Evidence packets contain source data and method excerpts,not labels or reference metadata. No evaluated-system output contributed to references.\n\n## Source admission and boundaries\n\n- Palmer LTER:raw field measurements,CC0 license snapshot;Gorman,Williams and Fraser2014 primary PLOS article,CC-BY4 explicitly stated in archived article. The paper documents egg-laying-period specificity and held-out sex-classification results. Source rows retain NA and study identifiers. Observed results do not establish all-season effects or causal relocation outcomes.\n- Puromycin:official R source + GPL2-or-later manual and COPYING retained. Original Treloar1974 experiment was transcribed via Bates and Watts1988. We did not acquire the original thesis; the observational values and stated historical experimental procedure are curated source evidence,not a fresh assay replication. Substrate units are ppm;instantaneous rates counts/min/min.\n- Grass CO2:official R binary84rows,12plants×7concentrations,plus R manual and GPL2-or-later text. Bounded binary extraction validates record type,length,all factor strings and exposure grid. The original Potvin etal1990 primary article is cited by the manual but not obtained. Manual labels concentration mL/L;we preserve source numeric codes rather than silently treating them as ppm. Uptake is micromol/m²/s. Repeated measurements are not independent plants.\n- FreeSolv:public curated experimental/calculated hydration records,upstream CC-BY4 LICENSE and explicit upstream original-license caveat retained. Selected six compounds have published experimental references;records citing unpublished data are not used. Hydration is not protein binding;default uncertainties are not measured confidence intervals. Full primary measurement papers,temperature and standard-state corrections were not independently reconstructed. No absolute accuracy/biological claim depends on absent detail.\n\n`data/v0.2.0/registry.json` records URLs,hashes,date,source type,attribution,licenses and limitations. Source split separation is stringent but yields only one dev source family:penguins. All other families are evaluation. This separation does not supply a hidden test set or population representativeness.\n\n## Rejected acquisition candidates\n\nNIST web endpoints returned403. Official GitHub ThermoML sample files identify themselves as examples/trials;one has duplicate chemical identifiers. They were rejected as experimental ground truth. Rdatasets uppercase CO2 requests returned lowercase atmospheric co2 time-series columns rather than plant uptake;those files were rejected and archived outside the benchmark data. Mercury pressure is a secondary CRC table and was superseded by the more relevant FreeSolv dataset. Acquisition diagnostics are local artifacts,not benchmark evidence.\n\n## Variant reference policy\n\nEvidence,verified_numbers,and paraphrase retain the same claim and sufficient source evidence,so their labels/scopes are invariant. No_assumptions removes only a separate reminder;all essential source conditions,design descriptions,units and comparison definitions remain in documents or claim,so labels/scopes remain unchanged. No_evidence removes every document:question/claim/procedure alone supplies none of these observations or provenance. All no_evidence references are insufficient_evidence with empty scopes,including originally refuted claims. This is an evidence-sufficiency test,not a factual-memory test. A truthful unsupported claim is not presumed false. Numeric checks are withheld from every model condition.\n\n## Item dossiers\n\n'''
    for ident,label,rationale,requirements,uncertainty,numeric in DOSSIERS:
        c=next(c for c in CASES if c['id']==ident)
        text+=f'### {ident}: {label}\n\nClaim: {c["packet"]["claim"]}\n\nEvidence: '+', '.join(c['reference']['evidence_ids'])+'; source family '+c['family']+'.\n\nAdjudication: '+rationale+'\n\nCorrectness criteria:\n\n'+''.join('- '+r+'\n' for r in requirements)+'\nAmbiguity/limitations: '+uncertainty+'\n\n'
        if numeric:text+='Recomputed numeric witness: `'+json.dumps(numeric,sort_keys=True)+'`.\n\n'
    text+='## What independent reviewers should challenge\n\nThe narrow empirical labels concern source-reported observations,not confirmation that laboratories and data transcriptions were error-free. R datasets are curated secondary transcriptions with incomplete original methods. FreeSolv inherits upstream licensing caveats and heterogeneous uncertainty conventions. All sixteen stronger/negative claims are authored examples and may have stylistic cues;no general scientific reasoning result can be inferred from their synthetic wording. Four source families are too few for a stable source-population estimate. Source groups,not rows or paired variants,are appropriate robustness units. Labels need domain expert review before release as a definitive benchmark.\n'
    text += '\n## Prefreeze corrections retained for review\n\nThe first materialized,unfrozen draft contained two manually transcribed grass summary errors. The CO03 Mississippi chilled high-concentration row is21.9(not21.4),giving mean281/15;CO04 Quebec chilled third row is41.4(not39.6),giving mean245/6. Raw source records were never altered. Exact replay identified and corrected both before scored runs;the negative test deliberately injects the old CO03mean557/30and verifies rejection. Two interpretation labels were also refined before freeze:the claim of84independent plants contradicts a12plant repeated-measure design,and a measured95%confidence-interval description contradicts a source note marking an uncertainty as default;both are refuted rather than merely insufficient.\n\nAll13reference tests passed at candidate handoff,including source corruption,numeric-reference corruption,source-split integrity,and withholding-evidence reference behavior. The17numeric witness checks verify arithmetic and source-record alignment only. There is no mechanical proof of the empirical/interpretive labels,and no outside expert or human adjudicator has yet approved them.\n'
    (ROOT/'docs/phase-ii/reference_dossiers.md').write_text(text)

if __name__=='__main__':build()
