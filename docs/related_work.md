# Targeted related-work and novelty assessment

This is a bounded initial literature check, not a systematic review and not a
priority claim. On 2026-11-13, we retrieved arXiv abstracts for four benchmark or
selective-prediction papers and Crossref bibliographic metadata for the references
below. Retrieval URLs, timestamps, HTTP status, and SHA-256 hashes are recorded in
[`literature_registry.json`](../references/literature_registry.json). These hashes
identify the retrieved metadata/HTML response, not the complete article. Full
papers were not reviewed in this pass. Search-result noise is retained in the
registry and is not silently treated as a cited reference.

## Relevant established work

| Area | Reference and evidence inspected | Relevance to SVB | What this comparison does not establish |
|---|---|---|---|
| Proper probabilistic scoring | Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*. [DOI:10.1198/016214506000001437](https://doi.org/10.1198/016214506000001437). Crossref metadata. | Proper scoring is established methodology. SVB's Brier-loss use and proof are not new scoring theory. | Correct reference labels, deployment calibration, or scientific validity do not follow from score propriety. |
| Abstention and selective prediction | Geifman & El-Yaniv (2017), *Selective Classification for Deep Neural Networks*. [arXiv:1705.08500](https://arxiv.org/abs/1705.08500). Abstract inspected. | Coverage and risk are established evaluation concepts; abstention must be measured with its denominator. | A synthetic benchmark does not reproduce this paper's experiments or establish useful deployment thresholds. |
| Verification, validation, and uncertainty | National Research Council (2012), *Assessing the Reliability of Complex Models: Mathematical and Statistical Foundations of Verification, Validation, and Uncertainty Quantification*. [DOI:10.17226/13395](https://doi.org/10.17226/13395). Crossref metadata. | Distinguishing implementation correctness, model adequacy, and uncertainty has substantial prior foundations. SVB must not present that distinction as a discovery. | We did not conduct a chapter-level comparison or show that SVB captures this field's full taxonomy. |
| Reproducibility versus replication | National Academies of Sciences, Engineering, and Medicine (2019), *Reproducibility and Replicability in Science*. [DOI:10.17226/25303](https://doi.org/10.17226/25303). Crossref metadata. | Repeating a calculation from the same data is a different activity from independent scientific corroboration. Terminology should be declared. | Reproducibility of SVB code is not proof of its labels or external validity. |
| Statistical interpretation | Wasserstein & Lazar (2016), *The ASA Statement on p-Values: Context, Process, and Purpose*. [DOI:10.1080/00031305.2016.1154108](https://doi.org/10.1080/00031305.2016.1154108). Crossref metadata. | Statistical computation and scientific interpretation are distinct evaluation targets. A p-value alone should not be treated as an effect size or a posterior truth probability. | A few textbook counterexamples are not a complete statistical reasoning benchmark. |
| Scientific problem solving | Wang et al. (2023), *SciBench: Evaluating College-Level Scientific Problem-Solving Abilities of Large Language Models*. [arXiv:2307.10635](https://arxiv.org/abs/2307.10635). Abstract inspected. | Existing benchmarks cover scientific calculations and problem solving. SVB should distinguish its evaluation of justification and missing evidence from merely adding more science questions. | No systematic item-overlap, task-difficulty, or model-performance comparison has been performed. |
| Scientific literature tasks | Wadden et al. (2024), *SciRIFF: A Resource to Enhance Language Model Instruction-Following over Scientific Literature*. [arXiv:2406.07835](https://arxiv.org/abs/2406.07835). Abstract inspected. | Literature-grounded instruction following is prior work relevant to source attribution and evidence handling. | SVB has not demonstrated superior evidence attribution or reference quality. |
| Executable scientific agents | Chen et al. (2024), *ScienceAgentBench: Toward Rigorous Assessment of Language Agents for Data-Driven Scientific Discovery*. [arXiv:2410.05080](https://arxiv.org/abs/2410.05080). Abstract inspected. | Real code execution and scientific task outcomes are already evaluated. Executability is necessary but not a novelty claim. | SVB's compact exact tasks are not equivalent to end-to-end scientific discovery or to that benchmark's scale. |
| Blind protein structure assessment | Kryshtafovych et al. (2021), *Critical assessment of methods of protein structure prediction (CASP)—Round XIV*. [DOI:10.1002/prot.26237](https://doi.org/10.1002/prot.26237). Crossref search metadata. | Blinded evaluation against independently obtained experimental targets is an established model for reducing developer access and selection effects. | SVB does not implement a CASP-style prospective competition or validate predictions of real protein structures. |
| Blind binding assessment | Parks et al. (2020), *D3R grand challenge 4: blind prediction of protein–ligand poses, affinity rankings, and relative binding free energies*. [DOI:10.1007/s10822-020-00289-y](https://doi.org/10.1007/s10822-020-00289-y). Crossref search metadata. | Pose prediction, ranking, and binding free energies are distinct targets; public blind challenges predate SVB. | A finite lattice model's exact partition function is not a D3R binding-affinity result. SVB does not claim a new binding benchmark validated against D3R targets. |

## Novelty matrix

| Candidate component | Assessment at this release | Evidence needed before a stronger claim |
|---|---|---|
| Separation of mathematical, numerical, statistical, physical, and empirical correctness | Established concepts combined into a benchmark taxonomy. | Domain-expert review and comparison against existing V&V/UQ taxonomies. |
| Explicit insufficient-evidence answers | Established epistemic and selective-prediction idea. | Test whether its operationalization changes decisions on independently adjudicated real claims. |
| Typed evidence DAG and scope non-escalation | Standard typed inference / information-flow style closure argument. The report proves a small conditional statement, with no priority claim. | A formal calculus, machine-checked implementation correspondence, and literature search in proof-carrying code, refinement types, assurance cases, provenance semirings, and causal evidence. |
| Coverage, false acceptance, Brier loss, and error outcomes | Established metrics. Keeping denominators visible is good evaluation practice. | Preregistered comparisons showing a specific failure hidden by a conventional metric on an externally collected dataset. |
| Exact independent oracles and mutation tests | Established software testing and numerical validation methods. | External reference-oracle audit and independent reproduction. |
| Freezing dataset bytes and split groups | Established benchmark hygiene. Public freeze is not hidden holdout. | An access-controlled custodian and prospective evaluation with a fresh, undisclosed set. |
| Noninvasive PCS/FoldBounds adapters | Engineering integration, not novel scientific methodology. | Broader systems and targets, independent adapter audits, and capability declarations fixed before evaluation. |
| Measuring correct calculation paired with unsupported interpretation | Potentially useful study design, not established novel research here. | A systematic novelty review, realistic independent claims, competent external systems, and evidence that conventional evaluation misses consequential failures. |

## What this release can support

The project can demonstrate that its particular executable checks distinguish
declared kinds of mistakes on its particular reference tasks, and can expose
limitations in the connected system interfaces. It cannot establish that current
scientific AI systems generally fail at scientific verification. A purpose-built
“always accept” or computation-only baseline illustrates the benchmark's behavior;
it is not evidence about a deployed AI population. A no-cost deterministic
experiment does not substitute for an actual LLM evaluation.

## Missing review before publication claims

1. Read full texts and audit cited claims; compare exact task definitions and
   source overlap rather than relying on titles and abstracts.
2. Extend the search to assurance cases and safety arguments (including GSN),
   proof-carrying code, refinement/epistemic type systems, scientific provenance,
   causal identification, conformal risk control, scientific claim verification,
   and recent scientific-agent benchmarks. This list identifies unreviewed areas,
   not literature that this release has examined.
3. Obtain independent scientific adjudication and a prospective held-out
   evaluation. The current investigators authored the cases, software, and initial
   interpretation; separate AI review does not remove this conflict.

No mathematical novelty, benchmark superiority, general scientific reliability,
or experimentally validated biological finding is claimed by this review.
