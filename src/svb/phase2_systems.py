"""Phase II frozen local conformance experiments; all subject checkouts read-only."""
from __future__ import annotations

import argparse
import base64
from collections import Counter
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any

PROJECT = Path(__file__).resolve().parents[2]
PROTOCOL = PROJECT / "data/v0.2.0/system_protocol.json"
LOCAL = PROJECT / "results/local/phase2"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extended_lattice(sequence: str, q: Fraction, threshold: int) -> dict[str, Any]:
    """Independent DFS over every anchored lattice SAW, without subject imports."""
    if not 2 <= len(sequence) <= 10 or set(sequence) - {"H", "P"} or q < 1:
        raise ValueError("outside frozen finite-model domain")
    occupied = {(0, 0), (1, 0)}
    path = [(0, 0), (1, 0)]
    histogram: Counter[int] = Counter()

    def enumerate_paths() -> None:
        if len(path) == len(sequence):
            score = 0
            for i, (x, y) in enumerate(path):
                for j in range(i + 2, len(path)):
                    if sequence[i] == sequence[j] == "H":
                        a, b = path[j]
                        score += abs(x - a) + abs(y - b) == 1
            histogram[score] += 1
            return
        x, y = path[-1]
        for point in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if point not in occupied:
                occupied.add(point)
                path.append(point)
                enumerate_paths()
                path.pop()
                occupied.remove(point)

    start = time.perf_counter()
    enumerate_paths()
    partition = sum((Fraction(n) * q**k for k, n in histogram.items()), Fraction())
    event_mass = sum((Fraction(n) * q**k for k, n in histogram.items() if k >= threshold), Fraction())
    return {"paths": sum(histogram.values()), "spectrum": dict(sorted(histogram.items())),
            "partition": str(partition), "probability": str(event_mass / partition),
            "reference_seconds": time.perf_counter() - start}


ATOMS = {"CH4": {"C": 1, "H": 4}, "O2": {"O": 2}, "CO2": {"C": 1, "O": 2},
         "H2O": {"H": 2, "O": 1}, "N2": {"N": 2}, "H2": {"H": 2},
         "NH3": {"N": 1, "H": 3}, "C2H6O": {"C": 2, "H": 6, "O": 1}}


def atom_counts(terms: list[list[Any]]) -> dict[str, int]:
    total: Counter[str] = Counter()
    for formula, coefficient in terms:
        if formula not in ATOMS or type(coefficient) is not int or coefficient <= 0:
            raise ValueError("unknown formula or invalid coefficient in frozen reference")
        for element, n in ATOMS[formula].items():
            total[element] += coefficient * n
    return dict(sorted(total.items()))


def interval_check(observed: dict[str, Any], reference: dict[str, Any], full_depth: bool,
                   previous: dict[str, Any] | None = None) -> dict[str, Any]:
    z = tuple(Fraction(x) for x in observed["partition_interval"])
    p = tuple(Fraction(x) for x in observed["event_probability_interval"])
    if len(z) != 2 or len(p) != 2:
        raise ValueError("interval must have two endpoints")
    exact_z, exact_p = Fraction(reference["partition"]), Fraction(reference["probability"])
    enclosed = z[0] <= exact_z <= z[1] and 0 <= p[0] <= exact_p <= p[1] <= 1
    nested = True
    if previous:
        old_z = tuple(Fraction(x) for x in previous["partition_interval"])
        old_p = tuple(Fraction(x) for x in previous["event_probability_interval"])
        nested = old_z[0] <= z[0] <= z[1] <= old_z[1] and old_p[0] <= p[0] <= p[1] <= old_p[1]
    exact = not full_depth or (z[0] == z[1] == exact_z and p[0] == p[1] == exact_p)
    return {"valid": enclosed and nested and exact, "enclosed": enclosed,
            "nested": nested, "full_depth_exact": exact if full_depth else None,
            "partition_relative_width": str((z[1] - z[0]) / exact_z),
            "probability_width": str(p[1] - p[0])}


def environment(pythonpath: Path | None = None) -> dict[str, str]:
    env = {"PATH": os.defpath, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
           "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
           "TMPDIR": str(PROJECT / "results"), "HOME": str(LOCAL)}
    if pythonpath:
        env["PYTHONPATH"] = str(pythonpath)
    return env


def execute(command: list[str], pythonpath: Path | None = None) -> dict[str, Any]:
    LOCAL.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    try:
        p = subprocess.run(command, cwd=PROJECT, env=environment(pythonpath), capture_output=True,
                           timeout=90, check=False)
        if len(p.stdout) + len(p.stderr) > 2097152:
            raise ValueError("captured output exceeds frozen protocol bound")
        return {"returncode": p.returncode, "stdout": p.stdout.decode(errors="replace"),
                "stderr": p.stderr.decode(errors="replace"), "seconds": time.perf_counter() - start,
                "command": command}
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        return {"execution_error": type(exc).__name__ + ": " + str(exc),
                "seconds": time.perf_counter() - start, "command": command}


def subject_metadata(repo: Path) -> dict[str, Any]:
    git = shutil.which("git")
    if not git or not repo.is_dir():
        return {"available": False}
    r = execute([git, "-C", str(repo), "rev-parse", "HEAD"])
    return {"available": True, "path": str(repo), "commit": r.get("stdout", "").strip()}


def foldbounds(repo: Path, spec: dict[str, Any]) -> dict[str, Any]:
    if not (repo / "src/foldbounds/__main__.py").is_file():
        return {"rows": [{"id": "subject", "outcome": "unsupported", "reason": "source checkout unavailable"}]}
    rows, references = [], {}
    for family in spec["families"]:
        ref = extended_lattice(family["sequence"], Fraction(family["q"]), family["threshold"])
        if ref["paths"] != spec["known_anchored_walk_counts"][str(len(family["sequence"]))]:
            raise ValueError("independent enumerator disagrees with known SAW count")
        references[family["id"]] = ref
        previous = None
        for depth in [len(family["sequence"]) if x == "N" else x for x in spec["depths"]]:
            row = _fold_run(repo, family, depth, [], ref, previous)
            if row["outcome"] != "execution_error":
                previous = row.get("observed")
            rows.append(row)
    for feature in spec["features"]:
        family = next(f for f in spec["families"] if f["id"] == feature["family"])
        row = _fold_run(repo, family, feature["depth"], feature["args"], references[family["id"]], None)
        row["id"] = feature["id"]
        row["family"] = family["id"]
        rows.append(row)
    return {"rows": rows, "independent_references": references,
            "scope": "N=8..10 exact finite 2D model; no experimental biophysics, binding or physical uncertainty model."}


def _fold_run(repo: Path, family: dict[str, Any], depth: int, args: list[str], reference: dict[str, Any], previous: dict[str, Any] | None) -> dict[str, Any]:
    command = [sys.executable, "-B", "-m", "foldbounds", family["sequence"], "--q", family["q"],
               "--depth", str(depth), "--event-at-least", str(family["threshold"]), *args]
    execution = execute(command, repo / "src")
    row: dict[str, Any] = {"id": family["id"] + "-depth" + str(depth), "family": family["id"],
                           "depth": depth, "feature_args": args, "execution": execution}
    try:
        if execution.get("returncode") != 0:
            raise ValueError("subject did not complete normally")
        row["observed"] = json.loads(execution["stdout"])
        row["checks"] = interval_check(row["observed"], reference, depth == len(family["sequence"]), previous)
        row["outcome"] = "valid" if row["checks"]["valid"] else "refuted"
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as exc:
        row.update(outcome="execution_error", reason=str(exc))
    return row


# This is SVB's input producer, not copied subject code. Existing subject APIs
# provide schema-valid packaging/normalization and are explicitly untrusted.
PRODUCER = r'''
import base64,hashlib,json,sys
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
from pcs.certificate_v06 import finalize_certificate_hashes_v06
from pcs.normalized_set_v06 import build_normalized_set_after_replay_v06
from pcs.signing_v06 import sign_certificate_v06
from pcs.package_v06 import build_package_manifest_v06,sign_package_manifest_v06
from pcs.canonical_json import canonicalize_jcs_bytes
request=json.loads(Path(sys.argv[1]).read_text());dest=Path(sys.argv[2]);dest.mkdir()
pred={'type':'reaction_balance','reactants':[{'formula':f,'coefficient':n} for f,n in request['reactants']],'products':[{'formula':f,'coefficient':n} for f,n in request['products']]}
cert={'spec_version':'pcs-0.6','checker_version':'pcs-python-kernel/0.6.0-dev','canonical_json_profile':'pcs-jcs-rfc8785-v1','semantic_hash_format':'pcs-certificate-semantic-sha256-v2','integrity_hash_format':'pcs-certificate-integrity-sha256-v2','generated_at':'2026-11-14T00:00:00+00:00','subject':'SVB v0.2 '+request['id'],'mission_scope':'synthetic atom conservation only; no empirical reaction claim','assumptions':[{'id':'A1','statement':'Only atom counts of specified formulas are considered.','scope':['C1']}],'claims':[{'id':'C1','statement':'Specified reactant and product atom counts agree.','kind':'computational','predicate':pred,'required_evidence':['E1'],'assumptions':['A1'],'assessment':{'status':'COMPUTATIONALLY_SUPPORTED','reason':'all declared computational checks passed'}}],'artifacts':[],'evidence':[{'id':'E1','kind':'computational_test','claim_ids':['C1'],'outcome':'PASS','checker':'pcs-python-kernel/0.6.0-dev','predicate':pred,'artifact_ids':[],'check_spec':pred}],'workflow':{'nodes':[]},'workflow_summary':{'node_count':0,'topological_order':[]},'semantic_hash':'','integrity_hash':''}
cert=finalize_certificate_hashes_v06(cert)
files={'certificate.json':canonicalize_jcs_bytes(cert)}
files.update(build_normalized_set_after_replay_v06(cert,{'valid':True,'claim_statuses':{'C1':'COMPUTATIONALLY_SUPPORTED'}})['files'])
key=Ed25519PrivateKey.from_private_bytes(hashlib.sha256(b'SVB-v0.2.0-public-test-signing-key-not-a-secret').digest())
pub=key.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
manifest=build_package_manifest_v06(cert,{n:{'sha256':hashlib.sha256(b).hexdigest(),'size':len(b)} for n,b in files.items()})
files.update({'package_manifest.json':canonicalize_jcs_bytes(manifest),'package_signature.json':canonicalize_jcs_bytes(sign_package_manifest_v06(manifest,key)),'certificate_signature.json':canonicalize_jcs_bytes(sign_certificate_v06(cert,key))})
for n,b in files.items():
 p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
transcript={'format':'pcs-lean-authority-observations-v1','certificate_semantic_hash':cert['semantic_hash'],'checker_version':cert['checker_version'],'workflow_ok':True,'workflow_analysis':[],'environment_capture':None,'replay':[{'evidence_id':'E1','kind':'computational_test','outcome':'PASS'}]}
(dest.parent/'transcript.json').write_bytes(canonicalize_jcs_bytes(transcript))
print(json.dumps({'key_base64':base64.b64encode(pub).decode(),'fingerprint':hashlib.sha256(pub).hexdigest()}))
'''


def verify_own_signed_container(package: Path, key_base64: str) -> dict[str, Any]:
    """Independent crypto/hash checks do not use subject verifier functions."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    key = Ed25519PublicKey.from_public_bytes(base64.b64decode(key_base64, validate=True))
    manifest = json.loads((package / "package_manifest.json").read_bytes())
    for name, expected in manifest["files"].items():
        data = (package / name).read_bytes()
        if len(data) != expected["size"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise ValueError("independent file binding failure")
    for filename in ("package_signature.json", "certificate_signature.json"):
        record = json.loads((package / filename).read_bytes())
        payload = canonical(record["payload"])
        if hashlib.sha256(payload).hexdigest() != record["payload_sha256"]:
            raise ValueError("independent signature-payload hash failure")
        key.verify(base64.b64decode(record["signature"], validate=True), payload)
    return {"independent_signature_checks": 2, "independent_file_hash_checks": len(manifest["files"])}


def pcs(repo: Path, spec: dict[str, Any]) -> dict[str, Any]:
    binary = repo / "formal/.lake/build/bin/pcs-lean-authority"
    if not binary.is_file():
        return {"rows": [{"id": "subject", "outcome": "unsupported", "reason": "precompiled authority unavailable; no build attempted"}]}
    rows = []
    for family in spec["reactions"]:
        for balanced in (True, False):
            products = family["products"] if balanced else family["unbalanced_products"]
            left, right = atom_counts(family["reactants"]), atom_counts(products)
            if (left == right) != balanced:
                raise ValueError("frozen PCS reference is inconsistent")
            row: dict[str, Any] = {"id": family["id"] + ("-balanced" if balanced else "-forged-pass"),
                                   "family": family["id"], "reference": {"reactant_atoms": left, "product_atoms": right},
                                   "expected": "ACCEPT" if balanced else "REJECT:replay"}
            with tempfile.TemporaryDirectory(prefix="pcs-unfamiliar-", dir=LOCAL) as tmp:
                work = Path(tmp)
                request = work / "request.json"
                request.write_bytes(canonical({"id": row["id"], "reactants": family["reactants"], "products": products}))
                produced = execute([sys.executable, "-B", "-c", PRODUCER, str(request), str(work / "package")], repo)
                row["producer_execution"] = produced
                try:
                    if produced.get("returncode") != 0:
                        raise ValueError("untrusted producer failed to construct a package")
                    meta = json.loads(produced["stdout"])
                    row["container_checks"] = verify_own_signed_container(work / "package", meta["key_base64"])
                    execution = execute([str(binary), str(work / "package"), meta["key_base64"], str(work / "transcript.json"), meta["fingerprint"]])
                    row["execution"] = execution
                    row["observed"] = execution.get("stdout", "").strip()
                    if execution.get("returncode") != 0:
                        row.update(outcome="execution_error", reason="authority failed to execute")
                    elif row["observed"] == row["expected"]:
                        row["outcome"] = "valid"
                    elif not balanced and row["observed"].startswith("REJECT:"):
                        row.update(outcome="construction_error", reason="rejection at an earlier stage cannot establish semantic replay robustness")
                    else:
                        row["outcome"] = "refuted"
                except (ValueError, KeyError, ImportError, TypeError) as exc:
                    row.update(outcome="construction_error", reason=str(exc))
            rows.append(row)
    rows.extend({"id": capability, "outcome": "unsupported", "reason": "No legitimate formal predicate or empirical input interface for this broad inference is exercised; not a product defect."} for capability in spec["unsupported"])
    return {"rows": rows, "binary_sha256": sha256(binary),
            "scope": "Fresh signed atom-conservation predicates with forged positive producer evidence; physical feasibility and free-form scientific claims remain outside scope."}


BROWSER = r'''
import {createRequire} from 'node:module';import http from 'node:http';import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
const require=createRequire(import.meta.url);const [root,pwPath,protocolPath,outdir]=process.argv.slice(2);const {chromium}=require(pwPath);const spec=JSON.parse(fs.readFileSync(protocolPath)).site;
const server=http.createServer((req,res)=>{if(!['GET','HEAD'].includes(req.method)){res.statusCode=405;return res.end();}let name=new URL(req.url,'http://localhost').pathname;if(name.startsWith('/api/')){res.statusCode=503;return res.end('{}');}const file=path.resolve(root,'.'+(name==='/'?'/index.html':name));if(!file.startsWith(path.resolve(root)+path.sep)){res.statusCode=403;return res.end();}try{res.setHeader('Content-Type',({'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'})[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.statusCode=404;res.end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base='http://127.0.0.1:'+server.address().port;const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});const rows=[];const external=[];const writes=[];
const canonical=v=>v===null||typeof v!=='object'?JSON.stringify(v):Array.isArray(v)?'['+v.map(canonical).join(',')+']':'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';
const digest=s=>crypto.createHash('sha256').update(s).digest('hex');
try{for(const width of spec.viewports){const context=await browser.newContext({viewport:{width,height:1000}});await context.route('**/*',route=>{const request=route.request();if(!['GET','HEAD'].includes(request.method())){writes.push(request.url());return route.abort();}if(new URL(request.url()).origin!==base){external.push(request.url());return route.abort();}return route.continue();});const page=await context.newPage();
async function reset(){await page.goto(base+'/check-my-files.html');await page.waitForFunction(()=>document.documentElement.dataset.fileCheckReady==='true');}
async function loadPair(files){for(let i=0;i<2;i++){await page.locator('#file'+i).setInputFiles({name:'svb-'+i+'.csv',mimeType:'text/csv',buffer:Buffer.from(files[i])});await page.waitForFunction(i=>!document.getElementById('column'+i).disabled,i);await page.locator('#column'+i).selectOption('0');}}
async function check(){await page.locator('#check').click();await page.locator('#result').waitFor({state:'visible'});}
for(const name of spec.cases){const row={id:name+'-width'+width,family:name,width};try{await reset();
if(name==='valid_overlap_scope'||name==='disjoint_scope'){await loadPair(name==='valid_overlap_scope'?spec.csv_overlap:spec.csv_disjoint);await check();row.observed={verdict:await page.locator('#verdict').innerText(),scope:await page.locator('.result-meaning').innerText(),local:await page.locator('#localExplanation').innerText(),matchingRows:await page.locator('#matchRows tr').count()};row.valid=(name==='valid_overlap_scope'?/1 shared ID/.test(row.observed.verdict):/No shared IDs/.test(row.observed.verdict))&&/Whether the IDs are accurate, other columns match, or the data supports a scientific conclusion/.test(row.observed.scope)&&/calculated in your browser/.test(row.observed.local);if(width===390&&name==='valid_overlap_scope')await page.screenshot({path:path.join(outdir,'site-valid-overlap.png'),fullPage:true});}
else if(name==='malformed_csv_clears_result'){await loadPair(spec.csv_overlap);await check();await page.locator('#file0').setInputFiles({name:'malformed.csv',mimeType:'text/csv',buffer:Buffer.from(spec.malformed_csv)});await page.waitForFunction(()=>document.getElementById('status').textContent.includes('not closed'));row.observed={status:await page.locator('#status').innerText(),resultHidden:await page.locator('#result').isHidden(),checkDisabled:await page.locator('#check').isDisabled()};row.valid=/not closed/.test(row.observed.status)&&row.observed.resultHidden&&row.observed.checkDisabled;}
else if(name==='forged_imported_receipt_needs_fresh_check'){const summary={left_rows:2,right_rows:2,left_unique:2,right_unique:2,left_repeated_rows:0,right_repeated_rows:0,shared_ids:1,left_affected_rows:1,right_affected_rows:1,left_spaced_ids:0,right_spaced_ids:0};const recipe={format:'pcs-file-check-recipe-v1',scope:'exact-utf8-id-overlap-v1',name:'SVB forged historical receipt',columns:[{header:'id',index:0},{header:'id',index:0}],previous:null};const inputs=spec.csv_overlap.map((s,i)=>({name:'input'+i+'.csv',sha256:digest(s),bytes:Buffer.byteLength(s),data_base64:Buffer.from(s).toString('base64')}));const replay={format:'pcs-file-check-replay-v1',recipe,inputs,summary,local_receipt:{lean_verdict:'DISJOINT',scientific_acceptance:true,authority:'fake'}};await page.locator('#openDocument').setInputFiles({name:'forged.json',mimeType:'application/json',buffer:Buffer.from(canonical(replay)+'\n')});await page.waitForFunction(()=>document.getElementById('status').textContent.includes('Replay ready'));const before=await page.locator('#result').isHidden();const notice=await page.locator('#importText').innerText();await check();row.observed={importedResultHidden:before,notice,verdict:await page.locator('#verdict').innerText(),localResult:await page.locator('#localResult').innerText(),localTitle:await page.locator('#localTitle').innerText()};row.valid=before&&/reported verdict is not trusted/.test(notice)&&/1 shared ID/.test(row.observed.verdict)&&!/complete|confirmed|agreed/i.test(row.observed.localResult);}
row.outcome=row.valid?'valid':'refuted';}catch(error){row.outcome='execution_error';row.error=error.message;}rows.push(row);}await context.close();}}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
console.log(JSON.stringify({rows,browser_version:browser.version(),blocked_external_requests:external.length,blocked_mutating_requests:writes.length,production_requests_sent:0}));
'''


def website(repo: Path, spec: dict[str, Any]) -> dict[str, Any]:
    node, chromium = shutil.which("node"), Path("/usr/bin/chromium")
    playwright = repo / "node_modules/playwright"
    if not node or not chromium.is_file() or not playwright.is_dir():
        return {"rows": [{"id": "subject", "outcome": "unsupported", "reason": "Node, system Chromium, or read-only Playwright installation unavailable"}]}
    harness = LOCAL / "browser_phase2.mjs"
    harness.write_text(BROWSER)
    execution = execute([node, str(harness), str(repo / "public"), str(playwright), str(PROTOCOL), str(LOCAL)])
    try:
        if execution.get("returncode") != 0:
            raise ValueError("browser harness failed to complete")
        result = json.loads(execution["stdout"])
        result["execution"] = execution
        result["scope"] = "Actual local browser DOM only; no production, account service, desktop native authority or human-comprehension claim."
        return result
    except (ValueError, KeyError, TypeError) as exc:
        return {"rows": [{"id": "browser_harness", "outcome": "execution_error", "reason": str(exc)}], "execution": execution}


def run(subject_root: Path = Path("/workspace")) -> dict[str, Any]:
    LOCAL.mkdir(parents=True, exist_ok=True)
    raw = PROTOCOL.read_bytes()
    protocol = json.loads(raw)
    expected_hash = (PROJECT / "results/v0.2.0/systems_protocol.sha256").read_text().split()[0]
    if hashlib.sha256(raw).hexdigest() != expected_hash:
        raise ValueError("frozen phase-II adapter protocol changed")
    result: dict[str, Any] = {"format": "svb-phase2-systems-v0.2.0", "protocol_sha256": expected_hash,
                              "runtime": {"python": platform.python_version(), "platform": platform.platform()},
                              "interpretation": protocol["interpretation"], "systems": {}}
    for name, directory, function in (("foldbounds", "FoldBounds", foldbounds),
                                       ("pcs", "proof-carrying-science", pcs),
                                       ("site", "proof-carrying-science-site", website)):
        repo = subject_root / directory
        measured = function(repo, protocol[name])
        counts = Counter(row["outcome"] for row in measured["rows"])
        measured["outcomes"] = dict(sorted(counts.items()))
        measured["observed_denominator"] = len(measured["rows"])
        measured["eligible_denominator"] = counts["valid"] + counts["refuted"]
        measured["metadata"] = subject_metadata(repo)
        result["systems"][name] = measured
    return result


def sanitized(result: dict[str, Any]) -> dict[str, Any]:
    """Strip raw command/source representations and local temporary artifact paths."""
    def clean(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: clean(item) for key, item in value.items() if key not in ("execution", "producer_execution")}
        if isinstance(value, list):
            return [clean(item) for item in value]
        return value
    summary = clean(result)
    for name, system in result["systems"].items():
        for i, row in enumerate(system["rows"]):
            if "execution" in row:
                summary["systems"][name]["rows"][i]["elapsed_seconds"] = row["execution"].get("seconds")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject-root", type=Path, default=Path("/workspace"))
    args = parser.parse_args()
    result = run(args.subject_root)
    (LOCAL / "systems.json").write_text(json.dumps(result, indent=2) + "\n")
    (PROJECT / "results/v0.2.0/systems.json").write_text(json.dumps(sanitized(result), indent=2) + "\n")
    print(json.dumps({name: {"outcomes": s["outcomes"], "observed": s["observed_denominator"], "eligible": s["eligible_denominator"]} for name, s in result["systems"].items()}))


if __name__ == "__main__":
    main()
