"""Evidence-first Lab Medicine 01 regression: sample identity, cohorts, AKI limits.

These assertions detect drift from original-source facts, not independent
medical sign-off or proof that a reader learned clinical reasoning.
"""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
ARTICLE=ROOT/"content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES=ROOT/"content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"

class LabInferenceConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.article=ARTICLE.read_text(encoding="utf-8")
        cls.sources=SOURCES.read_text(encoding="utf-8")

    def test_real_aml_sample_sequence_and_intervention(self):
        for cue in ("AML","A／12:00","B／20:03","C／20:48","D／23:37","12:00","20:03","20:48","23:37","6.7","7.8","3.6","氣送管","降鉀治療","30 分鐘"):
            with self.subTest(cue=cue):
                self.assertIn(cue,self.article)
        self.assertIn("PMC11462689",self.sources)

    def test_selection_denominators_not_treated_as_all_patients(self):
        for cue in ("66","2,440","1,576","864","597","95%","6%"):
            with self.subTest(cue=cue):
                self.assertIn(cue,self.sources)
        self.assertIn("不是所有",self.article)
        self.assertIn("不能搬到所有病房病人",self.article)

    def test_aki_creatinine_vs_cause_is_distinguished(self):
        for cue in ("KDIGO 2012","48 小時內","0.3 mg/dL","6 小時","病因"):
            with self.subTest(cue=cue):
                self.assertIn(cue,self.article)
        self.assertIn("8 小時總量不足以單獨證明連續 6 小時",self.sources)

    def test_high_potassium_source_rights_and_safety_limits(self):
        for cue in ("Figure 4","Table 22","低血糖","心電","UKKA"):
            with self.subTest(cue=cue):
                self.assertIn(cue,self.sources)
        self.assertIn("原圖不在本站翻印",self.sources)
        self.assertIn("不是",self.sources)
        self.assertNotIn("原始圖表已完整目視驗收",self.sources)
        self.assertIn("正常 ECG",self.article)

if __name__=="__main__": unittest.main()
