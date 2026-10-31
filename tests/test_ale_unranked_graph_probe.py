"""Held-out cross-modality adversarial tests for an unranked typed-graph probe."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_unranked_graph_probe import probe

def node(k, kind="INTERPRETATION", state="EXISTING_CONTEXT"):
    return {"id": k, "kind": kind, "status": state}

def edge(a,b,role="ASSOCIATION",sources=None):
    return {"from":a,"to":b,"role":role,
            "source_ids":sources or ["ada_2026"]}

def packet(candidates=None,established=None):
    return {"source_classification":"PUBLIC_SOURCE_LINKED",
            "focus":"diabetes-diagnosis",
            "nodes":[node("diabetes-diagnosis","DECISION"),
                     node("a1c-interpretation"),node("rbc-turnover","CONTEXT"),
                     node("hba1c-assay","MEASUREMENT"),
                     node("hb-variant","CONTEXT"),
                     node("unrelated-topic","MECHANISM")],
            "established_edges": established if established is not None else [
                {"from":"a1c-interpretation","to":"diabetes-diagnosis",
                 "role":"ASSOCIATION"}],
            "candidate_edges":candidates if candidates is not None else [
                edge("rbc-turnover","a1c-interpretation","VALIDITY_PREREQUISITE",["ada_2026","ngsp_2026"]),
                edge("hb-variant","hba1c-assay","MEASUREMENT_INTERFERENCE",["ngsp_methods_2026"]),
                edge("unrelated-topic","hb-variant","ASSOCIATION",["ada_2026"])]}

class UnrankedGapTests(unittest.TestCase):
    def test_no_rank_labels_input_yields_prioritized_missing_bridge(self):
        x=probe(packet())
        self.assertFalse(x["impact_labels_received"])
        self.assertEqual(x["most_urgent_candidate"]["from"],"rbc-turnover")
        self.assertEqual(x["most_urgent_candidate"]["role"],"VALIDITY_PREREQUISITE")
        self.assertFalse(x["independent_source_qa"])
        self.assertFalse(x["medical_semantics_inferred_from_raw_prose"])

    def test_same_tag_not_sufficient_for_causal_edge(self):
        x=probe(packet([edge("hb-variant","diabetes-diagnosis","IS_A")]))
        self.assertIsNone(x["most_urgent_candidate"])
        self.assertEqual(x["candidates"][0]["decision"],"ABSTAIN_RELATION")

    def test_existing_relation_not_renamed_novel(self):
        e={"from":"rbc-turnover","to":"a1c-interpretation",
           "role":"VALIDITY_PREREQUISITE"}
        x=probe(packet([edge(e["from"],e["to"],e["role"])],
                       established=[e,{"from":"a1c-interpretation",
                          "to":"diabetes-diagnosis","role":"ASSOCIATION"}]))
        self.assertEqual(x["candidates"][0]["decision"],"EXISTING_RELATION")
        self.assertIsNone(x["most_urgent_candidate"])

    def test_candidate_order_independent(self):
        q=packet()
        a=probe(q)
        q["candidate_edges"]=list(reversed(q["candidate_edges"]))
        self.assertEqual(a,probe(q))

    def test_no_presumed_truth_from_guideline_reference(self):
        x=probe(packet())
        self.assertFalse(x["candidates"][0]["clinical_truth_verified"])
        self.assertFalse(x["candidates"][0]["source_read_by_program"])
        self.assertEqual(x["concept_promotions"],0)

    def test_out_of_scope_gap_can_remain_unknown(self):
        x=probe(packet([edge("unrelated-topic","hb-variant")]))
        self.assertEqual(x["candidates"][0]["decision"],"PRESERVE_UNKNOWN")

    def test_reject_private_payload(self):
        q=packet()
        q["source_classification"]="OWNER_PRIVATE"
        with self.assertRaisesRegex(ValueError,"private"):
            probe(q)
        q=packet()
        q["notes"]="Patient HbA1c"
        with self.assertRaisesRegex(ValueError,"packet"):
            probe(q)

    def test_reject_broken_and_duplicate_relations(self):
        q=packet([edge("rbc-turnover","unknown","VALIDITY_PREREQUISITE")])
        with self.assertRaisesRegex(ValueError,"typed relation"):
            probe(q)
        q=packet([edge("rbc-turnover","a1c-interpretation","VALIDITY_PREREQUISITE")]*2)
        with self.assertRaisesRegex(ValueError,"duplicate"):
            probe(q)

    def test_no_fake_source_ids(self):
        q=packet([edge("rbc-turnover","a1c-interpretation","VALIDITY_PREREQUISITE",
                       ["https://private.google.com/patient"])])
        with self.assertRaisesRegex(ValueError,"public source"):
            probe(q)

    def test_missing_context_can_propose_extension_not_confirmation(self):
        q=packet([edge("rbc-turnover","a1c-interpretation","VALIDITY_PREREQUISITE")])
        q["nodes"][2]["status"]="EXTERNAL_ONLY"
        x=probe(q)
        self.assertEqual(x["candidates"][0]["context_operation_candidate"],
                         "SOURCE_CONTEXT_EXTENSION_CANDIDATE")

    def test_multiple_decisions_still_no_promotion(self):
        q=packet([edge("rbc-turnover","a1c-interpretation","VALIDITY_PREREQUISITE"),
                  edge("hba1c-assay","diabetes-diagnosis","DIAGNOSTIC_CONFIRMATION")])
        x=probe(q)
        self.assertEqual(sum(d["decision"]=="PRIORITY_RELATION_REVIEW"
                             for d in x["candidates"]),2)
        self.assertEqual(x["concept_promotions"],0)

if __name__ == "__main__":
    unittest.main()
