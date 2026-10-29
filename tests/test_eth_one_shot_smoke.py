"""Fail-closed one-shot API workflow contract; never invokes paid inference."""
import importlib.util
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from falsification_probe import InvalidProbe
spec = importlib.util.spec_from_file_location("eth_one_shot", ROOT / "tools/run_eth_synthetic_smoke.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

GOOD = {
    "GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "workflow_dispatch",
    "GITHUB_REF": "refs/heads/main",
    "GITHUB_REPOSITORY": "sheng-web-OS/Clinical_system",
    "OPENAI_MODEL": "gpt-5-mini", "OPENAI_API_KEY": "fake-test-only",
}

class OneShotTests(unittest.TestCase):
    def test_public_fixture_and_eight_call_ceiling(self):
        plan = mod.plan()
        self.assertEqual(plan["packets_per_arm"], 4)
        self.assertEqual(plan["max_api_calls"], 8)
        self.assertEqual(plan["mode"], "SYNTHETIC_ONLY_NOT_BLIND")

    def test_only_manual_trusted_main_with_key(self):
        mod.authorize(GOOD)
        for name, replacement in (
            ("GITHUB_EVENT_NAME", "pull_request"),
            ("GITHUB_EVENT_NAME", "schedule"),
            ("GITHUB_REF", "refs/heads/experiment"),
            ("GITHUB_REPOSITORY", "someone-else/project"),
            ("GITHUB_ACTIONS", "false"),
            ("OPENAI_MODEL", "another-model"),
            ("OPENAI_API_KEY", ""),
            ("PROBE_APPROVED_EXTERNAL_DATA", "true"),
        ):
            with self.subTest(name=name, replacement=replacement):
                with self.assertRaises(mod.SmokeHold):
                    mod.authorize({**GOOD, name: replacement})

    def test_no_model_run_if_not_authorized(self):
        with patch.object(mod, "run_adapter", side_effect=AssertionError("paid inference started")):
            with self.assertRaises(mod.SmokeHold):
                mod.execute({**GOOD, "GITHUB_REF": "refs/heads/PR"})

    def test_one_shot_workflow_only_manual_and_read_only(self):
        flow = (ROOT / ".github/workflows/eth-probe-one-shot.yml").read_text()
        self.assertIn("workflow_dispatch:", flow)
        self.assertNotIn("  schedule:", flow)
        self.assertNotIn("  push:", flow)
        self.assertNotIn("  pull_request:", flow)
        self.assertIn("contents: read", flow)
        self.assertIn("github.ref == 'refs/heads/main'", flow)
        self.assertIn("vars.CLINICAL_OS_AGENT_ENABLED == 'true'", flow)
        self.assertIn("inputs.confirm == 'SYNTHETIC_ONLY'", flow)
        self.assertNotIn("id-token: write", flow)
        self.assertNotIn("upload-artifact", flow)
        self.assertNotIn("pull-requests: write", flow)

    def test_deterministic_full_dry_run_two_arms_without_api(self):
        """Exercises real prepare/run/score plumbing, not model ability."""
        import json
        from falsification_probe import run_adapter as actual_runner

        toy = ROOT / "experiments/eth-falsification-probe/claim_update_toy_adapter.py"
        seen = []

        def fake_adapter_run(reviewer, response, adapter, timeout, allowed_env, relabel):
            self.assertEqual(adapter, mod.ADAPTER)
            self.assertFalse(relabel)
            self.assertEqual(set(allowed_env),
                             {"OPENAI_API_KEY", "OPENAI_MODEL", "PROBE_VARIANT"})
            seen.append(os.environ.get("PROBE_VARIANT"))
            result = actual_runner(reviewer, response, toy, timeout=timeout)
            content = json.loads(response.read_text())
            content["provider_usage"] = {row["probe_id"]: {"total_tokens": 8}
                                         for row in content["responses"]}
            response.write_text(json.dumps(content))
            return result

        with patch.dict(os.environ, GOOD, clear=True):
            with patch.object(mod, "run_adapter", side_effect=fake_adapter_run):
                result = mod.execute()
        self.assertEqual(seen, ["native", "clinical_lite"])
        self.assertEqual(result["status"], "SYNTHETIC_API_SMOKE_ONLY")
        self.assertEqual(result["results"]["native"]["total_packets"], 4)
        self.assertEqual(result["results"]["native"]["reported_tokens"], 32)
        self.assertEqual(result["results"]["clinical_lite"]["reported_tokens"], 32)
        self.assertNotIn("responses", json.dumps(result))
        self.assertNotIn("OPENAI_API_KEY", json.dumps(result))

    def test_dry_run_never_reads_key(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(mod.plan()["max_api_calls"], 8)

if __name__ == "__main__":
    unittest.main()
