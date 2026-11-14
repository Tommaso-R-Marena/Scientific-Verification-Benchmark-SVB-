# Phase II adversarial review

Internal model-agent review is a challenge process, not independent human or laboratory qualification. This report distinguishes direct source evidence, executed checks and unresolved scientific judgments. No existing subject repository is modified or used to establish reference labels.

## Initial preservation and source checks

On 2026-11-14 the frozen v0.1 test suite executed 39 tests, all passed. Phase II additions must preserve the frozen v0.1 source, data, protocol and results.

The downloaded `penguins_README.md` explicitly licenses the data CC0 and attributes collection to Kristen Gorman and Palmer Station LTER. It cites Gorman, Williams and Fraser (2014), doi:10.1371/journal.pone.0090081, and three original EDI datasets (Adelie/Gentoo version 5, Chinstrap version 6). Its request that prospective publishers contact the scientist is recorded as source context; no contact was sent. A CC0 reuse statement does not establish scientific adequacy or authorize claims on the collector’s behalf.

Independent CSV parsing established 344 rows: Adelie 152, Gentoo 124, Chinstrap 68; study groups PAL0708 110, PAL0809 114, PAL0910 120. There are 342 nonmissing body masses. Exact body-mass sums/nonmissing counts are Adelie 558800/151 g, Chinstrap 253850/68 g, Gentoo 624350/123 g. `Individual ID` alone has 190 distinct strings and 114 repeated keys; `(studyName, Individual ID)` is unique across all 344 rows. Reused strings do not by themselves prove the same biological animal was measured repeatedly.

## Review scope

The completed pre-freeze review below covers packet/reference separation, prompt leakage, scientific labels, score denominators, citation handling and empirical interpretation. It does not claim a completed human review or score unrun model evaluations.

## Pre-freeze findings and corrections

| Finding | Risk | Correction before scoring |
|---|---|---|
| Evidence-removal conditions initially reused full-record references | A scientifically correct abstention after removing the observation could count as a false rejection | `condition_reference` now requires explicit condition labels; all no-evidence packets are adjudicated insufficient because no observation survives. Missing condition adjudication fails admission. |
| Failed/unsupported run envelopes could still contain a scientific answer | Conflicting status and verdict could be silently ignored | Such envelopes become malformed rows and remain in total denominators. |
| Source overlap was computed without being exposed | Family separation could be mistaken for source separation | `source_overlap` explicitly reports cross-split source IDs and does not claim hidden access control. |
| A weaker output parser could appear to rescue invalid primary results | Well-formed verdict snippets could replace the stricter declared output contract | Explicit unique JSON-label extraction is secondary only; conflicting labels remain ambiguous, and strict malformed status is never upgraded. |
| Initial method summaries included author-written missing-evidence checklists | A document could reveal a reference judgment disguised as source content | Synthetic lists about absent clinical/protein/temperature evidence were removed; genuine source design and uncertainty notes remain. |
| Download named CO2 returned a different atmospheric time series | A familiar dataset name could silently pair wrong data and metadata | That candidate and NIST trial/example XML were excluded. Official uppercase R CO2 binary, with bounded extraction, supplies the grass observations. |
| Manual numeric transcriptions required checking | Incorrect reference means could create false system failures | Independently recomputed Mississippi chilled mean `281/15` and Quebec chilled mean `245/6`, matching corrected cases before freeze. |

These are construction qualifications, not post-result label tuning. No evaluated-system output supplied a reference answer.

## Final source and scientific-reference review

The final candidate has 32 cases (16 pairs), with all eight penguin cases in development and the 24 Puromycin/grass/FreeSolv cases in evaluation. Source families do not cross these splits. This is a public source-disjoint design, not a protected or independently adjudicated holdout; each family contributes several dependent tasks.

* **Puromycin:** R source/manual are retained under GPL-2.0-or-later with attribution and COPYING. Original thesis/full primary methods were not acquired. Direct parsing of the `.R` rate vector independently gives treated mean 131 and untreated mean 106.5 at 0.11 ppm, treated values 207 and 200 versus untreated 160 at 1.1 ppm. The source says the experiment was conducted once per condition, so 23 readings are not documented as 23 independent biological experiments. No clinical endpoint was measured in this supplied record.
* **Grass CO2:** This is the R grass cold-tolerance dataset, not atmospheric `co2`. The official serialized object has 84 readings, 12 plants and seven concentration codes per plant. A separate bounded XDR numerical-vector check reproduces Qn1 uptake 37.2 at code 350 and 35.3 at code 500. Independent grouping of the extracted source records gives Mississippi nonchilled mean `158/5`, chilled `281/15`; Quebec nonchilled `259/6`, chilled `245/6`, all at source code 1000. The R manual's concentration-unit transcription is unresolved, so packets use source codes rather than silently converting to ppm. The original primary paper was not obtained.
* **FreeSolv:** Upstream license is CC BY 4.0, with its original-source licensing qualification retained. Selected rows cite published experimental sources; no unpublished-reference row was selected. Direct semicolon parsing verifies ethanol minus methane experimental hydration values is −7 kcal/mol, triethylphosphate calculated-minus-experimental residual is −2.75 kcal/mol, and neopentane displayed values both equal 2.51 kcal/mol. The methanol 0.60 uncertainty is explicitly marked an assigned default because experimental uncertainty was unavailable. A claim that this field is a measured 95% replicate-derived confidence interval is contradicted by the source record; it must be refuted rather than merely declared insufficient. Hydration values do not supply protein-specific binding validation. Individual original experiments and standard-state corrections have not been reconstructed.
* **Penguins:** Independent source parsing confirms female/male Adélie counts 73 each and sums 245925/295175 g. The archived primary article explicitly states 39 out of 44 held-out Adélie sex classifications, 88.64%, and says those individuals were not used in developing the model. This supports the narrowly attributed reported result; it does not reproduce the original classification analysis or establish prospective universal accuracy.

No remaining scientific-reference blocker was found in these cases. `empirically_supported` denotes a narrowly source-backed reported observation or descriptive comparison, not a new independent biological validation. The distinction from `computationally_established` can be scientifically arguable for derived sample statistics; provisional labels and accepted-category analysis must remain visible, and external expert review is still required.

## Executed tests

From the independent SVB root:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -B -m unittest discover \
  -s tests -p test_phase2_adversarial.py -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -B -m unittest discover \
  -s tests -p test_phase2_references.py -v
```

The reviewer-owned suite executed **23 tests, all passed**. The separate reference suite executed **13 tests, all passed**. They test source bytes and numeric calculations, packet allowlists and private-reference exclusion, condition adjudication, citation fabrication/exact quotes, ungraded reasoning entailment, malformed overflow, denominator preservation, conflicting run status, and strict-primary versus secondary label extraction. No test result is an expert scientific adjudication.

The first draft of the new audit fixture ran against a simultaneously changing condition-reference API and produced seven fixture errors because required condition mappings were absent; adding the new declared fixture fields resolved them. That construction mismatch was not an evaluated-model failure and did not alter reference labels.

## Remaining interpretation risks

1. The public protocol and shared filesystem do not prevent investigators or tools from reading labels. Packet allowlists remove explicit gold from inference requests but cannot establish true secrecy or pretraining independence.
2. The no-assumptions condition removes a separate reminder while essential methods, units and claim definitions remain in source documents. Its references are intentionally unchanged. It is a weak annotation-removal ablation, not a decisive test of missing causal premises. No-evidence has its own references and cannot be compared as accuracy against the original full-information labels.
3. Exact citation-ID/quotation checks establish literal attribution only. A response can quote a genuine source and still reason incorrectly. Scientific reasoning accuracy remains null until blinded human rubric review is actually completed.
4. Small-source families, paired constructions and lexical cues such as “all”, “proves” and “clinical” limit external validity. A lexical baseline is needed to expose this shortcut. No broad scientific-reasoning or mechanistic-reliability claim follows from high label agreement.
5. A valid local model run is execution evidence; its parameters, truncation, format failures and full denominators must be reported. No model results had been inspected at the time of this pre-freeze scientific-reference review.
