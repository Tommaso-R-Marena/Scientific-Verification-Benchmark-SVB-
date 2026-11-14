"""Finite-model certificate correctness, decision utility, and descriptive cost.

Only fixed local FoldBounds commands are executed. Reference probabilities come
from SVB's independent exact enumerator, never the subject's output.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import statistics
import subprocess
import sys
import time
from typing import Any

from .phase2_systems import extended_lattice

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = ROOT / "data/v0.3.0/bound_utility_protocol.json"
LOCAL = ROOT / "results/local/bound-utility"
OUT = ROOT / "results/v0.3.0"


def threshold_decision(lower: Fraction, upper: Fraction, threshold: Fraction) -> str:
    """Certify the target P>=t with exact, asymmetric endpoint handling."""
    if not 0 <= lower <= upper <= 1 or not 0 <= threshold <= 1:
        raise ValueError("invalid probability interval or decision threshold")
    if lower >= threshold:
        return "yes"
    if upper < threshold:
        return "no"
    return "undecided"


def audit_interval(exact: Fraction, lower: Fraction, upper: Fraction,
                   thresholds: list[Fraction]) -> dict[str, Any]:
    if not 0 <= exact <= 1:
        raise ValueError("invalid independent reference probability")
    enclosed = 0 <= lower <= exact <= upper <= 1
    decisions = []
    for t in thresholds:
        outcome = threshold_decision(lower, upper, t)
        oracle = "yes" if exact >= t else "no"
        decisions.append({"threshold": str(t), "decision": outcome, "oracle_classification": oracle,
                          "wrong_definite_decision": outcome != "undecided" and outcome != oracle,
                          "is_reference_equality": t == exact, "is_boundary": t in (0, 1)})
    return {"enclosed": enclosed, "probability_width": str(upper-lower),
            "decisions": decisions,
            "wrong_definite_decisions": sum(d["wrong_definite_decision"] for d in decisions),
            "valid": enclosed and not any(d["wrong_definite_decision"] for d in decisions)}


def environment(repo: Path) -> dict[str, str]:
    return {"PATH": os.defpath, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "PYTHONPATH": str(repo / "src"), "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONNOUSERSITE": "1", "TMPDIR": str(LOCAL), "HOME": str(LOCAL)}


def execute(command: list[str], repo: Path, timeout: int) -> dict[str, Any]:
    start = time.perf_counter()
    try:
        completed = subprocess.run(command, cwd=ROOT, env=environment(repo),
                                   capture_output=True, timeout=timeout, check=False)
        if len(completed.stdout) + len(completed.stderr) > 1048576:
            raise ValueError("subject output exceeds protocol cap")
        return {"returncode": completed.returncode, "stdout": completed.stdout.decode(errors="replace"),
                "stderr": completed.stderr.decode(errors="replace"),
                "seconds": time.perf_counter()-start, "command": command}
    except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
        return {"execution_error": type(exc).__name__ + ": " + str(exc),
                "seconds": time.perf_counter()-start, "command": command}


def summarize(rows: list[dict[str, Any]], configurations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries = []
    for config in configurations:
        for role in ("all", "nontrivial", "positive_control", "negative_control"):
            selected = [r for r in rows if r["configuration"] == config["id"] and (role == "all" or r["role"] == role)]
            parsed = [r for r in selected if "audit" in r]
            decision_rows = [d for r in selected for d in r["decisions"]]
            counts = Counter(d["decision"] for d in decision_rows)
            decided = counts["yes"] + counts["no"]
            nonboundary = [d for d in decision_rows if not d["is_boundary"]]
            nonboundary_decided = sum(d["decision"] in ("yes", "no") for d in nonboundary)
            times = [r["elapsed_seconds"] for r in selected if "elapsed_seconds" in r]
            summaries.append({"configuration": config["id"], "role": role,
                              "expected_calls": len(selected), "parsed_calls": len(parsed),
                              "valid_enclosures": sum(r["audit"]["enclosed"] and r["partition_enclosed"] for r in parsed),
                              "outcomes": dict(sorted(Counter(r["outcome"] for r in selected).items())),
                              "expected_decisions": len(decision_rows), "decision_counts": dict(sorted(counts.items())),
                              "decided": decided, "decision_coverage": decided/len(decision_rows) if decision_rows else None,
                              "nonboundary_decision_denominator": len(nonboundary),
                              "nonboundary_decided": nonboundary_decided,
                              "nonboundary_decision_coverage": nonboundary_decided/len(nonboundary) if nonboundary else None,
                              "wrong_definite_decisions": sum(d.get("wrong_definite_decision", False) for d in decision_rows),
                              "reference_equality_decisions": dict(sorted(Counter(d["decision"] for d in decision_rows if d["is_reference_equality"]).items())),
                              "mean_probability_width": str(sum((Fraction(r["audit"]["probability_width"]) for r in parsed),Fraction())/len(parsed)) if parsed else None,
                              "median_wall_seconds": statistics.median(times) if times else None,
                              "minimum_wall_seconds": min(times) if times else None,
                              "maximum_wall_seconds": max(times) if times else None})
    return summaries


def run(repo: Path = Path("/workspace/FoldBounds")) -> dict[str, Any]:
    LOCAL.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    protocol_bytes = PROTOCOL.read_bytes()
    protocol_hash = hashlib.sha256(protocol_bytes).hexdigest()
    frozen = (OUT / "bound_utility_protocol.sha256").read_text().split()[0]
    if protocol_hash != frozen:
        raise ValueError("frozen bound utility protocol changed")
    protocol = json.loads(protocol_bytes)
    if len(protocol["families"])*len(protocol["configurations"]) > protocol["call_budget"]:
        raise ValueError("configured experiment exceeds frozen call budget")
    references = {}
    # Establish all reference values, including equality thresholds, before any
    # subject invocation. This cannot adapt to observed subject failures.
    for family in protocol["families"]:
        reference = extended_lattice(family["sequence"], Fraction(family["q"]), family["event_contact_threshold"])
        known = {8:543, 9:1479, 10:4067}[len(family["sequence"])]
        if reference["paths"] != known:
            raise ValueError("independent reference violates known SAW count")
        references[family["id"]] = reference
    rows = []
    available = (repo / "src/foldbounds/__main__.py").is_file()
    for family in protocol["families"]:
        reference = references[family["id"]]
        exact_p, exact_z = Fraction(reference["probability"]), Fraction(reference["partition"])
        thresholds = sorted({*(Fraction(t) for t in protocol["decision_thresholds"]), exact_p})
        for config in protocol["configurations"]:
            depth = len(family["sequence"]) if config["depth"] == "N" else config["depth"]
            row: dict[str, Any] = {"family": family["id"], "role": family["role"],
                                  "configuration": config["id"], "depth": depth,
                                  "decisions": [{"threshold": str(t), "decision": "unsupported" if not available else "execution_error",
                                                 "oracle_classification": "yes" if exact_p >= t else "no",
                                                 "is_reference_equality": t == exact_p, "is_boundary": t in (0,1),
                                                 "wrong_definite_decision": False} for t in thresholds]}
            if not available:
                row.update(outcome="unsupported", reason="read-only subject source is unavailable; no mock or build used")
                rows.append(row)
                continue
            command = [sys.executable, "-B", "-m", "foldbounds", family["sequence"],
                       "--q", family["q"], "--event-at-least", str(family["event_contact_threshold"]),
                       "--depth", str(depth), *config["args"]]
            execution = execute(command, repo, protocol["limits"]["timeout_seconds"])
            row.update(execution=execution, elapsed_seconds=execution["seconds"])
            try:
                if execution.get("returncode") != 0:
                    raise ValueError("subject did not execute normally")
                observed = json.loads(execution["stdout"])
                lower, upper = [Fraction(v) for v in observed["event_probability_interval"]]
                zlo, zhi = [Fraction(v) for v in observed["partition_interval"]]
                row["audit"] = audit_interval(exact_p, lower, upper, thresholds)
                row["decisions"] = row["audit"]["decisions"]
                row["partition_enclosed"] = zlo <= exact_z <= zhi
                row["relative_partition_width"] = str((zhi-zlo)/exact_z)
                row["observed"] = {"probability_interval": [str(lower),str(upper)],
                                   "partition_interval": [str(zlo),str(zhi)],
                                   "exact_paths": observed["exact_paths"], "bounded_subtrees": observed["bounded_subtrees"]}
                row["full_depth_exact"] = config["id"] != "full" or lower == upper == exact_p and zlo == zhi == exact_z
                row["outcome"] = "valid" if row["audit"]["valid"] and row["partition_enclosed"] and row["full_depth_exact"] else "refuted"
            except (KeyError, ValueError, TypeError, ZeroDivisionError) as exc:
                row.update(outcome="execution_error", reason=str(exc))
            rows.append(row)
    commit = None
    git = shutil.which("git")
    if available and git:
        commit_result = execute([git,"-C",str(repo),"rev-parse","HEAD"],repo,10)
        commit = commit_result.get("stdout","").strip()
    return {"format":"svb-bound-utility-v0.3.0", "protocol_sha256":protocol_hash,
            "subject":{"path":str(repo),"commit":commit},
            "runtime":{"python":platform.python_version(),"platform":platform.platform()},
            "reference_method":"independent SVB N<=10 anchored self-avoiding-walk enumeration and exact Fraction weights",
            "references":references,"rows":rows,"summaries":summarize(rows,protocol["configurations"]),
            "expected_cli_calls":protocol["call_budget"],"actual_cli_calls":sum("execution" in r for r in rows),
            "interpretation":protocol["interpretation"]}


def sanitized(result: dict[str, Any]) -> dict[str, Any]:
    def clean(value: Any) -> Any:
        if isinstance(value,dict):
            return {key:clean(item) for key,item in value.items() if key != "execution"}
        if isinstance(value,list):
            return [clean(item) for item in value]
        return value
    return clean(result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--foldbounds-root",type=Path,default=Path("/workspace/FoldBounds"))
    args = parser.parse_args()
    result = run(args.foldbounds_root)
    (LOCAL/"raw.json").write_text(json.dumps(result,indent=2)+"\n")
    (OUT/"bound_utility.json").write_text(json.dumps(sanitized(result),indent=2)+"\n")
    print(json.dumps({"calls":result["actual_cli_calls"],"outcomes":dict(Counter(r["outcome"] for r in result["rows"])),
                      "decisions":sum(len(r["decisions"]) for r in result["rows"]),
                      "wrong_definite_decisions":sum(d["wrong_definite_decision"] for r in result["rows"] for d in r["decisions"])}))


if __name__ == "__main__":
    main()
