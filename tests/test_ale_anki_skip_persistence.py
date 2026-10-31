"""CI-discoverable regression for owner-selected persistent skips, with no Anki/Drive I/O."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_anki_concept_map import latest_unlinked_review, remember_skip, skipped_for_catalog

REVIEW = ["anki-revlog:12345:222", "2026-10-31T00:00:00Z", "222", "333",
          "", "1", "UNKNOWN", "NOT_COLLECTED", "", "NOT_DIAGNOSED",
          "", "12345", "SYNCED_READ_ONLY", "2026-10-31T00:00:02Z"]


class SkipPersistenceIntegration(unittest.TestCase):
    def test_user_skip_survives_concept_catalog_rename_and_extension(self):
        with tempfile.TemporaryDirectory() as home:
            base = Path(home)
            remember_skip(base, ["concept-one"], 222)
            self.assertEqual(skipped_for_catalog(base, ["renamed", "new-concept"]), {"222"})
            self.assertIsNone(latest_unlinked_review(
                [REVIEW], [], skipped_for_catalog(base, ["renamed", "new-concept"])))
            self.assertEqual((base / "concept_map_skips.json").stat().st_mode & 0o777, 0o600)

    def test_corrupt_skip_entry_never_silently_unskips(self):
        with tempfile.TemporaryDirectory() as home:
            base = Path(home)
            remember_skip(base, ["concept-one"], 222)
            path = base / "concept_map_skips.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["skipped_cards"] = ["222", 999]
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(RuntimeError):
                skipped_for_catalog(base, ["catalog-updated"])


if __name__ == "__main__":
    unittest.main()
