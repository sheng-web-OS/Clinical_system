"""U01 public reader candidate must preserve safety and source navigation.

These are structural guardrails, not a substitute for clinical or independent
semantic review, and do not imply publication.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-urosepsis-esbl-first-dose.md"
SOURCE = ROOT / "content/xiaoma-internal-medicine/urosepsis-esbl-first-dose-sources.md"


class U01PublicReaderCandidateTest(unittest.TestCase):
    def test_reader_honors_patient_and_medication_boundary(self):
        s = READER.read_text(encoding="utf-8")
        for cue in (
            "病例為人工合成", "尚不足以單憑兩筆數值確認 KDIGO AKI",
            "MAP 約 68 mmHg", "meropenem", "疑似", "當院",
            "藥師", "無法", "第一劑",
        ):
            with self.subTest(cue=cue):
                self.assertIn(cue, s)
        for internal in ("Draft/HOLD", "PR #", "Issue #", "site/pages.json", "原始 Figure/表註腳對照"):
            with self.subTest(internal=internal):
                self.assertNotIn(internal, s)

    def test_source_nav_and_identity(self):
        text = READER.read_text(encoding="utf-8")
        self.assertIn("../urosepsis-esbl-first-dose-sources.md", text)
        self.assertIn("111 年第二次", text)
        self.assertIn("醫學（三）第 60 題", text)
        sources = SOURCE.read_text(encoding="utf-8")
        for cue in ("IDSA 2026", "IDSA 2025", "SSC", "KDIGO", "t=Q", "t=S", "t=M"):
            with self.subTest(cue=cue):
                self.assertIn(cue, sources)
        self.assertTrue((READER.parent / "../urosepsis-esbl-first-dose-sources.md").resolve().exists())


if __name__ == "__main__":
    unittest.main()
