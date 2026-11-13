"""Optional, noninvasive conformance runs against real local scientific tools.

No evaluated-system output constructs a reference answer. Subject checkouts are
read-only inputs; all temporary files are placed under the independent project.
Arbitrary submitted code/commands are never executed by this adapter.
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from fractions import Fraction
from typing import Any

PROJECT = Path(__file__).resolve().parents[2]
PROTOCOL = PROJECT / "data/system_protocol.json"


def canonical(value: Any) -> bytes:
    """Canonical encoding for our integer/string-only test protocol."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_lattice(sequence: str, q: Fraction, threshold: int) -> dict[str, Any]:
    """Independent exhaustive anchored SAW enumeration with pairwise contacts.

    The first edge is fixed east, removing the factor of four for rotations.
    Reflections remain distinct. No FoldBounds code is used here.
    """
    if len(sequence) < 2 or len(sequence) > 7 or set(sequence) - {"H", "P"} or q < 1:
        raise ValueError("outside frozen small-model specification")
    counts: Counter[int] = Counter()
    path = [(0, 0), (1, 0)]
    visited = set(path)

    def visit() -> None:
        if len(path) == len(sequence):
            contacts = sum(
                sequence[i] == sequence[j] == "H"
                and abs(path[i][0] - path[j][0]) + abs(path[i][1] - path[j][1]) == 1
                for i in range(len(path)) for j in range(i + 2, len(path))
            )
            counts[contacts] += 1
            return
        x, y = path[-1]
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            point = x + dx, y + dy
            if point not in visited:
                path.append(point)
                visited.add(point)
                visit()
                visited.remove(point)
                path.pop()

    visit()
    z = sum((n * q**k for k, n in counts.items()), Fraction())
    event = sum((n * q**k for k, n in counts.items() if k >= threshold), Fraction())
    return {"spectrum": dict(sorted(counts.items())), "paths": sum(counts.values()),
            "partition": str(z), "probability": str(event / z)}


def csv_reference(left: str, right: str) -> dict[str, Any]:
    """Independent standard-library parser for the frozen valid fixtures."""
    tables = [list(csv.reader(io.StringIO(text), strict=True)) for text in (left, right)]
    if any(not t or t[0] != ["id"] and t[0] != ["id", "value"] for t in tables):
        raise ValueError("unexpected fixture heading")
    if any(any(len(row) != len(table[0]) for row in table[1:]) for table in tables):
        raise ValueError("nonrectangular fixture")
    a, b = [Counter(row[0] for row in table[1:]) for table in tables]
    shared = sorted(set(a) & set(b), key=lambda s: s.encode())
    return {"shared_ids": len(shared), "shared": shared,
            "left_rows": sum(a.values()), "right_rows": sum(b.values()),
            "left_repeated_rows": sum(a.values()) - len(a),
            "right_repeated_rows": sum(b.values()) - len(b),
            "left_affected_rows": sum(a[k] for k in shared),
            "right_affected_rows": sum(b[k] for k in shared)}


def _environment(project: Path, pythonpath: Path | None = None) -> dict[str, str]:
    # No API tokens, proxies, identity credentials or inherited subject hooks.
    env = {"PATH": os.defpath, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
           "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
           "TMPDIR": str(project / "results"), "HOME": str(project / "results")}
    if pythonpath is not None:
        env["PYTHONPATH"] = str(pythonpath)
    return env


def _execute(command: list[str], project: Path, pythonpath: Path | None = None) -> dict[str, Any]:
    start = time.perf_counter()
    try:
        # Only commands constructed by this module, never from benchmark submissions.
        proc = subprocess.run(command, cwd=project, env=_environment(project, pythonpath),
                              capture_output=True, timeout=30, check=False)
        if len(proc.stdout) + len(proc.stderr) > 1048576:
            raise ValueError("subject output exceeded protocol limit")
        return {"returncode": proc.returncode, "stdout": proc.stdout.decode(errors="replace"),
                "stderr": proc.stderr.decode(errors="replace"),
                "seconds": time.perf_counter() - start, "command": command}
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        return {"execution_error": type(exc).__name__ + ": " + str(exc),
                "seconds": time.perf_counter() - start, "command": command}


def _row(case_id: str, expected: Any, observed: Any, valid: bool, execution: dict[str, Any]) -> dict[str, Any]:
    execution_failed = "execution_error" in execution or (not valid and execution.get("returncode", 0) != 0)
    return {"id": case_id, "expected": expected, "observed": observed,
            "outcome": "execution_error" if execution_failed else "valid" if valid else "refuted",
            "execution": execution}


def _metadata(repo: Path, project: Path) -> dict[str, Any]:
    if not repo.is_dir():
        return {"available": False, "path": str(repo)}
    # Git read operations only; do not run status, hooks, builds or package installers.
    proc = _execute([shutil.which("git") or "git", "-C", str(repo), "rev-parse", "HEAD"], project)
    return {"available": True, "path": str(repo), "commit": proc.get("stdout", "").strip()}


def evaluate_foldbounds(repo: Path, project: Path, protocol: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    python = Path(sys.executable)
    if not (repo / "src/foldbounds/__main__.py").is_file():
        return {"rows": [{"id": "subject", "outcome": "unsupported", "reason": "FoldBounds checkout unavailable"}]}
    for family in protocol["families"]:
        sequence, q, threshold = family["sequence"], Fraction(family["q"]), family["threshold"]
        reference = exact_lattice(sequence, q, threshold)
        previous = None
        for depth in sorted({2, min(4, len(sequence)), len(sequence)}):
            command = [str(python), "-B", "-m", "foldbounds", sequence, "--q", str(q),
                       "--event-at-least", str(threshold), "--depth", str(depth)]
            execution = _execute(command, project, repo / "src")
            observed: Any = None
            valid = False
            try:
                if execution.get("returncode") != 0:
                    raise ValueError("subject returned nonzero")
                observed = json.loads(execution["stdout"])
                z = [Fraction(x) for x in observed["partition_interval"]]
                p = [Fraction(x) for x in observed["event_probability_interval"]]
                valid = z[0] <= Fraction(reference["partition"]) <= z[1] and p[0] <= Fraction(reference["probability"]) <= p[1]
                if previous:
                    valid = valid and previous[0][0] <= z[0] <= z[1] <= previous[0][1] and previous[1][0] <= p[0] <= p[1] <= previous[1][1]
                if depth == len(sequence):
                    valid = valid and z[0] == z[1] == Fraction(reference["partition"]) and p[0] == p[1] == Fraction(reference["probability"])
                previous = z, p
            except (ValueError, KeyError, TypeError, ZeroDivisionError) as exc:
                execution["execution_error"] = str(exc)
            rows.append(_row(f"{sequence}-q{q}-t{threshold}-depth{depth}", reference, observed, valid, execution))
    for invalid in protocol["invalid"]:
        execution = _execute([str(python), "-B", "-m", "foldbounds", invalid["sequence"], "--q", invalid["q"]], project, repo / "src")
        rows.append(_row("reject-" + invalid["sequence"] + "-q" + invalid["q"], "nonzero exit", execution.get("returncode"),
                         isinstance(execution.get("returncode"), int) and execution["returncode"] != 0, execution))
    return {"rows": rows, "scope": "Small anchored finite 2D HP model; no physical protein validation or Lean proof replay."}


def _verify_pcs_fixture(fixture: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    """Independent third-party crypto + exact H/O stoichiometry reference."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    public = base64.b64decode(metadata["public_key_raw_base64"], validate=True)
    key = Ed25519PublicKey.from_public_bytes(public)
    manifest = json.loads((fixture / "package_manifest.json").read_bytes())
    for name, expected in manifest["files"].items():
        data = (fixture / name).read_bytes()
        if len(data) != expected["size"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise ValueError("independent manifest hash check failed")
    for name in ("package_signature.json", "certificate_signature.json"):
        sig = json.loads((fixture / name).read_bytes())
        payload = canonical(sig["payload"])
        if hashlib.sha256(payload).hexdigest() != sig["payload_sha256"]:
            raise ValueError("signature payload digest differs")
        key.verify(base64.b64decode(sig["signature"], validate=True), payload)
    certificate = json.loads((fixture / "certificate.json").read_bytes())
    predicate = certificate["claims"][0]["predicate"]
    # Explicit atom dictionary is independently specified, avoiding subject formula parsers.
    atoms = {"H2": {"H": 2}, "O2": {"O": 2}, "H2O": {"H": 2, "O": 1}}
    totals = []
    for side in ("reactants", "products"):
        count: Counter[str] = Counter()
        for term in predicate[side]:
            for element, n in atoms[term["formula"]].items():
                count[element] += term["coefficient"] * n
        totals.append(dict(count))
    if totals[0] != totals[1] or predicate["type"] != "reaction_balance":
        raise ValueError("independent atom count refutes positive fixture")
    return {"atom_counts": totals, "signed_file_hashes_checked": len(manifest["files"]),
            "independent_ed25519_signatures_checked": 2,
            "limitation": "Signature/hash and stoichiometry checks do not independently reimplement every PCS package admission rule."}


def evaluate_pcs(repo: Path, project: Path, protocol: dict[str, Any]) -> dict[str, Any]:
    binary = repo / "formal/.lake/build/bin/pcs-lean-authority"
    fixture = repo / protocol["fixture"]
    if not binary.is_file() or not fixture.is_dir():
        return {"rows": [{"id": "subject", "outcome": "unsupported", "reason": "Compiled authority or signed fixture unavailable; no subject build attempted"}]}
    metadata = json.loads((fixture / "metadata.json").read_bytes())
    try:
        reference = _verify_pcs_fixture(fixture, metadata)
    except Exception as exc:
        return {"rows": [{"id": "reference", "outcome": "execution_error", "reason": str(exc)}]}
    rows = []
    with tempfile.TemporaryDirectory(prefix="svb-pcs-", dir=project / "results") as directory:
        work = Path(directory)
        package = work / "package"
        # Copy known nonsensitive test vectors only. No source, config or credential files.
        manifest = json.loads((fixture / "package_manifest.json").read_bytes())
        for rel in [*manifest["files"], "certificate_signature.json", "package_signature.json", "package_manifest.json"]:
            dest = package / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((fixture / rel).read_bytes())
        certificate = json.loads((fixture / "certificate.json").read_bytes())
        transcript = {"format": "pcs-lean-authority-observations-v1",
                      "certificate_semantic_hash": certificate["semantic_hash"],
                      "checker_version": certificate["checker_version"], "workflow_ok": True,
                      "workflow_analysis": [], "environment_capture": None,
                      "replay": [{"evidence_id": "E1", "kind": "computational_test", "outcome": "PASS"}]}
        transcript_path = work / "observations.json"
        artifact = package / "artifacts/fixture.bin"
        original = artifact.read_bytes()
        for case in protocol["cases"]:
            artifact.write_bytes(original)
            transcript["replay"][0]["outcome"] = "FAIL" if case == "failed_observation" else "PASS"
            transcript_path.write_bytes(b"{}" if case == "malformed_transcript" else canonical(transcript))
            if case == "artifact_byte_corruption":
                artifact.write_bytes(bytes([original[0] ^ 1]) + original[1:])
                assert hashlib.sha256(artifact.read_bytes()).hexdigest() != manifest["files"]["artifacts/fixture.bin"]["sha256"]
            execution = _execute([str(binary), str(package), metadata["public_key_raw_base64"], str(transcript_path), metadata["public_key_fingerprint"]], project)
            observed = execution.get("stdout", "").strip()
            if case == "malformed_transcript":
                expected = "nonzero exit"
                valid = execution.get("returncode", 0) != 0
            else:
                expected = "ACCEPT" if case == "signed_balanced_positive" else "REJECT"
                valid = execution.get("returncode") == 0 and (observed == "ACCEPT" if expected == "ACCEPT" else observed.startswith("REJECT"))
            rows.append(_row(case, expected, observed, valid, execution))
            if case in protocol.get("unscored_reference_error_cases", []):
                rows[-1]["outcome"] = "reference_error"
                rows[-1]["score_eligible"] = False
                rows[-1]["adjudication"] = (
                    "Initial REJECT expectation was erroneous. The builtin Lean atom-balance checker "
                    "takes priority over transcript reports; the chemically balanced claim remains "
                    "true. Retained as an unscored diagnostic, not a PCS defect or a hidden-label result."
                )
    return {"rows": rows, "independent_reference": reference, "binary_sha256": sha256(binary),
            "scope": "One signed known atom-balance fixture plus byte/transcript rejection controls; not general scientific inference or adversarial security certification."}


def evaluate_site(repo: Path, project: Path, protocol: dict[str, Any]) -> dict[str, Any]:
    module = repo / "public/file-check-core.mjs"
    node = shutil.which("node")
    if not node or not module.is_file():
        return {"rows": [{"id": "subject", "outcome": "unsupported", "reason": "Node or actual JS module unavailable"}]}
    rows = []
    for case in protocol["cases"]:
        # Frozen strings passed through JSON literals, never interpreted as code.
        code = f'''import * as m from {json.dumps(module.as_uri())};
const c={json.dumps(case)};
try {{
 const result=m.analyze(m.parseCSV(m.utf8(c.left)),m.parseCSV(m.utf8(c.right)),[0,0]);
 const report=m.reportHTML({{name:'SVB local check',inputs:[{{name:'a',sha256:'0'.repeat(64)}},{{name:'b',sha256:'0'.repeat(64)}}],columns:[{{header:'id'}},{{header:'id'}}],result,localReceipt:null}});
 console.log(JSON.stringify({{accepted:true,result,browser_scope:report.includes('Browser calculation. No local Lean check was run.'),study_scope:report.includes('does not establish that the data is correct or suitable for a study')}}));
}} catch(e) {{ console.log(JSON.stringify({{accepted:false,error:e.message}})); }}'''
        execution = _execute([node, "--input-type=module", "--eval", code], project)
        observed = None
        expected: Any = "reject malformed CSV"
        valid = False
        try:
            observed = json.loads(execution["stdout"])
            if case["accepted"]:
                expected = csv_reference(case["left"], case["right"])
                valid = observed["accepted"] and observed["browser_scope"] and observed["study_scope"]
                if observed["accepted"]:
                    valid = valid and all(observed["result"]["summary"][k] == v for k, v in expected.items() if k != "shared")
                    valid = valid and [x["id"] for x in observed["result"]["shared"]] == expected["shared"]
            else:
                valid = observed["accepted"] is False
        except (ValueError, KeyError, TypeError) as exc:
            execution["execution_error"] = str(exc)
        rows.append(_row(case["id"], expected, observed, valid, execution))
    return {"rows": rows, "module_sha256": sha256(module),
            "scope": "Actual JS parser/intersection/report strings, not DOM rendering or production interface usability."}


def run(subject_root: Path = Path("/workspace"), project: Path = PROJECT) -> dict[str, Any]:
    protocol_bytes = PROTOCOL.read_bytes()
    protocol = json.loads(protocol_bytes)
    (project / "results").mkdir(exist_ok=True)
    systems = {}
    for name, directory, evaluate in (("foldbounds", "FoldBounds", evaluate_foldbounds),
                                      ("pcs", "proof-carrying-science", evaluate_pcs),
                                      ("site", "proof-carrying-science-site", evaluate_site)):
        repo = subject_root / directory
        result = evaluate(repo, project, protocol[name])
        counts = Counter(row["outcome"] for row in result["rows"])
        systems[name] = {**_metadata(repo, project), **result, "denominator": len(result["rows"]),
                         "eligible_denominator": sum(row.get("score_eligible", True) and row["outcome"] not in ("unsupported", "execution_error") for row in result["rows"]),
                         "outcomes": {k: counts.get(k, 0) for k in ("valid", "refuted", "execution_error", "unsupported", "reference_error")}}
    node = shutil.which("node")
    node_version = _execute([node, "--version"], project).get("stdout", "").strip() if node else None
    return {"format": "svb-system-evaluations-v1", "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
            "runtime": {"python": platform.python_version(), "platform": platform.platform(), "node": node_version},
            "systems": systems, "interpretation": protocol["interpretation"],
            "security_scope": "Known local tools only, minimal child environment and timeout; not a sandbox for arbitrary submitted programs."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject-root", type=Path, default=Path("/workspace"))
    parser.add_argument("--output", type=Path, default=PROJECT / "results/local/system_evaluations.json")
    args = parser.parse_args()
    destination = args.output.resolve()
    if not destination.is_relative_to(PROJECT):
        parser.error("all writes must stay inside the independent project")
    result = run(args.subject_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({name: value["outcomes"] for name, value in result["systems"].items()}))


if __name__ == "__main__":
    main()
