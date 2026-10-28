"""Regression: the morning Lab sheet contains four sampling timepoints, not three."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"


class LabMorningSheetTimepointContract(unittest.TestCase):
    def test_reader_and_source_count_the_same_four_sampling_times(self):
        article = ARTICLE.read_text(encoding="utf-8")
        source = SOURCES.read_text(encoding="utf-8")
        header = next(line for line in article.splitlines()
                      if line.startswith("| 項目（單位） |"))
        cells = [part.strip() for part in header.strip().strip("|").split("|")]
        self.assertEqual(len(cells) - 1, 4,
                         "The case table must retain all four sampling timestamps")
        self.assertIn("四時點", source,
                      "The source page must describe the four-timepoint synthetic case")
        self.assertIn("四時點", article,
                      "The reader's provenance paragraph must agree with the table")
        self.assertNotIn("三時間點患者數值", article,
                         "Old three-timepoint provenance mislabels the four-column case")


if __name__ == "__main__":
    unittest.main()
