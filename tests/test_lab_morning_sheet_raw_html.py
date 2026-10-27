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

    def test_figure_encodes_case_specific_parallel_decisions(self):
        """Avoid generic three-card figures that hide the case's conflicting signals."""
        article = ARTICLE.read_text(encoding="utf-8")
        match = re.search(r'<figure id="lab-three-clocks".*?</figure>', article, re.S)
        self.assertIsNotNone(match, "The original figure anchor must remain stable")
        figure = match.group(0)
        for cue in ("6.3", "4.9", "1.16", "1.69", "240", "0.4", "並行", "待確認"):
            with self.subTest(cue=cue):
                self.assertIn(cue, figure, "Figure must encode measured vs uncertain evidence and parallel actions")
        self.assertLess(article.index("| 項目（單位） |"), match.start(),
                        "Introduce the case and measurements before the visual comparison")

    def test_source_page_describes_case_figure_not_generic_cards(self):
        """Figure provenance must match the exact reader-facing case comparison."""
        source = (ROOT / "content/xiaoma-internal-medicine/lab-morning-sheet-sources.md").read_text(encoding="utf-8")
        section = source.split("## 6. 圖表的身分", 1)[1]
        for cue in ("6.3", "4.9", "1.69", "並行", "合成", "採檢"):
            with self.subTest(cue=cue):
                self.assertIn(cue, section, "Source locator must explain the actual figure and its inference limit")



if __name__ == "__main__":
    unittest.main()
