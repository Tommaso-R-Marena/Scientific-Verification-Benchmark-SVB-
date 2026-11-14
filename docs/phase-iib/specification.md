# Phase IIb specification: protocol/data 0.3.0

Phase IIb is an additive diagnostic experiment. The frozen Phase I/II protocols,
labels, implementations, raw outputs and unsuccessful outcomes remain historical
artifacts. The continuation uses the same draft PR, without a release-tag update
or merge. Python-package version 0.2 is unchanged; 0.3 denotes these data and
experimental protocols.

## Freeze and exposure

`data/v0.3.0/manifest.json` has SHA-256
`d87f519ccfe72490737779059fc73f5402fac5780a55d06f8adbd7f50d7119d5`.
It binds the protocol, source cases and registry, development qualification,
model identity records, final plan, prompt bytes, evaluator and runner before
the first new-source generation. This is an internal freeze, not an independently
registered protocol. The public repository exposes reference answers to its
authors, agents and other readers. Evaluation prompts omit them; this provides
prompt isolation, not a hidden benchmark or guaranteed absence from pretraining.

Development uses six author-defined or historical public controls. The new study
families are absent from those controls. All original public evaluation items
are historical/development material for Phase IIb. The final 12 items form six
pairs across three additional studies; related items are not independent samples.
All source transcriptions come through R's public distribution. Different
studies do not establish independence of source providers or curation pipelines.

## Three tasks and denominators

| Task | Requested output | Automatic qualification | Scientific scoring |
|---|---|---|---|
| A | One existing category string | Whitespace trimming, then exact equality to one of six labels | Exact taxonomy agreement, coarse accepted-group agreement, false acceptance, explicit false rejection, insufficiency and paired/family analysis |
| B | At most 80 words of prose with bracketed source IDs | Nonempty completion, word budget, JSON-like indicator, ID consistency, output-cap flag | Reasoning validity, source entailment and uncertainty adequacy await independent humans |
| C | Original rich response schema | Original Phase II strict schema/scorer, unchanged | Original strict categorical/scoped metrics; no repair or extracted-label replacement |

A's labels are `formally_established`, `computationally_established`,
`empirically_supported`, `refuted`, `insufficient_evidence`, and
`disputed_or_unresolved`. Computational and empirical categories can overlap
for observed-table properties. Exact taxonomy and coarse acceptance are therefore
reported separately. Coarse agreement merges only the three accepted categories;
it never merges rejection with insufficiency. Explicit false rejection means
`refuted` on an accepted reference; abstention is reported separately.

Each selected model has 36 unconstrained requests: 12 A with documents, the same
12 A without documents, six B with documents, and six C with documents. A separate
24-request constrained run repeats both A conditions. The six B/C cases are the
narrow/stronger pair from each study, fixed in `evaluation_plan.json`. Thus the
matched A/C comparison uses six cases, not all 12 A cases. There are no scheduled
B/C requests without documents. Missing, failed, unsupported and malformed
scheduled executions retain their denominators.

Document withdrawal removes only source documents. Claims, methodology and
naturally disclosed assumptions remain; the condition tests justification from
that remaining supplied record, not whether a pretrained model remembers an
external source. All withdrawn-document reference categories are provisionally
`insufficient_evidence`. This deliberately imbalanced condition cannot establish
broad classification competence on its own.

## Controls and interventions

Development reverses both label enumeration and definitions; alternative wording
is tested separately. Final A order is rotated by pair using the frozen seed.
Both members of a pair share an order. First-label positions are counterbalanced;
reference label positions are not exactly balanced. Small scientifically
meaningful claim changes share identical source evidence. Final-set paraphrase
robustness, verification assistance, and assumption-withholding were not run.

The optional A constraint is a six-category token trie plus EOS, containing no
item reference. It changes decoding and can change the selected category; it is
an explicit interface intervention rather than output repair or guaranteed
scientific improvement. C preserves its historical prompt, ordering and length.
Matched A/C differences therefore do not identify a causal effect of schema
complexity alone.

All models use public, pinned weights, offline CPU inference, float32, eager
attention, four threads, greedy decoding, seed zero and input cap 4096. Output
caps are A24, B128 and C384. No input is silently truncated. Raw completions,
execution statuses, caps, identity and prompt hashes are retained. The runner
loads no references and does not execute generated content. Scoring raw data is
stdlib-only; optional inference dependencies and model licenses are separate.

## Qualification and interpretation

The unchanged development gate requires A syntax at least 5/6, exact category
agreement at least 4/6, and standard/reversed-order consistency at least 4/6.
No candidate passes all three gates. The original 0.5B and 1.5B models remain a
prespecified diagnostic comparison; the bounded 3B extension remains development
only. No gate was relaxed, no model was selected using new-source outcomes, and
no output was retried because its answer was wrong.

The experiment can identify observable scientific errors conditional on the
supplied record and provisional reference judgments. It cannot establish a
validated scientific-AI ranking, independent generalization, expert agreement,
calibration from category-only answers, a pure parameter-count effect, or
superiority over other scientific benchmarks. Threshold-bound utility is a
separate model-relative study, described in `bound_utility.md`.
