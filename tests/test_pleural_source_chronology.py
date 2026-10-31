"""Regressions for PR188's observed synthetic-case/source-timing escape.

These only verify documentary invariants; they do not grant medical approval.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "archive/xiaoma-internal-medicine/drafts/2026-10-28-pleural-effusion-decision.md"


class PleuralSourceChronologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DRAFT.read_text(encoding="utf-8")
        cls.maxDiff = 200

    def test_main_case_is_published_56m_not_composite(self):
        opening = self.text.split("## 02")[0]
        self.assertIn("56 歲", opening)
        self.assertIn("10.7759/cureus.52986", opening)
        self.assertNotIn("本文以合成連續病例", opening)
        self.assertNotIn("61 歲男性", self.text)
        self.assertNotIn("74 歲女性", self.text)

    def test_original_table1_does_not_backfill_missing_ph(self):
        match = re.search(r"<!-- PLEURAL_CASE_TABLE:START -->(.*?)<!-- PLEURAL_CASE_TABLE:END -->",
                          self.text, re.S)
        self.assertIsNotNone(match, "Original observation table must be explicit")
        table = match.group(1)
        self.assertRegex(table, r"\|\s*胸水 pH\s*\|\s*未報告\s*\|\s*7\.42\s*\|")
        self.assertRegex(table, r"\|\s*胸水 LDH.*?\|\s*1,?254\s*\|\s*607\s*\|")
        self.assertRegex(table, r"\|\s*胸水 glucose.*?\|\s*71\s*\|\s*84\s*\|")
        self.assertIn("Day 3", table)
        self.assertIn("Day 5", table)

    def test_ph_729_is_separate_counterfactual(self):
        self.assertIn("獨立假想反事實", self.text)
        self.assertIn("不是這位 56 歲男性", self.text)
        self.assertNotIn("現在給男性病人新的結果", self.text)

    def test_original_caption_disagreement_not_silently_fixed(self):
        self.assertIn("Figure 2B", self.text)
        self.assertIn("Day 2", self.text)
        self.assertIn("Table 1", self.text)
        self.assertIn("Day 3", self.text)
        self.assertIn("原文內部", self.text)

    def test_figure_compares_symptoms_with_pleural_space(self):
        self.assertIn('id="pleural-case-evidence"', self.text)
        self.assertIn("症狀改善", self.text)
        self.assertIn("胸水增大", self.text)
        self.assertIn("不是介入療效的因果證明", self.text)

    def test_safety_and_official_identities_remain(self):
        for phrase in ("安全", "類風濕", "惡性", "pseudoexudate", "自編遷移題"):
            self.assertIn(phrase, self.text)
        for ident in ("112 年第一次", "114 年第一次", "115 年第二次"):
            self.assertIn(ident, self.text)
        self.assertNotIn("官方 PDF 本輪尚未成功重新逐頁開啟", self.text)


if __name__ == "__main__":
    unittest.main()
