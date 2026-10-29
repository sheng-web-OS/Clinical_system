"""Offline adversarial contract tests. No API key, GitHub network or model calls."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.dispatch_selector import DispatchError, load_manifest, select_tasks


class DispatcherShadowTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.manifest_path = Path(self.tmp.name) / "dispatch.json"
        self.base = json.loads(
            (Path(__file__).resolve().parents[1] / "ops/dispatch.json")
            .read_text(encoding="utf-8"))
        self.write(self.base)
        self.config = load_manifest(self.manifest_path)
        self.snapshot = {
            t["target"]: {"number": int(t["target"].split(":")[1]),
                          "state": "open", "is_pr": False}
            for t in self.config["tasks"]
        }

    def write(self, content):
        self.manifest_path.write_text(
            json.dumps(content, ensure_ascii=False), encoding="utf-8")

    def expect_invalid(self, config, reason):
        self.write(config)
        with self.assertRaisesRegex(DispatchError, reason):
            load_manifest(self.manifest_path)

    def test_open_queue_selects_p0_without_models_or_writes(self):
        result = select_tasks(self.config, self.snapshot)
        self.assertEqual("SHADOW_NO_ACTION", result["status"])
        self.assertEqual("ecg-original-evidence", result["selected"][0]["id"])
        self.assertEqual(0, result["model_calls"])
        self.assertEqual(0, result["write_actions"])
        self.assertFalse(result["execution_authorized"])

    def test_ranked_queue_has_fallback_when_first_task_has_active_owner(self):
        # Read-only selector MUST return more than the top open Issue: the
        # high-priority P0 can already have an active writer or a gated PR.
        result = select_tasks(self.config, self.snapshot)
        self.assertTrue(result["selection_requires_live_gate_check"])
        self.assertFalse(result["execution_authorized"])
        self.assertEqual(len(self.config["tasks"]), len(result["candidates"]))
        self.assertEqual("ecg-original-evidence", result["candidates"][0]["id"])
        self.assertEqual("mobile-figure-p0", result["candidates"][1]["id"])
        self.assertEqual("issue:79", result["candidates"][1]["target"])

    def test_only_open_issues_become_candidates(self):
        self.snapshot["issue:76"]["state"] = "closed"
        self.snapshot["issue:79"]["state"] = "closed"
        result = select_tasks(self.config, self.snapshot)
        self.assertEqual("public-narrative-audit", result["candidates"][0]["id"])
        self.assertFalse(any(c["target"] in {"issue:76", "issue:79"}
                             for c in result["candidates"]))

    def test_closed_task_advances_to_other_open_issue(self):
        self.snapshot["issue:76"]["state"] = "closed"
        result = select_tasks(self.config, self.snapshot)
        self.assertEqual("mobile-figure-p0", result["selected"][0]["id"])
        self.assertIn({"id": "ecg-original-evidence", "reason": "CLOSED"},
                      result["skipped"])

    def test_missing_live_metadata_fails_closed_not_fake_empty(self):
        del self.snapshot["issue:76"]
        with self.assertRaisesRegex(DispatchError,
                                    "SOURCE_METADATA_MISSING_OR_INVALID"):
            select_tasks(self.config, self.snapshot)

    def test_pr_metadata_cannot_impersonate_issue(self):
        self.snapshot["issue:76"]["is_pr"] = True
        with self.assertRaisesRegex(DispatchError, "EXPECTED_ISSUE_GOT_PR"):
            select_tasks(self.config, self.snapshot)

    def test_do_not_touch_registered_72h_experiment(self):
        cfg = copy.deepcopy(self.base)
        cfg["tasks"][0]["target"] = "issue:137"
        self.expect_invalid(cfg, "DISALLOWED_OR_DUPLICATE_TARGET")
        cfg = copy.deepcopy(self.base)
        cfg["frozen_eval"]["until_utc"] = "2026-10-30T00:00:00Z"
        self.expect_invalid(cfg, "PREREGISTERED_WINDOW_MUST_NOT_CHANGE")
        cfg = copy.deepcopy(self.base)
        cfg["frozen_eval"]["excluded_targets"].remove("pr:225")
        self.expect_invalid(cfg, "PROTECTED_EXPERIMENT_SCOPE")

    def test_no_execution_upgrade_or_expanded_batch(self):
        cfg = copy.deepcopy(self.base)
        cfg["mode"] = "execute"
        self.expect_invalid(cfg, "SHADOW_ONLY_ONE_TASK_PER_TICK")
        cfg = copy.deepcopy(self.base)
        cfg["max_tasks_per_run"] = 30
        self.expect_invalid(cfg, "SHADOW_ONLY_ONE_TASK_PER_TICK")

    def test_no_arbitrary_prompt_action_or_credential_field(self):
        cfg = copy.deepcopy(self.base)
        cfg["tasks"][0]["action"] = "run arbitrary shell"
        self.expect_invalid(cfg, "INVALID_TASK_SCHEMA")
        cfg = copy.deepcopy(self.base)
        cfg["tasks"][0]["kind"] = "execute_script"
        self.expect_invalid(cfg, "INVALID_TASK_POLICY")

    def test_no_duplicate_jobs_or_priority_type_coercion(self):
        cfg = copy.deepcopy(self.base)
        cfg["tasks"][1]["id"] = cfg["tasks"][0]["id"]
        self.expect_invalid(cfg, "INVALID_OR_DUPLICATE_TASK_ID")
        cfg = copy.deepcopy(self.base)
        cfg["tasks"][0]["priority"] = True
        self.expect_invalid(cfg, "INVALID_TASK_POLICY")

    def test_bad_json_types_fail_closed(self):
        cfg = copy.deepcopy(self.base)
        cfg["schema_version"] = True
        self.expect_invalid(cfg, "INVALID_REPOSITORY_OR_VERSION")
        cfg = copy.deepcopy(self.base)
        cfg["max_tasks_per_run"] = True
        self.expect_invalid(cfg, "SHADOW_ONLY_ONE_TASK_PER_TICK")
        cfg = copy.deepcopy(self.base)
        cfg["frozen_eval"]["excluded_targets"].append({"invalid": 1})
        self.expect_invalid(cfg, "PROTECTED_EXPERIMENT_SCOPE")
        cfg = copy.deepcopy(self.base)
        cfg["tasks"][0]["kind"] = ["quality_review"]
        self.expect_invalid(cfg, "INVALID_TASK_POLICY")

    def test_disabled_tasks_are_not_scheduled(self):
        cfg = copy.deepcopy(self.config)
        cfg["tasks"][0]["enabled"] = False
        result = select_tasks(cfg, self.snapshot)
        self.assertEqual("mobile-figure-p0", result["selected"][0]["id"])

    def test_closed_all_returns_empty_without_claiming_completion(self):
        for item in self.snapshot.values():
            item["state"] = "closed"
        result = select_tasks(self.config, self.snapshot)
        self.assertEqual([], result["selected"])
        self.assertEqual("SHADOW_NO_ACTION", result["status"])


if __name__ == "__main__":
    unittest.main()
