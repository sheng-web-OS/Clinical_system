"""Regression: an 8-hour average alone does not establish KDIGO's six-hour oliguria window.

This is a targeted inferential consistency fixture, not independent medical sign-off.
The source is KDIGO 2012 AKI guideline, chapter 2.1/Table 2 (printed p.19).
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"
MATRIX = ROOT / "audit/2026-10-28-lab-morning-evidence-matrix.md"


class UrineOutputIntervalInference(unittest.TestCase):
    def test_eight_hour_average_does_not_certify_six_hour_window(self):
        article = ARTICLE.read_text(encoding="utf-8")
        sources = SOURCES.read_text(encoding="utf-8")
        matrix = MATRIX.read_text(encoding="utf-8")
        self.assertIn("8 小時平均值不能單獨證實連續 6 小時的尿量門檻", article)
        self.assertIn("必須核對分時尿量", article)
        self.assertIn("不能僅由 8 小時總量證實連續 6 小時的門檻", sources)
        self.assertIn("8 小時總量不足以單獨證明連續 6 小時", matrix)


if __name__ == "__main__":
    unittest.main()
