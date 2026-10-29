"""Regression: a second public reading cannot silently duplicate a preserved original.

This exercises real publication metadata and injected future article additions.
It never rewrites the author's historical source bytes.
"""
import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from catalog import load_pages, validate_reading_version_collisions
from exam_archive import question_connections, question_key
from reading import primary_versions, render_article_index


class ReadingVersionCollisionContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = load_pages(ROOT)
        cls.original_name = "xiaoma-reading-20260720-diuretics.html"
        cls.integrated_name = "xiaoma-reading-diuretics-visual.html"

    def _pair(self, pages):
        original = next(p for p in pages if p["output"] == self.original_name)
        current = next(p for p in pages if p["output"] == self.integrated_name)
        return original, current

    def test_current_catalog_retains_original_but_has_single_primary_reading(self):
        validate_reading_version_collisions(self.pages)
        originals = primary_versions(self.pages)
        old, new = self._pair(self.pages)
        self.assertEqual(originals[old["output"]]["output"], new["output"])
        index = render_article_index(self.pages)
        self.assertEqual(index.count('href="' + new["output"] + '"'), 1)
        self.assertEqual(index.count('href="' + old["output"] + '"'), 1)
        key = question_key(new["related_exams"][0])
        linked = question_connections(self.pages, ROOT)[key]
        self.assertEqual([x["page"]["output"] for x in linked], [new["output"]])

    def test_missing_lineage_blocks_identical_title_even_without_exam_links(self):
        pages = copy.deepcopy(self.pages)
        original, current = self._pair(pages)
        del current["replaces_original"]
        original["related_exams"] = []
        current["related_exams"] = []
        with self.assertRaisesRegex(ValueError, "Undeclared original/integrated title collision"):
            validate_reading_version_collisions(pages)

    def test_spacing_and_punctuation_cannot_hide_duplicate_title(self):
        pages = copy.deepcopy(self.pages)
        _, current = self._pair(pages)
        del current["replaces_original"]
        current["title"] = "利尿效果不夠 為什麼下一步不一定是加量!"
        with self.assertRaisesRegex(ValueError, "Undeclared original/integrated title collision"):
            validate_reading_version_collisions(pages)

    def test_wrong_or_competing_lineage_is_rejected(self):
        for replacement in ("missing-original.html", "", ["unexpected"]):
            with self.subTest(replacement=replacement):
                pages = copy.deepcopy(self.pages)
                _, current = self._pair(pages)
                current["replaces_original"] = replacement
                with self.assertRaisesRegex(ValueError, "Invalid replaces_original"):
                    validate_reading_version_collisions(pages)
        pages = copy.deepcopy(self.pages)
        _, current = self._pair(pages)
        successor = copy.deepcopy(current)
        successor["output"] = "xiaoma-reading-diuretics-newer.html"
        successor["title"] = "另一個整合版本"
        pages.append(successor)
        with self.assertRaisesRegex(ValueError, "Multiple integrated successors"):
            validate_reading_version_collisions(pages)

    def test_related_exam_overlap_is_not_automatic_replacement(self):
        pages = copy.deepcopy(self.pages)
        _, current = self._pair(pages)
        independent = copy.deepcopy(current)
        independent["output"] = "other-angle-on-the-same-exam.html"
        independent["title"] = "不同臨床問題，同一道國考題"
        independent.pop("replaces_original")
        pages.append(independent)
        validate_reading_version_collisions(pages)
        key = question_key(current["related_exams"][0])
        # Different subjects may legitimately link the same national exam
        # without being collapsed, even when they share an exam identity.
        linked = question_connections(pages, ROOT)[key]
        self.assertEqual({x["page"]["output"] for x in linked},
                         {current["output"], independent["output"]})


if __name__ == "__main__":
    unittest.main()
