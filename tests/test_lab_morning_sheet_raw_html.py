"""Regression: Markdown emphasis inside raw HTML figures is not parsed by mistune."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"


class LabMorningSheetRawHtmlTest(unittest.TestCase):
    def test_no_unrendered_markdown_bold_in_raw_figure(self):
        article = ARTICLE.read_text(encoding="utf-8")
        figures = re.findall(r"<figure\b[^>]*>.*?</figure>", article, re.I | re.S)
        self.assertTrue(figures, "Expected the teaching figure to exist")
        for figure in figures:
            self.assertNotRegex(
                figure,
                r"\*\*[^<>\n]+?\*\*",
                "Mistune leaves Markdown **bold** literal inside raw HTML figure; use <strong>.",
            )


if __name__ == "__main__":
    unittest.main()
