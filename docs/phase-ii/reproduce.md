# Reproduce Phase II

Python3.12.14 was used. The independent core, reference checks and tests require only the standard library. Run from this repository root:

```sh
export PYTHONPATH="$PWD/src"
export PYTHONDONTWRITEBYTECODE=1
python3 -m svb.cli validate
python3 -m svb.phase2 validate
python3 -m unittest discover -s tests -v
python3 -m svb.phase2_references
python3 -m svb.phase2 baselines --output results/local/phase2-baselines.json
```

Compare the new baseline output with results/v0.2.0/baselines.json. The old v0.1 command `python3 -m svb.cli experiment --output results/local/v01-repeat` remains available and reproduces its old results without alteration. Do not rerun authoring/freezing scripts during evaluation.

## Replay recorded real-model responses

No model download is required to score the retained raw response file:

```sh
python3 scripts/analyze_phase2.py results/v0.2.0/models/qwen_scientific.jsonl --output results/local/phase2-model-scores.json
```

This reproduces scoring, not fresh model inference. For new offline CPU inference, follow model_access.md and install the pinned optional requirements-models.txt in an SVB-local ignored virtual environment. Model weights are public Apache2.0 and pinned by revision/hash; they are not committed. Expect significant CPU runtime for60 requests. Do not use paid model credentials or APIs.

```sh
python3 scripts/run_local_model.py --prompts data/v0.2.0/prompts/scientific_run.jsonl --output results/local/my-fresh-qwen.jsonl --max-new-tokens 384 --max-input-tokens 4096 --threads 4
```

Outputs refuse overwrite. The runner never imports scientific references or invokes generated code. Strict primary admission and format-only secondary agreement are separate. New-run runtime/token timings can vary even if deterministic textual outcomes match.

## Optional evaluated subjects

Authorized read-only sibling checkouts and the already-built PCS authority are needed only for:

```sh
python3 -B -m svb.phase2_systems
```

This invokes real local FoldBounds/PCS/Chromium interfaces without changing the subjects. Its raw timestamps and timings are not expected bit-identical; scientific control outcomes are. See system_evaluations.md for initial constructor/browser failures and final scope. No production endpoint is probed.

## External review preparation

```sh
python3 scripts/build_human_review.py --output results/local/new-human-reference-packets
python3 scripts/build_human_review.py --split evaluation --responses results/v0.2.0/models/qwen_scientific.jsonl --output results/local/new-human-response-packets
```

These exports omit gold/model metadata but do not create protected access controls. A human coordinator must audit identity cues before distributing to actually independent reviewers. Do not claim blinding, expert validation or hidden testing from field omission alone.
