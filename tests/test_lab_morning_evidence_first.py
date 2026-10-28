"""Source-identity regression for Lab Medicine 01: true case data vs study cohorts.

Prevents the old fabricated all-in-one patient from resurfacing as evidence.
Static checks do not establish medical safety or reader comprehension.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"


class LabEvidenceFirstIdentity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = ARTICLE.read_text(encoding="utf-8")
        cls.sources = SOURCES.read_text(encoding="utf-8")

    def test_real_case_sample_identity_and_treatment_confounding(self):
        for cue in ("AML", "206.8", "90% blasts", "12:00", "20:03", "20:48",
                    "23:37", "6.7", "7.8", "3.6", "Pneumatic tube",
                    "降鉀治療", "30 分鐘"):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.body)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC11462689/", self.body)
        self.assertIn("PMC11462689", self.sources)

    def test_cohort_denominators_and_selection_not_conflated(self):
        for cue in ("66", "399", "95%", "6%", "2,440", "1,576",
                    "864", "597", "當日", "重抽", "納排"):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.sources)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC7673871/", self.body)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC11908522/", self.body)

    def test_synthetic_case_no_longer_pretends_to_ground_treatment(self):
        self.assertIn("不同研究、不同病人", self.body)
        self.assertNotIn("舊版用一名 AI 設計的", self.body)
        self.assertNotIn("前一版用", self.body)
        self.assertNotIn("## 後段合成練習", self.body)
        self.assertIn("不提供選抽血項目或醫囑", self.body)

    def test_source_page_agrees_with_current_primary_evidence(self):
        for locator in ("PMC11462689", "PMC7673871", "PMC11908522"):
            with self.subTest(locator=locator):
                self.assertIn(locator, self.sources)
        self.assertIn("補充案例（非目前文章主故事）", self.sources)


if __name__ == "__main__":
    unittest.main()
