# Phase IIb: additional source families for SVB0.3.0

This12-case extension contains six matched pairs from three scientific studies not used in SVB0.2.0. The studies are all public R datasets and may be familiar to pretrained systems. A new study-family split is not a hidden set, proof of training noncontamination, or blinded adjudication. The frozen0.2.0 release remains historical/development material; none of its files is changed.

## Provenance,license and scientific limits

Official R source commit95b95f1a200c97a9aa027fe020263d2493141526 is archived by content hash in the new registry. Each dataset’s manual explicitly says it is distributed under GPL2or later. COPYING and package DESCRIPTION are retained. These source/data files remain GPL2-or-later and are not relicensed as Apache. No primary laboratory dataset was manufactured, and no evaluated-system output informed labels.

- **Sleep**:20records for10persons,paired across two soporific drugs; extra is hours of sleep increase compared with control. The manual warns group does not mean independent groups. Source citations Cushny and Peebles1905and Student1908are preserved;full primary treatment ordering,washout and sampling details were not independently reconstructed.
- **ChickWeight**:578growth observations on50chicks,with recorded protein diet,age in days and body weight in grams. Sources Crowder and Hand1990and Hand and Crowder1996are textbook transcriptions cited by R. An important transformation is source integer factor-code→explicit chick-ID label mapping. Raw integer code15names chick1,not chick15. Day21diet1and4observed sample sizes differ16versus9;complete-case means do not establish survival-adjusted or population causal effects.
- **BOD**:six recorded biochemical oxygen-demand values in mg/L versus days,attributed by R to Marske1967via Bates and Watts1988AppendixA1.4. Original water source,replication,organisms,error model and original methods are not independently verified. A nonmonotone observed segment does not uniquely establish a microbial mechanism.

All12labels are provisional author adjudications. Exact checks establish source-record and arithmetic properties;they do not validate laboratories,physical precision,clinical benefit,causal identification or population generalization. Narrow observed comparisons have empirical and computational allowed scopes;exact sample means and unit conversions use computationally_established. False numeric conclusions are refuted;unsupported causal/universal/mechanistic conclusions are insufficient_evidence.

## Variant policy

For evidence,no_assumptions,verified_numbers and paraphrase,the legitimate source observations and method facts remain available,so the reference label is unchanged. Separate assumptions only remind the reader of stored-number arithmetic. With every evidence document removed,the packet contains neither observed values nor an independently admitted record:every no_evidence reference is insufficient_evidence with empty scopes. This applies to originally refuted claims too and measures justification conditional on admitted evidence,not factual memory. Labels,checks,pair roles and missing-evidence analyses are never model inputs. Source documents contain legitimate methods/data,not adjudicator-written absent-evidence checklists.

## Dossiers

### SL01P: computationally_established

Target: Using patient ID to pair the recorded observations, the mean of drug 2 minus drug 1 sleep prolongation is 1.58 hours.

Evidence: SL-METHOD, SL-OBS;source family sleep.

Reference: Ten within-ID differences sum to 15.8 hours, giving an arithmetic mean of 1.58 hours.

Criteria:

- Pair records by patient ID rather than treating group labels as different persons.
- Compute the mean within-patient difference with hours as the unit.

Limitations: Curated historical R transcription, not an independent replication of the original experiment. Full primary protocols, treatment ordering, washout, measurement error and population sampling were not independently reconstructed. Exact calculations establish properties of recorded observations only.

Exact witness: `{"expected": {"mean_difference_hours": "79/50", "pairs": 10, "sum_difference_hours": "79/5"}, "operation": "sleep_paired_mean"}`.

### SL01X: refuted

Target: Using patient ID to pair the recorded observations, the mean of drug 2 minus drug 1 sleep prolongation is 3.16 hours.

Evidence: SL-METHOD, SL-OBS;source family sleep.

Reference: The recorded paired differences have mean 79/50 = 1.58 hours, contradicting the proposed 3.16-hour mean.

Criteria:

- Compute the paired mean rather than accepting a plausible supplied number.
- Identify the numerical contradiction without making a population-level treatment claim.

Limitations: Curated historical R transcription, not an independent replication of the original experiment. Full primary protocols, treatment ordering, washout, measurement error and population sampling were not independently reconstructed. Exact calculations establish properties of recorded observations only.

Exact witness: `{"expected": {"mean_difference_hours": "79/50", "pairs": 10, "sum_difference_hours": "79/5"}, "operation": "sleep_paired_mean"}`.

### SL02N: empirically_supported

Target: In every recorded patient pair, the sleep prolongation under drug 2 is at least as large as under drug 1.

Evidence: SL-METHOD, SL-OBS;source family sleep.

Reference: Nine recorded paired differences are positive and one is zero. No recorded patient has a negative drug-2-minus-drug-1 difference.

Criteria:

- Check all 10 patient pairs.
- Preserve the non-strict comparison and scope to recorded patients.

Limitations: Curated historical R transcription, not an independent replication of the original experiment. Full primary protocols, treatment ordering, washout, measurement error and population sampling were not independently reconstructed. Exact calculations establish properties of recorded observations only.

Exact witness: `{"expected": {"equal": 1, "greater": 9, "less": 0, "pairs": 10}, "operation": "sleep_signs"}`.

### SL02S: insufficient_evidence

Target: The recorded patient comparisons establish that drug 2 will increase sleep more than drug 1 for every future patient.

Evidence: SL-METHOD, SL-OBS;source family sleep.

Reference: A finite historical sample does not establish a strict benefit for every future patient; sampling, heterogeneity and applicability remain unestablished. One observed tie also prevents describing all recorded differences as strict increases, but it does not refute the separate universal future-patient target.

Criteria:

- Identify the shift from a finite recorded sample to every future patient.
- Explain why finite favorable observations do not establish a universal individual treatment response; do not claim the future outcome has been observed false.

Limitations: Curated historical R transcription, not an independent replication of the original experiment. Full primary protocols, treatment ordering, washout, measurement error and population sampling were not independently reconstructed. Exact calculations establish properties of recorded observations only.

### CW01P: computationally_established

Target: Among the supplied day-21 observations, the arithmetic mean weight for diet 4 exceeds that for diet 1 by exactly 2189/36 grams.

Evidence: CW-METHOD, CW-DAY21;source family chick_growth.

Reference: The 16 observed diet-1 weights have mean 711/4 g; the 9 observed diet-4 weights have mean 2147/9 g. Their difference is 2189/36 g.

Criteria:

- Use only supplied day-21 observations and their unequal denominators.
- Subtract the diet-1 mean from the diet-4 mean without treating arithmetic exactness as physical precision.

Limitations: Curated textbook/R observations rather than verified original laboratory records. Missing follow-up and selection are not resolved by a complete-case sample mean. Full diet composition, assignment, husbandry, original uncertainty and laboratory protocol were not independently obtained. No population-level causal effect is established by the stored-number arithmetic.

Exact witness: `{"expected": {"diet1_mean_g": "711/4", "diet1_n": 16, "diet4_mean_g": "2147/9", "diet4_minus_diet1_g": "2189/36", "diet4_n": 9}, "operation": "chick_day21"}`.

### CW01X: refuted

Target: Among the supplied day-21 observations, the arithmetic mean weight for diet 4 is lower than that for diet 1.

Evidence: CW-METHOD, CW-DAY21;source family chick_growth.

Reference: The recorded means are 2147/9 g for diet 4 and 711/4 g for diet 1; diet 4 is higher, so the target reverses the sample comparison.

Criteria:

- Compute the two sample means with correct denominators.
- Identify the reversed inequality, retaining the observed-sample scope.

Limitations: Curated textbook/R observations rather than verified original laboratory records. Missing follow-up and selection are not resolved by a complete-case sample mean. Full diet composition, assignment, husbandry, original uncertainty and laboratory protocol were not independently obtained. No population-level causal effect is established by the stored-number arithmetic.

Exact witness: `{"expected": {"diet1_mean_g": "711/4", "diet1_n": 16, "diet4_mean_g": "2147/9", "diet4_minus_diet1_g": "2189/36", "diet4_n": 9}, "operation": "chick_day21"}`.

### CW02N: empirically_supported

Target: The recorded body weight of chick 1 increased from 42 grams at birth to 205 grams on day 21 while it received diet 1.

Evidence: CW-METHOD, CW-CHICK1;source family chick_growth.

Reference: The supplied series records 42 g at Time 0 and 205 g at Time 21 for chick 1, whose Diet value is 1. This describes a within-chick observed change.

Criteria:

- Match the same chick ID and the two measurement times.
- Describe observed growth under diet 1 without assigning all growth causally to that diet.

Limitations: Curated textbook/R observations rather than verified original laboratory records. Missing follow-up and selection are not resolved by a complete-case sample mean. Full diet composition, assignment, husbandry, original uncertainty and laboratory protocol were not independently obtained. No population-level causal effect is established by the stored-number arithmetic.

Exact witness: `{"expected": {"birth_g": "42", "chick": "1", "day21_g": "205", "observed_gain_g": "163"}, "operation": "chick_one_growth"}`.

### CW02S: insufficient_evidence

Target: The growth series of chick 1 establishes that diet 1 caused exactly 163 grams of additional body weight compared with what this chick would have weighed without diet 1.

Evidence: CW-METHOD, CW-CHICK1;source family chick_growth.

Reference: An observed within-chick change is not an observed counterfactual diet effect. Development with age and other husbandry conditions can accompany the same series; the unobserved alternative weight is not identified.

Criteria:

- Distinguish a temporal gain of 163 g from a counterfactual causal contrast.
- Identify the unobserved alternative-diet outcome or adequate causal design that would be needed, without asserting the treatment effect is zero.

Limitations: Curated textbook/R observations rather than verified original laboratory records. Missing follow-up and selection are not resolved by a complete-case sample mean. Full diet composition, assignment, husbandry, original uncertainty and laboratory protocol were not independently obtained. No population-level causal effect is established by the stored-number arithmetic.

### OD01P: computationally_established

Target: The recorded demand on day 7 minus the recorded demand on day 1 equals 0.0115 grams per litre.

Evidence: OD-METHOD, OD-OBS;source family oxygen_demand.

Reference: The stored difference is 19.8 - 8.3 = 11.5 mg/L. Dividing by 1000 gives 0.0115 g/L.

Criteria:

- Subtract the two recorded values.
- Convert milligrams to grams using 1000 mg = 1 g while retaining the per-litre denominator.

Limitations: The small table is a curated historical transcription, not independently verified raw water-sample or laboratory records. No replicate structure, organism identification, experimental error model or physical mechanism is independently established here. Recorded nonmonotonicity alone need not be nonmonotonicity of an underlying latent process.

Exact witness: `{"expected": {"day1_mg_per_L": "83/10", "day7_mg_per_L": "99/5", "difference_g_per_L": "23/2000", "difference_mg_per_L": "23/2"}, "operation": "oxygen_change"}`.

### OD01X: refuted

Target: The recorded demand on day 7 minus the recorded demand on day 1 equals 11.5 grams per litre.

Evidence: OD-METHOD, OD-OBS;source family oxygen_demand.

Reference: The difference is 11.5 mg/L, not 11.5 g/L. The target is 1000 times the stored difference expressed in g/L.

Criteria:

- Check the original mg/L unit.
- Identify the factor-1000 conversion error, not merely the subtraction.

Limitations: The small table is a curated historical transcription, not independently verified raw water-sample or laboratory records. No replicate structure, organism identification, experimental error model or physical mechanism is independently established here. Recorded nonmonotonicity alone need not be nonmonotonicity of an underlying latent process.

Exact witness: `{"expected": {"day1_mg_per_L": "83/10", "day7_mg_per_L": "99/5", "difference_g_per_L": "23/2000", "difference_mg_per_L": "23/2"}, "operation": "oxygen_change"}`.

### OD02N: empirically_supported

Target: The recorded oxygen-demand values decrease between day 3 and day 4.

Evidence: OD-METHOD, OD-OBS;source family oxygen_demand.

Reference: The table records 19 mg/L at day 3 and 16 mg/L at day 4, a decline in these observations.

Criteria:

- Locate the two specified observations.
- Limit the statement to the recorded data rather than a noiseless latent process or mechanism.

Limitations: The small table is a curated historical transcription, not independently verified raw water-sample or laboratory records. No replicate structure, organism identification, experimental error model or physical mechanism is independently established here. Recorded nonmonotonicity alone need not be nonmonotonicity of an underlying latent process.

Exact witness: `{"expected": {"day3_mg_per_L": "19", "day4_mg_per_L": "16", "drop_mg_per_L": "3", "nonmonotone": true}, "operation": "oxygen_nonmonotone"}`.

### OD02S: insufficient_evidence

Target: The observed day-3 to day-4 decline uniquely establishes that the microorganisms in the water stopped aerobic respiration during that interval.

Evidence: OD-METHOD, OD-OBS;source family oxygen_demand.

Reference: A pair of demand readings does not uniquely identify microbial respiration or its cessation. Measurement variation, sampling and alternative processes remain compatible with the same recorded decline.

Criteria:

- Distinguish a measured decrease from a unique biological mechanism.
- Give at least one compatible alternative and avoid asserting that respiration actually ceased or certainly did not cease.

Limitations: The small table is a curated historical transcription, not independently verified raw water-sample or laboratory records. No replicate structure, organism identification, experimental error model or physical mechanism is independently established here. Recorded nonmonotonicity alone need not be nonmonotonicity of an underlying latent process.

## Reproduction and review needs

Run `PYTHONPATH=src python -m svb.phase2b_references` and the new `tests/test_phase2b_references.py` suite. Numeric witnesses are fixed independently of model responses and checked against source-derived tables. No external domain panel has adjudicated category boundaries. Reviewers should challenge the empirical-versus-computational label interpretation,the secondary nature of every source,classic-dataset contamination,small study-family count,complete-case chick selection,and authored strong-claim wording. No population performance conclusion follows from twelve cases.
