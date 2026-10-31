"""Reader-level chronology, competing mechanisms, and source scope; not clinical signoff."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"


class LabMorningReaderInference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = ARTICLE.read_text(encoding="utf-8")
        cls.sources = SOURCES.read_text(encoding="utf-8")

    def test_patient_problem_precedes_competing_mechanisms_and_timelines(self):
        b = self.body
        self.assertLess(b.index("為什麼來急診"), b.index("真實機轉") if "真實機轉" in b else b.index("高血鉀與假性高血鉀"))
        self.assertLess(b.index("## 第二問"), b.index("## 第三問"))
        for cue in ("Hb 4.5", "206.8", "40 mEq", "A，12:00", "B，20:03",
                    "C，20:48", "D，23:37", "氣送管", "whole blood",
                    "plasma", "降鉀治療約 30 分鐘"):
            with self.subTest(cue=cue):
                self.assertIn(cue, b)
        self.assertIn("重抽是再取得一個數值", b)

    def test_distinct_mechanisms_need_different_discriminating_evidence(self):
        b = self.body
        for cue in ("體內", "離體", "機械", "紅血球", "白血球", "血小板",
                    "真正能回答疑問的新證據", "運送改變", "治療作用",
                    "ECG", "低血糖"):
            with self.subTest(cue=cue):
                self.assertIn(cue, b)
        self.assertIn("高血鉀", b)
        self.assertIn("假性高血鉀", b)

    def test_dual_source_figure_separates_case_and_denominators(self):
        figure = re.search(r'<figure id="lab-three-clocks".*?</figure>', self.body, re.S)
        self.assertIsNotNone(figure)
        for cue in ("AML 病例", "6.7", "7.8", "n=66",
                    "n=2,440", "864", "597", "第三項獨立研究"):
            with self.subTest(cue=cue):
                self.assertIn(cue, figure.group())

    def test_no_unrelated_aki_case_in_main_narrative(self):
        b = self.body
        self.assertIn("獨立教材", b)
        self.assertIn("AKI", b)
        self.assertNotIn("Cr 1.16", b)
        self.assertNotIn("75 kg", b)
        self.assertIn("PMC7673871", self.sources)
        self.assertIn("PMC11908522", self.sources)


if __name__ == "__main__":
    unittest.main()
