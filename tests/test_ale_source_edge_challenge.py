"""Regression tests for explicitly sourced, bounded Q0 -> edge/Q3 review.

These assertions prove lexical role parsing and false-merge avoidance,
NOT medical semantic understanding or correctness of PA diagnosis.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from ale_source_edge_challenge import review

SOURCE = json.loads((ROOT / "experiments/ale-pa-2025-raw-role-contrast-20261031.json").read_text(encoding="utf-8"))
COMPARISON = json.loads((ROOT / "experiments/ale-pa-2025-source-edge-comparison-20261031.json").read_text(encoding="utf-8"))


class SourceEdgeChallengerTests(unittest.TestCase):
    def test_real_guideline_fixture_produces_one_local_role_contrast(self):
        result = review(SOURCE, COMPARISON)
        self.assertEqual(len(result["source_local_role_contrasts"]), 1)
        parsed = result["source_local_role_contrasts"][0]
        self.assertEqual(parsed["subject_quote"], "Potassium")
        self.assertEqual(parsed["negative_purpose_quote"], "screening itself")
        self.assertIn("interpretation of aldosterone",
                      parsed["positive_purpose_quote"])

    def test_exact_source_offsets(self):
        parsed = review(SOURCE, COMPARISON)["source_local_role_contrasts"][0]
        for term, expected in (("subject", "Potassium"),
                               ("negative", "screening itself"),
                               ("positive", parsed["positive_purpose_quote"])):
            bounds = parsed["source_offsets"][term]
            self.assertEqual(SOURCE["excerpt"][bounds["start"]:bounds["end"]],
                             expected)

    def test_challenges_wrong_direct_role(self):
        decisions = {x["id"]: x for x in review(SOURCE, COMPARISON)["edge_judgments"]}
        self.assertEqual(decisions["pa_false_direct_screen"]["decision"],
                         "CHALLENGE_DIRECT_SCREENING_ROLE")
        self.assertEqual(decisions["pa_false_direct_screen"]["matched_side"], "negative")

    def test_supports_positive_role_only_as_candidate(self):
        decisions = {x["id"]: x for x in review(SOURCE, COMPARISON)["edge_judgments"]}
        self.assertEqual(decisions["pa_source_interpretation"]["decision"],
                         "TEXT_SUPPORTS_INTERPRETATION_ROLE_CANDIDATE")
        self.assertFalse(decisions["pa_source_interpretation"]["medical_truth_verified"])

    def test_does_not_overinfer_required_condition(self):
        decisions = {x["id"]: x for x in review(SOURCE, COMPARISON)["edge_judgments"]}
        self.assertEqual(decisions["pa_false_stronger_necessary"]["decision"],
                         "ABSTAIN_SCOPE_NOT_ESTABLISHED")

    def test_does_not_assign_potassium_role_to_renin(self):
        decisions = {x["id"]: x for x in review(SOURCE, COMPARISON)["edge_judgments"]}
        self.assertEqual(decisions["pa_false_shared_subject"]["decision"],
                         "ABSTAIN_NO_EXACT_LOCAL_ROLE_MATCH")

    def test_does_not_infer_normal_k_excludes_pa(self):
        decisions = {x["id"]: x for x in review(SOURCE, COMPARISON)["edge_judgments"]}
        self.assertEqual(decisions["pa_false_diagnosis_claim"]["decision"],
                         "ABSTAIN_SCOPE_NOT_ESTABLISHED")

    def test_missing_supporting_edge_creates_review_not_new_concept(self):
        no_support = copy.deepcopy(COMPARISON)
        no_support["edges"] = [no_support["edges"][0]]
        out = review(SOURCE, no_support)
        self.assertEqual(out["missing_positive_role_review"],
                         "SOURCE_PHRASE_RELATION_REVIEW_NEEDED")
        self.assertEqual(out["canonical_concept_ids_created"], 0)
        self.assertEqual(out["graph_edits"], 0)

    def test_complete_comparison_does_not_generate_fake_missing_edge(self):
        out = review(SOURCE, COMPARISON)
        self.assertEqual(out["missing_positive_role_review"], "NONE_DETECTED")
        self.assertIsNotNone(out["q3_question"])
        self.assertFalse(out["existing_graph_semantics_verified"])

    def test_no_cue_does_not_invent_relation(self):
        packet = {**SOURCE, "excerpt":
                  "Potassium is measured alongside plasma aldosterone and renin in adults with hypertension."}
        out = review(packet, COMPARISON)
        self.assertEqual(out["source_local_role_contrasts"], [])
        self.assertIsNone(out["q3_question"])
        self.assertEqual(out["missing_positive_role_review"], "NONE_DETECTED")

    def test_explicit_subject_synthetic_cross_domain_stays_tentative(self):
        packet = {**SOURCE, "excerpt":
                  "The marker is assessed not for treatment choice but to aid in laboratory interpretation."}
        comparison = {"source_classification": "PUBLIC_SYNTHETIC_ONLY", "edges": [
            {"id": "hypothesis", "subject_anchor": "The marker",
             "target_anchor": "laboratory interpretation", "relation": "AIDS_INTERPRETATION"}]}
        out = review(packet, comparison)
        self.assertEqual(out["edge_judgments"][0]["decision"],
                         "TEXT_SUPPORTS_INTERPRETATION_ROLE_CANDIDATE")
        self.assertFalse(out["original_source_full_context_checked"])

    def test_same_keyword_different_subject_abstains(self):
        comparison = copy.deepcopy(COMPARISON)
        comparison["edges"] = [{"id": "hypothesis", "subject_anchor": "aldosterone",
                               "target_anchor": "screening itself",
                               "relation": "DIRECT_SCREENING_TEST"}]
        out = review(SOURCE, comparison)
        self.assertEqual(out["edge_judgments"][0]["decision"],
                         "ABSTAIN_NO_EXACT_LOCAL_ROLE_MATCH")

    def test_private_source_rejected(self):
        p = {**SOURCE, "source_classification": "OWNER_PRIVATE"}
        with self.assertRaisesRegex(ValueError, "private"):
            review(p, COMPARISON)

    def test_unexpected_candidate_roles_rejected(self):
        p = copy.deepcopy(COMPARISON)
        p["edges"][0]["relation"] = "CANONICAL_IS_A"
        with self.assertRaisesRegex(ValueError, "anchors"):
            review(SOURCE, p)

    def test_privacy_not_waived_by_public_label(self):
        p = copy.deepcopy(COMPARISON)
        p["edges"][0]["subject_anchor"] = "user@private.test"
        with self.assertRaises(ValueError):
            review(SOURCE, p)

    def test_editorial_negation_abstains(self):
        p = {**SOURCE, "excerpt":
             "The preprint is assessed not for publication but to support editorial checking."}
        out = review(p, {"source_classification": "PUBLIC_SYNTHETIC_ONLY", "edges": []})
        self.assertEqual(out["source_local_role_contrasts"], [])

    def test_duplicate_edge_id_rejected(self):
        p = copy.deepcopy(COMPARISON)
        p["edges"].append(copy.deepcopy(p["edges"][0]))
        with self.assertRaises(ValueError):
            review(SOURCE, p)

    def test_no_private_read_or_mutation(self):
        out = review(SOURCE, COMPARISON)
        self.assertIs(out["learner_state_read"], False)
        self.assertEqual(out["graph_edits"], 0)
        self.assertFalse(out["existing_graph_semantics_verified"])

    def test_determinism(self):
        self.assertEqual(review(SOURCE, COMPARISON), review(SOURCE, COMPARISON))


if __name__ == "__main__":
    unittest.main()
