# Release engineering and reviewability audit

Inventory target: the immutable Phase IIb head
`d832b6431c37871674d20ceb534e9b5fac797909`, compared with main
`30f842e241b0a37ab5d24ef6537113d6bbbb4103`. The machine-readable inventory is
`results/v0.4.0/release_audit.json`, reproducible with `scripts/audit_phase3.py`.
Numbers describe logical tracked-file bytes, not compressed Git storage or
network download cost. ZIP contents are not expanded in duplicate totals.

## Size and duplication

The earlier head contains **326 tracked files, 9,923,723 bytes**. PR #1's earlier
range changes **265 files**, with **85,060 text additions and five deletions**.
Approximately 6.81 MB is under data, 2.21 MB under results, 0.40 MB under docs,
0.15 MB each under scripts/src and 0.08 MB under tests. Thus the large line diff
is substantially data and JSON artifacts, not only implementation complexity.

Exact duplicate files account for **1,544,586 excess bytes**, before considering
copies embedded in ZIPs. A 921,086-byte primary penguin PDF appears in both the
source archive and expanded reviewer export. Three historical source-complete
review ZIPs are approximately 731–751 KB each, and contain further shared sources.
Raw model JSONL, metadata, strict scores and partial/interruption records are
intentional provenance. Their duplication should not be “fixed” by deleting
failed runs, old outputs or files bound by manifests.

The Phase III pilot uses one shared source ZIP and two small separate review
ZIPs. Each stage binds the shared archive hash. It adds no new scored science
cases or model outputs. Unpacked candidate archives, model weights, caches,
private ratings and coordinator personal records should remain outside tracked
artifacts. Old public labels remain public; ignored directories are not access
controls. A future archival release can publish unchanged content-addressed
bundles and an index, but must preserve historical bytes/paths or maintain an
explicit compatible historical checkout. Do not silently alter frozen manifests.

## Dependency and license boundaries

The independent core and recorded scoring use Python's standard library. Optional
model inference has a pinned requirements file; adapter signature checks,
Chromium/Node and Lean are separate subject-specific prerequisites. Model inference
is not hosted CI. Python-package version remains 0.2.0 while research data/protocol
versions are separate; no new package release is asserted.

Project code/authored text is Apache-2.0. Source records have separate terms:
GPL-2.0-or-later R artifacts and copied notices, CC0 penguin/PDB data, CC-BY
primary article/UCI data and FreeSolv subject to upstream original-source caveats.
Review exports retain registry attribution and original notices. Copying these
as scientific data does not justify relabeling them Apache-2.0 or resolving all
upstream rights questions. A distributor should recheck the exact intended bundle
and source caveats. This is a provenance/license-boundary audit, not legal advice
or a finding that a database license covers every primary measurement.

0.5B/1.5B selected weights are Apache-2.0; development-only 3B uses a noncommercial
Qwen RESEARCH LICENSE. Weights are not committed or redistributed. New literature
inspection retains metadata, response hashes and section notes rather than full
texts. Actual human records require consent and a publication decision separate
from public software availability. No new inference dependency or service is
introduced by Phase III.

CI uses explicit manual dispatch and now checks historical reproduction plus the
new stdlib pipeline/protocol. Existing action major tags are not immutable action
SHAs, a remaining supply-chain reproducibility limitation. No subject build,
production service or paid inference is part of Phase III. Existing historical
CI successes are not retrospective evidence of scientific validity.

## Recommended review units without history rewriting

Keep PR #1 draft as the provenance umbrella. Review it in these immutable ranges,
or ask maintainers whether equivalent stacked PRs based on branch pointers to
existing commits would help. **Do not force-push, squash away the research record,
cherry-pick altered frozen bytes, or merge without authorization.** No extra PRs
or branch pointers are created by this recommendation.

| Review unit | Immutable range / concern | Main reviewer needs |
|---|---|---|
| Phase II foundation | main → `7222c65c0937542897bcad375073a5d7ff5869f8` | Naturalistic prompt boundary, source data/licenses, scoring, provisional references |
| Phase II executed history | `7222c65` → `9757e4b2f82e9023a17b5173ca0d1495ad445b2d` | Actual raw model outputs, schema failure, interruption/recovery and integrity |
| Phase IIb | `9757e4b` → `d832b6431c37871674d20ceb534e9b5fac797909` | A/B/C separation, qualification, new references, bound utility and claims |
| Phase III continuation | `d832b64` → current head | Taxonomy semantics, pilot selection/masking, ingestion/privacy/metrics, external-readiness claims |

Within each range, review source/protocol and numerical references before reading
score summaries, then inspect raw outputs and reproduction logs. Related protocol,
scorer and artifacts should stay together when hashes bind them; splitting those
into independently mergeable fragments can create invalid intermediate versions.
A path-filtered review is safer than pretending they are independent components.
If stacked PRs are desired later, use existing chronological commits as boundaries,
verify each base/head's complete tests, and leave PR #1 and published history
intact. Expert scientific review remains a separate activity from code approval.
