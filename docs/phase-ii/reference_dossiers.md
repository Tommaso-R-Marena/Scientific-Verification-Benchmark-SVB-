# Phase II reference dossiers (SVB0.2.0)

These32cases form16paired scientific judgments from four source families. All references are provisional author adjudications,not external expert approvals. Numeric witnesses are independently recomputed from archived public source bytes by `src/svb/phase2_references.py`; those computations do not mechanically establish empirical adequacy or the hand-reviewed scope labels. Evidence packets contain source data and method excerpts,not labels or reference metadata. No evaluated-system output contributed to references.

## Source admission and boundaries

- Palmer LTER:raw field measurements,CC0 license snapshot;Gorman,Williams and Fraser2014 primary PLOS article,CC-BY4 explicitly stated in archived article. The paper documents egg-laying-period specificity and held-out sex-classification results. Source rows retain NA and study identifiers. Observed results do not establish all-season effects or causal relocation outcomes.
- Puromycin:official R source + GPL2-or-later manual and COPYING retained. Original Treloar1974 experiment was transcribed via Bates and Watts1988. We did not acquire the original thesis; the observational values and stated historical experimental procedure are curated source evidence,not a fresh assay replication. Substrate units are ppm;instantaneous rates counts/min/min.
- Grass CO2:official R binary84rows,12plants×7concentrations,plus R manual and GPL2-or-later text. Bounded binary extraction validates record type,length,all factor strings and exposure grid. The original Potvin etal1990 primary article is cited by the manual but not obtained. Manual labels concentration mL/L;we preserve source numeric codes rather than silently treating them as ppm. Uptake is micromol/m²/s. Repeated measurements are not independent plants.
- FreeSolv:public curated experimental/calculated hydration records,upstream CC-BY4 LICENSE and explicit upstream original-license caveat retained. Selected six compounds have published experimental references;records citing unpublished data are not used. Hydration is not protein binding;default uncertainties are not measured confidence intervals. Full primary measurement papers,temperature and standard-state corrections were not independently reconstructed. No absolute accuracy/biological claim depends on absent detail.

`data/v0.2.0/registry.json` records URLs,hashes,date,source type,attribution,licenses and limitations. Source split separation is stringent but yields only one dev source family:penguins. All other families are evaluation. This separation does not supply a hidden test set or population representativeness.

## Rejected acquisition candidates

NIST web endpoints returned403. Official GitHub ThermoML sample files identify themselves as examples/trials;one has duplicate chemical identifiers. They were rejected as experimental ground truth. Rdatasets uppercase CO2 requests returned lowercase atmospheric co2 time-series columns rather than plant uptake;those files were rejected and archived outside the benchmark data. Mercury pressure is a secondary CRC table and was superseded by the more relevant FreeSolv dataset. Acquisition diagnostics are local artifacts,not benchmark evidence.

## Variant reference policy

Evidence,verified_numbers,and paraphrase retain the same claim and sufficient source evidence,so their labels/scopes are invariant. No_assumptions removes only a separate reminder;all essential source conditions,design descriptions,units and comparison definitions remain in documents or claim,so labels/scopes remain unchanged. No_evidence removes every document:question/claim/procedure alone supplies none of these observations or provenance. All no_evidence references are insufficient_evidence with empty scopes,including originally refuted claims. This is an evidence-sufficiency test,not a factual-memory test. A truthful unsupported claim is not presumed false. Numeric checks are withheld from every model condition.

## Item dossiers

### PG01N: empirically_supported

Claim: For the nonmissing recorded observations, Gentoo penguins have a higher mean body mass than Adélie penguins.

Evidence: PG-METHOD, PG-MASS; source family penguins.

Adjudication: The measured sample means are 624350/123 g for Gentoo and 558800/151 g for Adélie, so the stated descriptive comparison is supported.

Correctness criteria:

- Exclude the two NA body masses.
- Compute the species-specific sample means and limit the comparison to these observations.

Ambiguity/limitations: Field observations at the recorded breeding stage and sites; missingness, selection, year dependence and measurement errors are not resolved by an exact sample summary. Source record correctness is assumed; independent expert adjudication has not occurred.

Recomputed numeric witness: `{"expected": {"Adelie_n": 151, "Adelie_sum_g": "558800", "Gentoo_n": 123, "Gentoo_sum_g": "624350", "gentoo_gt_adelie": true}, "operation": "penguin_species_mass"}`.

### PG01S: insufficient_evidence

Claim: The observed species difference proves that moving an Adélie penguin to Biscoe Island would cause its mass to become that of a Gentoo penguin.

Evidence: PG-METHOD, PG-MASS; source family penguins.

Adjudication: Species and islands were not randomized, and a cross-species association cannot identify an intervention on one individual. Genetic, sex, age, diet and other factors remain compatible explanations.

Correctness criteria:

- Identify the observational design and species-versus-intervention mismatch.
- Do not call the descriptive species difference a measured causal effect of relocation.

Ambiguity/limitations: Field observations at the recorded breeding stage and sites; missingness, selection, year dependence and measurement errors are not resolved by an exact sample summary. Source record correctness is assumed; independent expert adjudication has not occurred.

### PG02N: empirically_supported

Claim: In these sex-identified Adélie observations, the male mean body mass exceeds the female mean body mass.

Evidence: PG-METHOD, PG-SEX; source family penguins.

Adjudication: There are 73 male masses summing 295175 g and 73 female masses summing 245925 g; the observed means differ by 49250/73 g.

Correctness criteria:

- Compare sex-specific averages with their denominators.
- Distinguish the observed conditional sample comparison from all-season extrapolation.

Ambiguity/limitations: Field observations at the recorded breeding stage and sites; missingness, selection, year dependence and measurement errors are not resolved by an exact sample summary. Source record correctness is assumed; independent expert adjudication has not occurred.

Recomputed numeric witness: `{"expected": {"FEMALE_n": 73, "FEMALE_sum_g": "245925", "MALE_n": 73, "MALE_sum_g": "295175"}, "operation": "penguin_sex_mass"}`.

### PG02S: insufficient_evidence

Claim: These egg-laying-period observations establish the same male–female mass difference during every season throughout Antarctica.

Evidence: PG-METHOD, PG-SEX; source family penguins.

Adjudication: The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Field observations at the recorded breeding stage and sites; missingness, selection, year dependence and measurement errors are not resolved by an exact sample summary. Source record correctness is assumed; independent expert adjudication has not occurred.

### PG03N: computationally_established

Claim: The supplied table has 344 records, 190 distinct Individual ID strings, and 344 distinct (studyName, Individual ID) pairs.

Evidence: PG-METHOD, PG-ID; source family penguins.

Adjudication: Counting rows and exact strings establishes the stated table properties. The source packet does not establish a cross-study animal-linkage key.

Correctness criteria:

- Count records, unique ID strings and composite keys.
- Do not confuse a repeated string with documented longitudinal identity.

Ambiguity/limitations: Field observations at the recorded breeding stage and sites; missingness, selection, year dependence and measurement errors are not resolved by an exact sample summary. Source record correctness is assumed; independent expert adjudication has not occurred.

Recomputed numeric witness: `{"expected": {"rows": 344, "unique_id": 190, "unique_study_id": 344}, "operation": "penguin_ids"}`.

### PG03S: insufficient_evidence

Claim: Repeated Individual ID strings across studies establish that these are repeated measurements of the same animals and allow individual growth rates to be inferred.

Evidence: PG-METHOD, PG-ID; source family penguins.

Adjudication: The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Field observations at the recorded breeding stage and sites; missingness, selection, year dependence and measurement errors are not resolved by an exact sample summary. Source record correctness is assumed; independent expert adjudication has not occurred.

### PG04N: empirically_supported

Claim: The primary article reports 39 correct classifications out of 44 held-out Adélie individuals, approximately 88.64%, under its stated sex-classification procedure.

Evidence: PG-METHOD, PG-HOLDOUT; source family penguins.

Adjudication: The primary article directly reports the held-out result and 39/44 rounds to 88.64%. This supports the precise reporting claim, not an independently replicated predictor.

Correctness criteria:

- Identify39/44 and the within-study held-out procedure.
- Preserve the task(population sex classification)and reported-result qualification.

Ambiguity/limitations: Field observations at the recorded breeding stage and sites; missingness, selection, year dependence and measurement errors are not resolved by an exact sample summary. Source record correctness is assumed; independent expert adjudication has not occurred.

Recomputed numeric witness: `{"expected": {"correct": 39, "percent_2dp": "88.64", "total": 44}, "operation": "holdout_fraction"}`.

### PG04S: insufficient_evidence

Claim: The reported held-out accuracy establishes 88.64%classification accuracy for any future penguin population, species and seasonal stage.

Evidence: PG-METHOD, PG-HOLDOUT; source family penguins.

Adjudication: The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Field observations at the recorded breeding stage and sites; missingness, selection, year dependence and measurement errors are not resolved by an exact sample summary. Source record correctness is assumed; independent expert adjudication has not occurred.

### PU01N: empirically_supported

Claim: At recorded concentration 0.11 ppm, the treated mean reaction rate is 131 counts/min/min and the untreated mean is 106.5 counts/min/min.

Evidence: PU-METHOD, PU-DATA; source family puromycin.

Adjudication: Treated readings 123 and 139 average 131; untreated 98 and 115 average 106.5. These are observed condition summaries, with no independent-preparation uncertainty estimate.

Correctness criteria:

- Compute the two means from the rows at0.11ppm.
- Restrict the claim to these recorded enzyme observations.

Ambiguity/limitations: Curated transcription of a historical enzyme experiment; the original thesis and full laboratory protocol were not obtained. The two readings at many concentrations do not establish independent biological replication. No patient data, molecular binding assay or original measurement uncertainty is supplied.

Recomputed numeric witness: `{"expected": {"difference": "49/2", "treated": "131", "untreated": "213/2"}, "operation": "puromycin_mean_011"}`.

### PU01S: insufficient_evidence

Claim: The difference at 0.11 ppm establishes a precisely estimated population-average treatment effect across independent enzyme preparations.

Evidence: PU-METHOD, PU-DATA; source family puromycin.

Adjudication: The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Curated transcription of a historical enzyme experiment; the original thesis and full laboratory protocol were not obtained. The two readings at many concentrations do not establish independent biological replication. No patient data, molecular binding assay or original measurement uncertainty is supplied.

### PU02N: empirically_supported

Claim: At 1.1 ppm, the two treated rates are 207 and 200 counts/min/min, while the single untreated rate is 160 counts/min/min.

Evidence: PU-METHOD, PU-DATA; source family puromycin.

Adjudication: The table records the stated instantaneous rates; the outcomes are enzyme reaction counts, not clinical benefit.

Correctness criteria:

- Locate the three1.1ppm observations.
- Retain the measured outcome and avoid clinical interpretation.

Ambiguity/limitations: Curated transcription of a historical enzyme experiment; the original thesis and full laboratory protocol were not obtained. The two readings at many concentrations do not establish independent biological replication. No patient data, molecular binding assay or original measurement uncertainty is supplied.

Recomputed numeric witness: `{"expected": {"treated": ["207", "200"], "untreated": ["160"]}, "operation": "puromycin_high"}`.

### PU02S: insufficient_evidence

Claim: The higher treated reaction rates establish that Puromycin improves patients’ health or survival.

Evidence: PU-METHOD, PU-DATA; source family puromycin.

Adjudication: The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Curated transcription of a historical enzyme experiment; the original thesis and full laboratory protocol were not obtained. The two readings at many concentrations do not establish independent biological replication. No patient data, molecular binding assay or original measurement uncertainty is supplied.

### PU03N: empirically_supported

Claim: For treated observations, increasing substrate from 0.02 to 1.1 ppm increases the recorded mean rate by less than the 55-fold increase in concentration.

Evidence: PU-METHOD, PU-DATA; source family puromycin.

Adjudication: The means are 61.5 and 203.5, giving rate ratio 407/123, which is below 55. Many kinetic mechanisms, assay effects or noise processes can yield a sublinear finite response.

Correctness criteria:

- Compute61.5and203.5from the treated rows.
- Compare rate ratio407/123with substrate ratio55without interpreting the finite ratio as a mechanism proof.

Ambiguity/limitations: Curated transcription of a historical enzyme experiment; the original thesis and full laboratory protocol were not obtained. The two readings at many concentrations do not establish independent biological replication. No patient data, molecular binding assay or original measurement uncertainty is supplied.

Recomputed numeric witness: `{"expected": {"concentration_ratio": "55", "high": "407/2", "low": "123/2", "rate_ratio": "407/123"}, "operation": "puromycin_ratio"}`.

### PU03S: insufficient_evidence

Claim: The recorded sublinear rate increase uniquely establishes Michaelis–Menten binding kinetics and identifies the molecular binding mechanism.

Evidence: PU-METHOD, PU-DATA; source family puromycin.

Adjudication: The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Curated transcription of a historical enzyme experiment; the original thesis and full laboratory protocol were not obtained. The two readings at many concentrations do not establish independent biological replication. No patient data, molecular binding assay or original measurement uncertainty is supplied.

### PU04P: computationally_established

Claim: The table contains 12 treated rows and 11 untreated rows.

Evidence: PU-METHOD, PU-DATA; source family puromycin.

Adjudication: Direct counting yields 12 and 11 rows; this is not a count of biological preparations.

Correctness criteria:

- Count state labels.
- Distinguish rows from independent experiments.

Ambiguity/limitations: Curated transcription of a historical enzyme experiment; the original thesis and full laboratory protocol were not obtained. The two readings at many concentrations do not establish independent biological replication. No patient data, molecular binding assay or original measurement uncertainty is supplied.

Recomputed numeric witness: `{"expected": {"treated": 12, "untreated": 11}, "operation": "puromycin_counts"}`.

### PU04X: refuted

Claim: The 23 rows constitute 23 independent biological experiments, as documented by this study.

Evidence: PU-METHOD, PU-DATA; source family puromycin.

Adjudication: The supplied method explicitly describes one treated and one untreated experiment with varying substrate concentration. It contradicts the claim that the study documents 23 independent biological experiments.

Correctness criteria:

- Cite the once-treated/once-untreated protocol.
- Do not equate concentration readings with independent biological replication.

Ambiguity/limitations: Curated transcription of a historical enzyme experiment; the original thesis and full laboratory protocol were not obtained. The two readings at many concentrations do not establish independent biological replication. No patient data, molecular binding assay or original measurement uncertainty is supplied.

### CO01N: empirically_supported

Claim: For plant Qn1, the recorded uptake at concentration code 500 is 35.3, lower than 37.2 at code 350.

Evidence: CO-METHOD, CO-DATA; source family grass_co2.

Adjudication: The within-plant measured values support the narrow statement. A single nonmonotone segment does not distinguish noise, adaptation, order effects or reproducible inhibition.

Correctness criteria:

- Locate both Qn1 rows and compare their uptake rates.
- Avoid treating two sequential readings as independent causal evidence of inhibition.

Ambiguity/limitations: Twelve plants and repeated concentration observations; no independent experimental repetition or randomization protocol is supplied. The R concentration-unit label is preserved but not silently interpreted as ppm. Source transcription and original calibration uncertainties are not independently verified.

Recomputed numeric witness: `{"expected": {"350": "186/5", "500": "353/10", "difference": "-19/10"}, "operation": "grass_qn1"}`.

### CO01S: insufficient_evidence

Claim: The observed decrease in Qn1 establishes a reproducible inhibitory CO2 effect above concentration 350 for this species.

Evidence: CO-METHOD, CO-DATA; source family grass_co2.

Adjudication: The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Twelve plants and repeated concentration observations; no independent experimental repetition or randomization protocol is supplied. The R concentration-unit label is preserved but not silently interpreted as ppm. Source transcription and original calibration uncertainties are not independently verified.

### CO02N: computationally_established

Claim: The table has 12 distinct Plant identifiers and 84 rows, with seven recorded concentrations per plant.

Evidence: CO-METHOD, CO-DATA; source family grass_co2.

Adjudication: There are 12 plant identifiers with seven rows each. Repeated measurements do not supply 84 independent plants.

Correctness criteria:

- Count12plant identifiers and seven rows per plant.
- Identify the repeated-measures unit.

Ambiguity/limitations: Twelve plants and repeated concentration observations; no independent experimental repetition or randomization protocol is supplied. The R concentration-unit label is preserved but not silently interpreted as ppm. Source transcription and original calibration uncertainties are not independently verified.

Recomputed numeric witness: `{"expected": {"per_plant": 7, "plants": 12, "rows": 84}, "operation": "grass_counts"}`.

### CO02S: refuted

Claim: A comparison using all 84 rows as 84 independent plants is justified by the supplied repeated-observation design.

Evidence: CO-METHOD, CO-DATA; source family grass_co2.

Adjudication: The supplied design explicitly has 12 plants measured 7 times, so treating 84 rows as 84 independent plants contradicts the documented experimental units.

Correctness criteria:

- Name the plant as the experimental unit.
- Explain why per-row independence is not supplied.

Ambiguity/limitations: Twelve plants and repeated concentration observations; no independent experimental repetition or randomization protocol is supplied. The R concentration-unit label is preserved but not silently interpreted as ppm. Source transcription and original calibration uncertainties are not independently verified.

### CO03P: empirically_supported

Claim: For the three Mississippi nonchilled plants at concentration code 1000, the mean recorded uptake exceeds the mean of the three Mississippi chilled plants.

Evidence: CO-METHOD, CO-DATA; source family grass_co2.

Adjudication: At code 1000 the nonchilled values are 35.5, 31.5, 27.8(mean 31.6);chilled values are 21.9, 14.4, 19.9(mean 281/15). The finite observed comparison holds.

Correctness criteria:

- Use only Mississippi plants at code1000.
- State the3-versus3plant denominators and limit to observed conditions.

Ambiguity/limitations: Twelve plants and repeated concentration observations; no independent experimental repetition or randomization protocol is supplied. The R concentration-unit label is preserved but not silently interpreted as ppm. Source transcription and original calibration uncertainties are not independently verified.

Recomputed numeric witness: `{"expected": {"chilled": "281/15", "nonchilled": "158/5"}, "operation": "grass_mississippi_1000"}`.

### CO03X: refuted

Claim: For the three Mississippi plants in each condition at concentration code 1000, the chilled mean recorded uptake is greater than the nonchilled mean.

Evidence: CO-METHOD, CO-DATA; source family grass_co2.

Adjudication: This reverses the empirical table comparison:the chilled mean 281/15 is below 158/5. This refutes the proposed sample comparison, not every possible cold-treatment effect.

Correctness criteria:

- Compute both means.
- Identify the reversed inequality without extrapolating to every plant.

Ambiguity/limitations: Twelve plants and repeated concentration observations; no independent experimental repetition or randomization protocol is supplied. The R concentration-unit label is preserved but not silently interpreted as ppm. Source transcription and original calibration uncertainties are not independently verified.

Recomputed numeric witness: `{"expected": {"chilled": "281/15", "nonchilled": "158/5"}, "operation": "grass_mississippi_1000"}`.

### CO04N: empirically_supported

Claim: At concentration code 1000, the observed mean uptake of the three Quebec nonchilled plants exceeds that of the three Quebec chilled plants.

Evidence: CO-METHOD, CO-DATA; source family grass_co2.

Adjudication: Quebec nonchilled uptake values 39.7, 44.3, 45.5 have mean 259/6;chilled values 38.7, 42.4, 41.4 have mean 245/6. The sample comparison holds without population or ecosystem extrapolation.

Correctness criteria:

- Use3plants in each Quebec treatment condition at the same code.
- Preserve the restricted species,source scale and measured outcome.

Ambiguity/limitations: Twelve plants and repeated concentration observations; no independent experimental repetition or randomization protocol is supplied. The R concentration-unit label is preserved but not silently interpreted as ppm. Source transcription and original calibration uncertainties are not independently verified.

Recomputed numeric witness: `{"expected": {"chilled": "245/6", "nonchilled": "259/6"}, "operation": "grass_quebec_1000"}`.

### CO04S: insufficient_evidence

Claim: The Quebec experiment establishes the same cold-treatment effect for all grass species under future field climates.

Evidence: CO-METHOD, CO-DATA; source family grass_co2.

Adjudication: The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Twelve plants and repeated concentration observations; no independent experimental repetition or randomization protocol is supplied. The R concentration-unit label is preserved but not silently interpreted as ppm. Source transcription and original calibration uncertainties are not independently verified.

### FS01N: empirically_supported

Claim: FreeSolv reports experimental hydration free energy-5.00 kcal/mol for ethanol and+2.00 kcal/mol for methane, so the reported ethanol value is more negative.

Evidence: FS-METHOD, FS-DATA; source family freesolv.

Adjudication: The two curator-reported experimental hydration values support their narrow ordering. Transfer to water is not a protein-ligand binding free energy.

Correctness criteria:

- Identify the experimental rather than calculated columns.
- Preserve hydration-to-water scope and kcal/mol units.

Ambiguity/limitations: Public curated experimental/calculated thermodynamic records,not original laboratory raw measurements. Individual primary experimental papers and full transfer standard-state corrections are not independently replayed. Default uncertainties are not measured error bars. No protein-binding or temperature-series validation is supplied.

Recomputed numeric witness: `{"expected": {"difference": "-7", "ethanol": "-5", "methane": "2"}, "operation": "freesolv_values"}`.

### FS01S: insufficient_evidence

Claim: These hydration values prove that ethanol binds more tightly than methane to an arbitrary protein target.

Evidence: FS-METHOD, FS-DATA; source family freesolv.

Adjudication: The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Public curated experimental/calculated thermodynamic records,not original laboratory raw measurements. Individual primary experimental papers and full transfer standard-state corrections are not independently replayed. Default uncertainties are not measured error bars. No protein-binding or temperature-series validation is supplied.

### FS02N: computationally_established

Claim: For the FreeSolv triethylphosphate record, the signed GAFF hydration residual is-2.75 kcal/mol (calculated minus experimental).

Evidence: FS-METHOD, FS-DATA; source family freesolv.

Adjudication: The source fields give-10.25-(-7.50)=-2.75 kcal/mol. A calculation error for one hydration record does not identify all protein-binding errors.

Correctness criteria:

- Subtract-7.50from-10.25with the stated sign convention.
- Do not generalize a single hydration residual to all compounds or binding calculations.

Ambiguity/limitations: Public curated experimental/calculated thermodynamic records,not original laboratory raw measurements. Individual primary experimental papers and full transfer standard-state corrections are not independently replayed. Default uncertainties are not measured error bars. No protein-binding or temperature-series validation is supplied.

Recomputed numeric witness: `{"expected": {"calculated": "-41/4", "compound": "triethylphosphate", "experimental": "-15/2", "residual": "-11/4"}, "operation": "freesolv_residual"}`.

### FS02S: insufficient_evidence

Claim: This single residual proves that GAFF is inaccurate by exactly 2.75 kcal/mol for every protein-binding calculation.

Evidence: FS-METHOD, FS-DATA; source family freesolv.

Adjudication: The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Public curated experimental/calculated thermodynamic records,not original laboratory raw measurements. Individual primary experimental papers and full transfer standard-state corrections are not independently replayed. Default uncertainties are not measured error bars. No protein-binding or temperature-series validation is supplied.

### FS03N: computationally_established

Claim: The FreeSolv methanol record marks its 0.60 kcal/mol experimental-uncertainty field as an assigned default because experimental uncertainty is not presently available.

Evidence: FS-METHOD, FS-DATA; source family freesolv.

Adjudication: The record note explicitly says the experimental uncertainty is unavailable and a default was assigned. The numeric field alone does not provide a confidence level or replication design.

Correctness criteria:

- Read the default-assignment note.
- Distinguish an assigned uncertainty convention from measured replicate-based uncertainty.

Ambiguity/limitations: Public curated experimental/calculated thermodynamic records,not original laboratory raw measurements. Individual primary experimental papers and full transfer standard-state corrections are not independently replayed. Default uncertainties are not measured error bars. No protein-binding or temperature-series validation is supplied.

Recomputed numeric witness: `{"expected": {"compound": "methanol", "default_note": true, "uncertainty": "3/5"}, "operation": "freesolv_default"}`.

### FS03S: refuted

Claim: The methanol 0.60 kcal/mol field is a measured 95%confidence interval from independent replicate hydration experiments.

Evidence: FS-METHOD, FS-DATA; source family freesolv.

Adjudication: The source explicitly calls 0.60 an assigned default because experimental uncertainty is unavailable;this contradicts describing that field as a measured 95%confidence interval.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Public curated experimental/calculated thermodynamic records,not original laboratory raw measurements. Individual primary experimental papers and full transfer standard-state corrections are not independently replayed. Default uncertainties are not measured error bars. No protein-binding or temperature-series validation is supplied.

### FS04N: empirically_supported

Claim: For neopentane, the displayed FreeSolv experimental and calculated hydration values both equal 2.51 kcal/mol.

Evidence: FS-METHOD, FS-DATA; source family freesolv.

Adjudication: The source reports both values as 2.51 with experimental uncertainty 0.60(default) and calculated uncertainty 0.02. Displayed agreement is not zero uncertainty or validation over temperature.

Correctness criteria:

- Identify equality of the rounded displayed values.
- Retain nonzero uncertainty and distinguish display equality from exact physical identity.

Ambiguity/limitations: Public curated experimental/calculated thermodynamic records,not original laboratory raw measurements. Individual primary experimental papers and full transfer standard-state corrections are not independently replayed. Default uncertainties are not measured error bars. No protein-binding or temperature-series validation is supplied.

Recomputed numeric witness: `{"expected": {"calculated": "251/100", "calculated_uncertainty": "1/50", "compound": "neopentane", "experimental": "251/100", "experimental_uncertainty": "3/5"}, "operation": "freesolv_equal"}`.

### FS04S: insufficient_evidence

Claim: Equality of the two displayed neopentane values proves exact physical prediction with zero model discrepancy at every temperature.

Evidence: FS-METHOD, FS-DATA; source family freesolv.

Adjudication: The admitted measurement and design do not supply the population, mechanism or applicability evidence required by this stronger claim.

Correctness criteria:

- Identify the exact scope extension.
- Explain at least one compatible alternative or missing validation; do not assert the stronger claim is false.

Ambiguity/limitations: Public curated experimental/calculated thermodynamic records,not original laboratory raw measurements. Individual primary experimental papers and full transfer standard-state corrections are not independently replayed. Default uncertainties are not measured error bars. No protein-binding or temperature-series validation is supplied.

## What independent reviewers should challenge

The narrow empirical labels concern source-reported observations,not confirmation that laboratories and data transcriptions were error-free. R datasets are curated secondary transcriptions with incomplete original methods. FreeSolv inherits upstream licensing caveats and heterogeneous uncertainty conventions. All sixteen stronger/negative claims are authored examples and may have stylistic cues;no general scientific reasoning result can be inferred from their synthetic wording. Four source families are too few for a stable source-population estimate. Source groups,not rows or paired variants,are appropriate robustness units. Labels need domain expert review before release as a definitive benchmark.

## Prefreeze corrections retained for review

The first materialized,unfrozen draft contained two manually transcribed grass summary errors. The CO03 Mississippi chilled high-concentration row is21.9(not21.4),giving mean281/15;CO04 Quebec chilled third row is41.4(not39.6),giving mean245/6. Raw source records were never altered. Exact replay identified and corrected both before scored runs;the negative test deliberately injects the old CO03mean557/30and verifies rejection. Two interpretation labels were also refined before freeze:the claim of84independent plants contradicts a12plant repeated-measure design,and a measured95%confidence-interval description contradicts a source note marking an uncertainty as default;both are refuted rather than merely insufficient.

All13reference tests passed at candidate handoff,including source corruption,numeric-reference corruption,source-split integrity,and withholding-evidence reference behavior. The17numeric witness checks verify arithmetic and source-record alignment only. There is no mechanical proof of the empirical/interpretive labels,and no outside expert or human adjudicator has yet approved them.
