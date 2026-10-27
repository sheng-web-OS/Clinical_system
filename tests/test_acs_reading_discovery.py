"""Prevent the ACS deep lesson from being demoted to hidden navigation or metadata.

A Clinical OS article must be a real reading card for its publication day.
The examination lessons already have their own canonical identities.
This test checks metadata/discovery only, not whether the medicine is correct.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from reading import is_current_lesson, render_today_updates, render_article_index
from exam_archive import validate_exam_catalog

ARTICLE = "acs-reading.html"
EXAM_PAGES = (
    "xiaoma-exam-113-2-med3-acs-q6.html",
    "xiaoma-exam-114-2-med3-acs-q6-q9.html",
    "xiaoma-exam-115-2-med3-acs-q11-q13.html",
)


class ACSReadingDiscovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = json.loads((ROOT / "site/pages.json").read_text("utf-8"))
        cls.article = next(p for p in cls.pages if p["output"] == ARTICLE)

    def test_readable_clinical_article_is_not_hidden_as_navigation(self):
        self.assertEqual(self.article.get("kind"), "ai_integrated")
        self.assertEqual(self.article.get("collection"), "clinical-os")
        self.assertTrue(is_current_lesson(self.article))
        self.assertEqual(self.article.get("date"), "2026-10-27")

    def test_main_reading_reaches_today_and_atlas_without_fake_exam_cards(self):
        today = render_today_updates(self.pages, today="2026-10-27")
        atlas = render_article_index(self.pages)
        self.assertIn('href="' + ARTICLE + '"', today)
        self.assertIn('href="' + ARTICLE + '"', atlas)
        for exam in EXAM_PAGES:
            self.assertNotIn('href="' + exam + '"', today)
            self.assertIn('href="' + exam + '"', atlas)

    def test_acs_source_catalog_title_covers_all_recorded_exam_years(self):
        # Reader-facing source title must not hide the 115-year official cases.
        source = next(p for p in self.pages
                      if p["source"] == "content/xiaoma-internal-medicine/acs-exam-sources.md")
        title = source["title"]
        self.assertTrue(
            "113–115" in title or all(y in title for y in ("113", "114", "115")),
            "Source-page title must cover 113, 114, and 115 official exam years",
        )

    def test_seven_recorded_exam_crosslinks_stay_valid_after_rewriting_h2(self):
        related = self.article.get("related_exams", [])
        self.assertEqual(len(related), 7)  # six new official 113–115 + prior 108 Q76
        self.assertEqual(len({(q["year_roc"], q["sitting"], q["question_number"])
                              for q in related}), 7)
        validate_exam_catalog(self.pages, ROOT)

    def test_acs_exam_source_backlink_describes_twelve_chapter_lesson(self):
        # Regression: the source page must not describe the rewritten 12-section
        # article as the older four-chapter external course.
        source = (ROOT / "content/xiaoma-internal-medicine/acs-exam-sources.md").read_text("utf-8")
        self.assertIn("[ACS 十二章臨床整合教材](../clinical-os/acs.md)", source)
        self.assertNotIn("[ACS 四章整合入口]", source)


if __name__ == "__main__":
    unittest.main()
