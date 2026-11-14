# Phase IIb executed research report

Phase IIb makes a limited real-model experiment interpretable: a legal minimal
verdict can now be distinguished from a wrong scientific verdict. It does not
qualify a general scientific verifier. All three tested model candidates failed
at least one unchanged development gate. On the final public-source diagnostic
comparison, both selected models produced admissible minimal verdicts for all
12 evidence-present items, while neither produced an admissible rich response
on its six matched cases. Observable numerical and scope errors remain after
reducing format burden. Scientific reference interpretations remain provisional
author judgments; no independent human reviews have occurred.

## Executions, freeze and preservation

The continuation starts from `9757e4b2f82e9023a17b5173ca0d1495ad445b2d` on the
existing draft PR #1. The additive foundation is commit
`e7bd1d8d197897428ca846f1f3fcdc3b8835c619`. Main remains the Phase I commit
`30f842e241b0a37ab5d24ef6537113d6bbbb4103`; nothing is merged. The historical
PCS reference error, Phase II's 60/60 primary schema failures, interrupted-run
record and all other original negative findings remain unchanged. A byte audit
checks 111 protected prior code/data/result files against the continuation base.
Read-only subject HEADs, tracked bytes and Git statuses match their initial
snapshots. No PCS, FoldBounds or website source was modified.

The data/protocol 0.3 manifest was frozen before the first new-source request;
its SHA-256 is
`d87f519ccfe72490737779059fc73f5402fac5780a55d06f8adbd7f50d7119d5`.
This is an internal freeze, not external preregistration or a protected test.
See [specification](specification.md) for all denominators, prompt controls,
interventions and construct limits. Frozen Phase I/II manifests still validate.

Actual execution includes **75 development calls** across pinned public
Qwen2.5-Instruct 0.5B, 1.5B and 3B checkpoints and **120 final calls** across the
original 0.5B/1.5B pair. Every generation completed; there were no input
truncations, paid API calls, private model credentials or correctness retries.
One final B response hit its 128-token cap and remains incomplete in the record.
The two final models used approximately 993.25 seconds of observed generation
and 1,018.63 seconds of runner wall time including loading, on shared CPU
hardware. These timings are descriptive. The development-only 3B checkpoint uses
the noncommercial Qwen RESEARCH LICENSE, rather than Apache-2.0; no weights are
redistributed. Complete identity/license hashes and versions accompany every run.

## Development qualification: all failures retained

The fixed gate required standard A syntax >=5/6, exact category agreement >=4/6,
and standard/reversed-enumeration consistency >=4/6. Controls were authored
instruction probes and two historical public cases, not new scientific studies.

| Model | Standard syntax | Standard exact | Same category after order reversal | Constrained standard exact | All gates |
|---|---:|---:|---:|---:|---|
| 0.5B | 6/6 | 0/6 | 3/6 | 0/6 | Fail |
| 1.5B | 6/6 | 4/6 | 3/6 | 3/6 | Fail |
| 3B, development only | 6/6 | 4/6 | 2/6 | 4/6 | Fail |

Alternative-wording exact agreement was 1/3, 3/3 and 2/3 respectively; wording
*consistency with the standard prediction* is a different quantity. The bounded
third candidate was added after the first two failures and before new-source
inference. No thresholds were relaxed or fourth candidate sought. The original
capacity levels remain diagnostic measurements, not qualified model selection.
See [qualification](model_qualification.md) and the complete versioned records.

## New scientific evidence and reference calculations

Twelve cases form six pairs from three additional studies: historical paired
sleep prolongation, longitudinal chick growth and biochemical oxygen demand.
There are three computational, three narrow empirical-source-fact, three refuted
and three insufficient-evidence references. The nine exact numerical witnesses
and all source transformations check independently. Examples include:

- Sleep: 10 within-patient differences sum to 15.8 hours, mean **1.58 hours**;
  nine are positive and one is tied. This does not establish improvement for
  every future patient.
- Chick growth: day-21 diet-4 minus diet-1 sample means equal **2189/36 g**,
  with n=9 and n=16 respectively. Chick 1 grows from **42 to 205 g**; the
  observed 163 g increase does not identify that chick's causal counterfactual.
- Oxygen demand: day-7 minus day-1 equals **11.5 mg/L = 0.0115 g/L**. A recorded
  day-3/day-4 decrease does not uniquely identify cessation of aerobic respiration.

Sources are licensed archived official R transcriptions, not new laboratory
measurements or independent replications of primary experiments. Additional
study families share a curation channel. They may be in model pretraining.
The source dossiers distinguish finite recorded facts from population, causal
and mechanistic interpretation. No new statistical uncertainty interval is
invented for a data source lacking a justified measurement/replication model.
See [source dossiers](new_sources.md) and `reference_checks.json`.

## A: minimal scientific verdicts

All denominators below include malformed outputs. Coarse correctness merges the
three accepted evidence categories only; exact category agreement stays visible.
False acceptance means an accepted label on a refuted or insufficient reference.
Explicit false rejection means `refuted` on an accepted reference; abstention is
reported separately in the machine-readable confusion matrices.

| Model / decoding | Documents | Admitted / 12 | Exact / 12 | Coarse / 12 | False accept / nonaccept references | Explicit false reject / accepted references |
|---|---|---:|---:|---:|---:|---:|
| 0.5B unconstrained | Present | 12 | 2 | 2 | 1/6 | 2/6 |
| 0.5B constrained | Present | 12 | 1 | 2 | 1/6 | 2/6 |
| 1.5B unconstrained | Present | 12 | 6 | 6 | 2/6 | 1/6 |
| 1.5B constrained | Present | 12 | 5 | 6 | 2/6 | 1/6 |
| 0.5B unconstrained | Withheld | 9 | 0 | 0 | 2/12 | Not applicable |
| 0.5B constrained | Withheld | 12 | 0 | 0 | 2/12 | Not applicable |
| 1.5B unconstrained | Withheld | 12 | 7 | 7 | 3/12 | Not applicable |
| 1.5B constrained | Withheld | 12 | 7 | 7 | 3/12 | Not applicable |

The three inadmissible 0.5B outputs without documents remain malformed, rather
than repaired into a verdict. The decoding constraint improves their syntax but
does not improve coarse scientific agreement. Exact accepted-category choices
change under the constraint; it is an intervention in decoding, not a repair of
the unconstrained record.

Under document withdrawal the target is justification from the supplied record;
all references are insufficient evidence. Models may have prior source memory,
but recalling external information does not demonstrate uptake of the withheld
record. This intentionally single-class condition is not a standalone balanced
competence test. Among the six supported evidence-present cases, the number with
both an accepted evidence-present prediction and correct insufficiency after
withdrawal is **0/6 for 0.5B and 1/6 for 1.5B**, in either decoding mode.

### Study-family and pair analysis

| Model, unconstrained with documents | Chick growth exact / 4 | Oxygen demand exact / 4 | Sleep exact / 4 | Both exact in pair / 6 |
|---|---:|---:|---:|---:|
| 0.5B | 1 | 0 | 1 | 0 |
| 1.5B | 3 | 2 | 1 | 1 |

Constrained family exact counts are 0/0/1 and 3/1/1 in the same column order;
coarse family counts remain 1/0/1 and 3/2/1. Each family contains related
source-derived items; these are three study clusters, not 12 independent
scientific experiments. No population confidence intervals, p-values, causal
parameter-count claim or general model ranking is inferred.

Concrete errors survive accepted-category ambiguity. The 0.5B model accepts
CW01X, the false reversal of the observed day-21 mean ordering. The 1.5B model
accepts OD01X, a factor-1000 unit error, and SL02S, an unsupported universal
future-patient treatment claim. Both models also decline some supported narrow
facts. These are observable outputs conditional on the packet and current
references, not proof of a latent reasoning mechanism.

The unchanged lexical baseline admits 12/12 evidence-present cases, exact 3/12,
coarse 6/12, with **5/6 false accepts**. Without documents it gives 2/12 correct
and 10/12 false accepts. The unchanged numerical baseline is **unsupported on
12/12 in both conditions**: zero answer coverage and zero correct answers.
Its limited parser does not recognize these packet forms. Zero observed false
accepts at zero coverage are not a safety advantage. Neither weak baseline
justifies a superiority claim over existing scientific AI methods.

## B: explanations and attribution

Both models produce nonempty prose on all six scheduled cases. Neither includes
a bracketed supplied-document ID on any of the six responses. The 0.5B prose
stays within the 80-word budget; five 1.5B responses exceed it and one reaches the
128-token cap. These are interface measurements, not scientific reasoning scores.
`scientific_reasoning_accuracy` remains null and human-reviewed n remains zero.

An explicitly internal, post-result [failure audit](output_audit.md) records
claim/source conflation, contradictory causal language, and an overlooked tie.
A correct-looking limitation can coexist with a false preceding statement.
B was generated in separate calls without A conditioning; disagreements are
preserved. There is no assessment of private internal reasoning faithfulness.

Source-complete candidate packages retain each model's six raw B outputs and
all 44 source packets. Provider metadata and gold are excluded from the ZIPs;
38 packets per candidate have no submitted response. Actual reviewers should
adjudicate references first, then assess the six available candidates. These
packages do not create protected access or actual blinding. No reviews were
invented, and no reviewer was contacted.

## C: preserved full-schema compliance

Both models have **0/6 strict admissions**, all six outputs schema-malformed.
On those same six cases, A admits 6/6 for each model, with exact agreement 0/6
and 4/6 respectively. All 12 C generations completed successfully at the process
level. The unchanged historical scorer normalizes malformed responses to its
`execution_error` scoring status; `raw_statuses: malformed` and the run logs
preserve the distinction from a runtime crash. Its zero admitted false accepts
and null admitted risk cannot establish scientific safety. The historical
item-wise Wilson field is not used for inference on clustered items.

A/C compares matched cases but different instruction bundles: C preserves old
ordering, definitions and longer schema instructions. It establishes measured
interface burden under these bundles, not a causal estimate attributable solely
to schema complexity. Format-only label extraction remains a secondary
historical diagnostic and never rescues the strict score.

## Formal correctness versus practical bound utility

A separate frozen study executed **32 actual FoldBounds CLI calls** on eight
small anchored HP-model families, with independent exact enumeration. All 32
probability/partition enclosures were valid. Across 248 related threshold
observations, no definite decision was wrong. Yet for six nontrivial families,
shallow/moderate configurations decided **0/36 interior thresholds**, enriched
**34/36**, and full enumeration **36/36**. Enriched configuration median wall
time was about 0.166 s versus 0.079 s for full enumeration at these tiny sizes.

Thus enclosure correctness and informativeness differ, and extra certification
machinery need not be cost-effective for every workload. The threshold decision
safety proof is elementary and conditional on a valid enclosure. These results
do not establish protein-model physical adequacy, asymptotic scaling, clinical
utility or a novel mathematical theory. PCS proof checking likewise does not
supply missing empirical evidence. See [utility analysis](bound_utility.md).

## Reference qualification and external review

The [reference audit](reference_adjudication_audit.md) checks all 11 historical
empirical-support cases. Their archived facts and arithmetic check, but the
empirical/computational category boundary, missing primary methods and scope
require real domain judgment. No frozen gold is rewritten. The external package
contains 44 packets and 132 blank role forms, retained source bytes and notices.
The proposed panel needs two appropriately assigned domain reviewers and a
statistical reviewer; the [review brief](external_review_brief.md) estimates
22–37 domain-review hours plus 7–15 statistical-review hours before orientation,
primary-source retrieval and disagreement resolution. These are planning
estimates, not completed reviews or commitments.

External priorities are primary-method reconstruction, atomic claim/category
qualification, experimental-unit/uncertainty checks, reference disagreement, and
candidate source entailment. Independent custody and genuinely fresh model
exposure controls remain absent. Public field filtering cannot remedy that.

## Claims and hypothesis status

**Established computational observations:** artifact hashes validate; references
recompute; all 157 software tests pass; the actual pinned models produce the
recorded categories/prose/schema failures; and the small finite-model bound
utility contrast reproduces from exact references. Hosted foundation CI passed;
A clean export of the staged tracked tree also passes all 157 tests, all three
manifest checks and both source-reference checks. Phase I baseline JSON/CSV,
Phase II baseline JSON and Phase IIb recorded scores reproduce byte-for-byte
there. Final-head hosted status is linked from the PR/platform, not preclaimed
here.

**Internal author judgments:** the six-label references, source interpretation,
scientific severity and manual output examples. No human scientific agreement
or broad scientific-reasoning accuracy is established by these judgments.

**Exploratory interpretation:** lower format burden reveals specific inappropriate
acceptances previously obscured by total schema failure. This improves diagnostic
interpretability; it does not validate SVB as a general scientific-reasoning
instrument or show superiority over modern systems.

H1 (ordinary QA accuracy conceals false acceptance) lacks a matched conventional
QA comparison. H2 (scope evaluation adds reliability information) has specific
scope-error examples but no strong external-method comparison. H3 (verification
assistance improves mathematics without empirical inference) was not tested in
Phase IIb. H4 (explicit dependencies improve gap detection) lacks a controlled
intervention. All four remain unconfirmed as general research hypotheses.

Publication-quality claims still require independent reference adjudication,
more diverse primary experimental sources, stronger models passing development
controls, genuinely prospective independent custody/exposure procedures,
human rationale scoring, appropriate clustered designs and strong comparison
methods. This draft provides an auditable experiment and review package,
not external scientific validation.

See [reproduction commands](reproduce.md), [manuscript continuation](manuscript.md),
`results/v0.3.0/results.json` and the machine-readable evidence ledger for exact
artifacts and execution accounting.
