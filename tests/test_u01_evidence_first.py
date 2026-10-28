"""Guard evidence-first ESBL reader provenance; this is not clinical QA."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-urosepsis-esbl-first-dose.md"
SOURCE = ROOT / "content/xiaoma-internal-medicine/urosepsis-esbl-first-dose-sources.md"

class EvidenceFirstUrosepsisTest(unittest.TestCase):
    def test_original_case_and_trial_are_main_evidence(self):
        text = READER.read_text(encoding="utf-8")
        before_exercise = text.split("### 反事實練習｜", 1)[0]
        for cue in ("83/44", "ceftriaxone", ">64", "<0.25",
                    "MERINO", "23/187", "7/191", "IDSA 2025", "IDSA 2026"):
            with self.subTest(cue=cue):
                self.assertIn(cue, before_exercise)
        self.assertIn("並非發表病例", text)
    def test_synthetic_order_sheet_does_not_return(self):
        text = READER.read_text(encoding="utf-8")
        for cue in ("第一劑醫囑草案", "## 值班交班，", "合成練習 A｜",
                    "### T+48｜", "### T+72｜"):
            with self.subTest(cue=cue):
                self.assertNotIn(cue, text)
        self.assertIn("不提供可直接開立", text)
        self.assertIn("../urosepsis-esbl-first-dose-sources.md", text)
    def test_guideline_methods_and_ni_hypothesis_are_distinguished(self):
        reader = READER.read_text(encoding="utf-8")
        source = SOURCE.read_text(encoding="utf-8")
        # The 2025 cUTI guideline used GRADE, but 2026 AMR guidance did not;
        # do not turn a definitive AST list into an empiric first-dose order.
        for cue in ("GRADE", "未使用 GRADE", "empiric", "definitive", "2025 cUTI", "2026 AMR"):
            with self.subTest(cue=cue):
                self.assertIn(cue, reader)
        for cue in ("5 個百分點", "14.5", "P=.90", "23/187", "7/191"):
            with self.subTest(cue=cue):
                self.assertIn(cue, reader)
        self.assertIn("未能證成", reader)
        self.assertIn("未使用 GRADE", source)
        self.assertIn("noninferiority", source)

    def test_provenance_lives_in_source_page(self):
        source = SOURCE.read_text(encoding="utf-8")
        for cue in ("PMC8633641", "MERINO", "IDSA 2026", "當院"):
            self.assertIn(cue, source)

if __name__ == "__main__":
    unittest.main()
