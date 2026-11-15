# Repeat the PCS–SVB diagnostic

Independent core/recorded checks need Python3.12 and no model packages:

```sh
PYTHONPATH=src python3 -B -m unittest discover -s tests -v
python3 research/pcs-assurance-v1/analyze.py
```

This replays recorded data and exact arithmetic, not a fresh PCS execution.
Every input, record, Lean proof and execution trace is in `raw_executions.zip`,
whose file hashes are indexed in `archive_manifest.json`. Inspect/unpack as data;
do not execute arbitrary files from an untrusted archive.

For fresh actual execution, use Linux, Bubblewrap with unprivileged namespaces,
Python3.11+ at `/usr/bin/python3` inside the sandbox, and Lean4.28.0. Failure of
OS isolation is a blocker, not permission to run unconstrained. The adapter's
sandbox has no network or credentials and no access to the host workspace.
Use a separate ignored SVB cache, never fetch/check out/build in the original
read-only subject repositories:

```sh
mkdir -p results/local/pcs-assurance
git init --bare results/local/pcs-assurance/subject.git
git --git-dir=results/local/pcs-assurance/subject.git fetch --filter=blob:none \
  https://github.com/Tommaso-R-Marena/proof-carrying-science.git \
  bd6d88f71833e101fdb6b491df248f0ded0d6f75
python3 research/pcs-assurance-v1/prepare_subject.py
python3 research/pcs-assurance-v1/reproduce.py \
  --lean-root /absolute/path/to/lean-4.28.0-linux \
  --output results/local/fresh-pcs-check --ids S01 S06 S10
```

The export copies only26 top-level implementation/checker files, never benchmark,
prospective, adjudication or model data. Each must match the recorded identity.
The portable reproduction entry point uses the frozen worker unchanged and writes
only to a fresh ignored directory; it refuses overwrites. For the original full
run, `run.py` records its exact original environment/path assumptions and fixed
artifact paths; do not rerun it over retained results. Fresh timestamps/costs differ;
mathematical/outward statuses should agree. Default `reproduce.py` executes S01;
pass any explicit list of the18 frozen IDs to reproduce more.

Supplemental probes are separately versioned post-hoc diagnostics in their own
scripts/results. Their original paths refuse overwrites; repeat in a separate
SVB checkout after unpacking original evidence if necessary. `artifact_probes.py`
compares the old runner with PCS's existing v2 candidate, using actual Lean.
`supplemental_probes.py` retains the failed first forgery and the successful newline
variant separately. `replay_probes.py` rechecks a genuine bundle and a re-digested
false confirmation. `assumption_probe.py` changes a declared SD assumption,
without altering PCS policy. The direct commands in each execution JSON are
reconstructable Bubblewrap invocations with read-only subject/toolchain mounts.

The six reviewer packets in `review/` reuse the Phase III
`docs/phase-iii/reviewer_guide.md`, response worksheet and ingestion schema.
They link the old shared `data/v0.4.0/pilot/source_materials.zip` for R sources;
no old package is changed. Reference packets precede release of candidate receipts.
Current packet filtering is not genuine independent blinding. No actual-review
registry or human ratings are supplied.

Licenses: new SVB code/authored synthetic controls Apache-2.0; embedded PCS checker
code remains attributed to PCS under its Apache-2.0 license; public R records
retain GPL-2.0-or-later notices in the preserved source registry/archive. Model
weights, subject Git caches and private data are not distributed. No full new
scientific articles or prospective datasets are acquired.
