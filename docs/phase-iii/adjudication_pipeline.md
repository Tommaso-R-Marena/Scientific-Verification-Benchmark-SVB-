# Human-review ingestion and descriptive analysis

The implementation accepts data, never executable submissions. No actual human
ratings exist or were ingested during Phase III. Tests use conspicuously marked
software fixtures; production rejects their origin. These fixtures verify
software behavior and are not reference judgments or agreement evidence.

## Preparation and activation

The pilot directory contains a public coordinator context (packet/candidate
content hashes and source-family strata), a blank registry template, separate
reference/candidate ZIPs, and a shared source ZIP. Coordinator context and
selection mappings are excluded from reviewer ZIPs. Public access to those
files still makes identities and references reconstructable; no secrecy or
successful blinding is claimed.

The blank registry intentionally fails ingestion until an authorized human
coordinator completes it. Copy one reviewer row per actual anonymous reviewer:
set role to domain/methods/formal, fill reference packet IDs and candidate IDs
assigned, and attest genuine human origin, checked credentials, independence and
consent. Set coordinator_attestation true only after those checks. Never infer
these facts from a model-generated form. No personal names or contact details
belong in public code or the anonymous forms. Two assigned domain reviewers plus
one methods reviewer per packet are planned, with formal supplementation where
needed. The analysis reports unassigned minimum role slots rather than pretending
a partial registry completes the panel.

Copy the blank response from the relevant ZIP and fill assigned entries only.
Submit completed or unable_to_assess entries; omit unreviewed assignments so
missingness remains visible. Add a human attestation and exposure/conflict and
expertise declarations. The reviewer can return the worksheet for verified
coordinator transcription; retain original source records. Additional outside
sources/tools are logged separately and do not expand the frozen envelope.

## Production command

Keep registry and real submissions private, outside the repository or under
ignored `results/local/`. For example:

```sh
export PYTHONPATH="$PWD/src"
export PYTHONDONTWRITEBYTECODE=1
python3 -m svb.adjudication \
  --context data/v0.4.0/pilot/coordinator_context.json \
  --registry results/local/actual-review/registry.json \
  --forms results/local/actual-review/reviewer-a.json results/local/actual-review/reviewer-b.json \
  --output results/local/actual-review/analysis-1.json
```

Those actual-review paths are placeholders, not fabricated supplied reviews.
The output refuses overwrite. Inside SVB it can only be written under ignored
results/local; outside SVB a new private path is permitted. This reduces accidental
publication, not access control. Authorization and consent are still needed to
publish any human records. The summary retains validated forms/rationales for
traceability and is consequently private too.

Validation checks exact fields, bounded strict JSON (duplicate keys and nonfinite
numbers rejected), enums and types, registered anonymous identities/assignments,
packet and candidate hashes, independent first-round declarations, provenance
attestations, supplied evidence IDs and exact quoted substrings. Completed
judgments require a scientific rationale and source locator. An optional quotation
must be literal; a correct ID/quote does not prove the source entails the claim.
Missing assumptions, reviewer uncertainty, proposed revisions and alternative
categories are retained. Simultaneous applicability and alternative target
interpretations are distinct values. None-fit is distinct from unassessable.

Candidate review requires a coordinator-attested reference-round-one lock. This
is a procedural attestation, not cryptographic evidence that independent human
work happened. Input-file hashes and canonical form digests are retained. Round
two must link a supplied immutable first-round canonical content digest from the
same reviewer/stage and cannot add cases lacking a first-round response. First
rounds remain available; no score or gold is overwritten.

## Agreement and denominators

All measures are descriptive for this purposive pilot. The sample is twelve
related claims in five study families, with repeated reviewers and paired items;
it does not support iid intervals or population scientific-reliability claims.

| Measure | Definition and denominator | Main limitation |
|---|---|---|
| Coverage | Registered assigned, submitted, completed, unable-to-assess and missing counts separately, by stage/round | Unrecruited panel slots are reported separately; optional round-two absence is not a first-round failure |
| Exact set agreement | Fraction of jointly completed items with identical admissible-label sets | Both none-fit empty sets agree about category inadequacy; not proof of correct science |
| Mean Jaccard | Mean of intersection/union over jointly completed nonempty unions | Empty unions excluded with a count; no chance correction, and shared broad sets can score well |
| Singleton-only Cohen κ | (P_o−P_e)/(1−P_e), where P_e is the product-marginal chance term, using only both-single-defensible items | Selects away multi-category ambiguity; exclusion n is explicit; marginal/prevalence sensitive |
| Category-relation κ | Nominal κ on single/simultaneous/alternative/none-fit judgments | Agreement on “ambiguous” is not agreement on a scientific answer |
| Evidence-relation κ | Nominal κ on support/opposition/neither/both among jointly completed items | Depends on common target interpretation and admission policy |
| Candidate dimensions | Separate nominal κ for reasoning, attribution, scope and uncertainty judgments | Not a common truth score; unassessability and judgment interpretation still matter |

κ is null when n=0 or P_e=1, including perfect agreement on a constant category.
No conventional “moderate/substantial” cutoff is used as a qualification rule.
No pooled κ over repeated reviewer pairs or automatic majority reference is
computed. Each pair carries joint-assignment, completion and exclusion counts,
roles, and exposure declarations. Per-item and family identifiers remain
available for source-dependent criticism. Missing/unassessable records do not
become perfect agreement or invented abstentions. Reference-source knowledge
and public-answer exposure are retained, not described as successful blinding.

## Disagreement and error resolution

Each record can separately flag taxonomy overlap, ambiguous target, incomplete
sources, suspected reference error, and irreconcilable interpretation. The report
marks an error allegation as requiring independent checking, never a proven
correction. The human coordinator should route arithmetic/source allegations to
an independent check, then obtain a rationale and second review. Verified
corrections require a new versioned reference artifact and erratum with the old
reference and results preserved. Ambiguity without a defensible unique answer
should remain multi-category, disputed or unscored under a future protocol.
Irreconcilable judgments are a scientifically meaningful outcome, not a parser
failure. Consensus after discussion does not by itself establish truth.

The human-origin and eligibility declarations are documentary safeguards. This
software cannot authenticate a person's identity, certify their expertise,
verify that no discussion occurred, or establish actual independence. A person
or independently governed review organization must do that work.
