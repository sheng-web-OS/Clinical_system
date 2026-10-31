"""Synthetic-only unit tests, no real user data and no network requests."""
import contextlib
import io
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch
import ale_anki_readonly as p


class AnkiReadOnlyTests(unittest.TestCase):
    def test_readonly_whitelist(self):
        with self.assertRaisesRegex(ValueError, 'refused'):
            p.invoke("deleteNotes", notes=[1])

    def test_no_duplicate_review_from_parent_child_decks(self):
        ev = [5002, 101, -1, 1, 1, -1, 2500, 1300, 1]
        with patch.object(p, "invoke", return_value=[ev]):
            got = p.recent_reviews(["Main", "Main::Sub"], 5000)
        self.assertEqual(got, [ev])

    def test_baseline_verify_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "private.json"
            with patch.object(p.time, "time", return_value=1700000000.0):
                with patch.object(p, "invoke", side_effect=[6, ["Test"]]):
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(p.begin(path), 0)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            ev = [1700000000001, 222, -1, 1, 10, 1, 2500, 1100, 1]
            with patch.object(p, "invoke", side_effect=[6, ["Test"], [ev], [{"cardId": 222, "note": 333, "question": "private raw text"}]]):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    self.assertEqual(p.verify(path), 0)
            self.assertNotIn("private raw text", out.getvalue())
            self.assertNotIn("222", out.getvalue())
            self.assertIn("CARD_NOTE_LINK_OK", out.getvalue())
            s = json.loads(path.read_text())
            self.assertEqual(s["last_verified"]["anki_note_id"], 333)
            self.assertNotIn("question", s["last_verified"])

    def test_no_review_does_not_fake_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "private.json"
            p.save_private(path, {"schema": 1, "started_at_ms": 10, "last_verified": None})
            with patch.object(p, "invoke", side_effect=[6, ["Test"], []]):
                with contextlib.redirect_stdout(io.StringIO()) as out:
                    self.assertEqual(p.verify(path), 2)
            self.assertIn("NO_NEW_REVIEWS", out.getvalue())

    def test_invalid_response_fails_closed(self):
        with patch.object(p.urllib.request, "urlopen") as http:
            http.return_value.__enter__.return_value.read.return_value = b'{"result": true}'
            with self.assertRaisesRegex(RuntimeError, "Unexpected"):
                p.invoke("version")


if __name__ == "__main__":
    unittest.main()
