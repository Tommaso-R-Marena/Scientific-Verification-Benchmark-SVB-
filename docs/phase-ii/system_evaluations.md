# Phase II: harder local system experiments

This phase executes actual FoldBounds, PCS and website implementations without
editing, installing dependencies, building, or generating caches in their
checkouts. It extends only the independent SVB project. The original v0.1
adapter, protocol and results remain unchanged.

## Frozen controls and independent references

`data/v0.2.0/system_protocol.json` was written before the first scored run and
hashed as
`91e1671707808c2531330d7afc3b665d81cf3907053915fa7dd7f305a416eac0`.
The digest is retained in `results/v0.2.0/systems_protocol.sha256` and checked
before execution. No input, expected scientific outcome, or scoring criterion
changed after observation. Freezing is local and auditable, not a claim of
third-party preregistration, inaccessible labels, or statistical independence.

The three subjects have separate capability-appropriate denominators. Their
control counts are not pooled into a performance ranking.

| Subject | Cases and reference | Scope |
|---|---|---|
| FoldBounds | Six length-8–10 sequence/q/threshold families, four baseline depths each, three advanced refinement settings: 27 controls. Own four-direction exhaustive SAW enumeration, pairwise contacts and exact `Fraction` arithmetic. | Finite anchored 2D HP-model enclosure, narrowing, full-depth exactness, and measured tightness/runtime. No protein applicability, ligand-binding prediction or empirical biological verification. |
| PCS | Three independently atom-balanced reactions (methane combustion, ammonia formation, ethanol combustion), each paired with an atom-unbalanced variant carrying forged positive evidence: six eligible controls. Independent explicit atom tables and third-party Ed25519/file-hash checks. | Actual compiled Lean authority over fresh signed packages. Physical feasibility/kinetics is not inferred from atom conservation. Two broader capabilities are explicitly recorded unsupported. |
| Website | Actual DOM behavior for overlap, disjointness, invalid-input invalidation and forged imported receipts at widths 390 and 1280: eight observations across four workflows. | Real headless Chromium and actual page JavaScript on an ephemeral loopback static server. No production, account, native desktop checker or human-comprehension claims. |

FoldBounds' independent enumerator fixes the first bond east, retains
reflections, and explores every extension to an unvisited adjacent site. It
does not import any FoldBounds algorithm. The length-8/9/10 anchored path
counts are 543, 1479 and 4067 respectively, corresponding to unrestricted
square-lattice SAW counts 2172, 5916 and 16268 divided by four first-bond
orientations (OEIS A001411). Unit tests check those counts, a hand-checkable
HHHH exact mass, reversal symmetry of a nonpalindromic sequence, and detection
of excluded/widening intervals. The same-environment cross-check is an
independent implementation, not external adjudication or machine-checked
refinement between implementations.

For PCS, the untrusted producer imports its existing public packaging,
hashing, signing and normalization APIs in a separate `python -B` process.
It does **not** supply the truth labels. The input reactions and exact atom
counts are specified by SVB before that process runs. Every generated package
claims PASS and computational support, including the false variants. A
deterministic **public test key**, identified as such in the protocol, signs
these synthetic packages; it is not an identity credential. Independent code
checks all declared file lengths/hashes and the two Ed25519 signatures. The
actual compiled authority must then ACCEPT the balanced predicate or reject
the signed false predicate specifically at `replay`. An earlier structural
rejection is a construction error, not evidence that Lean detected the
scientific error. These are unfamiliar package bytes relative to the v0.1
fixture, not a claim that these textbook reactions are absent from PCS tests
or model training corpora.

## Executed results

The final retained measurements are `results/v0.2.0/systems.json`.

| Subject | Observed controls | Eligible denominator | Matched references | Unsupported | Execution/construction errors in final run |
|---|---:|---:|---:|---:|---:|
| FoldBounds | 27 | 27 | 27 | 0 | 0 |
| PCS | 8 | 6 | 6 | 2 | 0 |
| Website | 8 | 8 | 8 | 0 | 0 |

PCS returned ACCEPT for each of the three fresh balanced containers and
`REJECT:replay` for each of the three properly signed, falsely PASS-labeled
atom-unbalanced containers. Empirical safety of a real biological system and
truth of unrestricted free-form claim statements remain unsupported interfaces
in this experiment. Their unsupported states remain visible in the total
observed denominator and are not counted as correct rejections or defects.

FoldBounds enclosed every exact reference and produced exact equality at full
depth. Its baseline intervals narrowed with depth in all six sampled families.
That correctness did **not** ensure useful shallow probability bounds. For the
ten-residue all-H model at q=2 and contact threshold 2, the exact partition
function is 13323 and the exact event probability is 9304/13323. Baseline depths
2,4,6 all retained probability width 1. The advanced controls reduced partition
width strongly but left almost the entire probability range unresolved:

| Ten-residue all-H setting | Relative partition-interval width | Probability-interval width |
|---|---:|---:|
| Baseline depth 4 | 19722.77955 | 1.00000000 |
| Matching, lookahead 0, depth 4 | 6.32132 | 0.99975075 |
| Matching, lookahead 2, depth 4 | 5.87668 | 0.99621291 |
| Matching + memory-4 terminal transfer, depth 4 | 2.24889 | 0.99901825 |
| Baseline full depth 10 | 0 | 0 |

Relative partition width means `(upper-lower)/exact Z`, not relative error of
a point estimate. Different advanced settings were required to enclose the
reference, not to dominate each other. Their different probability widths are
therefore reported without assuming a total quality ordering. This is a
concrete negative usefulness result for these sampled settings; it does not
establish inefficiency for all FoldBounds algorithms or physical systems.

Single-process full-depth CLI wall times for the controlled all-H, q=2,
threshold-2 size sweep were approximately 0.076 s (N=8), 0.095 s (N=9) and
0.138 s (N=10) in the retained final run. These include interpreter startup
and scheduler effects, have no repetitions, and support only a descriptive
small-size observation, not asymptotic scaling or a performance comparison.
Exact fractions and raw per-control elapsed times are in the result file.

Actual browser observations showed the expected one shared ID or no shared
IDs, visible “Still unknown” language about scientific conclusions, and visible
browser-only calculation scope. Replacing a valid input with an unclosed CSV
quote hid the prior result and disabled checking. Importing a historical receipt
falsely claiming a Lean DISJOINT verdict and scientific acceptance did not
display a live result; a fresh check of the embedded original files produced
the actual overlap and no native confirmation. The two viewports are repeat
observations of the same four workflows, not eight independent human studies.
The screenshot at `results/local/phase2/site-valid-overlap.png` was visually
inspected: the visible result separated exact ID overlap, browser calculation,
and the unknown scientific adequacy of the data. No production requests or
mutating requests were sent. Chromium version was 156.0.8078.79.

## Preserved failures and repairs

The first complete attempted run is retained as
`results/v0.2.0/systems_initial_construction_errors.json`. FoldBounds passed all
27 controls then. All six PCS packages failed construction before authority
execution because SVB supplied a free-text assessment reason where the PCS
schema requires the exact canonical reason associated with the status. This
was corrected in SVB's producer to the documented canonical value. It is not
a correct scientific rejection by PCS.

The first browser launch failed before exercising any workflow because the
long temporary path exceeded the Unix-domain socket pathname limit. SVB's
temporary root was shortened to its own `results/` directory. No subject,
system policy, trust check or browser assertion was modified. These initial
failures remain visible rather than being collapsed into final pass counts.
Raw stderr, execution commands, synthetic signed containers and browser profile
artifacts stay under gitignored local results; synthesized package directories
are removed after each invocation. The frozen protocol and reference labels
were unchanged throughout these engineering repairs.

## Reproduction and boundaries

From the SVB project root:

```sh
PYTHONPATH=src python3 -B -m unittest discover -s tests -p test_phase2_systems.py -v
PYTHONPATH=src python3 -B -m svb.phase2_systems
```

The first command passed all six self-contained independent-method tests.
The second uses the actual checkouts under `/workspace` by default; select a
different trusted parent with `--subject-root`. It writes sanitized results
under `results/v0.2.0/` and verbose results under gitignored
`results/local/phase2/`. Existing v0.1 artifacts are not touched. No production
URL, deployment, database, CI, paid model or external API is invoked.

Required optional subject prerequisites are installed Python cryptography and
PCS schema dependencies, an already compiled authority, Node, the site's
read-only installed Playwright, and `/usr/bin/chromium`. Missing interfaces are
reported explicitly. Child environments exclude inherited credentials and
proxy/identity bindings, set `PYTHONDONTWRITEBYTECODE=1`, and write browser/home
state only under SVB. Each subprocess has a 90-second timeout and a checked
2 MiB captured-output bound. This is isolation for fixed, trusted local tools;
it is not a streaming output bound or a security sandbox for arbitrary code.
Browser routing restricts requests to its ephemeral loopback origin and aborts
non-GET/HEAD requests. No network grant or repository change was required.

The remaining scientific limitations are substantial: hand-selected small
controls, paired rather than independent observations, only three elementary
reaction families, shared compiler/runtime trust, no fresh formal-proof source
replay, no empirical uncertainty propagation through molecular models, no
trained-model evaluation and no human usability evidence. The binary and source
commit hashes identify what was run but cannot by themselves establish physical
validity, author identity, absence of compiler defects, or universal security.
External replication and independent adjudication remain necessary.
