# Adversarial review

This review was performed by a separate model-agent role during construction. It
is an internal challenge process, not independent expert adjudication, empirical
validation, or evidence of agreement among human reviewers. Source records and
exact computations provide the evidence below; model agreement does not.

## Source audit

Read-only inspection and direct retrieval on 2026-11-13 established:

| Source | Verified fact | Consequence for adjudication |
|---|---|---|
| UCI dataset 53 API and dataset page | 150 Iris rows, cm units, dataset DOI `10.24432/C56C76`; dataset page explicitly licenses data under CC BY 4.0 | Attribute the data; numerical claims must name the pinned archived variant |
| Downloaded `iris.zip` / `iris.names` | Both `iris.data` and `bezdekIris.data` are present; documentation identifies discrepancies in rows 35/38 relative to Fisher | These variants are not interchangeable, and neither may silently be presented as a freshly validated experiment |
| RCSB usage policies and downloaded `1CRN.pdb` | PDB archive data are CC0; entry records X-ray diffraction, 1.50 Å resolution, engineered chain A | Deposited decimal-coordinate geometry is a reproducible model calculation, not exact physical geometry or binding evidence |

Sources inspected: <https://archive.ics.uci.edu/api/dataset?id=53>,
<https://archive.ics.uci.edu/dataset/53/iris>,
<https://www.rcsb.org/pages/policies>, and
<https://files.rcsb.org/download/1CRN.pdb>.

An independently written `Fraction`/fixed-column audit (no PCS or FoldBounds
outputs used) found:

* `iris.data` SHA-256:
  `6f608b71a7317216319b4d27b4d9bc84e6abd734eda7872b71a458569e2656c0`;
  150 rows, 50 rows per class, exact archived sample sepal-length mean
  `1753/300 cm`.
* `bezdekIris.data` SHA-256:
  `0fed2a99db77ec533a62dc66894d3ec6df3b58b6a8f3cf4a6b47e4086b7f97dc`;
  the same sepal-length mean, but other columns differ.
* 1CRN chain A has 46 CA records with blank alternate-location markers;
  the file contains zero HETATM records. The exact squared distance between
  the deposited CA coordinates of residues 1 and 2 is
  `1439353/100000 Å²`, or approximately `3.79388059907 Å` distance.

These observations do not establish biochemical binding, solution-state
uncertainty, model adequacy, or a new biological discovery. The absence of a
ligand in one deposited structure would not refute binding in another context.

## Required adversarial checks

The core evaluator must reject duplicate JSON object keys, NaN/infinity,
duplicate or unknown task IDs, inconsistent response fields, impossible
probabilities, and out-of-range confidence. Missing, malformed, unsupported,
and failed executions must remain visible in the total task denominator.
Label accuracy must not hide unsupported certainty or evidence-scope escalation.

An intentionally corrupted reference label must be checked against its
independent calculation or explicit evidence-sufficiency argument; merely
checking a dataset hash is integrity protection, not label validation. Split
checks must detect duplicate examples and shared scientific families, while
acknowledging that metadata checks cannot prove semantic independence.

## Limitations reviewers should challenge

* Construction and internal review use related model agents. External scientific
  experts have not adjudicated the labels.
* A public frozen dataset with visible answers is not a secret held-out set.
  Hashing prevents undetected changes; it does not prevent developer exposure or
  pretraining contamination.
* Curated synthetic and small archived-data tasks cannot estimate real-world
  failure prevalence. Confidence intervals over such tasks are descriptive and
  require a specified sampling model for population interpretation.
* Deterministic reference methods and structured baselines may share a
  specification, so their agreement is a conformance check, not proof of
  general scientific reasoning ability.
* A response can supply correct labels and still give false reasoning or
  fabricate evidence. Structured label/scope scoring is not full textual
  scientific adjudication.
* Small-model or primitive adapters must not be advertised as an evaluation of
  every capability of PCS, FoldBounds, or the site.

## Findings and corrections before the scored comparison

| Finding | Initial evidence | Correction / remaining limit |
|---|---|---|
| Checker paths could leave the dataset directory | The first audit run read both `../private.txt` and an absolute path in a deliberately isolated audit fixture instead of rejecting them | The core added path confinement; both attack subtests now fail admission |
| Arithmetic success label could be an inappropriate evidence type | A caller-selected success label could make an exact calculation appear empirically established | The core now limits arithmetic success categories; this is still a specification checker, not empirical adjudication |
| Near-duplicate unit conversions crossed dev/evaluation splits | C01 and C03 used the same 1000 nM conversion with different proposed answers but unrelated family IDs | Both are now dev items in `unit-conversion-nM-uM` |
| Closely related two-state examples crossed splits | B01/B02 reused weights/degeneracies 1 and 3 | Both are now dev items in `two-state-weights-1-3` |
| Unresolved exemplar asserted an unsupported conclusion | U01 initially claimed the pilot determines a universally sufficient affinity model | U01 now asks an explicitly open, unscored research question; it is not evidence of an established scientific controversy |
| Proof validity and scientific insufficiency can be confused | A false assertion that evidence "proves" a target can be refuted as an entailment while the target proposition itself remains unknown | Protocol/text must retain the target/justification distinction; M02 judges the supplied invalid proof, scientific missing-bridge items judge adequacy of evidence for accepting the target |

The corrections precede final scored baseline runs. They are benchmark
qualification changes, not post-result label tuning to favor PCS or FoldBounds.
Only the declared family mechanism is mechanically checked; the near-duplicate
findings above required semantic review and show why unique IDs alone do not
prevent leakage. Shared archived data may still connect tasks across capability
domains, and there is no protected hidden split.

## Executed independent qualification tests

Command from the new project:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -B -m unittest discover \
  -s tests -p test_adversarial_review.py -v
```

The pre-freeze audit run executed **18 tests, all passed**. Tests cover duplicate JSON
keys, NaN/infinity, invalid confidence probabilities, failed execution asserting
a verdict, probability/label disagreement, inert prompt-injection text, duplicate
and unknown IDs, missing/error denominator preservation, unsupported scope
claims, false-accept denominators, empty answer sets, equivalent rational
representations, impossible conditioning, true-theorem/invalid-proof separation,
file path escape, independent Decimal-based Iris/PDB calculations, intentionally
corrupted reference labels, and declared family leakage.

The initial 14-test run had two failing path-escape subtests; that failure was
reported and corrected, rather than omitted from the record. The final run is a
software qualification result. It does not independently validate every natural
language interpretation or prove scientific usefulness in deployed workflows.

The exact numeric references inspected in M01/M06, C01–C06, S01/S04,
B01/B02/B04, and P01/P02 matched their stated arithmetic and archived-data
specifications. Missing-bridge items have plausible compatible alternatives;
they remain author-adjudicated scientific-scope judgments, not external expert
labels or discoveries made by the deterministic checker. The pilot has no scored
case that independently establishes a new empirical biological claim. Its
`empirically_supported` schema category should not be advertised as a validated
empirical-reasoning coverage result.

## Final frozen-artifact review

After execution, a separate audit of the frozen results found the reported
denominators and numerators consistent: 34 total tasks comprise 11 development
tasks, 22 scored evaluation tasks and one retained unscored open question.
`scope_gated` returns 21/22 correct labels versus 10/22 for `calculation_only`.
The remaining C04 population-variance calculation fails under the shared unstable
binary64 calculation. No claim of external superiority follows: the explicit
missing-bridge annotations make the scope contrast an authored diagnostic control,
and the policies are not general scientific verifiers. The hybrid ablations are
explicitly labelled post-hoc rather than preregistered.

The risk/coverage figures preserve unsupported outputs and distinguish them from
correct insufficient-evidence decisions. Confidence vectors are one-hot; the
reported Brier scores are computable but do not establish calibration, and a
smooth risk/coverage curve would be unsupported. The Wilson intervals are
descriptive under a hypothetical sampling model, not uncertainty about a random
sample of real scientific claims.

Three additional post-freeze audit tests cover numeric exponent overflow
(`1e999`, including nesting), retention/exclusion of the unresolved row, and the
distinction between unsupported execution and a correct insufficient-evidence
judgment. The final audit-only suite therefore executed **21 tests, all passed**.
These added tests did not modify frozen source, data, labels, baselines or result
artifacts.

`results/lean_scope.log` reports that `SVB.scope_preservation` and
`SVB.excluded_type` depend on no axioms. This supports the small rule-closure
theorem in `theory/Scope.lean`, not the empirical soundness of admitted scientific
rules, correctness of the Python evaluator, or a theorem proving scientific
reliability. The frozen reference protocol's statement about absence of a new
machine-checked theorem concerns the benchmark's task references; the separately
added scope theorem must retain its narrower interpretation.

The system adapter results remain capability conformance checks. In particular,
PCS has three eligible controls and one retained `reference_error`, rather than
four successful adversarial checks; FoldBounds has 18 small finite-model controls;
the site's six checks exercise actual JavaScript modules rather than browser DOM
presentation. These are neither comprehensive security audits nor a pooled
leaderboard. No additional result-blocking defect was found during this final
review. External adjudication, genuinely blinded challenge construction and more
scientifically demanding evidence cases remain necessary before publication-grade
scientific performance claims.
