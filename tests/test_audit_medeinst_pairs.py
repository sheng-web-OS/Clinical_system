"""No medical inference: test paired MedEinst audit contract on invented text."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from audit_medeinst_pairs import audit
from prepare_medeinst_holdout import HoldoutError, MEDEINST_TEST_SHA256


class AggregateAuditContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = self.root / "synthetic.jsonl"
        prefix = "SIMULATED CASE with a fictitious symptom for a testing-only diagnosis comparison. "
        self.records = [
            {"case_id": "a", "case_type": "control",
             "narrative": prefix + "Observation M.", "ground_truth": "Gold X"},
            {"case_id": "a", "case_type": "trap",
             "narrative": prefix + "Observation N.", "ground_truth": "Gold Y"},
            {"case_id": "b", "case_type": "control",
             "narrative": prefix + "Observation Q.", "ground_truth": "Gold P"},
            {"case_id": "b", "case_type": "trap",
             "narrative": prefix + "Observation R.", "ground_truth": "Gold S"},
        ]
        self.save()

    def save(self):
        raw = "".join(json.dumps(r, ensure_ascii=False) + "\n"
                      for r in self.records).encode()
        self.path.write_bytes(raw)
        self.sha = hashlib.sha256(raw).hexdigest()

    def call(self):
        return audit(self.path, self.sha, mode="synthetic-fixture")

    def test_aggregate_only_and_not_clinically_certified(self):
        result = self.call()
        self.assertEqual(2, result["pairs"])
        self.assertEqual(4, result["dataset_records"])
        self.assertEqual("STRUCTURAL_AUDIT_ONLY", result["verdict"])
        self.assertFalse(result["one_fact_intervention_verified"])
        self.assertFalse(result["clinical_counterfactual_validated"])
        self.assertEqual(0, result["model_calls"])
        dumped = json.dumps(result)
        for forbidden in ("SIMULATED CASE", "Gold X", '"case_id"', '"narrative"'):
            self.assertNotIn(forbidden, dumped)

    def test_works_with_case_suffixes(self):
        for r in self.records:
            r["case_type"] += "_case"
        self.save()
        self.assertEqual(2, self.call()["pairs"])

    def test_incomplete_pair_fails(self):
        self.records.pop()
        self.save()
        with self.assertRaisesRegex(HoldoutError, "INCOMPLETE_DATASET_PAIR"):
            self.call()

    def test_duplicate_variant_fails(self):
        self.records.append(self.records[0].copy())
        self.save()
        with self.assertRaisesRegex(HoldoutError, "DUPLICATE_PAIR_VARIANT"):
            self.call()

    def test_duplicate_gold_is_detected_without_leaking_labels(self):
        self.records[1]["ground_truth"] = self.records[0]["ground_truth"]
        self.save()
        report = self.call()
        self.assertEqual(1, report["same_diagnosis_label_pairs"])
        self.assertEqual("HOLD_DATASET_PAIR_SEMANTICS", report["verdict"])
        self.assertNotIn("Gold X", json.dumps(report))

    def test_identical_case_text_is_detected(self):
        self.records[1]["narrative"] = self.records[0]["narrative"]
        self.save()
        report = self.call()
        self.assertEqual(1, report["identical_narrative_pairs"])
        self.assertEqual("HOLD_DATASET_PAIR_SEMANTICS", report["verdict"])

    def test_digest_refuses_changed_dataset(self):
        self.path.write_text(self.path.read_text() + "\n", encoding="utf-8")
        with self.assertRaisesRegex(HoldoutError, "DATASET_DIGEST_MISMATCH"):
            self.call()

    def test_official_source_requires_published_sha(self):
        with self.assertRaisesRegex(HoldoutError, "UNTRUSTED_BENCHMARK_SHA256"):
            audit(self.path, self.sha)
        with self.assertRaisesRegex(HoldoutError, "DATASET_DIGEST_MISMATCH"):
            audit(self.path, MEDEINST_TEST_SHA256)

    def test_invalid_variant_type_fails_closed(self):
        self.records[0]["case_type"] = "intervention"
        self.save()
        with self.assertRaisesRegex(HoldoutError, "INVALID_AUDIT_RECORD"):
            self.call()

    def test_invalid_json_fails_closed(self):
        self.path.write_text("{broken")
        self.sha = hashlib.sha256(self.path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(HoldoutError, "INVALID_JSONL"):
            self.call()

    def test_invalid_id_is_not_coerced(self):
        self.records[0]["case_id"] = 88
        self.save()
        with self.assertRaisesRegex(HoldoutError, "INVALID_AUDIT_RECORD"):
            self.call()

    def test_malformed_label_fails(self):
        self.records[0]["ground_truth"] = ""
        self.save()
        with self.assertRaisesRegex(HoldoutError, "INVALID_AUDIT_RECORD"):
            self.call()


    def test_one_long_official_style_narrative_is_a_worker_exclusion_not_malformed_data(self):
        self.records[0]["narrative"] += ("A" * 12500)
        self.save()
        report = self.call()
        self.assertEqual(1, report["narratives_above_worker_limit"])
        self.assertEqual(1, report["pairs_above_worker_limit"])
        self.assertEqual("STRUCTURAL_AUDIT_WITH_WORKER_EXCLUSIONS", report["verdict"])
        self.assertFalse(report["one_fact_intervention_verified"])

    def test_invalid_extremely_short_narrative_stays_rejected(self):
        self.records[0]["narrative"] = "too short"
        self.save()
        with self.assertRaisesRegex(HoldoutError, "INVALID_AUDIT_RECORD"):
            self.call()


if __name__ == "__main__":
    unittest.main()
