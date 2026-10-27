"""Regression for the real 2026-10-27 Sepsis post-publish navigation failure.

Reader-facing lesson belongs in 今日更新／正在讀. The six-question
compilation belongs to official-exam navigation and source provenance to citations.
Does not modify clinical text or editorial release receipts.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from reading import is_current_lesson, is_reference_page, render_today_updates
from home import render_home
from build import render_reader

ARTICLE = "clinical-sepsis-infection-to-shock.html"
EXAMS = "xiaoma-exam-sepsis-112-114-five-questions.html"
PROVENANCE = "clinical-sepsis-evidence.html"


class SepsisReaderRoleRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        cls.by_output = {p["output"]: p for p in cls.pages}

    def test_reading_roles_are_explicit_and_mutually_exclusive(self):
        article = self.by_output[ARTICLE]
        exams = self.by_output[EXAMS]
        provenance = self.by_output[PROVENANCE]
        self.assertEqual(article.get("kind"), "ai_integrated")
        self.assertEqual(exams.get("kind"), "exam_compilation")
        self.assertEqual(provenance.get("kind"), "source_reference")
        self.assertTrue(is_current_lesson(article))
        self.assertFalse(is_current_lesson(exams))
        self.assertFalse(is_current_lesson(provenance))
        self.assertTrue(is_reference_page(provenance))
        self.assertNotEqual(article["source"], exams["source"])

    def test_today_reading_promotes_main_lesson_not_exam_metadata(self):
        daily = render_today_updates(self.pages, today="2026-10-27")
        self.assertIn('href="' + ARTICLE + '"', daily)
        self.assertNotIn('href="' + EXAMS + '"', daily)
        self.assertNotIn('href="' + PROVENANCE + '"', daily)
        self.assertIn("Sepsis：感染如何變成器官衰竭？", daily)

    def test_home_has_exactly_one_main_and_no_exam_or_provenance_cards(self):
        home = render_home(self.pages)
        self.assertEqual(home.count('href="' + ARTICLE + '"'), 1)
        self.assertNotIn('href="' + EXAMS + '"', home)
        self.assertNotIn('href="' + PROVENANCE + '"', home)

    def test_exam_compilation_has_no_fabricated_lesson_number(self):
        exam = self.by_output[EXAMS]
        rendered = render_reader(exam, "<p>Six genuine official questions</p>", [])
        self.assertIn('<p class="reader-kicker">感染與重症・官方真題</p>', rendered)
        self.assertNotIn('官方真題　 /　', rendered)
        self.assertIn('本頁導覽', rendered)


if __name__ == "__main__":
    unittest.main()
