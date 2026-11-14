# Phase IIb reference-adjudication audit

**Status: internal author/model-agent audit. No external reviewer has been
contacted, recruited, or represented as having approved any reference.** No
historical gold is overwritten. Expert qualifications, exposure declarations,
independent ratings and disagreements remain prerequisites for external
qualification.

## What is being audited

The eleven historical `empirically_supported` references in SVB 0.2.0 are
source-backed descriptions of recorded data or a published report. Their
arithmetic/source transcription is reproducible, but that does not settle the
exclusive six-category adjudication. A proposition about the displayed contents
of an experimental table can be computationally established and descriptively
supported by a source at the same time. These evidence types are not mutually
exclusive scientific states. Exact-category agreement must therefore be
reported separately from coarse acceptance/nonacceptance, with category
ambiguity explicitly visible. No post-result convenient relabelling is
permitted.

None of these eleven is an independently replicated biological discovery, a
population-effect estimate qualified by an external panel, or a guarantee that
the original measurement process was accurate. They must not be advertised as
eleven externally validated empirical scientific inferences.

## Historical eleven: preserved facts and qualification questions

The times below are **planning estimates per reviewer**, not measured review
labor, commitments, recruitment, or completed ratings. They include inspecting
the supplied packet and calculation, not a full literature investigation. If
source retrieval or methods reconstruction is needed, the reviewer must record
actual additional time or mark the evidence gap unresolved. At least two
independent domain scientists and one statistical/methods reviewer are required
under the existing human-review protocol; a coordinator does not substitute for
one of those reviews.

| Case | Source/computation confirmed internally | Main adjudication question | Needed expertise and priority | Estimated first-pass time |
|---|---|---|---|---|
| PG01N | Nonmissing Gentoo mean `624350/123 g` exceeds Adélie `558800/151 g` in the archived rows | Is the atomic target an archived sample comparison, a physical species difference, or a population statement? Is one exclusive evidence-type category appropriate? | Quantitative ecology plus missing-data/statistical review; P2 | 15–25 min |
| PG02N | Sex-identified Adélie records have 73 male masses summing 295175 g and 73 female masses summing 245925 g | Does filtering recorded sex/mass define the target sample clearly? What, if any, inference survives selection/missingness? | Penguin/ecological measurement specialist and biostatistician; P2 | 15–25 min |
| PG04N | The primary Gorman et al. article reports 39/44 held-out Adélie classifications, 88.64% | Is “the article reports” a provenance fact rather than an independently reproduced prediction-performance result? Were study holdout and target population preserved? | Classification/validation statistician and quantitative ecologist; P1 | 20–35 min |
| PU01N | At 0.11 ppm, treated values 123/139 average 131; untreated 98/115 average 106.5 counts/min/min | Does a calculated condition summary justify a descriptive recorded comparison while leaving replication/population uncertainty unknown? | Enzyme-assay scientist plus experimental-design statistician; P1 | 15–25 min |
| PU02N | At 1.1 ppm, treated values are 207 and 200, untreated is 160 | Does a table lookup require an empirical-status verdict, or is a computational/source-transcription verdict equally defensible? What is actually known about biological replication? | Enzyme-assay scientist and biostatistician; P1 | 15–25 min |
| PU03N | Treated mean rate rises from 61.5 to 203.5; ratio `407/123` is below the concentration ratio 55 | Are ratio arithmetic, assay observation, and kinetic-mechanism interpretation properly separated? | Enzyme kinetics and nonlinear-model/statistical expertise; P1 | 20–30 min |
| CO01N | Qn1 has recorded uptake 35.3 at concentration code 500, below 37.2 at code 350 | Does the packet preserve the unresolved source concentration-unit transcription and the distinction between one observed decrease and a reproducible inhibitory response? | Plant ecophysiology and repeated-measures statistician; P1 | 20–30 min |
| CO03P | Mississippi means at code 1000 are `158/5` nonchilled versus `281/15` chilled, three plants per group | Is the finite observed ordering the only target, or is a causal/population treatment effect being inferred? | Plant ecophysiology and experimental-design statistician; P1 | 20–30 min |
| CO04N | Quebec means at code 1000 are `259/6` nonchilled versus `245/6` chilled, three plants per group | Are plant-level units, repeated concentrations and the scope of the finite comparison preserved? | Plant ecophysiology and repeated-measures statistician; P1 | 20–30 min |
| FS01N | FreeSolv records experimental hydration values −5.00 for ethanol and +2.00 for methane, in kcal/mol | Is this a curator-reported numerical ordering or a separately qualified physical ordering? Are solvent/standard-state/temperature assumptions sufficient for any stronger interpretation? | Physical chemistry/solvation thermodynamics and measurement-UQ expertise; P1 | 25–40 min |
| FS04N | Neopentane’s displayed experimental/calculated values both equal 2.51 kcal/mol; nonzero uncertainty fields and assigned-default note remain | Does equality of rounded source fields establish only displayed equality? Is `computationally_established` a valid co-category, and what would “empirical support” add? | Molecular free-energy specialist and measurement-UQ expert; highest priority | 25–40 min |

Numeric/source checks identify no false archived value in these eleven. The
principal unresolved issue is the meaning and exclusivity of the category,
followed by what experimental/measurement assumptions are actually admitted.
The original Treloar thesis, Potvin primary experiment and individual FreeSolv
primary measurement methods were not all obtained or replayed. Experts must
not be asked to certify those absent materials as if they had inspected them.

The eleven internal first-pass estimates sum to approximately 210–335 minutes
per appropriately qualified reviewer, before source onboarding, duplicated
independent reviews, coordinator checks or arbitration. Expertise should be
assigned by family, not by expecting one person to cover all domains. The
reviewer-facing distribution package should contain all historical and new
cases, not merely the eleven currently positive-labelled cases; selecting only
those would itself expose an adjudication cue.

## Neutral questions for external reviewers

Use these questions for every case, including refuted and insufficient-evidence
controls. Case-specific expected answers or the historical label must not be
embedded in the reviewer packet.

1. What exactly is the atomic target: a statement about supplied bytes/report,
   a mathematical calculation, a recorded measurement, an observed sample
   comparison, a population/causal effect, a mechanism, or a physical prediction?
2. Which parts can be checked from the packet, which require assumptions, and
   which require unavailable evidence? State evidence locations and, where
   possible, reproduce the relevant arithmetic.
3. Is the target contradicted, supported within its stated scope, or unresolved
   by this evidence envelope? Distinguish failure of one justification from
   falsity of the target proposition.
4. Which evidence-type categories apply? If several apply or none is uniquely
   defensible, record that ambiguity instead of forcing an exclusive category.
5. Are units, experimental units, repeated measurements, source provenance,
   uncertainty and relevant conditioning/selection rules preserved?
6. What narrower conclusion survives, and what additional evidence would be
   necessary for the proposed stronger conclusion, if any?

## New-family qualification plan

The intended new families are `sleep`, `ChickWeight` and `BOD`, supplied through
pinned official R datasets and associated GPL-2.0-or-later documentation. They
are secondary curated study transcriptions; acquisition of an official package
snapshot does not amount to retrieving or replicating original laboratory
methods. Their final packets and references require a separate pre-freeze audit.

* Sleep: clinical trial/paired-design statistician plus a clinician or
  psychopharmacology researcher. Verify that repeated patient identifiers,
  treatment labels and comparison-to-control definitions are handled correctly;
  do not manufacture randomization/crossover/washout details absent from source
  methods. Budget 20–40 minutes per case plus primary-source retrieval if needed.
* ChickWeight: longitudinal experimental-design statistician and poultry/nutrition
  scientist. Audit diet assignment, repeated chick trajectories, missing or
  unequal follow-up and the distinction between observed diet differences and
  causal/universal efficacy. Budget 20–40 minutes per case.
* BOD: environmental/aqueous chemistry scientist and nonlinear-model/measurement
  specialist. Audit oxygen-demand units, sampling/time structure and whether
  six readings establish merely a displayed trend or an identified kinetic
  process. Budget 15–30 minutes per case.

No provisional label or packet is called expert-adjudicated before actual
qualified independent ratings exist. No invitations, messages or personal data
are produced by this audit.

## Pre-freeze audit of the twelve new cases

The materialized v0.3.0 candidate contains four cases per source family, in six
paired controls. All twelve are new to SVB's evaluation set, not guaranteed to be
unseen by pretrained models. The three R dataset families are preserved as
secondary curated transcriptions with source hashes, GPL notices and explicit
primary-methods limitations. No new source-file or numeric-reference defect was
found in this audit.

| New cases | Source fact independently checked | Scope assessment and external question |
|---|---|---|
| SL01P / SL01X | Pairing the two ten-value vectors by patient ID gives differences 1.2, 2.4, 1.3, 1.3, 0, 1, 1.8, 0.8, 4.6, 1.4 hours; sum 15.8 and mean 1.58 | The 3.16-hour assertion contradicts the supplied arithmetic. Check that the target is the finite displayed-data mean, not a clinical average causal effect. |
| SL02N / SL02S | Nine recorded paired differences are positive, one is zero, none is negative | The recorded nonnegative pattern is supported. It does not establish a strict improvement for every future patient. The observed tie is not itself a counterexample about a distinct future population. Category overlap between observed table fact and computational check remains a reviewer question. |
| CW01P / CW01X | Day-21 diet-1 observations: n=16, sum 2844 g, mean 711/4 g. Diet 4: n=9, sum 2147 g, mean 2147/9 g. Difference 2189/36 g | The reverse ordering is refuted for these supplied observations. Unequal observed follow-up counts must not be turned into complete-cohort means or an unqualified causal diet effect. |
| CW02N / CW02S | Chick 1 has weight 42 g at birth and 205 g on day 21 under recorded diet 1; observed gain 163 g | The within-chick observed change is supported. The unobserved counterfactual weight without diet 1 is not identified by that series; 163 g observed growth is not thereby 163 g caused by the diet. |
| OD01P / OD01X | Day 7 minus day 1 is 19.8−8.3=11.5 mg/L = 0.0115 g/L | The 11.5 g/L assertion is a factor-1000 unit error. Treating stored decimals as exact computation inputs does not imply physically exact measurements. |
| OD02N / OD02S | Recorded demand goes from 19 mg/L at day 3 to 16 mg/L at day 4 | A decline in supplied readings is supported, not unique identification that microorganisms stopped aerobic respiration. Sampling, measurement and process interpretation are not supplied by a two-point comparison. |

The planned new empirical-status cases SL02N, CW02N and OD02N retain the same
evidence-type ambiguity as the historical descriptive cases: they are narrowly
reported observations and can also be checked as computations on supplied data.
The internal audit endorses the narrow facts and refusal of unsupported
extensions, not an externally certified exclusive category. Coarse
acceptance/nonacceptance and exact six-category agreement must remain distinct.

## Prospective format/competence separation review

Task A requires one plain category string. Task B requests short explanatory
prose and document attribution. Task C retains a rich response schema. Their
admission rates answer different engineering questions. Formatting success alone
must not become scientific success; exact citation-ID checks must not become
reasoning-entailment scores.

A response body with unsupported syntax is not automatically a wrong scientific
argument, and a category-only output matching gold supplies no reasoning to
adjudicate. Noncompleted outputs, malformed outputs, missing runs and unsupported
capability remain explicit denominators. A failed run that carries a purported
verdict cannot silently be treated as an ordinary abstention.

Any A-versus-C comparison must use the same selected cases, source families,
information condition and model. Comparing A over twelve tasks against C over a
different subset would confound task composition with format burden. Likewise,
rotating category definitions in A while keeping the category order fixed in C
would make the difference a bundle of instruction changes, not a clean causal
estimate of output-schema burden. Qualification, protocol changes and model
selection must occur using development/qualification material before the new
source-family evaluation, with unsuccessful runs retained.

## Completed pre-evaluation engineering and package review

The independent reviewer-owned suite
`tests/test_phase2b_adversarial.py` executed **16 tests, all passed**. Checks
include strict minimal-label admission without JSON/fence/case/alias repair;
rotation of the actual label definitions; private-reference exclusion; exact
category versus coarse acceptance; timeout/unsupported/malformed/missing
outcomes in total denominators; rejection of contradictory noncompleted
verdicts; duplicate/foreign/mixed-interface envelopes; explicit source-family
summaries; condition-specific references; and separate attribution, reasoning
and rich-schema admission results.

The separate new-source suite executed **12 tests, all passed**, including
source hashes, source-to-extraction consistency, nine numerical witnesses,
wrong-reference/data-corruption detection, source family/pair integrity, actual
R factor labels, and the observational/counterfactual distinction. The separate
review-package suite executed **10 tests, all passed**.

The prepared external-review package was also inspected independently. The
reviewer-facing `prepared_v1/reviewer_package.zip` contains 44 mixed packets
(all 32 historical and 12 new), 132 blank first-round forms, the neutral rubric,
a blank conflict/exposure declaration, source registry, licensed source
snapshots and a file-hash manifest. No internal coordination mapping is in the
ZIP. Recursive inspection of packet/source-manifest metadata found no exported
reference/gold/checker/model/provider/split/family/pair/role fields. The internal
mapping and this audit report must not be handed to a supposedly reference-blind
rater before locking first-round judgments.

The package is prepared for coordinator review and separately authorized
recruitment/distribution. No distribution, contact, human review, confidentiality
boundary or actual blinding is claimed. Public labels, recognizable claims and
source knowledge can still expose a provisional reference; exposure declarations
and coordinator audit remain essential.

Task C deliberately preserves the historical rich instruction bundle, including
its original category ordering, whereas A counterbalances definitions. Their
matched-case comparison is therefore descriptive of different interface bundles,
not a causal estimate of schema burden alone. The cleaner syntax intervention
is unconstrained versus six-category-constrained A under otherwise matched
prompts/model/settings; constraints can force legal vocabulary without creating
scientific competence. Task B's automatic attribution/completion indicators
remain separate from human scientific-reasoning assessment.

No model evaluation results were used to adjust labels or these reference
judgments. Existing frozen releases and subject repositories were not modified
by this reviewer. Further human qualification and scientific performance remain
open rather than inferred from passing software checks.
