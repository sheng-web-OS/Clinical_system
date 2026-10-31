"""Regression: error diagnostics must distinguish provider status without leaks."""
import io
import json
import unittest
import urllib.error
from unittest.mock import patch

from tools.drive_source_agent import classify_openai_http_error, model_decision

CTX = {"task_id": "DEMO-2026-10-29-A",
       "source_class": "synthetic_public_fixture",
       "source_state": "missing", "requires_original": True}
SECRET_MARKER = "sk-dont-print-secret"
SENSITIVE_BODY = "PRIVATE CONFIDENTIAL FIXTURE INPUT"
MODEL = "gpt-5-mini"


def provider_error(status, payload):
    return urllib.error.HTTPError(
        url="https://api.openai.com/v1/responses",
        code=status,
        msg="should-not-appear-in-logs",
        hdrs=None,
        fp=io.BytesIO(json.dumps(payload).encode("utf-8")),
    )


class HttpDiagnosticsTests(unittest.TestCase):
    def test_http_400_invalid_request_has_safe_status(self):
        error = provider_error(400, {
            "error": {"code": "invalid_request_error",
                      "message": "bad body " + SENSITIVE_BODY}})
        result = classify_openai_http_error(error)
        self.assertEqual(result, "MODEL_HTTP_400_INVALID_REQUEST")
        self.assertNotIn(SENSITIVE_BODY, result)

    def test_http_401_invalid_key_detectable_without_key(self):
        error = provider_error(401, {
            "error": {"code": "invalid_api_key", "message": SECRET_MARKER}})
        result = classify_openai_http_error(error)
        self.assertEqual(result, "MODEL_HTTP_401_INVALID_API_KEY")
        self.assertNotIn(SECRET_MARKER, result)

    def test_429_quota_differs_from_rate_limit(self):
        quota = provider_error(429, {"error": {"code": "insufficient_quota"}})
        rate = provider_error(429, {"error": {"code": "rate_limit_exceeded"}})
        self.assertEqual(classify_openai_http_error(quota),
                         "MODEL_HTTP_429_INSUFFICIENT_QUOTA")
        self.assertEqual(classify_openai_http_error(rate),
                         "MODEL_HTTP_429_RATE_LIMIT")

    def test_http_429_quota_may_use_type_when_code_is_null(self):
        quota = provider_error(429, {
            "error": {"type": "insufficient_quota", "code": None,
                      "message": SECRET_MARKER + SENSITIVE_BODY}})
        label = classify_openai_http_error(quota)
        self.assertEqual(label, "MODEL_HTTP_429_INSUFFICIENT_QUOTA")
        self.assertNotIn(SECRET_MARKER, label)

    def test_http_429_billing_codes_are_specific(self):
        cases = (
            ("credit_balance_exhausted", "CREDIT_BALANCE_EXHAUSTED"),
            ("organization_usage_limit_exceeded", "ORG_USAGE_LIMIT_EXCEEDED"),
            ("organization_spend_limit_exceeded", "ORG_SPEND_LIMIT_EXCEEDED"),
            ("project_spend_limit_exceeded", "PROJECT_SPEND_LIMIT_EXCEEDED"),
        )
        for code, expected in cases:
            with self.subTest(code=code):
                error = provider_error(429, {"error": {
                    "code": code, "type": "insufficient_quota",
                    "message": SECRET_MARKER}})
                self.assertEqual(classify_openai_http_error(error),
                                 "MODEL_HTTP_429_" + expected)

    def test_code_takes_precedence_over_generic_type(self):
        error = provider_error(429, {"error": {
            "code": "rate_limit_exceeded", "type": "insufficient_quota"}})
        self.assertEqual(classify_openai_http_error(error),
                         "MODEL_HTTP_429_RATE_LIMIT")

    def test_nonallowlisted_type_not_logged(self):
        error = provider_error(429, {"error": {
            "code": None, "type": SECRET_MARKER, "message": SENSITIVE_BODY}})
        self.assertEqual(classify_openai_http_error(error), "MODEL_HTTP_429")

    def test_unrecognized_provider_error_code_never_exposed(self):
        malicious = "inject_" + SENSITIVE_BODY
        error = provider_error(403, {"error": {"code": malicious,
                                               "message": SECRET_MARKER}})
        result = classify_openai_http_error(error)
        self.assertEqual(result, "MODEL_HTTP_403")
        self.assertNotIn(malicious, result)
        self.assertNotIn(SECRET_MARKER, result)

    def test_non_json_body_produces_only_status(self):
        error = urllib.error.HTTPError(
            "https://api.openai.com/v1/responses", 502,
            "internal logs", None, io.BytesIO(SECRET_MARKER.encode()))
        self.assertEqual(classify_openai_http_error(error), "MODEL_HTTP_502")

    def test_http_error_first_not_generic_network_error(self):
        error = provider_error(400, {"error": {"code": "unsupported_parameter"}})
        with patch("tools.drive_source_agent.urllib.request.urlopen",
                   side_effect=error):
            with self.assertRaisesRegex(RuntimeError,
                                        "^MODEL_HTTP_400_UNSUPPORTED_PARAMETER$"):
                model_decision(CTX, "test-only-secret", MODEL)

    def test_no_configured_key_blocks_before_http(self):
        with patch("tools.drive_source_agent.urllib.request.urlopen") as api:
            with self.assertRaisesRegex(RuntimeError, "^NOT_CONFIGURED_MODEL$"):
                model_decision(CTX, None, MODEL)
            api.assert_not_called()


if __name__ == "__main__":
    unittest.main()
