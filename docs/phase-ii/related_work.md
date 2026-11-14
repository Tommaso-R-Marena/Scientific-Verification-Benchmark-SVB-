# Phase II targeted literature review: evidence, uncertainty, and scientific scope

## Review scope and evidence level

This follow-up goes beyond Phase I's bibliographic/abstract inspection. On
**2026-11-14 UTC**, we retrieved the full text of ten selected papers and read
their relevant construction, evaluation, annotation, contamination, and
limitations sections. The selection was purposive: sources were chosen to
challenge the intended SVB construct and human-review design. This is **not a
systematic review**, not a line-by-line reading of every paper, and not evidence
of novelty or benchmark superiority. We did not reproduce these papers' model
experiments or independently audit their human ratings.

[`references/phase2_registry.json`](../../references/phase2_registry.json)
records exact URLs, HTTP status, retrieval date, response-byte SHA-256, inspected
sections, version context, license evidence, and limitations for each source.
Four articles were inspected as arXiv HTML; six as PDF text, including ACL and
PMLR copies. All ten full-text retrievals succeeded with TLS verification enabled.
Additional publisher/Anthology pages were inspected for licensing. Raw full text
is retained only in this project's ignored local cache, not redistributed in Git.
An accessible arXiv paper with a perpetual non-exclusive distribution license is
**not** presumed to have a permissive reuse license. An article's license does not
establish rights to its underlying benchmark, publisher papers, or textbook
questions. No source benchmark's items or answer keys were imported by this
review.

The observations below are our paraphrases of the inspected methods. Reported
sample sizes and review procedures are claims in those papers, not newly
replicated SVB measurements. The selected revisions include SciBench v3 (2024),
ScienceAgentBench v3 (2025), SciRIFF v4 (2025), PaperQA2 v2 (2024), and OpenScholar
v1 (2024); do not silently apply these descriptions to earlier releases.

## 1. Claim verification and evidence relations

### SciFact: scientific textual support is narrower than scientific truth

Wadden et al., *Fact or Fiction: Verifying Scientific Claims* (2020),
[ACL paper](https://aclanthology.org/2020.emnlp-main.609/),
[arXiv:2004.14974](https://arxiv.org/abs/2004.14974), defines SUPPORTS, REFUTES,
and NO INFO for **individual claim–abstract pairs**, with minimal rationale
sentences. This is a crucial construct distinction: the paper explicitly says
assigning a global scientific truth label requires systematic expert review and
focuses on the simpler evidence-relation problem. A claim can in principle have
supporting and refuting abstracts, although that conflict did not occur in their
curated dataset. Therefore a NO INFO result is not a proof of falsity or proof
that no evidence exists elsewhere.

The source describes 1,409 claims and 5,183 abstracts. Claims derive from citation
sentences, with expert-created negations to obtain refutations. Claim writers
cannot see the cited abstract when writing; verifiers judge claims they did not
write. The annotator pool includes scientific NLP experts and life-science
undergraduates/graduates, rather than a uniformly external scientific panel.
Independent reannotation of 232 pairs gives reported label Cohen's κ=0.75 and
sentence-rationale κ=0.71 (§3.3). These quality measurements are useful evidence
about annotation consistency, not an experimental validation of every claim.

**Implication for SVB:** record both evidence entailment and whether a stronger
empirical interpretation is justified. Retain conflicts and missing evidence;
do not advertise that distinction as novel. Reference-rationale provenance and
independent reannotation are prerequisites to a stronger SVB qualification claim.

### FEVER: evidence retrieval and label accuracy answer different questions

Thorne et al., *FEVER: a large-scale dataset for Fact Extraction and VERification*
(2018), [ACL paper](https://aclanthology.org/N18-1074/),
[arXiv:1803.05355](https://arxiv.org/abs/1803.05355), uses generated/mutated
Wikipedia-derived claims with SUPPORTED, REFUTED, and NOT ENOUGH INFO labels.
Evidence sentence selection is part of evaluation for supported/refuted claims;
label-only correctness can be substantially different. Section 3 documents the
annotation team, five-rater sample agreement, super-annotator checks, and an
author audit. Those are specific quality-control procedures, not equivalent to
independent review of a scientific study's statistical and physical adequacy.

Its public encyclopedic corpus and synthetic claim modifications are possible
exposure and artifact channels. A later model's benchmark contamination cannot
be inferred absent merely because an original paper provided train/test splits.

**Implication for SVB:** evaluate evidence locators and faithfulness separately
from verdict matching. Include unsupported/missing-evidence controls without
assuming every unsuccessful retrieval proves insufficiency of the actual
scientific literature. Use family grouping to keep all semantic mutations of a
claim in one split.

## 2. Scientific calculations, code, and literature instructions

### SciBench: specified scientific problem solving

Wang et al., *SciBench: Evaluating College-Level Scientific Problem-Solving
Abilities of Large Language Models*, [arXiv:2307.10635](https://arxiv.org/abs/2307.10635),
constructs college textbook and course-exam questions with numeric answers,
units, LaTeX expressions, and worked solutions. The inspected dataset section
explains manual extraction/verification and its preference for numerical
free-response items to permit standardized assessment. The ethical statement
discusses textbook fair-use rationale and instructor permissions; these statements
do not give SVB a blanket license to redistribute the questions.

The closed exam subset and manual extraction are described as exposure
mitigations. Manual PDF extraction cannot by itself prove that the meaning of a
question was absent from model training. Textbook numerical correctness also
does not adjudicate a real study's model adequacy, causal inference, or empirical
support.

**Implication for SVB:** scientific calculation is an important baseline construct
with extensive prior work. Naturalistic evidence assessment needs a different
reference protocol rather than simply adding scientific vocabulary to exact
arithmetic tasks. Distinguish correct numerical answer from correct scientific
scope and preserve their separate denominators.

### ScienceAgentBench: authenticity and expert validation of executable tasks

Chen et al., *ScienceAgentBench: Toward Rigorous Assessment of Language Agents for
Data-Driven Scientific Discovery*, [arXiv:2410.05080](https://arxiv.org/abs/2410.05080),
reports 102 tasks adapted from 44 peer-reviewed publications across four
disciplines. The output is a self-contained Python program; success criteria
inspect results, and rubrics permit partial assessment. Section 2.2 describes
nine domain experts examining realism, instructions, needed knowledge, and
rubrics, followed by independent annotator execution of tasks they did not
compose. This is materially stronger external domain involvement than SVB has
currently achieved. SVB must not claim equivalent expert validation because an
AI agent inspected its task files.

The paper directly identifies shortcuts from public reference programs and
exposed test labels. It removes selected test examples where possible, re-splits
modeling datasets, and substitutes dummy test labels to prevent direct reporting.
These are concrete mitigations, not a demonstration that all pretraining
contamination is absent. Its §4.2 human evaluation uses two evaluators and hides
program execution/success outcomes. The discussion notes that a rubric derived
from one reference implementation can undervalue a scientifically equivalent
alternative. Hiding success is different from hiding candidate model identity or
withholding reference implementation details.

**Implication for SVB:** source code success, code rubric compliance, and scientific
conclusion adequacy are separate constructs. Reviewers should assess permitted
alternative methods rather than treat a reference program's stylistic choices as
scientific requirements. SVB's reviewed packets should distinguish identity
blinding from anchoring on provisional gold.

### SciRIFF: task-held-out instruction following with attribution

Wadden et al., *SciRIFF: A Resource to Enhance Language Model Instruction-Following
over Scientific Literature*, [arXiv:2406.07835](https://arxiv.org/abs/2406.07835),
standardizes 54 scientific literature tasks in the inspected v4. These include
extraction, QA, classification, summarization, and entailment; some structured
outputs pair answers with attribution. Paper authors with scientific NLP
experience write task templates/schemas over existing human-annotated resources.
That is not a new independent domain-expert adjudication of every inherited
scientific claim.

The evaluation withholds nine task types. Section 3.2 identifies and removes
7.5K overlapping scientific examples from Tülu V2 Mix for controlled experiments.
The evaluation table explicitly separates verdict and evidence scores for SciFact,
and answer and attribution for Qasper. Some long-form evaluations use an LLM
judge; this creates an additional measurement uncertainty rather than a trusted
scientific authority. Task-held-out evaluation and removal of known training
overlap do not establish source-lineage disjointness or absence of unknown
base-model exposure.

**Implication for SVB:** publicly supplied JSON can support useful interfaces,
but schema-following and declared missing-evidence gates remain different from
discovering absent premises in natural scientific text. Phase II should document
which distinction it measures, log source exposure, and avoid claiming a generic
new evidence-aware benchmark architecture.

## 3. Retrieval, literature synthesis, and attribution

### PaperQA2 and LitQA2 are not ScholarQABench

Skarlinski et al., *Language agents achieve superhuman synthesis of scientific
knowledge*, [arXiv:2409.13740](https://arxiv.org/abs/2409.13740), describes
PaperQA2 and **LitQA2**, among other tasks. The title is the authors' framing,
not an SVB endorsement of general scientific superiority. LitQA2 asks
multiple-choice questions requiring main-text reasoning rather than title/abstract
lookup and permits insufficient-information responses. Methods §8.2 describes
author/contractor question construction, specialist human evaluation, compensation,
consent, and model-based answer-letter extraction. Prior LLM checks helped find
questions or distractors that were too easy; this is a disclosed model-informed
construction decision, not model-independent case selection.

A particularly relevant negative finding is that some initially public LitQA2
questions became Google-indexed via data aggregators, contaminating a later human
comparison. The authors excluded affected answers from that comparison. This
does not establish contamination of every model run, but it shows why public
benchmark answers can undermine a claimed prospective comparison even when
researchers intended a fresh round. Performance and exclusion decisions are not
independently replicated here.

**Implication for SVB:** versioned exposure histories and preserved exclusions
are essential. A public source/family-disjoint freeze is useful, but cannot be
called protected holdout. Selecting cases after trying a model needs disclosure
and cannot later be described as a pristine blind comparison.

### OpenScholar and ScholarQABench: long-form synthesis with expert rubrics

Asai et al., *OpenScholar: Synthesizing Scientific Literature with
Retrieval-augmented LMs*, [arXiv:2411.14199](https://arxiv.org/abs/2411.14199),
introduces **ScholarQABench**. It combines adapted single-paper tasks with
expert-written multi-paper literature questions and reference/rubric data.
Its table distinguishes question-only collections from those with long-form
references; the overall question count must not be equated with expert-verified
full answers. For the adapted single-paper SciFact and PubMedQA subsets, the
paper removes uncertain cases and uses binary open retrieval. That construct
differs from the original three-way evidence-verdict tasks and from SVB's aim of
preserving insufficiency as a meaningful outcome.

Sections 3 and 5 describe domain expert writers, independent rubric contributors,
and a 16-person human panel, with one to three raters per instance in the human
assessment. Experts do not assess their own questions. The limitations explicitly
acknowledge that usefulness/preference raters may focus on writing and coverage,
while detailed citation correctness and factuality are separate. Breadth,
helpfulness, factual entailment, and empirical evidence adequacy should not be
silently equated.

**Implication for SVB:** do not mix model identity masking, source credibility,
factual correctness, and preference ratings. Explicit limitations of the human
rubric are as important as high aggregate agreement. SVB currently has none of
this paper's external human-review evidence and must say so.

### ALCE: correct answers and good citations can come apart

Gao et al., *Enabling Large Language Models to Generate Text with Citations*
(2023), [ACL paper](https://aclanthology.org/2023.emnlp-main.398/),
[arXiv:2305.14627](https://arxiv.org/abs/2305.14627), evaluates long-form answers
over ASQA, QAMPARI and ELI5 with retrieval corpora and separates fluency,
correctness, and citation quality. Citation recall asks whether cited passages
support a statement; citation precision penalizes irrelevant citations. Automatic
NLI-based support scores are model judgments, not proof that a cited study is
true or physically applicable.

Section 3.4 identifies passage-copying shortcuts that can obtain nearly perfect
citation scores while failing fluency or answer coverage. Its construction also
uses public QA resources; no supplied citation-supervision training set does not
mean no model pretraining exposure.

**Implication for SVB:** include citation mismatch, omitted contradictory evidence,
unsupported scope, and irrelevant-but-real citation controls. Show multiple
components instead of inventing a weighted “scientific truth” score. Textual
entailment can justify attribution while leaving statistical quality or empirical
generalization unresolved.

## 4. Abstention, calibration, and scope of guarantees

Geifman and El-Yaniv, *Selective Classification for Deep Neural Networks*
(2017), [arXiv:1705.08500](https://arxiv.org/abs/1705.08500), defines a selection
function and reports risk conditioned on the accepted probability mass together
with coverage. Its formal setup assumes samples drawn iid from an underlying
distribution. A zero-coverage policy does not establish zero scientific error;
the conditional risk denominator vanishes. An authored public purposive set does
not satisfy the sampling and exposure premises needed to import a risk-control
guarantee.

Guo et al., *On Calibration of Modern Neural Networks* (2017),
[PMLR paper](https://proceedings.mlr.press/v70/guo17a.html),
[arXiv:1706.04599](https://arxiv.org/abs/1706.04599), distinguishes confidence
calibration from classification accuracy and fits post-hoc calibration on held-out
validation data under explicit same-distribution assumptions. ECE summarizes
confidence–accuracy discrepancy through bins. Binning choices, finite sample
size, shift, and conditioning on answers matter. A score or calibration method
does not turn a mistaken scientific reference label into truth.

**Implication for SVB:** meaningful probabilistic scoring needs genuine probability
outputs and enough independently adjudicated cases. One-hot hand-coded policies
cannot support a useful confidence-ranking or smooth risk-coverage claim. A
natural-language “confidence” field must not be treated as calibrated numerical
probability without an operational mapping and held-out assessment. Keep
insufficient evidence, unsupported capability, execution error, and refusal
distinct; they have different scientific meanings and denominators.

## 5. Cross-paper construct comparison

| Construct | Existing concrete precedent | What it establishes | Additional SVB evidence still needed |
|---|---|---|---|
| Claim/evidence verdict with rationales | SciFact; FEVER | Whether a fixed corpus passage supports/refutes a claim under an annotation protocol | Independent statistical/model-adequacy review of stronger scientific interpretations |
| Numerical scientific reasoning | SciBench | Answer correctness in a specified problem | Uncertainty/model discrepancy and real source-study applicability |
| Executable scientific workflow | ScienceAgentBench | Program/result success plus graded reference-informed rubrics | Claim-to-conclusion evidence sufficiency with legitimate alternative methods |
| Structured scientific instructions with attribution | SciRIFF | Task-following and inherited answer/evidence metrics | Naturalistic premise discovery and source-lineage exposure accounting |
| Literature question answering/synthesis | PaperQA2/LitQA2; OpenScholar/ScholarQABench | Reference/rubric-informed answers, evidence retrieval, usefulness and/or citation measures | Claim-level empirical validity with uncertainty and conflicts preserved |
| Evidence attribution quality | ALCE; ScholarQABench | Whether cited text supports output and whether citations are relevant | Whether the underlying experiment or model supports the real-world conclusion |
| Abstention/calibration | Selective classification; calibration work | Coverage-conditioned error or confidence agreement under stated assumptions | Reliable scientific labels, adequate sample design, and genuine probability outputs |

All of these precedents challenge a novelty claim based merely on combining
scientific text, citations, uncertainty, exact calculations, and multiple metrics.
The potentially useful SVB contribution is a transparent *operational integration*
that keeps evidence scope and unknowns visible across these constructs. It is
currently an engineering/research hypothesis, not a proven novel method.

## 6. Human review and exposure consequences for Phase II

The complete prospective protocol is
[`human_adjudication.md`](human_adjudication.md). It requires two independent
domain scientists plus a statistical reviewer, first-round records before
discussion, separate scientific-source visibility and candidate-identity masking,
and no forced consensus gold. No experts were contacted or reviews performed as
part of writing this literature assessment.

The shared workspace cannot provide a genuine protected holdout. The strongest
honest present alternative is a public frozen split disjoint in **study/source
lineage and task family**, with explicit model-exposure and deviation logs. Source
material must be visible when provenance is part of the question; a model's
developer may nevertheless have seen it during training or benchmark design.
Exposure is unknown unless supported by evidence, not automatically absent.
No “secret” answer file should be committed or treated as secret merely because
its name is opaque. Later genuinely blind evidence needs an external custodian
and access control, not a second directory in this checkout.

## 7. Novelty status and next literature work

**Established:** evidence-linked verdicts, uncertainty/abstention, program-result
checks, scientific datasets, human rubrics, attribution metrics, calibration,
versioning, and contamination controls all have substantial precedent.

**Useful combination, not established novelty:** exact independent references plus
explicit typed-scope distinctions, data-only submissions, visible reference-error
history, and noninvasive capability-specific adapters.

**Unvalidated hypothesis:** a well-adjudicated naturalistic claim/evidence
benchmark could reveal scientifically important scope escalations that a
particular existing answer-only metric misses. To establish that, SVB needs
independent human judgments, competent actual systems, prespecified contrasts,
source/family separation, adequate sample design, and comparison to the closest
evidence-aware alternatives. Hand-designed computation-only policies cannot
prove this claim.

Unreviewed areas remain, including formal assurance cases and scientific evidence
calculi, recent post-2025 agent benchmarks, conformal risk control, causal
identification and model validation standards, and detailed field-specific
biochemical reference practices. A broader reproducible search, full reference
audits, and external expert criticism are prerequisites to a publication novelty
statement. Nothing here establishes general scientific AI reliability or an
empirically validated biological discovery.
