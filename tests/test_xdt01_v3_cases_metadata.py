"""Synthetic-only v3 provenance compatibility; no live or rubric access."""
import hashlib
import importlib.util
import json
import pathlib
import tempfile
import unittest

from tests.test_prepare_xdt01_cases_only import synthetic_cases

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "tools/prepare_xdt01_rich_pilot.py"
spec = importlib.util.spec_from_file_location("v3_metadata_preparer", SCRIPT)
rich = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rich)


def v3_cases():
    cases = synthetic_cases()
    cases.update({"phase": "internal_exploratory",
                  "artifact_version": "synthetic-v3-metadata",
                  "exposure_status": "SYNTHETIC_EXPOSURE_MARKER",
                  "formal_freeze_at_creation": "NOT_FROZEN_AT_CREATION",
                  "human_review_at_creation": "NO_HUMAN_REVIEW_AT_CREATION",
                  "study_classification": "INTERNAL_EXPLORATORY"})
    return cases


class V3CasesMetadataTests(unittest.TestCase):
    def test_cases_only_stages_v3_but_does_not_forward_provenance_labels(self):
        cases = v3_cases()
        raw = (json.dumps(cases, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary).resolve()
            repo = root / "public-repo"
            repo.mkdir()
            source = root / "cases.json"
            source.write_bytes(raw)
            stage = root / "private-stage"
            receipt = rich.stage_cases_only(
                cases_file=source, cases_sha256=hashlib.sha256(raw).hexdigest(),
                repo_root=repo, stage_root=stage,
                candidate_commit=rich.FROZEN_CANDIDATE, skill_sha256="a" * 64)
            self.assertEqual(receipt["status"], "OFFLINE_CASES_ONLY_REVIEW_HOLD")
            self.assertEqual(receipt["model_calls"], 0)
            self.assertFalse(receipt["independent_access_denial_verified"])
            self.assertEqual({path.name for path in stage.iterdir()},
                             {"H01.txt", "H02.txt", "H03.txt", "stage_manifest.json"})
            manifest = json.loads((stage / "stage_manifest.json").read_bytes())
            self.assertEqual(manifest["source_sha256"],
                             {"cases": hashlib.sha256(raw).hexdigest()})
            self.assertEqual(manifest["phase"], "pilot")
            expected = rich.validate_cases(synthetic_cases())
            originals = {case["id"]: case for case in cases["cases"]}
            for row in manifest["cases"]:
                task_bytes = (stage / (row["slot"] + ".txt")).read_bytes()
                packet = json.loads(task_bytes)
                self.assertEqual(set(packet), {"package_id", "instructions", "case"})
                self.assertEqual(packet["case"], originals[packet["case"]["id"]])
                self.assertEqual(task_bytes, expected[packet["case"]["id"]])
                self.assertEqual(row["sha256"], hashlib.sha256(task_bytes).hexdigest())
                self.assertEqual(row["evidence_count"], len(packet["case"]["evidence"]))
                for field in rich.CASES_ONLY_V3_METADATA:
                    self.assertNotIn(field, packet)
                    self.assertNotIn(cases[field].encode("utf-8"), task_bytes)

    def test_package_id_change_is_preserved_and_changes_model_facing_bytes(self):
        original = rich.validate_cases(synthetic_cases())
        cases = v3_cases()
        cases["package_id"] = "xdt-cases-only-fixture-v3"
        changed = rich.validate_cases(cases, cases_only=True)
        for cid, task_bytes in changed.items():
            self.assertNotEqual(task_bytes, original[cid])
            packet = json.loads(task_bytes)
            self.assertEqual(packet["package_id"], cases["package_id"])
            self.assertEqual(packet["instructions"], cases["instructions"])

    def test_partial_extra_wrong_phase_or_classification_metadata_is_rejected(self):
        bad_cases = []
        for field in rich.CASES_ONLY_V3_METADATA:
            value = v3_cases()
            del value[field]
            bad_cases.append(value)
        value = v3_cases()
        value["extra_provenance"] = "unexpected"
        bad_cases.append(value)
        for phase in ("pilot", "exploratory", ""):
            value = v3_cases()
            value["phase"] = phase
            bad_cases.append(value)
        for classification in ("LIVE_AUTHORIZED", "VALIDATED", "internal_exploratory"):
            value = v3_cases()
            value["study_classification"] = classification
            bad_cases.append(value)
        for index, cases in enumerate(bad_cases):
            with self.subTest(index=index), self.assertRaises(rich.Hold):
                rich.validate_cases(cases, cases_only=True)
        for field in rich.CASES_ONLY_V3_METADATA:
            for invalid in (None, False, 1, [], {}, "", " \t\n", "\ud800", "x" * 257):
                value = v3_cases()
                value[field] = invalid
                with self.subTest(field=field, invalid=repr(invalid)):
                    with self.assertRaises(rich.Hold):
                        rich.validate_cases(value, cases_only=True)

    def test_full_facilitator_validation_remains_strict_v2(self):
        cases = v3_cases()
        with self.assertRaisesRegex(rich.Hold, "CASES_SCHEMA"):
            rich.validate_cases(cases)
        # Rejected before any gold or scoring validation; no private files exist.
        with self.assertRaisesRegex(rich.Hold, "CASES_SCHEMA"):
            rich.validate(cases, None, None)

    def test_original_schema_stays_strict_in_both_modes(self):
        cases = synthetic_cases()
        self.assertEqual(rich.validate_cases(cases),
                         rich.validate_cases(cases, cases_only=True))
        cases["phase"] = "internal_exploratory"
        for cases_only in (False, True):
            with self.subTest(cases_only=cases_only), self.assertRaises(rich.Hold):
                rich.validate_cases(cases, cases_only=cases_only)


if __name__ == "__main__":
    unittest.main()
