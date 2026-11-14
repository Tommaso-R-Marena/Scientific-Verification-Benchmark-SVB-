# External scientific review brief — preparation only

**No reviewers have been contacted or recruited, and no external human ratings
or expert approvals exist.** This package is ready for a coordinator to inspect
and distribute only after separate authorization, consent, conflict checks,
appropriate compensation/ethics arrangements, and source-rights review. It does
not publish the benchmark or ask anyone to approve it automatically.

## Purpose and boundaries

Review whether the supplied scientific record justifies each exact claim,
including whether a narrow arithmetic/source fact has been confused with a
population, causal, mechanistic, or physical conclusion. Determine where the
six exclusive support categories themselves are ambiguous. A scientifically
legitimate outcome is disagreement, insufficient evidence, a proposed narrower
claim, multiple defensible categories, or a request for better sources—not a
forced gold label.

The prepared distribution contains **all 32 historical items and all 12 new
items**, rather than exposing only eleven author-labeled empirical positives.
Selecting only that positive subset would leak the intended category. Historical
items are exposed development/audit material; new items are public and are not a
secret held-out set. Field omission and opaque IDs support administration but
cannot prove blinding or prevent access to public labels.

The coordinator has a separate internal mapping and may prioritize category
ambiguity and scientific-source gaps without disclosing provisional labels or
model identities to reviewers. Do not give raters an internal audit that lists
the author gold before they lock first-round judgments. If they already know
public labels or the subset selection rule, record that exposure and do not
describe them as reference-blind.

## Required expertise and priorities

Every item requires two independent domain scientists and a statistical reviewer.
The same person may cover multiple compatible topics, but no reviewer assesses
an item they authored or a system they helped develop. Reviewers state actual
expertise, source familiarity, conflicts, benchmark exposure, and tool use.

| Source area | Expertise needed | Questions requiring particular care |
|---|---|---|
| Hydration thermodynamics/FreeSolv | Physical chemistry, solvation measurements, computational chemistry, measurement uncertainty | What quantity and standard-state/model context is represented? Are values physical measurements, calculated estimates, database transcriptions, or displayed equalities? What does an assigned uncertainty mean? |
| Puromycin enzyme rates | Enzyme kinetics/biochemistry and assay biostatistics | What are experimental units and replicates? What is counted, and in which units? Which inference is descriptive, mechanistic, or population-level, and what information is missing? |
| Repeated plant CO2 uptake | Ecophysiology, repeated-measures analysis, experimental design | Do rows identify distinct plants or repeated measurements? What concentration/uptake scales and treatment context are actually documented? What extrapolation is justified? |
| Penguin ecology/classification | Field ecology, longitudinal identity, classification evaluation, missing-data statistics | What is the observational sampling window/population? Are repeated IDs verified animal identities? Is a reported accuracy merely transcribed or independently reproduced? |
| Sleep observations | Paired/crossover clinical or physiological statistics | What is paired, what is independent, and what design/uncertainty information is supplied? Are sample and population conclusions separated? |
| Chick weight trajectories | Animal nutrition, longitudinal analysis, missingness/attrition | What is the experimental unit and longitudinal linkage? Do growth, diet, timing, dropout, and generalization claims require assumptions not in the record? |
| Biochemical oxygen demand | Environmental chemistry, assay interpretation, time-course/measurement uncertainty | What do time and demand measurements quantify? Which interpolation, monotonicity, mechanistic, or extrapolation statements follow from the actual observations? |

These are neutral source-family prompts, not per-case answer hints. Apply the
same core questions below to **every** item. A specialist may reject a premise
or flag an incomplete source; neither action should be penalized for disagreeing
with the benchmark author.

## Core questions for each case

1. What exactly is asserted: archive identity/transcription, arithmetic, a
   measured sample fact, a population statement, or a causal/mechanistic claim?
2. Which supplied source passage or reproducible calculation bears on that
   target? Does it actually support, contradict, or leave it unresolved?
3. What are the experimental units, repetitions, units, sampling/design,
   measurement precision, numerical approximation, and relevant uncertainties?
4. Which assumptions bridge the evidence to the conclusion? Are they stated,
   scientifically defensible, and supported at this scope?
5. Which of the six categories are defensible, if any? Could more than one be
   appropriate because the question mixes evidence types? Explain rather than
   forcing an exclusive label.
6. What is the strongest justified narrower statement, and what additional
   evidence would change the judgment? Is the difficulty scientific uncertainty,
   source incompleteness, wording ambiguity, or a correctable reference error?

For actual candidate justifications, separately judge factual/calculation
accuracy, source entailment, scope, and uncertainty. Literal quote/ID checks and
writing quality are not semantic evidence. Minimal-verdict A outputs do not
contain requested reasoning; mark explanation criteria not assessed rather than
inventing a rationale. B prose is an externally checkable explanation, not proof
of internal chain-of-thought faithfulness. C schema compliance is separate.

## Process and effort estimate

The first pass is independent. Reviewers receive source-complete packets,
blank forms, a common rubric, and conflict/exposure declarations, with no author
reference, model identity, correctness aggregate, or expected answer. They lock
first-round labels, permissible alternatives, evidence locators, calculations,
rationales, and uncertainty before discussion. Reviewers may ask for the original
primary source; missing full methods must remain a recorded limitation. A
supplementary external search is logged separately and does not silently change
the original evidence envelope.

Planning estimates—not measured work or quoted fees—are 15–25 minutes per item
per domain reviewer and 10–20 minutes per statistical review for an initial
pass. Across 44 items this is about 22–37 domain-review hours plus 7–15 statistical
hours, before source orientation, document retrieval, and disagreement meetings.
Seven source areas may require approximately 0.5–1 hour of orientation per
reviewer per relevant area. Some ambiguous physical-chemistry or source-method
items can take substantially longer. An internal detailed audit estimates
20–40 minutes for particularly important historical cases; that is not a
guarantee that a complete external review fits a fixed time budget.

Human assessment of candidate outputs adds separate work proportional to the
number and length of actual answers. Do not multiply the case-review estimate
by every model/run without a staffing plan. A coordinator may stage workload,
but the full set and source mix must remain visible and any selection policy
disclosed to the eventual analysis. No expert time, compensation, or completion
has been claimed here.

Disagreements are classified and retained before any moderated discussion.
Second-round amendments are new records. Do not manufacture consensus through a
majority vote, privilege a benchmark author, or drop difficult cases to improve a
score. An item can remain ambiguous/unscored, request revision, or retain an
insufficiency judgment. External suggestions never silently modify the immutable
historical labels.

## Package and return records

`scripts/build_phase2b_review.py` prepares a fresh project-local directory with a
reviewer ZIP and its hash manifest, source records/artifacts, anonymous packets,
blank reviewer forms, and exposure/conflict declarations. Administrative mapping
stays in a separate `internal/` directory, excluded from the reviewer ZIP.
Neither location is a security boundary in this public shared workspace.

The materialized source-complete preparation is
`data/v0.3.0/review/prepared_v1/reviewer_package.zip`: 44 scientific packets,
132 blank role-specific first-round forms, source artifacts/rights records,
rubric, conflict/exposure declaration, and a per-file hash manifest (39 ZIP
members; 731,253 bytes). Its SHA-256 is
`b5f1a13e05eaea64e91ea03c961645909fd546a8548eaaa3f5d45e430a8c9c5f`.
All case/registry input hashes matched at preparation; a second run produced a
byte-identical ZIP. Eleven packet/preparation tests passed. These are software
and packaging checks, not human review or scientific reference validation.

Reproduce to a **fresh** project-local directory:

```sh
python3 -B scripts/build_phase2b_review.py \
  --output results/local/new-external-review-preparation
```

When actual raw candidate records are available, add `--responses PATH` and
`--candidate-task A`, `B`, or `C`, plus `--candidate-condition evidence` or
`no_evidence`. Only matching task/condition records enter the candidate view;
absent candidates remain explicit, raw prose is not repaired, and provider,
model, score, latency and token envelope fields are omitted. Such a candidate
package is a separate preparation with its own ZIP hash. First-round reference
qualification should not show model answers.

The coordinator must inspect the ZIP for source completeness, rights,
confidentiality, model-identifying prose, and label leakage before external
distribution. A candidate's exact text is preserved; it is not automatically
rewritten to hide identity. Redactions require a separate logged audit that
does not alter scientific meaning. Scientific source identities remain visible
because provenance and method context are essential.

Returned records use reviewer codes, packet/content hashes, expertise/conflict
declarations, first-round and later judgments, reasons, citations, and the
reviewer's uncertainty. Consent-governed personal information and private
correspondence stay outside public artifacts. Publish only authorized redacted
records. Zero human review is the current fact, and a generated packet or two
agreeing AI critiques must not be described as independent expert validation.
