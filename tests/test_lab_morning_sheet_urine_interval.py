"""Guard KDIGO time-window inference in the evidence-first reader."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
ARTICLE=ROOT/"content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES=ROOT/"content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"
MATRIX=ROOT/"audit/2026-10-28-lab-morning-evidence-matrix.md"

class UrineOutputIntervalInference(unittest.TestCase):
    def test_aggregate_urine_8h_not_auto_six_hour_kdigo_window(self):
        t=ARTICLE.read_text(encoding="utf-8")
        s=SOURCES.read_text(encoding="utf-8")
        m=MATRIX.read_text(encoding="utf-8")
        self.assertIn("尿量 8 小時總計",t)
        self.assertIn("連續至少 6 小時",t)
        self.assertIn("不能僅由 8 小時總量證實連續 6 小時",s)
        self.assertIn("8 小時總量不足以單獨證明連續 6 小時",m)

if __name__=="__main__": unittest.main()
