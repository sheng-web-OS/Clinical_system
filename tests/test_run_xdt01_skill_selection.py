"""Regression probes for the XDT-01 actual Skill-selection execution path.

These use injected test doubles only. Passing them is NOT a model result.
"""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import run_xdt01_skill_selection as x


def provider(text, i):
    return {
        "id": "resp_test_" + str(i), "model": x.MODEL, "status": "completed",
        "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
        "output": [{"type": "message", "content": [
            {"type": "output_text", "text": text}]}],
    }


class SelectionRunnerTests(unittest.TestCase):
    def test_use_is_conditional_and_first_request_has_no_skill(self):
        calls = []
        skill = "SECRET_SKILL_BYTES_NOT_IN_INVENTORY"
        loader_count = []

        def model(req):
            calls.append(req)
            return provider("USE" if len(calls) == 1 else "correct choice",
                            len(calls))

        def load():
            loader_count.append(1)
            return skill

        value = x.run_arm("public test packet", "C", load, model)
        self.assertEqual(value["selection"], "USE")
        self.assertTrue(value["skill_loaded"])
        self.assertEqual(value["first_pass"], "correct choice")
        self.assertEqual(value["provider_calls"], 2)
        self.assertEqual(value["usage"]["total_tokens"], 30)
        self.assertEqual(len(loader_count), 1)
        self.assertNotIn(skill, json.dumps(calls[0]))
        self.assertIn(x.INVENTORY, calls[0]["instructions"])
        self.assertIn(skill, calls[1]["instructions"])
        self.assertEqual(calls[0]["input"], calls[1]["input"])
        self.assertEqual(calls[0]["model"], calls[1]["model"])

    def test_skip_does_not_read_full_skill(self):
        calls = []

        def model(req):
            calls.append(req)
            return provider("SKIP" if len(calls) == 1 else "no special technique",
                            len(calls))

        def forbidden_loader():
            self.fail("SKIP must not read Skill bytes")

        value = x.run_arm("simple fact task", "C", forbidden_loader, model)
        self.assertEqual(value["selection"], "SKIP")
        self.assertFalse(value["skill_loaded"])
        self.assertEqual(value["provider_calls"], 2)
        self.assertNotIn(x.SKILL_PREFIX, calls[1]["instructions"])

    def test_a_and_b_have_no_inventory_and_only_one_call(self):
        for arm in ("A", "B"):
            calls = []
            def model(req):
                calls.append(req)
                return provider("a decision", 1)
            outcome = x.run_arm("same task", arm, caller=model)
            self.assertIsNone(outcome["selection"])
            self.assertEqual(outcome["provider_calls"], 1)
            self.assertNotIn(x.INVENTORY, calls[0]["instructions"])
            self.assertNotIn(x.SKILL_PREFIX, calls[0]["instructions"])
            self.assertEqual(x.EVIDENCE in calls[0]["instructions"], arm == "B")

    def test_selection_receipt_precedes_answer_and_survives_answer_failure(self):
        received = []
        requests = []

        def model(req):
            requests.append(req)
            if len(requests) == 1:
                return provider("USE", 1)
            raise x.TrialError("SYNTHETIC_SECOND_CALL_FAILED")

        with self.assertRaisesRegex(x.TrialError, "SYNTHETIC_SECOND_CALL_FAILED"):
            x.run_arm("task", "C", lambda: "skill", model,
                      on_event=received.append)
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]["kind"], "selection")
        self.assertEqual(received[0]["text"], "USE")
        self.assertEqual(received[0]["usage"]["total_tokens"], 15)

    def test_invalid_selection_fails_without_answer_call(self):
        calls = []
        def model(req):
            calls.append(req)
            return provider("I would probably use it", len(calls))
        with self.assertRaisesRegex(x.TrialError, "INVALID_SELECTION_FIRST_PASS"):
            x.run_arm("task", "C", lambda: "skill", model)
        self.assertEqual(len(calls), 1)

    def test_reused_provider_id_rejected(self):
        def model(req):
            return provider("USE", 1)
        with self.assertRaisesRegex(x.TrialError, "REUSED_PROVIDER_RESPONSE"):
            x.run_arm("task", "C", lambda: "skill", model)

    def test_missing_loader_or_invalid_arm(self):
        with self.assertRaisesRegex(x.TrialError, "C_REQUIRES"):
            x.run_arm("task", "C", None, lambda r: provider("SKIP", 1))
        with self.assertRaisesRegex(x.TrialError, "INVALID_ARM"):
            x.run_arm("task", "Z", None, lambda r: provider("a", 1))

    def test_invalid_usage_or_model_is_rejected(self):
        for problem in ("usage", "model"):
            value = provider("answer", 1)
            if problem == "usage":
                value["usage"]["total_tokens"] = 300
            else:
                value["model"] = "different-model"
            with self.assertRaises(x.TrialError):
                x.parse_provider_response(value)

    def test_task_must_be_outside_public_repository(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            task = root / "case.txt"
            task.write_text("visible", encoding="utf-8")
            with self.assertRaisesRegex(x.TrialError, "INSIDE_PUBLIC_REPO"):
                x.private_read(task, 200, root, "CASE")

    def test_skill_must_be_hashed_public_code(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            path = root / "skill.md"
            path.write_text("frozen", encoding="utf-8")
            correct = hashlib.sha256(b"frozen").hexdigest()
            self.assertEqual(x.get_skill(path, correct, root), "frozen")
            with self.assertRaisesRegex(x.TrialError, "SKILL_BYTES_CHANGED"):
                x.get_skill(path, "0" * 64, root)

    def test_one_case_plan_creates_no_fake_first_pass(self):
        with tempfile.TemporaryDirectory() as d:
            parent = Path(d)
            packet = parent / "case.txt"
            packet.write_text("Private test task; no model call.", encoding="utf-8")
            output = parent / "plan"
            digest = hashlib.sha256(packet.read_bytes()).hexdigest()
            args = [
                "--arm", "A", "--task-file", str(packet),
                "--task-sha256", digest,
                "--candidate-commit", "a" * 40,
                "--output-dir", str(output),
            ]
            with patch.object(x, "verify_commit") as check:
                self.assertEqual(x.main(args), 0)
            check.assert_called_once()
            state = json.loads((output / "status.json").read_text())
            self.assertEqual(state["status"], "NOT_RUN")
            self.assertFalse((output / "first_pass.json").exists())

    def test_unauthorized_execution_rejected_before_api(self):
        with tempfile.TemporaryDirectory() as d:
            parent = Path(d)
            packet = parent / "task.txt"
            packet.write_text("private test input", encoding="utf-8")
            args = ["--arm", "A", "--task-file", str(packet),
                    "--task-sha256", hashlib.sha256(packet.read_bytes()).hexdigest(),
                    "--candidate-commit", "a" * 40,
                    "--output-dir", str(parent / "out"), "--execute-api"]
            with patch.object(x, "verify_commit"):
                with self.assertRaisesRegex(x.TrialError, "BUDGET_AUTHORIZATION_REQUIRED"):
                    x.main(args)

    def test_read_only_first_pass_no_grading(self):
        value = x.run_arm("task", "A", caller=lambda req: provider("answer", 1))
        self.assertNotIn("decision_correct", value)
        self.assertNotIn("reviewer", value)
        self.assertNotIn("passed", value)
        self.assertEqual(value["first_pass"], "answer")


if __name__ == "__main__":
    unittest.main()
