import unittest
from fractions import Fraction as Q
from svb.bound_utility import audit_interval, threshold_decision


class ThresholdCertificateUtility(unittest.TestCase):
    def test_strict_upper_and_inclusive_lower_at_equality(self):
        self.assertEqual(threshold_decision(Q(1,2),Q(3,4),Q(1,2)),"yes")
        self.assertEqual(threshold_decision(Q(1,4),Q(1,2),Q(1,2)),"undecided")
        self.assertEqual(threshold_decision(Q(1,4),Q(1,2),Q(3,4)),"no")

    def test_boundary_controls(self):
        self.assertEqual(threshold_decision(Q(0),Q(0),Q(0)),"yes")
        self.assertEqual(threshold_decision(Q(0),Q(0),Q(1,100)),"no")
        self.assertEqual(threshold_decision(Q(1),Q(1),Q(1)),"yes")
        self.assertEqual(threshold_decision(Q(0),Q(1),Q(1)),"undecided")

    def test_wrong_certificate_decision_fails_exact_reference(self):
        audit=audit_interval(Q(1,5),Q(3,5),Q(4,5),[Q(1,2)])
        self.assertFalse(audit['valid'])
        self.assertFalse(audit['enclosed'])
        self.assertEqual(audit['wrong_definite_decisions'],1)

    def test_wide_but_valid_interval_is_correct_and_useless_interior(self):
        audit=audit_interval(Q(3,5),Q(0),Q(1),[Q(1,4),Q(1,2),Q(3,4)])
        self.assertTrue(audit['valid'])
        self.assertEqual(audit['probability_width'],'1')
        self.assertEqual([x['decision'] for x in audit['decisions']],['undecided']*3)

    def test_complete_grid_valid_enclosures_never_make_wrong_decision(self):
        # Exhaustive finite control of the elementary endpoint proof, including
        # all p/threshold equalities on this rational grid.
        grid=[Q(x,8) for x in range(9)]
        for p in grid:
            for lo in grid:
                for hi in grid:
                    if lo<=p<=hi:
                        audit=audit_interval(p,lo,hi,grid)
                        self.assertTrue(audit['valid'])
                        self.assertEqual(audit['wrong_definite_decisions'],0)

    def test_refinement_can_only_preserve_definite_decisions(self):
        thresholds=[Q(x,8) for x in range(9)]
        wide=audit_interval(Q(1,2),Q(1,4),Q(3,4),thresholds)
        narrow=audit_interval(Q(1,2),Q(3,8),Q(5,8),thresholds)
        for before,after in zip(wide['decisions'],narrow['decisions']):
            if before['decision']!='undecided':self.assertEqual(before['decision'],after['decision'])

    def test_invalid_intervals_are_not_admitted(self):
        for lo,hi,t in ((Q(3,4),Q(1,4),Q(1,2)),(Q(-1),Q(1),Q(1,2)),(Q(0),Q(1),Q(2))):
            with self.assertRaises(ValueError):threshold_decision(lo,hi,t)


if __name__=='__main__':unittest.main()
