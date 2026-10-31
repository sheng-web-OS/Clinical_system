"""Synthetic negative controls for proposing parent Concept Families."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_candidate_discovery import discover

SIG = {"from_role": "measurement", "to_role": "diagnostic_classification",
       "missing_bridge_role": "additional_context"}


def case(id_, family, signature=None, checked="checked"):
    return {"id": id_, "family_id": family,
            "reasoning_signature": copy.deepcopy(signature or SIG),
            "source_ref": "public-test/" + id_, "source_check": checked}


class CandidateDiscoveryTests(unittest.TestCase):
    def test_forms_new_parent_without_preexisting_pattern_name(self):
        result = discover({"examples": [case("a", "f1"), case("b", "f2")]})
        self.assertEqual(result["proposal_count"], 1)
        self.assertEqual(result["gate"]["results"][0]["status"],
                         "PROPOSED_PENDING_INDEPENDENT_QA")
        self.assertEqual(result["candidate_preflight"][0]["challenge_status"],
                         "COUNTEREXAMPLE_NOT_OBSERVED")
        self.assertEqual(result["promotions_performed"], 0)

    def test_counterexample_blocks_until_reconciled(self):
        result = discover({"examples": [case("a", "f1"), case("b", "f2")],
                           "challenges": [case("contra", "f3")]})
        candidate = result["gate"]["results"][0]
        self.assertIn("UNADDRESSED_COUNTEREXAMPLE", candidate["blockers"])
        self.assertEqual(candidate["status"], "HOLD_REVISION_REQUIRED")
        self.assertEqual(result["candidate_preflight"][0]["challenge_status"],
                         "OPEN_COUNTEREXAMPLE")

    def test_same_family_not_generalized(self):
        self.assertEqual(discover({"examples": [case("a", "f1"), case("b", "f1")]})
                         ["proposal_count"], 0)

    def test_different_causal_bridges_not_merged(self):
        different = dict(SIG, missing_bridge_role="longitudinal_evidence")
        out = discover({"examples": [case("a", "f1"), case("b", "f2", different)]})
        self.assertEqual(out["proposal_count"], 0)

    def test_source_unchecked_cannot_pass_gate(self):
        res = discover({"examples": [case("a", "f1"), case("b", "f2", checked="unverified")]})
        self.assertIn("SUPPORT_SOURCE_NOT_CHECKED", res["gate"]["results"][0]["blockers"])

    def test_idempotent_order_independent_proposal(self):
        first = discover({"examples": [case("a", "f1"), case("b", "f2")]})
        second = discover({"examples": [case("b", "f2"), case("a", "f1")]})
        self.assertEqual(first, second)

    def test_dependency_impact_without_mutation(self):
        res = discover({"examples": [case("a", "f1"), case("b", "f2")],
                        "dependencies": [{"id": "derived", "depends_on": ["a"]}]})
        self.assertEqual(res["gate"]["results"][0]["dependency_recheck"][0]["claim_id"],
                         "derived")
        self.assertFalse(res["gate"]["results"][0]["promotion_authorized"])

    def test_duplicate_source_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate observation id"):
            discover({"examples": [case("a", "f1"), case("a", "f2")]})


    def test_public_guideline_probe_is_challenged_not_promoted(self):
        import json
        fixture = (Path(__file__).resolve().parents[1] / "experiments" /
                   "ale-recursive-concept-probe-20261031.json")
        packet = json.loads(fixture.read_text(encoding="utf-8"))
        result = discover(packet)
        self.assertEqual(result["proposal_count"], 1)
        self.assertEqual(len(result["candidate_preflight"][0]["families"]), 3)
        self.assertEqual(result["gate"]["results"][0]["status"], "HOLD_REVISION_REQUIRED")
        self.assertEqual(result["gate"]["results"][0]["unaddressed_counterexamples"],
                         ["renal-persistent-egfr-exception"])
        self.assertEqual(result["promotions_performed"], 0)

    def test_q3_scope_guard_generates_new_q0_without_promoting(self):
        positives = [case("a", "cardio"), case("b", "renal")]
        for item in positives:
            item["context_features"] = ["single_measurement", "missing_clinical_context"]
        negative = case("challenge", "other")
        negative["context_features"] = ["longitudinal_confirmed"]
        out = discover({"examples": positives, "challenges": [negative]})
        self.assertEqual(out["gate"]["results"][0]["status"], "HOLD_REVISION_REQUIRED")
        self.assertEqual(len(out["recursive_scope_refinements"]), 1)
        refined = out["recursive_scope_refinements"][0]
        self.assertEqual(refined["stage"], "Q3_TO_Q0_SCOPE_HYPOTHESIS")
        self.assertEqual(refined["required_context_features"], ["missing_clinical_context"])
        self.assertFalse(refined["promotion_authorized"])
        self.assertIn("unseen counterexample", refined["question_q3"])

    def test_refinement_rejected_when_counterexample_satisfies_all_conditions(self):
        positives = [case("a", "cardio"), case("b", "renal")]
        for item in positives:
            item["context_features"] = ["single_measurement"]
        negative = case("challenge", "other")
        negative["context_features"] = ["single_measurement"]
        out = discover({"examples": positives, "challenges": [negative]})
        self.assertEqual(out["recursive_scope_refinements"], [])

    def test_refinement_requires_conditions_not_plausible_wording(self):
        out = discover({"examples": [case("a", "cardio"), case("b", "renal")],
                        "challenges": [case("challenge", "other")]})
        self.assertEqual(out["recursive_scope_refinements"], [])

    def test_multi_feature_guard_can_exclude_two_different_challenges(self):
        positives = [case("a", "f1"), case("b", "f2")]
        for item in positives:
            item["context_features"] = ["absent_corroboration", "single_timepoint"]
        c1, c2 = case("c1", "f3"), case("c2", "f4")
        c1["context_features"] = ["absent_corroboration"]
        c2["context_features"] = ["single_timepoint"]
        out = discover({"examples": positives, "challenges": [c1, c2]})
        self.assertEqual(out["recursive_scope_refinements"][0]["required_context_features"],
                         ["absent_corroboration", "single_timepoint"])

    def test_refinement_requires_bounded_machine_safe_features(self):
        a, b, c = case("a", "f1"), case("b", "f2"), case("c", "f3")
        for record in (a, b):
            record["context_features"] = ["invalid natural language with patient details"]
        c["context_features"] = []
        with self.assertRaisesRegex(ValueError, "role tokens"):
            discover({"examples": [a, b], "challenges": [c]})



if __name__ == "__main__":
    unittest.main()
