# Phase II human adjudication and blinding protocol

**Status: protocol and packet preparation only. No external experts have been
recruited, contacted, or recorded as having reviewed SVB.** Separate AI review,
software tests, and this document are not scientific expert adjudication.
Any current author labels remain provisional. This protocol must be registered
with a content hash before the first human rating or newly scored model run to
support a prospective claim; a later registration must disclose its timing.

## 1. Unit of adjudication and people required

The unit is an atomic claim with a fixed evidence envelope: question, exact
proposed claim, assumptions, population/model/application scope, source
documents/data, source versions, transformations, and permitted tools. Related
claim variants and papers from the same underlying study form one family. A
correct calculation and the attached empirical interpretation may receive
different judgments. A citation-entailment judgment is not a global truth label.

Each item needs **two independent domain scientists and one statistical reviewer**.
Domain scientists must have a relevant doctoral qualification or a documented
equivalent research record. The statistical reviewer needs documented training
and research experience in the methods used (including causal inference,
uncertainty quantification, or computational inference when relevant). For a
purely deductive item, the statistical reviewer may mark statistical criteria
not applicable with a reason; the third independent review still occurs. A
formal/numerical specialist supplements the panel for proofs or certified
computation when the primary reviewers lack that expertise.

A nonvoting coordinator checks conflicts and credentials, assigns anonymous
codes, freezes packets, and releases comparison mappings after ratings are
locked. No scientist evaluates an item they authored, a system they developed,
or research for which they have a material professional or financial conflict.
Adjudicators declare prior exposure to the item, source paper, provisional
reference, system, or previous model answer. Knowing a research topic is not
automatically a conflict; prior knowledge of its stored gold is exposure that
must be recorded. If an independent panel cannot be staffed, qualification is
incomplete rather than presumed.

Do not recruit or contact anyone under this protocol without a separate
authorization. Any compensation, consent process, data governance, and applicable
institutional research/ethics determination must be settled before participation.
Publish anonymized professional-role and conflict summaries only with consent;
personal names and private correspondence do not belong in benchmark artifacts.

## 2. Three different meanings of blind

1. **Candidate/model-identity blinding.** A response reviewer receives a random
   candidate code, not provider, model, training method, author, run cost, system
   score, reference status, or other responses' rankings. Randomize order for
   each reviewer. Hide authorship cues in filenames and metadata. A coordinator
   must audit the answer body for explicit identity disclosures. Writing style
   may still identify a system. Any necessary redaction is logged with original
   and displayed hashes and must not change a scientific argument or citation.
   If identity cannot be removed without changing meaning, mark the instance
   unblinded rather than claiming successful masking.
2. **Provisional-reference blinding.** An item reviewer gives an independent
   label and rationale without seeing SVB's provisional label, derivation,
   expected response, checker kind, or author confidence. Hiding a label while
   exposing an explanation that gives it away is insufficient. Reference
   blinding addresses anchoring; it does **not** imply candidate identity was
   concealed. Reviewers who already saw the public reference cannot be described
   as reference-blind.
3. **Scientific-source identity is ordinarily visible.** Study design,
   provenance, retractions, population, and measurement methods can matter to
   adequacy. Do not remove the source DOI, methods, or limitations merely to
   simulate a blind test. Reviewers must declare familiarity and distinguish
   evidence from reputation. A separate source-anonymization experiment would
   change the construct and require its own protocol.

A packet generator can omit fields; it cannot enforce secrecy, certify absence
of implicit identity cues, or establish that a human remained blind. Human
confirmation and coordinator audit are required. The shared SVB workspace has no
protected holdout: investigators and agents can inspect its files. A filename
called `hidden`, a gitignored mapping, or a held-out split does not create access
control.

## 3. Two-stage review with fixed evidence and search rules

### Stage A: reference qualification

Each reviewer independently receives the same source-complete packet, no model
answer and no provisional gold. They reproduce the specified calculation where
appropriate, inspect the study/model assumptions, identify compatible
countermodels, and assess the scientific scope. Reviewers may not coordinate
before locking first-round judgments.

The primary label answers **whether the conclusion follows from the supplied
evidence envelope**. An optional supplementary-source exercise is logged
separately: a reviewer may recommend an additional primary source or correction,
but it does not silently change the original question. New evidence, a retraction,
or corrected data requires an item revision, new hash, and reassessment. Search
timestamps, queries, source URLs, versions, and whether AI tools were used must
be declared. Primary reviews should use no generative assistant; inability to
enforce this rule is disclosed. Ordinary reference managers, calculators,
statistical software, and proof assistants are permitted with versions and
commands recorded.

### Stage B: response assessment

After item qualification is locked, a separate response panel is preferred.
When staffing requires reuse of the same reviewers, record their prior
reference knowledge and do not call the response assessment reference-blind.
Candidate identity remains masked. Present each response individually before
any pairwise comparison; randomized pairwise ordering with a tie option is an
optional secondary measure. Reviewers inspect both the proposed verdict and its
evidence attribution. Fluency, length, and perceived usefulness must not replace
scientific correctness. A response that happens to match the reference label
but cites nonexistent evidence does not receive full evidence credit.

No response or reference is improved after observing a weak system without a
versioned deviation record. Do not exclude an unfavorable response because it
looks unintelligent, contains an execution failure, or exposes an author error.

## 4. Complete packet specification

Each packet must contain the following fields or an explicit missing-data flag.
Absence is itself potentially relevant evidence; it must not be filled with an
invented premise.

| Field | Meaning |
|---|---|
| `packet_id`, `packet_version`, `packet_sha256` | Anonymous task identity, protocol version, and hash of displayed bytes |
| `question`, `claim` | Exact atomic scientific question and proposed conclusion |
| `assumptions` | All admitted mathematical, physical, causal, computational, and measurement assumptions |
| `model_and_scope` | Model class, units, population, conditions, temporal cutoff, intended applicability and quantifiers |
| `evidence` | Exact supplied excerpts/data/artifacts, stable source IDs, locations, and evidence roles; contradictory evidence remains visible |
| `source_manifest` | DOI/URL/version/license, access date, content hash, transformations and exact packet-relative artifact paths |
| `calculation_specification` | Quantity to reproduce, inputs, algorithm/tolerance if explicitly part of the question; no expected numeric answer or reference code |
| `uncertainty_supplied` | Supplied sampling, parameter, numerical, measurement and model uncertainty; missing components flagged |
| `tools_and_time_budget` | Allowed external search/tools and predeclared review budget; actual elapsed time recorded separately |
| `candidate_code`, `candidate_response` | Stage B only; exact masked answer, citations and claimed scopes; not an edited reference |
| `blinding_audit` | Whether identity cues and provisional-reference cues were checked, reviewer exposure declaration, redactions and limitations |
| `review_form_version` | Exact rubric and response-form version |

Do **not** include original task IDs if they encode labels, split/family labels,
the author gold, `reference`, `expected_response`, `checker`, model/provider
metadata, aggregate scores, or post-hoc explanations that reveal the expected
verdict. Artifact relative paths must be explicit and traversals/symlinks audited;
do not give reviewers executable untrusted submissions. Scientific source
identities remain available by design. The coordinator retains packet-to-task and
candidate-to-system mappings outside distributed packets and records their hashes.

## 5. Independent reviewer form and rationale rubric

Each reviewer returns:

- reviewer code, role, domain match, conflicts, familiarity/exposure, date,
  packet/response hash, actual time, tools/search and any deviations;
- one proposed label: formally established, computationally established,
  empirically supported, refuted, insufficient evidence, or disputed/unresolved;
  `needs_revision` and `cannot_assess` are review statuses, not forced truth labels;
- supported scopes and explicitly unsupported scopes, named assumptions required
  for the conclusion, strongest missing bridge, and whether the supplied proof
  or calculation is valid separately from the theorem/interpretation;
- pinpoint citations and reproducible calculations, a counterexample or explicit
  alternative model where relevant, and the evidence that would change the label;
- confidence in the adjudication itself (`low`, `moderate`, `high`) with a reason,
  rather than a fabricated posterior probability that the claim is true;
- disposition of every rubric criterion and a concise written rationale.

Use the following criterion-specific rubric. Scores are diagnostic; they are not
summed into an arbitrary “scientific truth” number.

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Logical/computational reasoning | Specific invalid step or incorrect result | Reasonable but an essential step is not checked | Reproduced/justified under explicit assumptions |
| Numerical and statistical treatment | Invalid uncertainty, units, conditioning, design or inference | Partly addressed; material missing information | Appropriate for the declared quantity/design, with limits |
| Evidence attribution | Mismatched/nonexistent or contradicted attribution | Relevant evidence but locator or support incomplete | Pinpoint evidence supports the actual statement at its stated scope |
| Model/application bridge | Unsupported escalation or incompatible assumptions | Bridge plausible but insufficiently supported | Necessary bridge supported within an explicit restricted scope |
| Verdict and scope communication | Incorrect certainty or scope | Partly correct, material ambiguity | Appropriate verdict, limitations and uncertainty stated |

`N/A` needs a rationale; `not assessable from packet` is not a middle score. For
example, a finite exact arithmetic question may have no empirical bridge to
assess. Conversely, absence of empirical data on a real-world efficacy claim is
not N/A: it is a missing support issue. Evidence can refute a particular equality
without refuting a broader scientific theory. “Not enough evidence” is not
interchangeable with “false.” A source explicitly reporting an association does
not by itself justify a causal interpretation, and no source corpus establishes
the impossibility of undiscovered contradictory evidence.

## 6. Disagreement, errors, and final disposition

First-round judgments are immutable records. The coordinator creates a
disagreement table before any discussion. Distinguish: calculation error,
source mismatch, differing interpretation, ambiguous claim, absent evidence,
conflicting evidence, inadequate reviewer expertise, and provisional-reference
error. Reviewers then exchange anonymized rationales and may submit a separate
second-round judgment. Preserve both rounds and all revisions; do not replace
them with consensus alone.

An item enters a definitively scored subset only if the two domain reviewers and
statistical reviewer independently agree that its claim and evidence envelope
are well-defined and the final label is defensible. This is a qualification rule,
not proof of truth. Numerical disagreements must be resolved through independently
reproduced calculations. A moderator must not settle unresolved scientific
disagreement by majority vote or by agreeing with the benchmark author. Options
are: retain as disputed/unresolved and unscored, retain as insufficiency if that
is the agreed scientific conclusion, revise and re-review, or exclude with a
documented reason. An extra specialist may clarify an issue, not manufacture a
gold label. Author reference errors remain visible as reference errors; they are
not silently reassigned to system failures or successes.

Publish eligible, ineligible, unresolved, missing-review, and excluded counts.
Keep candidate execution failures and unsupported tasks in observed totals.
Report the scientific label distribution and domain/source-family coverage so a
benchmark with only arithmetic positives does not look like empirical validation.

## 7. Agreement, analysis, and governance

Predeclare label agreement, per-criterion disagreements, reasons for revisions,
and a confusion table across independent first-round raters. With adequate data,
report a nominal multi-rater agreement statistic (e.g. Krippendorff's alpha) and
its sampling design; keep exact agreement alongside it because prevalence can
distort a single summary. Do not compute or claim human agreement until human
ratings actually exist. Agreement is not correctness. Cluster uncertainty by
source/study family for analyses of related cases, and report when too few
clusters make a useful interval impossible. Do not label a purposive small
convenience sample iid or assert a powered superiority result without a design
that supports it.

Keep signed/versioned reviewer records, consent-governed role summaries,
protocol/packet hashes, mapping-access logs, deviations, adjudication minutes,
and disposition histories. Public release uses consented, redacted records.
No private reviewer identity, secret label set, candidate credentials, or
confidential manuscript belongs in the Git repository. A coordinator must audit
the privacy and rights of sources before sending packets outside the project.

## 8. Holdout and model-exposure alternative in this workspace

There is no technical protected holdout in the shared workspace. The strongest
honest current design is a **public, frozen, family/source-disjoint evaluation**
with exposure records and prospective external custody as future work.

- Group preprints, journal versions, errata, datasets, reanalyses and paraphrases
  from the same underlying study before splitting. Group related control pairs
  and model/sequence/parameter variants. Avoid calling a file-level random split
  source-disjoint. Require no shared study/source lineage or task family across
  development and scored evaluation, and record any unavoidable overlap.
- Freeze data, sources, transformations, schema, reference method, scoring code,
  model prompts, adapter versions, and analysis protocol. Preserve failed or
  excluded runs and every post-freeze deviation. Public freeze establishes bytes
  and timing, not developer ignorance of the answers.
- Before each model run, log provider/model/checkpoint and version, known training
  cutoff, unknown training exposure explicitly, prompt hash, tool permissions,
  every supplied task/source file hash, retrieval results, prior benchmark access,
  use of development feedback, and whether developers saw evaluation labels.
  Record request time, response hash, completion/error status, and costs when
  applicable. Do not claim absence of memorization from a new filename or cutoff
  statement. No personal credentials or API tokens enter these logs.
- Distinguish **model input filtering** from protection against an investigator
  inspecting public gold. A public structured export may omit gold but it is not
  a secrecy guarantee. Do not commit a purported “secret” answer file or call a
  reversible hash a hidden label. Current provisional references are public and
  should be described as such.
- Future stronger evidence needs a separate trusted custodian, access-controlled
  fresh sources and reference answers, audit logs, no developer access before
  locked predictions, and a disclosed release schedule. Merely hiding model
  names from response raters does not supply this holdout.

The packet workflow is useful preparation for human qualification. Until actual
independent reviewers and a prospective evaluation are available, claims must
remain limited to author-constructed computational controls and the observed
system behavior, with expert qualification and protected generalization marked
**not performed**.
