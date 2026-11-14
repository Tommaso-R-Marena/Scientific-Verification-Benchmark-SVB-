# Twelve-case external-adjudication pilot

Selection criteria and IDs are fixed in `data/v0.4.0/pilot_selection.json`, after
Phase IIb results but before any actual human judgments. This is a purposive
scientific-review pilot, not an unseen model test, representative task sample,
or independently blinded study. No reviewer was contacted.

The pilot retains six complete pairs across five study families. Its scientific
coverage is enzyme-assay experimental units (PU01), physical chemistry and
rounded uncertainty fields (FS04), paired patient observations/generalization
(SL02), longitudinal growth/counterfactual attribution (CW02), oxygen-demand
unit contradiction (OD01), and mechanism interpretation (OD02). It deliberately
includes positive recorded facts, refutation, insufficiency and evidence-type
ambiguity. Old labels and case identities occur in coordinator materials, never
as reference answers in reviewer ZIPs. This document should not be supplied to
an intended answer-blind first-round rater before judgments are locked.

The reason for twelve rather than eight is to retain both the oxygen numerical
contradiction and mechanism pair, all six existing B-response cases, and the two
historical biochemical/thermodynamic ambiguity pairs. Selection did not use
future reviewer judgments. Authors already knew model results; no model-outcome-
blind or preregistered selection claim is made. Potential lexical cues, correlated
pairs and secondary-source dependence are audit targets, not hidden benefits.

## Distribution artifacts

- `reference_review.zip`: twelve answer-filtered packets, a blank reference form,
  guide/worksheet and a manifest. No candidate responses or author gold.
- `candidate_review.zip`: the same scientific packets, twelve raw B responses
  for six cases across two models, a blank candidate form and guide/worksheet.
  It excludes provider metadata and scores; raw prose is never repaired/redacted.
- `source_materials.zip`: one shared archive of the five source families, exact
  bytes, registry, attribution and notices. Both review packages bind its hash.
- `coordinator_context.json`: packet/candidate hashes and family strata for
  ingestion. `preparation_record.json` links original case identities. These
  public files are **not part of either reviewer ZIP**, but public readers can
  reconstruct mappings. Confidentiality or successful masking is not established.
- `registry_template.json`: blank eligibility/consent/assignment structure. It is
  intentionally not an activated human registry and cannot be ingested as one.

A coordinator must audit identity/provisional-answer cues, source rights and
completeness, consent, qualifications, conflicts and actual prior exposure before
sending any package. Reference first rounds precede candidate review. Sources
remain identifiable for legitimate scientific context. Masking model-envelope
fields does not remove potentially identifying prose or public lookup paths.

## People and manageable scope

Plan two domain judgments and one methods judgment per case: **36 first-round
judgments**, versus 132 in the earlier full package. Domain reviewers can be
assigned only relevant subsets; no one is presumed expert across clinical design,
enzyme assay, animal growth and molecular thermodynamics. A methods reviewer
should cover paired/longitudinal design, selection, counterfactual identification
and uncertainty; formal/numerical expertise can supplement arithmetic checking.

At an estimated 15–30 minutes per case judgment, the full first pass is 9–18
reviewer-hours: 6–12 domain hours and 3–6 methods hours, before orientation,
primary-source retrieval and discussion. Candidate review is optional after that
lock and adds an estimated 3–6 hours across the panel. No time was measured or
reviewer recruited. Start with a qualified subset if necessary; the pipeline
reports missing registered assignments and unfilled panel slots transparently.

A successful pilot need not produce agreement. It should produce inspectable
rationales, source/method gaps, defensible categories or category rejection,
correctable errors distinguished from persistent ambiguity, and a credible
estimate of actual reviewer workload. Any later taxonomy/reference change needs
a new protocol and an explicit historical erratum, not silent rescoring.
