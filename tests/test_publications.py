import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "site"))
from catalog import load_pages


class PublicationBoundary(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ("site", "content/lessons", "archive"):
            (self.root / folder).mkdir(parents=True)
        (self.root / "content/example.md").write_text("# Public teaching\n")
        (self.root / "content/lessons/day.md").write_text("# Lesson\n")
        (self.root / "archive/private.md").write_text("private learner history")
        self.row = {"source": "content/example.md", "output": "example.html", "title": "Example", "subtitle": "Teaching"}

    def load(self, rows):
        (self.root / "site/pages.json").write_text(json.dumps(rows))
        return load_pages(self.root)

    def test_explicit_content_is_allowed(self):
        self.assertEqual(self.load([self.row])[0]["output"], "example.html")

    def test_private_archive_is_rejected(self):
        with self.assertRaises(ValueError):
            self.load([dict(self.row, source="archive/private.md")])

    def test_path_traversal_is_rejected(self):
        with self.assertRaises(ValueError):
            self.load([dict(self.row, source="content/../archive/private.md")])

    def test_symlink_to_private_source_is_rejected(self):
        external = self.root.parent / (self.root.name + "-private.md")
        external.write_text("private")
        self.addCleanup(external.unlink)
        (self.root / "content/leak.md").symlink_to(external)
        with self.assertRaises(ValueError):
            self.load([dict(self.row, source="content/leak.md")])

    def test_duplicate_output_is_rejected(self):
        with self.assertRaises(ValueError):
            self.load([self.row, self.row])

    def test_symlink_into_private_archive_is_rejected(self):
        (self.root / "content/leak.md").symlink_to(self.root / "archive/private.md")
        with self.assertRaises(ValueError):
            self.load([dict(self.row, source="content/leak.md")])

    def test_outside_output_is_rejected(self):
        with self.assertRaises(ValueError):
            self.load([dict(self.row, output="../private.html")])

    def test_lesson_without_review_is_rejected(self):
        with self.assertRaises(ValueError):
            self.load([dict(self.row, source="content/lessons/day.md", date="2026-10-21")])

    def test_invalid_lesson_date_is_rejected(self):
        with self.assertRaises(ValueError):
            self.load([dict(self.row, source="content/lessons/day.md", date="2026-02-30", review="author_source_check")])


if __name__ == "__main__":
    unittest.main()
