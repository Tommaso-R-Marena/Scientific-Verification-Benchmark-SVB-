"""Review packaging tests: sources, leakage boundaries, raw text and manifests."""
from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("svb_phase2b_review", ROOT / "scripts/build_phase2b_review.py")
assert SPEC and SPEC.loader
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)


def case(identifier):
    return {"id": identifier, "family": "DO_NOT_EXPORT_FAMILY", "split": "DO_NOT_EXPORT_SPLIT",
            "reference": {"label": "DO_NOT_EXPORT_GOLD"},
            "pair": {"role": "DO_NOT_EXPORT_ROLE"},
            "packet": {"question": "What follows?", "claim": "The record reports a measurement.",
                       "methodology": "Assess the fixed record.", "assumptions": ["Use supplied evidence."],
                       "documents": [{"id": "DOC", "title": "Scientific source", "text": "Measured x.",
                                      "source_id": "study"}]}}


class ReviewPackage(unittest.TestCase):
    def setUp(self):
        cache = ROOT / ".cache"
        cache.mkdir(exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(prefix="review-test-", dir=cache)
        self.root = Path(self.directory.name)
        self.source = self.root / "data/v0.2.0/sources/source.txt"
        self.source.parent.mkdir(parents=True)
        self.source.write_bytes(b"Public scientific data and license notes.\n")
        self.registry = {"sources": {"study": {"title": "A source", "url": "https://example.test/paper",
            "license": "CC0-1.0", "limitations": "Small observed sample.",
            "split": "DO_NOT_EXPORT_SPLIT", "reference": "DO_NOT_EXPORT_GOLD",
            "artifacts": [{"path": "data/v0.2.0/sources/source.txt", "sha256": review.sha(self.source.read_bytes()),
                           "bytes": self.source.stat().st_size}]}}}

    def tearDown(self):
        self.directory.cleanup()

    def build(self, **kw):
        return review.build([case("old")], [case("new")], [self.registry], root=self.root, **kw)

    def test_all_cases_mixed_and_gold_metadata_excluded(self):
        files, internal = self.build()
        text = b"\n".join(files.values()).decode()
        for marker in ("DO_NOT_EXPORT_GOLD", "DO_NOT_EXPORT_FAMILY", "DO_NOT_EXPORT_SPLIT", "DO_NOT_EXPORT_ROLE"):
            self.assertNotIn(marker, text)
        packets = json.loads(files["packets.json"])
        self.assertEqual(len(packets), 2)
        self.assertEqual(set(packets[0]), review.PACKET_KEYS | {"public_id"})
        self.assertEqual(len(internal["packet_mapping"]), 2)
        self.assertEqual(len(json.loads(files["blank_forms.json"])), 6)

    def test_manifest_covers_exact_bytes_and_internal_mapping_not_zipped(self):
        files, internal = self.build()
        manifest = json.loads(files["manifest.json"])
        for name, record in manifest["files"].items():
            self.assertEqual(record["sha256"], review.sha(files[name]))
            self.assertEqual(record["bytes"], len(files[name]))
        with zipfile.ZipFile(io.BytesIO(review.deterministic_zip(files))) as archive:
            self.assertEqual(set(archive.namelist()), set(files))
            self.assertFalse(any(name.startswith("internal/") for name in archive.namelist()))
            self.assertIsNone(archive.testzip())
        self.assertEqual(review.deterministic_zip(files), review.deterministic_zip(files))

    def test_archived_sources_have_checked_hashes_and_own_rights(self):
        files, _ = self.build()
        sources = json.loads(files["source_registry.json"])["sources"]
        self.assertEqual(sources["study"]["license"], "CC0-1.0")
        artifact = sources["study"]["artifacts"][0]
        self.assertEqual(files[artifact["package_path"]], self.source.read_bytes())
        self.source.write_bytes(b"corrupted")
        with self.assertRaises(review.PreparationError):
            self.build()

    def test_path_escape_and_unregistered_sources_fail(self):
        self.registry["sources"]["study"]["artifacts"][0]["path"] = "/tmp/outside-svb-source"
        with self.assertRaises(review.PreparationError):
            self.build()
        with self.assertRaises(review.PreparationError):
            review.scientific_sources([], {"missing"}, self.root)

    def test_duplicate_ids_and_extra_packet_metadata_fail(self):
        with self.assertRaises(review.PreparationError):
            review.prepare_packets([("old", [case("same")]), ("new", [case("same")])])
        c = case("x")
        c["packet"]["reference"] = "secret"
        with self.assertRaises(review.PreparationError):
            review.packet(c)

    def test_registry_cannot_smuggle_case_answers_as_source_artifact(self):
        answers = self.root / "data/v0.2.0/cases.json"
        answers.write_text('{"reference":"DO_NOT_EXPORT_GOLD"}')
        self.registry["sources"]["study"]["artifacts"] = [{
            "path": "data/v0.2.0/cases.json", "sha256": review.sha(answers.read_bytes()),
            "bytes": answers.stat().st_size}]
        with self.assertRaises(review.PreparationError):
            self.build()

    def test_actual_response_raw_text_preserved_envelope_identity_removed(self):
        pid = review.public_id("new")
        raw = "I am an identifiable model; this text is intentionally not automatically redacted."
        records = [{"id": pid, "task": "B", "condition": "evidence", "status": "completed",
                    "raw_text": raw, "model_id": "DO_NOT_EXPORT_MODEL", "score": "DO_NOT_EXPORT_SCORE"}]
        files, internal = self.build(records=records)
        candidates = json.loads(files["candidate_packets.json"])
        supplied = next(p for p in candidates if p["public_id"] == pid)
        self.assertEqual(supplied["candidate"]["raw_response"], raw)
        self.assertNotIn("DO_NOT_EXPORT_MODEL", files["candidate_packets.json"].decode())
        self.assertNotIn("DO_NOT_EXPORT_SCORE", files["candidate_packets.json"].decode())
        missing = next(p for p in candidates if p["public_id"] != pid)
        self.assertEqual(missing["candidate"]["generation_state"], "not_supplied")

    def test_no_evidence_response_packet_does_not_restore_documents(self):
        packets, _ = review.prepare_packets([("old", [case("old")])])
        out, _ = review.candidate_packets(packets, [], "A", "no_evidence")
        self.assertEqual(out[0]["documents"], [])

    def test_duplicate_foreign_or_nontext_responses_fail(self):
        packets, _ = review.prepare_packets([("old", [case("old")])])
        pid = packets[0]["public_id"]
        record = {"id": pid, "task": "B", "condition": "evidence", "raw_text": "text"}
        with self.assertRaises(review.PreparationError):
            review.candidate_packets(packets, [record, record], "B", "evidence")
        with self.assertRaises(review.PreparationError):
            review.candidate_packets(packets, [{"id": "foreign"}], "B", "evidence")
        record["raw_text"] = {"repair": "forbidden"}
        with self.assertRaises(review.PreparationError):
            review.candidate_packets(packets, [record], "B", "evidence")

    def test_forms_are_blank_and_do_not_claim_humans(self):
        files, _ = self.build()
        forms = json.loads(files["blank_forms.json"])
        self.assertEqual({f["reviewer_role"] for f in forms}, set(review.ROLES))
        self.assertTrue(all(f["reviewer_code"] is None and f["first_round"]["primary_label"] is None
                            and f["review_status"] == "not_started" for f in forms))
        self.assertEqual(json.loads(files["manifest.json"])["human_reviews_completed"], 0)

    def test_duplicate_keys_and_nonfinite_json_refused(self):
        for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
            with self.assertRaises(review.PreparationError):
                review.strict_loads(text)


if __name__ == "__main__":
    unittest.main()
