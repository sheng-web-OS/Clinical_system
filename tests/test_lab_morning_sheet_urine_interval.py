"""AKI interval example stays in the source annex, not grafted onto the AML case."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"
MATRIX = ROOT / "audit/2026-10-28-lab-morning-evidence-matrix.md"


class UrineOutputIntervalInference(unittest.TestCase):
    def test_kdigo_example_kept_as_separate_source_not_aml_observation(self):
        t = ARTICLE.read_text(encoding="utf-8")
        s = SOURCES.read_text(encoding="utf-8")
        m = MATRIX.read_text(encoding="utf-8")
        self.assertIn("8 小時總量不足以單獨證明連續 6 小時", s)
        self.assertIn("8 小時總量不足以單獨證明連續 6 小時", m)
        self.assertIn("不是此篇 AML 患者發生 AKI 的證據", s)
        self.assertNotIn("尿量 8 小時總計", t)
        self.assertNotIn("75 kg", t)


if __name__ == "__main__":
    unittest.main()
