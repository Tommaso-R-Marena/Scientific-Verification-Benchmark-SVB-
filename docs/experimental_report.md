# Executed experimental report: SVB 0.1.0

## Design and evidence boundary

The primary experiment was frozen before scoring. It uses 34 public authored tasks: 11 development controls, 22 scored evaluation items and one retained unscored open question. The scored subset spans six domains and is a purposive convenience set, not a sampled population. Code and references have internal adversarial review but no independent human domain adjudication. The public metadata explicitly describes missing evidence: this is a test of engineered policies on structured controls, not a blind scientific AI challenge.

The independent core used no external APIs, no paid services and no subject-repository imports. Exact Fraction calculations, finite countermodels, independent Decimal checks and source-byte hashes support the numerical references. Scientific sufficiency labels require review of their alternative-world arguments; the checker cannot mechanically validate arbitrary empirical adequacy. No empirically_supported positive is scored.

## Frozen diagnostic comparison

| Policy | Correct / scored | Accuracy | False accepts / nonaccept reference | Scope overclaims | Mean Brier, answered |
|---|---:|---:|---:|---:|---:|
| always_accept | 3/22 | 0.1364 | 18/18 | 8 | 1.7273 |
| always_insufficient | 10/22 | 0.4545 | 0/18 | 0 | 1.0909 |
| always_unsupported | 0/22 | 0.0000 | 0/18 | 0 | undefined |
| calculation_only | 10/22 | 0.4545 | 11/18 | 10 | 1.0909 |
| scope_gated | 21/22 | 0.9545 | 0/18 | 0 | 0.0909 |

All policies except always_unsupported answered all items; unsupported has zero coverage and undefined answered risk/Brier. Insufficient evidence is a substantive completed judgment, not the same as unsupported capability. There are four acceptance-reference and 18 nonaccept-reference items. Missing and failed runs remain in total denominators. All observed completed responses are retained; no unfavorable task was removed after core scoring.

Computation-only and always-insufficient have identical categorical accuracy (10/22), but the former makes 11 false acceptances while the latter makes zero. Accuracy alone therefore hides materially different behavior on these controls. The scope-gated policy gets 21/22 and still rejects the correct exact variance in C04: its unstable binary64 E[X²]-E[X]² calculation is not repaired by an evidence-scope gate. This is a negative result for numerical reliability, retained unchanged. Python 3.12 built-in sum uses an improved summation algorithm; the apparent cancellation case C02 is correctly rejected by both arithmetic policies. These measurements do not estimate prevalence of analogous errors in deployed tools.

One-hot confidence vectors are intentionally degenerate diagnostic outputs, not calibrated probabilities. Brier scoring shows realized category error, not demonstrated population calibration. No smooth risk-coverage curve is meaningful without a confidence ranking. Wilson 95% intervals are available in the JSON only as descriptive reference under hypothetical iid assumptions; those assumptions do not hold for this purposive dependent dataset. For scope_gated the interval is approximately [0.7820,0.9919], but it must not be interpreted as a population performance guarantee. No superiority p-value is reported.

## Post-hoc decomposition

Hybrids of the two frozen response files isolate the two changed mechanisms, without altering any label: scope gate only 20/22 (one false accept), strict JSON only 11/22 (ten false accepts), both 21/22 (zero false accepts). These are post-hoc diagnostic decompositions, not preregistered independent model trials. The missing-bridge gate is explicitly supplied the relevant metadata; success is not evidence of discovering missing assumptions from arbitrary scientific prose.

## Genuine subject conformance

| Subject | Matched / eligible | Observed total | Reference errors |
|---|---:|---:|---:|
| FoldBounds | 18/18 | 18 | 0 |
| PCS | 3/3 | 4 | 1 |
| PCS website module | 6/6 | 6 | 0 |

These are separate capability tests with separate denominators. FoldBounds exact anchored 2D HP enumeration covers six small length-4–7 parameter families and nested-depth outputs plus two invalid-input controls; related depths are not independent samples. PCS checks an existing signed balanced reaction, artifact corruption and malformed transcript with an actual compiled Lean authority. One initially expected REJECT instead returned ACCEPT because verified builtin atom counting intentionally overrides untrusted transcript assertions. That is a benchmark author reference error: both protocol versions and the unfavorable observation are preserved, the case is unscored, and the experiment is not described as pristine preregistration. The website experiment imports its real JS CSV module and report generator, not a mocked implementation; it checks four valid and two malformed cases plus scope strings. DOM/visual usability and production services are not evaluated.

No subject defect or general scientific-verification guarantee is established. Passing toy-model controls cannot validate physical protein binding, experimental data quality or empirical safety. Runtime timings include process startup and are not a controlled scaling study. See system_evaluations.md and results/system_summary.json for exact scope, commits and executable/module identities.

## Mathematics and novelty

A separate standalone Lean 4.28 file verifies conditional unary rule-closure and excluded-type invariants with no axioms, no subject imports and no Mathlib. The more general multipremise DAG argument is given as a complete written induction, not claimed to be mechanically checked by that file. The frozen reference protocol statement that no new machine-checked theorem is claimed concerns the benchmark reference tasks and absence of a new mathematical discovery; the later elementary mechanization is recorded separately. Type-source closure, proper scoring and selective evaluation are established ideas. No genuinely novel theorem or empirically superior general AI method has been demonstrated.

## Validity, limits and reproduction

Construct validity: narrow structured declarations simplify the scientific judgment problem. Reference reliability: exact arithmetic and byte hashes are inspectable; physical/epistemic labels still need external experts. Selection bias: authored controls and familiar PCS fixture limit generalization. Leakage: all labels and checker specifications are public; grouping fixes known paired leaks but does not prove semantic independence. Statistical power: no population power or significance claim is justified. External validity: no real clinical, biological-affinity or general LLM evaluation occurred. Dependence: related controls and systems are not exchangeable statistical trials. Confounding: the primary gated contrast changes both scope and strict JSON behavior, separated only by the labelled post-hoc hybrid decomposition. Novelty search: targeted metadata/abstract review only, not systematic full-paper review.

Run the README core commands from a fresh checkout. No runtime Python dependency or network is required. Core result JSON and CSV reproduced byte-for-byte in Python 3.12.14. Frozen hashes detect corruption; future benchmark revisions must bump version and preserve prior records. Optional adapters need authorized subject checkouts and a precompiled authority; their unavailable outcomes are explicit. The independent Lean proof is optional and reproducible with Lean 4.28. The 36-test final suite and underlying evidence logs are retained. Subject HEADs, tracked bytes and Git statuses remained unchanged.

## Three next steps

1. External domain adjudication, empirical positives and genuinely protected family-separated testing.
2. Blinded real model/tool responses with independently judged scientific reasoning and calibrated uncertainty.
3. Independent laboratory replication, broader licensed biophysical data, local DOM evaluation and hard sandboxing before executable submissions.
