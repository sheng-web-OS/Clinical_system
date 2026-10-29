"""Synthetic-only tests for staged B/C worker input isolation; no model calls."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from prepare_staged_bc_packets import prepare, PacketError, sha

COMMIT = "a" * 40
SKILL = b"---\nname: decision-question-triage\n---\nExperimental candidate for unit test only."
CASES = {"H01.md": b"SYNTHETIC CASE ONE: no patient or private observations",
         "S01.md": b"SYNTHETIC CONTROL: ordinary explanation should not force research"}


class StagedPacketsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.input_zip = self.root / "stage1.zip"
        self.skill = self.root / "SKILL.md"
        self.skill.write_bytes(SKILL)
        self.manifest = self.root / "manifest.json"
        self.output = self.root / "output"
        self.make_fixture()

    def make_fixture(self, overrides=None):
        sources = dict(CASES)
        if overrides is not None:
            sources = overrides
        with ZipFile(self.input_zip, "w") as z:
            for name, content in sources.items():
                z.writestr(name, content)
        manifest_files = [{"path": "stage1/" + name,
                           "bytes": len(content), "sha256": sha(content)}
                          for name, content in CASES.items()]
        manifest_files += [
            {"path": "stage2/H01.md", "bytes": 123,
             "sha256": "f" * 64},
            {"path": "reviewer_only/rubric.md", "bytes": 456,
             "sha256": "e" * 64},
        ]
        obj = {"status": "PREPARED_NOT_RUN", "version": 2,
               "actual_model_calls": 0, "files": manifest_files}
        self.manifest.write_text(json.dumps(obj, sort_keys=True))
        self.digest = sha(self.manifest.read_bytes())

    def go(self, **kw):
        inputs = dict(stage1_zip=self.input_zip, manifest_path=self.manifest,
                      skill_path=self.skill, output_dir=self.output,
                      expected_manifest_sha256=self.digest,
                      expected_skill_sha256=sha(SKILL), candidate_commit=COMMIT,
                      repo_root=ROOT)
        inputs.update(kw)
        return prepare(**inputs)

    def assert_reject(self, msg, **kw):
        with self.assertRaisesRegex(PacketError, msg):
            self.go(**kw)
        self.assertFalse(self.output.exists())

    def test_four_worker_zip_inputs_avoid_stage2_and_reviewer_keys(self):
        result = self.go()
        self.assertEqual("PACKETS_PREPARED_NO_MODEL_RUN", result["status"])
        self.assertEqual(4, len(result["workers"]))
        self.assertEqual(0, result["provider_model_calls"])
        self.assertIsNone(result["actual_cost_usd"])
        self.assertFalse(result["clinical_transfer_validated"])
        self.assertEqual("NOT_VERIFIED", result["worker_context_isolation"])
        for cid in ("H01", "S01"):
            blobs = {}
            for arm in ("B", "C"):
                path = self.output / f"{cid}_{arm}_stage1.zip"
                with ZipFile(path) as z:
                    members = set(z.namelist())
                    self.assertEqual({"task.md", "instructions.txt"}
                                     | ({"candidate_skill.md"} if arm == "C" else set()),
                                     members)
                    blobs[arm] = (z.read("task.md"), z.read("instructions.txt"))
                    self.assertEqual(z.read("task.md"), CASES[cid + ".md"])
                    if arm == "C":
                        self.assertEqual(z.read("candidate_skill.md"), SKILL)
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(blobs["B"], blobs["C"])
        self.assertEqual((self.output / "facilitator_manifest.json").stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.output.stat().st_mode & 0o777, 0o700)

    def test_manifest_digest_mismatch_is_fail_closed(self):
        self.assert_reject("MANIFEST_HASH_MISMATCH",
                           expected_manifest_sha256="0" * 64)

    def test_stage1_byte_tamper_is_rejected(self):
        self.make_fixture({**CASES, "H01.md": b"SYNTHETIC CASE ALTERED not source text"})
        self.assert_reject("STAGE1_ENTRY_HASH_MISMATCH")

    def test_stage1_extra_member_cannot_leak_reviewer(self):
        self.make_fixture({**CASES, "reviewer_only/rubric.md": b"LEAKED PRIVATE ANSWER KEY"})
        self.assert_reject("STAGE1_ARCHIVE_MEMBERS_MISMATCH")

    def test_zip_path_traversal_rejected(self):
        self.make_fixture({"../H01.md": CASES["H01.md"], "S01.md": CASES["S01.md"]})
        self.assert_reject("STAGE1_ARCHIVE_ENTRY_REJECTED")

    def test_archive_duplicate_case_name_rejected(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with ZipFile(self.input_zip, "w") as z:
                z.writestr("H01.md", CASES["H01.md"])
                z.writestr("H01.md", CASES["H01.md"])
        self.assert_reject("STAGE1_ARCHIVE_ENTRY_REJECTED")

    def test_wrong_skill_bytes_rejected(self):
        self.skill.write_bytes(SKILL + b"\nUnreviewed changed instruction")
        self.assert_reject("SKILL_BYTES_NOT_PINNED")

    def test_control_cannot_be_silently_dropped_or_added(self):
        self.assert_reject("INVALID_CASE_SELECTION", cases=("H01", "H01"))
        self.assert_reject("CASE_NOT_FROZEN", cases=("H01", "D01"))

    def test_existing_output_cannot_be_overwritten(self):
        self.output.mkdir()
        with self.assertRaisesRegex(PacketError, "OUTPUT_EXISTS_REFUSE_OVERWRITE"):
            self.go()

    def test_public_repo_output_path_rejected(self):
        self.assert_reject("PRIVATE_PACKETS_MUST_STAY_OUTSIDE_PUBLIC_REPO",
                           repo_root=self.root)

    def test_no_authentication_or_model_claims_from_test_packets(self):
        result = self.go()
        self.assertNotIn("provider_response_id", json.dumps(result))
        self.assertEqual(result["independent_review"], "NOT_DONE")
        self.assertEqual(result["candidate_commit_claimed_not_git_verified"], COMMIT)


if __name__ == "__main__":
    unittest.main()
