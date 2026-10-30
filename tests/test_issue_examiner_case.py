"""Offline one-case handoff tests: all examples are fictional; no network."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import seal_private_case_exam as seal
import issue_examiner_case as handoff


class IssueOneCaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fake_repo = self.root / "public"
        self.fake_repo.mkdir()
        self.exam = self.root / "examiner"
        self.gold_parent = self.root / "facilitator"
        self.worker_parent = self.root / "worker"
        for d in (self.exam, self.gold_parent, self.worker_parent):
            d.mkdir()
        self.stage = self.exam / "stage1"
        self.gold = self.gold_parent / "sealed"
        self.out = self.worker_parent / "inbox"
        cases = {"schema_version": 1, "source_class": "synthetic", "cases": [
            {"id": "fiction-1", "role": "transfer", "task": "This is a fictional task. Choose whether to inspect an extra source."},
            {"id": "fiction-2", "role": "normal", "task": "This is a fictional task. Ordinary reasoning is sufficient."},
            {"id": "fiction-3", "role": "boundary", "task": "This is a fictional task. Evidence is missing so pause."},
        ]}
        key = {"schema_version": 1, "keys": [
            {"id": f"fiction-{n}", "expected_decision": "SKIP",
             "clinical_rationale": "This is a fictional gold answer not for worker exposure."}
            for n in (1, 2, 3)
        ]}
        self.case_file = self.root / "cases.json"
        self.gold_file = self.root / "gold.json"
        self.case_file.write_text(json.dumps(cases))
        self.gold_file.write_text(json.dumps(key))
        seal.seal(
            self.case_file, self.gold_file, self.stage, self.gold,
            expected_cases_sha256=self.digest(self.case_file),
            expected_gold_sha256=self.digest(self.gold_file),
            suite_id="synthetic-holdout-001", repo_root=self.fake_repo)

    @staticmethod
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def call(self, **kw):
        args = dict(
            stage_root=self.stage, slot="H01", output_root=self.out,
            expected_manifest_sha256=self.digest(self.stage / "manifest.json"),
            expected_archive_sha256=self.digest(self.stage / "stage1.zip"),
            repo_root=self.fake_repo)
        args.update(kw)
        return handoff.issue_one(**args)

    def test_only_one_neutral_task_is_exported(self):
        receipt = self.call()
        self.assertEqual(receipt["status"], "ONE_CASE_EXPORTED_NOT_DELIVERED")
        self.assertEqual(receipt["file_count"], 1)
        self.assertFalse(receipt["worker_access_verified"])
        self.assertEqual({p.name for p in self.out.iterdir()}, {"task.md"})
        task = (self.out / "task.md").read_text()
        self.assertNotIn("fiction-", task)
        self.assertNotIn("clinical_rationale", task)
        self.assertNotIn("gold answer", task)
        self.assertEqual(hashlib.sha256(task.encode()).hexdigest(),
                         receipt["task_sha256"])
        self.assertEqual(os.stat(self.out).st_mode & 0o777, 0o700)
        self.assertEqual(os.stat(self.out / "task.md").st_mode & 0o777, 0o600)
        self.assertTrue((self.gold / "facilitator_key.json").exists())

    def test_unlisted_slot_rejected_without_output(self):
        with self.assertRaisesRegex(seal.SealError, "SLOT_NOT_FOUND"):
            self.call(slot="H99")
        self.assertFalse(self.out.exists())

    def test_malformed_slot_rejected_without_output(self):
        for name in ["../H01", "H01.md", "H01/other", "H1", "H01\n"]:
            with self.subTest(name=name):
                with self.assertRaisesRegex(seal.SealError, "SLOT_INVALID"):
                    self.call(slot=name)
                self.assertFalse(self.out.exists())

    def test_digest_mismatch_rejected_without_output(self):
        with self.assertRaisesRegex(seal.SealError, "EXAMINER_INPUT_DIGEST_MISMATCH"):
            self.call(expected_archive_sha256="0" * 64)
        self.assertFalse(self.out.exists())

    def test_manifest_tamper_rejected_even_when_rehashed(self):
        p = self.stage / "manifest.json"
        doc = json.loads(p.read_text())
        doc["secret_reviewer_key"] = "Fictional"
        p.write_text(json.dumps(doc))
        with self.assertRaisesRegex(seal.SealError, "STAGE1_SCHEMA_INVALID"):
            self.call()
        self.assertFalse(self.out.exists())

    def test_zip_extra_entry_rejected_even_when_rehashed(self):
        p = self.stage / "stage1.zip"
        with ZipFile(p, "a", compression=ZIP_DEFLATED) as z:
            z.writestr("gold.txt", "Fictional private gold")
        with self.assertRaisesRegex(seal.SealError, "STAGE1_ZIP_ENTRY_MISMATCH"):
            self.call()
        self.assertFalse(self.out.exists())

    def test_zip_edited_task_rejected_even_when_rehashed(self):
        p = self.stage / "stage1.zip"
        with ZipFile(p) as z:
            entries = {n:z.read(n) for n in z.namelist()}
        entries["H01.md"] = b"This fictional task was edited after sealing."
        with ZipFile(p, "w", compression=ZIP_DEFLATED) as z:
            for n, raw in entries.items():
                z.writestr(n, raw)
        with self.assertRaisesRegex(seal.SealError, "STAGE1_ZIP_SIZE_MISMATCH|STAGE1_ZIP_DIGEST_MISMATCH"):
            self.call()
        self.assertFalse(self.out.exists())

    def test_output_cannot_overlap_examiner(self):
        with self.assertRaisesRegex(seal.SealError, "WORKER_OUTPUT_OVERLAPS_EXAMINER"):
            self.call(output_root=self.exam / "worker")
        self.assertFalse((self.exam / "worker").exists())

    def test_output_cannot_enter_checkout(self):
        forbidden = TOOLS.parent / "__examiner_worker_export_forbidden__"
        self.assertFalse(forbidden.exists())
        with self.assertRaisesRegex(seal.SealError, "PUBLIC_REPO_PATH_FORBIDDEN"):
            self.call(output_root=forbidden)
        self.assertFalse(forbidden.exists())

    def test_output_must_be_new(self):
        self.out.mkdir()
        (self.out / "keep").write_text("preserve")
        with self.assertRaisesRegex(seal.SealError, "OUTPUT_ALREADY_EXISTS"):
            self.call()
        self.assertTrue((self.out / "keep").exists())

    def test_symlinked_stage_parent_is_rejected(self):
        alias = self.root / "alias"
        alias.symlink_to(self.exam, target_is_directory=True)
        with self.assertRaisesRegex(seal.SealError, "SYMLINK_ANCESTOR_FORBIDDEN"):
            self.call(stage_root=alias / "stage1")
        self.assertFalse(self.out.exists())

    def test_cli_success_has_no_model_or_isolation_claim(self):
        p = TOOLS / "issue_examiner_case.py"
        command = [sys.executable, str(p),
            "--stage-root", str(self.stage), "--slot", "H01",
            "--output-root", str(self.out),
            "--manifest-sha256", self.digest(self.stage / "manifest.json"),
            "--archive-sha256", self.digest(self.stage / "stage1.zip")]
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        doc = json.loads(result.stdout)
        self.assertEqual(doc["model_calls"], 0)
        self.assertFalse(doc["worker_access_verified"])
        self.assertEqual([p.name for p in self.out.iterdir()], ["task.md"])


if __name__ == "__main__":
    unittest.main()
