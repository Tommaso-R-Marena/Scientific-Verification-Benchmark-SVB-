"""Independent IIb audit: classification, prose and rich-schema boundaries."""
from __future__ import annotations

import copy
import json
import unittest

from svb.core import Invalid, LABELS
from svb.phase2 import public_id
from svb.phase2b import (DEFINITIONS, build_prompt, minimal_verdict,
                        score_a, score_b, score_c)


def case(name="audit", family="source-a", label="empirically_supported"):
    return {
        "id": name, "family": family, "split": "evaluation",
        "pair": {"id": name + "-pair", "role": "narrow"},
        "packet": {
            "question": "Assess the stated conclusion from this record.",
            "claim": "The recorded sample contains four measurements.",
            "documents": [{"id": "OBS", "title": "Source record",
                           "text": "The sample contains four measurements.", "source_id": family}],
            "methodology": "Read the supplied observation record.",
            "assumptions": ["Restrict the claim to the recorded sample."]},
        "reference": {"label": label, "scopes": ["computational", "empirical"],
                      "rationale": "PRIVATE_REFERENCE_SENTINEL", "kind": "empirical_source_fact",
                      "status": "provisional_author_adjudicated",
                      "condition_labels": {"evidence": label, "no_evidence": "insufficient_evidence"},
                      "condition_scopes": {"evidence": ["computational", "empirical"], "no_evidence": []}},
        "checker": {"expected": "PRIVATE_CHECKER_SENTINEL"},
    }


def row(c, text, task="A", condition="evidence", status="completed"):
    return {"id": public_id(c), "task": task, "condition": condition,
            "status": status, "raw_text": text}


class MinimalClassificationAudit(unittest.TestCase):
    def test_all_categories_admit_with_only_surrounding_whitespace(self):
        for label in LABELS:
            with self.subTest(label=label):
                self.assertEqual(minimal_verdict(" \n" + label + "\t"), label)

    def test_no_json_punctuation_case_alias_or_explanation_repairs(self):
        for text in ('"refuted"', '{"label":"refuted"}', 'Refuted', 'refuted.',
                     '```refuted```', 'refuted because the mean is wrong',
                     'true', 'refuted insufficient_evidence', '', None):
            with self.subTest(text=text), self.assertRaises(Invalid):
                minimal_verdict(text)

    def test_rotated_definitions_rotate_the_actual_first_category(self):
        c = case()
        for order in range(6):
            system = build_prompt(c, "A", order=order)["messages"][0]["content"]
            expected = list(LABELS[order:] + LABELS[:order])
            actual = sorted(expected, key=lambda x: system.index(x + " = "))
            self.assertEqual(actual, expected)
            for label in LABELS:
                self.assertEqual(system.count(label + " = " + DEFINITIONS[label]), 1)

    def test_private_reference_and_family_metadata_not_exported(self):
        c = case()
        for task in ("A", "B", "C"):
            prompt = build_prompt(c, task)
            text = json.dumps(prompt)
            self.assertNotIn("PRIVATE_REFERENCE_SENTINEL", text)
            self.assertNotIn("PRIVATE_CHECKER_SENTINEL", text)
            p = json.loads(prompt["messages"][1]["content"])
            self.assertEqual(set(p), {"question", "claim", "documents", "methodology", "assumptions"})
            self.assertNotIn("family", p)
            self.assertNotIn("reference", p)

    def test_coarse_acceptance_is_separate_from_exclusive_category(self):
        c = case()
        result = score_a([c], [row(c, "computationally_established")], "evidence")
        self.assertEqual(result["summary"]["exact_correct"], 0)
        self.assertEqual(result["summary"]["coarse_correct"], 1)
        self.assertEqual(result["summary"]["admitted"], 1)

    def test_missing_timeout_unsupported_malformed_keep_total_denominator(self):
        cs = [case(str(i), "family-" + str(i)) for i in range(4)]
        records = [row(cs[0], None, status="timeout"),
                   row(cs[1], None, status="unsupported"),
                   row(cs[2], '"empirically_supported"')]
        result = score_a(cs, records, "evidence")
        self.assertEqual(result["summary"]["n"], 4)
        self.assertEqual(result["summary"]["statuses"],
                         {"timeout": 1, "unsupported": 1, "malformed": 1, "missing": 1})
        self.assertEqual(result["summary"]["admitted"], 0)
        self.assertEqual(result["summary"]["exact_correct"], 0)

    def test_noncompleted_run_cannot_assert_a_verdict(self):
        c = case()
        for status in ("unsupported", "timeout", "execution_error"):
            result = score_a([c], [row(c, "empirically_supported", status=status)], "evidence")
            self.assertEqual(result["summary"]["statuses"], {"malformed": 1})

    def test_duplicate_foreign_and_mixed_interface_records_rejected(self):
        c = case()
        variants = [[row(c, "refuted"), row(c, "refuted")],
                    [{"id": "foreign", "task": "A", "condition": "evidence"}],
                    [row(c, "refuted", task="B")],
                    [row(c, "refuted", condition="no_evidence")]]
        for records in variants:
            with self.subTest(records=records), self.assertRaises(Invalid):
                score_a([c], records, "evidence")

    def test_nonarray_and_nonobject_execution_records_rejected(self):
        c = case()
        for records in ({}, [None], ["not an envelope"]):
            with self.subTest(records=records), self.assertRaises(Invalid):
                score_a([c], records, "evidence")

    def test_removed_evidence_changes_reference_without_mutating_historical_case(self):
        c = case()
        original = copy.deepcopy(c)
        result = score_a([c], [row(c, "insufficient_evidence", condition="no_evidence")], "no_evidence")
        self.assertEqual(result["summary"]["exact_correct"], 1)
        self.assertEqual(result["summary"]["correct_insufficiency"], 1)
        self.assertEqual(c, original)
        self.assertEqual(json.loads(build_prompt(c, "A", "no_evidence")["messages"][1]["content"])["documents"], [])

    def test_family_summary_preserves_all_selected_families(self):
        cs = [case(str(i), "family-" + str(i)) for i in range(3)]
        result = score_a(cs, [row(c, "empirically_supported") for c in cs], "evidence")
        self.assertEqual(len(result["by_source_family"]), 3)
        self.assertEqual(sum(x["n"] for x in result["by_source_family"].values()), 3)
        self.assertEqual(result["summary"]["n"], 3)


class SeparateProseAndSchemaAudit(unittest.TestCase):
    def test_real_source_id_does_not_establish_reasoning_correctness(self):
        c = case()
        result = score_b([c], [row(c, "All future patients are guaranteed cured [OBS].", task="B")], "evidence")
        self.assertEqual(result["nonsupplied_id_cases"], 0)
        self.assertEqual(result["human_reviewed"], 0)
        self.assertIsNone(result["scientific_reasoning_accuracy"])
        self.assertEqual(result["rows"][0]["reasoning_validity"], "pending_independent_human_review")

    def test_nonsupplied_prose_attribution_is_distinct_from_global_paper_fabrication(self):
        c = case()
        result = score_b([c], [row(c, "A source reports this [invented-packet-id].", task="B")], "evidence")
        self.assertEqual(result["nonsupplied_id_cases"], 1)
        self.assertEqual(result["rows"][0]["nonsupplied_ids"], ["invented-packet-id"])
        self.assertIsNone(result["scientific_reasoning_accuracy"])

    def test_noncompleted_prose_is_malformed_without_scoring_its_citations(self):
        c = case()
        result = score_b([c], [row(c, "A claim [invented-id].", task="B", status="timeout")], "evidence")
        self.assertEqual(result["statuses"], {"malformed": 1})
        self.assertEqual(result["nonsupplied_id_cases"], 0)

    def test_plain_category_is_not_repaired_into_a_rich_schema(self):
        c = case()
        result = score_c([c], [row(c, "empirically_supported", task="C")], "evidence")
        self.assertEqual(result["summary"]["raw_statuses"], {"malformed": 1})
        self.assertEqual(result["summary"]["correct"], 0)

    def test_rich_schema_label_accuracy_does_not_hide_nonsupplied_evidence(self):
        c = case()
        answer = {"label": "empirically_supported", "scopes": ["empirical"],
                  "confidence": {label: float(label == "empirically_supported") for label in LABELS},
                  "evidence_ids": ["absent"], "reasoning": "An unsupported source step.", "citations": []}
        result = score_c([c], [row(c, json.dumps(answer), task="C")], "evidence")
        self.assertEqual(result["summary"]["correct"], 1)
        self.assertEqual(result["summary"]["fabricated_source_cases"], 1)
        self.assertEqual(result["summary"]["evidence_integrity_accepted_errors"], 1)
        self.assertIsNone(result["summary"]["reasoning_accuracy"])


if __name__ == "__main__":
    unittest.main()
