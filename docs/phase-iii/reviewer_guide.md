# SVB scientific review pilot: reviewer guide

This is a request to examine scientific claims and the categories used to assess
them. Materials are prepared only; no reviews or successful blinding are claimed.
You may challenge the question, evidence envelope, categories or provisional
interpretation. You are not asked to endorse SVB or a system's scientific value.

## Before starting

A coordinator should confirm consent, relevant expertise, conflicts and your
assigned packet IDs. Use an anonymous reviewer code. Personal identity, private
correspondence and consent records stay outside the public repository. Declare
source familiarity, exposure to public SVB answers, and any inferred candidate
identity. Public cases and labels are reconstructable; do not assume secrecy.
Scientific source identities are deliberately visible.

Use `reference_review.zip` and the separately supplied `source_materials.zip`
first. Verify the source-bundle hash in `source_bundle.json`. Source snapshots
retain their own licensing; archived R code is reading material, not instructions
to execute. The archive may lack primary experimental methods. Flag missing
methods rather than certifying unseen laboratory work. Treat the supplied record
as the fixed evidence envelope. Log outside sources/tools separately; evidence
found elsewhere may motivate a new packet, not silently change this one.

## Round 1: independent reference judgments

Work independently, before discussion and before seeing candidate responses.
For each assigned packet:

1. Identify the exact target and its population/system, conditions, units and
   quantifier. Separate an archived observation from population, causal or
   mechanistic inference. State any ambiguity in the target.
2. Give a short scientific rationale, a supplied document ID and an exact locator
   (row, table, paragraph or reproducible calculation). A quotation is optional;
   if supplied it must be exact. State missing assumptions and uncertainty.
3. Choose the evidence relation: `support_only`, `opposition_only`, `both`, or
   `neither`. These describe arguments admitted for this exact target, not
   absolute truth. If no responsible judgment is possible, use
   `assessment_status: unable_to_assess`, `not_assessable` dimensions and explain.
4. Select every defensible historical category. Mark whether there is a single
   defensible category, several simultaneously applicable categories, alternative
   target interpretations, or no category that fits. Do not confuse several
   applicable evidence types with uncertainty about which single answer is true.
5. Propose retain, clarification, correction, preserved ambiguity or exclusion.
   Distinguish a suspected reference error from ambiguous categories, incomplete
   sources or irreconcilable interpretation. You need not force agreement.

Historical category meanings:

| Category | Intended historical meaning, open to challenge |
|---|---|
| `formally_established` | Mathematical proposition follows from explicit assumptions |
| `computationally_established` | Specified finite calculation is correct for supplied inputs |
| `empirically_supported` | Observations support a narrowly scoped conclusion under recorded conditions |
| `refuted` | Supplied evidence sufficiently contradicts the exact target |
| `insufficient_evidence` | Supplied record establishes neither acceptance nor refutation |
| `disputed_or_unresolved` | Record explicitly documents an unsettled or disputed research question |

A table fact can be supported by both calculation and observation. A formal
result can be computationally checked. A documented dispute may contain support,
opposition, both, or neither under the present envelope. Do not treat these
possible overlaps as reviewer errors. The proposed separate dimensions are
experimental and may themselves be unsuitable; propose alternatives freely.

## Forms and time

`response_form.md` is a short worksheet. `blank_response.json` is the ingestion
format with twelve blank entries. Fill only assigned entries; remove unassigned
entries. Blank forms are intentionally invalid submissions until completed.
`legacy_labels` is a list, not a probability distribution. Reviewer uncertainty
is low/moderate/high/not_assessable, not a calibrated probability of scientific
truth. Specify its reason. `issues` may contain taxonomy_overlap, ambiguous_target,
reference_error_suspected, source_incomplete or irreconcilable_interpretation.
Use an empty list if none applies. Completed judgments require a source citation.

A coordinator may transcribe a completed worksheet to JSON, retain the original,
and ask you to verify the transcription. Such transcription must not invent
ratings or rationales. Record tools and outside research under
`tools_and_external_sources`. If necessary source material is absent, reporting
that gap is a legitimate outcome. Planning estimate: 15–30 minutes per assigned
reference packet, plus orientation and any primary-method retrieval. Record
actual work separately; no estimate is a commitment.

## Candidate review: separate stage

The coordinator releases `candidate_review.zip` only after first-round reference
records are locked. It contains twelve retained raw explanations for six cases,
with anonymous candidate codes. Read each against its packet. Assess stated
reasoning, source attribution, scope and uncertainty separately; give specific
citations and a rationale. No verdict was requested in this explanation task.
Do not infer private internal reasoning faithfulness. Missing source IDs, a
correct limitation and an incorrect preceding assertion can coexist. Do not
repair or finish a candidate's text before judging it. Register prior identity
cues rather than assuming the masking worked.

## Optional round 2

Discuss differences only after immutable first-round forms are stored. Submit a
new round-two form linked by `prior_form_sha256`, the SHA-256 of the canonical
JSON content of the first form (sorted keys, compact separators, UTF-8; the
coordinator's ingestion utility reports it). Preserve original judgments and
explain changes. Agreement is not required; no automated majority vote produces
a scientific reference. External findings or corrected packets require separately
versioned evidence and explicit re-review.
