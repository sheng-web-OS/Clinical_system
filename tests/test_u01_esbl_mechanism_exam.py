"""Regression guards for U01 official ESBL exam ID and enzyme-to-therapy bridge.

This is a deterministic editorial guard, NOT a medical review or proof of
clinical correctness. Source validation requires the original MOEX PDFs and
2026 IDSA AMR section, as recorded in the private sources-qa document.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "archive/pgy-antibiotics/u01/lesson.md"
SOURCES = ROOT / "archive/pgy-antibiotics/u01/sources-qa.md"


class U01ESBLMechanismAndExamTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lesson = LESSON.read_text(encoding="utf-8")
        cls.sources = SOURCES.read_text(encoding="utf-8")

    def test_exam_is_grounded_in_verifiable_year_and_number(self):
        section = self.lesson.split("## 真正的二階國考對題｜", 1)[1]
        section = section.split("## 值班交班", 1)[0]
        for cue in (
            "111 年第二次", "醫學（三）第 60 題", "官方標準答案 A",
            "cefotaxime", "aztreonam", "ertapenem",
            "t=Q", "t=S", "t=M",
        ):
            with self.subTest(cue=cue):
                self.assertIn(cue, section)

    def test_mechanism_has_limited_inference_instead_of_absolute_carbapenem_susceptibility(self):
        section = self.lesson.split("### 從酵素、抗生素靶點到臨床選藥：", 1)[1]
        section = section.split("### T0 的競爭方案", 1)[0]
        for cue in (
            "penicillin-binding proteins", "aztreonam", "carbapenem",
            "不是「必然」", "TMP-SMX", "不同抗藥性機轉",
            "MERINO", "164/187", "184/191",
        ):
            with self.subTest(cue=cue):
                self.assertIn(cue, section)
        self.assertNotIn("所有 ESBL 感染都必須使用 carbapenem。", section)

    def test_private_audit_discloses_official_pdf_and_evidence_limits(self):
        for cue in (
            "Q60", "官方試題", "標準答案",
            "MERINO", "NOT ORDER-READY", "藥師",
        ):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.sources)


if __name__ == "__main__":
    unittest.main()
