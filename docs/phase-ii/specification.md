# SVB Phase II specification, dataset version 0.2.0

This is an additive public evaluation release candidate, not a protected test or an independently expert-validated benchmark. The v0.1 manifest, tasks, protocols, original scoring implementation and recorded results remain unchanged. Its39-test clean-checkout reproduction and successful hosted run are recorded in results/v0.2.0/v01_reproduction.json.

## Cases and epistemic targets

There are32 cases in16 pairs. Penguin observations/primary article supply8 development items. Puromycin enzyme rates, grass-plant repeated CO2 uptake and FreeSolv hydration thermodynamics supply24 evaluation items across three distinct source families. The split is source-family-disjoint, not a claim of arbitrary semantic independence or unbiased population sampling. Sources derived from the same scientific dataset stay together. Eleven cases are provisionally empirically_supported, five computationally_established, twelve insufficient_evidence and four refuted. Evaluation alone has8,4,8,4 respectively.

Empirical support here is narrow: recorded descriptive experimental/observational facts under the named source context. It is not independent reproduction of laboratory execution. The R datasets are curated secondary transcriptions; original full laboratory protocols were not obtained. FreeSolv mixes experimental and calculated fields, includes assigned default uncertainties, and carries upstream license/provenance caveats. The primary penguin article supplies an attributable actual experimental context but is development data. All categorical labels remain provisional author judgments; an empirical-source-fact label is not external expert qualification.

The case schema separates `packet` from `reference`. Public packet fields are exactly question, claim, documents (id/title/text/source_id), methodology and naturally disclosed assumptions. Internal IDs, families, pair roles, splits, labels, numeric-check descriptions, absence lists, counterexamples and adjudication reasoning do not enter model prompts. Opaque IDs are mapping conveniences, not secrecy. Source-derived design limitations and original uncertainty notes remain legitimate evidence. Synthetic adjudicator absence checklists were removed before freeze.

## Information conditions

Evidence supplies documents. No_evidence withholds documents, and each case has a separately adjudicated insufficient_evidence reference for that supplied-record condition. No_assumptions removes only a mostly redundant assumptions annotation; important design facts remain in source documents, so this is a weak ablation. Verified_numbers adds calculator facts for the specified first four evaluation cases without answering scientific adequacy. Paraphrase changes only the task question, not the claim or record; this is limited wording sensitivity, not a broad robustness study.

Conditions use explicit condition_labels and condition_scopes. A justified no-document abstention is not an error against an inaccessible full-record answer. Metadata about the information condition does not tell the evaluated model which reference label applies.

## Policies and real model

A bounded public-packet numerical parser performs exact arithmetic/counts/residuals and explicitly declines unsupported prose. The evidence-aware policy is deliberately a weak lexical comparator. It is not an oracle or a scientific verification service. Both receive only public packets; neither reads case IDs or references.

The pinned public Qwen2.5-0.5B-Instruct model runs offline locally, without private model credentials or paid APIs. Its immutable prompt bundle contains60 intended requests:24 evidence,24 no_evidence and the first four evaluation cases each under verified_numbers, no_assumptions and paraphrase. The small assistance/paraphrase subset contains only two enzyme pairs from one source and cannot establish general effects. Development tested access/format on unrelated arithmetic, not scientific evaluation answers. The model's pretraining exposure to public scientific datasets is unknown.

The run uses greedy generation, seed0, CPU float32,4threads, maximum384 output tokens and4096 input tokens. Inputs exceeding the cap fail explicitly; inputs are never silently truncated. Raw malformed and token-limited outputs remain retained. No response repair, correctness-based retry or parameter tuning follows scored outputs.

## Scoring and uncertainty

Primary scoring requires valid structured output and normalized six-class probabilities, with unknown IDs/duplicates/contradictions rejected. Every preselected case remains in denominators; raw execution, timeout, unsupported, malformed and missing statuses remain distinct. Exact category accuracy is separate from coarse epistemic decision accuracy: a computational versus empirical support-category mismatch must not automatically be described as false scientific acceptance. Scope escalation is counted for accepted final conclusions, not for uncertainty/refutation scope annotations.

A frozen secondary diagnostic extracts only an unambiguous explicit JSON label field. It never rescues primary malformed outputs, repairs probabilities or validates reasoning. If primary coverage is low, claims about scientific ability remain limited even if a label is extractable.

Evidence IDs and verbatim quotes are checked mechanically. A real quote does not establish entailment; human reasoning accuracy, fabricated semantic support and adequate uncertainty interpretation remain unscored pending actual reviewer work. Human packets/rubrics are complete, but no human review or agreement statistic is claimed. Brier/confidence risk calculations apply only to valid vectors. These few related cases do not support iid population CIs, superiority significance or calibrated-deployment guarantees.

The frozen code/source/prompt manifest is data/v0.2.0/manifest.json. Scientific acquisition mistakes, rejected sources, prefreeze reference corrections and initial adapter construction failures are retained in the review and evidence records. A hash identifies a specification; it does not prove the scientific correctness of labels.
