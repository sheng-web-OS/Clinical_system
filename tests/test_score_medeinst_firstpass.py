"""Deterministic adversarial tests for MedEinst published-label scorer; NO real inference."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from prepare_medeinst_holdout import HoldoutError
from score_medeinst_firstpass import ARMS, read_frozen, score


def fixture():
    slots = ["s_" + f"{x:024x}" for x in range(1, 5)]
    digest = "a" * 64
    entries = {}
    case_ids = ("pair-one", "pair-one", "pair-two", "pair-two")
    variants = ("control", "trap", "control", "trap")
    labels = ("Diagnosis X", "Diagnosis Y", "Diagnosis P", "Diagnosis Q")
    crosswalk = {"source_class": "synthetic_fixture_not_medeinst",
                 "source_sha256": digest, "medical_gold_loaded": False,
                 "private_crosswalk_only": True, "cases": []}
    for idx, (slot, pair_id, var, label) in enumerate(
            zip(slots, case_ids, variants, labels), 1):
        packet_hash = f"{idx:064x}"
        entries[slot] = {"case_id": pair_id, "variant": var,
                         "ground_truth": label, "packet_sha256": packet_hash}
        crosswalk["cases"].append({"case_id": f"M{idx:02d}",
                                   "worker_slot": slot,
                                   "packet_sha256": packet_hash})
    gold = {"schema_version": 1, "dataset_sha256": digest,
            "entries": entries}
    # Control accuracy = 2/2 in each arm; each case scored independently.
    preds = {
        "native": ("Diagnosis X", "Diagnosis X", "Diagnosis P", "Diagnosis R"),
        "retrieval": ("Diagnosis X", "Diagnosis Y", "Diagnosis P", "Diagnosis P"),
        "skill": ("Diagnosis X", "Diagnosis Y", "Diagnosis P", "Diagnosis Q"),
    }
    records = []
    for arm in ARMS:
        for idx, label in enumerate(preds[arm], 1):
            records.append({
                "case_id": f"M{idx:02d}", "arm": arm,
                "attempt_status": "COMPLETED", "diagnosis": label,
                "first_pass_sha256": f"{(idx + len(arm)):064x}",
                "worker_context": f"isolated-fixture-{idx}-{arm}",
            })
    submission = {"schema_version": 1, "exposure": "development",
                  "records": records}
    return gold, crosswalk, submission


class MedEinstPublishedLabelScoreTests(unittest.TestCase):
    def setUp(self):
        self.gold, self.crosswalk, self.submission = fixture()

    def report(self):
        return score(self.gold, self.crosswalk, self.submission)

    def test_conditional_btr_is_not_one_minus_robust_accuracy(self):
        report = self.report()
        arms = report["arm_results"]
        self.assertEqual(0.5, arms["native"]["bias_trap_rate"])
        self.assertEqual(0, arms["native"]["robust_accuracy"])
        self.assertEqual(0.5, arms["retrieval"]["robust_accuracy"])
        self.assertEqual(0.5, arms["retrieval"]["bias_trap_rate"])
        self.assertEqual(1.0, arms["skill"]["robust_accuracy"])
        self.assertEqual(0.0, arms["skill"]["bias_trap_rate"])
        self.assertEqual(0.5, report["skill_minus_retrieval_robust_accuracy"])
        self.assertEqual(2, report["denominator_pairs"])

    def test_no_skill_or_clinical_certification_even_when_score_is_perfect(self):
        report = self.report()
        self.assertFalse(report["skill_transfer_validated"])
        self.assertFalse(report["promotion_authorized"])
        self.assertFalse(report["model_execution_verified"])
        self.assertFalse(report["clinical_expert_review_verified"])
        self.assertFalse(report["medical_gold_accepted_as_clinical_truth"])
        self.assertEqual("DEVELOPMENT_LABEL_MATCH_ONLY", report["status"])

    def test_no_protected_values_appear_in_aggregate_output(self):
        out = json.dumps(self.report())
        for forbidden in ["Diagnosis X", "Diagnosis P", "pair-one",
                          "isolated-fixture", "s_000000", "M01"]:
            self.assertNotIn(forbidden, out)

    def test_incomplete_call_refused_not_zero_scored(self):
        self.submission["records"][0]["attempt_status"] = "FAILED"
        with self.assertRaisesRegex(HoldoutError, "INCOMPLETE_MODEL_TRIAL_NO_SCORE"):
            self.report()

    def test_missing_trial_refused(self):
        self.submission["records"].pop()
        with self.assertRaisesRegex(HoldoutError, "INCOMPLETE_ARM_CASE_MATRIX"):
            self.report()

    def test_duplicate_trial_refused(self):
        self.submission["records"][0] = copy.deepcopy(self.submission["records"][1])
        with self.assertRaisesRegex(HoldoutError, "UNKNOWN_OR_DUPLICATE_TRIAL"):
            self.report()

    def test_shared_context_between_variants_refused(self):
        self.submission["records"][1]["worker_context"] = \
            self.submission["records"][0]["worker_context"]
        with self.assertRaisesRegex(HoldoutError, "WORKER_CONTEXT_NOT_UNIQUE"):
            self.report()

    def test_reused_answer_sha_is_not_proof_of_runtime(self):
        self.submission["records"][1]["first_pass_sha256"] = \
            self.submission["records"][0]["first_pass_sha256"]
        self.assertFalse(self.report()["model_execution_verified"])

    def test_no_correct_control_has_null_not_zero_bias_rate(self):
        for rec in self.submission["records"]:
            if rec["case_id"] in ("M01", "M03") and rec["arm"] == "native":
                rec["diagnosis"] = "Unknown"
        result = self.report()["arm_results"]["native"]
        self.assertEqual(0, result["bias_trap_denominator"])
        self.assertIsNone(result["bias_trap_rate"])
        self.assertEqual(0.0, result["control_accuracy"])

    def test_frozen_file_digests_must_match_true_bytes(self):
        with tempfile.TemporaryDirectory() as work:
            file = Path(work) / "frozen.json"
            raw = json.dumps(self.gold).encode()
            file.write_bytes(raw)
            expected = hashlib.sha256(raw).hexdigest()
            self.assertEqual(self.gold, read_frozen(file, expected))
            with self.assertRaisesRegex(HoldoutError, "FROZEN_FILE_CHANGED"):
                read_frozen(file, "f" * 64)
            with self.assertRaisesRegex(HoldoutError, "EXPECTED_FROZEN_FILE_SHA_REQUIRED"):
                read_frozen(file, "not-a-sha")

    def test_gold_crosswalk_hash_tampering_refused(self):
        self.gold["entries"][next(iter(self.gold["entries"]))]["packet_sha256"] = "b"*64
        with self.assertRaisesRegex(HoldoutError, "GOLD_CROSSWALK_BINDING_MISMATCH"):
            self.report()

    def test_different_benchmark_source_refused(self):
        self.crosswalk["source_sha256"] = "f"*64
        with self.assertRaisesRegex(HoldoutError, "SOURCE_DIGEST_CROSSWALK_MISMATCH"):
            self.report()

    def test_identical_control_and_trap_diagnoses_refused(self):
        vals = list(self.gold["entries"].values())
        vals[1]["ground_truth"] = vals[0]["ground_truth"]
        with self.assertRaisesRegex(HoldoutError, "UNPAIRED_OR_SAME_LABEL_GOLD"):
            self.report()

    def test_overbroad_model_answer_does_not_match_diagnosis_label(self):
        for rec in self.submission["records"]:
            if rec["case_id"] == "M02" and rec["arm"] == "skill":
                rec["diagnosis"] = "Diagnosis Y or Diagnosis X"
        self.assertEqual(0.5, self.report()["arm_results"]["skill"]["robust_accuracy"])

    def test_same_source_but_unverified_models_never_cause_promotion(self):
        self.submission["records"][0]["diagnosis"] = " Diagnosis   X "
        self.assertEqual(1.0, self.report()["arm_results"]["native"]["control_accuracy"])
        self.assertFalse(self.report()["promotion_authorized"])


if __name__ == "__main__":
    unittest.main()
