"""Regressions for the overflowing daily list and articles lost from discovery."""
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from reading import render_article_index, render_today_updates, taipei_day, is_current_lesson, is_reference_page


class Links(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.links = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href"))


class DailyReadingIndex(unittest.TestCase):
    def setUp(self):
        self.pages = json.loads((ROOT / "site/pages.json").read_text("utf8"))

    def test_day_changes_at_taipei_midnight_not_host_midnight(self):
        self.assertEqual(taipei_day(datetime(2026, 10, 26, 15, 59, tzinfo=timezone.utc)), "2026-10-26")
        self.assertEqual(taipei_day(datetime(2026, 10, 26, 16, 0, tzinfo=timezone.utc)), "2026-10-27")

    def test_today_includes_revised_old_article_but_not_unchanged_old_articles(self):
        links = Links(render_today_updates(self.pages, "2026-10-27")).links
        self.assertIn("xiaoma-20261023-acid-base.html", links)
        self.assertIn("xiaoma-20261027-cticu-abg-cabg-lactate.html", links)
        self.assertNotIn("xiaoma-20261021-hypoxemia.html", links)
        self.assertNotIn("xiaoma-reading-20260712-heart-failure.html", links)
        self.assertNotIn("xiaoma-exam108-q46-chronic-cough.html", links)
        self.assertNotIn("xiaoma-reading-cholestasis-evidence-action.html", links)
        # The candidate catalog can add other same-day lessons (e.g. PE).
        # Derive expected cards from the current published manifest instead of freezing
        # an obsolete daily count when a release branch adds a real article.
        expected = {
            p["output"] for p in self.pages
            if is_current_lesson(p)
            and p.get("updated", p["date"]) == "2026-10-27"
        }
        self.assertEqual(set(links) - {"knowledge-atlas.html#article-index"}, expected)
        self.assertEqual(len(links), len(expected) + 1)

    def test_exam_compilation_and_source_reference_are_not_reading_cards(self):
        daily = Links(render_today_updates(self.pages, "2026-10-27")).links
        full_home = __import__("home").render_home(self.pages)
        exam_url = "xiaoma-20261027-gi-liver-national-exam-trio.html"
        source_url = "xiaoma-exam-gi-liver-three-sources.html"
        for url in (exam_url, source_url):
            with self.subTest(url=url):
                self.assertNotIn(url, daily)
                self.assertNotIn('href="' + url + '"', full_home)
        # Clinical lessons WITH linked practice questions must still be surfaced.
        self.assertIn("xiaoma-20261023-acid-base.html", daily)
        self.assertIn("xiaoma-20261027-pe-normotensive-shock.html", daily)
        atlas = render_article_index(self.pages)
        self.assertIn('href="' + exam_url + '"', atlas)
        self.assertIn("國考詳解與練習", atlas)
        self.assertNotIn('href="' + source_url + '"', atlas)
        # The source stays published and reachable from the teaching page.
        self.assertIn(source_url, {p["output"] for p in self.pages})

    def test_classification_comes_from_content_role_not_number_of_exam_links(self):
        normal = next(p for p in self.pages if p["output"] == "xiaoma-20261023-acid-base.html")
        exam_collection = next(p for p in self.pages if p["output"] == "xiaoma-20261027-gi-liver-national-exam-trio.html")
        self.assertTrue(normal.get("exam_questions"))
        self.assertTrue(is_current_lesson(normal))
        self.assertEqual("exam_compilation", exam_collection["kind"])
        self.assertFalse(is_current_lesson(exam_collection))

    def test_no_updates_does_not_fall_back_to_yesterdays_articles(self):
        # Test a truly empty date; a real 2026-10-28 article must appear today.
        # Choose one day beyond the latest content date to preserve the
        # no-yesterday-fallback invariant as the catalog continues to grow.
        last = max(
            p.get("updated", p["date"])
            for p in self.pages if is_current_lesson(p)
        )
        empty_day = (datetime.strptime(last, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertFalse(any(is_current_lesson(p) and p.get("updated", p["date"]) == empty_day
                             for p in self.pages))
        markup = render_today_updates(self.pages, empty_day)
        self.assertNotIn('class="lesson-card"', markup)
        self.assertIn('<p data-today-empty>今日尚無文章更新。</p>', markup)
        self.assertIn("knowledge-atlas.html#article-index", markup)

    def test_every_published_article_has_exactly_one_index_entry(self):
        links = Links(render_article_index(self.pages)).links
        expected = {p["output"] for p in self.pages if p.get("date") and not is_reference_page(p)}
        self.assertEqual(set(links), expected)
        self.assertEqual(len(links), len(expected))
        self.assertNotIn("xiaoma-sources.html", links)


if __name__ == "__main__":
    unittest.main()
