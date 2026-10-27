"""Reader-first contract for the GI/liver three-question teaching lesson.

This is a structural check. Clinical interpretation still requires EPQC review.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSON = "content/xiaoma-internal-medicine/lessons/2026-10-27-gi-liver-exam-trio.md"


class GiLiverReaderEntryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.markdown = (ROOT / LESSON).read_text(encoding="utf-8")
        cls.page = next(
            p for p in json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
            if p["source"] == LESSON
        )

    def test_reader_deck_explains_clinical_purpose_not_exam_bookkeeping(self):
        subtitle = self.page["subtitle"]
        self.assertNotIn("Q1 ×", subtitle)
        self.assertNotIn("Q22 ×", subtitle)
        for term in ("ALP", "Child–Pugh", "SAAG"):
            self.assertIn(term, subtitle)

    def test_opening_starts_with_medicine_not_repeated_exam_inventory(self):
        opening = self.markdown.split("## 112 年第一次", 1)[0]
        self.assertNotIn("112 年第一次 Q1、114 年第一次", opening)
        self.assertNotIn("這三題不應整理成", opening)
        self.assertNotIn("官方更正答案與臨床推理", opening)
        for clinical_value in ("病因", "預後", "腹水", "門脈高壓"):
            self.assertIn(clinical_value, opening)

    def test_question_identities_and_answer_material_remain_present(self):
        self.assertEqual(
            [(112, 1, 1), (114, 1, 22), (114, 2, 22)],
            [(q["year_roc"], q["sitting"], q["question_number"])
             for q in self.page["exam_questions"]]
        )
        self.assertEqual(3, self.markdown.count("<details><summary>完成作答後"))
        self.assertEqual(3, self.markdown.count("**官方答案 D（未更正）。**"))
        self.assertEqual(3, self.markdown.count("[官方更正答案表]("))
        self.assertIn("exam-gi-liver-three-sources.md", self.markdown)


if __name__ == "__main__":
    unittest.main()
