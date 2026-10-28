"""Raw HTML figure fidelity, revised for three distinct real evidence sources."""
from pathlib import Path
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
ARTICLE=ROOT/"content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"

class LabMorningSheetRawHtmlTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.article=ARTICLE.read_text(encoding="utf-8")

    def test_no_unrendered_markdown_inside_html_figure(self):
        figures=re.findall(r"<figure\\b[^>]*>.*?</figure>",self.article,re.I|re.S)
        self.assertTrue(figures)
        for fig in figures:
            self.assertNotRegex(fig,r"\\*\\*[^<>\\n]+?\\*\\*")

    def test_figure_states_separate_evidence_sources_not_synthetic_timelines(self):
        fig=re.search(r'<figure id="lab-three-clocks".*?</figure>',self.article,re.S)
        self.assertIsNotNone(fig)
        for cue in ("AML 病例","K 6.7","7.8","n=66","3.9","n=2,440","864","不同","並非同一位病人"):
            with self.subTest(cue=cue):
                self.assertIn(cue,fig.group())
        self.assertNotIn("Cr 1.16",fig.group())
        self.assertNotIn("09:00",fig.group())

if __name__=="__main__": unittest.main()
