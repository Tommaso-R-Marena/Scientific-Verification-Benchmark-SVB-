# Phase IIb local model qualification

This stage separates a minimal categorical interface (A), short reasoning and attribution (B), and the older full structured schema (C). The models are actual pretrained language models, not diagnostic fixtures or our own generated reference responses. Qualification controls are development-only. They do not establish performance on the new scientific sources, protected evaluation, expert adjudication or scientific competence.

## Two publicly accessible capacity levels

| Key | Model | Pinned revision | Safetensors bytes | License |
|---|---|---|---:|---|
| qwen-0.5b | Qwen/Qwen2.5-0.5B-Instruct | `7ae557604adf67be50417f59c2c2f167def9a775` | 988,097,824 | Apache-2.0 |
| qwen-1.5b | Qwen/Qwen2.5-1.5B-Instruct | `989aa7980e4cf806f80c7fef2b1adb7bc71aa306` | 3,087,467,144 | Apache-2.0 |

Both checkpoints are public, ungated and nonprivate. SHA-256 of each downloaded safetensors file was compared with Hugging Face LFS metadata at the pinned revision. The 1.5B weight digest is `dd924a11b4c220f385b51ffa522daea7c9f3d850e31b162bb5661df483c6d3ee`; the 0.5B digest is `fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe`. All model/config/tokenizer/license hashes and URLs are in `results/v0.3.0/model_access.json`. Weights remain in ignored `results/local/models/`; no model weights or private credentials are committed.

Inference reused the unchanged optional environment pinned in `requirements-models.txt`: Python 3.12.14, Torch 2.7.1+cpu, Transformers 4.51.3. Both use eager attention, float32, four CPU threads, greedy decoding and seed zero. The 1.5B loaded resident memory was approximately 6.6 GB during development, comfortably within the approximately 33 GiB available. Public-source pretraining exposure is unknown. Two models from one family do not represent the population of scientific AI systems, and their differences do not identify a causal effect of parameter count.

## Interfaces and explicit intervention

`scripts/run_phase2b_model.py` reads only exported JSONL objects with exactly `id`, `task`, `condition`, and `messages`. It never reads a case reference, checker, missing-evidence annotation, expected answer, adjudicator rationale or oracle. Model files are hash-verified, loading is offline and uses `trust_remote_code=False`, `local_files_only=True` and safetensors. Prompts over the input cap fail explicitly; no source text is silently truncated. No answer is repaired, rerun because it appears wrong, or replaced with a fixture.

* **A:** the raw response must be exactly one of the six existing categories after whitespace trimming. Quotes, fences, explanations and JSON wrappers are not silently stripped. The generation cap is 24 new tokens.
* **B:** short prose reasoning and source-document attribution, cap 128 tokens. Generation completion does not establish valid reasoning, correct attribution or human-adjudicated reasoning quality.
* **C:** the existing six-field rich schema, cap 384 tokens. Its formatting and scientific reasoning must be evaluated separately from A; category or syntax success does not imply valid confidence vectors or citations.

The optional `--constrained-a` flag restricts decoding to a trie containing all six tokenizer category sequences, followed by EOS. It contains no expected category for the current case. It prevents output-format escape, not scientific error, and greedy token selection under this constraint is not a proof or a calibrated class posterior. The intervention is recorded in every affected raw response and run metadata. It applies only to task A and is compared in a separate bundle; B and C are never silently constrained.

The official checkpoints have a nonnull 32,768-token sliding-window field with `use_sliding_window=false`; the installed Transformers version emits the previously documented generic warning even for eager attention. Inputs are capped at 4,096 and output caps remain far below that window. Model/config/package code was not edited to suppress the warning.

Six dependency-free tests in `tests/test_phase2b_runner.py` check exact category admission, trie closure/EOS behavior, duplicate/hidden prompt metadata rejection, nonfinite JSON rejection and interface enum admission. These tests are software checks, not scientific evidence.

## Fixed development qualification

The parent protocol `data/v0.3.0/development_protocol.json` was written before these outputs. Each model received 19 unconstrained requests: six standard A controls, the same six with reversed category enumeration, three alternative-wording controls, two B controls and two C controls. A separate constrained bundle repeated the six standard A requests. All 50 requests across both models completed generation, with zero input truncations, output-cap hits or execution errors. Raw outputs and metadata remain under `results/v0.3.0/development/`.

The six A controls cover the existing taxonomy. Two are the already-public historical penguin pair; four are explicitly authored instruction controls (a mathematical axiom, a specified exact sum, a false arithmetic equality and a fictional unresolved question). They are not new scientific discoveries or hidden holdout cases.

The prespecified A gate required standard exact-category syntax at least 5/6, standard correctness at least 4/6, and standard/reverse enumeration consistency at least 4/6. Wording consistency is descriptive.

| Model | Standard syntax | Standard correct | Order consistent | Alternative-wording consistent | Constrained correct | A gate |
|---|---:|---:|---:|---:|---:|---|
| 0.5B | 6/6 | 0/6 | 3/6 | 0/3 | 0/6 | Fail |
| 1.5B | 6/6 | 4/6 | 3/6 | 3/3 | 3/6 | Fail |

Both models therefore fail the fixed gate; neither may be advertised as a qualified scientific verifier. The stronger model meets the standard syntax/correctness gates but fails enumeration stability. Both prechosen capacity levels are retained diagnostically rather than selecting a winner or tuning prompts against the new scientific cases. Constraining syntax does not cure the observed comprehension/classification errors.

Observed generation times were 55.88 seconds (0.5B unconstrained), 11.26 seconds (0.5B constrained), 210.99 seconds (1.5B unconstrained), and 36.61 seconds (1.5B constrained). These are observed costs on this shared CPU environment, not a controlled latency or scaling study. Model loading/hash verification and process wall time are additionally recorded in the run metadata. No paid API, private token or remote inference service was used.

## Reproduce optional inference

Reuse the existing optional model environment; the dependency file is not changed:

```sh
uv venv --python 3.12 results/local/model-venv
uv pip install --python results/local/model-venv/bin/python -r requirements-models.txt
HF_HOME="$PWD/results/local/hf-cache" HF_HUB_DISABLE_IMPLICIT_TOKEN=1 \
  results/local/model-venv/bin/python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download('Qwen/Qwen2.5-1.5B-Instruct',
  revision='989aa7980e4cf806f80c7fef2b1adb7bc71aa306', token=False,
  local_dir='results/local/models/Qwen2.5-1.5B-Instruct', max_workers=3,
  allow_patterns=['LICENSE','README.md','config.json','generation_config.json',
    'merges.txt','model.safetensors','tokenizer.json','tokenizer_config.json','vocab.json'])
PY
```

The corresponding 0.5B pinned download is documented in the Phase II model-access report. Run a **new** artifact path without overwriting the retained experiment:

```sh
HF_HOME="$PWD/results/local/hf-cache" PYTHONDONTWRITEBYTECODE=1 \
  results/local/model-venv/bin/python scripts/run_phase2b_model.py \
  --model qwen-1.5b \
  --prompts data/v0.3.0/prompts/qualification_unconstrained.jsonl \
  --output results/local/phase2b-reproduction/qwen-1.5b_unconstrained.jsonl \
  --threads 4 --max-input-tokens 4096 --max-a 24 --max-b 128 --max-c 384
```

Use `qualification_constrained.jsonl` and `--constrained-a` for the declared syntax intervention. Each output has a `.run.json` companion with pinned weights/runner/prompt hashes, runtime versions, settings and every generation's status, token counts and elapsed time. Final scientific inference must wait until its separate public-source case/protocol freeze; qualification does not permit changing scientific labels after seeing model answers. External scientific experts have not completed adjudication.

## Bounded third development candidate

Both original candidates failed the unchanged enumeration-consistency gate. A single additional candidate was authorized before any new-source scientific generation: Qwen/Qwen2.5-3B-Instruct at revision aa8e72537993ba99e69dfaafa59ed015b17504d1. Its two safetensors shards total6,171,926,992bytes and matched the authoritative Hugging Face LFS digests. It fits available CPU memory (~12.6GB resident during qualification). It uses the Qwen RESEARCH LICENSE, which expressly permits noncommercial research/evaluation, **not Apache-2.0**; no weights are redistributed and no model training occurs. The initial two-candidate runner and model-access capsules are archived, and the candidate extension records timing, failed gates, fixed thresholds and the maximum-three-candidates rule.

The third candidate also fails the same minimal-A order gate: standard exact4/6, syntax6/6, order-consistent2/6. Its complete25-request development record is retained. No threshold was lowered, no fourth candidate added, and no new-source outputs were used to select or optimize a prompt. The originally prechosen0.5B and1.5B levels remain diagnostic comparisons, not claimed qualified scientific verifiers.

Minimal-response format failure is now separable from wrong category selection. A decoder constrained to six category token sequences plus EOS is reported as an intervention, not a silent repair or evidence of better reasoning. The full rich task retains its historical instruction bundle; comparisons with minimal A are matched by source cases but cannot isolate a pure schema-burden causal effect because order, length and wording differ.
