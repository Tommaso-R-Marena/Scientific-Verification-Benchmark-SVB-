# Capability crosswalk: PCS ClaimCheck × independent SVB assurance

PCS implementation: `bd6d88f71833e101fdb6b491df248f0ded0d6f75`.
Website draft: `45f14f068c18c4a0f41f9b65cf113eb7806053df` (site PR149).
SVB stacked base: `e8dd9702ffd4717d12b19bfca727c638612bfea4` (draft PR1).
These are unmerged research interfaces, not PCS v0.6 production authority.

| Actual outcome/layer | Establishes | Does not establish | Independent test / human responsibility |
|---|---|---|---|
| Kernel MATCH_PROVED | Reviewed `run` agrees with a typed calculation on embedded bytes, under declared parsing, rounding, NA and unit conventions | That this is the intended variable, authors' file/population, a physical measurement, or a causal result | Independent rational computation, exact source/executable hashes, actual kernel run, strict proof-to-checker binding; scientific source/custody review remains separate |
| MISMATCH_PROVED | This reading of these bytes fails the exact numerical tolerance | An error in a paper, wrong science, or an incorrect measurement | Independent arithmetic; inspect alternate readings, conventions and custody. Expert adjudication must qualify any accusation |
| CONDITIONAL_ON_CONVENTION | Explicit mathematical branches differ, e.g. sample versus population SD | A unique scientific convention or false paper | Independent squared-interval checks; resolve/admit assumptions externally |
| UNDEFINED_PROVED / NOT_ESTABLISHED | A defined unsupported/undefined outcome, or no accepted mathematical result | A negative scientific fact | Distinguish capability, input/gate failure, timeouts, genuine undefined statistic and process failure |
| SUPPORTED_BY_AUTOMATIC_CHECKS | Fixed source-wording/eligible-reading/decoy heuristics passed | Correct natural-language understanding or calibrated confidence that a reading is faithful | Source IDs/quotes and literal bindings can be checked independently; difficult interpretation needs humans |
| CONFIRMATION | Number reproduced under an automatically supported reading | The whole sentence/paper is scientifically correct, authentic data custody, empirical support | Jointly inspect math, reading and scientific axes; do not map directly to empirically_supported |
| DISCREPANCY_FOR_REVIEW | A mismatch with policy-required corroboration and convention checks | An accusation that the paper is wrong | Review queue outcome, with independent computation and source interpretation; no automatic paper-error score |
| REQUIRE_HUMAN_REVIEW | Reading evidence did not meet automatic policy; math may still be preserved | Successful verification or scientific error | Measure coverage separately. Legitimate conservatism is not false mathematics |
| Scientific NOT_ASSESSED | No scientific adequacy judgment is made | Support, refutation, or certainty about empirical conclusions | Design, sampling, mechanisms, causality, measurement and target scope require independent evidence/expertise |
| Website preview | Browser computation; no kernel result | A formal certificate | Draft explicitly labels no authority; inspect display boundary separately from kernel behavior |
| Imported kernel-run JSON | Local report names expected proof/data/checker hashes | Authentication that Lean actually ran | Page explicitly says REPORTED / NOT VERIFIED. Hash correspondence is not origin authentication |
| Stand-alone proof runner | Depends on validating what theorem is actually about, not just kernel acceptance | Arbitrary valid Lean files necessarily concern the reviewed checker | Known noncanonical-tail exploit reproduced; existing v2 guard rejected it; canonical file accepted by both |

## Connection to the proposed SVB axes

Keep the exact typed claim, data identity, computational result, evidence-to-claim
binding, scope/assumptions, empirical support and uncertainty separate. No lossless
map exists to one historical SVB label. A theorem refuting a numerical reading
can be formally established, computationally established, and refute that reading
simultaneously; science can remain unassessed. A conditional result or review
request is not automatically disputed science or insufficient evidence in every
sense. Historical labels and results remain unchanged.

The decoy frequency (at most2% among a bounded set of comparable numerals/readings)
is a mechanical selection heuristic, not a calibrated semantic error probability,
p-value, posterior, or guarantee of at most2% unsupported confirmations. No such
probability model is established by the diagnostic or by a kernel proof.

## Assurance contract and trusted base

`Scope.lean` is an elementary typed-admission policy: computation authorizes its
mathematical scope; binding needs its own admitted check; a scientific conclusion
requires a separately admitted empirical bridge. Two actual Lean4.28 theorems
check that scientific authorization implies that bridge and cannot follow when
it is false. They depend on no axioms. This is ordinary typed inference, not new
logic; compare SVB's preserved Scope theorem, Phase III evidence/provenance review,
ECO/PROV and established dependent-type methods.

The proof assumes the inductive policy, the meanings assigned to its fields,
truthful admissions and the Lean trusted kernel/toolchain. It does not verify
Python, authenticate a receipt, prove an interpretation, justify a bridge,
validate measurements, or establish complete scientific safety. A serialized
`kernel_accepted: true` flag is not itself an authentic kernel check. PCS proof
TCB includes Lean4.28/kernel/GMP, the reviewed checker, its generated obligation
binding, process/axiom checks, hashing and filesystem. Its Mathlib meaning theorems
were inspected as documented claims, not rebuilt in this SVB experiment.

The independent software replayer rechecks proofs/math and some policy invariants,
but explicitly takes eligible-reading enumeration, positional patterns and some
lexical findings as recorded. It is not wholly independent semantic verification.
