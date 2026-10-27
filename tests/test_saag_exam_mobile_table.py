"""Layout regression: the source table is unchanged and the mobile view is readable.

A browser viewport test is still required before a production release.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-27-gi-liver-exam-trio.md"
STYLES = ROOT / "site/styles.css"

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
        cls.scoped = cls.css.split("/* 114-II Q22 SAAG: layout-only progressive enhancement.", 1)[1]

    def test_official_table_remains_source_accurate(self):
        self.assertIn("| 選項 | 血清 albumin | 腹水 albumin | 腹水 total protein | SAAG |", self.md)
        self.assertEqual(1, self.md.count("| 選項 | 血清 albumin"))
        found = re.findall(r"^\|\s*([ABCD])\s*\|([^\n]+)\|\s*$", self.md, re.M)
        self.assertEqual(4, len(found))
        for option, cells in found:
            self.assertEqual(ROWS[option], tuple(x.strip() for x in cells.split("|")))
            serum, ascites, _, saag = map(float, ROWS[option])
            self.assertAlmostEqual(serum - ascites, saag, places=5)
        self.assertIn("衍生值，非題目另行提供的實測項", self.md)
        self.assertIn("原卷與延伸參考", self.md)
        self.assertNotIn("本篇來源與版本界線", self.md)

    def test_css_is_scoped_to_this_article_and_does_not_duplicate_numbers(self):
        self.assertIn('article.reading-prose:has(a[href="xiaoma-exam-gi-liver-three-sources.html"]) > table', self.scoped)
        self.assertIn("@media(max-width:760px)", self.scoped)
        self.assertIn("grid-template-columns:repeat(2,minmax(0,1fr))", self.scoped)
        self.assertIn("overflow:visible", self.scoped)
        self.assertNotIn("overflow-x:auto", self.scoped)
        for position, title in enumerate((
            "血清 albumin", "腹水 albumin", "腹水 total protein", "SAAG（計算值）"
        ), start=2):
            self.assertIn(f'td:nth-child({position})::before{{content:"{title}"}}', self.scoped)
        self.assertNotIn("3.1", self.scoped, "Numeric source data must not be duplicated in CSS")
        self.assertEqual(1, self.css.count("/* 114-II Q22 SAAG: layout-only progressive enhancement."))


if __name__ == "__main__":
    unittest.main()
