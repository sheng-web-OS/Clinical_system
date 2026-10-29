"""No model/provider required: verify exact-input counterfactual test harness."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from falsification_probe import build_packets, prepare, score, InvalidProbe


def fixture():
    """Purely fictional document-routing exercise, not a medical decision rule."""
    return {
        "schema_version": 1,
        "case_id": "synthetic_route_01",
        "task": "Choose the routing question and action; cite the fact IDs used. Simulated only.",
        "case_text": "The submission is described as {{F1}}. Its cover is {{F2}}.",
        "facts": {"F1": "signed by its submitter", "F2": "blue"},
        "candidate_questions": {"q_signature": "Is the submission signed?",
                                "q_cover": "Which cover color is most attractive?"},
        "candidate_decisions": {"accept": "accept for routing", "hold": "hold for signature"},
        "review_flag_ids": ["unsupported_completion"],
        "baseline_gold": {"question_id": "q_signature", "evidence_ids": ["F1"],
                          "decision_id": "accept", "review_flags": []},
        "probes": [
            {"id": "p01", "fact_id": "F1", "new_value": "missing a signature",
             "relation": "flip", "gold": {"question_id": "q_signature", "evidence_ids": ["F1"],
                                            "decision_id": "hold", "review_flags": []}},
            {"id": "p02", "fact_id": "F2", "new_value": "green",
             "relation": "stable", "gold": {"question_id": "q_signature", "evidence_ids": ["F1"],
                                              "decision_id": "accept", "review_flags": []}},
        ],
    }


def correct_replies(key):
    return {"case_id": key["case_id"], "responses": [
        {"probe_id": pid, "packet_sha256": a["packet_sha256"], **a["gold"]}
        for pid, a in key["answers"].items()]}


class FalsificationProbeTests(unittest.TestCase):
    def setUp(self):
        self.spec = fixture()
        self.packets, self.key = build_packets(self.spec)
        self.replies = correct_replies(self.key)

    def test_clean_pair_and_pivot_pass(self):
        report = score(self.key, self.replies)
        self.assertTrue(report["passed"])
        self.assertEqual(report["trial_count"], 3)
        self.assertEqual(report["results"][1]["observed_relation"], "flip")
        self.assertEqual(report["results"][2]["observed_relation"], "stable")

    def test_packets_show_only_one_changed_fact(self):
        base, pivot, noise = self.packets
        self.assertIn("[F1] signed by its submitter", base["case_text"])
        self.assertIn("[F1] missing a signature", pivot["case_text"])
        self.assertIn("[F2] green", noise["case_text"])
        self.assertIn("[F2] blue", pivot["case_text"])
        self.assertIn("[F1] signed by its submitter", noise["case_text"])
        self.assertFalse(any("gold" in p or "relation" in p for p in self.packets))

    def test_changed_answer_without_changed_evidence_is_wrong(self):
        self.replies["responses"][1]["decision_id"] = "accept"
        out = score(self.key, self.replies)
        self.assertFalse(out["passed"])
        self.assertEqual(out["results"][1]["first_observed_mismatch"], "S3_decision")
        self.assertFalse(out["results"][1]["relation_passed"])

    def test_wrong_question_is_first_observed_defect(self):
        self.replies["responses"][0]["question_id"] = "q_cover"
        out = score(self.key, self.replies)
        self.assertEqual(out["results"][0]["first_observed_mismatch"], "S1_question")

    def test_wrong_evidence_and_false_review_criticism(self):
        self.replies["responses"][0]["evidence_ids"] = ["F2"]
        self.replies["responses"][0]["review_flags"] = ["unsupported_completion"]
        out = score(self.key, self.replies)
        self.assertEqual(out["results"][0]["failed_stages"], ["S2_evidence", "S4_review"])

    def test_duplicate_or_stale_replies_fail_closed(self):
        self.replies["responses"][0]["packet_sha256"] = "old"
        with self.assertRaisesRegex(InvalidProbe, "stale"):
            score(self.key, self.replies)
        self.replies["responses"][0]["packet_sha256"] = self.packets[0]["packet_sha256"]
        self.replies["responses"].append(copy.deepcopy(self.replies["responses"][0]))
        with self.assertRaisesRegex(InvalidProbe, "duplicate"):
            score(self.key, self.replies)

    def test_missing_responses_fail_closed(self):
        self.replies["responses"].pop()
        with self.assertRaisesRegex(InvalidProbe, "missing or extra"):
            score(self.key, self.replies)

    def test_noop_or_inconsistent_gold_rejected(self):
        self.spec["probes"][0]["new_value"] = self.spec["facts"]["F1"]
        with self.assertRaisesRegex(InvalidProbe, "actually change"):
            build_packets(self.spec)
        self.spec = fixture()
        self.spec["probes"][0]["relation"] = "stable"
        with self.assertRaisesRegex(InvalidProbe, "contradicts"):
            build_packets(self.spec)

    def test_nonunique_placeholder_rejected(self):
        self.spec["case_text"] += " Again: {{F1}}"
        with self.assertRaisesRegex(InvalidProbe, "exactly one"):
            build_packets(self.spec)

    def test_key_not_exposed_to_reviewer_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec_path = root / "spec.json"
            spec_path.write_text(json.dumps(self.spec), encoding="utf-8")
            reviewer = root / "reviewer"
            key_path = root / "coordinator" / "key.json"
            prepared = prepare(spec_path, reviewer, key_path)
            self.assertEqual(len(prepared), 3)
            self.assertEqual(len(list(reviewer.glob("*.json"))), 3)
            self.assertEqual(set(json.loads((reviewer / "baseline.json").read_text())),
                             set(self.packets[0]))
            with self.assertRaisesRegex(InvalidProbe, "overwrite"):
                prepare(spec_path, reviewer, key_path)

    def test_refuse_key_under_reviewer_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec_path = root / "spec.json"
            spec_path.write_text(json.dumps(self.spec), encoding="utf-8")
            with self.assertRaisesRegex(InvalidProbe, "cannot reside"):
                prepare(spec_path, root / "reviewer", root / "reviewer" / "key.json")


if __name__ == "__main__":
    unittest.main()
