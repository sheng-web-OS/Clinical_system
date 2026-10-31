"""Synthetic-only regression for owner-private Anki red-flag feedback bridge."""
import importlib.util
from pathlib import Path
import sys
import types
import tempfile
import unittest
from unittest.mock import patch

anki = types.ModuleType("ale_anki_readonly")
anki.check_version = lambda: 6
anki.invoke = lambda action, **params: []
drive = types.ModuleType("ale_anki_drive_sync")
drive.BASE = Path("/nonexistent-private-mac")
drive.CONFIG_NAME = "private_config.json"
drive.LOCK_NAME = "private_lock"
drive.Sheets = object
drive.authorized_session = lambda path: None
drive.checked_json = lambda value: value
drive.load_json = lambda path, required=False: {}
drive.private_dir = lambda path: None
drive.private_write = lambda path, data: None

source = Path(__file__).resolve().parents[1] / "tools" / "ale_anki_flag_feedback.py"
spec = importlib.util.spec_from_file_location("ale_anki_flag_feedback", source)
mod = importlib.util.module_from_spec(spec)
# Restore sys.modules after loading; do NOT affect other Clinical OS tests.
with patch.dict(sys.modules, {
    "ale_anki_readonly": anki,
    "ale_anki_drive_sync": drive,
}):
    spec.loader.exec_module(mod)

NOW = "2026-10-31T14:00:00+00:00"

class FakeSession:
    def __init__(self):
        self.posts = []
        self.puts = []
        self.titles = ["Error_Events"]

    def get(self, url, params=None, timeout=None):
        return {"sheets": [{"properties": {"title": name}} for name in self.titles]}

    def post(self, url, json=None, params=None, timeout=None):
        self.posts.append((url, json))
        if url.endswith(":batchUpdate"):
            self.titles.append(json["requests"][0]["addSheet"]["properties"]["title"])
            return {"replies": [{}]}
        return {"updates": {"updatedRows": 1}}

    def put(self, url, json=None, params=None, timeout=None):
        self.puts.append((url, json))
        return {"updatedCells": len(json["values"][0])}

class FakeSheet:
    def __init__(self):
        self.root = "https://sheets.googleapis.com/v4/spreadsheets/dummy/values"
        self.session = FakeSession()
        self.header = []
        self.rows = []

    def get(self, range_str):
        if range_str.endswith("!A1:J1"):
            return [mod.HEADER] if self.session.puts else self.header
        return self.rows if range_str.endswith("!A2:J") else []

class TestRedFlagFeedback(unittest.TestCase):
    def test_new_flag_creates_unverified_signal_not_error_verdict(self):
        checkpoint, rows = mod.plan_events({}, {"42": 9}, NOW)
        self.assertEqual(rows[0][0], "anki-red-flag:42:1")
        self.assertEqual(rows[0][5:9], ["UNKNOWN", "PENDING_DIAGNOSIS", "UNMAPPED", "NOT_ASSESSED"])
        self.assertTrue(checkpoint["cards"]["42"]["active"])

    def test_same_flag_deduplicated(self):
        first, _ = mod.plan_events({}, {"42": 9}, NOW)
        second, rows = mod.plan_events(first, {"42": 9}, NOW)
        self.assertFalse(rows)
        self.assertEqual(second["cards"]["42"]["cycle"], 1)

    def test_clear_does_not_mean_qa_resolved(self):
        first, _ = mod.plan_events({}, {"42": 9}, NOW)
        second, rows = mod.plan_events(first, {}, NOW)
        self.assertEqual(rows, [])
        self.assertFalse(second["cards"]["42"]["active"])
        self.assertNotIn("RESOLVED", str(second))

    def test_reflag_after_observed_absence(self):
        first, _ = mod.plan_events({}, {"42": 9}, NOW)
        second, _ = mod.plan_events(first, {}, NOW)
        third, rows = mod.plan_events(second, {"42": 9}, NOW)
        self.assertEqual(rows[0][0], "anki-red-flag:42:2")
        self.assertEqual(third["cards"]["42"]["cycle"], 2)

    def test_mismatched_anki_note_rejected(self):
        first, _ = mod.plan_events({}, {"42": 9}, NOW)
        with self.assertRaisesRegex(RuntimeError, "identity"):
            mod.plan_events(first, {"42": 10}, NOW)

    def test_corrupt_local_state_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "checkpoint"):
            mod.plan_events({"schema": 3, "cards": {}}, {"42": 9}, NOW)

    def test_card_level_read_not_sibling(self):
        with patch.object(mod, "invoke", side_effect=[
            [42], [{"cardId": 42, "note": 9, "flags": 1}],
        ]) as query:
            self.assertEqual(mod.read_flagged_cards(), {"42": 9})
            self.assertEqual(query.call_args_list[0].kwargs["query"], "flag:1")

    def test_flag_changed_during_scan_is_not_accepted(self):
        with patch.object(mod, "invoke", side_effect=[
            [42], [{"cardId": 42, "note": 9, "flags": 0}],
        ]):
            with self.assertRaisesRegex(RuntimeError, "changed"):
                mod.read_flagged_cards()

    def test_duplicate_inventory_rejected(self):
        with patch.object(mod, "invoke", return_value=[42, 42]):
            with self.assertRaisesRegex(RuntimeError, "duplicated"):
                mod.read_flagged_cards()

    def test_private_tab_bootstrap(self):
        sheet = FakeSheet()
        mod.ensure_feedback_tab(sheet)
        self.assertEqual(sheet.session.titles[-1], "Card_Feedback")
        self.assertEqual(len(sheet.session.puts), 1)

    def test_existing_wrong_schema_rejected_without_write(self):
        sheet = FakeSheet()
        sheet.session.titles.append("Card_Feedback")
        sheet.header = [["not", "the", "correct", "schema"]]
        with self.assertRaisesRegex(RuntimeError, "schema"):
            mod.ensure_feedback_tab(sheet)
        self.assertEqual(sheet.session.posts, [])
        self.assertEqual(sheet.session.puts, [])

    def test_existing_signal_remains_immutable_but_diagnosis_editable(self):
        sheet = FakeSheet()
        _, rows = mod.plan_events({}, {"42": 9}, NOW)
        persisted = list(rows[0])
        persisted[5] = "REVIEWED_DIAGNOSIS_HYPOTHESIS"
        sheet.rows = [persisted]
        self.assertEqual(mod.sync_event_rows(sheet, rows), (0, 1))
        self.assertEqual(sheet.session.posts, [])

    def test_remote_id_tampering_blocks_success(self):
        sheet = FakeSheet()
        _, rows = mod.plan_events({}, {"42": 9}, NOW)
        persisted = list(rows[0])
        persisted[3] = "wrong-note"
        sheet.rows = [persisted]
        with self.assertRaisesRegex(RuntimeError, "mismatch"):
            mod.sync_event_rows(sheet, rows)

    def test_remote_duplicate_blocks_success(self):
        sheet = FakeSheet()
        _, rows = mod.plan_events({}, {"42": 9}, NOW)
        sheet.rows = [rows[0], rows[0]]
        with self.assertRaisesRegex(RuntimeError, "Duplicate"):
            mod.sync_event_rows(sheet, rows)

    def test_false_transport_ack_without_remote_readback_blocks_checkpoint(self):
        sheet = FakeSheet()
        _, rows = mod.plan_events({}, {"42": 9}, NOW)
        with self.assertRaisesRegex(RuntimeError, "readback"):
            mod.sync_event_rows(sheet, rows)

    def test_later_retry_recovers_remote_observation_without_overwriting_diagnosis(self):
        sheet = FakeSheet()
        _, original = mod.plan_events({}, {"42": 9}, NOW)
        sheet.rows = [list(original[0])]
        sheet.rows[0][5] = "DIAGNOSIS_REVIEW_PENDING"
        _, retry = mod.plan_events({}, {"42": 9}, "2026-10-31T14:05:00+00:00")
        self.assertEqual(mod.sync_event_rows(sheet, retry), (0, 1))
        self.assertEqual(retry[0][1], NOW)
        self.assertEqual(sheet.rows[0][5], "DIAGNOSIS_REVIEW_PENDING")
        self.assertEqual(sheet.session.posts, [])

    def test_recovery_rejects_changed_note_even_with_valid_old_timestamp(self):
        sheet = FakeSheet()
        _, original = mod.plan_events({}, {"42": 9}, NOW)
        sheet.rows = [list(original[0])]
        sheet.rows[0][3] = "10"
        _, retry = mod.plan_events({}, {"42": 9}, "2026-10-31T14:05:00+00:00")
        with self.assertRaisesRegex(RuntimeError, "mismatch"):
            mod.sync_event_rows(sheet, retry)
        self.assertEqual(sheet.session.posts, [])

    def test_recovery_rejects_invalid_naive_or_future_observation_time(self):
        for invalid in ("NOT_VERIFIED", "2026-10-31T14:00:00", "2026-10-31T14:10:00+00:00"):
            with self.subTest(timestamp=invalid):
                sheet = FakeSheet()
                _, rows = mod.plan_events({}, {"42": 9}, NOW)
                sheet.rows = [list(rows[0])]
                sheet.rows[0][1] = invalid
                _, retry = mod.plan_events({}, {"42": 9}, "2026-10-31T14:05:00+00:00")
                with self.assertRaisesRegex(RuntimeError, "timestamp"):
                    mod.sync_event_rows(sheet, retry)
                self.assertEqual(sheet.session.posts, [])

    def test_run_persists_recovered_time_after_checkpoint_write_failure(self):
        sheet = FakeSheet()
        _, original = mod.plan_events({}, {"42": 9}, NOW)
        sheet.rows = [list(original[0])]
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(mod, "load_json", side_effect=lambda p, required=False:
                    {"tab": "Error_Events", "spreadsheet_id": "dummy"} if required else {}), \
                    patch.object(mod, "read_flagged_cards", return_value={"42": 9}), \
                    patch.object(mod, "utc_now", return_value="2026-10-31T14:05:00+00:00"), \
                    patch.object(mod, "Sheets", return_value=sheet), \
                    patch.object(mod, "ensure_feedback_tab"), \
                    patch.object(mod, "private_write", side_effect=[OSError("synthetic failure"), None]) as save:
                with self.assertRaises(OSError):
                    mod.run(Path(tmp))
                self.assertEqual(mod.run(Path(tmp)), (1, 0, 1))
        self.assertEqual(save.call_args.args[1]["cards"]["42"]["first_detected_utc"], NOW)
        self.assertEqual(len(sheet.rows), 1)
        self.assertEqual(sheet.session.posts, [])

    def test_partial_batch_append_lost_ack_recovers_without_duplicate_rows(self):
        sheet = FakeSheet()
        _, rows = mod.plan_events({}, {"42": 9, "43": 10}, NOW)
        sheet.rows = [list(rows[0])]

        def append_then_lose_ack(url, json=None, **kwargs):
            sheet.session.posts.append((url, json))
            sheet.rows.extend([list(row) for row in json["values"]])
            raise OSError("synthetic ACK loss after append")

        with patch.object(sheet.session, "post", side_effect=append_then_lose_ack):
            _, retry = mod.plan_events({}, {"42": 9, "43": 10}, "2026-10-31T14:05:00+00:00")
            with self.assertRaises(OSError):
                mod.sync_event_rows(sheet, retry)
        _, final_retry = mod.plan_events({}, {"42": 9, "43": 10}, "2026-10-31T14:10:00+00:00")
        self.assertEqual(mod.sync_event_rows(sheet, final_retry), (0, 2))
        self.assertEqual([row[1] for row in final_retry], [NOW, "2026-10-31T14:05:00+00:00"])
        self.assertEqual(len(sheet.rows), 2)
        self.assertEqual(len(sheet.session.posts), 1)

if __name__ == "__main__":
    unittest.main()
