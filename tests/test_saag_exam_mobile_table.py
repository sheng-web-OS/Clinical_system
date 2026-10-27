"""Guard the 114-II Q22 values and the one-table mobile presentation.

The semantic/static checks do not substitute for a rendered iPhone viewport.
"""
from pathlib import Path
from html.parser import HTMLParser
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-27-gi-liver-exam-trio.md"
STYLES = ROOT / "site/styles.css"

HEADERS = ("血清 albumin", "腹水 albumin", "腹水 total protein", "SAAG")
ROWS = {
    "A": ("3.1", "2.1", "2.3", "1.0"),
    "B": ("4.3", "2.6", "3.0", "1.7"),
    "C": ("2.8", "2.0", "2.8", "0.8"),
    "D": ("2.8", "1.2", "2.0", "1.6"),
}


class SaagExamMobileTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.md = LESSON.read_text(encoding="utf-8")
        cls.css = STYLES.read_text(encoding="utf-8")
        cls.table = cls.md.split('<table class="saag-exam-table"', 1)[1].split("</table>", 1)[0]

    def test_single_table_has_original_measurements_and_correct_saag(self):
        self.assertEqual(1, self.md.count('<table class="saag-exam-table"'))
        self.assertEqual(5, len(re.findall(r'<th scope="col">', self.table)))
        self.assertEqual(4, len(re.findall(r'<th scope="row">', self.table)))
        self.assertEqual(16, len(re.findall(r'<td>', self.table)))
        for label, values in ROWS.items():
            row_match = re.search(r'<tr><th scope="row">' + label + r'</th>(.*?)</tr>', self.table, re.S)
            self.assertIsNotNone(row_match, f"Missing {label}")
            row = row_match.group(1)
            self.assertEqual(values, tuple(re.findall(r'<span class="saag-value">([0-9.]+)</span>', row)))
            self.assertEqual(HEADERS, tuple(re.findall(r'<span class="saag-mobile-label" aria-hidden="true">(.*?)</span>', row)))
            serum, ascitic, protein, saag = map(float, values)
            self.assertAlmostEqual(serum - ascitic, saag, places=5)
        self.assertIn("衍生值，非題目另行提供的實測項", self.md)

    def test_accessible_headers_and_mobile_labels_reuse_single_data_copy(self):
        self.assertIn('aria-label="四組原題測值及計算所得的 SAAG"', self.md)
        self.assertIn('scope="row"', self.table)
        self.assertIn('aria-hidden="true"', self.table)
        self.assertIn("原卷與延伸參考", self.md)
        self.assertNotIn("本篇來源與版本界線", self.md)
        self.assertNotIn("原始資料使用：考選部", self.md)

    def test_scoped_mobile_css_cards_do_not_require_sideways_scroll(self):
        start = self.css.index("/* The 114-II Q22 SAAG comparison")
        scoped = self.css[start:]
        for required in (
            ".reading-prose table.saag-exam-table",
            "grid-template-columns:repeat(2,minmax(0,1fr))",
            ".reading-prose .saag-mobile-label{display:block",
            ".reading-prose .saag-value{display:block",
            "max-width:100%",
            "overflow:visible",
        ):
            self.assertIn(required, scoped)
        self.assertNotIn("overflow-x:auto", scoped)
        self.assertEqual(1, self.css.count("/* The 114-II Q22 SAAG comparison"))


if __name__ == "__main__":
    unittest.main()
