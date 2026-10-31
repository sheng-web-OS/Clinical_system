"""Offline contract checks for Mac-only ALE unattended user LaunchAgent."""
import plistlib
import unittest
from pathlib import Path

from tools.ale_anki_launchd import LABEL, make_agent_config


class LaunchdContract(unittest.TestCase):
    def setUp(self):
        self.wrapper = Path("/Users/test/ClinicalOS-ALE-bridge/tools/ale_anki_unattended_run.sh")
        self.logs = Path("/Users/test/Library/Application Support/ClinicalOS-ALE/logs")

    def test_user_agent_is_bounded_and_not_persistent(self):
        config = make_agent_config(self.wrapper, self.logs)
        self.assertEqual(config["Label"], LABEL)
        self.assertEqual(config["StartInterval"], 1800)
        self.assertTrue(config["RunAtLoad"])
        self.assertFalse(config["KeepAlive"])
        self.assertEqual(config["ProgramArguments"], ["/bin/bash", str(self.wrapper)])

    def test_serializes_as_native_plist_without_secrets(self):
        data = plistlib.dumps(make_agent_config(self.wrapper, self.logs))
        self.assertEqual(plistlib.loads(data)["StartInterval"], 1800)
        for term in (b"client_secret", b"refresh_token", b"spreadsheet_id", b"Anki_note_id"):
            self.assertNotIn(term, data)

    def test_reject_nonabsolute_and_extreme_frequency(self):
        with self.assertRaises(ValueError):
            make_agent_config(Path("relative.sh"), self.logs)
        for interval in (1, 599, 86401):
            with self.subTest(interval=interval), self.assertRaises(ValueError):
                make_agent_config(self.wrapper, self.logs, interval)


if __name__ == "__main__":
    unittest.main()
