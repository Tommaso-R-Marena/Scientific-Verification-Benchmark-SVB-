# Reproduce Phase IIb

Run from the SVB root using Python 3.12 (recorded: 3.12.14). Core tests, source
reference checks and recorded-response scoring need only the standard library.
They need no model credentials, network, subject repositories or model packages.

```sh
export PYTHONPATH="$PWD/src"
export PYTHONDONTWRITEBYTECODE=1
python3 -m unittest discover -s tests -v
python3 -m svb.cli validate
python3 -m svb.phase2 validate
python3 -m svb.phase2b validate
python3 -m svb.phase2_references
python3 -m svb.phase2b_references
python3 scripts/analyze_phase2b.py --output results/local/phase2b-replay.json
cmp results/local/phase2b-replay.json results/v0.3.0/results.json
python3 scripts/verify_phase2b_runs.py
```

The verifier rechecks pinned model revisions, runner hashes, raw-output hashes,
prompt-file hashes, each request hash, unique planned identities and decoding
mode. Its fixed output `results/v0.3.0/run_integrity.json` is deterministic. A
successful check establishes artifact identity, not scientific reference validity.
The manifest validator fails on a modified frozen artifact. Do not regenerate
cases, export different prompts or refreeze a manifest to evaluate this version.

The Phase I/II commands in their original reproduction documents remain valid.
The exact Phase I baseline JSON/CSV and the Phase II baseline JSON can be
regenerated into `results/local/` and compared with the retained artifacts.
The Phase IIb frozen numerical baseline reports unsupported on all new packet
forms. Its zero false accepts have zero answer coverage and do not establish
scientific safety.

## Fresh optional model inference

This is fresh generation, separate from replaying recorded outputs. Download
only the public pinned checkpoints and verify the file hashes listed in
`results/v0.3.0/model_access.json`. The selected 0.5B/1.5B models are Apache-2.0;
the development-only 3B model has a distinct noncommercial Qwen RESEARCH LICENSE.
Weights are not distributed in this repository. See `model_qualification.md`
for the pinned install/download procedure and resource measurements.

Use the optional Python environment installed from `requirements-models.txt`:

```sh
HF_HOME="$PWD/results/local/hf-cache" HF_HUB_DISABLE_IMPLICIT_TOKEN=1 \
  results/local/model-venv/bin/python scripts/run_phase2b_model.py \
  --model qwen-1.5b --prompts data/v0.3.0/prompts/evaluation_unconstrained.jsonl \
  --output results/local/fresh-phase2b/qwen-1.5b_unconstrained.jsonl \
  --threads 4 --max-input-tokens 4096 --max-a 24 --max-b 128 --max-c 384
python3 -m svb.phase2b score results/local/fresh-phase2b/qwen-1.5b_unconstrained.jsonl \
  --mode unconstrained --output results/local/fresh-phase2b/scores.json
```

Repeat explicitly with the 0.5B model key, or with the frozen
`evaluation_constrained.jsonl` plus `--constrained-a` and score `--mode constrained`.
Use fresh paths: the runner refuses overwrites. Generation times depend on
hardware and scheduling. The fixed-plan orchestration script targets the
retained original paths and therefore intentionally refuses a replay into them.
Do not delete old outputs to make that script run. No paid inference or private
model credentials are required or authorized.

## Review preparation and subject utility

```sh
python3 scripts/build_phase2b_review.py --output results/local/new-review-package
python3 scripts/build_phase2b_review.py \
  --responses results/v0.3.0/evaluation/qwen-1.5b_unconstrained.jsonl \
  --candidate-task B --candidate-condition evidence \
  --output results/local/new-candidate-review-package
```

Packet field filtering is not access control. A coordinator must audit identity
cues, arrange actually independent reviewers and collect genuine reviews before
claiming blinded or expert adjudication. No reviewer was contacted.

For fresh FoldBounds utility execution, an authorized read-only local FoldBounds
checkout is required at the path in the frozen utility protocol:

```sh
python3 -m unittest discover -s tests -p test_bound_utility.py -v
python3 -m svb.bound_utility
```

The utility command writes its designated result artifact; preserve the recorded
result before a new execution, or use a separate SVB checkout for reproduction.
Endpoint decisions and exact references should agree; timings will differ.
No FoldBounds build or source change is required. Subject integrity checks use
local historical snapshots and are separately recorded in the evidence ledger.
