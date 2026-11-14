# Phase IIb methodology audit: separate decisions, justifications, and contracts

**Status:** prospective method audit and interpretation limits. This document does
not supply new reference labels, revise historical results, or certify an actual
model's reasoning. Existing data, protocols, raw responses, sources, and subject
repositories remain unchanged. Human scientific review has not occurred.

## 1. The confound being addressed

The earlier 60-response small-model experiment completed generation but admitted
no outputs under the full six-class probability/scope/citation contract. That is a
negative **model–prompt–schema qualification** result. It cannot by itself
measure accuracy of scientific classification, scientific reasoning, or evidence
use. Extracting an explicit label from invalid output is a useful secondary
observation but does not repair the primary contract or validate its explanation.

Phase IIb separates three requested products:

| Task | Requested observable | Primary construct | What a successful output does not establish |
|---|---|---|---|
| **A: minimal verdict** | Exactly one of the six category strings, under a fixed documented trimming/admission rule | Scientific category decision conditional on the supplied evidence, with format burden reduced | Correct rationale, evidence attribution, confidence calibration, empirical truth beyond the source, or the model's internal reasoning process |
| **B: brief justification and attribution** | A concise externally assessable explanation with identifiable supplied evidence; prose may be allowed | Whether the stated inference and evidence use justify the target at the declared scope | Faithfulness to internal computation, absence of unseen bias, or correctness merely because the prose is plausible |
| **C: full verification response** | The original structured category/scope/probability/evidence/citation contract | Interface interoperability and strict verification protocol compliance, alongside admitted scientific decisions | Scientific competence from syntax alone; scientific incompetence from schema failure alone |

Report all three with their own observed and eligible denominators. A case whose
scientific target is outside a numerical tool's scope is not equivalent to an
incorrect accepting answer. Do not collapse unsupported capability, withheld
evidence, incomplete generation, invalid syntax, and a false scientific
conclusion into a single failure explanation.

## 2. Construct map and discriminating controls

| Construct | Control/contrast | Recorded outcome | Main confounds and limits |
|---|---|---|---|
| Basic instruction following | Non-scientific format/access controls fixed before scored runs; exact six-label vocabulary for A | Completion, exact admissibility, label/token leakage, output-limit hits | Success on a toy control is not scientific qualification; controls must not reveal test answers. |
| Category interpretation | Balanced examples on development data only; category-order counterbalancing; independent review of category ambiguity | Per-class confusion, order sensitivity, alternate admissible categories proposed by experts | Order changes are new conditions. A first-category pattern alone does not identify a causal order bias. |
| Evidence uptake | Same claim with full versus withheld documents, each with a separately fixed reference appropriate to its evidence envelope | Condition-specific verdicts, unsupported citations, supplied-evidence references | Removing data changes what is justified; do not score against the inaccessible full-information answer. Correct recall is not supplied-evidence use. |
| Scope discrimination | Narrow/stronger paired targets sharing scientific evidence; no role or missing-bridge metadata in model input | Both-correct pairs, acceptance of unsupported stronger targets, narrow-fact correctness | Related pairs are dependent; lexical strength cues can substitute for scientific appraisal. |
| Numerical correctness | Independently reproduced exact or tolerance-justified calculations; displayed calculator facts isolated from scientific labels | Calculation agreement, numerical error, judgment changes after assistance | Correct numbers do not establish design validity, statistical uncertainty, model adequacy, or empirical applicability. |
| Stated inferential quality | Blind human review of B against the supplied source, with reproducible calculations and countermodels | Criterion-specific reasoning judgments, source entailment, missing assumptions, unresolved cases | Good prose may be post-hoc. Reviewers can be anchored by verdicts, reputation, or earlier public labels. No internal chain-of-thought faithfulness is inferred. |
| Literal attribution | Evidence IDs and exact quoted substrings checked independently from B semantics | Nonsupplied IDs, altered quotes, absent citations | A valid ID or quotation can be irrelevant, contradicted, or scientifically weak; an unknown packet ID does not necessarily name a fabricated real paper. |
| Schema fidelity | A unconstrained versus A constrained to the same six labels; C separately assessed | Syntax/contract success and scientific agreement on *all* selected cases | Constrained decoding can force a legal category while shifting choices; compliance is not comprehension. C differs in task demand and cannot be treated as an identical task. |
| Robustness | Prespecified question paraphrase, row permutation, equivalent units, and genuinely different evidence controls | Outcome invariance where expected; appropriate changes when scientific meaning changes | Paraphrasing only the question is a limited perturbation. Do not expect invariance to changing units without conversion or removing causal assumptions. |
| Empirical adequacy | Independent domain/statistical review of source design, measurements, provenance, and target scope | Qualified, ambiguous, disputed, revised, or unscored reference dispositions | Recalculated tables, a formal certificate, two agreeing models, or reviewer consensus do not replicate the original experiment. |

These controls probe failure modes rather than decompose cognition into
independent latent factors. No individual contrast fully isolates a mental
mechanism. Document the residual confounds instead of assigning a causal name to
every observed score difference.

## 3. Unconstrained and constrained A are distinct treatments

Keep model revision, source packet, category meaning, decoding settings, input
budget, and task selection fixed where feasible. Log the exact grammar/token
constraint, label order, allowable whitespace, stopping rule, tokenizer, and
whether a label is selected through generation or candidate likelihood. Those
methods are not interchangeable. In particular, taking the maximum likelihood
of six category strings is a classifier experiment, not free-response compliance.

For each A treatment report:

- all scheduled requests, completed generations, missing/timeouts/errors,
  admissible outputs and coverage;
- exact-category agreement, coarse accepting/nonaccepting decisions, correct
  insufficiency, per-class confusion, and pair outcomes using explicitly named
  reference sets;
- labels and scientific outcomes on the *same* cases, with syntax-invalid
  unconstrained answers retained, never silently discarded;
- costs, output-limit/input-limit events, and conditioning/exposure differences.

Perfect constrained syntax may demonstrate the constraint worked. If category
agreement improves, the result is conditional on that decoding treatment and the
provisional reference; it does not prove scientific reasoning improved. If raw
unconstrained answers are nonconforming, a format-only extraction stays a
separate analysis. Do not introduce a fallback, repair, extra examples, or changed
grammar after examining evaluation failures and call it the same frozen run.

Category-order and simple-response diagnostics prompted by earlier failures are
post-hoc development investigations unless registered for a new evaluation.
Their results must not overwrite the older unfavorable run. Historical Phase II
cases are now exposed development/audit material, not fresh held-out tests.

## 4. B evaluates a public justification, not private internal reasoning

A reviewer should be able to inspect B's claims, calculations, references, and
limits independently. The appropriate request is a concise scientific
justification, not disclosure of hidden private reasoning. Grade whether the
*stated* reasoning is valid and sufficient for the proposed conclusion. Keep
distinct:

1. correctness of the final scientific category;
2. factual/arithmetical accuracy of the explanation;
3. whether the cited source actually entails the statement;
4. whether the inference stays within the source's design/model scope;
5. whether uncertainty and competing explanations are handled;
6. whether any explanation is faithful to the model's internal causal process.

The first five admit externally checkable observations; the sixth is not
established by plausible text or human agreement. A correct verdict with an
invalid explanation is not full verification. An incorrect verdict can accompany
a correct calculation followed by an invalid scope transition. B must be graded
separately from A, with the human panel's disagreement retained.

If B is generated after, or conditioned on, a model's A answer, report that
conditioning because it can anchor/rationalize the explanation. If B is a
separate call, it may disagree with A; retain the disagreement rather than
editing either answer. A-versus-B accuracy is not a controlled test of the benefit
of reasoning unless the full experimental design supports that interpretation.

## 5. Literature bearing on interpretation

Phase II's ten-source selected-full-text review remains unchanged in
`docs/phase-ii/related_work.md` and `references/phase2_registry.json`. In
particular, SciFact/FEVER already separate evidence relations from verdicts,
ALCE separates attribution from answer correctness, ScienceAgentBench documents
reference-rubric limitations, and OpenScholar distinguishes usefulness from
factual/citation accuracy. These are prior foundations, not new SVB discoveries.

Two additional targeted full-text inspections address explanation faithfulness:

- **Turpin et al., *Language Models Don't Always Say What They Think: Unfaithful
  Explanations in Chain-of-Thought Prompting*, arXiv:2305.04388v2.** Selected
  methods/results/limitations sections show how irrelevant answer-position and
  suggested-answer cues can influence outputs without being mentioned in a
  plausible explanation. The limitations call their test necessary rather than
  sufficient for faithfulness. This supports recording cue/order sensitivity
  and avoiding an inference from plausible explanation to actual reasoning.
- **Lanham et al., *Measuring Faithfulness in Chain-of-Thought Reasoning*,
  arXiv:2307.13702v1.** Methods intervene through early answering, inserted
  mistakes, filler tokens, and paraphrasing; the paper explicitly lacks direct
  ground truth about internal reasoning and treats its tests as evidence about
  possible failures, not conclusive proof of faithfulness. SVB does not replicate
  these interventions or import their model findings as its own results.

Full HTML and abstracts were retrieved on 2026-11-14 with hashes, licenses, and
review scope recorded in
`data/v0.3.0/review/method_literature_registry.json`, separate from the reviewer
ZIP. Turpin's article states CC-BY-4.0; Lanham's arXiv copy has a perpetual
non-exclusive distribution license, not a permissive reuse grant. Raw text stays
in ignored local cache. This is a targeted follow-up, not a systematic novelty
search or line-by-line reading of both articles.

No new theorem, empirical benchmark superiority, or general scientific-AI
reliability result follows from the A/B/C separation. It is a useful
measurement design assembled from established principles. Its utility needs
independent references, competent systems, appropriate sampling, and external
replication.

## 6. Reference ambiguity is a separate threat

Several historical narrow source facts can reasonably be read as an arithmetic
reproduction, a descriptive empirical observation, or both. Scoring them as a
single exclusive support category can make category disagreement look like
scientific false acceptance. Report exact labels alongside coarse epistemic
decisions and expert-proposed alternative admissible categories. A panel may
judge an item ambiguous, suggest a narrower target, or withhold a definitive
label; it must not be forced to affirm the original author label.

Historical references stay immutable. Proposed revisions belong in a new
versioned adjudication record, including provenance, rationale, uncertainty, and
disagreement. Do not silently broaden an accepted-label set after looking at
model predictions. No external panel has yet qualified the historical eleven
provisional empirical claims or the twelve new items.

## 7. Evidence strength and stop conditions

The 32 historical cases are previously observed audit/development material. The
12 added public cases are newly authored for this phase, not proven absent from
model pretraining or protected from investigator access. Group source/study
lineage and paired targets, freeze before new scored runs, record all exposure
and deviations, and do not call a shared workspace a secret holdout.

Do not interpret A/B/C results as scientific competence if category semantics
remain materially unresolved, if response failures eliminate the answered
denominator, if original source methods are insufficient for the intended claim,
or if external reasoning judgments are absent. Report the experiment that
actually occurred and the qualification that failed. The new source families
remain a small purposive set; related claims and repeated model conditions are
not independent scientific studies and do not support iid population guarantees.

Recommended next evidence is independent domain/statistical adjudication,
source-complete replication by an external party, and a prospectively custodied
evaluation of additional capable systems. Architectural complexity and more
generated text are not substitutes for those observations.
