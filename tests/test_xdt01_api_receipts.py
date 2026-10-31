"""Focused zero-network faults for paid-attempt durability; all providers are fake."""
import hashlib
import io
import json
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import run_xdt01_skill_selection as runner
from xdt01_attempt_journal import AttemptJournal


def provider(text="answer", number=1, **updates):
    value = {"id": "resp_fake_%d" % number, "status": "completed", "model": runner.MODEL,
             "usage": {"input_tokens": 20, "output_tokens": 5, "total_tokens": 25},
             "output": [{"type": "message", "content": [{"type": "output_text", "text": text}]}]}
    value.update(updates)
    return value


class AttemptReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.network = patch.object(socket.socket, "connect", side_effect=AssertionError("REAL_NETWORK_FORBIDDEN"))
        self.network.start()

    def tearDown(self):
        self.network.stop()
        self.temp.cleanup()

    def journal(self, arm="A"):
        directory = self.root / arm
        directory.mkdir(mode=0o700)
        grant = {"experiment_id": "f" * 64, "arm": arm, "task_sha256": "a" * 64,
                 "candidate_commit": "b" * 40, "max_calls": 2 if arm == "C" else 1}
        (directory / "grant.json").write_text(json.dumps(grant))
        return directory, AttemptJournal(directory, arm, "a" * 64, "b" * 40)

    def outcome(self, directory, index=1):
        return json.loads((directory / ("outcome-%02d.json" % index)).read_text())["evidence"]

    def test_attempt_is_durable_before_send_and_never_reusable(self):
        directory, journal = self.journal()
        calls = []
        def fake(request):
            attempt = directory / "attempt-01.json"
            self.assertTrue(attempt.is_file())
            self.assertEqual(attempt.stat().st_mode & 0o777, 0o600)
            self.assertEqual(json.loads(attempt.read_text())["billing_status"], "UNKNOWN_BILLED")
            calls.append(request)
            return provider()
        runner.run_arm("synthetic fault marker", "A", caller=fake, attempt_journal=journal)
        with self.assertRaises(ValueError):
            runner.run_arm("synthetic fault marker", "A", caller=fake, attempt_journal=journal)
        self.assertEqual(len(calls), 1)
        evidence = self.outcome(directory)
        self.assertEqual(evidence["response_id"], "resp_fake_1")
        self.assertEqual(evidence["usage"]["total_tokens"], 25)

    def test_partial_success_then_timeout_retains_both_attempts(self):
        directory, journal = self.journal("C")
        calls = []
        def fake(request):
            calls.append(request)
            if len(calls) == 1:
                return provider("USE")
            raise TimeoutError("SENSITIVE_ERROR_TEXT_MUST_NOT_BE_RETAINED")
        with self.assertRaisesRegex(runner.TrialError, "PROVIDER_TIMEOUT"):
            runner.run_arm("synthetic fault marker", "C", lambda: "synthetic skill", fake,
                           attempt_journal=journal)
        self.assertEqual(len(calls), 2)
        self.assertEqual(self.outcome(directory, 1)["response_id"], "resp_fake_1")
        second = self.outcome(directory, 2)
        self.assertEqual(second["billing_status"], "UNKNOWN_BILLED")
        self.assertNotIn("SENSITIVE_ERROR_TEXT", json.dumps(second))
        with self.assertRaises(ValueError):
            journal.reserve(2, "answer", "c" * 64)

    def test_incomplete_selector_retains_id_usage_and_stops(self):
        directory, journal = self.journal("C")
        calls = []
        def fake(request):
            calls.append(request)
            return provider("", status="incomplete", output=[],
                            incomplete_details={"reason": "max_output_tokens"},
                            usage={"input_tokens": 200, "output_tokens": 350, "total_tokens": 550,
                                   "output_tokens_details": {"reasoning_tokens": 350}})
        with self.assertRaisesRegex(runner.TrialError, "PROVIDER_NOT_COMPLETED"):
            runner.run_arm("synthetic fault marker", "C", lambda: self.fail("No Skill load after failed selector"),
                           fake, attempt_journal=journal)
        self.assertEqual(len(calls), 1)
        evidence = self.outcome(directory)
        self.assertEqual(evidence["response_id"], "resp_fake_1")
        self.assertEqual(evidence["usage"]["output_tokens_details"]["reasoning_tokens"], 350)
        self.assertEqual(evidence["incomplete_reason"], "max_output_tokens")
        self.assertEqual(evidence["billing_status"], "UNKNOWN_BILLED")
        self.assertFalse((directory / "attempt-02.json").exists())

    def test_http_error_retains_safe_headers_without_body_or_key(self):
        directory, journal = self.journal()
        error = urllib.error.HTTPError("https://api.openai.com/v1/responses", 429,
                                      "SENSITIVE_PROVIDER_MESSAGE", {"x-request-id": "req_fake_429"},
                                      io.BytesIO(b"PRIVATE_PROVIDER_BODY"))
        with patch.dict(runner.os.environ, {"OPENAI_API_KEY": "SYNTHETIC_KEY_NOT_A_CREDENTIAL"}), \
             patch.object(runner.urllib.request, "urlopen", side_effect=error) as send:
            with self.assertRaisesRegex(runner.TrialError, "PROVIDER_HTTP_ERROR"):
                runner.run_arm("synthetic fault marker", "A", attempt_journal=journal)
        send.assert_called_once()
        evidence = self.outcome(directory)
        self.assertEqual(evidence["http_status"], 429)
        self.assertEqual(evidence["provider_request_id"], "req_fake_429")
        serialized = json.dumps(evidence)
        for forbidden in ("SYNTHETIC_KEY", "PRIVATE_PROVIDER_BODY", "SENSITIVE_PROVIDER_MESSAGE"):
            self.assertNotIn(forbidden, serialized)

    def test_raw_transport_timeout_retains_unknown_billing(self):
        directory, journal = self.journal()
        with patch.dict(runner.os.environ, {"OPENAI_API_KEY": "SYNTHETIC_KEY_NOT_A_CREDENTIAL"}), \
             patch.object(runner.urllib.request, "urlopen", side_effect=TimeoutError("private detail")) as send:
            with self.assertRaisesRegex(runner.TrialError, "PROVIDER_TIMEOUT"):
                runner.run_arm("synthetic fault marker", "A", attempt_journal=journal)
        send.assert_called_once()
        self.assertEqual(self.outcome(directory)["billing_status"], "UNKNOWN_BILLED")

    def test_crash_after_reservation_has_unknown_billing_and_no_reuse(self):
        directory, journal = self.journal()
        journal.reserve(1, "answer", "c" * 64)
        self.assertFalse((directory / "outcome-01.json").exists())
        with self.assertRaises(ValueError):
            journal.reserve(1, "answer", "c" * 64)
        self.assertEqual(json.loads((directory / "attempt-01.json").read_text())["billing_status"], "UNKNOWN_BILLED")

    def test_invalid_json_shape_still_keeps_transport_evidence(self):
        directory, journal = self.journal()
        class FakeReply:
            headers = {"x-request-id": "req_fake_shape"}
            status = 200
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, limit): return b"[]"
        with patch.dict(runner.os.environ, {"OPENAI_API_KEY": "SYNTHETIC_KEY_NOT_A_CREDENTIAL"}), \
             patch.object(runner.urllib.request, "urlopen", return_value=FakeReply()) as send:
            with self.assertRaisesRegex(runner.TrialError, "PROVIDER_INVALID_RESPONSE_SHAPE"):
                runner.run_arm("synthetic fault marker", "A", attempt_journal=journal)
        send.assert_called_once()
        evidence = self.outcome(directory)
        self.assertEqual(evidence["provider_request_id"], "req_fake_shape")
        self.assertEqual(evidence["http_status"], 200)
        self.assertEqual(evidence["billing_status"], "UNKNOWN_BILLED")

    def test_provider_parser_failure_still_retains_available_metadata(self):
        directory, journal = self.journal()
        malformed = provider(usage={"input_tokens": 20, "output_tokens": 5})
        with self.assertRaisesRegex(runner.TrialError, "PROVIDER_USAGE_INVALID"):
            runner.run_arm("synthetic fault marker", "A", caller=lambda request: malformed,
                           attempt_journal=journal)
        evidence = self.outcome(directory)
        self.assertEqual(evidence["response_id"], "resp_fake_1")
        self.assertEqual(evidence["usage"], {"input_tokens": 20, "output_tokens": 5})

    def test_protocol_requests_remain_byte_equivalent(self):
        # Canonical request hashes from public frozen commit 03f29b980ba326ac0509299b9c94292d6a1a5d5a.
        # Input "marker" and loaded Skill "skill" are synthetic contract fixtures.
        # This needs no historical checkout, Git object, API or private case data.
        frozen = {
            "A": ["44412a915e27b4e2eda40f54013e514e4f7f1dcb098a0b0238a6302671a4a05f"],
            "B": ["dadd51792b021d6a4a2a8a5303b8020c209cd2a0890d861deb81c4d6abdf3b01"],
            "C-SKIP": ["10aa1c0c5316e80ee75700e6542af4aa90fc6dac61294918bbf1042a51d8a79b",
                       "20ccee71bf6b4e06f8dc906019581ec1fd0fbc9bf3712e9097465a065f24493b"],
            "C-USE": ["10aa1c0c5316e80ee75700e6542af4aa90fc6dac61294918bbf1042a51d8a79b",
                      "af43890bf85ce5ea74cd75d9085a969382b7fbb0bd255270c34764a68339c673"],
        }
        for arm, choice in (("A", None), ("B", None), ("C", "SKIP"), ("C", "USE")):
            requests = []
            def fake(request):
                requests.append(request)
                return provider(choice if arm == "C" and len(requests) == 1 else "answer",
                                len(requests))
            runner.run_arm("marker", arm, lambda: "skill", fake)
            current = [hashlib.sha256(json.dumps(request, ensure_ascii=False, sort_keys=True,
                                                 separators=(",", ":")).encode()).hexdigest()
                       for request in requests]
            self.assertEqual(current, frozen[arm + ("-" + choice if choice else "")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
