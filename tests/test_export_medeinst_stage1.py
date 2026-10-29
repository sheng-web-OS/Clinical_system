"""Synthetic structural tests; these do NOT certify actual medical case reasoning."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from prepare_medeinst_holdout import HoldoutError, prepare
from export_medeinst_stage1 import export_stage1, sha

ROWS = [
    {"case_id": "fixture-pair", "case_type": "control",
     "narrative": "SIMULATED long teaching vignette with a fictitious observation A and possible disease Q.",
     "ground_truth": "Fictitious Gold Q"},
    {"case_id": "fixture-pair", "case_type": "trap",
     "narrative": "SIMULATED long teaching vignette with a fictitious observation B and possible disease R.",
     "ground_truth": "Fictitious Gold R"},
]


class Stage1ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "public"
        self.repo.mkdir()
        self.dataset = self.root / "fiction.jsonl"
        self.dataset.write_text("".join(json.dumps(x) + "\n" for x in ROWS))
        digest = sha(self.dataset.read_bytes())
        self.worker = self.root / "workers"
        self.gold = self.root / "gold"
        prepare(self.dataset, digest, ["fixture-pair"], self.worker, self.gold,
                repo_root=self.repo, source_mode="synthetic-fixture")
        self.out = self.root / "stage"
    
    def go(self, **kw):
        opts = {
            "worker_root": self.worker, "output_dir": self.out,
            "expected_source_class": "synthetic_fixture_not_medeinst",
            "repo_root": self.repo,
        }
        opts.update(kw)
        return export_stage1(**opts)

    def test_stage1_zip_matches_pr225_manifest_contract_and_excludes_gold(self):
        result = self.go()
        self.assertEqual("STAGE1_ONLY_NO_MODEL_RUN", result["status"])
        self.assertEqual(0, result["actual_model_calls"])
        self.assertEqual(2, result["packets"])
        self.assertFalse(result["clinical_transfer_validated"])
        manifest = json.loads((self.out / "manifest.json").read_text())
        self.assertEqual(2, manifest["version"])
        self.assertEqual("PREPARED_NOT_RUN", manifest["status"])
        self.assertEqual(0, manifest["actual_model_calls"])
        self.assertEqual(["stage1/M01.md", "stage1/M02.md"],
                         [x["path"] for x in manifest["files"]])
        with ZipFile(self.out / "stage1.zip") as z:
            self.assertEqual(["M01.md", "M02.md"], z.namelist())
            for item in manifest["files"]:
                name = item["path"].removeprefix("stage1/")
                task = z.read(name)
                self.assertEqual(item["bytes"], len(task))
                self.assertEqual(item["sha256"], sha(task))
                self.assertNotIn(b"Fictitious Gold", task)
                self.assertNotIn(b"case_id", task)
                self.assertNotIn(b"ground_truth", task)
        private_crosswalk = json.loads((self.out / "private_crosswalk.json").read_text())
        self.assertEqual(2, len(private_crosswalk["cases"]))
        self.assertTrue(private_crosswalk["private_crosswalk_only"])
        self.assertFalse(private_crosswalk["medical_gold_loaded"])
        self.assertNotIn("Fictitious Gold", json.dumps(private_crosswalk))
        self.assertEqual(0o600, (self.out / "stage1.zip").stat().st_mode & 0o777)

    def test_source_mode_mismatch_fails_closed(self):
        with self.assertRaisesRegex(HoldoutError, "SOURCE_CLASS_MISMATCH"):
            self.go(expected_source_class="MedEinst_DDXPlus_simulated_research_case")
        self.assertFalse(self.out.exists())

    def test_output_inside_repo_fails_closed(self):
        with self.assertRaisesRegex(HoldoutError, "OUTPUT_MUST_BE_SEPARATE"):
            self.go(output_dir=self.repo / "stage")

    def test_refuse_reuse(self):
        self.go()
        with self.assertRaisesRegex(HoldoutError, "NEW_OUTPUT_ROOT_REQUIRED"):
            self.go()

    def test_reject_extra_worker_file(self):
        slot = next(self.worker.iterdir())
        (slot / "answers.json").write_text("EXPOSED")
        with self.assertRaisesRegex(HoldoutError, "UNSAFE_OR_UNEXPECTED_WORKER_SLOT"):
            self.go()

    def test_reject_label_injected_as_unexpected_field(self):
        slot = next(self.worker.iterdir())
        path = slot / "packet.json"
        packet = json.loads(path.read_text())
        packet["ground_truth"] = "Fictitious Gold"
        path.write_text(json.dumps(packet))
        with self.assertRaisesRegex(HoldoutError, "PACKET_UNEXPECTED_FIELDS"):
            self.go()

    def test_symlinked_slot_rejected(self):
        slot = next(self.worker.iterdir())
        alias = self.worker / ("s_" + "e"*24)
        alias.symlink_to(slot, target_is_directory=True)
        with self.assertRaisesRegex(HoldoutError, "UNSAFE_OR_UNEXPECTED_WORKER_SLOT"):
            self.go()

    def test_reject_oversize_case_text(self):
        slot = next(self.worker.iterdir())
        path = slot / "packet.json"
        data = json.loads(path.read_text())
        data["case_text"] = "x" * 12001
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(HoldoutError, "PACKET_INVALID_CONTENT"):
            self.go()

    def test_reject_unsafe_slot_name(self):
        slot = next(self.worker.iterdir())
        slot.rename(self.worker / "unvalidated-name")
        with self.assertRaisesRegex(HoldoutError, "UNSAFE_OR_UNEXPECTED_WORKER_SLOT"):
            self.go()

    def test_does_not_accept_public_repo_inputs(self):
        with self.assertRaisesRegex(HoldoutError, "WORKER_INPUT_MUST_BE_OUTSIDE_PUBLIC_REPO"):
            self.go(worker_root=self.repo)


if __name__ == "__main__":
    unittest.main()
