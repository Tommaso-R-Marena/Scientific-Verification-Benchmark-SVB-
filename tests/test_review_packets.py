"""Review preparation must not export author gold or model envelope metadata."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "svb_review_builder", ROOT / "scripts/build_human_review.py")
assert SPEC is not None and SPEC.loader is not None
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)


def sample_case() -> dict:
    return {
        "id": "internal-case", "split": "evaluation",
        "family": "SECRET_FAMILY", "pair": {"role": "SECRET_ROLE"},
        "reference": {"rationale": "SECRET_GOLD", "label": "SECRET_LABEL"},
        "packet": {
            "question": "Is this justified?", "claim": "A source reports x.",
            "documents": [{"id": "doc", "title": "Primary source",
                           "text": "The reported result was x.", "source_id": "source"}],
            "methodology": "Read the supplied record.", "assumptions": ["Fixed record."],
        },
    }


class HumanReviewPackets(unittest.TestCase):
    def test_gold_and_qualification_metadata_are_absent(self):
        out = review.prepare([sample_case()], "evidence")
        text = json.dumps(out)
        self.assertFalse(any(value in text for value in
                             ("SECRET_GOLD", "SECRET_LABEL", "SECRET_FAMILY", "SECRET_ROLE")))
        self.assertEqual(set(out[0]), {"public_id", "question", "claim", "documents",
                                      "methodology", "assumptions"})

    def test_public_transformations_preserve_information_conditions(self):
        self.assertEqual(review.prepare([sample_case()], "no_evidence")[0]["documents"], [])
        self.assertEqual(review.prepare([sample_case()], "no_assumptions")[0]["assumptions"], [])

    def test_raw_answer_is_preserved_but_identity_envelope_is_filtered(self):
        packet = review.prepare([sample_case()], "evidence")
        raw = "Scientifically wrong unparsed answer."
        record = {"id": packet[0]["public_id"], "condition": "evidence",
                  "status": "completed", "raw_text": raw,
                  "model_name": "SECRET_MODEL", "gold": "SECRET_GOLD", "tokens": 99}
        out = review.attach_responses(packet, [record], "evidence")
        self.assertEqual(out[0]["candidate_response"], raw)
        self.assertNotIn("SECRET_MODEL", json.dumps(out))
        self.assertNotIn("SECRET_GOLD", json.dumps(out))

    def test_foreign_and_duplicate_responses_are_refused(self):
        packet = review.prepare([sample_case()], "evidence")
        with self.assertRaises(review.Invalid):
            review.attach_responses(packet, [{"id": "foreign"}], "evidence")
        record = {"id": packet[0]["public_id"], "condition": "evidence",
                  "status": "completed", "raw_text": "x"}
        with self.assertRaises(review.Invalid):
            review.attach_responses(packet, [record, record], "evidence")

    def test_missing_candidate_is_not_silently_dropped(self):
        out = review.attach_responses(review.prepare([sample_case()], "evidence"), [], "evidence")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["response_status"], "missing")
        self.assertIsNone(out[0]["candidate_response"])

    def test_outside_project_output_is_refused(self):
        with self.assertRaises(review.Invalid):
            review.project_path(Path("/tmp/outside-svb-review"))

    def test_ordering_is_reproducible_without_hiding_access(self):
        first = sample_case()
        second = sample_case()
        second["id"] = "another-internal-case"
        self.assertEqual(review.prepare([first, second], "evidence", seed=4),
                         review.prepare([first, second], "evidence", seed=4))


if __name__ == "__main__":
    unittest.main()
