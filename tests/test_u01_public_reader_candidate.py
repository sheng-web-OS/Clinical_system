"""Evidence-origin regression for the public U01 reader, not clinical validation."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-urosepsis-esbl-first-dose.md"
SOURCE = ROOT / "content/xiaoma-internal-medicine/urosepsis-esbl-first-dose-sources.md"


class U01PublicReaderCandidateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = READER.read_text(encoding="utf8")
        cls.sources = SOURCE.read_text(encoding="utf8")

    def test_real_cases_are_primary_and_independently_linked(self):
        for cue in ("28 歲女性", "81 歲日本女性", "83/44", "68/36",
                    "ceftriaxone", "meropenem", "PCN",
                    "https://www.mdpi.com/2079-6382/10/5/533",
                    "https://pmc.ncbi.nlm.nih.gov/articles/PMC8633641/"):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.text)

    def test_history_not_falsely_imputed_to_published_cases(self):
        for cue in ("原報告並無", "不能把它說成", "並非把兩個不同病人的紀錄拼在一起",
                    "不能單憑換藥後改善", "沒有對照組", "不提供"):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.text)
        self.assertNotIn("病例為人工合成", self.text)
        self.assertNotIn("10/28 07:15", self.text)

    def test_source_nav_exam_and_authoritative_guidelines(self):
        self.assertIn("../urosepsis-esbl-first-dose-sources.md", self.text)
        self.assertIn("111 年第二次", self.text)
        self.assertIn("醫學（三）第 60 題", self.text)
        for cue in ("IDSA 2026", "IDSA 2025", "SSC 2026",
                    "KDIGO 2012", "MERINO", "t=Q", "t=S", "t=M"):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.sources)
        self.assertTrue(SOURCE.exists())

    def test_no_order_ready_or_internal_editorial_metadata(self):
        for bad in ("Draft/HOLD", "PR #", "Issue #", "site/pages.json",
                    "meropenem 1 g q8h", "insulin-glucose", "500 mL bolus"):
            with self.subTest(bad=bad):
                self.assertNotIn(bad, self.text)


if __name__ == "__main__":
    unittest.main()
