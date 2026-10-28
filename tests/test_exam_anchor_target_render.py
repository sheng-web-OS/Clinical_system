"""Reader-target regression for 29+20 official heart-sounds exam links.

The archive may contain a syntactically valid href while the rendered article
omits its target span. In particular, Markdown **emphasis** in an exam heading
must not invalidate the canonical question anchor.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
import build
from exam_archive import question_anchor, render_exam_archive

SOURCES = {
    "content/xiaoma-internal-medicine/lessons/2026-10-27-heart-sounds-cross-discipline-exams.md": 29,
    "content/xiaoma-internal-medicine/exams/heart-sounds-cross-specialty-expanded-111-115.md": 20,
}


class ExamRenderedAnchorTargetRegression(unittest.TestCase):
    def test_all_49_year_archive_deep_links_have_real_reader_targets(self):
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        selected = [page for page in pages if page["source"] in SOURCES]
        self.assertEqual(len(selected), 2)
        archive = render_exam_archive(pages, ROOT)
        total = 0
        with tempfile.TemporaryDirectory() as temp_dir:
            # Render the actual reader through the production build function,
            # not a separately reimplemented Markdown-to-anchor approximation.
            with patch.object(build, "DIST", Path(temp_dir)):
                for page in selected:
                    self.assertEqual(len(page["exam_questions"]), SOURCES[page["source"]])
                    build.render(page["source"], page["output"], page["title"], page["subtitle"])
                    reader = (Path(temp_dir) / page["output"]).read_text(encoding="utf-8")
                    for question in page["exam_questions"]:
                        with self.subTest(page=page["output"], question=question["question_heading"]):
                            target = question_anchor(question)
                            self.assertEqual(reader.count('id="' + target + '"'), 1,
                                             "Published exam archive deep link has no unique reader target")
                            self.assertIn('href="' + page["output"] + '#' + target + '"', archive)
                            total += 1
        self.assertEqual(total, 49)

    def test_cross_page_canonical_question_identities_are_unique(self):
        """The old 29+46 combination duplicated 26 official exam identities.

        This guards the actual canonical metadata on both reader pages, not
        merely whether their URLs render. Historical 29+46 is a documented
        regression example, not a completed blinded clinical replay.
        """
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        selected = [page for page in pages if page["source"] in SOURCES]
        self.assertEqual(len(selected), 2)
        identities = [
            (question["year_roc"], question["sitting"],
             question["subject"], question["question_number"])
            for page in selected for question in page["exam_questions"]
        ]
        self.assertEqual(len(identities), 49)
        self.assertEqual(len(identities), len(set(identities)),
                         "Two reader pages repeat the same official exam identity")

        # Negative control: inserting one repeated question must be detectable.
        # This is a fixture-sensitivity check, not a real old-head CI RED.
        duplicated = identities + [identities[0]]
        self.assertLess(len(set(duplicated)), len(duplicated))

    def test_corrected_answer_emphasis_is_not_a_broken_target(self):
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        original = next(page for page in pages if page["source"] in SOURCES and
                        page["source"].endswith("2026-10-27-heart-sounds-cross-discipline-exams.md"))
        q9 = next(question for question in original["exam_questions"] if
                  (question["year_roc"], question["sitting"], question["subject"], question["question_number"])
                  == (115, 2, "醫學（五）", 9))
        self.assertIn("**標準答案更正為 B 或 D**", q9["question_heading"])
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(build, "DIST", Path(temp_dir)):
                build.render(original["source"], original["output"], original["title"], original["subtitle"])
            reader = (Path(temp_dir) / original["output"]).read_text(encoding="utf-8")
        self.assertEqual(reader.count('id="' + question_anchor(q9) + '"'), 1)


if __name__ == "__main__":
    unittest.main()
