"""Regression tests for source-derived manuscript status and release boundaries."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_corpus_inventory import inspect_inventory, INTAKE


class CorpusInventoryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for d in ("site", "archive/xiaoma-reading/intake",
                  "content/xiaoma-reading/originals"):
            (self.root / d).mkdir(parents=True, exist_ok=True)
        self.source = "content/xiaoma-reading/originals/2026-07-12-test.md"
        (self.root / self.source).write_text("# Actual full text", encoding="utf8")
        self.status = "imported → " + chr(96) + self.source + chr(96)
        self.published = {
            "source": self.source,
            "output": "xiaoma-test.html",
            "title": "A recovered test article",
            "subtitle": "Test",
            "kind": "historical_original",
            "review": "source_recovery_only",
            "date": "2026-07-12",
            "source_sha256": hashlib.sha256(
                (self.root / self.source).read_bytes()).hexdigest(),
        }
        self.write_ledger(self.status)
        self.write_pages([self.published])

    def write_ledger(self, status):
        ledger = "\n".join([
            "# Intake", "| 日期（文章自述） | 原始題名 | 系列／來源標籤 | 內容移轉 |",
            "|---|---|---|---|",
            "| 2026-07-12 | Test essay | Xiaoma | " + status + " |",
            "| 2026-07-13 | Untouched note | Other | conversation_only |",
            "", "## Later editorial notes", "Do not count this sentence.",
        ])
        (self.root / INTAKE).write_text(ledger, encoding="utf8")

    def write_pages(self, pages):
        (self.root / "site/pages.json").write_text(
            json.dumps(pages, ensure_ascii=False), encoding="utf8")

    def test_counts_are_derived_from_actual_files_and_manifest(self):
        report, errors = inspect_inventory(self.root)
        self.assertEqual(errors, [])
        self.assertEqual((report["intake_total"], report["intake_imported"],
                          report["intake_conversation_only"], report["original_files"],
                          report["published_originals"]), (2, 1, 1, 1, 1))

    def test_imported_does_not_mean_published(self):
        self.write_pages([{"source": "content/xiaoma-reading/originals/2026-07-12-test.md",
                           "output": "reader.html", "title": "Draft", "subtitle": "Test"}])
        report, errors = inspect_inventory(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(report["published_originals"], 0)
        self.assertEqual(report["imported_unpublished_paths"], [self.source])

    def test_missing_file_fails(self):
        (self.root / self.source).unlink()
        report, errors = inspect_inventory(self.root)
        self.assertIsNone(report)
        self.assertTrue(errors)

    def test_private_source_snapshot_is_counted_but_not_published(self):
        snapshot = "archive/xiaoma-reading/intake/2026-07-16-acute-af.md"
        (self.root / snapshot).write_text("User-provided full text", encoding="utf8")
        self.write_ledger("**source_snapshot_archived** → " + chr(96) +
                          snapshot + chr(96) + "；clinical review pending")
        report, errors = inspect_inventory(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(report["intake_source_snapshots"], 1)
        self.assertEqual(report["source_snapshot_paths"], [snapshot])
        self.assertEqual(report["intake_imported"], 0)
        self.assertEqual(report["published_originals"], 1)

    def test_missing_private_source_snapshot_fails(self):
        self.write_ledger("source_snapshot_archived → " + chr(96) +
                          "archive/xiaoma-reading/intake/missing.md" + chr(96))
        report, errors = inspect_inventory(self.root)
        self.assertTrue(any("Missing or escaped source" in err for err in errors))

    def test_unknown_status_not_silently_counted(self):
        self.write_ledger("reviewed_by_ai_and_published")
        report, errors = inspect_inventory(self.root)
        self.assertTrue(any("Unknown intake" in err for err in errors))

    def test_unapproved_text_change_fails_fingerprint(self):
        (self.root / self.source).write_text("# Replaced", encoding="utf8")
        report, errors = inspect_inventory(self.root)
        self.assertIsNone(report)
        self.assertTrue(any("Recovered original changed" in err for err in errors))

    def test_historical_checkpoint_is_not_current_status(self):
        stale = self.root / "archive/xiaoma-reading/recovery-worklist-20261021.json"
        stale.write_text('{"verified_full_originals": []}', encoding="utf8")
        report, errors = inspect_inventory(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(report["original_files"], 1)


if __name__ == "__main__":
    unittest.main()
