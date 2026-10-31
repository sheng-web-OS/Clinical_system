"""Regression tests for evidence-change -> candidate-revision proposals."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_learning_delta import compare_updates

SIG = {"from_role": "metric", "to_role": "decision",
       "missing_bridge_role": "context"}


def obs(cid, family, features, checked="checked"):
    return {"id": cid, "family_id": family, "reasoning_signature": dict(SIG),
            "source_ref": "synthetic-public/" + cid, "source_check": checked,
            "context_features": list(features)}


def starting_packet():
    return {"examples": [
        obs("a", "software", ["proxy_only", "additional_context_needed"]),
        obs("b", "finance", ["proxy_only", "additional_context_needed"])
    ], "challenges": []}


def new_challenge(features=("narrow_target_defined",), checked="checked", cid="counter"):
    return obs(cid, "other", features, checked)


class LearningDeltaTests(unittest.TestCase):
    def test_identical_evidence_no_change(self):
        p = starting_packet()
        result = compare_updates(p, copy.deepcopy(p))
        self.assertEqual(result["state"], "NO_EVIDENCE_CHANGE")
        self.assertEqual(result["action_count"], 0)
        self.assertFalse(result["promotion_authorized"])
        self.assertEqual(result["learning_gain"], "NOT_MEASURED")

    def test_counterevidence_changes_parent_and_proposes_scoped_guard(self):
        before = starting_packet()
        after = copy.deepcopy(before)
        after["challenges"].append(new_challenge())
        result = compare_updates(before, after)
        actions = {x["action"] for x in result["actions"]}
        self.assertIn("RECHECK_PARENT_EVIDENCE", actions)
        self.assertIn("PROPOSE_SCOPED_HYPOTHESIS", actions)
        self.assertEqual(result["state"], "REVIEW_CANDIDATE_UPDATES")
        self.assertEqual(result["memory_mutations_performed"], 0)

    def test_new_counterexample_with_same_guard_withdraws_scope(self):
        before = starting_packet()
        before["challenges"].append(new_challenge())
        after = copy.deepcopy(before)
        after["challenges"].append(new_challenge(
            features=("proxy_only", "additional_context_needed"), cid="breaks_guard"))
        result = compare_updates(before, after)
        self.assertIn("WITHDRAW_SCOPE_HYPOTHESIS",
                      [a["action"] for a in result["actions"]])
        self.assertFalse(result["promotion_authorized"])

    def test_unchecked_counterexample_does_not_create_guard(self):
        before = starting_packet()
        after = copy.deepcopy(before)
        after["challenges"].append(new_challenge(checked="unchecked"))
        result = compare_updates(before, after)
        self.assertIn("RECHECK_PARENT_EVIDENCE",
                      [a["action"] for a in result["actions"]])
        self.assertNotIn("PROPOSE_SCOPED_HYPOTHESIS",
                         [a["action"] for a in result["actions"]])

    def test_source_text_change_without_structural_change_is_not_a_learning_win(self):
        before = starting_packet()
        after = copy.deepcopy(before)
        after["examples"][0]["observation"] = "Novel author wording, not new evidence attestation"
        result = compare_updates(before, after)
        self.assertEqual(result["state"], "EVIDENCE_CHANGED_NO_DECISION_DELTA")
        self.assertEqual(result["action_count"], 0)
        self.assertEqual(result["learning_gain"], "NOT_MEASURED")
        self.assertFalse(result["independent_semantic_verification"])

    def test_retract_invalidated_parent_when_support_removed(self):
        before = starting_packet()
        after = copy.deepcopy(before)
        after["examples"] = [before["examples"][0]]
        result = compare_updates(before, after)
        self.assertIn("WITHDRAW_PARENT_PROPOSAL",
                      [a["action"] for a in result["actions"]])

    def test_inputs_remain_unchanged_and_output_is_reproducible(self):
        before = starting_packet()
        after = copy.deepcopy(before)
        after["challenges"].append(new_challenge())
        original = copy.deepcopy((before, after))
        self.assertEqual(compare_updates(before, after), compare_updates(before, after))
        self.assertEqual((before, after), original)


if __name__ == "__main__":
    unittest.main()
