"""Reference-method checks; no evaluated system is needed by this test suite."""
import unittest
from fractions import Fraction

from svb.system_evaluations import exact_lattice, csv_reference


class IndependentReferences(unittest.TestCase):
    def test_published_small_walk_counts_and_contact_mass(self):
        # Unrestricted c3=36 walks / four first-bond orientations = nine.
        result = exact_lattice("HHHH", Fraction(2), 1)
        self.assertEqual(result["paths"], 9)
        self.assertEqual(result["spectrum"], {0: 7, 1: 2})
        self.assertEqual(result["partition"], "11")
        self.assertEqual(result["probability"], "4/11")

    def test_homopolymer_q_one_counts_and_all_polar_zero_event(self):
        self.assertEqual(exact_lattice("HHHHHH", Fraction(1), 1)["partition"], "71")
        self.assertEqual(exact_lattice("PPPPPP", Fraction(2), 1)["probability"], "0")

    def test_reference_refuses_invalid_model(self):
        for sequence, q in (("HXH", Fraction(2)), ("HHH", Fraction(1, 2))):
            with self.assertRaises(ValueError):
                exact_lattice(sequence, q, 1)

    def test_reversal_symmetry_preserves_exact_spectrum(self):
        a = exact_lattice("HHPHPPH", Fraction(3, 2), 1)
        b = exact_lattice("HHPHPPH"[::-1], Fraction(3, 2), 1)
        self.assertEqual(a, b)

    def test_csv_exact_ids_and_multiplicity(self):
        result = csv_reference("id\na\na\n01\n", "id\na\n1\n")
        self.assertEqual(result["shared"], ["a"])
        self.assertEqual(result["left_affected_rows"], 2)
        self.assertEqual(result["left_repeated_rows"], 1)

    def test_csv_row_order_metamorphism(self):
        a = csv_reference("id\na\nb\n", "id\nb\nc\n")
        b = csv_reference("id\nb\na\n", "id\nc\nb\n")
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
