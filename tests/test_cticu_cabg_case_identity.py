"""Prevent article-order labels from being confused with the source's case numbers.

Wardhana's Patient 3 is the first teaching case in this article; Smyth's
euDKA patient is the second teaching case, not Wardhana's Patient 2.
"""
from pathlib import Path
import unittest

LESSON = (Path(__file__).resolve().parents[1] /
          "content/xiaoma-internal-medicine/lessons/2026-10-27-cticu-abg-cabg-lactate.md")


class CTICUCABGCaseIdentityTests(unittest.TestCase):
    def test_source_patient_numbers_distinct_from_article_order(self):
        text = LESSON.read_text("utf-8")
        self.assertIn("其中第三名是 **69 歲男性**", text)
        self.assertIn("Smyth 等人在 2021 年報告**另一名** 54 歲 CABG 病人", text)
        for misleading in (
            "第二名病人的完整",
            "替第一名填上",
            "第一例 lactate 14.8",
            "第二例正常 lactate",
        ):
            with self.subTest(misleading=misleading):
                self.assertNotIn(misleading, text)
        self.assertIn("本文第一個案例（原研究的第三名 CABG 病人）", text)
        self.assertIn("本文第二個案例（euDKA 病人）", text)


if __name__ == "__main__":
    unittest.main()
