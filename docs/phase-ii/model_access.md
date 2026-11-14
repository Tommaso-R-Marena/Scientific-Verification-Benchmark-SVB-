# Actual local model access and inference record

## What was actually available

The selected computer had 5 CPU cores and approximately 33 GiB RAM, but no Torch, Transformers, llama.cpp, Ollama or locally cached language model was found. Presence checks for `HF_TOKEN`, `HUGGING_FACE_HUB_TOKEN`, `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` were all false; no secret values or credential files were inspected. No private credential or paid inference endpoint was used.

A real, ungated public pretrained instruction model was downloaded:

* Model: `Qwen/Qwen2.5-0.5B-Instruct`, approximately 0.49 billion parameters.
* Pinned Hugging Face revision: `7ae557604adf67be50417f59c2c2f167def9a775`.
* License: Apache-2.0, confirmed in pinned model card and LICENSE.
* Safetensors size: 988,097,824 bytes.
* SHA-256: `fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe`, matched to Hugging Face LFS metadata at the pinned revision.
* Runtime: Python 3.12.14, Torch 2.7.1+cpu, Transformers 4.51.3, float32 CPU inference.

All model file identities, source URLs, hashes, license and access limitations are recorded in `results/v0.2.0/model_access.json`. Weights and dependencies remain under ignored `results/local/` and are not committed. Open pretrained weights are not evidence that a model has never encountered these public sources; training-data exposure is unknown.

## Executed access smoke checks

Before any Phase II scored scientific evaluation, the model actually generated `{"answer":"4"}` for an unrelated `2+2` JSON smoke prompt. The first execution used SDPA; a second used eager attention and returned the same text. Both prompts, raw strings, token counts, elapsed times and runtime metadata are retained under `results/v0.2.0/models/smoke*`. These are access checks, not scored scientific evidence or mock model responses. The first used 10 output tokens in approximately 1.11 seconds; the eager run used 10 in approximately 1.06 seconds. Process/model loading took around 5–6 seconds.

Transformers emits a generic sliding-window warning for both SDPA and eager because the official config has a nonnull `sliding_window=32768`; that warning's guard does not test `use_sliding_window`, which is false in the pinned official configuration. Actual attention applies sliding-window behavior only if `use_sliding_window` is true. Scientific inference uses eager attention, and configured input/output caps are below 32,768 tokens. No model file, package source, expected hash or verification behavior was edited to silence the warning. Sampling warnings were avoided by explicitly disabling unused sampling parameters in greedy generation. The warning and its limitation are disclosed rather than reported as proof of model correctness.

A later full-schema generic arithmetic development prompt also ran before scientific scoring. It completed with 65 output tokens in approximately 9.21 seconds, but returned a scalar confidence and an empirical scope for an arithmetic claim. The raw malformed response is retained as `structured_smoke.outputs.jsonl`; it is not repaired or counted as a scientific benchmark success. This demonstrates why generation completion, schema validity and reasoning correctness must be evaluated separately. No prompt tuning or inference repair was performed in response.

## Runner boundary

`scripts/run_local_model.py` accepts only pre-exported JSONL records:

```json
{"id":"public-opaque-id","condition":"evidence","messages":[{"role":"system","content":"Task-wide instruction"},{"role":"user","content":"Naturalistic packet"}]}
```

No task objects, references, checker annotations, missing-evidence fields, expected answers, oracle implementations or adjudicator rationales are loaded by the runner. The parser rejects extra fields, duplicate id/condition pairs, duplicate JSON keys, nonfinite numbers, and assistant exemplars. System/user text is untrusted task content rather than executable code. Only maintained local model code is executed: `trust_remote_code=False`, `local_files_only=True`, safetensors required, model hashes checked before loading. Inference is offline, greedy and seeded; it uses eager attention and no retries based on the answer. Raw text is never repaired, parsed into a preferred label or replaced with a diagnostic fixture. Failed runs and token-limit flags remain visible.

No source packet is silently truncated. Inputs over the recorded cap become explicit `execution_error` records. The maximum new-token cap can truncate an answer, but that fact is recorded; it must not be described as a completed valid response merely because generation returned. Root's independent evaluator—not this runner—grades categorical labels, scopes, citations, confidence, reasoning and malformed outputs against its own criteria.

Five dependency-free tests in `tests/test_model_runner.py` verify the input/output boundary. They do not require model downloads or Torch. These are engineering tests; smoke completion alone is not experimental scientific reasoning validation.

## Reproduction

Core tests and deterministic SVB evaluation need none of these dependencies. For optional local inference, use an environment entirely inside the independent project:

```sh
uv venv --python 3.12 results/local/model-venv
uv pip install --python results/local/model-venv/bin/python -r requirements-models.txt
HF_HOME="$PWD/results/local/hf-cache" HF_HUB_DISABLE_IMPLICIT_TOKEN=1 \
  results/local/model-venv/bin/python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download('Qwen/Qwen2.5-0.5B-Instruct',
  revision='7ae557604adf67be50417f59c2c2f167def9a775', token=False,
  local_dir='results/local/models/Qwen2.5-0.5B-Instruct', max_workers=3,
  allow_patterns=['LICENSE','README.md','config.json','generation_config.json',
    'merges.txt','model.safetensors','tokenizer.json','tokenizer_config.json','vocab.json'])
PY
```

Export naturalistic prompt JSONL only through the Phase II packet interface after validating its frozen manifest. Then invoke:

```sh
HF_HOME="$PWD/results/local/hf-cache" PYTHONDONTWRITEBYTECODE=1 \
  results/local/model-venv/bin/python scripts/run_local_model.py \
  --prompts results/v0.2.0/models/EXPORTED.prompts.jsonl \
  --output results/v0.2.0/models/UNIQUE.outputs.jsonl \
  --threads 4 --max-input-tokens 4096 --max-new-tokens 384
```

The output path must remain inside SVB and must not already exist. Metadata includes prompt-file SHA, runner SHA, pinned weight SHA, runtime versions, generation settings and per-record timing/token counts. To preserve failed experiments, choose a new output filename for every later run. Full public scientific-run outcomes belong in the Phase II experimental report; no independent expert review, protected hidden evaluation or scientific superiority follows from this access setup.
