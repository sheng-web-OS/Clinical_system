"""Synthetic local Concept Map pilot tests; no Anki/Google network I/O."""
import unittest
import ale_anki_concept_map as m

E = ["anki-revlog:12345:222", "2026-10-31T00:00:00Z", "222", "333",
     "", "1", "UNKNOWN", "NOT_COLLECTED", "", "NOT_DIAGNOSED",
     "", "12345", "SYNCED_READ_ONLY", "2026-10-31T00:00:02Z"]


class ConceptMapTests(unittest.TestCase):
    def test_latest_unlinked(self):
        self.assertEqual(m.latest_unlinked_review([E], []), E)

    def test_previous_confirmed_blocks_same_card(self):
        previous = ["", "333", "222", "concept-a", "", "", "", "", "", "",
                    "OWNER_CONFIRMED_SINGLE_CARD"]
        self.assertIsNone(m.latest_unlinked_review([E], [previous]))

    def test_map_row_exact_11_fields(self):
        row = m.mapping_row(E, "concept-a", "2026-10-31T00:00:00+00:00")
        self.assertEqual(len(row), 11)
        self.assertEqual(row[0], "")
        self.assertEqual(row[2], "222")
        self.assertEqual(row[10], "OWNER_CONFIRMED_SINGLE_CARD")

    def test_invalid_source_event_rejected(self):
        invalid = E.copy()
        invalid[0] = "not-a-review-key"
        with self.assertRaises(ValueError):
            m.mapping_row(invalid, "concept-a", "2026-10-31")

    def test_tag_suggestion_is_exact(self):
        card = {"tags": ["ALE::concept::c1", "maybe-c2", "ALE::concept::c3"]}
        self.assertEqual(m.suggested_concepts(card, ["c1", "c2"]), ["c1"])

    def test_question_preview_strips_html_script_and_control(self):
        text = m.local_question_preview(
            {"question": "<script>secret()</script><b>A &amp; B</b>\x1b[31m"})
        self.assertNotIn("secret", text)
        self.assertNotIn("<b>", text)
        self.assertNotIn("\x1b", text)
        self.assertIn("A & B", text)

    def test_missing_event_skipped(self):
        self.assertIsNone(m.latest_unlinked_review([["invalid"]], []))

    def test_map_never_promotes_sibling_cards(self):
        row = m.mapping_row(E, "c", "2026-10-31")
        self.assertEqual(row[5], "TESTS_THIS_CARD_DIRECTION_ONLY")

    def test_skip_persists_across_catalog_change(self):
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            catalog = ["concept-one", "concept-two"]
            self.assertEqual(m.skipped_for_catalog(base, catalog), set())
            m.remember_skip(base, catalog, 222)
            self.assertEqual(m.skipped_for_catalog(base, catalog), {"222"})
            self.assertIsNone(m.latest_unlinked_review([E], [], m.skipped_for_catalog(base, catalog)))
            self.assertIsNone(m.latest_unlinked_review([E], [], m.skipped_for_catalog(base, catalog + ["new-concept"])))

    def test_skip_files_are_private(self):
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            m.remember_skip(base, ["concept-one"], 222)
            self.assertEqual((base / m.SKIP_NAME).stat().st_mode & 0o777, 0o600)
            self.assertEqual(base.stat().st_mode & 0o777, 0o700)

    def test_skip_duplicate_is_idempotent(self):
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            m.remember_skip(base, ["c"], 222)
            m.remember_skip(base, ["c"], 222)
            self.assertEqual(m.skipped_for_catalog(base, ["c"]), {"222"})

    def test_no_concept_selected_rejected(self):
        with self.assertRaises(ValueError):
            m.mapping_row(E, "", "2026-10-31")


if __name__ == "__main__":
    unittest.main()
