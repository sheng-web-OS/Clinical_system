"""Deterministic EJE metric integrity tests. No claims about model quality."""
from pathlib import Path
import importlib.util
import unittest

MODULE = Path(__file__).resolve().parents[1] / "experiments/editorial-judgment/score.py"
spec = importlib.util.spec_from_file_location("eje_score", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

CASES = {"cases": [
    {"id": "a", "status": "replayable", "type": "negative-control"},
    {"id": "b", "status": "needs_freeze", "type": "clinical"}
]}


def one_case():
    return {
        "arm": "lite", "id": "a", "tp_major": 0, "fn_major": 0,
        "tp_material": 1, "fn_material": 1, "false_positives": 1,
        "source_claims": 2, "supported_source_claims": 2,
        "human_minutes": 4, "human_turns": 1,
        "correct_decision_and_scope": False, "over_revision": True,
        "new_p0_p1": False, "contaminated": False,
        "stages": {"N": 2, "X": 1, "C": 0, "V": 2}
    }


class TestEJEScore(unittest.TestCase):
    def test_counts_and_noncompensating_controls(self):
        x = mod.score(CASES, {"judgments": [one_case()]})["lite"]
        self.assertEqual(x["material_recall"], .5)
        self.assertEqual(x["finding_precision"], .5)
        self.assertEqual(x["major_recall"], None)
        self.assertEqual(x["negative_control_overrevision"], 1.0)
        self.assertEqual(x["human_correction_minutes"], 4)
        self.assertEqual(x["stage_means"]["C"], 0)

    def test_contaminated_does_not_count_as_autonomous(self):
        x = one_case()
        x["contaminated"] = True
        self.assertEqual(
            mod.score(CASES, {"judgments": [x]})["lite"]["status"],
            "NO_INDEPENDENT_EVIDENCE")

    def test_unfrozen_example_cannot_be_scored(self):
        x = one_case()
        x["id"] = "b"
        with self.assertRaisesRegex(ValueError, "frozen replayable"):
            mod.score(CASES, {"judgments": [x]})

    def test_false_source_claim_invalid(self):
        x = one_case()
        x["supported_source_claims"] = 3
        with self.assertRaisesRegex(ValueError, "Supported source claims"):
            mod.score(CASES, {"judgments": [x]})


if __name__ == "__main__":
    unittest.main()
