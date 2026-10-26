"""Historical physician exam questions must be organized by exam year, not writing date."""
import copy
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from catalog import load_pages
from exam_archive import validate_exam_catalog, render_exam_archive, render_exam_year_teasers

class ExamArchiveContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = load_pages(ROOT)

    def test_108_first_stage_two_med3_includes_fourth_batch_without_duplicates(self):
        rows = [p for p in self.pages if p.get("exam") and
                (p["exam"]["year_roc"], p["exam"]["sitting"], p["exam"]["stage"], p["exam"]["subject"]) ==
                (108, 1, 2, "醫學（三）")]
        self.assertGreaterEqual(len(rows), 6)
        for p in rows:
            exam = p["exam"]
            self.assertEqual((exam["year_roc"], exam["sitting"], exam["stage"], exam["subject"]),
                             (108, 1, 2, "醫學（三）"))
            body = (ROOT / p["source"]).read_text("utf8")
            headings = {int(x) for x in re.findall(r"(?m)^## 第 (\d+) 題", body)}
            self.assertEqual(headings, set(exam["question_numbers"]))
        baseline = {key for key in validate_exam_catalog(self.pages)
                    if key[:4] == (108, 1, 2, "醫學（三）")}
        self.assertTrue({(108, 1, 2, "醫學（三）", q)
                         for q in (2, 8, 11, 12, 17, 22, 23, 25, 26, 27, 28, 61, 63, 75, 76, 78)}
                        .issubset(baseline),
                        "Previously published official question identities must remain")

    def test_all_published_exam_question_headings_match_deep_links(self):
        """Every official Q anchor must exist exactly once, across every exam year."""
        for page in self.pages:
            exam = page.get("exam")
            if not exam:
                continue
            body = (ROOT / page["source"]).read_text("utf8")
            headings = [int(n) for n in re.findall(r"(?m)^## 第\\s*(\\d+)\\s*題", body)]
            self.assertCountEqual(headings, exam["question_numbers"],
                                  "Broken #q-N reader anchors: " + page["source"])

    def test_year_archive_does_not_use_publication_year(self):
        index = render_exam_archive(self.pages)
        teaser = render_exam_year_teasers(self.pages)
        self.assertIn('id="year-108"', index)
        self.assertIn("108 年（2019）", index)
        self.assertIn("醫師第二階段", index)
        self.assertIn("醫學（三）", index)
        self.assertNotIn('id="year-2026"', index)
        self.assertIn('href="xiaoma-exams.html#year-108"', teaser)
        self.assertEqual(index.count('class="exam-lesson"'),
                         sum(bool(page.get("exam")) for page in self.pages))
        for q in (2, 8, 11, 12, 17, 22, 23, 25, 26, 27, 28, 61, 63, 75, 76, 78):
            self.assertIn("#q-" + str(q) + '"', index)

    def test_future_year_sorts_above_108_automatically(self):
        pages = copy.deepcopy(self.pages)
        newer = copy.deepcopy(next(p for p in pages if p.get("exam")))
        newer["exam"] = {**newer["exam"], "year_roc": 109, "question_numbers": [1]}
        newer["source"] = "content/example-future.md"
        newer["output"] = "example-future.html"
        pages.append(newer)
        html = render_exam_archive(pages)
        self.assertLess(html.index('id="year-109"'), html.index('id="year-108"'))
        self.assertIn("109 年（2020）", html)

    def test_question_collisions_fail_closed(self):
        pages = copy.deepcopy(self.pages)
        same = copy.deepcopy(next(p for p in pages if p.get("exam")))
        same["source"] = "content/other.md"
        same["output"] = "other.html"
        pages.append(same)
        with self.assertRaisesRegex(ValueError, "Duplicate exam question identity"):
            validate_exam_catalog(pages)

    def test_invalid_exam_identity_cannot_enter_archive(self):
        for key, val in (("year_roc", 2026), ("sitting", 0), ("stage", 3),
                         ("question_numbers", [0]), ("question_numbers", [2,2]), ("subject", "")):
            with self.subTest(key=key, value=val):
                pages = copy.deepcopy(self.pages)
                page = next(p for p in pages if p.get("exam"))
                page["exam"][key] = val
                with self.assertRaises(ValueError):
                    validate_exam_catalog(pages)

    def test_archive_has_a_public_page_and_keeps_old_links(self):
        outputs = {p["output"] for p in self.pages}
        for output in ("xiaoma-exams.html", "xiaoma-108a-cardiac-reasoning.html",
                       "xiaoma-exam108-renal-foundations.html", "xiaoma-exam108-renal-perfusion.html"):
            self.assertIn(output, outputs)
        markdown = (ROOT / "content/xiaoma-internal-medicine/exams/index.md").read_text("utf8")
        self.assertIn("XIAOMA_EXAM_ARCHIVE", markdown)
        portal = (ROOT / "content/xiaoma-internal-medicine/index.md").read_text("utf8")
        self.assertIn("XIAOMA_EXAM_YEAR_TEASERS", portal)
        self.assertIn("exams/index.md", portal)

if __name__=="__main__":
    unittest.main()
