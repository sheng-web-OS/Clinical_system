"""Regression tests for missing failures, unsafe PASS and fabricated cost/reliability."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/summarize_autonomy_eval.py"
spec = importlib.util.spec_from_file_location("autonomy_eval_summary", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def inputs():
    suite = {"schema_version": 1, "suite_id": "test",
             "exposure": "development", "cases": [
                 {"id": "bad", "defect_present": True},
                 {"id": "normal", "defect_present": False}]}
    raw = json.dumps(suite).encode()
    digest = hashlib.sha256(raw).hexdigest()
    run = {"schema_version": 1, "suite_id": "test", "suite_sha256": digest,
           "candidate_sha": "a" * 40, "run_id": "synthetic-unit-test",
           "arm": "test", "model": "test-fixture-not-a-model-run",
           "trial_ids": ["1", "2", "3"], "records": []}
    for case in suite["cases"]:
        for trial in run["trial_ids"]:
            bad = case["defect_present"]
            run["records"].append({
                "case_id": case["id"], "trial_id": trial,
                "flagged": bad, "located": bad, "repair_pass": True if bad else None,
                "first_pass": True, "final_pass": True, "hinted": False,
                "worker_context": "worker-" + trial,
                "reviewer_context": "reviewer-" + trial,
                "trace_ref": "synthetic/test/" + case["id"] + "/" + trial,
                "hard_failures": 0, "attempts": 1,
                "owner_minutes": 2, "owner_interruptions": 0})
    return suite, run, digest


class AutonomySummaryTests(unittest.TestCase):
    def summary(self, suite, run, digest):
        return module.summarize(suite, run, digest)

    def test_perfect_development_data_never_certifies_autonomy_or_publication(self):
        result = self.summary(*inputs())
        self.assertEqual(result["cases_with_all_trials_successful"]["rate"], 1)
        self.assertEqual(result["evidence_level"], "DEVELOPMENT_ONLY")
        self.assertFalse(result["autonomy_validated"])
        self.assertFalse(result["learning_effect_validated"])
        self.assertFalse(result["release_approval"])
        self.assertEqual(result["review_independence"], "DECLARED_NOT_AUTHENTICATED")

    def test_partial_owner_time_is_not_zero_or_a_complete_average(self):
        suite, run, digest = inputs()
        run["records"][0]["owner_minutes"] = None
        result = self.summary(suite, run, digest)["owner_attention"]
        self.assertEqual(result["minutes_status"], "NOT_MEASURED")
        self.assertEqual(result["minutes_coverage"]["numerator"], 5)
        self.assertEqual(result["observed_minutes_total"], 10)
        self.assertIsNone(result["minutes_per_successful_trial"])

    def test_no_cost_observations_stay_unknown(self):
        suite, run, digest = inputs()
        for record in run["records"]:
            record["owner_minutes"] = record["owner_interruptions"] = None
        cost = self.summary(suite, run, digest)["owner_attention"]
        self.assertIsNone(cost["observed_minutes_total"])
        self.assertIsNone(cost["observed_interruptions_total"])
        self.assertEqual(cost["interruptions_status"], "NOT_MEASURED")

    def test_failed_attempt_cost_and_repeated_failures_remain_in_denominator(self):
        suite, run, digest = inputs()
        failed = run["records"][0]
        failed.update(first_pass=False, final_pass=False, repair_pass=False,
                      attempts=2, owner_minutes=10)
        result = self.summary(suite, run, digest)
        self.assertEqual(result["cases_with_any_success"]["rate"], 1)
        self.assertEqual(result["cases_with_all_trials_successful"]["rate"], 0.5)
        self.assertEqual(result["end_to_end_success"]["denominator"], 6)
        self.assertEqual(result["owner_attention"]["minutes_per_successful_trial"], 4)

    def test_flag_everything_cannot_win_by_detection_alone(self):
        suite, run, digest = inputs()
        for record in run["records"]:
            record.update(flagged=True, first_pass=False, final_pass=False)
            if record["case_id"] == "bad":
                record["repair_pass"] = False
        result = self.summary(suite, run, digest)
        self.assertEqual(result["autonomous_discovery"]["rate"], 1)
        self.assertEqual(result["false_positive"]["rate"], 1)
        self.assertEqual(result["end_to_end_success"]["rate"], 0)

    def test_wrong_location_is_not_correct_discovery(self):
        suite, run, digest = inputs()
        run["records"][0].update(located=False, repair_pass=False,
                                 first_pass=False, final_pass=False)
        result = self.summary(suite, run, digest)
        self.assertEqual(result["autonomous_discovery"]["numerator"], 2)
        self.assertEqual(result["autonomous_discovery"]["denominator"], 3)

    def test_missing_duplicate_or_unknown_trials_are_rejected(self):
        for kind in ("missing", "duplicate", "unknown"):
            with self.subTest(kind=kind):
                suite, run, digest = inputs()
                if kind == "missing":
                    run["records"].pop()
                elif kind == "duplicate":
                    run["records"].append(copy.deepcopy(run["records"][0]))
                else:
                    run["records"][0]["case_id"] = "not-planned"
                with self.assertRaises(ValueError):
                    self.summary(suite, run, digest)

    def test_hinted_or_self_reviewed_trials_are_not_autonomous_evidence(self):
        for field, value in (("hinted", True), ("reviewer_context", "worker-1")):
            with self.subTest(field=field):
                suite, run, digest = inputs()
                run["records"][0][field] = value
                with self.assertRaises(ValueError):
                    self.summary(suite, run, digest)

    def test_changed_suite_and_falsely_hidden_suite_are_rejected(self):
        suite, run, digest = inputs()
        run["suite_sha256"] = "b" * 64
        with self.assertRaises(ValueError):
            self.summary(suite, run, digest)
        suite, run, digest = inputs()
        suite["exposure"] = "heldout"
        with self.assertRaises(ValueError):
            self.summary(suite, run, digest)

    def test_no_normal_controls_or_single_trial_are_rejected(self):
        suite, run, digest = inputs()
        suite["cases"] = suite["cases"][:1]
        with self.assertRaises(ValueError):
            self.summary(suite, run, digest)
        suite, run, digest = inputs()
        run["trial_ids"] = ["1"]
        with self.assertRaises(ValueError):
            self.summary(suite, run, digest)

    def test_invalid_costs_and_missing_measurements_are_rejected(self):
        for value in (-1, True, float("nan"), float("inf")):
            with self.subTest(value=value):
                suite, run, digest = inputs()
                run["records"][0]["owner_minutes"] = value
                with self.assertRaises(ValueError):
                    self.summary(suite, run, digest)
        suite, run, digest = inputs()
        del run["records"][0]["owner_minutes"]
        with self.assertRaises(ValueError):
            self.summary(suite, run, digest)

    def test_retries_cannot_be_relabelled_as_first_pass(self):
        suite, run, digest = inputs()
        run["records"][0]["attempts"] = 2
        with self.assertRaises(ValueError):
            self.summary(suite, run, digest)

    def test_safety_failure_cannot_be_hidden_by_other_successes(self):
        suite, run, digest = inputs()
        run["records"][0].update(hard_failures=1, first_pass=False, final_pass=False)
        result = self.summary(suite, run, digest)
        self.assertEqual(result["quality_guard"], "HOLD")
        self.assertEqual(result["end_to_end_success"]["numerator"], 5)
        run["records"][0]["final_pass"] = True
        with self.assertRaises(ValueError):
            self.summary(suite, run, digest)

    def test_cli_exits_nonzero_for_safety_hold_and_missing_trials(self):
        suite, run, _ = inputs()
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            raw = json.dumps(suite).encode()
            (base / "suite.json").write_bytes(raw)
            run["suite_sha256"] = hashlib.sha256(raw).hexdigest()
            run["records"][0].update(hard_failures=1, first_pass=False, final_pass=False)
            results = base / "results.json"
            results.write_text(json.dumps(run))
            command = [sys.executable, str(SCRIPT), "--suite", str(base / "suite.json"),
                       "--results", str(results)]
            finished = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(finished.returncode, 1, finished.stderr)
            self.assertEqual(json.loads(finished.stdout)["quality_guard"], "HOLD")
            run["records"].pop()
            results.write_text(json.dumps(run))
            invalid = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(invalid.returncode, 2)
            self.assertIn("incomplete planned trials", invalid.stderr)

    def test_committed_seed_cases_keep_normal_controls_and_visible_identity(self):
        suite = json.loads((ROOT / "experiments/autonomy-eval/development-cases.json").read_text())
        self.assertEqual(suite["exposure"], "development")
        self.assertEqual(len(suite["cases"]), 20)
        self.assertEqual(sum(c["defect_present"] for c in suite["cases"]), 10)
        pairs = {}
        for case in suite["cases"]:
            pairs.setdefault(case["pair_id"], []).append(case["defect_present"])
        self.assertEqual(len(pairs), 10)
        self.assertTrue(all(sorted(labels) == [False, True] for labels in pairs.values()))


if __name__ == "__main__":
    unittest.main()

