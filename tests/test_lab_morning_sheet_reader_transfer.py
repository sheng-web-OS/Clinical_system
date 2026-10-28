"""Guard observed case→clinical inference bridges in the rewritten Lab lesson.

These static regression probes are not independent clinical review or reader
comprehension testing, and cannot substitute for the semantic release gate.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCE = ROOT / "content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"


class LabMorningReaderInference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.article = ARTICLE.read_text(encoding="utf-8")
        cls.sources = SOURCE.read_text(encoding="utf-8")

    def test_0900_observations_have_actual_decision_and_reversal(self):
        section = self.article.split("### 09:00：", 1)[1].split("### 第四筆", 1)[0]
        for cue in ("09:00 的新病例資料", "112/70", "75.6 kg", "75.0 kg",
                    "殘尿約 65 mL", "不反射性", "腎臟", "90/55", "四肢冰冷"):
            with self.subTest(cue=cue):
                self.assertIn(cue, section)
        self.assertNotIn("假設查房時發現", section)

    def test_figure_changes_clinical_state_not_just_time_labels(self):
        figure = re.search(r'<figure id="lab-three-clocks".*?</figure>',
                           self.article, re.S)
        self.assertIsNotNone(figure)
        figure = figure.group()
        for cue in ("A｜09:00", "B｜", "112/70", "90/55", "殘餘鬱血",
                    "低 forward perfusion", "立即升級", "並行", "待確認"):
            with self.subTest(cue=cue):
                self.assertIn(cue, figure)
        self.assertNotIn("<h3>分鐘｜", figure)
        self.assertNotIn("<h3>小時｜", figure)
        self.assertNotIn("<h3>天｜", figure)

    def test_non_k_non_cr_signal_changes_management_but_not_overclaims(self):
        section = self.article.split("### 第四筆", 1)[1].split("## 第三問", 1)[0]
        for cue in ("08:40", "PVCs", "Mg 1.5", "Loop diuretic",
                    "評估鎂補充", "AKI", "不能根據一個 Mg 1.5"):
            with self.subTest(cue=cue):
                self.assertIn(cue, section)
        self.assertIn("不等於已證明", section)
        self.assertIn("NHS Specialist Pharmacy Service", self.sources)
        self.assertIn("ESC ACVC/EHRA/HFA 2025", self.sources)

    def test_handoff_acknowledges_both_updated_decisions(self):
        handoff = self.article.split("回到原病例，今天的交班", 1)[1].split(
            "這樣的交班真正提供", 1
        )[0]
        for cue in ("09:00", "JVP", "08:40", "PVCs", "Mg 1.5"):
            with self.subTest(cue=cue):
                self.assertIn(cue, handoff)


if __name__ == "__main__":
    unittest.main()
