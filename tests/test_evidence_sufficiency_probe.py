"""A sufficient positive, sufficient negative, and insufficient UNKNOWN differ.

Synthetic test fixture only, not a medical adjudication or isolated model trial.
"""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from falsification_probe import (InvalidProbe, build_packets, prepare,
                                 run_adapter, score, compare_rescue, prepare_rescue)
SPEC = ROOT / "experiments/eth-falsification-probe/synthetic-evidence-sufficiency.json"
ADAPTER = ROOT / "experiments/eth-falsification-probe/sufficiency_toy_adapter.py"


class EvidenceSufficiencyTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads(SPEC.read_text())
        self.packets, self.key = build_packets(self.spec)

    def test_three_way_contract_positive_negative_unknown_and_stable(self):
        self.assertEqual(len(self.packets), 4)
        choices = {k: v["gold"]["decision_id"] for k,v in self.key["answers"].items()}
        self.assertEqual(choices["baseline"], choices["irrelevant_cover_color"])
        self.assertNotEqual(choices["document_unsigned"], choices["document_unknown"])
        self.assertEqual(self.key["answers"]["document_unknown"]["gold"]["support_status"],
                         "insufficient")
        self.assertTrue(all("support_status" not in p for p in self.packets))
        self.assertTrue(all("gold" not in p and "relation" not in p for p in self.packets))

    def test_conflicting_or_partial_gold_support_rejected(self):
        partial = copy.deepcopy(self.spec)
        del partial["probes"][0]["gold"]["support_status"]
        with self.assertRaisesRegex(InvalidProbe, "support_status must be present"):
            build_packets(partial)
        bad = copy.deepcopy(self.spec)
        bad["baseline_gold"]["support_status"] = "probably"
        with self.assertRaisesRegex(InvalidProbe, "invalid support_status"):
            build_packets(bad)

    def test_unknown_not_equated_with_explicit_unsigned(self):
        replies = {"case_id": self.key["case_id"], "responses": [
            {"probe_id": pid, "packet_sha256": a["packet_sha256"], **a["gold"]}
            for pid,a in self.key["answers"].items()]}
        self.assertTrue(score(self.key, replies)["passed"])
        unknown = next(r for r in replies["responses"] if r["probe_id"] == "document_unknown")
        unknown["decision_id"] = self.key["answers"]["document_unsigned"]["gold"]["decision_id"]
        unknown["support_status"] = "sufficient"
        out = score(self.key, replies)
        self.assertFalse(out["passed"])
        bad = next(r for r in out["results"] if r["probe_id"] == "document_unknown")
        self.assertEqual(bad["failed_stages"], ["S2_evidence", "S3_decision"])
        self.assertEqual(bad["first_observed_mismatch"], "S2_evidence")

    def test_unknown_stays_unknown_when_only_cover_changes(self):
        # Counterbalance the baseline: do not let availability of the record
        # be inferred from whether the probe is called a baseline or variant.
        unknown = copy.deepcopy(self.spec)
        unknown["case_id"] = "synthetic_evidence_support_unknown_first"
        unknown["facts"]["F1"] = self.spec["probes"][1]["new_value"]
        unknown["baseline_gold"] = copy.deepcopy(self.spec["probes"][1]["gold"])
        unknown["probes"] = [
            {"id":"cover_green", "fact_id":"F2", "new_value":"green",
             "relation":"stable", "gold":copy.deepcopy(unknown["baseline_gold"])},
            {"id":"new_signed_evidence", "fact_id":"F1",
             "new_value":self.spec["facts"]["F1"], "relation":"flip",
             "gold":copy.deepcopy(self.spec["baseline_gold"])},
        ]
        packets, key = build_packets(unknown)
        self.assertEqual(key["answers"]["baseline"]["gold"]["support_status"],
                         "insufficient")
        self.assertEqual(key["answers"]["cover_green"]["relation"], "stable")
        self.assertEqual(key["answers"]["new_signed_evidence"]["relation"], "flip")
        self.assertEqual(len(packets), 3)

    def test_real_subprocess_succeeds_with_new_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            prepare(SPEC, root / "packets", root / "keys" / "gold.json")
            run=run_adapter(root / "packets", root / "responses.json", ADAPTER, relabel=True)
            self.assertEqual(run["executed"], 4)
            self.assertEqual(run["isolation"], "NOT_VERIFIED")
            response=json.loads((root / "responses.json").read_text())
            out=score(json.loads((root / "keys" / "gold.json").read_text()), response)
            self.assertTrue(out["passed"])
            self.assertEqual(out["trial_count"], 4)

    def test_old_adapter_cannot_silently_drop_support_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            prepare(SPEC, root / "packets", root / "keys" / "gold.json")
            old = root / "old_adapter.py"
            old.write_text(ADAPTER.read_text().replace('"support_status": support,', ''),
                           encoding="utf-8")
            with self.assertRaisesRegex(InvalidProbe, "unexpected response fields"):
                run_adapter(root / "packets", root / "responses.json", old)
            self.assertFalse((root / "responses.json").exists())

    def test_rescue_pipeline_preserves_sufficiency_gold(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            hints=root / "hints.json"
            hints.write_text(json.dumps({"question_hint":"Identify signature status from a reliable record.",
                                         "evidence_hint":"A missing signature record is not a confirmed unsigned document."}))
            prepare_rescue(SPEC, hints, root / "arms", root / "keys")
            out=root / "answers"
            out.mkdir()
            for arm in ("N","Q","E","QE"):
                run_adapter(root / "arms" / arm, out / (arm+".json"), ADAPTER, relabel=True)
            report=compare_rescue(root / "keys", out)
            self.assertTrue(all(r["passed"] for r in report["arms"].values()))


if __name__ == "__main__":
    unittest.main()
