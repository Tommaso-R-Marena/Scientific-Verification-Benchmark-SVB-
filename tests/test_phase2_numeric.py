import unittest
from fractions import Fraction
from svb.phase2_numeric import arithmetic, respond


def packet(claim, table="sample,mass\na,2\nb,4\n"):
    return {"question": "Is this numerical statement justified?", "claim": claim,
            "documents": [{"id": "measurements", "title": "Observed values", "text": table, "source_id": "study"}],
            "methodology": "Exact descriptive arithmetic only.", "assumptions": ["Every supplied row is included once."]}


class PublicPacketNumericalBaseline(unittest.TestCase):
    def test_computes_actual_mean_and_refutes_wrong_mean(self):
        self.assertEqual(respond(packet("The mean of mass is 3."))["label"], "computationally_established")
        self.assertEqual(respond(packet("The mean of mass is 6."))["label"], "refuted")

    def test_changed_data_changes_judgment_without_reference_access(self):
        a = respond(packet("The mean of mass is 3."))
        b = respond(packet("The mean of mass is 3.", "sample,mass\na,6\nb,8\n"))
        self.assertNotEqual(a["label"], b["label"])

    def test_exact_decimal_arithmetic_and_no_eval(self):
        self.assertEqual(arithmetic("0.1 + 0.2"), Fraction(3, 10))
        self.assertEqual(respond(packet("0.1 + 0.2 = 0.3"))["label"], "computationally_established")
        for expression in ("__import__('os')", "2**100", "x + 1", "1/0", "1e9999999999999"):
            with self.assertRaises((ValueError, ZeroDivisionError)):
                arithmetic(expression)

    def test_fenced_table_and_paired_mean(self):
        table = "Repeated measurements:\n```csv\nbefore,after\n2,5\n4,6\n```"
        r = respond(packet("The mean change (after minus before) is 2.5.", table))
        self.assertEqual(r["label"], "computationally_established")
        self.assertEqual(r["evidence_ids"], ["measurements"])

    def test_difference_and_ratio_use_column_means(self):
        table = "x,y\n4,2\n8,4\n"
        self.assertEqual(respond(packet("The difference between mean of x and mean of y is 3.", table))["label"], "computationally_established")
        self.assertEqual(respond(packet("The ratio of mean of x to mean of y is 2.", table))["label"], "computationally_established")

    def test_interpretation_ambiguity_and_metadata_are_unsupported(self):
        for claim in ("The mean of mass is 3 and the treatment cures patients.", "The mean of mass is approximately 3.", "The treatment is effective."):
            self.assertEqual(respond(packet(claim))["status"], "unsupported")
        p = packet("The mean of mass is 3.")
        p["reference"] = {"label": "computationally_established"}
        self.assertEqual(respond(p)["status"], "unsupported")
        p = packet("The mean of mass is 3.")
        p["documents"].append({**p["documents"][0], "id": "second"})
        self.assertEqual(respond(p)["status"], "unsupported")

    def test_missing_evidence_and_bad_numeric_rows_do_not_pass(self):
        p = packet("The mean of mass is 3.")
        p["documents"] = []
        self.assertEqual(respond(p)["status"], "unsupported")
        self.assertEqual(respond(packet("The mean of mass is 3.", "sample,mass\na,2\nb,NA\n"))["status"], "unsupported")

    def test_response_has_sixkeys_and_uncalibrated_onehot(self):
        r = respond(packet("The sum of mass is 6."))
        self.assertEqual(set(r), {"label", "scopes", "confidence", "evidence_ids", "reasoning", "citations"})
        self.assertEqual(sum(r["confidence"].values()), 1)
        self.assertIn("uncalibrated", r["reasoning"])

    def test_generic_record_and_distinct_pair_counts(self):
        table = "experiment,record\na,x\na,y\nb,x\n"
        self.assertEqual(respond(packet("The supplied table has 3 records, 2 distinct record strings, and3 distinct (experiment, record) pairs.", table))["label"], "computationally_established")
        table = "arm,value\nexposed,4\nexposed,6\ncontrol,2\n"
        self.assertEqual(respond(packet("The table contains 2 exposed rows and1 control rows.", table))["label"], "computationally_established")

    def test_generic_signed_residual_and_unit_mismatch(self):
        table = "name,experimental_kcal_mol,calculated_kcal_mol,experimental_reference,calculated_reference\ncompoundX,-2.5,-4.0,articleA,articleB\ncompoundY,1,1,articleA,articleB\n"
        self.assertEqual(respond(packet("For the compoundX record, the signed simulation residual is-1.5 kcal/mol (calculated minus experimental).", table))["label"], "computationally_established")
        self.assertEqual(respond(packet("For the compoundX record, the signed simulation residual is-1.5 kJ/mol (calculated minus experimental).", table))["status"], "unsupported")


if __name__ == "__main__":
    unittest.main()
