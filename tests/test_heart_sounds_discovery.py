"""Regression: official heart-sounds question collections must not appear as daily reading.

The main clinical lesson stays discoverable; all 49 cross-disciplinary official
questions remain reachable by exam year and the article index's exam category.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from reading import is_current_lesson, render_article_index, render_today_updates

MAIN = "xiaoma-20261027-heart-sounds-structural-exam.html"
EXAM_29 = "xiaoma-20261027-heart-sounds-cross-discipline-exams.html"
EXAM_20 = "xiaoma-exam-heart-sounds-structural-cross-specialty-111-115.html"


class HeartSoundsDiscoveryRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        cls.pages = pages
        cls.by_output = {p["output"]: p for p in pages}

    def test_main_lesson_is_distinct_from_official_question_collections(self):
        self.assertTrue(is_current_lesson(self.by_output[MAIN]))
        for output, expected_count in ((EXAM_29, 29), (EXAM_20, 20)):
            with self.subTest(output=output):
                page = self.by_output[output]
                self.assertEqual(page["kind"], "exam_compilation")
                self.assertIn("官方真題", page["section"])
                self.assertEqual(len(page["exam_questions"]), expected_count)
                self.assertFalse(is_current_lesson(page))

    def test_daily_cards_only_promote_the_main_lesson(self):
        # Substantive revision moves the main lesson to its actual updated
        # date; official exam compilations must never be treated as daily lessons.
        main = self.by_output[MAIN]
        effective_date = main.get("updated", main["date"])
        for on_date in {main["date"], effective_date}:
            with self.subTest(on_date=on_date):
                html = render_today_updates(self.pages, today=on_date)
                if on_date == effective_date:
                    self.assertIn('href="' + MAIN + '"', html)
                else:
                    self.assertNotIn('href="' + MAIN + '"', html)
                self.assertNotIn('href="' + EXAM_29 + '"', html)
                self.assertNotIn('href="' + EXAM_20 + '"', html)

    def test_question_compilations_stay_in_exam_article_index(self):
        html = render_article_index(self.pages)
        self.assertIn("國考詳解與練習", html)
        self.assertIn('href="' + EXAM_29 + '"', html)
        self.assertIn('href="' + EXAM_20 + '"', html)

    def test_any_official_exam_section_cannot_be_a_daily_lesson(self):
        example = dict(self.by_output[MAIN], kind=None, section="心臟與循環・官方真題")
        self.assertFalse(is_current_lesson(example))


if __name__ == "__main__":
    unittest.main()
