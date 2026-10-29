"""Mechanical tests only; passing them does not establish medical validity."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from prepare_medeinst_holdout import HoldoutError, prepare, MEDEINST_TEST_SHA256


class MedEinstHoldoutContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.dataset = self.root / "synthetic-demo.jsonl"
        self.worker = self.root / "workers"
        self.private = self.root / "facilitator"
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.rows = [
            {"case_id": "demo-1", "case_type": "control", "narrative": "SIMULATED PLACEHOLDER: a patient has symptom A and feature B, with no other facts.", "ground_truth": "Diagnosis X"},
            {"case_id": "demo-1", "case_type": "trap", "narrative": "SIMULATED PLACEHOLDER: a patient has symptom A and feature C, with no other facts.", "ground_truth": "Diagnosis Y"},
            {"case_id": "demo-2", "case_type": "control", "narrative": "SIMULATED PLACEHOLDER: a patient has symptom Z and feature L, with no other facts.", "ground_truth": "Diagnosis P"},
            {"case_id": "demo-2", "case_type": "trap", "narrative": "SIMULATED PLACEHOLDER: a patient has symptom Z and feature M, with no other facts.", "ground_truth": "Diagnosis Q"},
        ]
        self.save()

    def save(self):
        raw = "".join(json.dumps(r) + "\n" for r in self.rows).encode("utf-8")
        self.dataset.write_bytes(raw)
        self.digest = hashlib.sha256(raw).hexdigest()

    def run_pilot(self, ids=None, digest=None, worker=None, private=None):
        return prepare(self.dataset, digest or self.digest,
                       ids or ["demo-1", "demo-2"],
                       worker or self.worker, private or self.private,
                       repo_root=self.repo, source_mode="synthetic-fixture")

    def test_offline_blinding_and_secret_separation(self):
        result = self.run_pilot()
        self.assertEqual({"worker_packets": 4, "model_calls": 0, "status": "NOT_RUN"}, result)
        packets = list(self.worker.glob("*/packet.json"))
        self.assertEqual(4, len(packets))
        key = json.loads((self.private / "answer_key.json").read_text())
        self.assertEqual({"control", "trap"}, {v["variant"] for v in key["entries"].values()})
        self.assertEqual(4, len(key["entries"]))
        for path in packets:
            raw = path.read_bytes()
            self.assertNotIn(b"ground_truth", raw)
            self.assertNotIn(b"case_id", raw)
            self.assertNotIn(b"Diagnosis X", raw)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),
                             key["entries"][path.parent.name]["packet_sha256"])
        self.assertEqual("NOT_RUN", json.loads((self.private / "run_manifest.json").read_text())["status"])

    def test_stale_or_forged_input_digest_fails_closed(self):
        with self.assertRaisesRegex(HoldoutError, "DATASET_DIGEST_MISMATCH"):
            self.run_pilot(digest="e" * 64)
        self.assertFalse(self.worker.exists())

    def test_missing_pair_fails_closed(self):
        self.rows.pop()
        self.save()
        with self.assertRaisesRegex(HoldoutError, "INCOMPLETE_SELECTED_PAIR"):
            self.run_pilot()

    def test_duplicate_variant_fails_closed(self):
        self.rows.append(self.rows[0].copy())
        self.save()
        with self.assertRaisesRegex(HoldoutError, "DUPLICATE_SELECTED_VARIANT"):
            self.run_pilot()

    def test_same_label_not_a_counterfactual_flip(self):
        self.rows[1]["ground_truth"] = self.rows[0]["ground_truth"]
        self.save()
        with self.assertRaisesRegex(HoldoutError, "COUNTERFACTUAL_LABELS_NOT_DISTINCT"):
            self.run_pilot()

    def test_no_result_inside_public_repo(self):
        with self.assertRaisesRegex(HoldoutError, "OUTPUT_INSIDE_PUBLIC_REPOSITORY"):
            self.run_pilot(worker=self.repo / "workers")

    def test_reject_nested_reviewer_gold_and_worker_roots(self):
        with self.assertRaisesRegex(HoldoutError, "OUTPUT_ROOTS_MUST_BE_SEPARATE"):
            self.run_pilot(worker=self.root / "workers", private=self.root / "workers" / "private")

    def test_reject_reuse_to_prevent_overwrite(self):
        self.run_pilot()
        with self.assertRaisesRegex(HoldoutError, "OUTPUT_MUST_BE_NEW"):
            self.run_pilot()

    def test_missing_selected_case_fails_closed(self):
        with self.assertRaisesRegex(HoldoutError, "SELECTED_CASE_ID_MISSING"):
            self.run_pilot(ids=["absent"])

    def test_malformed_jsonl_fails_closed(self):
        self.dataset.write_text("{not-json}\n", encoding="utf-8")
        bad_digest = hashlib.sha256(self.dataset.read_bytes()).hexdigest()
        with self.assertRaisesRegex(HoldoutError, "INVALID_JSONL"):
            self.run_pilot(digest=bad_digest)

    def test_symlinked_output_parent_fails_closed(self):
        alias = self.root / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(HoldoutError, "OUTPUT_SYMLINK_ANCESTOR"):
            self.run_pilot(worker=alias / "workers")

    def test_reject_duplicate_pair_selection(self):
        with self.assertRaisesRegex(HoldoutError, "PRESELECT"):
            self.run_pilot(ids=["demo-1", "demo-1"])

    def test_official_mode_rejects_self_pinned_arbitrary_file(self):
        with self.assertRaisesRegex(HoldoutError, "UNTRUSTED_BENCHMARK_SHA256"):
            prepare(self.dataset, self.digest, ["demo-1"],
                    self.worker, self.private, repo_root=self.repo)
        self.assertFalse(self.worker.exists())

    def test_official_source_hash_constant_matches_published_xet_digest(self):
        self.assertEqual(64, len(MEDEINST_TEST_SHA256))
        self.assertEqual("b6b688fa41f788c17cdbf5076b5215782c9eb00efec1a3d3384c002836550a57",
                         MEDEINST_TEST_SHA256)
        with self.assertRaisesRegex(HoldoutError, "DATASET_DIGEST_MISMATCH"):
            prepare(self.dataset, MEDEINST_TEST_SHA256, ["demo-1"],
                    self.worker, self.private, repo_root=self.repo)

    def test_identical_narratives_with_different_diagnoses_rejected(self):
        self.rows[1]["narrative"] = self.rows[0]["narrative"]
        self.save()
        with self.assertRaisesRegex(HoldoutError, "IDENTICAL_NARRATIVES_WITH_CONFLICTING_LABELS"):
            self.run_pilot()

    def test_invalid_case_id_type_rejected(self):
        self.rows[0]["case_id"] = ["demo-1"]
        self.save()
        with self.assertRaisesRegex(HoldoutError, "INVALID_CASE_ID_TYPE"):
            self.run_pilot()

    def test_synthetic_mode_cannot_claim_official_medeinst(self):
        self.run_pilot(ids=["demo-1"])
        packet = next(self.worker.glob("*/packet.json"))
        self.assertEqual("synthetic_fixture_not_medeinst",
                         json.loads(packet.read_text())["source_class"])
        metadata = json.loads((self.private / "run_manifest.json").read_text())
        self.assertEqual("synthetic-fixture", metadata["source_mode"])
        self.assertFalse(metadata["medical_validated"])


if __name__ == "__main__":
    unittest.main()
