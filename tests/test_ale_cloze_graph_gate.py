"""Public-safe regression: real graph ID/edge anchored, *model-authored* Cloze pilots.

These tests catch documented engineering/contract regressions and known
ambiguous exam-meta templates, NOT medical correctness or reader usefulness.
"""
import copy
import json
import unittest
from pathlib import Path

from tools.ale_cloze_graph_gate import list_graph_targets, check_graph_anchored_cloze

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "experiments/ale-eudka-problem-family-bridge-20261031.json"
PILOT = ROOT / "experiments/ale-cloze-graph-pilot-20261031.json"


class TestSourceLinkedClozeGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = json.loads(GRAPH.read_text(encoding="utf-8"))
        cls.pilot = json.loads(PILOT.read_text(encoding="utf-8"))

    def proposal(self, index=0):
        return copy.deepcopy(self.pilot["proposals"][index])

    def test_graph_first_discovers_valid_relation_targets_without_cards(self):
        targets = list_graph_targets(self.graph)
        ids = {t["edge_id"] for t in targets}
        self.assertTrue({"E4", "E5", "E7", "E12"} <= ids)
        self.assertFalse({"E8", "E9", "E10"} & ids)
        self.assertTrue(all(t["candidate_only"] and not t["has_generated_card"]
                            for t in targets))
        self.assertTrue(all(t["suggested_format"] == "Cloze" for t in targets))

    def test_three_real_source_anchored_proposals_render(self):
        self.assertEqual(len(self.pilot["proposals"]), 3)
        r = [check_graph_anchored_cloze(self.graph, p)
             for p in self.pilot["proposals"]]
        self.assertEqual([x["card_count"] for x in r], [1, 1, 2])
        self.assertEqual([x["cloze_count"] for x in r], [2, 2, 3])
        self.assertIn("{{c1::", r[0]["text"])
        self.assertIn("{{c2::", r[2]["text"])
        self.assertTrue(all(not x["ready_to_import"] for x in r))
        self.assertTrue(all(x["semantic_acceptance"] == "PENDING_INDEPENDENT_REVIEW"
                            for x in r))
        self.assertTrue(all(x["owner_acceptance"] == "NOT_OBSERVED" for x in r))

    def test_wrong_decision_target_rejected(self):
        p = self.proposal(1)
        p["concept_node_id"] = "C_MI_ISCHEMIC_EVIDENCE"
        with self.assertRaisesRegex(ValueError, "WRONG_CONCEPT_TARGET"):
            check_graph_anchored_cloze(self.graph, p)

    def test_source_suppression_and_fabrication_rejected(self):
        p = self.proposal()
        p["source_refs"] = ["S_MI18"]
        with self.assertRaisesRegex(ValueError, "SOURCE_MISMATCH"):
            check_graph_anchored_cloze(self.graph, p)
        p = self.proposal()
        p["source_refs"] = []
        with self.assertRaisesRegex(ValueError, "PROVENANCE"):
            check_graph_anchored_cloze(self.graph, p)

    def test_topic_only_with_no_edge_rejected(self):
        p = self.proposal()
        del p["edge_id"]
        with self.assertRaisesRegex(ValueError, "MISSING_OR_UNSUPPORTED"):
            check_graph_anchored_cloze(self.graph, p)

    def test_higher_order_bridge_is_not_clinical_card(self):
        p = self.proposal()
        p["edge_id"] = "E8"
        with self.assertRaisesRegex(ValueError, "MISSING_OR_UNSUPPORTED"):
            check_graph_anchored_cloze(self.graph, p)

    def test_guarded_exam_meta_template_rejected(self):
        p = self.proposal()
        p["template"] = "在考題中，這代表[[conclusion]]，因缺乏[[chronicity]]。"
        with self.assertRaisesRegex(ValueError, "EXAM_META"):
            check_graph_anchored_cloze(self.graph, p)
        p = self.proposal()
        p["learning_goal"] = "國考情境中的隱藏線索"
        with self.assertRaisesRegex(ValueError, "EXAM_META"):
            check_graph_anchored_cloze(self.graph, p)

    def test_missing_scope_or_edge_reason_rejected(self):
        p = self.proposal()
        p["scope_boundary"] = ""
        with self.assertRaisesRegex(ValueError, "SCOPE"):
            check_graph_anchored_cloze(self.graph, p)
        p = self.proposal()
        p["reason_this_tests_edge"] = ""
        with self.assertRaisesRegex(ValueError, "EDGE_TO_RETRIEVAL"):
            check_graph_anchored_cloze(self.graph, p)

    def test_wrong_relation_label_rejected(self):
        p = self.proposal()
        p["tested_relation"] = "is_a"
        with self.assertRaisesRegex(ValueError, "WRONG_CONCEPT_TARGET"):
            check_graph_anchored_cloze(self.graph, p)
        p = self.proposal()
        p["retrieval_role"] = "none"
        with self.assertRaisesRegex(ValueError, "RETRIEVAL_ROLE"):
            check_graph_anchored_cloze(self.graph, p)

    def test_missing_hint_and_incoherent_group_are_rejected(self):
        p = self.proposal()
        p["slots"][0]["needs_hint"] = True
        p["slots"][0]["hint"] = ""
        with self.assertRaisesRegex(ValueError, "hint"):
            check_graph_anchored_cloze(self.graph, p)
        p = self.proposal()
        p["why_together"] = ""
        with self.assertRaisesRegex(ValueError, "coherence"):
            check_graph_anchored_cloze(self.graph, p)

    def test_no_private_owner_material_in_public_fixture(self):
        fixture = PILOT.read_text(encoding="utf-8").lower()
        for bad in ("anki_card_id", "owner_email", "learner_answer_event",
                    "private_sheet_url", "access_token", "review_history"):
            self.assertNotIn('"' + bad + '"', fixture)
        self.assertIs(self.pilot["owner_private_data"], False)
        self.assertIs(self.pilot["ankiconnect_write"], False)


if __name__ == "__main__":
    unittest.main()
