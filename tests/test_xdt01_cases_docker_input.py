"""Cases-only -> nine original-format jobs; synthetic, no Docker/API required."""
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import XDT01_docker_executor as controller
import prepare_xdt01_rich_pilot as rich
try:
    from tests.test_prepare_xdt01_cases_only import synthetic_cases
except ModuleNotFoundError:
    from test_prepare_xdt01_cases_only import synthetic_cases


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class CasesDockerInputTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.repo = self.root / "public-repo"
        skill = self.repo / "experiments/cross-domain-transfer/decision-skill-v0.md"
        skill.parent.mkdir(parents=True)
        skill.write_bytes(b"synthetic skill byte pin")
        self.cases = synthetic_cases()
        self.source = self.root / "cases.json"
        raw = json.dumps(self.cases, ensure_ascii=False).encode()
        self.source.write_bytes(raw)
        self.stage = self.root / "stage"
        rich.stage_cases_only(cases_file=self.source, cases_sha256=sha(raw),
                             repo_root=self.repo, stage_root=self.stage,
                             candidate_commit=controller.FROZEN_HEAD,
                             skill_sha256=sha(skill.read_bytes()))
        self.manifest = self.stage / "stage_manifest.json"

    def load(self, pin=None):
        return controller.staged_data(self.stage, pin or sha(self.manifest.read_bytes()), self.repo)

    def edit_manifest(self, edit):
        value = json.loads(self.manifest.read_bytes())
        edit(value)
        self.manifest.write_text(json.dumps(value))

    def test_three_full_packets_become_nine_single_case_arm_packets(self):
        # These files must not be sought or opened, even when present alongside cases.
        gold = self.root / "gold.json"
        rubric = self.root / "scoring.private.json"
        gold.write_text("SYNTHETIC_FORBIDDEN_GOLD_CANARY")
        rubric.write_text("SYNTHETIC_FORBIDDEN_RUBRIC_CANARY")
        original_open = Path.open
        def safe_open(path, *args, **kwargs):
            self.assertNotIn(path, {self.source, gold, rubric})
            return original_open(path, *args, **kwargs)
        with patch.object(Path, "open", safe_open):
            jobs, source_pin = self.load()
        self.assertEqual(len(jobs), 9)
        self.assertEqual(source_pin["cases_sha256"], sha(self.source.read_bytes()))
        originals = {row["id"]: row for row in self.cases["cases"]}
        seen = {}
        for job, raw in jobs:
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                self.assertEqual(sorted(archive.namelist()), ["job.json", "task.txt"])
                self.assertEqual(json.loads(archive.read("job.json")), job)
                task = archive.read("task.txt")
            obj = json.loads(task)
            self.assertEqual(obj["case"], originals[obj["case"]["id"]])
            self.assertEqual(obj["instructions"], self.cases["instructions"])
            self.assertEqual(sha(task), job["task_sha256"])
            self.assertEqual(set(job), {"job_id", "arm", "task_sha256", "candidate_commit", "skill_sha256"})
            self.assertEqual(job["skill_sha256"] is None, job["arm"] in {"A", "B"})
            seen.setdefault(job["task_sha256"], []).append(job["arm"])
        self.assertEqual(len(seen), 3)
        self.assertTrue(all(sorted(arms) == ["A", "B", "C"] for arms in seen.values()))

    def test_tampered_evidence_bytes_rejected_against_pinned_stage(self):
        task = self.stage / "H01.txt"
        obj = json.loads(task.read_bytes())
        obj["case"]["evidence"].pop()
        task.write_text(json.dumps(obj))
        with self.assertRaisesRegex(controller.Hold, "SHA_OR_SIZE_MISMATCH"):
            self.load()

    def test_manifest_digest_malformed_schema_and_traversal_are_rejected(self):
        with self.assertRaisesRegex(controller.Hold, "DIGEST_MISMATCH"):
            self.load("0" * 64)
        original = self.manifest.read_bytes()
        for edit in (lambda v: v.update(gold_file="must-not-open"),
                     lambda v: v["cases"][0].update(slot="../cases"),
                     lambda v: v.update(model_calls=True),
                     lambda v: v["cases"].pop()):
            self.manifest.write_bytes(original)
            self.edit_manifest(edit)
            with self.assertRaises(controller.Hold):
                self.load()

    def test_evidence_count_mismatch_and_skill_byte_change_fail_closed(self):
        original = self.manifest.read_bytes()
        self.edit_manifest(lambda v: v["cases"][0].update(evidence_count=1))
        with self.assertRaisesRegex(controller.Hold, "EVIDENCE_COUNT_MISMATCH"):
            self.load()
        self.manifest.write_bytes(original)
        (self.repo / "experiments/cross-domain-transfer/decision-skill-v0.md").write_text("changed")
        with self.assertRaisesRegex(controller.Hold, "FROZEN_SKILL_SHA_MISMATCH"):
            self.load()

    def test_cases_only_cannot_authorize_live_or_read_credentials(self):
        with patch.object(controller.shutil, "which", return_value="docker"), \
             patch.object(controller, "repo_verified", return_value=self.repo), \
             patch.object(controller.os, "getenv", side_effect=AssertionError("NO_CREDENTIAL_READ")), \
             patch.object(controller, "staged_data") as loader:
            with self.assertRaisesRegex(controller.Hold, "CASES_ONLY_OFFLINE_ONLY"):
                controller.launch(None, self.repo, self.root / "new-workspace", True,
                                  cases_stage=self.stage, stage_manifest_sha256="a" * 64)
            loader.assert_not_called()

    def test_stage_reshuffle_and_new_job_ids_do_not_reset_claim(self):
        jobs, source_pin = self.load()
        state = self.root / "operator-state"
        experiment, grants = controller.claim_experiment(jobs, None, state, source_pin=source_pin)
        again, same_source = self.load()
        self.assertEqual(controller.experiment_identity(jobs), controller.experiment_identity(again))
        self.assertEqual(len(grants), 9)
        claim = json.loads((experiment / "claim.json").read_bytes())
        self.assertEqual(claim["source_pin"], source_pin)
        self.assertEqual(claim["reserved_calls"], 12)
        with self.assertRaisesRegex(controller.Hold, "ALREADY_CLAIMED"):
            controller.claim_experiment(again, None, state, source_pin=same_source)


if __name__ == "__main__":
    unittest.main()
