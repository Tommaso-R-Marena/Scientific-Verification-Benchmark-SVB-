# Internal post-result output and methodology audit

This is an internal author audit after the frozen comparison, not independent
expert adjudication. It selects examples for external review without changing
reference labels, prompts, outputs, scoring code or primary denominators. No
scientific reasoning-accuracy aggregate is derived from these observations.

## Falsification checks and retained problems

| Challenge | Executed observation | What remains unresolved |
|---|---|---|
| Minimal answers might still be wholly malformed | Both final models admit all 12 evidence-present A outputs; 0.5B without documents has three malformed outputs | Category interpretation and development order instability remain confounds |
| Larger checkpoint might pass the unchanged gate | 3B standard syntax 6/6, exact 4/6, but order consistency 2/6; all three candidates fail | A different model family and qualified interface are needed before representative capability comparisons |
| Constrained syntax might cure science errors | All constrained A outputs are legal; coarse correctness and false-accept counts are unchanged | Decoding changes the category path; no general causal benefit is established |
| Exact taxonomy might penalize equally accepted evidence types | Separate coarse acceptance retains the 0.5B 2/12 and 1.5B 6/12 evidence-present agreement | Empirical/computational overlap needs expert category qualification; all historical gold is preserved |
| Low false acceptance might just reflect abstention | 0.5B makes seven uncertain judgments, six supported references have only one accepting prediction; numerical baseline answers zero cases | Lower false-accept counts alone cannot rank safety or usefulness |
| Correct prose might be inferred from a useful disclaimer | B contains unsupported assertions next to limitations, including within the same response | Independent claim-level entailment and uncertainty adjudication are absent |
| Absence of unknown IDs might be called good attribution | Neither model supplies a bracketed document ID in any B response | Zero unknown IDs is vacuous here; source attribution is missing rather than validated |
| Rich `execution_error` status might be read as a crash | All 12 C generations complete; raw admission status is malformed | Historical scorer normalizes these to its error status; report both layers |
| Per-item intervals might imply independent evidence | Items derive from three studies; old C Wilson field is retained but unused for inference | Need substantially more independent families and a prospectively justified clustered analysis |
| New study sources might be called independent primary validation | Three studies are new to SVB but use a common public R curation channel | Original methods, laboratory reliability and pretraining exposure remain unaudited |
| Public field filtering might be called blinded testing | Prompt allowlists and review ZIPs omit answers/provider envelope | Public cases and labels are reconstructable; no independent custodian or actual blind review exists |
| Certified intervals might imply useful scientific decisions | All 32 enclosures pass, yet shallow/moderate decide no nontrivial interior thresholds | Only tiny mathematical models were examined; physical applicability is not tested |

## Specific raw B examples for human review

Locations are `results/v0.3.0/evaluation/<model>_unconstrained.jsonl`; public IDs
are deterministic case identities. Raw text is not corrected in the candidate
packets.

1. **0.5B, CW02S:** “the observed increase in body weight due to the consumption
   of diet 1” is offered as justification of an exact individual causal
   counterfactual. The supplied longitudinal measurements do not observe the
   same chick without that diet. Detailed repeated measurements do not identify
   the missing counterfactual. Reviewers should distinguish observed growth
   from the target's attributable growth.
2. **0.5B, OD02S:** “The text clearly states … the microorganisms … stopped
   aerobic respiration” attributes the target claim to the scientific record.
   The source reports demand observations and their units; it does not establish
   that unique mechanism. This is claim/source conflation even without a
   fabricated bibliographic citation.
3. **1.5B, CW02S:** the response first says the record establishes that diet 1
   caused exactly 163 g of additional weight, then says it “does not establish
   causation.” It reaches the 128-token cap mid-explanation. The contradiction
   and incomplete ending must remain visible; a later disclaimer does not
   silently erase the preceding causal assertion.
4. **1.5B, SL02S:** the response says drug 2 increases sleep more for “each
   individual patient observed,” then correctly rejects generalization to all
   future patients. Patient 5 has −0.1 hours under both drugs, so the strict
   observed-patient statement overlooks a tie. A reviewer must inspect both the
   useful scope limitation and the false intermediate assertion.
5. **0.5B, OD02N:** the response calls the observed decrease justified, then
   says it is impossible to determine if the claim is true from the data. The
   atomic target is a recorded day-3/day-4 ordering, not an unobserved mechanism.
   This illustrates the need to distinguish measurement reliability from what
   the supplied table says.

These are internally identified, checkable concerns, not final reviewer grades.
No model-internal reasoning faithfulness is inferred. More capable models,
neutral paraphrases, independent rows/units perturbations and stronger scientific
baselines remain future experiments; no unexecuted robustness run is claimed.

## Reviewer preparation and identity cues

The source-only ZIP contains 44 packets and 132 blank role forms. Two additional
candidate ZIPs contain the same scientific packets plus exactly six available
raw B candidates each; 38 missing candidates per package are explicitly marked.
No gold, provider metadata, timing or internal coordination map enters a ZIP.
Scientific source IDs remain visible for legitimate provenance review.

These are preparation artifacts, not distributed review. Current directory and
ZIP paths indicate candidate provenance to a repository reader. A coordinator
must assign neutral distribution names, inspect raw prose for identity cues,
obtain conflict/exposure declarations, and keep references separate from model
answers during the first round. Internal maps are ignored by Git, but public
labels and deterministic identities remain reconstructable. Neither hashing nor
ignored files creates a protected evaluation.

The report and ledger deliberately preserve: all gate failures; all malformed
outputs; low or zero baseline coverage; the output-cap hit; source-channel
limitations; label ambiguity; the historical PCS reference error; and the lack
of external reviewers. None is resolved by internal AI agreement.
