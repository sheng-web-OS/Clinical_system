#!/usr/bin/env python3
"""Regression checks for the EJE scoring safety gate; no clinical truth is inferred."""
import copy
import unittest

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


if __name__ == "__main__":
    unittest.main()
