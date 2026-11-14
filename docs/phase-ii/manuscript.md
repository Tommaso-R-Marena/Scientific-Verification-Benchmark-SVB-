# Scientific Verification Beyond Correct Calculation: A Source-Grounded Pilot

**Phase II working manuscript, SVB 0.2.0. Publication-oriented draft; not
publication-ready or externally expert-qualified.** This draft reports completed
reference, baseline, local-system, and 60-response offline-model experiments.
The model experiment completed generation but failed strict response admission
on every output. Human scientific reasoning assessment has not occurred. No
paper or scientific claim has been published by preparing this document.

## Abstract

Correct arithmetic and faithful quotation need not justify an empirical,
causal, or mechanistic scientific conclusion. We present Phase II of an
independent Scientific Verification Benchmark (SVB), replacing explicit
missing-evidence declarations in an earlier diagnostic pilot with naturalistic
source records and methods. The release contains 32 claims in 16 pairs from four
source families. Eight penguin-source items form development data; 24 evaluation
items use enzyme-rate observations, repeated plant-uptake measurements, and
hydration thermodynamics. The evaluation labels comprise eight narrowly empirical
source facts, four computational conclusions, eight insufficient-evidence
judgments, and four refutations. All labels are provisional author adjudications;
zero external human reviews have occurred. Seventeen numerical witnesses and
documented source transformations were independently recomputed. A weak lexical
policy scored 13/24 with six false acceptances among 12 nonacceptance references.
A public-packet numerical parser scored 3/24 with 4/24 coverage, illustrating
that coverage, categorical agreement, and scientific acceptance differ.
Noninvasive tests matched independent finite references for FoldBounds on 27/27
controls, PCS on 6/6 eligible controls with two unsupported capabilities retained,
and website DOM workflows on 8/8 observations. FoldBounds' sampled shallow
probability intervals remained almost vacuous despite valid enclosure and much
narrower partition bounds. A pinned offline Qwen2.5-0.5B-Instruct run completed all
60 requested generations across five information conditions, but none satisfied
the strict schema. Every output's unique explicit JSON label was
`formally_established`, a category absent from the new reference set, giving zero
secondary exact-label agreement. The primary result is failed model/prompt/schema
qualification, not a zero-accuracy estimate of scientific reasoning. These
results establish an executable, auditable evaluation pipeline and useful
negative controls, not scientific AI reliability, biological validation, or novel
mathematics. Human scientific review remains unperformed.

## 1. Introduction

Scientific verification has several targets. A program may reproduce a statistic
while assuming independent observations where the experiment repeatedly measured
the same plant. A database can contain an uncertainty number that was assigned
as a default rather than measured from replicates. A finite lattice model can
produce an enclosing probability interval without providing a useful estimate,
let alone proving applicability to a physical protein. A system that gives the
right category but attributes it to an irrelevant source creates a different
failure from an incorrect numerical computation.

SVB asks whether such distinctions can be measured reproducibly without taking
an evaluated system's answers as truth. Phase I supplied exact mathematical and
computational controls, including explicit missing-bridge fields. That design
made a narrow end-to-end implementation possible but substantially simplified
the evidence problem. Phase II uses source documents, tables, methods, and paired
claims whose scientific scopes differ while the underlying record remains fixed.
Internal references, pair roles, checker kinds, and absence lists are omitted
from model-facing packets.

Our completed contributions are a public source-grounded evaluation artifact,
independent numerical checks, outcome-preserving scoring, two transparent
baselines, harder noninvasive subject controls, a deeper targeted literature
review, and a prospective human-review protocol. These are research infrastructure
and preliminary measurements. We do not equate naturalistic presentation with
external validity, public freezing with protected testing, or typed evidence with
a new theory of scientific truth.

## 2. Related work and construct distinctions

We retrieved full text for ten selected papers and inspected relevant methods,
evaluation, annotation, exposure, and limitations sections. This is deeper than
Phase I's abstract/metadata pass, but remains a purposive review rather than a
systematic search or full-paper audit. URLs, versions, response-byte hashes,
licenses, and inspected sections are in `references/phase2_registry.json`.

SciFact [1] evaluates SUPPORTS/REFUTES/NO INFO relations between scientific claims
and individual abstracts with rationale sentences, explicitly distinguishing
that task from assigning global scientific truth. FEVER [2] couples encyclopedic
claim labels with evidence retrieval and annotation quality checks. Thus
evidence-linked judgments and insufficiency are established constructs. SciBench
[3] evaluates scientific problem solving with numerical answers and units;
answering a specified calculation differs from evaluating an empirical study.

ScienceAgentBench [4] uses publication-derived executable tasks with domain
experts, reference results, and program rubrics. Its methods address memorized
loaders and test-label shortcuts, and its human analysis notes that one reference
implementation can bias a rubric against valid alternatives. SciRIFF [5]
standardizes scientific literature instructions, answer/evidence outputs, and
task-held-out evaluation; removal of known training overlaps is not proof of
absence of unknown pretraining exposure.

PaperQA2's LitQA2 [6] asks main-text literature questions and documents human
comparisons, including a public-question indexing problem that invalidated part
of a later comparison. ScholarQABench belongs instead to OpenScholar [7], with
multi-paper questions, expert rubrics, citation measurements, and human
preferences. Those preferences do not by themselves establish citation validity
or empirical adequacy. ALCE [8] likewise distinguishes answer correctness,
fluency, and citation quality; text-copying shortcuts can score well on one
component while failing another.

Selective prediction [9] supplies risk–coverage reasoning under explicit sampling
assumptions. Calibration work [10] separates confidence agreement from accuracy
and requires an appropriate validation/test design. Neither imports a deployment
guarantee into this small, related, purposive dataset. These precedents rule out
a novelty assertion based merely on combining scientific text, citations,
uncertainty, program execution, and several metrics. Any distinct value of SVB
must be established through qualified tasks and real comparative evidence.

## 3. Scientific formulation and hypotheses

Each claim is evaluated against a fixed admitted record: assumptions, scientific
model or design, source identities, data transformations, methods, and intended
scope. Six categories are retained: formally established, computationally
established, empirically supported, refuted, insufficient evidence, and
disputed/unresolved. Labels identify the support available for the stated target,
not universal truth beyond the record.

“Empirically supported” in Phase II means a narrow descriptive observation or
source-reported experimental fact under its named context. Exact reproduction of
the source table does not prove the original laboratory execution occurred as
reported. A correctly computed fact and an inadequately supported population
effect can coexist. Refuting a supplied interpretation need not refute its
underlying descriptive statistic; missing evidence is not automatically a false
claim.

The frozen protocol states four exploratory hypotheses:

| Hypothesis | Operational question | Evidence grade at this draft |
|---|---|---|
| H1 | Do exact-label agreement, false acceptance, and attribution checks reveal different outcomes? | Partly exercised by deterministic baselines and a descriptive raw-output audit. Zero strict model coverage prevents a scientific-accuracy conclusion; reasoning remains unadjudicated. No claim about conventional QA systems generally. |
| H2 | Can policies distinguish a narrow source fact from a stronger paired claim using naturalistic evidence? | Measured on 12 pairs for transparent baselines. The small model's invariant unused-category labels and zero strict admission do not establish naturalistic scientific discrimination or its general absence. References remain provisional. |
| H3 | Does numerical assistance change judgments without resolving empirical interpretation? | All four assistance responses were generated, but none was admitted and all extracted labels were unchanged. No informative assistance effect is established; the subset has only two enzyme pairs from one source. |
| H4 | Does an evidence-dependency framework improve scientific verification beyond established alternatives? | Not established. Requires independent human adjudication, competent comparison systems, and prospective evaluation. |

The earlier elementary Lean unary scope-closure proof remains a conditional
syntactic invariant. It neither verifies the Phase II implementation nor proves
scientific premise truth or the practical utility of the evidence representation.
No new mathematical result is claimed here.

## 4. Dataset construction and ground-truth protocol

### 4.1 Sources, pairs, and split

There are 32 cases in 16 pairs. Penguin observations and a primary PLOS article
[11] supply eight development cases. The evaluation set has eight Puromycin,
eight grass CO2, and eight FreeSolv cases: 24 claims in 12 pairs. The split is
disjoint by underlying source family; public datasets and records remain
potentially familiar to pretrained models. Three evaluation families do not
constitute three representative samples of all science, and paired claims are
not independent observations.

| Source family | Split and cases | Evidence and important limitation |
|---|---|---|
| Palmer penguins and Gorman et al. primary article | Development, 8 | Field observations at a particular breeding stage; repeated ID strings are not a verified animal-linkage key, and seasonal/geographic causal extensions are not established. |
| R Puromycin transcription | Evaluation, 8 | Historical enzyme concentration/rate observations and source manual; original thesis/full laboratory methods were not obtained. Twenty-three readings are not 23 independent biological experiments. |
| R CO2 plant experiment transcription | Evaluation, 8 | Twelve plants measured at seven concentrations; 84 rows do not represent 84 independent plants. Original primary article not obtained; source concentration codes are preserved without silently resolving unit transcription. |
| FreeSolv v0.52 | Evaluation, 8 | Published-reference experimental/calculated hydration records; default uncertainty notes retained. Hydration is not protein binding, and full primary measurement methods/standard-state corrections were not reconstructed. |

The evaluation label distribution is eight empirically supported, four
computationally established, eight insufficient evidence, and four refuted.
Across both splits, the corresponding counts are 11, 5, 12, and 4. Unlike Phase I,
Phase II exercises an empirical-support category, but only at narrow
source-record scope. It does not add new empirical biological experiments or
externally validated gold.

### 4.2 Independent reference evidence

`src/svb/phase2_references.py` recomputes numerical witnesses from archived source
bytes without importing the evaluated subjects. The retained checks validate 17
numerical witnesses, all 69 Puromycin cells, 168 CO2 numerical cells, and six
selected FreeSolv records. Source hashes and transformations are checked before
scoring. These checks explicitly report that empirical adequacy was not
mechanically validated and external human adjudication did not occur.

For example, the Puromycin source at recorded concentration 0.11 gives treated
and untreated mean rates 131 and 106.5 counts/min/min, an exact difference 49/2.
That descriptive record does not supply precise population uncertainty across
independent enzyme preparations. The CO2 table has 12 plant IDs and 84 rows;
counting rows correctly cannot justify treating all rows as independent plants.
The FreeSolv methanol record marks 0.60 kcal/mol as an assigned uncertainty
default; describing it as a measured replicate-based 95% confidence interval
contradicts the supplied record.

Reference dossiers identify source evidence, exact criteria, ambiguity, and
limitations. Labels are **provisional author adjudications**. No subject output
was used as an independent reference. Sources and their licenses are recorded in
`data/v0.2.0/registry.json`; upstream GPL, CC0, and CC-BY materials retain their
own rights and caveats rather than inheriting the SVB code license. Rejected
acquisition candidates and prefreeze corrections are documented rather than
quietly treated as qualified sources.

### 4.3 Public packet boundary and information conditions

A public packet contains only question, claim, documents
(`id`, `title`, `text`, `source_id`), methodology, and naturally disclosed
assumptions. Opaque IDs support mapping, not secrecy. Reference labels,
adjudicator rationales, family/pair roles, splits, numeric checker descriptions,
and synthetic missing-evidence lists do not enter the evaluated policy interface.
General response instructions still describe the scientific categories; this is
not an unprompted measure of scientific reasoning.

Five information conditions are frozen. **Evidence** supplies the documents.
**No evidence** withholds them and uses separately adjudicated
insufficient-evidence references; a justified refusal to infer without the record
is not scored against an inaccessible full-record answer. **Verified numbers**
adds calculator facts but no adequacy judgment. **No assumptions** removes a
mostly redundant annotation while methods remain visible, making it a weak
ablation. **Paraphrase** changes the task question, not the underlying claim or
documents; it tests limited wording invariance rather than broad robustness.

## 5. Experimental methods

### 5.1 Executed deterministic policies

The numerical baseline parses only the public packet, reproduces bounded
arithmetic/counts/residuals, and returns unsupported where its declared numerical
interface cannot answer. It does not read source files or references. The
evidence-aware comparator is intentionally a weak lexical policy, not a general
scientific verifier. Its label and scope choices are transparent, one-hot, and
uncalibrated. Both were run against all 24 evaluation items in the evidence
condition.

Primary scoring requires a valid structured response, all six finite
probabilities summing to one, and a selected label consistent with those
probabilities. Missing, unsupported, malformed, timeout, and execution outcomes
remain visible. Exact category agreement is separated from coarse epistemic
decision agreement: a supported empirical source fact labeled computationally
established is a category mismatch, not necessarily a false scientific
acceptance. False acceptance uses the 12 refuted/insufficient references; false
rejection uses the 12 support references.

Automatic attribution checks validate supplied evidence IDs and exact quotation
membership. A real quotation may be irrelevant or fail to entail the claim;
semantic attribution, rationale validity, and uncertainty adequacy are unscored
pending human review. Brier loss and confidence-threshold risk apply only to
valid vectors. One-hot policies provide no meaningful confidence ranking.
No population p-value, iid confidence guarantee, or arbitrary severity-weighted
leaderboard is inferred from these related purposive cases.

### 5.2 Completed prespecified real-model experiment

The pinned public `Qwen/Qwen2.5-0.5B-Instruct` checkpoint, revision
`7ae557604adf67be50417f59c2c2f167def9a775`, was downloaded and checked against
recorded hashes. Access and unrelated arithmetic smoke checks completed. The
scientific run executed offline on CPU float32, four threads,
greedy generation, seed 0, with a 4,096-input-token cap and 384-new-token cap.
Inputs are not silently truncated; raw malformed and token-limited outputs are
retained. No paid API or private model credential is used.

The frozen bundle specified 60 calls: 24 evidence, 24 no-evidence, and the first
four evaluation cases each under verified-numbers, no-assumptions, and paraphrase.
There are no correctness-based retries or scientific-label tuning during this
run. Public pretraining exposure is unknown, and the model is a small instruct
checkpoint rather than a representative population of scientific AI systems.

An environment transition interrupted the first session after 46 complete,
durable response envelopes. Their original bytes and identities were preserved;
the exact remaining 14 frozen prompts were resumed in a second session. No
completed response was regenerated or selected by correctness. The concatenated
completed record has 60 unique requested condition/ID pairs, 60 completed
generations, no input truncations, and one output reaching the generation cap.
`qwen_scientific_interruption.json` documents the interruption, preserved prefix,
and exact continuation. The completed record's SHA-256 is
`611be1e93470b66feab9fffcd2fb9510f49301ca5a773b5f6c91af3fa88b51c4`.

The sum of retained per-generation times is 935.509 seconds. It is a **lower
bound** on actual compute/wall time because work not durably recorded at the
environment transition is not reconstructed; it excludes model loading and
other setup. No paid inference charge occurred. A completed generation is
distinct from a well-formed or scientifically justified answer.

Primary admission and the predeclared format-only secondary analysis are kept
separate. The latter extracts one unambiguous explicit JSON label without JSON
repair or rationale-based guessing. It never rescues primary malformed outputs
or validates reasoning. Results are from the actual recorded model responses,
not inferred from baselines or smoke tests.

A separate, explicitly post-hoc development-only order diagnostic subsequently ran four calls on the two PG04 claims. Reversing only the enumeration of permitted categorical labels changed both extracted choices from `formally_established` to `refuted`, with the scientific record unchanged; all four remained schema-invalid. This is direct presentation sensitivity in two development examples, not an independent generalization finding. It does not establish a literal first-listed-label mechanism because the reversed first label was `disputed_or_unresolved`. Definitions retained original order, there was no full counterbalancing, and no further tuning or rounds followed. Raw calls and the protocol are retained separately from the primary60-call run in `results/v0.2.0/development_order_audit.json` and its linked artifacts.

### 5.3 Actual local subject interfaces

PCS, FoldBounds, and website experiments use separate capability-appropriate
protocols; their counts are not pooled. Existing checkouts are read-only: no
source edits, repository state changes, dependency installation, builds, or cache
generation occur in subject directories. Children execute fixed known interfaces
with timeouts, filtered environments, and outputs confined to SVB. These
precautions do not create a general sandbox for arbitrary submitted code.
No production endpoint, deployment, account database, paid model, or external
security probe is part of the experiments.

## 6. Completed results

### 6.1 Baseline distinctions

The following are recorded in `results/v0.2.0/baselines.json`, against provisional
author references.

| Policy | Exact category correct / all | Answered coverage | Category correct / answered | Coarse decision correct / all | False acceptance / nonaccept references | Both-correct pairs |
|---|---:|---:|---:|---:|---:|---:|
| Weak lexical evidence-aware policy | 13/24 | 24/24 | 13/24 | 17/24 | 6/12 | 4/12 |
| Bounded numerical parser | 3/24 | 4/24 | 3/4 | 4/24 | 0/12 | 0/12 |

The numerical parser's four accepted answers all correspond to provisionally
supported narrow claims. Three match the exact support category and one uses
computational support where the reference uses empirical support. Its coarse
decision agreement is therefore 4/24, not 3/24, while it leaves 20 tasks
unsupported. Zero false acceptance is consistent with this narrow coverage and
does not establish general scientific caution or adequacy assessment. The parser
does not correctly identify any insufficiency case because it declines them as
outside its capability.

The lexical policy accepts 18 items. Of the six false acceptances, three are
insufficient-evidence targets and three are refuted targets. It also labels four
computational positives empirically supported, explaining part of the difference
between 13 exact categories and 17 coarse decisions. Five of eight
insufficiency cases receive the appropriate label. Neither policy has an
automatically established reasoning-quality score; the retained field is null
and human-adjudicated reasoning count is zero.

The reported mean Brier losses are 11/12 for the lexical policy and 1/2 on the
numerical parser's four answered items. Their different coverage and deterministic
one-hot construction preclude a deployment calibration interpretation. Mechanical
source-ID and exact-quote checks found no nonexistent IDs or mismatched quotes in
these baseline outputs; this does not demonstrate that their explanations entail
their conclusions.

These are diagnostic policies, not evidence about a broad class of conventional
scientific QA tools. In particular, the old hinted-scope policy's 21/22 Phase I
score is **not directly comparable**: it used different tasks, visible structured
missing-evidence cues, and a different category distribution. Phase II does not
claim an improvement or deterioration by subtracting those scores.

### 6.2 Model: completed generation, failed qualification

`results/v0.2.0/model_scores.json` retains all selected requests and strict
outcomes. All 60 outputs are malformed under the declared response contract;
strict admitted coverage is zero in every information condition.

| Information condition | Completed generations | Strict admitted responses | Unique explicit JSON labels extracted | Secondary exact-label agreement |
|---|---:|---:|---:|---:|
| Evidence | 24 | 0 | 24 | 0/24 |
| No evidence | 24 | 0 | 24 | 0/24 |
| Verified numbers | 4 | 0 | 4 | 0/4 |
| No assumptions annotation | 4 | 0 | 4 | 0/4 |
| Question paraphrase | 4 | 0 | 4 | 0/4 |

Every extracted label is `formally_established`, the first category listed in
the fixed instruction and a category unused by all 32 new source-grounded
references. The all-case primary contract success count is therefore 0/60, but
this must **not** be interpreted as a scientific reasoning accuracy estimate:
there is no admitted-answer denominator. Answered accuracy, admitted acceptance
risk, valid-vector Brier loss, and calibrated selective risk are undefined/null.
There are zero valid six-class confidence vectors. Some outputs report scalar
confidence; those values are not repaired into probability distributions. A
primary false-accept count of zero means no verdict passed admission, not that
the model was safe, cautious, or correct.

The predeclared secondary label extraction also gives zero agreement everywhere.
This is a diagnostic of the recorded label-collapse pattern, not a valid
replacement benchmark score or evidence that all underlying factual judgments
are independently known to be wrong. The unchanged label across evidence,
calculator, reminder-removal, and limited paraphrase conditions does not establish
a meaningful treatment effect. It prevents an affirmative H1–H4 conclusion from
this model run.

A separate **post-hoc descriptive raw-JSON audit**,
`results/v0.2.0/model_attribution_audit.json`, examines objects even when their
scientific response contract fails. Fifty-eight of 60 are parseable JSON objects:
23/24 evidence, 23/24 no-evidence, and 4/4 in each other condition. All 23
parseable no-evidence objects name at least one evidence ID absent from the
zero-document packet. This is **nonsupplied packet-ID attribution**, not a finding
that the model fabricated real papers, authors, or DOIs. The one capped output is
in the no-evidence condition; nonparseable outputs remain unassessable for this
full-object audit.

No invalid exact quotations were found in the parseable-object audit, but the
model generally supplied empty citation lists. Absence of a mismatched quote is
not evidence of supported reasoning. Exact quote presence would establish literal
consistency, not semantic entailment, scientific source quality, or sufficiency.
The internal selected-text audit in `model_failure_audit.md` identifies examples
of independently visible factual mistakes: describing 84 repeated plant
observations as 84 different plants, treating 23 enzyme readings as 23 independent
biological experiments, and asserting patient-outcome support in a no-document
condition. These examples were selected after observation and are not a new
preregistered or blinded-human reasoning-accuracy metric. That audit preserves
its explicit 46-response prefix boundary rather than pretending to audit every
completed response identically.

Competing explanations include the demanding schema, misunderstood categories,
first-position preference, generic answer reuse, and scientific reasoning errors.
The invariant first-listed label is observed; a causal label-order effect is not
established by the primary run. This is a negative qualification of **this small
checkpoint with this prompt/schema**, not a demonstration of weakness in general
scientific AI, PCS, FoldBounds, or all language models. Any post-hoc changed-order
or simplified-response diagnostic must be reported separately on development
data, with its timing and changed construct disclosed; it cannot replace the
unfavorable frozen experiment.

### 6.3 FoldBounds: enclosure can remain uninformative

The actual FoldBounds CLI matched independently enumerated finite-model
references on 27/27 controls. Six length-8–10 sequence/parameter families use
four baseline depths each, plus three advanced refinements. The independent
enumerator fixes the first edge east, retains reflections, and counts pairwise
contacts with exact rational weights. Enclosure, nested baseline refinement, and
full-depth equality hold for these sampled controls. No fresh Lean proof replay
or real-protein inference is established by this adapter.

A negative usefulness result survives successful correctness checks. For ten
all-H residues, q=2, event threshold 2, the independent exact partition is 13,323
and event probability is `9304/13323`. Baseline depths 2, 4, and 6 leave
probability width 1. At depth 4, advanced settings reduce the relative partition
width dramatically but leave almost all of the probability range unresolved:

| Setting | `(upper Z − lower Z)/exact Z` | Probability-interval width |
|---|---:|---:|
| Baseline depth 4 | 19,722.77955 | 1.00000000 |
| Matching, lookahead 0 | 6.32132 | 0.99975075 |
| Matching, lookahead 2 | 5.87668 | 0.99621291 |
| Matching plus memory-4 terminal transfer | 2.24889 | 0.99901825 |
| Baseline full depth 10 | 0 | 0 |

Relative partition width is not relative error of a point estimate. Different
refinements are not assumed totally ordered in probability tightness. Single
full-depth CLI times for all-H lengths 8, 9, 10 were approximately 0.076, 0.095,
and 0.138 seconds, including interpreter/scheduler effects without repetitions.
These are descriptive small-size observations, not asymptotic scaling or
efficiency claims.

### 6.4 PCS and website trust boundaries

| Subject | Observed | Eligible | Reference matches | Unsupported |
|---|---:|---:|---:|---:|
| FoldBounds | 27 | 27 | 27 | 0 |
| PCS | 8 | 6 | 6 | 2 |
| Website DOM | 8 | 8 | 8 | 0 |

PCS received fresh signed packages for three independently balanced reactions
and atom-unbalanced variants, all carrying producer PASS claims. Independent
atom tables and third-party signature/file-hash checks precede the actual
compiled Lean authority. It accepted the balanced cases and returned
`REJECT:replay` for all three properly signed false predicates. Two broader
interfaces—real biological empirical safety and unrestricted free-form scientific
truth—remain unsupported. Those observations are not counted as false rejections,
successes, or system bugs. Atom conservation does not prove reaction feasibility,
kinetics, or biological safety.

The website experiment used real headless Chromium and actual page JavaScript
for four workflows at widths 390 and 1280: overlap, disjointness, invalid-input
invalidation, and a forged imported receipt. It retained visible browser-only and
unknown-scientific-adequacy scope language. Invalid CSV hid a prior result; an
imported receipt asserting a false Lean result did not become live confirmation,
and a fresh file check produced the real overlap. The eight observations are
repeated workflow controls, not independent usability or comprehension studies.
There were no production or mutating requests.

Initial SVB construction failures remain in a separate artifact: PCS packages
first used a noncanonical assessment reason and failed before authority
execution, while the first browser profile path exceeded a Unix socket path
limit. Repairs were confined to SVB's producer and temporary paths. These
construction errors were not counted as scientific rejections, and subject code,
frozen references, and assertions were unchanged. The preserved Phase I
reference-error history is also not erased by the Phase II successes.

## 7. Human qualification and threats to validity

### Human evidence remains absent

Thirty-two public-field reference-review packets and a tested packet generator
have been prepared. The prospective protocol requires two independent domain
scientists plus a statistical reviewer, first-round records before discussion,
pinpoint evidence, separately judged assumptions and inference, and preserved
disagreements. It distinguishes candidate/model-identity blinding from hiding
provisional reference answers. Scientific source identity ordinarily remains
visible because provenance is part of the construct. A generator cannot certify
absence of implicit identity cues or prior reviewer exposure.

No reviewers were contacted, recruited, or recorded as having rated these tasks.
Human review count and reasoning-adjudication count are zero. No agreement
statistic, expert-certified accuracy, or reference consensus is claimed. Where
experts disagree, the protocol permits unresolved/unscored cases or versioned
revision rather than forced majority gold.

### Reference validity and empirical grounding

Exact arithmetic and source hashes are narrower than source authenticity,
measurement validity, independent replication, or empirical adequacy. Puromycin
and CO2 are secondary historical transcriptions without original full methods;
FreeSolv combines experimental and calculated records with documented default
uncertainties and licensing/provenance caveats. Naturalistic snippets were authored
from these records and may simplify what expert readers need. The empirically
supported category must therefore remain explicitly source- and scope-relative.

### Leakage, sampling, and external validity

There is no protected holdout in this shared workspace. Public family/source
separation reduces direct cross-split reuse but cannot prove model training
nonexposure or prevent an investigator inspecting labels. The strongest current
alternative is an honest public freeze with exposure logs, immutable prompt and
code identities, no answer-driven retries, and preserved deviations. An external
custodian and access controls would be needed for a genuine unseen-label claim;
committing an opaque “secret” file would not provide that protection.

The dataset has three evaluation source families and paired dependent claims.
It is not population-representative or powered for broad superiority. The
assistance/paraphrase subset is especially small and source-restricted. Repeated
probability, source, or viewport controls do not increase the number of independent
scientific studies. A single small Qwen checkpoint with zero admitted responses
cannot characterize scientific LLMs generally. H1–H3 remain exploratory without
an affirmative scientific conclusion; H4 remains unestablished.

### Measurement boundaries

Strict-format failure and scientific judgment failure must be separated without
discarding either. A secondary extractable label cannot establish a valid
probability vector, correct reasoning, or faithful evidence use. Source-ID and
quote membership are syntax checks, not entailment or fabrication detection in
general. Scope preservation in a formal calculus requires sound premises and
rules; no theorem makes natural-language evidence declarations authentic.

## 8. Discussion and next research steps

Phase II advances practical measurability: it removes direct reference/checker
cues from policy inputs, adds source-grounded paired claims and empirical-record
categories, runs harder actual-system controls, and preserves coverage and failure
denominators. The shallow FoldBounds result is a useful concrete reminder that
certified correctness and informativeness are distinct. PCS and website successes
show selected local boundaries, not universal scientific truth or security.

The deterministic policies demonstrate how coarse acceptance, category labels,
and interface coverage can disagree. They do not demonstrate a new state of the
art or a previously unknown scientific reasoning failure. The targeted literature
review shows extensive relevant precedent. No mathematical novelty, general
empirical reliability, biological discovery, or broad evidence-dependency utility
has been established.

The three highest-value next steps are:

1. **Qualify references externally.** Staff the declared domain/statistical panel,
   audit the primary evidence and licensing, retain disagreements, and replace
   provisional labels only through versioned records. Prioritize empirical
   uncertainty and study-design claims over generating more easy arithmetic.
2. **Qualify and independently replicate actual-model evaluation.** Preserve the
   completed unfavorable run, strict admission, secondary label diagnostics,
   failures, and exposure logs. Qualify a simpler response contract on development
   data and test competent additional systems under a new prospective externally
   custodied source-family-disjoint protocol. Human reasoning and attribution
   review is needed before interpreting label agreement as scientific competence.
3. **Expand scientific references and comparison design.** Add independently
   characterized experimental systems and more source families, stable numerical
   baselines and correlated uncertainty controls. Compare against the closest
   evidence-aware literature methods, and extend formalization only where it can
   correspond to a tested implementation rather than increase architectural
   complexity.

## 9. Reproducibility statement

The version-0.1 frozen tasks, implementation identities, and results remain
unchanged. Phase II is additive. The core/reference code is standard-library
Python; optional local model and system prerequisites are documented separately.
From the independent project root:

```sh
export PYTHONPATH="$PWD/src"
export PYTHONDONTWRITEBYTECODE=1
python3 -B -m svb.cli validate
python3 -B -m svb.phase2 validate
python3 -B -m unittest discover -s tests -v
python3 -B -m svb.phase2_references
python3 -B -m svb.phase2 baselines --output results/local/phase2-baselines-repeat.json
```

Do not rerun authoring or freezing scripts during evaluation. Retained
measurements are `results/v0.2.0/reference_checks.json`, `baselines.json`,
`systems.json`, `model_scores.json`, and `model_attribution_audit.json`; raw
construction failures and detailed local observations remain separate. The final
test suite passed 105 tests; the earlier hosted CI run passed the then-current
103 tests and must not be described as having run the later additions. The
protocol, sources, data, prompts, scorer, numerical references, and runner were
content-hashed before the scored scientific model run. The model and prompt
bundle have recorded revisions/hashes; those identities do not prove label
correctness or absence of training exposure.

The complete primary model artifact is
`results/v0.2.0/models/qwen_scientific_complete.jsonl`, with combined run metadata
in `qwen_scientific_complete.run.json` and the separate interruption ledger.
For data-only scoring replay:

```sh
python3 -B scripts/analyze_phase2.py \
  results/v0.2.0/models/qwen_scientific_complete.jsonl \
  --output results/local/phase2-model-scores-repeat.json
```

`docs/phase-ii/reproduce.md` describes fresh inference, optional subject
reproduction, and review-packet generation. Replaying records reproduces scoring,
not fresh inference. Wall times, browser profiles, and temporary paths need not
be bit-identical. No publication, deployment, paid API usage, or change to PCS,
FoldBounds, or their website is implied by these commands or this draft.

## References

1. Wadden, D., et al. *Fact or Fiction: Verifying Scientific Claims*. EMNLP,
   2020. [10.18653/v1/2020.emnlp-main.609](https://doi.org/10.18653/v1/2020.emnlp-main.609).
2. Thorne, J., et al. *FEVER: a large-scale dataset for Fact Extraction and
   VERification*. NAACL, 2018. [10.18653/v1/N18-1074](https://doi.org/10.18653/v1/N18-1074).
3. Wang, X., et al. *SciBench: Evaluating College-Level Scientific
   Problem-Solving Abilities of Large Language Models*.
   [arXiv:2307.10635](https://arxiv.org/abs/2307.10635), inspected v3.
4. Chen, Z., et al. *ScienceAgentBench: Toward Rigorous Assessment of Language
   Agents for Data-Driven Scientific Discovery*.
   [arXiv:2410.05080](https://arxiv.org/abs/2410.05080), inspected v3.
5. Wadden, D., et al. *SciRIFF: A Resource to Enhance Language Model
   Instruction-Following over Scientific Literature*.
   [arXiv:2406.07835](https://arxiv.org/abs/2406.07835), inspected v4.
6. Skarlinski, M. D., et al. *Language agents achieve superhuman synthesis of
   scientific knowledge*. [arXiv:2409.13740](https://arxiv.org/abs/2409.13740),
   inspected v2. The title is the authors' claim, not an SVB finding.
7. Asai, A., et al. *OpenScholar: Synthesizing Scientific Literature with
   Retrieval-augmented LMs*. [arXiv:2411.14199](https://arxiv.org/abs/2411.14199),
   inspected v1.
8. Gao, T., et al. *Enabling Large Language Models to Generate Text with
   Citations*. EMNLP, 2023.
   [10.18653/v1/2023.emnlp-main.398](https://doi.org/10.18653/v1/2023.emnlp-main.398).
9. Geifman, Y., & El-Yaniv, R. *Selective Classification for Deep Neural
   Networks*. [arXiv:1705.08500](https://arxiv.org/abs/1705.08500), 2017.
10. Guo, C., et al. *On Calibration of Modern Neural Networks*. ICML, 2017.
    [PMLR 70:1321–1330](https://proceedings.mlr.press/v70/guo17a.html).
11. Gorman, K. B., Williams, T. D., & Fraser, W. R. *Ecological Sexual Dimorphism
    and Environmental Variability within a Community of Antarctic Penguins
    (Genus Pygoscelis)*. PLOS ONE, 2014.
    [10.1371/journal.pone.0090081](https://doi.org/10.1371/journal.pone.0090081).

Exact scientific-data identities, original references, redistribution terms,
transformations, and source limitations are recorded in
`data/v0.2.0/registry.json`. The reviewed full-text literature is documented in
`references/phase2_registry.json`; no systematic novelty search is claimed.
