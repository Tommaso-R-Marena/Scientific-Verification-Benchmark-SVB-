# Reproduce Phase III

From the repository root, Python 3.12 and the standard library suffice. No model,
subject checkout, network, reviewer record or private credential is required for
the core software checks and recorded analysis.

```sh
export PYTHONPATH="$PWD/src"
export PYTHONDONTWRITEBYTECODE=1
python3 -m unittest discover -s tests -v
python3 -m svb.cli validate
python3 -m svb.phase2 validate
python3 -m svb.phase2b validate
python3 -m svb.phase3 validate
python3 -m svb.phase2_references
python3 -m svb.phase2b_references
python3 scripts/verify_phase2b_runs.py
python3 scripts/analyze_phase2b.py --output results/local/phase2b-phase3-replay.json
cmp results/local/phase2b-phase3-replay.json results/v0.3.0/results.json
python3 scripts/audit_phase3.py
```

The audit command reproduces the designated version-0.4 numerical, false-acceptance,
development-construct and release-inventory JSON artifacts; a clean tree should
show no differences in them. These are post-hoc historical analyses, not new model
results or human reviews. Release inventory uses Git objects at the fixed earlier
head, so a fresh clone must include history (hosted CI requests fetch-depth 0).

Generate a byte-identical pilot preparation into a fresh ignored path:

```sh
python3 scripts/build_phase3_pilot.py --output results/local/pilot-replay
cmp results/local/pilot-replay/reference_review.zip data/v0.4.0/pilot/reference_review.zip
cmp results/local/pilot-replay/candidate_review.zip data/v0.4.0/pilot/candidate_review.zip
cmp results/local/pilot-replay/source_materials.zip data/v0.4.0/pilot/source_materials.zip
```

The builder refuses overwrite. Frozen proposal files and prepared archive hashes
are checked by `svb.phase3 validate`. Do not regenerate a manifest to make changed
content pass. Test-only review fixtures are created in software tests and never
counted as actual human judgments; production rejects them. The blank registry
and forms intentionally fail ingestion until genuine human declarations and
assignments exist.

See `adjudication_pipeline.md` for the actual-review CLI and privacy boundary.
No example actual-review files are supplied. Keep real personal records and
ratings private; external distribution, contact and any publication of ratings
require explicit authorization/consent. A public ZIP is not a protected holdout.
The seven literature pages/PDF were retrieved for targeted inspection; only
metadata/hashes/section notes are committed. Re-fetching live URLs may return
different bytes and does not affect offline protocol reproduction.
