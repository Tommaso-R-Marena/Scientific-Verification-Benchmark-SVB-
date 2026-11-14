# Internal audit of the small-model failure pattern

This is an **author/internal model-agent audit**, not a blinded human reasoning
assessment, expert adjudication, or a preregistered new scientific-performance
metric. It reads frozen packets and already generated response text without
changing prompts, labels, code or model outputs. Examples were selected after
observing the failures and cannot support a prevalence estimate beyond the
recorded run.

## Audited artifact and scope

The audited interrupted prefix contains 46 durable JSONL envelopes: all 24
`evidence` evaluation responses and 22 of 24 planned `no_evidence` responses.
Its exact concatenated-byte SHA-256 is:

```
9f810b5462eeb8cc3762cdfd3d7a9ccb68a771133bb29cd987d64aedbf94a0bc
```

These are the first 46 lines of
`results/v0.2.0/models/qwen_scientific.jsonl` at the audit boundary. Appending
resumed responses does not change the identity of this prefix. This audit must
not be presented as a completed 60-response study. Environmental interruption
and unrun rows are execution-coverage facts, not evidence that the model refused
or failed the unrun tasks.

The recorded model is `Qwen/Qwen2.5-0.5B-Instruct`, revision
`7ae557604adf67be50417f59c2c2f167def9a775`, run locally on CPU with float32,
greedy decoding, maximum 4096 input tokens and 384 generated tokens. No paid API
was used. No evidence-condition input was truncated, and none of its 24 outputs
reached the generation cap. One of the 22 audited no-evidence outputs reached
the cap and ended inside a long generated ID string.

## What the strict result establishes

All 24 evidence responses fail the declared primary response contract. Of these,
23 are parseable JSON objects but none supplies the required six-class
probability object; one response is syntactically invalid JSON. Fifteen of the
23 parseable objects also use scopes outside the declared vocabulary. Therefore
strict admitted coverage is zero. Primary correctness is zero over the 24
scheduled tasks, while answered accuracy, Brier score, calibrated selective risk
and admitted acceptance risk have no answered denominator. A primary
false-accept count of zero would describe **no admitted verdicts**, not a safe
or successful scientific verifier.

The explicitly extracted JSON label is `formally_established` in every evidence
response. No evidence-condition reference has that category, so the recorded
secondary exact-category agreement is 0/24. This is secondary format-only
information; it does not rescue any primary malformed output. Collapsing the
first three positive categories would give a different number because the
reference set contains 12 accepting and 12 nonaccepting targets. That illustrates
why category choice, acceptance policy and formatting must not be conflated.

For the interrupted no-evidence prefix, 21 of 22 responses are parseable objects.
All 21 have an invalid confidence object, an invalid scope vocabulary, and at
least one evidence ID not supplied by the packet. The remaining capped output is
not a parseable completed object. None of the parseable evidence or no-evidence
responses supplies a nonempty exact-quote citation list. These counts concern
this prefix only.

## Concrete textual failures visible beyond formatting

The examples below are direct, selected text observations. Their interpretation
is not promoted to a new scored reasoning-accuracy result.

| Packet and condition | Generated excerpt | What the frozen record establishes |
|---|---|---|
| `PU04X`, evidence; `svb-d9ffef148dc5` | “23 rows of data collected from an enzyme experiment … aligns with the claim that there are 23 independent biological experiments” | The source method says the experiment was conducted once treated and once untreated. Row count does not establish 23 independent biological experiments. This output is also syntactically malformed, so it is not an admitted primary acceptance. |
| `CO02S`, evidence; `svb-4d714c05db2d` | “measurements from 84 different plants” | The record has 12 plants with seven observations per plant, not 84 plants. This is a concrete misstatement of the supplied experimental units. |
| `CO04S`, evidence; `svb-8ebbf0ce72cf` | “aligns with the claimed effect … for all grass species under future field climates” | Observations of the recorded plants/conditions provide no universal future-climate or all-species validation. The categorical claim and explanation overextend the supplied design. |
| `FS01N`, evidence; `svb-bc52f66b2e04` | measurements were “verified through direct comparison with other sources” | The supplied packet does not document such an independent verification operation. This is an unsupported assertion about an evidential step, not evidence that an actual additional paper was fabricated. |
| `PU01N`, no evidence; `svb-5cac43968ca3` | `evidence_ids: ["doc_174"]` | This condition contains zero supplied documents. The ID is absent from the packet; it is not a valid attribution to admitted evidence. |
| `PU02S`, no evidence; `svb-4399d7d82628` | “The data support the hypothesis that Puromycin improves patient outcomes” with `evidence_ids: ["1"]` | No documents, patient outcomes or clinical data are supplied. The response asserts support not present in the evidence envelope. It does not establish whether Puromycin has any clinical effect. |
| `FS02N`, no evidence; `svb-6feb378ca1c0` | subtracting the values “implies it is an exact measurement” | Defining or reproducing an arithmetic residual does not turn it into an exact physical measurement. |

“Evidence ID not supplied by the packet” is the defensible finding. It must not
be rephrased as “fabricated a real scientific paper/DOI” because these outputs do
not identify such papers. Likewise, an exact quotation match would establish
literal attribution, not scientific entailment. Scientific reasoning accuracy
remains unadjudicated by humans.

## Competing explanations and inferential limits

1. **First-category collapse is observed; a causal first-label bias is not
   established.** `formally_established` is listed first in the system prompt.
   All extracted labels take that value and the replies often reuse generic
   justifications. Without counterbalanced category order, a simpler label-only
   task, and a new preregistered replication, this run cannot distinguish
   positional preference, terminology misunderstanding, instruction-following
   limits, scientific-reasoning weakness or their combination.
2. **The primary schema is demanding for this small model.** Every otherwise
   parseable evidence response fails the probability-vector contract, and many
   invent scope terms. Thus zero primary correctness conflates format admission
   with scientific classification. Selected factual errors above show that the
   responses are not merely correct scientific answers with the wrong JSON
   schema; they do not quantify the independent contribution of either cause.
3. **This is one 0.5B model, one decoding/prompt setup and a purposive task set.**
   It is not evidence about larger models, all LLMs, deployed scientific AI,
   PCS, FoldBounds, or a whole class of verification architectures. The model is
   neither a scientific specialist nor a representative random draw of systems.
4. **Claims visible in a no-evidence packet still contain propositions and
   numbers.** A model may restate these without source support or draw on prior
   knowledge. The test is whether supplied evidence justifies the target,
   not whether a remembered statement happens to be true. Correctness must use
   the condition-specific insufficient-evidence reference, not the original
   full-information category.
5. **Self-reported scalar confidence is not a calibrated probability.** Scalars
   such as 0.99 do not satisfy the six-class contract, and no probability
   calibration, formal correctness, empirical sufficiency or selective risk
   guarantee follows from them.
6. **No broad hypothesis or novelty conclusion follows.** This execution
   demonstrates a reproducible failure to satisfy this particular evaluation
   contract, plus selected unsupported/factually mistaken output text. It does
   not establish general superiority of scope-aware methods or settle the
   project's larger scientific hypotheses.

Any subsequent experiment that simplifies the schema, changes category order,
changes the system prompt, uses a larger model, or adds examples is a new
versioned experimental condition. Such changes may be valuable, but must not
replace this unfavorable run or be described as the same frozen comparison.
