# Measuring the Scope of Scientific Verification: An Executable Pilot Benchmark

**Publication-oriented working draft, version 0.1.0 — not publication-ready.**
This document reports a completed initial implementation and its recorded
experiments. It is not a public release announcement, externally adjudicated
benchmark, or claim of a new mathematical theory. No external AI API or paid
model evaluation was performed.

## Abstract

Scientific calculations can be correct while their attached interpretations
remain unsupported. We introduce an independent pilot Scientific Verification
Benchmark (SVB) that represents mathematical, computational, numerical,
statistical, modeling, empirical, provenance, and sufficiency judgments separately.
The executable release contains 34 authored tasks: 11 development items, 22 scored
evaluation items, and one retained unscored research question. References use
exact arithmetic, finite countermodels, source-byte checks, and explicit
author-adjudicated missing-evidence arguments; none are supplied by the evaluated
systems. Public data include an archived Iris dataset variant and deposited
crambin coordinates. Five deterministic diagnostic policies were executed. A
calculation-only policy scored 10/22 and falsely accepted 11/18 nonacceptance
reference cases. Adding declared scope and strict-JSON gates scored 21/22 with
0/18 false acceptances, while retaining a floating-point variance failure. These
are engineered controls, not estimates of AI generalization. Noninvasive local
tests matched references for FoldBounds on 18/18 related controls, PCS on 3/3
eligible controls among four observations, and website computational modules on
6/6 controls. One initial PCS discrepancy exposed an author reference error and
was retained unscored. A small independent unary scope-closure theorem was checked
in Lean; broader scientific soundness remains conditional. The release establishes
a reproducible diagnostic pipeline, not general scientific reliability,
biological validation, or demonstrated mathematical novelty.

## 1. Introduction

A verifier can establish a formula within a model without establishing that the
model is physically adequate. Repeating a computation on fixed data cannot alone
establish causal identification or independent experimental corroboration.
Evaluation must preserve these distinctions rather than collapsing every
successful computation into acceptance of a scientific conclusion.

SVB investigates an operational question: can a small, independently specified
evaluation pipeline detect incorrect computations, missing assumptions, and
invalid transitions from limited evidence to stronger claims? The first release
prioritizes auditable references and real execution over breadth. PCS, FoldBounds,
and the PCS website inform capability selection but are prospective subjects,
not architectural dependencies or reference authorities.

The contributions are engineering and methodological integration: a frozen public
pilot, data-only scoring, explicit unsuccessful/unsupported outcomes, independent
reference routines, diagnostic policies, narrow local adapters, and an evidence
ledger. We do not claim the taxonomy, proper scoring, abstention metrics, or typed
closure result is novel.

## 2. Related work

Verification, validation, and uncertainty quantification already distinguish
software correctness from model adequacy [1]. Reproducibility and independent
scientific replication are likewise distinct activities [2]. Statistical
interpretation cannot be reduced to a numerical p-value [3]. Proper scoring rules
[4] and selective prediction [5] provide established tools for probabilistic
evaluation and coverage/risk reporting.

SciBench evaluates scientific problem solving [6], SciRIFF addresses scientific
literature instruction following [7], and ScienceAgentBench evaluates executable
data-driven scientific tasks [8]. SVB's proposed emphasis is the admitted scope of
a justification and explicit evidence insufficiency. That emphasis has not been
shown here to be unique, more comprehensive, or superior to those resources.
CASP and D3R demonstrate established blind assessment traditions for protein
structure and ligand-related predictions [9,10]. SVB does not reproduce their
prospective blinding or experimental target coverage.

This initial review inspected selected arXiv abstracts and Crossref metadata;
the full papers were not reviewed. The structured novelty matrix and retrieval
registry are in `docs/related_work.md` and
`references/literature_registry.json`. A systematic novelty claim would require
substantially more review, especially in assurance cases, scientific provenance,
refinement types, causal identification, and scientific claim verification.

## 3. Problem formulation

An item comprises a question, proposed claim, assumptions, model-relative
specification, identified evidence sources, uncertainty, reference method,
appropriate response, and adjudication limitations. Labels are
`formally_established`, `computationally_established`, `empirically_supported`,
`refuted`, `insufficient_evidence`, and `disputed_or_unresolved`. A label names the
kind of conclusion supported by the supplied evidence, not a universal claim
about reality. The empirical-support label has **no instantiated cases in this
release**.

Execution status is separate from scientific labeling: unsupported task, failed
execution, and malformed output must not silently disappear. An appropriate
insufficient-evidence answer is a substantive scientific judgment, whereas an
unsupported adapter is a capability limitation. A true theorem with an invalid
supplied proof is distinguished from a false theorem. Refuting a justification
does not automatically refute its conclusion.

A typed justification graph admits only declared rules and evidence identities.
The written scope theorem states that if all source and rule conclusion types
remain in an allowed set, no derivation introduces an excluded type. Conditional
semantic soundness additionally requires true premises and sound admitted rules.
Those assumptions include the difficult scientific questions; the theorem does
not establish them. `theory/Scope.lean` independently mechanizes only a unary
rule-closure formulation, not the full multi-premise graph or the implemented
benchmark. Lean 4.28.0 reported no axioms for its two closure theorems.

## 4. Benchmark construction and references

The 34 items span mathematics (6), computation (6), statistics (6), biophysics
(7), provenance (4), and verification reliability/safety (5). Their 11/23
development/evaluation allocation contains one unscored open question, leaving 22
scored evaluation cases. The scored evaluation references comprise one formally
established, three computationally established, eight refuted, and ten
insufficient-evidence judgments. The unscored item asks what model would suffice
universally for ligand affinity prediction; it is retained as an open program
question rather than an adjudicated scientific controversy.

References were authored independently of subject outputs. Exact rational
calculations address finite equalities, variance, and statistical-mechanical
quantities. Explicit compatible countermodels justify nonidentifiability and
missing-bridge judgments. Source identity uses hashes and documented transforms;
a matching hash does not establish that a scientific source is true. The
author-specified missing-evidence declarations are especially easy for a policy
to read; success on them is not autonomous scientific evidence discovery.

Public data are UCI Iris, DOI `10.24432/C56C76`, from the `iris.data` archive
variant, and deposited crambin structure 1CRN, DOI `10.2210/pdb1CRN/pdb`. The
registry preserves source URLs, licenses, hashes, and transformations. Iris
historical variants are not silently equated; decimal coordinate bytes are
treated exactly as stored values, not as exact physical positions. Geometry
questions do not establish ligand affinity or physical protein populations.

`data/manifest.json` freezes task, protocol, source, and core implementation
identities before the first scored core comparison. Labels are public. The
development/evaluation grouping is a reproducibility measure, not access control;
there is no protected held-out set. Cases, references, and interpretations have
not received external human scientific expert adjudication. Separate AI review
is criticism, not independent empirical evidence or a substitute for that review.

## 5. Experimental methods

The core experiment executes five fixed policies against the public task view,
which excludes stored reference labels and explanations. `always_accept`,
`always_insufficient`, and `always_unsupported` are denominator controls.
`calculation_only` performs finite checks and treats correct calculations as
sufficient; `scope_gated` adds a declared missing-evidence gate and strict JSON
handling. Both retain the same floating-point calculation. They are hand-coded
diagnostic policies with knowledge of the item schema, not trained models or
competitive general scientific reasoning systems.

We report all-task exact-label accuracy, answered coverage, false acceptance over
the 18 nonacceptance references, accepted risk, scope overclaims, and multiclass
Brier loss on answered items. Unsupported responses remain in total accuracy and
have zero answered coverage. One-hot policies do not provide a useful confidence
ranking, so no smooth risk-coverage curve or calibration finding is asserted.

The retained post-hoc ablation switches responses on missing-bridge and
strict-JSON item kinds. It decomposes recorded behavior without modifying frozen
labels; it is not a separately preregistered discovery. Wilson intervals are
reported only as descriptive calculations under a hypothetical iid Bernoulli
model. The purposively selected and related cases do not satisfy that sampling
model, so these are not population confidence guarantees or superiority tests.

System evaluations follow separate capability protocols. Actual local interfaces
are invoked with timeouts, fixed commands, restricted child environments, and
outputs located in the independent project. No arbitrary submitted code is
executed. Existing subjects are read-only; no source, configuration, branch, or
deployment change is made. These precautions are not a security sandbox for
arbitrary programs.

## 6. Results

### 6.1 Executed core controls

The values below are from `results/core/baselines.json`.

| Policy | Correct / scored | Answered coverage | False acceptances / nonacceptance references | Accepted risk | Mean Brier, answered |
|---|---:|---:|---:|---:|---:|
| Always accept | 3/22 | 22/22 | 18/18 | 19/22 | 1.7273 |
| Always insufficient | 10/22 | 22/22 | 0/18 | Undefined: no acceptances | 1.0909 |
| Always unsupported | 0/22 | 0/22 | 0/18 | Undefined: no acceptances | Undefined: no answers |
| Calculation only | 10/22 | 22/22 | 11/18 | 11/14 | 1.0909 |
| Scope and strict-JSON gates | 21/22 | 22/22 | 0/18 | 0/3 | 0.0909 |

Accepted risk uses exact reference-label correctness: always accept asserts the
computational category even for the one formal-category reference, explaining
19/22 accepted-label errors versus 18/18 false acceptances on nonacceptance
references. These two metrics answer different questions.

The calculation-only and gated accuracy descriptive Wilson ranges are
26.9–65.3% and 78.2–99.2%, respectively, under the hypothetical iid model only.
No statistical significance or deployment generalization is inferred. The result
demonstrates the intended diagnostic contrast on authored cases, not that real
AI systems have these error rates.

Both computational policies incorrectly reject the correct exact population
variance `2/3` of `[10^9+1,10^9+2,10^9+3]`. Their unstable floating-point
variance calculation is unchanged by adding a scope gate. This retained failure
shows the gate does not repair numerical conditioning. It also prevents a claim
of complete correctness even on this small pilot.

### 6.2 Post-hoc decomposition

`results/ablations.json` reports 20/22 correct and 1/18 false acceptances with only
the scope gate, 11/22 and 10/18 with only strict JSON handling, and 21/22 and
0/18 with both. The ten remaining strict-JSON-only false acceptances are the
declared missing-evidence cases. The decomposition supports the mechanism of
this diagnostic implementation; it does not establish a new generally effective
verification algorithm.

### 6.3 Noninvasive subject evaluations

| Subject | Observed controls | Eligible controls | Matched reference | Reference errors |
|---|---:|---:|---:|---:|
| FoldBounds | 18 | 18 | 18 | 0 |
| PCS | 4 | 3 | 3 | 1 |
| Website module | 6 | 6 | 6 | 0 |

FoldBounds was run through its actual CLI on six small sequence/parameter
families, length 4–7. Sixteen depth-specific checks and two invalid-input
controls passed: independently enumerated exact values fell inside returned
intervals and full-depth results matched. These are related small cases, not 18
independent protein experiments. No Lean proof replay or physical validation was
performed by this adapter.

PCS used its actual compiled authority, one signed balanced-reaction fixture,
independent stoichiometry and signature/hash checks, plus corruption/transcript
controls. An initially expected rejection instead returned acceptance when an
external transcript said FAIL. Inspection established that the builtin Lean
atom-balance checker takes priority over that transcript. The initial expectation
was an **author reference error**, not evidence of a PCS defect. The original
expectation and observation remain recorded unscored; the case was not converted
to an additional scored success. The four-observation total is retained, with
only three eligible controls. The revised system protocol explicitly discloses
post-observation adjudication; these results have no pristine preregistration
claim. Independent signature/stoichiometry checks do not reimplement every PCS
admission rule.

The actual website JavaScript parser, overlap analyzer, and report generator
matched four valid and two malformed CSV controls. Generated report text retained
the tested scope statements. This is not a DOM-rendering, human-comprehension,
account-service, or production-interface evaluation. No pooled leaderboard is
appropriate for these different capabilities.

## 7. Limitations and threats to validity

**Construct validity.** Explicit missing-evidence fields simplify the target
problem. Natural-language extraction, fabricated-paper detection, scientific
model selection, and expert adjudication are not solved. The empirical-supported
category is empty, limiting what the taxonomy has actually exercised.

**Reference validity.** Exact arithmetic references are narrow but auditable;
scope judgments are author-adjudicated. The PCS reference-error finding is direct
evidence that reference construction itself can fail. System-authored signed
containers test compatibility and selected boundaries, not unfamiliar scientific
generalization.

**Selection, leakage, and power.** Public labels, convenience cases, small counts,
and related parameter variations preclude hidden-test, iid, or population claims.
The study does not measure prevalence of scientific overclaiming in current AI.
There is no paid or open-weight LLM run, prospective external submission, power
calculation for a scientific effect, or broad system comparison.

**Theory and implementation.** Lean checks a small unary closure invariant;
semantic soundness still assumes valid source admission and sound bridge rules.
The benchmark implementation is not formally refined to the theorem. A true
mathematical theorem does not establish physical applicability.

**External validity.** Synthetic finite tasks and source-model calculations do
not validate binding affinities, biological discoveries, causal treatment effects,
or general AI safety. Source authenticity, licensing metadata, and adjudication
should receive independent review before redistribution or publication claims.

## 8. Discussion and next research steps

The defensible finding is that a functioning independent pipeline can preserve
distinct error classes and make denominators, unsupported capabilities, and
reference mistakes visible. The authored diagnostic contrast shows why correct
calculation is insufficient for stronger scientific claims when the missing
bridge is explicitly represented. It does not demonstrate that SVB newly detects
a previously unknown class of scientific error or outperforms existing resources.

PCS could benefit from separately evaluating admission correctness and evidence
adequacy on independently sourced unfamiliar claims. FoldBounds could benefit
from broader independent interval, perturbation, and scaling tests while keeping
model-relative guarantees distinct from physical validation. Neither benefit
requires changing the subjects to match this benchmark.

The three highest-value next steps are:

1. Obtain external human mathematical, statistical, and scientific adjudication;
   add genuinely empirical-support cases with independent validation evidence and
   retain disagreements instead of forcing labels.
2. Establish a custodian-controlled fresh evaluation set and prospective protocol;
   test competent external systems or real scientific agents with cost and access
   authorized in advance, separating capability coverage from incorrect certainty.
3. Expand independent references and adversarial controls, including multi-premise
   formalization, stable numerical algorithms, realistic correlated uncertainty,
   and blinded biochemical targets; reproduce the release independently before
   claiming novelty or broad reliability.

## 9. Reproducibility statement

The core uses Python's standard library and runs without any subject checkout.
Recorded experiments used Python 3.12.14. From the new project root:

```sh
PYTHONPATH=src python3 -B -m unittest discover -s tests -v
PYTHONPATH=src python3 -B -m svb.cli validate
PYTHONPATH=src python3 -B -m svb.cli references
PYTHONPATH=src python3 -B -m svb.cli experiment --output results/reproduced
PYTHONPATH=src python3 -B scripts/analyze.py
```

The retained test log records 39 passing tests at the time of writing.
`results/core/baselines.json`, `results/ablations.json`, and
`results/system_summary.json` contain the reported measurements; manifests retain
content identities and the public-freeze boundary. Optional subject reproduction
is described in `docs/system_evaluations.md`; it needs the actual trusted local
subjects and, for the PCS signature cross-check, `cryptography`. Full raw local
records are separate from sanitized retained summaries. Timings are not promised
bit-identical and are not interpreted as controlled scaling measurements.

The new repository remains separate from the three subjects. Nothing in this
draft publishes a paper, deploys a service, or authorizes release of private
research code. A complete independent replication, external adjudication, and
full-text literature review remain prerequisites for publication-quality claims.

## References

1. National Research Council. *Assessing the Reliability of Complex Models*.
   2012. DOI: [10.17226/13395](https://doi.org/10.17226/13395).
2. National Academies of Sciences, Engineering, and Medicine. *Reproducibility
   and Replicability in Science*. 2019. DOI:
   [10.17226/25303](https://doi.org/10.17226/25303).
3. Wasserstein, R. L., & Lazar, N. A. *The ASA Statement on p-Values: Context,
   Process, and Purpose*. 2016. DOI:
   [10.1080/00031305.2016.1154108](https://doi.org/10.1080/00031305.2016.1154108).
4. Gneiting, T., & Raftery, A. E. *Strictly Proper Scoring Rules, Prediction,
   and Estimation*. 2007. DOI:
   [10.1198/016214506000001437](https://doi.org/10.1198/016214506000001437).
5. Geifman, Y., & El-Yaniv, R. *Selective Classification for Deep Neural
   Networks*. 2017. [arXiv:1705.08500](https://arxiv.org/abs/1705.08500).
6. Wang, X., et al. *SciBench: Evaluating College-Level Scientific
   Problem-Solving Abilities of Large Language Models*. 2023.
   [arXiv:2307.10635](https://arxiv.org/abs/2307.10635).
7. Wadden, D., et al. *SciRIFF: A Resource to Enhance Language Model
   Instruction-Following over Scientific Literature*. 2024.
   [arXiv:2406.07835](https://arxiv.org/abs/2406.07835).
8. Chen, Z., et al. *ScienceAgentBench: Toward Rigorous Assessment of Language
   Agents for Data-Driven Scientific Discovery*. 2024.
   [arXiv:2410.05080](https://arxiv.org/abs/2410.05080).
9. Kryshtafovych, A., et al. *Critical assessment of methods of protein
   structure prediction (CASP)—Round XIV*. 2021. DOI:
   [10.1002/prot.26237](https://doi.org/10.1002/prot.26237).
10. Parks, C. D., et al. *D3R grand challenge 4: blind prediction of
    protein–ligand poses, affinity rankings, and relative binding free energies*.
    2020. DOI: [10.1007/s10822-020-00289-y](https://doi.org/10.1007/s10822-020-00289-y).

Scientific-data references are identified separately in `data/registry.json`.
