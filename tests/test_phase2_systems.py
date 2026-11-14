import unittest
from fractions import Fraction
from svb.phase2_systems import atom_counts, extended_lattice, interval_check, sanitized


class PhaseTwoIndependentMethods(unittest.TestCase):
    def test_walk_counts_through_length_ten(self):
        for length, count in ((8, 543), (9, 1479), (10, 4067)):
            self.assertEqual(extended_lattice("P" * length, Fraction(2), 1)["paths"], count)

    def test_rational_probabilities_and_reflection_reversal(self):
        a = extended_lattice("HHPHPPHPHH", Fraction(7, 4), 2)
        b = extended_lattice("HHPHPPHPHH"[::-1], Fraction(7, 4), 2)
        self.assertEqual(a["partition"], b["partition"])
        self.assertEqual(a["probability"], b["probability"])
        self.assertTrue(0 <= Fraction(a["probability"]) <= 1)

    def test_small_enumerator_agrees_with_hand_count(self):
        r = extended_lattice("HHHH", Fraction(2), 1)
        self.assertEqual(r["partition"], "11")
        self.assertEqual(r["probability"], "4/11")

    def test_atom_conservation_detects_signed_producer_lie(self):
        self.assertEqual(atom_counts([["CH4", 1], ["O2", 2]]), atom_counts([["CO2", 1], ["H2O", 2]]))
        self.assertNotEqual(atom_counts([["N2", 1], ["H2", 3]]), atom_counts([["NH3", 1]]))

    def test_false_or_widening_bounds_do_not_pass(self):
        ref = {"partition": "11", "probability": "4/11"}
        good = {"partition_interval": ["10", "12"], "event_probability_interval": ["1/4", "1/2"]}
        excludes = {"partition_interval": ["1", "2"], "event_probability_interval": ["0", "1"]}
        wider = {"partition_interval": ["9", "13"], "event_probability_interval": ["0", "1"]}
        self.assertTrue(interval_check(good, ref, False)["valid"])
        self.assertFalse(interval_check(excludes, ref, False)["valid"])
        self.assertFalse(interval_check(wider, ref, False, good)["valid"])
        self.assertFalse(interval_check(good, ref, True)["valid"])

    def test_summary_omits_raw_subject_execution_arguments(self):
        result = {"systems": {"x": {"rows": [{"id": "a", "execution": {"command": ["private"], "seconds": 1}}]}}}
        cleaned = sanitized(result)
        self.assertNotIn("execution", cleaned["systems"]["x"]["rows"][0])
        self.assertEqual(cleaned["systems"]["x"]["rows"][0]["elapsed_seconds"], 1)


if __name__ == "__main__":
    unittest.main()
