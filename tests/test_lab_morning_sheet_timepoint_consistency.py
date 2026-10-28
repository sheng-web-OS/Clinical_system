"""Timing/assay provenance of real AML case, not synthetic 4-timepoint ward data."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
ARTICLE=ROOT/"content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES=ROOT/"content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"

class LabMorningSheetTimepointContract(unittest.TestCase):
    def test_real_case_a_to_d_are_reported_with_method_not_conflated(self):
        t=ARTICLE.read_text(encoding="utf-8")
        for cue in ("Sample","12:00","20:03","20:48","23:37","Plasma","Pneumatic tube","步行","30 分鐘"):
            with self.subTest(cue=cue):
                self.assertIn(cue,t)
        self.assertNotIn("| 項目（單位） |",t)
        self.assertIn("PMC11462689",SOURCES.read_text(encoding="utf-8"))

if __name__=="__main__": unittest.main()
