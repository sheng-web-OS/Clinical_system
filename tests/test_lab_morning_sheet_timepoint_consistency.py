"""Ensure exact AML A-D timing and distinct sample handling are preserved."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"


class LabMorningSheetTimepointContract(unittest.TestCase):
    def test_case_samples_keep_method_and_intervention_confounder(self):
        t = ARTICLE.read_text(encoding="utf-8")
        for cue in ("A，12:00", "B，20:03", "C，20:48", "D，23:37",
                    "3.0", "6.7", "7.8", "3.6", "plasma", "whole blood",
                    "氣送管", "步行", "30 分鐘", "分析儀", "治療作用"):
            with self.subTest(cue=cue):
                self.assertIn(cue, t)
        self.assertLess(t.index("B，20:03"), t.index("D，23:37"))
        self.assertIn("PMC11462689", SOURCES.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
