"""ALE-01 private bridge regression suite. Synthetic inputs, no network/OAuth."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import ale_anki_drive_sync as p

REV1 = [2000000000001, 700101, -1, 1, 1, -1, 2500, 700, 1]
REV2 = [2000000000002, 700102, -1, 3, 7, 1, 2500, 1800, 1]

class FakeSheet:
    def __init__(self, ids=None, ambiguous=False, bad_header=False):
        self.keys = list(ids or [])
        self.rows = []
        self.ambiguous = ambiguous
        self.bad_header = bad_header
        self.append_calls = 0

    def verify_schema(self):
        if self.bad_header:
            raise RuntimeError("schema does not match")

    def existing_ids(self):
        return list(self.keys)

    def existing_rows(self):
        return [list(row) for row in self.rows]

    def append(self, rows):
        self.append_calls += 1
        self.rows += rows
        self.keys += [r[0] for r in rows]
        if self.ambiguous:
            self.ambiguous = False
            raise RuntimeError("connection lost after remote append")

class PrivateBridgeTests(unittest.TestCase):
    def run_sync(self, base, sheet, events=None, note_ids=None):
        events = [REV1, REV2] if events is None else events
        with patch.object(p, "check_version", return_value=6), \
             patch.object(p, "invoke", return_value=["A"]), \
             patch.object(p, "recent_reviews", return_value=events), \
             patch.object(p, "note_mapping", return_value=note_ids or {700101: 8, 700102: 9}), \
             patch.object(p.time, "time", return_value=2000000001.0):
            return p.synchronize(base, sheet)

    def test_private_file_permissions(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"private"/"state.json"
            p.private_write(path, {"schema": 1})
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(path.parent.stat().st_mode & 0o777, 0o700)
            self.assertEqual(p.load_json(path)["schema"], 1)

    def test_config_requires_desktop_client(self):
        with tempfile.TemporaryDirectory() as d:
            c = Path(d)/"client.json"
            c.write_text(json.dumps({"installed": {"client_id": "test"}}))
            with patch("builtins.print"):
                p.configure(Path(d)/"vault", "https://docs.google.com/spreadsheets/d/" + "A"*30 + "/edit", str(c))
            self.assertEqual(p.load_json(Path(d)/"vault"/p.CONFIG_NAME)["spreadsheet_id"], "A"*30)
            self.assertEqual((Path(d)/"vault"/p.CLIENT_NAME).stat().st_mode & 0o777, 0o600)

    def test_event_row_contract(self):
        row = p.event_rows([REV1], {700101: 43}, "2026-10-31T02:00:00Z")[0]
        self.assertEqual(len(row), len(p.HEADER))
        self.assertEqual(row[4], "")
        self.assertEqual(row[5:8], ["1", "UNKNOWN", "NOT_COLLECTED"])
        self.assertEqual(row[9], "NOT_DIAGNOSED")
        self.assertNotIn("question", str(row))

    def test_upload_and_readback(self):
        with tempfile.TemporaryDirectory() as d:
            sh, base = FakeSheet(), Path(d)/"local"
            result = self.run_sync(base, sh)
            self.assertEqual(result["new_events_uploaded"], 2)
            self.assertEqual(result["unique_cards_linked_to_notes"], 2)
            self.assertEqual(len(sh.rows), 2)
            self.assertEqual(p.load_json(base/p.STATE_NAME)["last_verified_review_ms"], REV2[0])

    def test_rerun_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            base, sh = Path(d)/"local", FakeSheet()
            self.run_sync(base, sh)
            result = self.run_sync(base, sh)
            self.assertEqual(result["new_events_uploaded"], 0)
            self.assertEqual(result["already_present"], 2)
            self.assertEqual(sh.append_calls, 1)

    def test_lost_response_recovers_without_duplicate(self):
        with tempfile.TemporaryDirectory() as d:
            base, sh = Path(d)/"local", FakeSheet(ambiguous=True)
            with self.assertRaisesRegex(RuntimeError, "connection lost"):
                self.run_sync(base, sh)
            self.assertFalse((base/p.STATE_NAME).exists())
            result = self.run_sync(base, sh)
            self.assertEqual(result["new_events_uploaded"], 0)
            self.assertEqual(len(sh.keys), 2)
            self.assertEqual(sh.append_calls, 1)

    def test_duplicate_remote_keys_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            key = p.event_key(REV1)
            sh = FakeSheet([key, key])
            with self.assertRaisesRegex(RuntimeError, "duplicate"):
                self.run_sync(Path(d)/"local", sh)
            self.assertEqual(sh.append_calls, 0)

    def test_schema_mismatch_blocks_upload(self):
        with tempfile.TemporaryDirectory() as d:
            sh = FakeSheet(bad_header=True)
            with self.assertRaisesRegex(RuntimeError, "schema"):
                self.run_sync(Path(d)/"local", sh)
            self.assertEqual(sh.append_calls, 0)

    def test_deleted_card_has_blank_note(self):
        row = p.event_rows([REV1], {}, "2026-10-31T02:00:00Z")[0]
        self.assertEqual(row[3], "")
        self.assertEqual(row[0], "anki-revlog:2000000000001:700101")

    def test_no_events_never_claims_uploaded(self):
        with tempfile.TemporaryDirectory() as d:
            sh = FakeSheet()
            result = self.run_sync(Path(d)/"local", sh, events=[])
            self.assertEqual(result["new_events_uploaded"], 0)
            self.assertEqual(sh.append_calls, 0)


class ContentReadbackTests(PrivateBridgeTests):
    """Same synthetic fixture; extra cases reject key-only false positives."""

    def test_rating_corruption_halts_cursor_and_retry(self):
        class AlteredSheet(FakeSheet):
            def append(self, rows):
                super().append(rows)
                self.rows[-1][5] = "4"
        with tempfile.TemporaryDirectory() as d:
            sh, base = AlteredSheet(), Path(d)/"private"
            with self.assertRaisesRegex(RuntimeError, "immutable review content"):
                self.run_sync(base, sh)
            self.assertFalse((base/p.STATE_NAME).exists())
            with self.assertRaisesRegex(RuntimeError, "immutable review content"):
                self.run_sync(base, sh)
            self.assertEqual(sh.append_calls, 1)

    def test_note_id_corruption_halts_cursor(self):
        class AlteredSheet(FakeSheet):
            def append(self, rows):
                super().append(rows)
                self.rows[0][3] = "999999"
        with tempfile.TemporaryDirectory() as d:
            sh, base = AlteredSheet(), Path(d)/"private"
            with self.assertRaisesRegex(RuntimeError, "note identity"):
                self.run_sync(base, sh)
            self.assertFalse((base/p.STATE_NAME).exists())

    def test_existing_wrong_rating_rejected_even_when_key_present(self):
        with tempfile.TemporaryDirectory() as d:
            base, sh = Path(d)/"private", FakeSheet()
            self.run_sync(base, sh)
            sh.rows[0][5] = "4"
            with self.assertRaisesRegex(RuntimeError, "immutable review content"):
                self.run_sync(base, sh)
            self.assertEqual(sh.append_calls, 1)

    def test_diagnostic_fields_are_mutable_without_duplication(self):
        with tempfile.TemporaryDirectory() as d:
            base, sh = Path(d)/"private", FakeSheet()
            self.run_sync(base, sh)
            sh.rows[0][6] = "OWNER_VERIFIED_CAUSE"
            sh.rows[0][9] = "DIAGNOSED"
            result = self.run_sync(base, sh)
            self.assertEqual(result["already_present"], 2)
            self.assertEqual(sh.append_calls, 1)

    def test_lost_ack_corruption_stops_recovery(self):
        class CorruptAmbiguous(FakeSheet):
            def append(self, rows):
                self.append_calls += 1
                self.rows.extend(rows)
                self.keys.extend(r[0] for r in rows)
                self.rows[0][2] = "123456"
                raise RuntimeError("connection lost")
        with tempfile.TemporaryDirectory() as d:
            sh, base = CorruptAmbiguous(), Path(d)/"private"
            with self.assertRaisesRegex(RuntimeError, "connection lost"):
                self.run_sync(base, sh)
            with self.assertRaisesRegex(RuntimeError, "immutable review content"):
                self.run_sync(base, sh)
            self.assertEqual(sh.append_calls, 1)



class FakeAuditSheet:
    def __init__(self, rows):
        self.rows = rows
    def verify_schema(self):
        return None
    def get(self, a1):
        if a1 != "Error_Events!A2:N":
            raise AssertionError("Unexpected range")
        return self.rows

class PrivateAuditTests(unittest.TestCase):
    def row(self):
        now_iso = p.datetime.fromtimestamp((REV1[0]+10000)/1000, tz=p.timezone.utc).isoformat()
        return p.event_rows([REV1], {700101: 313}, now_iso)[0]

    def test_audit_accepts_valid_unmapped_event(self):
        result = p.audit_private_sheet(FakeAuditSheet([self.row()]))
        self.assertEqual(result, {"events": 1, "unique_events": 1, "unmapped_family": 1})

    def test_audit_rejects_duplicate(self):
        row = self.row()
        with self.assertRaisesRegex(RuntimeError, "Duplicate"):
            p.audit_private_sheet(FakeAuditSheet([row, row]))

    def test_audit_rejects_wrong_card_identity(self):
        row = self.row()
        row[2] = "98765"
        with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
            p.audit_private_sheet(FakeAuditSheet([row]))

    def test_audit_rejects_invalid_rating(self):
        row = self.row()
        row[5] = "5"
        with self.assertRaisesRegex(RuntimeError, "rating"):
            p.audit_private_sheet(FakeAuditSheet([row]))

    def test_audit_rejects_unverified_status(self):
        row = self.row()
        row[12] = "SIMULATED"
        with self.assertRaisesRegex(RuntimeError, "sync status"):
            p.audit_private_sheet(FakeAuditSheet([row]))

    def test_audit_rejects_future_event_before_upload(self):
        row = self.row()
        row[13] = "2026-10-31T00:00:00+00:00"
        with self.assertRaisesRegex(RuntimeError, "out of order"):
            p.audit_private_sheet(FakeAuditSheet([row]))

    def test_audit_rejects_wrong_row_width(self):
        row = self.row()[:13]
        with self.assertRaisesRegex(RuntimeError, "row width"):
            p.audit_private_sheet(FakeAuditSheet([row]))

    def test_audit_empty_sheet_is_valid_but_not_evidence(self):
        result = p.audit_private_sheet(FakeAuditSheet([]))
        self.assertEqual(result["events"], 0)
        self.assertEqual(result["unique_events"], 0)

if __name__ == "__main__":
    unittest.main()
