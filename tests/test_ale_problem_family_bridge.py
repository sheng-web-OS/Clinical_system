"""Regression tests for the source-linked, owner-directed ALE problem family candidate.

These tests enforce a bounded *structural/semantic-intent* contract only.
They do NOT confirm clinical source truth, independently review claims,
prove autonomous discovery or assess a private learner.
"""
import json
import unittest
from pathlib import Path


GRAPH = (Path(__file__).resolve().parents[1]
         / "experiments/ale-eudka-problem-family-bridge-20261031.json")


class TestProblemCenteredConceptFamily(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(GRAPH.read_text(encoding="utf-8"))
        cls.families = {f["id"]: f for f in cls.data["families"]}
        cls.concepts = {c["id"]: c for c in cls.data["concepts"]}
        cls.edges = {e["id"]: e for e in cls.data["typed_edges"]}
        cls.sources = {s["id"]: s for s in cls.data["source_refs"]}
        cls.q3 = {q["id"]: q for q in cls.data["q3_challenges"]}

    def test_family_structure_preserves_three_problem_contexts(self):
        local = [f for f in self.families.values()
                 if f["kind"] == "problem_centered"]
        bridge = [f for f in self.families.values()
                  if f["kind"] == "higher_order_bridge"]
        self.assertEqual(len(local), 3)
        self.assertEqual(len(bridge), 1)
        self.assertEqual(set(bridge[0]["component_family_ids"]),
                         {f["id"] for f in local})

    def test_unique_nodes_and_all_edges_refer_to_real_targets(self):
        data = self.data
        self.assertEqual(len(self.families), len(data["families"]))
        self.assertEqual(len(self.concepts), len(data["concepts"]))
        self.assertEqual(len(self.edges), len(data["typed_edges"]))
        ids = set(self.concepts) | set(self.families)
        for edge in self.edges.values():
            self.assertIn(edge["from"], ids)
            self.assertIn(edge["to"], ids)
            self.assertTrue(edge["type"] and edge["condition"])
            self.assertTrue(edge["source_ids"])
            self.assertTrue(set(edge["source_ids"]) <= set(self.sources))

    def test_concept_membership_can_be_traced_in_both_directions(self):
        for concept in self.concepts.values():
            for family_id in concept["family_ids"]:
                self.assertIn(family_id, self.families)
                self.assertIn(concept["id"],
                              self.families[family_id]["concept_ids"])
        for family in self.families.values():
            for cid in family["concept_ids"]:
                self.assertIn(cid, self.concepts)
                self.assertIn(family["id"],
                              self.concepts[cid]["family_ids"])

    def test_cross_family_bridge_is_an_analogy_not_taxonomic_merge(self):
        bridge = "CF_EVIDENCE_SCOPE_BRIDGE_V0"
        edges = [e for e in self.edges.values() if e["to"] == bridge]
        self.assertEqual(len(edges), 3)
        self.assertEqual({e["type"] for e in edges},
                         {"illustrates_shared_reasoning_pattern"})
        self.assertNotIn("is_a", {e["type"] for e in edges})
        self.assertNotIn("causes", {e["type"] for e in edges})

    def test_dka_ketones_do_not_alone_satisfy_formal_DKA(self):
        edge = self.edges["E3"]
        self.assertEqual(edge["from"], "C_EUDKA_KETONE_NOT_ETIOLOGY")
        self.assertEqual(edge["to"], "C_DKA24_THREE_COMPONENTS")
        self.assertEqual(edge["type"], "does_not_alone_satisfy")
        self.assertIn("D", edge["condition"])
        self.assertIn("A", edge["condition"])
        self.assertIn("Q3_C", self.q3)

    def test_MI_edges_target_classification_not_ischemia_evidence(self):
        for key in ("E6", "E7"):
            self.assertEqual(self.edges[key]["to"], "C_MI_CLASSIFICATION")
            self.assertEqual(self.edges[key]["type"], "insufficient_without")
        self.assertEqual(self.edges["E11"]["from"],
                         "C_MI_ISCHEMIC_EVIDENCE")
        self.assertEqual(self.edges["E11"]["to"], "C_MI_CLASSIFICATION")
        self.assertEqual(self.edges["E11"]["type"], "required_for")
        self.assertEqual(self.concepts["C_MI_CLASSIFICATION"]
                         ["inference_role"], "diagnostic_classification_target")

    def test_troponin_acute_injury_requires_threshold_and_serial_change(self):
        acute = self.concepts["C_TROPONIN_ACUITY"]["claim"].lower()
        self.assertIn("99th", acute)
        self.assertIn("rise/fall", acute)
        self.assertIn("Q3_G", self.q3)
        self.assertEqual(self.edges["E12"]["from"], "C_TROPONIN_INJURY")
        self.assertEqual(self.edges["E12"]["to"], "C_TROPONIN_ACUITY")
        self.assertEqual(self.edges["E12"]["type"], "insufficient_without")

    def test_type3_fatal_exception_blocks_universal_biomarker_rule(self):
        self.assertIn("type 3", self.concepts["C_MI_CLASSIFICATION"]
                      ["claim"].lower())
        q3 = self.q3["Q3_F"]
        self.assertIn("C_MI_CLASSIFICATION", q3["targets"])
        self.assertIn("S_MI18", q3["source_ids"])
        self.assertIn("type 3", q3["observation"].lower())

    def test_source_review_not_equated_to_independent_approval(self):
        self.assertIs(self.data["independent_medical_qa"], False)
        self.assertIs(self.data["canonical_knowledge_mutation"], False)
        self.assertIs(self.data["autonomous_semantic_induction"], False)
        self.assertIs(self.data["learner_gain_measured"], False)
        self.assertTrue(all(s["independent_qa"] is False
                            for s in self.sources.values()))

    def test_every_claim_and_q3_has_provenance(self):
        for concept in self.concepts.values():
            self.assertTrue(concept["source_ids"])
            self.assertTrue(set(concept["source_ids"]) <= set(self.sources))
        for challenge in self.q3.values():
            self.assertTrue(set(challenge["source_ids"]) <= set(self.sources))
            self.assertTrue(set(challenge["targets"]) <= set(self.concepts))

    def test_real_case_and_masked_case_not_conflated(self):
        real = self.sources["S_EUDKA_SITE"]["locator"]
        masked = self.q3["Q3_E"]["observation"]
        self.assertIn("NOT 2024 masked case", real)
        self.assertIn("283/266", masked)
        self.assertIn("186", masked)
        self.assertIn("TIMELINE_UNKNOWN", self.q3["Q3_E"]["disposition"])

    def test_no_private_learner_state_in_public_fixture(self):
        lower = GRAPH.read_text(encoding="utf-8").lower()
        for forbidden in ("private_sheet_url", "owner_email", "anki_card_id",
                          "review_history", "access_token", "password",
                          "learner_answer_event"):
            self.assertNotIn('"' + forbidden + '"', lower)


if __name__ == "__main__":
    unittest.main()
