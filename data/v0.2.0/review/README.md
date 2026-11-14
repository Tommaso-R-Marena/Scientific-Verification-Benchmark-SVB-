# Phase II review packets

This directory is reserved for reproducible **human review preparation**. No
domain scientist or statistical expert has yet reviewed these tasks. A packet,
an AI critique, or a passing test is not evidence of external expert validation.
The governing protocol is
[`docs/phase-ii/human_adjudication.md`](../../../docs/phase-ii/human_adjudication.md).

`reference_evidence/packets.json` currently contains 32 public-field exports,
prepared from the current case file. These are not completed scientific review
records. Its manifest records the source case hash and displayed packet hash,
states that no external human review occurred, and flags identity/exposure audits
as required. The public packet keeps exactly `question`, `claim`, `documents`,
`methodology`, `assumptions`, and an opaque `public_id`. IDs are reproducible
pseudonyms, not cryptographic anonymity or secret-label protection. The complete
source/rights registry is `data/v0.2.0/registry.json`; a coordinator must attach
appropriate source provenance and reviewer forms before external distribution.

From the project root, generate another fresh export without overwriting an
existing directory:

```sh
PYTHONPATH=src python3 -B scripts/build_human_review.py \
  --condition evidence --seed 1 \
  --output data/v0.2.0/review/another_reference_export
```

The `--responses` option accepts one actual run's raw JSON/JSONL records. It adds
anonymous candidate codes and exact raw response text while omitting model,
provider, latency, token, cost, and score metadata. Missing executions remain
explicit. It does **not** repair response text or remove self-identifying prose;
coordinator review is necessary before claiming identity blinding. Other
information conditions use the same public evidence transformations as the model
interface. Outputs stay inside this independent project and the tool refuses an
existing output directory.

Prepare two distinct packet types:

1. **Item qualification:** question, exact claim, assumptions, scope, complete
   source/evidence manifest, calculation specification, uncertainty and review
   form. Exclude provisional references, expected answers, checker kinds,
   split/family metadata, author conclusions, and all candidate responses.
2. **Candidate assessment:** the qualified item packet plus one anonymous
   candidate answer and its citations/scopes. Exclude model/provider/developer
   identity, aggregate results, costs, rankings and provisional gold. Preserve
   scientific source identities because provenance is part of the construct.

Every item requires two independent domain scientists and one statistical
reviewer. They record first-round judgments before discussion, source locators,
calculations/countermodels, uncertainty, conflicts, expertise, prior exposure,
and whether identity masking succeeded. Disagreement remains visible and may
leave an item unresolved or unscored. No majority vote manufactures scientific
ground truth. No external contacting, recruitment, or compensation has been
performed or authorized by creating these materials.

Packet IDs and candidate codes should be independent of task labels. Content
hashes and a coordinator's mapping support reproducibility. A filtered packet
does not guarantee blinding: answer wording can reveal a model, and reviewers
may already have seen public references. Audit those issues before describing
any review as blinded.

Use project-local output paths. Store any private reviewer information,
consent-governed ratings, or unreleased identity mappings outside versioned
artifacts under coordinator-controlled access. **Do not commit secret labels**.
This shared workspace has no technically protected holdout. The current
alternative is an explicitly public, frozen, family/source-disjoint split plus
model-exposure logs. Honest public references must not be advertised as hidden
gold. Expert-qualified outcomes and protected prospective generalization remain
unperformed until separate evidence establishes them.
