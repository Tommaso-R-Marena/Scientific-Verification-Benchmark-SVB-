"""Prepare public review packets; field omission is not access-control or blinding.

Run from the independent project. No reference label, checker, family, pair role,
model identity or aggregate score is copied to a review packet. Raw answer bodies
are preserved: a human coordinator must audit identity cues before distribution.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import random
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from svb.core import Invalid, loads  # noqa: E402
from svb.phase2 import CONDITIONS, build_prompt, public_id  # noqa: E402


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def project_path(path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise Invalid("review inputs and outputs must stay inside independent project")
    return resolved


def prepare(cases: list[dict], condition: str, split: str = "all",
            seed: int = 0) -> list[dict]:
    if split not in ("all", "dev", "evaluation"):
        raise Invalid("invalid review split")
    packets = []
    seen = set()
    for case in cases:
        if split != "all" and case.get("split") != split:
            continue
        pid = public_id(case)
        if pid in seen:
            raise Invalid("duplicate review identifier")
        seen.add(pid)
        # Reuse the model's exact public evidence transformation, then copy only
        # the legitimate packet; do not expose model instruction text to raters.
        prompt = build_prompt(case, condition)
        packet = loads(prompt["messages"][-1]["content"])
        packets.append({"public_id": pid, **packet})
    if not packets:
        raise Invalid("no review cases selected")
    random.Random(seed).shuffle(packets)
    return packets


def attach_responses(packets: list[dict], records: list[dict], condition: str,
                     seed: int = 0) -> list[dict]:
    known = {p["public_id"] for p in packets}
    selected = {}
    for record in records:
        if record.get("condition", condition) != condition:
            continue
        pid = record.get("id")
        if pid not in known:
            raise Invalid("response refers to a foreign review ID; select matching split")
        if pid in selected:
            raise Invalid("duplicate response for review ID")
        selected[pid] = record
    out = []
    for packet in packets:
        pid = packet["public_id"]
        record = selected.get(pid)
        raw = None
        if record is not None:
            raw = record.get("raw_text", record.get("raw_output"))
            if raw is not None and not isinstance(raw, str):
                raise Invalid("raw response must be text; no implicit response repair")
        status = "missing" if record is None else record.get("status", "unknown")
        if not isinstance(status, str) or len(status) > 100:
            raise Invalid("invalid response status")
        # No provider/model/version/latency/token/cost metadata is retained.
        # Identity could remain inside raw text; never rewrite that text here.
        candidate_code = "candidate-" + sha(canonical([pid, seed, raw]))[:12]
        out.append({**deepcopy(packet), "candidate_code": candidate_code,
                    "response_status": status, "candidate_response": raw})
    return out


def read_records(path: Path) -> list[dict]:
    text = path.read_text()
    if text.lstrip().startswith("["):
        records = loads(text)
    else:
        records = [loads(line) for line in text.splitlines() if line.strip()]
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise Invalid("response records must be JSON objects in an array or JSONL")
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "data/v0.2.0/cases.json")
    parser.add_argument("--output", type=Path, required=True,
                        help="Fresh project-local output directory; never overwrite existing review data")
    parser.add_argument("--condition", choices=CONDITIONS, default="evidence")
    parser.add_argument("--split", choices=("all", "dev", "evaluation"), default="all")
    parser.add_argument("--seed", type=int, default=0,
                        help="Public ordering seed, not a cryptographic secret")
    parser.add_argument("--responses", type=Path,
                        help="One system's raw JSON/JSONL run file; no identity metadata exported")
    args = parser.parse_args()
    try:
        cases_path = project_path(args.cases)
        output = project_path(args.output)
        if output.exists():
            raise Invalid("refusing to overwrite an existing review directory")
        cases = loads(cases_path.read_text())
        if not isinstance(cases, list) or not all(isinstance(x, dict) for x in cases):
            raise Invalid("cases must be an array of objects")
        packets = prepare(cases, args.condition, args.split, args.seed)
        inputs = {"case_file_sha256": sha(cases_path.read_bytes())}
        stage = "reference_qualification"
        if args.responses:
            response_path = project_path(args.responses)
            inputs["response_file_sha256"] = sha(response_path.read_bytes())
            packets = attach_responses(packets, read_records(response_path),
                                       args.condition, args.seed)
            stage = "candidate_assessment"
        output.mkdir(parents=True)
        packet_bytes = json.dumps(packets, sort_keys=True, indent=2,
                                  ensure_ascii=False, allow_nan=False).encode() + b"\n"
        (output / "packets.json").write_bytes(packet_bytes)
        manifest = {
            "format": "svb-human-review-preparation-v1", "stage": stage,
            "review_status": "not_reviewed_by_external_humans",
            "packet_count": len(packets), "condition": args.condition,
            "ordering_seed": args.seed, "packet_sha256": sha(packet_bytes), **inputs,
            "blinding_status": "metadata_filtered; coordinator identity-cue and exposure audit required",
            "protected_holdout": False,
            "source_identity": "intentionally retained for evidence/provenance assessment",
            "secret_labels_committed": False,
            "limitation": "Shared public workspace; opaque IDs and omitted references do not guarantee blindness or secrecy.",
        }
        (output / "manifest.json").write_text(
            json.dumps(manifest, sort_keys=True, indent=2, allow_nan=False) + "\n")
        print(json.dumps({"packets": len(packets), "stage": stage,
                          "output": str(output), "human_reviews_performed": 0}))
    except (Invalid, OSError, KeyError, TypeError, ValueError) as exc:
        parser.exit(2, f"{type(exc).__name__}: {exc}\n")


if __name__ == "__main__":
    main()
