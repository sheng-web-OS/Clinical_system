"""Reader-facing conceptual bridges in the evidence-first Lab lesson.

These are source-identity and narrative-regression probes, not independent
medical review, blind reader transfer measurement or a publication waiver.
"""
from pathlib import Path
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
ARTICLE=ROOT/"content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES=ROOT/"content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"

class LabMorningReaderInference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.article=ARTICLE.read_text(encoding="utf-8")
        cls.sources=SOURCES.read_text(encoding="utf-8")

    def test_actual_sample_method_and_intervention_explained_before_study(self):
        body=self.article
        self.assertLess(body.index("## 第一問"),body.index("## 第二問"))
        self.assertLess(body.index("20:03"),body.index("## 第二問"))
        for cue in ("12:00","20:03","20:48","23:37","氣送管","步行",
                    "whole blood","plasma","降鉀治療約 30 分鐘"):
            with self.subTest(cue=cue):
                self.assertIn(cue,body)

    def test_figure_separates_case_report_and_distinct_denominators(self):
        figure=re.search(r'<figure id="lab-three-clocks".*?</figure>',
                         self.article,re.S)
        self.assertIsNotNone(figure)
        t=figure.group()
        for cue in ("AML 病例","6.7","7.8","n=66","n=2,440","864",
                    "第三項獨立研究"):
            with self.subTest(cue=cue):
                self.assertIn(cue,t)
        self.assertNotIn("09:00",t)

    def test_study_selection_not_transferred_to_high_risk_patient(self):
        body=self.article
        for cue in ("eGFR <60","血液惡性疾病","不能搬到所有病房病人",
                    "不能拿這個比例估計所有急診高鉀患者","ECG 正常","降鉀介入後"):
            with self.subTest(cue=cue):
                self.assertIn(cue,body)
        self.assertIn("PMC7673871",self.sources)
        self.assertIn("PMC11908522",self.sources)

    def test_non_potassium_panel_remains_differentiated_not_prescribed(self):
        last=self.article.split("## 第三問",1)[1]
        for cue in ("Serum total CO₂","Hb","platelet","Mg","BUN／Cr",
                    "沒有對應臨床症候群","不能編造"):
            with self.subTest(cue=cue):
                self.assertIn(cue,last)

if __name__=="__main__": unittest.main()
