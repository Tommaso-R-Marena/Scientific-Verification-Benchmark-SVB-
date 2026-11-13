# Noninvasive system conformance experiments

These are executed capability-specific controls against the actual local tools.
They are separate from the general SVB dataset and are not a leaderboard. No
subject output is used to construct a reference answer. Their small, convenience
sample and known PCS fixture do not estimate generalization or scientific safety.

## Isolation and reproduction

From the independent project root:

```sh
PYTHONPATH=src python3 -B -m unittest discover -s tests -p test_system_evaluations.py -v
PYTHONPATH=src python3 -B -m svb.system_evaluations
```

The first command runs six reference-method tests without needing any subject
repository. The second writes detailed local execution records to
`results/local/system_evaluations.json` (gitignored), reading default subjects
under `/workspace`. `--subject-root` selects a different trusted local checkout
parent; `--output` must stay inside this independent project. The sanitized
retained measurement is `results/system_summary.json`. Reference Ed25519 checking
in this optional PCS adapter uses the installed `cryptography` package (tested
with 50.0.0); the benchmark core and reference unit tests do not import it. An
unavailable dependency or subject is recorded explicitly, never substituted with
a mock or zero-test success.

Subject Python runs use `-B`, `PYTHONDONTWRITEBYTECODE=1` and an explicit source
search path, with this new project as the working directory. Node imports the
actual subject module through an absolute file URL. The PCS executable is invoked
directly; there is no Lake invocation, source edit, dependency installation or
cache creation in a subject directory. Known nonsensitive signed test vectors
are copied into a temporary directory under this project's `results/`, then
deleted. No private source code is copied into benchmark artifacts. Temporary
command arguments and raw output stay in gitignored local records.

Children receive a minimal environment, no inherited API tokens, identity
credentials or proxies. Commands are fixed by the adapter, have a 30-second
timeout and a checked 1 MiB captured-output limit. These precautions are for
known local tools; they are not a sandbox or a streaming memory bound for
arbitrary programs. SVB does not accept arbitrary submitted commands. Only
read-only Git commit identification is performed on subjects. The before/after
subject status was unchanged: FoldBounds already had an untracked `.lake/`
directory from onboarding; the other two subjects were clean.

## Reference methods and scope

| Subject | Independent reference | Executed interface | Meaning and limits |
|---|---|---|---|
| FoldBounds | Exact `Fraction` weights and a fresh four-direction self-avoiding-walk enumerator with pairwise contact counting; first edge fixed east, reflections distinct | Actual `python -m foldbounds` CLI for six sequence/parameter families, length 4–7, unique depths 2,4,N, and two invalid-input cases | Interval enclosure, nested refinement, exact full-depth agreement, and input admission only. No physical protein/ligand inference, empirical validation, Lean theorem replay, or broad scaling claim. |
| PCS | Direct H/O atom counts for `2 H2 + O2 -> 2 H2O`, all manifest file sizes/SHA-256 hashes, two third-party Ed25519 signature checks | Actual compiled `pcs-lean-authority` directory mode with an existing signed test fixture; artifact-byte corruption, inconsistent reported outcome, malformed transcript | Signed fixture compatibility and byte/transcript admission boundaries. Independent reference does not reimplement every PCS admission rule. A familiar system-authored container is not an unfamiliar scientific benchmark. |
| Website | Python standard-library CSV parsing and exact sets/counters on hand-specified fixtures | Actual `file-check-core.mjs` parser, overlap analyzer and HTML report generator, imported in Node | Exact identifier/duplicate behavior, malformed-input rejection, and two scope statements in generated report text. This does not test DOM rendering, visual presentation, account services, production or human comprehension. |

FoldBounds enumeration has no borrowed subject algorithm: each recursively added
site is one of the four neighboring unvisited sites. Induction on prefix length
shows every anchored walk occurs exactly once. Contacts are counted over all
nonadjacent sequence-index pairs. A hand-checkable HHHH control has 9 anchored
walks: 7 with no H–H contact and 2 with one contact, hence Z=11 and P=4/11 at q=2.
The unit tests also check the known 71 anchored length-6 walks, all-polar zero
event mass, invalid model parameters, CSV row-order invariance and nonpalindromic
sequence-reversal symmetry. This is independently executable arithmetic, not a
formal proof that either implementation is correct for every input.

## Protocol freeze and a reference-error discovery

`data/system_protocol.v1.json` existed before the first scored adapter run. Its
SHA-256 was
`f8ba4074599992a874f0a29e23a6b5fc521c64769a034171e55c49ac0be166e6`.
The first-run record is retained locally as
`results/local/system_evaluations.initial_v1.json`. Three PCS controls matched
their expected behavior; one did not: the atom-balanced signed positive was
still accepted when its external replay transcript reported FAIL.

That discrepancy uncovered an **author reference error**, not a PCS bug. The
provisional protocol had incorrectly assumed transcript outcomes override every
checker. Source inspection of `formal/PCS/V2/Authority.lean` (`transcriptOracles`)
and `formal/PCS/V2/DomainAuthority.lean` established that verified builtins have
priority over transcript fallback. Lean recomputes this reaction's atom balance;
a forged external FAIL does not refute an independently established balanced
reaction. The changed transcript does not alter the claim or any source data.

Protocol v1.1 explicitly preserves the original erroneous REJECT expectation,
records this case as `reference_error` and excludes it from the eligible
correctness denominator. It does not relabel it as a new PCS success. Its
observation remains in the total denominator. Both protocols are retained;
v1.1 declares `frozen_before_execution: false`. These PCS results therefore have
no pristine preregistration or hidden-label claim. No general benchmark labels
were derived from this source inspection. This negative finding illustrates why
independent ground truth must be audited before interpreting verifier failures.

## Executed results

| Subject | Total observed controls | Eligible correctness denominator | Matched reference | Execution errors | Reference errors |
|---|---:|---:|---:|---:|---:|
| FoldBounds | 18 | 18 | 18 | 0 | 0 |
| PCS | 4 | 3 | 3 | 0 | 1 |
| Website | 6 | 6 | 6 | 0 | 0 |

The FoldBounds total contains 16 depth-specific interval checks within six
families plus two rejection controls. These related observations are not 18
independent scientific samples. No binomial interval or significance claim is
attached to their pass fraction. PCS accepted the unmodified signed balanced
case, rejected the corrupted artifact at `package`, and returned exit 2 for a
malformed transcript. The unscored diagnostic returned ACCEPT as described
above. The site matched four valid CSV controls and rejected two malformed
ones; each valid generated report explicitly said it was a browser calculation
and did not establish study adequacy.

The full results identify repository commit SHAs and the authority executable
and JS module hashes. Raw elapsed times include process startup, parsing and
operating-system scheduling; they are not a controlled computational-scaling
experiment. Reproduction checks the deterministic scientific outcomes rather
than demanding bit-identical timing or temporary directory names.

No subject defect, empirical biological discovery, universal verification
guarantee, cross-system superiority, or novel algorithm is established by these
controls. Unsupported capability, execution failure and reference error remain
separate from an incorrect subject verdict. The adapters deliberately do not
turn a successful finite computation into an empirical scientific claim.

## Post-observation adapter admission hardening

Final review found that accepting any nonzero exit could misclassify a signal or unrelated crash as an intended negative control. The adapter now requires the known validation exit code and diagnostic for FoldBounds input validation and PCS malformed transcripts. Three regression tests distinguish validation errors, unrelated failures, signals and timeouts. All 28 observed case outcomes matched the original retained measurements on rerun; `results/adapter_hardening.json` records this. This is disclosed post-observation engineering hardening, not a changed scientific label or a hidden preregistered trial. The original sanitized measurement and protocol history remain retained.
