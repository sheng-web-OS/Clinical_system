"""Synthetic-only tests. No real Anki/Google credentials or private card data."""
import hashlib
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import ale_anki_import_queue as q


def sample(key="ALE26-M08-01"):
    front = "<!--" + key + "-->When is a score insufficient?"
    back = "A test score cannot replace clinical assessment."
    return {
        "card_key": key, "front_html": front, "back_html": back,
        "tags": "ALE::pilot clinical::respiratory",
        "deck": "ClinicalOS::ALE_20261031_Pilot",
        "source_ref": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
        "independent_review_ref": "https://github.com/sheng-web-OS/Clinical_system/issues/258#issuecomment-123",
        "qa_status": "INDEPENDENT_MEDICAL_QA_PASS",
        "release_status": "READY_TO_IMPORT", "import_status": "PENDING",
        "anki_note_id": "", "content_sha256": q.digest(front, back),
    }


def array(row):
    return [row[k] for k in q.HEADER]


class Session:
    def __init__(self, sheet):
        self.sheet = sheet

    def put(self, url, params=None, json=None, timeout=None):
        vals = json["values"][0]
        self.sheet.entry["import_status"] = vals[0]
        self.sheet.entry["anki_note_id"] = vals[1]
        self.sheet.entry["content_sha256"] = vals[2]
        class Response:
            status_code = 200
            def json(self):
                return {"updatedCells": 3}
        return Response()


class Sheet:
    root = "https://sheets.googleapis.com/v4/spreadsheets/placeholder/values"

    def __init__(self, entry):
        self.entry = dict(entry)
        self.session = Session(self)

    def get(self, a1):
        if a1 == q.TAB + "!A1:L1":
            return [q.HEADER]
        if a1 == q.TAB + "!A2:L":
            return [array(self.entry)]
        if a1 == q.TAB + "!A2:L2":
            return [array(self.entry)]
        if a1 == q.TAB + "!J2:L2":
            return [[self.entry["import_status"], self.entry["anki_note_id"], self.entry["content_sha256"]]]
        raise AssertionError("Unexpected range " + a1)


class TestQueue(unittest.TestCase):
    def test_digest_deterministic_and_bound_to_answer(self):
        a = sample()
        self.assertEqual(a["content_sha256"], q.digest(a["front_html"], a["back_html"]))
        self.assertNotEqual(a["content_sha256"], q.digest(a["front_html"], "different"))

    def test_required_review(self):
        a = sample()
        a["independent_review_ref"] = ""
        with self.assertRaises(ValueError):
            q.validate_ready(a)

    def test_no_only_writer_qa(self):
        a = sample()
        a["qa_status"] = "SELF_CHECK_ONLY"
        with self.assertRaises(ValueError):
            q.validate_ready(a)

    def test_html_scripts_forbidden(self):
        a = sample()
        a["back_html"] = '<img src=x onerror=alert(1)>'
        with self.assertRaises(ValueError):
            q.validate_ready(a)

    def test_wrong_digest_forbidden(self):
        a = sample()
        a["content_sha256"] = "0"*64
        with self.assertRaises(ValueError):
            q.validate_ready(a)

    def test_untrusted_deck_forbidden(self):
        a = sample()
        a["deck"] = "Default"
        with self.assertRaises(ValueError):
            q.validate_ready(a)

    def test_skipped_never_written(self):
        a = sample()
        a["import_status"] = "SKIPPED"
        with patch.object(q, "local_anki", side_effect=AssertionError("No calls")):
            self.assertEqual(q.process(Sheet(a)), (0, 0))

    def test_draft_qa_never_written(self):
        a = sample()
        a["release_status"] = "HOLD"
        with patch.object(q, "local_anki", side_effect=AssertionError("No calls")):
            self.assertEqual(q.process(Sheet(a)), (0, 0))

    def test_new_note_created_and_verified(self):
        a = sample(key="CARD-TEST1")
        s = Sheet(a)
        called = []
        def api(action, **params):
            called.append(action)
            if action == "version": return 6
            if action == "deckNames": return [a["deck"]]
            if action == "findNotes": return []
            if action == "addNote": return 123
            if action == "notesInfo":
                return [{"noteId": 123, "modelName": "Basic",
                         "tags": ["ale::card::CARD-TEST1"],
                         "fields": {"Front": {"value": a["front_html"]},
                                    "Back": {"value": a["back_html"]}}}]
            raise AssertionError(action)
        with patch.object(q, "local_anki", side_effect=api):
            self.assertEqual(q.process(s), (1, 0))
        self.assertEqual(called.count("addNote"), 1)
        self.assertEqual(s.entry["import_status"], "IMPORTED")
        self.assertEqual(s.entry["anki_note_id"], "123")

    def test_retry_recovers_existing_and_does_not_duplicate(self):
        a = sample(key="CARD-TEST2")
        s = Sheet(a)
        called = []
        def api(action, **params):
            called.append(action)
            if action == "version": return 6
            if action == "deckNames": return [a["deck"]]
            if action == "findNotes": return [456]
            if action == "notesInfo":
                return [{"noteId": 456, "modelName": "Basic",
                         "tags": ["ale::card::CARD-TEST2"],
                         "fields": {"Front": {"value": a["front_html"]},
                                    "Back": {"value": a["back_html"]}}}]
            raise AssertionError("No writes expected")
        with patch.object(q, "local_anki", side_effect=api):
            self.assertEqual(q.process(s), (0, 1))
        self.assertNotIn("addNote", called)
        self.assertEqual(s.entry["anki_note_id"], "456")

    def test_duplicate_existing_conflict_stops(self):
        a = sample(key="CARD-TEST3")
        s = Sheet(a)
        def api(action, **params):
            if action == "version": return 6
            if action == "deckNames": return [a["deck"]]
            if action == "findNotes": return [111, 222]
            raise AssertionError("No writes expected")
        with patch.object(q, "local_anki", side_effect=api):
            with self.assertRaises(RuntimeError):
                q.process(s)
        self.assertEqual(s.entry["import_status"], "PENDING")

    def test_legacy_pilot_reconciliation(self):
        a = sample()
        events = []
        def api(action, **params):
            events.append(action)
            if action == "findNotes":
                return [] if "ale::card::" in params["query"] else [777]
            if action == "notesInfo":
                return [{"noteId": 777, "modelName": "Basic", "tags": ["ALE::pilot"],
                         "fields": {"Front": {"value": a["front_html"]},
                                    "Back": {"value": a["back_html"]}}}]
            raise AssertionError("Unexpected write")
        with patch.object(q, "local_anki", side_effect=api):
            self.assertEqual(q.existing_note(a, q.note_tag(a["card_key"])), 777)
        self.assertNotIn("addNote", events)

    def test_status_defaults_disabled(self):
        with TemporaryDirectory() as tmp:
            with patch.object(q, "private_dir"):
                self.assertTrue(q.run(Path(tmp), "run").startswith("ALE_AUTOIMPORT_DISABLED"))


if __name__ == "__main__":
    unittest.main()
