# Separating verdict reliability, explanation validity and protocol compliance in SVB

Phase IIb manuscript continuation. Internal research draft; no external human
adjudication, peer review, independently protected evaluation or general
scientific-AI ranking is claimed. Earlier manuscripts remain unchanged.

## Abstract

A scientific-verification benchmark can confuse inability to satisfy a response
schema with inability to assess evidence. SVB Phase II yielded no admissible
rich-schema outputs in its primary small-model experiment. We preserve that
negative result and freeze a new diagnostic protocol separating minimal
six-category verdicts (A), brief explanations and attribution (B), and the
historical rich verification contract (C). Development qualification used 75
actual requests across three pinned public Qwen2.5-Instruct sizes. All candidates
failed at least one unchanged gate. A subsequent diagnostic comparison used
120 actual requests across the original 0.5B and 1.5B checkpoints on 12 paired
public-source cases from three additional studies. Both models admitted 12/12
evidence-present A outputs, with exact provisional-reference agreement 2/12 and
6/12 and inappropriate acceptance 1/6 and 2/6. Neither admitted any of six
matched C responses. Constrained decoding ensured category syntax but did not
improve coarse correctness. Separate prose outputs contained unsupported
attribution and contradictory assertions; reasoning validity remains unscored
pending human review. An independent small FoldBounds study found 32 valid
enclosures but large configuration differences in threshold-decision usefulness.
The contribution is an auditable separation of observable failure types and an
external-review package, rather than a validated instrument or superiority claim.

## Motivation and established foundations

Scientific claims depend on calculation, measurement, design and scope; one
validated component does not establish the others. Evidence-linked fact checking
(SciFact/FEVER), attribution evaluation (ALCE), scientific agent evaluations,
formal verification, and selective prediction already address important parts
of this problem. The preserved Phase II related-work review and the targeted
Phase IIb [methodology audit](methodology_audit.md) locate SVB among these
approaches. Work by Turpin et al. and Lanham et al. also cautions that plausible
explanations do not establish faithfulness to internal computation. No novelty
is claimed for typed evidence dependencies, proper scoring, interval reasoning,
selective decisions or ordinary uncertainty propagation.

The strongest current SVB contribution is a reproducible diagnostic framework
that keeps numerical checks, justified scope, interface qualification and
scientific adjudication distinct, with failures retained. Whether these
measurements add practically important information beyond strong existing
benchmarks and verifiers is an open comparative research question.

## Methods

The versioned protocol freezes code, source bytes, labels, model identities,
prompts, parameters and scheduled denominators before new-source generation.
Qualification controls use authored instructions and historical public material;
new study families appear only in the final diagnostic comparison. The
six-category taxonomy is preserved; exact agreement is reported alongside
coarse acceptance because empirical and computational descriptions can overlap.
No response is repaired or retried for correctness.

Twelve items form six scientifically meaningful pairs across paired historical
sleep observations, chick growth and biochemical oxygen demand. Each pair shares
evidence while changing a numerical claim or the scope of an inference. Nine
exact reference witnesses recompute from archived source data. The public R
transcriptions carry provenance and licensing, but do not replicate primary
laboratory methods. All scientific labels are provisionally author-adjudicated.

Each selected model receives A with and without documents, plus B and C on six
source-balanced cases. A separate category-trie constraint is compared with
unconstrained A. B asks for a public scientific justification and source IDs,
not private internal reasoning. Its automatic checks describe prose, word
limits, attribution syntax and truncation; they do not grade scientific validity.
C retains the original strict scorer. All outcomes are reported by item and
study family, without treating correlated items as independent experiments.

See [specification](specification.md) and [reproduction](reproduce.md) for pinned
identities, request counts, hashes, resources, strict admission and conditions.
The selected 0.5B/1.5B weights are Apache-2.0; the development-only 3B checkpoint
has a noncommercial research license. No paid inference is used.

## Results

All three candidates fail the prespecified A gate, particularly order stability
(3/6, 3/6 and 2/6). Thus final measurements characterize diagnostic behavior of
the two originally selected sizes, not qualified scientific-system performance.

Both final models produce legal A categories on all evidence-present cases.
Exact agreement is 2/12 and 6/12; coarse acceptance agreement is also 2/12 and
6/12. False acceptance occurs on 1/6 and 2/6 nonaccepted reference cases. The
latter includes a factor-1000 oxygen-demand unit error and an unsupported
universal treatment claim. The 0.5B model also explicitly rejects two supported
cases, and the 1.5B model one. Both-correct pair counts are 0/6 and 1/6. Family
strata and every prediction appear in the executed report and raw artifacts.

With documents withheld, 0.5B admits 9/12 with no correct insufficiency verdicts;
1.5B admits 12/12 with 7/12 correct insufficiency verdicts. Supported-case
acceptance followed by appropriate insufficiency after withdrawal occurs on
0/6 and 1/6 cases. A constraint legalizes all categories but does not improve
coarse correctness or inappropriate acceptance. It changes decoding, so exact
category shifts cannot be called output repair or pure scientific improvement.

All six B outputs per model contain nonempty prose but none supplies requested
bracketed source IDs. Five 1.5B responses exceed 80 words and one reaches the
generation cap. Internal examples include attributing an unsupported mechanism
to the source and asserting causation before denying it. No human reasoning
accuracy or source-entailment score is reported. Both models admit 0/6 C outputs;
all generators completed, but all rich outputs are malformed. A/C differs in
instruction order and length as well as schema; it does not isolate a causal
schema-complexity effect.

The unchanged lexical baseline gives 3/12 exact agreement and 5/6 false accepts
with documents. The unchanged numerical baseline supports none of these packet
forms. These limited baselines do not establish superiority over modern
scientific methods.

A separate frozen 32-call FoldBounds analysis finds valid exact-reference
enclosures throughout, yet shallow/moderate configurations decide 0/36 selected
nontrivial interior thresholds, enriched 34/36 and full enumeration 36/36.
There are no wrong definite decisions among 248 related threshold observations.
For these tiny models, full enumeration is cheaper in median wall time than the
enriched setting. Correct enclosure, useful decision coverage and computational
cost are empirically distinct. The elementary decision-safety result assumes
valid mathematical bounds and says nothing about physical model adequacy.

## Interpretation and limitations

Minimal A removes total rich-schema failure as the sole explanation of the
observed categorical outcomes. Specific inappropriate acceptances are now
measurable. The remaining mix of instruction following, category interpretation,
evidence recognition and scientific reasoning is not fully disentangled.
Failed qualification gates, one model family, only three source clusters,
source-category ambiguity, public exposure and absent independent human review
prevent a representative scientific-capability ranking.

The public corpus cannot establish hidden testing or guaranteed source novelty.
A frozen protocol detects changes but does not supply independent custody.
Source curation and exact arithmetic do not validate original measurements or
missing primary methods. A source-complete package of 44 packets and 132 blank
forms, plus raw candidate B packages, is ready for a coordinator; zero reviews
have been completed and no experts contacted. External adjudication should
preserve alternative admissible labels and disagreement rather than force a
unique answer where evidence types overlap.

The broad hypotheses remain open: conventional QA concealment needs a matched
QA comparison; added scope-detection value needs strong external baselines;
verification-assistance effects and dependency-representation benefits require
controlled experiments. Publication-quality validation also needs qualified
stronger systems, diverse primary sources, independent exposure controls,
claim-level human evaluation and more independent study families. Present
findings justify an improved diagnostic interface and concrete observed failure
examples, not novel scientific discoveries, mathematical novelty, broad model
reliability or benchmark superiority.
