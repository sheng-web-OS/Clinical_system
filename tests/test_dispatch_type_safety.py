"""Pre-activation fail-closed malformed JSON checks. No network or paid API."""
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.dispatch_selector import (
    DispatchError, fetch_open_issue_snapshot, load_manifest, select_tasks,
)

ROOT = Path(__file__).resolve().parents[1]


class DispatchTypeSafetyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_manifest(ROOT / "ops/dispatch.json")

    def test_unhashable_mode_list_and_dict_fail_closed(self):
        for invalid in (["shadow"], {"value": "shadow"}):
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as d:
                config = copy.deepcopy(self.config)
                config["mode"] = invalid
                path = Path(d) / "dispatch.json"
                path.write_text(json.dumps(config), encoding="utf-8")
                with self.assertRaisesRegex(
                        DispatchError, "^UNAPPROVED_MODE_OR_TASK_BATCH$"):
                    load_manifest(path)

    def test_bad_snapshot_state_fails_closed(self):
        snapshot = {
            task["target"]: {
                "number": int(task["target"].split(":")[1]),
                "state": "open",
                "is_pr": False,
            }
            for task in self.config["tasks"]
        }
        for invalid in (["open"], {"value": "open"}):
            with self.subTest(invalid=invalid):
                data = copy.deepcopy(snapshot)
                data["issue:76"]["state"] = invalid
                with self.assertRaisesRegex(
                        DispatchError, "^SOURCE_METADATA_MISSING_OR_INVALID$"):
                    select_tasks(self.config, data)

    def test_malformed_live_metadata_fails_closed(self):
        config = copy.deepcopy(self.config)
        config["tasks"] = config["tasks"][:1]
        number = int(config["tasks"][0]["target"].split(":")[1])
        for invalid in (["open"], {"value": "open"}):
            with self.subTest(invalid=invalid):
                payload = json.dumps({"number": number, "state": invalid})
                with mock.patch("tools.dispatch_selector.urllib.request.urlopen",
                                return_value=io.BytesIO(payload.encode())):
                    with self.assertRaisesRegex(
                            DispatchError, "^GITHUB_METADATA_UNVERIFIED$"):
                        fetch_open_issue_snapshot(config)

    def test_valid_shadow_mode_and_metadata_unchanged(self):
        snapshot = {
            task["target"]: {
                "number": int(task["target"].split(":")[1]),
                "state": "open",
                "is_pr": False,
            }
            for task in self.config["tasks"]
        }
        result = select_tasks(self.config, snapshot)
        self.assertFalse(result["execution_authorized"])
        self.assertEqual("SHADOW_NO_ACTION", result["status"])
        self.assertEqual("ecg-original-evidence", result["selected"][0]["id"])

    def test_valid_live_metadata_unchanged(self):
        config = copy.deepcopy(self.config)
        config["tasks"] = config["tasks"][:1]
        number = int(config["tasks"][0]["target"].split(":")[1])
        payload = json.dumps({"number": number, "state": "open"})
        with mock.patch("tools.dispatch_selector.urllib.request.urlopen",
                        return_value=io.BytesIO(payload.encode())):
            result = fetch_open_issue_snapshot(config)
        self.assertEqual("open", result[config["tasks"][0]["target"]]["state"])


if __name__ == "__main__":
    unittest.main()
