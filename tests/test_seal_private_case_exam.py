"""Private examiner smoke uses wholly fictional, synthetic data only."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

P = Path(__file__).resolve().parents[1] / "tools" / "seal_private_case_exam.py"
spec = importlib.util.spec_from_file_location("seal_private_case_exam", P)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class SealTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "public_repo"
        self.repo.mkdir()
        self.a = self.root / "examiner"
        self.b = self.root / "facilitator"
        self.a.mkdir()
        self.b.mkdir()
        self.st = self.a / "sealed"
        self.key = self.b / "sealed"
        self.cases = {"schema_version": 1, "source_class": "synthetic", "cases": [
            {"id": "case-01", "role": "transfer", "task": "Fictional subject has marker X; choose whether evidence is required."},
            {"id": "case-02", "role": "normal", "task": "Fictional normal control; leave stable findings unchanged."},
            {"id": "case-03", "role": "boundary", "task": "Fictional background-only question; avoid invented diagnosis."},
        ]}
        self.gold = {"schema_version": 1, "keys": [
            {"id": f"case-0{i}", "expected_decision": "SKIP" if i != 1 else "RETRIEVE",
             "clinical_rationale": "Fictional synthetic control; not medical gold."}
            for i in range(1, 4)
        ]}
        self.case_file = self.root / "cases.json"
        self.gold_file = self.root / "gold.json"
        self.save()

    def save(self):
        self.case_file.write_text(json.dumps(self.cases), encoding="utf-8")
        self.gold_file.write_text(json.dumps(self.gold), encoding="utf-8")

    def call(self, **overrides):
        args = dict(cases_file=self.case_file, gold_file=self.gold_file,
                    stage1_root=self.st, key_root=self.key,
                    expected_cases_sha256=hashlib.sha256(self.case_file.read_bytes()).hexdigest(),
                    expected_gold_sha256=hashlib.sha256(self.gold_file.read_bytes()).hexdigest(),
                    suite_id="holdout-2026-01", repo_root=self.repo)
        args.update(overrides)
        return m.seal(**args)

    def test_success_staged_handoff_and_gold_separate(self):
        receipt = self.call()
        self.assertEqual(receipt["status"], "PREPARED_NOT_RUN")
        self.assertFalse(receipt["worker_isolation_verified"])
        manifest = json.loads((self.st / "manifest.json").read_text())
        self.assertEqual(manifest["version"], 2)
        self.assertEqual(manifest["actual_model_calls"], 0)
        self.assertEqual({x["path"] for x in manifest["files"]},
                         {"stage1/H01.md", "stage1/H02.md", "stage1/H03.md"})
        with ZipFile(self.st / "stage1.zip") as z:
            self.assertEqual(set(z.namelist()), {"H01.md", "H02.md", "H03.md"})
            for row in manifest["files"]:
                self.assertEqual(hashlib.sha256(z.read(row["path"].removeprefix("stage1/"))).hexdigest(), row["sha256"])
            self.assertNotIn(b"Fictional synthetic control; not medical gold.", b"".join(z.read(n) for n in z.namelist()))
        self.assertNotIn("case-01", (self.st / "manifest.json").read_text())
        self.assertIn("case-01", (self.key / "facilitator_key.json").read_text())
        self.assertFalse(json.loads((self.key / "facilitator_key.json").read_text())["independent_reviewer_authenticated"])
        self.assertEqual(os.stat(self.key).st_mode & 0o777, 0o700)
        self.assertEqual(os.stat(self.key / "facilitator_key.json").st_mode & 0o777, 0o600)

    def test_hash_mismatch_fail_closed(self):
        with self.assertRaisesRegex(m.SealError, "FROZEN_SOURCE_MISMATCH"):
            self.call(expected_cases_sha256="a" * 64)
        self.assertFalse(self.st.exists())

    def test_gold_mismatch_fail_closed(self):
        self.gold["keys"].pop()
        self.save()
        with self.assertRaisesRegex(m.SealError, "ANSWER_KEY_COVERAGE_MISMATCH"):
            self.call()
        self.assertFalse(self.st.exists())

    def test_duplicate_case_fail_closed(self):
        self.cases["cases"][1]["id"] = "case-01"
        self.save()
        with self.assertRaisesRegex(m.SealError, "CASE_ID_INVALID_OR_DUPLICATE"):
            self.call()

    def test_requires_normal_and_boundary_controls(self):
        self.cases["cases"][2]["role"] = "transfer"
        self.save()
        with self.assertRaisesRegex(m.SealError, "TRANSFER_NORMAL_BOUNDARY_CONTROLS_REQUIRED"):
            self.call()

    def test_refuse_public_git_path(self):
        with self.assertRaisesRegex(m.SealError, "PUBLIC_REPO_PATH_FORBIDDEN"):
            self.call(stage1_root=self.repo / "packets")
        self.assertFalse((self.repo / "packets").exists())

    def test_refuse_public_repo_input(self):
        source = self.repo / "private-vignette.json"
        source.write_bytes(self.case_file.read_bytes())
        with self.assertRaisesRegex(m.SealError, "PUBLIC_REPO_INPUT_FORBIDDEN"):
            self.call(cases_file=source)

    def test_refuse_same_parent_for_gold(self):
        with self.assertRaisesRegex(m.SealError, "EXAMINER_AND_GOLD_ROOTS_MUST_BE_SEPARATED"):
            self.call(key_root=self.a / "keys")

    def test_refuse_existing_output_and_preserve(self):
        self.st.mkdir()
        (self.st / "keep.txt").write_text("do not delete")
        with self.assertRaisesRegex(m.SealError, "OUTPUT_ALREADY_EXISTS"):
            self.call()
        self.assertTrue((self.st / "keep.txt").exists())

    def test_refuse_symlink_source(self):
        x = self.root / "pointer"
        x.symlink_to(self.case_file)
        with self.assertRaisesRegex(m.SealError, "PRIVATE_SOURCE_INVALID"):
            self.call(cases_file=x)

    def test_refuse_unbounded_case(self):
        self.cases["cases"][0]["task"] = "x" * 12001
        self.save()
        with self.assertRaisesRegex(m.SealError, "TASK_MISSING_OR_TOO_LARGE"):
            self.call()

    def test_refuse_unknown_case_fields(self):
        self.cases["cases"][0]["patient_name"] = "Fake"
        self.save()
        with self.assertRaisesRegex(m.SealError, "ONLY_NEUTRAL_CASE_FIELDS_ALLOWED"):
            self.call()

    def test_invalid_source_class_fail_closed(self):
        self.cases["source_class"] = "raw_patient_record"
        self.save()
        with self.assertRaisesRegex(m.SealError, "SOURCE_CLASS_REQUIRED"):
            self.call()

    def test_private_skill_selection_gold_stays_out_of_stage1(self):
        for item, action in zip(self.gold["keys"], ("USE", "SKIP", "HOLD")):
            item["expected_skill_action"] = action
            item["skill_action_rationale"] = "Fictional private policy only"
        self.save()
        self.call()
        private = json.loads((self.key / "facilitator_key.json").read_text())
        self.assertTrue(private["skill_selection_gold_predeclared"])
        with ZipFile(self.st / "stage1.zip") as archive:
            tasks = b"".join(archive.read(n) for n in archive.namelist())
            self.assertNotIn(b"Fictional private policy only", tasks)
            self.assertNotIn(b"expected_skill_action", tasks)
        self.assertNotIn("expected_skill_action", (self.st / "manifest.json").read_text())

    def test_private_skill_selection_gold_must_cover_all(self):
        self.gold["keys"][0]["expected_skill_action"] = "USE"
        self.gold["keys"][0]["skill_action_rationale"] = "A fictional choice"
        self.save()
        with self.assertRaisesRegex(m.SealError, "PARTIAL_SKILL_ACTION_GOLD_FORBIDDEN"):
            self.call()
        self.assertFalse(self.st.exists())

    def test_private_skill_selection_gold_requires_negative_controls(self):
        for item in self.gold["keys"]:
            item["expected_skill_action"] = "USE"
            item["skill_action_rationale"] = "A fictional label"
        self.save()
        with self.assertRaisesRegex(m.SealError, "SKILL_ACTION_CONTROLS_REQUIRED"):
            self.call()
        self.assertFalse(self.st.exists())

    def test_invalid_skill_label_is_refused(self):
        for item, action in zip(self.gold["keys"], ("USE", "SKIP", "HOLD")):
            item["expected_skill_action"] = action
            item["skill_action_rationale"] = "A fictional label"
        self.gold["keys"][1]["expected_skill_action"] = "ALWAYS_USE"
        self.save()
        with self.assertRaisesRegex(m.SealError, "SKILL_ACTION_GOLD_INVALID"):
            self.call()
        self.assertFalse(self.st.exists())

    def test_cli_rejects_misleading_repo_root_before_writing(self):
        # Reproduces the reported full-CLI public-checkout bypass safely.
        public_output = P.parent.parent / "__case_examiner_must_not_create__"
        self.assertFalse(public_output.exists())
        args = [sys.executable, str(P), "--cases-file", str(self.case_file),
                "--gold-file", str(self.gold_file), "--stage1-root", str(public_output),
                "--key-root", str(self.key), "--cases-sha256",
                hashlib.sha256(self.case_file.read_bytes()).hexdigest(),
                "--gold-sha256", hashlib.sha256(self.gold_file.read_bytes()).hexdigest(),
                "--suite-id", "holdout-2026-01", "--repo-root", str(self.repo)]
        result = subprocess.run(args, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["error"], "REPO_ROOT_OVERRIDE_FORBIDDEN")
        self.assertFalse(public_output.exists())
        self.assertFalse(self.key.exists())

    def test_library_guard_rejects_real_checkout_even_with_fake_root(self):
        public_output = P.parent.parent / "__case_examiner_must_not_create__"
        self.assertFalse(public_output.exists())
        with self.assertRaisesRegex(m.SealError, "PUBLIC_REPO_PATH_FORBIDDEN"):
            self.call(repo_root=self.repo, stage1_root=public_output)
        self.assertFalse(public_output.exists())

    def test_rejects_symlinked_input_ancestor_into_public_repo(self):
        (self.repo / "cases.json").write_bytes(self.case_file.read_bytes())
        alias = self.root / "hidden_alias"
        alias.symlink_to(self.repo, target_is_directory=True)
        with self.assertRaisesRegex(m.SealError, "PUBLIC_REPO_INPUT_FORBIDDEN"):
            self.call(cases_file=alias / "cases.json")
        self.assertFalse(self.st.exists())
        self.assertFalse(self.key.exists())

    def test_rejects_symlinked_gold_ancestor_into_public_repo(self):
        (self.repo / "gold.json").write_bytes(self.gold_file.read_bytes())
        alias = self.root / "hidden_gold_alias"
        alias.symlink_to(self.repo, target_is_directory=True)
        with self.assertRaisesRegex(m.SealError, "PUBLIC_REPO_INPUT_FORBIDDEN"):
            self.call(gold_file=alias / "gold.json")
        self.assertFalse(self.st.exists())
        self.assertFalse(self.key.exists())

    def test_excludes_private_inputs_in_real_code_checkout(self):
        source = P.parent.parent / "AGENTS.md"
        if not source.exists():
            self.skipTest("no code-checkout sentinel in isolated runner")
        with self.assertRaisesRegex(m.SealError, "PUBLIC_REPO_INPUT_FORBIDDEN"):
            self.call(cases_file=source)
        self.assertFalse(self.st.exists())

    def test_refuse_paths_with_symlinked_ancestor(self):
        sym = self.root / "alias"
        sym.symlink_to(self.a, target_is_directory=True)
        with self.assertRaisesRegex(m.SealError, "SYMLINK_ANCESTOR_FORBIDDEN"):
            self.call(stage1_root=sym / "sealed")


if __name__ == "__main__":
    unittest.main()
