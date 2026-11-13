"""Post-observation hardening: unrelated crashes are not rejection evidence."""
import unittest
from svb.system_evaluations import known_rejection
class RejectionAdmission(unittest.TestCase):
 def test_signal_is_not_rejection(self):
  self.assertFalse(known_rejection({'returncode':-9,'stderr':'invalid'},(2,),'invalid'))
 def test_timeout_is_not_rejection(self):
  self.assertFalse(known_rejection({'execution_error':'timeout','returncode':2,'stderr':'invalid'},(2,),'invalid'))
 def test_only_documented_validation_failure_passes(self):
  self.assertFalse(known_rejection({'returncode':2,'stderr':'unrelated I/O failure'},(2,),'invalid transcript'))
  self.assertTrue(known_rejection({'returncode':2,'stderr':'invalid transcript'},(2,),'invalid transcript'))
