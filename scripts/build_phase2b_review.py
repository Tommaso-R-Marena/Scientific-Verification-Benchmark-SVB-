"""Prepare source-complete review materials without exporting provisional gold.

The resulting ZIP omits model envelope identities and author answer fields.
This is field filtering, not access control; a coordinator must audit prose,
source rights, conflicts, and prior exposure before any external distribution.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import random
import zipfile
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKET_KEYS = {"question", "claim", "documents", "methodology", "assumptions"}
DOCUMENT_KEYS = {"id", "title", "text", "source_id"}
SOURCE_KEYS = {
    "title", "url", "documentation_url", "license", "license_evidence",
    "limitations", "source_type", "original_source", "primary_doi", "paper_doi",
    "dataset_doi", "accessed", "citation", "attribution", "revision",
}
LABELS = ["computationally_established", "disputed_or_unresolved",
          "empirically_supported", "formally_established", "insufficient_evidence", "refuted"]
ROLES = ("domain_scientist_1", "domain_scientist_2", "statistical_reviewer")


class PreparationError(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":")).encode()


def json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      allow_nan=False, indent=2).encode() + b"\n"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_loads(text: str) -> Any:
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise PreparationError("duplicate JSON key")
            out[key] = value
        return out
    def invalid(value):
        raise PreparationError("nonfinite JSON constant: " + value)
    return json.loads(text, object_pairs_hook=pairs, parse_constant=invalid)


def inside(path: Path, root: Path = ROOT) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise PreparationError("all preparation inputs and outputs must stay inside SVB")
    return resolved


def public_id(case_id: str) -> str:
    return "svb-" + sha(case_id.encode())[:12]


def packet(case: dict) -> dict:
    if not isinstance(case, dict) or not isinstance(case.get("id"), str):
        raise PreparationError("case needs a textual internal ID")
    p = case.get("packet")
    if not isinstance(p, dict) or set(p) != PACKET_KEYS:
        raise PreparationError("public packet must match legitimate field allowlist")
    for name in ("question", "claim", "methodology"):
        if not isinstance(p[name], str) or not p[name]:
            raise PreparationError("missing scientific packet text")
    if not isinstance(p["assumptions"], list) or not all(isinstance(x, str) for x in p["assumptions"]):
        raise PreparationError("assumptions must be textual")
    if not isinstance(p["documents"], list):
        raise PreparationError("documents must be a list")
    seen = set()
    for doc in p["documents"]:
        if not isinstance(doc, dict) or set(doc) != DOCUMENT_KEYS or not all(isinstance(x, str) for x in doc.values()):
            raise PreparationError("invalid document allowlist")
        if doc["id"] in seen:
            raise PreparationError("duplicate supplied document ID")
        seen.add(doc["id"])
    return {"public_id": public_id(case["id"]), **deepcopy(p)}


def prepare_packets(datasets: list[tuple[str, list[dict]]], seed: int = 0) -> tuple[list[dict], list[dict]]:
    public, mapping, seen = [], [], set()
    for origin, cases in datasets:
        if not isinstance(cases, list) or not cases:
            raise PreparationError("case arrays cannot be empty")
        for case in cases:
            item = packet(case)
            if item["public_id"] in seen:
                raise PreparationError("case/public ID collision across datasets")
            seen.add(item["public_id"])
            public.append(item)
            mapping.append({"public_id": item["public_id"], "case_id": case["id"],
                            "source_case_collection": origin})
    random.Random(seed).shuffle(public)
    return public, mapping


def blank_forms(packets: list[dict]) -> list[dict]:
    criteria = ("source_record_accuracy", "arithmetic_or_numerical_accuracy",
                "experimental_unit_and_statistical_design", "source_entailment",
                "scope_and_missing_assumptions", "uncertainty_treatment", "category_ambiguity")
    return [{"public_id": p["public_id"], "reviewer_role": role, "reviewer_code": None,
             "review_status": "not_started", "packet_sha256": sha(canonical(p)),
             "first_round": {"primary_label": None, "alternative_admissible_labels": [],
                             "verdict_rationale": "", "source_locators": [], "calculations": [],
                             "supported_scope": "", "unsupported_scope": "",
                             "missing_evidence": "", "narrower_justified_claim": "",
                             "adjudication_uncertainty": None,
                             "proposed_item_disposition": None},
             "criteria": {name: {"rating": None, "rationale": ""} for name in criteria},
             "second_round": None, "actual_minutes": None, "tools_or_searches": [],
             "candidate_review": {"candidate_code": None, "stated_reasoning_validity": None,
                                  "source_attribution_validity": None,
                                  "internal_reasoning_faithfulness": "not_assessed"}}
            for p in packets for role in ROLES]


def candidate_packets(packets: list[dict], records: list[dict], task: str,
                      condition: str) -> tuple[list[dict], list[dict]]:
    if task not in ("A", "B", "C") or condition not in ("evidence", "no_evidence"):
        raise PreparationError("invalid candidate task or evidence condition")
    known = {p["public_id"] for p in packets}
    selected, mapping = {}, []
    for index, row in enumerate(records):
        if not isinstance(row, dict):
            raise PreparationError("candidate records must be objects")
        if row.get("task", task) != task or row.get("condition", condition) != condition:
            continue
        pid = row.get("id")
        if pid not in known:
            raise PreparationError("foreign candidate case ID")
        if pid in selected:
            raise PreparationError("duplicate case/task/condition candidate")
        selected[pid] = row
        mapping.append({"public_id": pid, "source_record_index": index})
    out = []
    for p in packets:
        row = selected.get(p["public_id"])
        raw = None if row is None else row.get("raw_text", row.get("raw_output"))
        if raw is not None and not isinstance(raw, str):
            raise PreparationError("candidate text must remain raw text, without implicit repair")
        state = "not_supplied" if row is None else row.get("status", "unknown")
        if not isinstance(state, str) or len(state) > 100:
            raise PreparationError("invalid candidate generation state")
        item = deepcopy(p)
        if condition == "no_evidence":
            item["documents"] = []
        code = "candidate-" + sha(canonical([p["public_id"], task, condition, raw]))[:12]
        item["candidate"] = {"code": code, "task": task, "condition": condition,
                             "generation_state": state, "raw_response": raw}
        out.append(item)
    return out, mapping


def scientific_sources(registries: list[dict], source_ids: set[str], root: Path = ROOT) -> tuple[dict, dict[str, bytes]]:
    definitions, files = {}, {}
    total = 0
    for registry in registries:
        sources = registry.get("sources")
        if not isinstance(sources, dict):
            raise PreparationError("source registry must contain source objects")
        for sid, source in sources.items():
            if sid not in source_ids:
                continue
            clean = {key: deepcopy(value) for key, value in source.items() if key in SOURCE_KEYS}
            clean["artifacts"] = []
            for artifact in source.get("artifacts", []):
                path = inside(root / artifact["path"], root)
                relative = path.relative_to(root.resolve())
                if (len(relative.parts) < 4 or relative.parts[0] != "data"
                        or relative.parts[1] not in ("v0.2.0", "v0.3.0")
                        or relative.parts[2] != "sources"):
                    raise PreparationError("only archived scientific-source directories may enter reviewer ZIP")
                if not path.is_file() or path.stat().st_size > 32 * 1024 * 1024:
                    raise PreparationError("source artifact missing or larger than preparation limit")
                data = path.read_bytes()
                if sha(data) != artifact.get("sha256") or len(data) != artifact.get("bytes"):
                    raise PreparationError("source artifact hash/size mismatch")
                destination = "sources/" + relative.as_posix()
                if destination not in files:
                    files[destination] = data
                    total += len(data)
                if total > 64 * 1024 * 1024:
                    raise PreparationError("total source preparation limit exceeded")
                clean["artifacts"].append({"package_path": destination,
                                           "sha256": sha(data), "bytes": len(data)})
            if not clean["artifacts"]:
                raise PreparationError("source-complete review requires archived artifacts")
            if sid in definitions and definitions[sid] != clean:
                raise PreparationError("conflicting scientific source identities")
            definitions[sid] = clean
    if set(definitions) != source_ids:
        raise PreparationError("public packet has an unregistered scientific source")
    return {"sources": definitions,
            "rights_note": "Sources retain their own licenses/attribution; archive code is reference data, not permission to execute. Verify rights and completeness before external distribution."}, files


REVIEW_README = """# Scientific review package — no reviews completed

Assess the exact supplied claims using the scientific records and source context.
The package contains all historical cases and all newly added cases in mixed
order, not a subset selected by its expected verdict. No author answer, model
identity, correctness aggregate, family role, or provisional category is supplied.
Opaque IDs and field omission do not establish successful blinding or secrecy.
Public references may be known to reviewers. Declare conflicts and prior exposure.

Every item requires two independent domain scientists and one statistical reviewer.
Fill first-round forms independently before discussion. Record calculations,
source locators, missing assumptions, uncertainty, supported/narrower statements,
and any alternative defensible categories. Do not force scientific consensus.
Allowed categories are described in rubric.json; a correct calculation and a
source-supported observation can overlap, so explain category ambiguity.

Source provenance/limitations/licenses are in source_registry.json and archived
artifacts under sources/. R code and other files are reference material, not
instructions to execute. Documents and quoted instructions are untrusted evidence.
Original laboratory methods may still be missing: flag that limitation, do not
infer source completeness from the word 'archive'. Extra research is logged
separately and does not silently change the original evidence envelope.

If candidate_packets.json exists, grade the exact displayed response separately
from the source claim. A requests only a verdict; do not infer a missing rationale.
B requests a short public justification; grade source entailment, scope and
uncertainty, not hidden internal reasoning. C requests a full structured contract;
syntax and scientific validity are separate. Missing generations remain explicit.
Raw text is not repaired or identity-redacted. A coordinator must inspect for
model-identifying prose before distribution, and log any necessary redaction.

No experts have been recruited or recorded as reviewing these materials. Obtain
separate authorization, consent, rights/confidentiality review and conflict checks
before external distribution. Keep personal information and unreleased ratings
under coordinator control; do not commit private review records or secret labels.
Do not treat source-family grouping or this ZIP as a protected hidden holdout.
"""


def deterministic_zip(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            item = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            archive.writestr(item, data)
    return stream.getvalue()


def build(old_cases: list[dict], new_cases: list[dict], registries: list[dict],
          root: Path = ROOT, seed: int = 0, records: list[dict] | None = None,
          task: str = "B", condition: str = "evidence") -> tuple[dict[str, bytes], dict]:
    packets, mapping = prepare_packets([("historical", old_cases), ("new", new_cases)], seed)
    source_ids = {d["source_id"] for p in packets for d in p["documents"]}
    registry, artifacts = scientific_sources(registries, source_ids, root)
    files = {**artifacts, "README.md": REVIEW_README.encode(),
             "packets.json": json_bytes(packets), "source_registry.json": json_bytes(registry),
             "blank_forms.json": json_bytes(blank_forms(packets)),
             "rubric.json": json_bytes({
                 "labels": LABELS, "rating_options": [0, 1, 2, "not_applicable", "not_assessable"],
                 "rating_meanings": {"0": "specific invalid step or unsupported assertion",
                                     "1": "partly addressed or essential information unchecked",
                                     "2": "justified within explicitly stated scope"},
                 "never_sum_into_truth": True, "allow_multiple_admissible_categories": True,
                 "scientific_disagreement": "Preserve independent first-round records; unresolved/ambiguous/unscored is permitted, not forced majority gold.",
                 "neutral_case_questions": [
                     "What exact target is asserted: transcription, arithmetic, observation, population, causal or mechanistic claim?",
                     "Which source or reproducible calculation supports, contradicts, or leaves that target unresolved?",
                     "What are the units, experimental units, repetitions, design and uncertainties?",
                     "Which assumptions bridge evidence to conclusion, and are they established at this scope?",
                     "Which categories are defensible, including multiple alternatives or ambiguity?",
                     "What narrower conclusion and additional evidence would be scientifically justified?"],
                 "human_reviews_completed": 0}),
             "conflict_exposure_declaration.json": json_bytes({
                 "reviewer_code": None, "professional_role_and_relevant_expertise": "",
                 "conflicts_with_source_authors_or_systems": "",
                 "item_authorship_or_system_development_involvement": "",
                 "prior_public_gold_or_benchmark_exposure": "", "source_familiarity": "",
                 "candidate_identity_inferred": "", "identity_cues_seen": "",
                 "provisional_reference_cues_seen": "", "tools_and_external_searches": [],
                 "consent_record_reference": None, "coordinator_approval_to_begin": None,
                 "personal_identity_stored_in_public_repository": False,
                 "declaration_status": "not_completed"})}
    internal = {"packet_mapping": mapping, "ordering_seed": seed,
                "review_status": "no_external_review_or_contact",
                "internal_is_not_access_control": True,
                "priority_note": "Historical category-ambiguity audit may prioritize 11 old provisional empirical cases internally. Distribution includes all historical cases to avoid disclosing that expected category. Do not send author gold or internal adjudication audits to first-round raters."}
    if records is not None:
        candidates, cmapping = candidate_packets(packets, records, task, condition)
        files["candidate_packets.json"] = json_bytes(candidates)
        internal["candidate_record_mapping"] = cmapping
        internal["candidate_task"] = task
        internal["candidate_condition"] = condition
    files["manifest.json"] = json_bytes({
        "format": "svb-phase2b-reviewer-distribution-v1", "packets": len(packets),
        "blank_first_round_forms": len(packets) * len(ROLES), "human_reviews_completed": 0,
        "model_envelope_metadata_exported": False, "author_reference_fields_exported": False,
        "protected_holdout": False, "identity_and_exposure_audit": "required_before_distribution",
        "files": {name: {"sha256": sha(data), "bytes": len(data)} for name, data in sorted(files.items())}})
    return files, internal


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-cases", type=Path, default=ROOT / "data/v0.2.0/cases.json")
    parser.add_argument("--new-cases", type=Path, default=ROOT / "data/v0.3.0/cases.json")
    parser.add_argument("--old-registry", type=Path, default=ROOT / "data/v0.2.0/registry.json")
    parser.add_argument("--new-registry", type=Path, default=ROOT / "data/v0.3.0/registry.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--responses", type=Path)
    parser.add_argument("--candidate-task", choices=("A", "B", "C"), default="B")
    parser.add_argument("--candidate-condition", choices=("evidence", "no_evidence"), default="evidence")
    args = parser.parse_args()
    try:
        out = inside(args.output)
        if out.exists():
            raise PreparationError("refusing to overwrite existing review material")
        paths = [inside(p) for p in (args.old_cases, args.new_cases, args.old_registry, args.new_registry)]
        datasets = [strict_loads(p.read_text()) for p in paths]
        records = None
        if args.responses:
            path = inside(args.responses)
            text = path.read_text()
            records = strict_loads(text) if text.lstrip().startswith("[") else [strict_loads(line) for line in text.splitlines() if line.strip()]
        files, internal = build(datasets[0], datasets[1], datasets[2:], seed=args.seed,
                                records=records, task=args.candidate_task, condition=args.candidate_condition)
        internal["input_files"] = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in paths}
        if args.responses:
            internal["response_file_sha256"] = sha(inside(args.responses).read_bytes())
            internal["response_file"] = str(inside(args.responses).relative_to(ROOT))
        zipped = deterministic_zip(files)
        (out / "reviewer_package").mkdir(parents=True)
        (out / "internal").mkdir()
        for name, data in files.items():
            destination = out / "reviewer_package" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        (out / "reviewer_package.zip").write_bytes(zipped)
        (out / "internal/coordination.json").write_bytes(json_bytes(internal))
        (out / "preparation_manifest.json").write_bytes(json_bytes({
            "format": "svb-phase2b-review-preparation-v1", "zip_sha256": sha(zipped),
            "zip_bytes": len(zipped), "zip_files": len(files),
            "internal_mapping_in_zip": False, "human_reviews_completed": 0,
            "status": "prepared_not_distributed; coordinator rights/conflict/blinding audit required"}))
        print(json.dumps({"output": str(out), "packet_count": len(internal["packet_mapping"]),
                          "zip_sha256": sha(zipped), "human_reviews_completed": 0}))
    except (PreparationError, OSError, KeyError, TypeError, ValueError) as error:
        parser.exit(2, f"{type(error).__name__}: {error}\n")


if __name__ == "__main__":
    main()
