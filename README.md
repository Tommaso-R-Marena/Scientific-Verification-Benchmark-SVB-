# Scientific Verification Benchmark (SVB)

An independent **research pilot** for evaluating what a scientific conclusion's evidence actually establishes. It runs without PCS, FoldBounds, model APIs, network access or third-party Python packages. This is an authored, internally reviewed diagnostic benchmark; it is not a validated general scientific-AI benchmark or a biological discovery.

SVB separates mathematical validity, computation, numerical reliability, statistics, model adequacy, empirical support, provenance and evidence sufficiency. A correct computation does not automatically establish its physical interpretation.

## Run the independent core

Python 3.12.14 was used. From this repository root:

```sh
export PYTHONPATH="$PWD/src"
export PYTHONDONTWRITEBYTECODE=1
python3 -m svb.cli validate
python3 -m unittest discover -s tests -v
python3 -m svb.cli experiment --output results/local/my-run
python3 -m svb.cli references
python3 -m svb.cli export > results/local/public-tasks.json
```

No install or dependency download is needed. Optional editable installation uses `requirements-build.txt` and `pyproject.toml`. Source-data bytes, registry, core code and protocol are frozen in `data/manifest.json`; validation fails if they change. Do not rerun the dataset authoring script to evaluate a frozen release.

## What ran

* **34 authored tasks:** 11 development, 22 scored evaluation and one unscored open question, across six domains. Mathematical derivations and exact calculations use independent references; empirical-sufficiency labels are author-adjudicated and need external expert review.
* **33 initial tests** passed, including intentional corrupted references, data corruption, family leakage, units, uncertainty, malformed inputs, missing runs and scope overclaims. Later audit additions and final count are in `results/tests.log`.
* Five executed diagnostic policies. Calculation-only and always-insufficient both score 10/22 but have very different false-acceptance behavior. Explicit scope/JSON gates achieve 21/22 and still fail unstable variance. This demonstrates the metrics on constructed controls; it does not establish general AI performance.
* Genuine noninvasive adapters: FoldBounds 18/18 small-model controls, PCS 3/3 eligible of four observed controls (one benchmark reference error), website module 6/6. These are narrow conformance measurements, not a shared leaderboard or security/physical-validity certification.
* An independent Lean 4.28 proof of a small conditional scope-closure invariant checks with no axioms. This is a standard structural result, not a novel theorem or proof of empirical reliability.

See [experimental report](docs/experimental_report.md), [capability assessment](docs/capability_assessment.md), [reference protocol](docs/reference_protocol.md), [review findings](docs/adversarial_review.md), [mathematical report](docs/mathematical_report.md), [draft manuscript](docs/manuscript.md) and [next research steps](docs/expansion.md). Machine-readable artifacts and a standalone SVG are under `results/core/`.

## Data-only submissions

Create a JSON array of response objects (`schemas/response.schema.json`):

```json
{"id":"M03","status":"ok","label":"refuted","scopes":["mathematical"],"confidence":{"formally_established":0,"computationally_established":0,"empirically_supported":0,"refuted":1,"insufficient_evidence":0,"disputed_or_unresolved":0},"reason":"Finite quantifier countermodel."}
```

Run `python3 -m svb.cli score my-responses.json --output results/local/my-scores.json`. Omitted evaluation IDs stay in the denominator. Unsupported/error responses require `label: null`, `confidence: null` and empty scopes. Free-text reasoning is inert and not judged. Do not submit executable code: arbitrary code execution is unsupported.

The frozen evaluation is public and contains visible labels. Hashes detect revision/corruption; they do not create a hidden holdout or prevent contamination. No class labelled `empirically_supported` is populated in this version.

## Optional real-system evaluation

```sh
# Requires authorized local subject checkouts, Node.js and a precompiled PCS authority.
# For PCS's independent signature check only: install requirements-adapters.txt in an SVB-local venv.
PYTHONPATH=src python3 -B -m svb.system_evaluations
```

Read `docs/system_evaluations.md` for default paths, exact scope, protocol history and the retained initial reference error. Adapters never edit or build the subjects. No website deployment or production probing occurs. The basic benchmark remains independent if subjects are unavailable.

To check the standalone theorem with a separately installed Lean 4.28: `lean theory/Scope.lean`. No Mathlib or subject library is imported. Logs are in `results/lean_scope.log`.

## Reproducibility and status

Core output reproduced byte-for-byte in the recorded Python environment. Optional adapter timings vary. Existing subject file hashes/status were compared before and after; no tracked file changed. The prior FoldBounds untracked `.lake/` directory was pre-existing and untouched by benchmark construction.

Code is Apache-2.0; UCI Iris is CC BY 4.0 and PDB archive data are CC0 (see source registry and attribution). Literature review retrieved metadata/abstracts, not a complete systematic full-paper review. The manuscript is an internal research draft, not publication-ready. No broad novelty claim is supported.

A standalone GitHub Actions workflow is provided for explicit manual dispatch. No hosted CI run was started; local tests are the validation evidence. This avoids automatically consuming hosted compute on initial private-repository upload.

GitHub's integration denied repository creation (`createRepository`); the complete local project is committed. See [private repository publishing steps](docs/publishing.md) for the exact commands to use with an authorized account. No remote/public release was made.
