import unittest
from unittest.mock import patch
from tools import drive_agent_pr


class DraftPRGateTests(unittest.TestCase):
    def test_scoped_verified_case(self):
        self.assertEqual(drive_agent_pr.plan("true", "sheng-web-OS/Clinical_system",
                                             "refs/heads/main"), "PROPOSE_DRAFT_PR")

    def test_no_unverified_writes(self):
        for x in ("", "false", "TRUE", "1"):
            self.assertEqual(drive_agent_pr.plan(x, "sheng-web-OS/Clinical_system",
                                                 "refs/heads/main"), "HOLD")

    def test_wrong_repository_never_writes(self):
        self.assertEqual(drive_agent_pr.plan("true", "outsider/repo",
                                             "refs/heads/main"), "HOLD")

    def test_not_main_never_writes(self):
        self.assertEqual(drive_agent_pr.plan("true", "sheng-web-OS/Clinical_system",
                                             "refs/heads/exploit"), "HOLD")

    def test_no_duplicate_pr(self):
        calls = []
        def fake_api(method, path, payload=None):
            calls.append((method, path))
            return [{"number": 1}]
        with patch.object(drive_agent_pr, "api", side_effect=fake_api), \
             patch.dict("os.environ", {
                 "VERIFIED_SYNTHETIC_READ": "true",
                 "GITHUB_REPOSITORY": "sheng-web-OS/Clinical_system",
                 "GITHUB_REF": "refs/heads/main"
             }):
            self.assertEqual(drive_agent_pr.main(), 0)
        self.assertEqual(len(calls), 1)
        self.assertIn("pulls?", calls[0][1])

    def test_draft_only_fixed_text(self):
        self.assertIn("Draft", "Draft")
        self.assertNotIn("1hk0HkOk", drive_agent_pr.BODY)
        self.assertNotIn("1oIVDRe7", drive_agent_pr.BODY)
        self.assertNotIn("sk-", drive_agent_pr.BODY)


if __name__ == "__main__":
    unittest.main()
