"""Regression for the CABG case-based Figure 1 and its mobile transition."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-27-cticu-abg-cabg-lactate.md"


class CTICUCABGFigureRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lesson = LESSON.read_text("utf-8")
        start = cls.lesson.index('<figure id="cticu-measurement-layers"')
        end = cls.lesson.index("</figure>", start)
        cls.figure = cls.lesson[start:end + len("</figure>")]

    def test_old_four_cards_cannot_replace_case_evidence(self):
        self.assertNotIn("圖 1｜四個不能互換的觀察層次", self.lesson)
        self.assertIn("圖 1｜高 lactate 與高 ScvO₂ 並存", self.figure)
        self.assertIn("14.8", self.figure)
        self.assertIn("95%", self.figure)
        self.assertIn("血液每分鐘能送出多少氧？", self.figure)

    def test_one_transition_arrow_below_message(self):
        self.assertNotIn("↓　兩個數字不互相否定", self.figure)
        self.assertNotIn("共同缺的是因果證據　↓", self.figure)
        self.assertRegex(
            self.figure,
            r'兩個數字不互相否定；共同缺的是因果證據'
            r'<div aria-hidden="true"[^>]*>↓</div>',
        )

    def test_distinguish_observation_from_inference(self):
        self.assertIn("血中乳酸濃度｜實測", self.figure)
        self.assertIn("中心靜脈血氧飽和度｜實測", self.figure)
        self.assertIn("不能直接推出：", self.figure)
        self.assertIn("CaO₂ × CO → DO₂", self.figure)
        self.assertIn("不是</strong>已算出的病人數值", self.figure)


if __name__ == "__main__":
    unittest.main()
