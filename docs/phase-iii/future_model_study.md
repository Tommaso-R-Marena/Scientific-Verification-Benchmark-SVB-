# Future stronger-model study: design only

No new model download, inference, paid service, GPU allocation or confidential
holdout is created by this specification. This is a planning document, not a
frozen final experiment or a claim that a stronger comparison has happened.
Actual human taxonomy/reference adjudication should precede final task choice.

## Prerequisites and stop conditions

1. Independent domain/methods reviewers qualify the exact claims, evidence
   envelopes and proposed axes, preserving disagreement and none-fit cases.
   Freeze a new task/rubric after the pilot; do not assume version-0.4 proposal
   is already validated. Scientific errors are meaningful negative outcomes.
2. Define an explicit target population of scientific tasks and a source-family
   sampling procedure. Historical public cases are development only. A final
   sample size and any inferential procedure need justified family-level
   variability/effect assumptions; no power calculation can be invented before
   those inputs exist.
3. Arrange a genuinely independent custodian with access control outside the
   developer/agent workspace, then audit it. If unavailable, run a disclosed
   public reproducibility study and abandon hidden/blinded claims.
4. Confirm resources, model licenses and human review time. Do not incur paid
   inference or use private credentials without separate authorization. If
   qualification or resource profiling fails, stop before the expensive sweep,
   retain failures, and issue a new protocol if a design changes.

## Models and interface qualification

Target at least three independently developed model families and, where feasible,
a capacity contrast within one family. Illustrative candidates include public
7–9B instruction checkpoints from Qwen, Mistral and Gemma families, subject to
actual licensing/access/resource checks. These are examples, not selected
versions; no availability, exact license or performance is assumed. Gated or
custom-license checkpoints require a verified permitted-use decision before
access. Record exact repository/revision, tokenizer/config/weight hashes,
quantization/backend and release date. A generic model name is insufficient.

Use independently reviewed development material only:

- Twenty-four non-scientific format/instruction controls with known outputs,
  including ordinary evidence-access and target-versus-component instructions.
  Require at least 23/24 exact minimal-format admissions and 22/24 simple
  instruction-target responses. These are prespecified operational gates, not
  confidence bounds on scientific reliability.
- Repeat those controls with reversed/permuted response enumeration and neutral
  equivalent wording; require at least 23/24 stable *target evidence relations*.
  Evidence-type attribution is a separate dimension, avoiding the historical
  gate's conflation. Record any type instability rather than merging it silently.
- Run a separately adjudicated scientific development panel to expose weak
  reasoning, class imbalance and scope errors. Do not require high scientific
  accuracy as a condition of reporting an interface-qualified model: systematic
  inappropriate acceptance would be a valuable negative result. No final cases
  may influence prompt selection or thresholds.
- Retain every failed candidate and its denominators. If all candidates fail
  interface qualification, do not claim a representative scientific comparison.

If a decoding constraint is used, declare its grammar, legal strings, stopping
rule and backend. Compare constrained/unconstrained runs separately. A constraint
must not encode the reference or repair text. Keep instruction content/order
identical when estimating a format intervention; a rich task with different
instructions remains a different treatment bundle.

## Resource profiling before scientific inference

For P parameters, raw weight storage is approximately 4P bytes at float32, 2P
at bf16/fp16, P at 8-bit or P/2 at 4-bit, before quantization metadata, KV cache,
activations, loading copies and framework overhead. A 7B float32 checkpoint
therefore needs roughly 28 GB for weights alone; the earlier ~33 GiB host may
not safely fit the whole run. Low-bit storage is not a guarantee of RAM fit,
backend correctness or comparable accuracy. CPU latency must be measured, not
extrapolated from parameter count alone.

Profile loading, peak RSS/device memory, 4k and intended maximum input lengths,
short verdicts and a capped explanation on independent controls. Use batch one
initially. Record measured tokens/second and estimate total requests×tokens/time
plus loading and adjudication effort. A local 24 GB GPU might fit some 7–9B
lower-precision configurations, but no hardware or permission is assumed. A
coordinator must approve an actual resource/time cap before execution. Model
identity checks and short development profiling are separate from a final scored
run. Quantized and unquantized results are different model/backend conditions.

## Independent custody and exposure

A custodian independent of the evaluated-system developers selects new source
families and atomic targets after model/version selection, arranges independent
scientific review and stores evaluation packets/labels in a separately governed
private location. Developers and authoring agents must not be able to read them.
An audited access log and signed protocol/content commitment establish timing;
public hashes, public-key encryption alone, untracked files or prompt omissions
do not establish confidentiality or independence.

Record who could access packets, source familiarity, model pretraining cutoff
where documented, previous prompt exposure, endpoint retention/training policy,
operator changes and any breach. Public source articles may still be in model
training; private new target construction reduces one exposure path but does
not prove source novelty. The custodian assembles prompts containing only
legitimate scientific information and runs a data-only model interface, without
allowing arbitrary developer submissions to execute. References remain outside
model/tool context. Tools receive only authorized evidence/data; no hidden oracle
or reviewer reasoning is exposed.

Release evaluation artifacts for reproducibility after the embargo and permitted
consents, at which point they cease to be protected tests for later experiments.
If access conditions fail, retain the run but label it exposed; never retroactively
call it hidden or independently blinded.

## Conditions and analyses to freeze before final execution

Use the same independently adjudicated targets across model conditions: supplied
evidence, documents withheld, verification assistance, and explicitly disclosed
assumptions where scientifically meaningful. Each condition requires its own
reference envelope. Do not remove information yet score against inaccessible
full-information answers. Verification tools may return exact arithmetic or
proof scope, never a reference conclusion. Freeze prompts, ordering/paraphrases,
tool budgets, sampling parameters, output caps, retries/failure policy and model
identities before the custodian opens final evaluation.

Primary analyses should keep these distinct:

- Evidence-relation correctness and inappropriate acceptance under the exact
  target, with definite versus ambiguous references separated.
- Supported narrow-claim acceptance and stronger-claim rejection in the same pair.
- Item and study-family outcomes, paired within-model condition differences and
  macro summaries over a defined family sample. Keep all scheduled missing,
  malformed, timed-out and unsupported outcomes visible.
- Stated reasoning/source entailment and uncertainty judged by independent humans,
  including meaningful disagreements. IDs/quotes alone are syntax diagnostics.
- Coverage, committed-decision risk and abstention, plus output/tool/time cost.
  Calibrated probabilities require a separately qualified elicitation interface
  and proper scoring on a justified target, not a verdict string.
- Scientifically irrelevant paraphrase/row-order controls, source-length and
  meaningful unit/assumption/evidence changes. Specify expected invariance or
  justified change before seeing outputs.

Do not pool fundamental capability differences into a leaderboard. No optional
stopping after a favorable result, post-result case exclusion, metric selection
or reference changes without an explicit deviation/erratum. Inferential intervals,
if justified by the source sampling plan and sufficient independent families,
should treat the study family as a cluster. Repeated items, modes, thresholds and
reviewer pairs do not multiply independent n. With few purposive families, use
descriptive outcomes and no population significance claim. Comparisons between
model families or sizes do not automatically identify causal effects.
