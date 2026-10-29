#!/usr/bin/env python3
"""Regression checks for the EJE scoring safety gate; no clinical truth is inferred."""
import copy
import unittest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments' / 'editorial-judgment'))
from score import score


CASES = {"cases": [{"id": "J01", "status": "replayable", "type": "negative-control"}]}
BASE = {
    "arm": "Native", "id": "J01",
    "tp_major": 0, "fn_major": 0,
    "tp_material": 0, "fn_material": 0, "false_positives": 0,
    "source_claims": 0, "supported_source_claims": 0,
    "human_minutes": 0, "human_turns": 0,
    "correct_decision_and_scope": True, "over_revision": False,
    "new_p0_p1": False, "contaminated": False,
    "stages": {"N": 2, "X": 2, "C": 2, "V": 2},
}


def evaluate(**updates):
    row = copy.deepcopy(BASE)
    row.update(updates)
    return score(CASES, {"judgments": [row]})["Native"]


class TestSafetyGate(unittest.TestCase):
    def test_no_major_error_is_not_validation(self):
        result = evaluate()
        self.assertEqual(result["status"], "PILOT_ONLY")
        self.assertEqual(result["safety_gate"], "NOT_VALIDATED")
        self.assertEqual(result["generalization"], "NOT_TESTED_RETROSPECTIVE_SEEDS")

    def test_major_miss_forces_hold(self):
        result = evaluate(fn_major=1, fn_material=1)
        self.assertEqual(result["status"], "PILOT_HOLD")
        self.assertEqual(result["safety_gate"], "HOLD")
        self.assertEqual(result["hold_reasons"]["missed_major"], 1)

    def test_introduced_major_error_forces_hold(self):
        result = evaluate(new_p0_p1=True)
        self.assertEqual(result["status"], "PILOT_HOLD")
        self.assertEqual(result["hold_reasons"]["introduced_p0_p1"], 1)

    def test_overrevision_cannot_be_correct_scope(self):
        with self.assertRaises(ValueError):
            evaluate(over_revision=True, correct_decision_and_scope=True)

    def test_contaminated_response_cannot_count_as_independent(self):
        result = evaluate(contaminated=True)
        self.assertEqual(result["status"], "NO_INDEPENDENT_EVIDENCE")

    def test_negative_control_cannot_be_awarded_true_positive(self):
        # A clean document cannot yield a legitimate detected defect.
        for counts in ({"tp_major": 1, "tp_material": 1},
                       {"fn_major": 1, "fn_material": 1},
                       {"tp_material": 1}, {"fn_material": 1}):
            with self.subTest(counts=counts):
                with self.assertRaisesRegex(ValueError, "negative.control"):
                    evaluate(**counts)

    def test_fractional_detection_counts_are_rejected(self):
        for field in ("tp_major", "fn_major", "tp_material", "fn_material",
                      "false_positives", "source_claims", "supported_source_claims",
                      "human_turns"):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, "integer"):
                    evaluate(**{field: 0.5})

    def test_missing_case_and_contaminated_case_stay_in_denominator(self):
        two = {"cases": [
            {"id": "J01", "status": "replayable", "type": "negative-control"},
            {"id": "J02", "status": "replayable", "type": "reader-value"},
        ]}
        first = copy.deepcopy(BASE)
        result = score(two, {"judgments": [first]})["Native"]
        self.assertEqual(result["status"], "PILOT_INCOMPLETE")
        self.assertEqual(result["eligible_replayable_cases"], 2)
        self.assertEqual(result["cases"], 1)
        self.assertEqual(result["case_coverage"], 0.5)
        second = copy.deepcopy(first)
        second["id"] = "J02"
        second["contaminated"] = True
        result = score(two, {"judgments": [first, second]})["Native"]
        self.assertEqual(result["status"], "PILOT_INCOMPLETE")
        self.assertEqual(result["contaminated_excluded"], 1)
        self.assertEqual(result["case_coverage"], 0.5)

    def test_self_reported_minutes_not_misrepresented_as_verified(self):
        result = evaluate(human_minutes=7, human_turns=2)
        self.assertIsNone(result["human_correction_minutes"])
        self.assertEqual(result["human_time_evidence"], "NOT_VERIFIED")
        self.assertEqual(result["unverified_reported_minutes"], 7)
        self.assertEqual(result["unverified_reported_turns"], 2)

    def test_duplicate_cases_in_manifest_are_rejected(self):
        duplicates = {"cases": [
            {"id": "J01", "status": "replayable", "type": "negative-control"},
            {"id": "J01", "status": "replayable", "type": "negative-control"},
        ]}
        with self.assertRaisesRegex(ValueError, "Duplicate case"):
            score(duplicates, {"judgments": [copy.deepcopy(BASE)]})


if __name__ == "__main__":
    unittest.main()
