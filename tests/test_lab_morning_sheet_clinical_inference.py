"""Clinical inference and applicability of source evidence; not physician signoff."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"


class LabInferenceConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.article = ARTICLE.read_text(encoding="utf-8")
        cls.sources = SOURCES.read_text(encoding="utf-8")

    def test_true_aml_vs_ex_vivo_competitors_not_prematurely_resolved(self):
        for cue in ("AML", "206.8", "90% blasts", "6.7", "7.8", "3.6",
                    "補鉀", "體內", "離體", "ECG", "不能把", "30 分鐘"):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.article)
        self.assertIn("PMC11462689", self.sources)

    def test_study_denominators_not_generalized_to_all_patients(self):
        for cue in ("66", "2,440", "1,576", "864", "597", "95%", "6%"):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.sources)
        self.assertIn("只選進", self.article)
        self.assertIn("不能搬來保證", self.article)

    def test_aki_in_other_evidence_not_misidentified_as_aml_course(self):
        self.assertIn("Cr", self.article)
        self.assertIn("AKI", self.article)
        self.assertIn("獨立教材", self.article)
        self.assertNotIn("Cr 1.16", self.article)
        self.assertIn("KDIGO 2012", self.sources)

    def test_hyperkalemia_safety_and_figure_rights(self):
        for cue in ("Figure 4", "Table 22", "低血糖", "UKKA", "原圖不在本站翻印"):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.sources)
        self.assertIn("ECG", self.article)
        self.assertIn("不可", self.article)


if __name__ == "__main__":
    unittest.main()
