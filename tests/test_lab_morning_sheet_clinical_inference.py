"""Guard the synthetic case's calculations and key clinical inference boundaries.

These content fixtures detect regression; they do NOT certify medical safety,
guideline conformance, source rights or independent paragraph review.
"""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"


class LabInferenceConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.article = ARTICLE.read_text(encoding="utf-8")
        cls.sources = SOURCES.read_text(encoding="utf-8")

    def test_four_timepoints_and_units(self):
        row = next(line for line in self.article.splitlines()
                   if line.startswith("| Creatinine（mg/dL）"))
        self.assertEqual(re.findall(r"(?<!\d)1\.\d{2}(?!\d)", row),
                         ["1.05", "1.16", "1.68", "1.69"])
        self.assertIn("10/28 07:15 重新採檢", self.article)

    def test_aki_creatinine_change_is_stated_and_correct(self):
        self.assertGreaterEqual(1.68 - 1.16, 0.3)
        self.assertIn("48 小時內增加至少 0.3 mg/dL", self.article)
        self.assertIn("尿量 240 mL/8h", self.sources)

    def test_same_timepoint_ag_is_calculated_not_inferred_as_normal(self):
        self.assertIn("133 − (100 + 20) = 13 mmol/L", self.article)
        self.assertIn("沒有 albumin", self.article)
        self.assertIn("不是另一項實測", self.article)
        self.assertIn("不能由 AG 13", self.article)

    def test_moderate_hyperkalemia_safety(self):
        self.assertIn("moderate hyperkalaemia", self.article)
        self.assertIn("K 6.0–6.4 mmol/L", self.article)
        self.assertIn("正常", self.article)
        self.assertIn("低血糖與反彈", self.article)
        self.assertIn("2C", self.sources)
        self.assertIn("UKKA", self.sources)

    def test_staged_evidence_and_rights_not_falsely_certified(self):
        self.assertIn("KDIGO 2012 原表／原圖", self.sources)
        self.assertIn("未完整審閱 180 頁", self.sources)
        self.assertIn("原始圖表已完整目視驗收", self.sources)
        self.assertIn("合成教學情境", self.article)


if __name__ == "__main__":
    unittest.main()
