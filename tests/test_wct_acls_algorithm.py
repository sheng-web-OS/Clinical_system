"""Contract: the public WCT lesson must display an actionable ACLS flow, not only a source link.

These are structural regression checks; visual and independent medical QA are separate.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-reading/integrated/2026-10-26-wct-acls-decision.md"
CSS = ROOT / "site/styles.css"
SOURCE = ROOT / "content/xiaoma-reading/arrhythmia-sources.md"

class TestWctAclsFigure(unittest.TestCase):
    def setUp(self):
        self.text = ARTICLE.read_text(encoding="utf8")
        self.css = CSS.read_text(encoding="utf8")

    def test_real_algorithm_is_in_article_before_advanced_discussion(self):
        marker = '<figure id="wct-acls-flowchart"'
        self.assertIn(marker, self.text)
        self.assertLess(self.text.index(marker), self.text.index("## Tachycardia 是不穩定的原因"))
        chart = self.text.split(marker, 1)[1].split("</figure>", 1)[0]
        self.assertIn("<figcaption>", chart)
        self.assertGreaterEqual(chart.count("acls-f-question"), 5)
        self.assertGreaterEqual(chart.count("acls-f-option"), 9)

    def test_critical_therapeutic_branches_survive(self):
        chart = self.text.split('<figure id="wct-acls-flowchart"', 1)[1].split("</figure>", 1)[0]
        for required in (
            "無脈搏", "cardiac arrest algorithm", "sustained polymorphic VT",
            "Unsynchronized high-energy shock", "Synchronized cardioversion",
            "Unstable pre-excited AF", "QRS ≥ 120 ms", "regular 且 monomorphic",
            "Class IIb", "不要給 adenosine", "procainamide", "ibutilide",
            "2025 AHA", "2023 ACC/AHA AF"
        ):
            with self.subTest(claim=required):
                self.assertIn(required, chart)
        self.assertIn("2025-Algorithms/Algorithm-ACLS-Tachycardia-250514.pdf", chart)

    def test_not_rehosting_copyrighted_aha_chart(self):
        chart = self.text.split('<figure id="wct-acls-flowchart"', 1)[1].split("</figure>", 1)[0]
        self.assertIn("不是 AHA 官方流程圖", chart)
        self.assertNotRegex(chart, r'<img[^>]+(?:heart\.org|Algorithm-ACLS)')
        self.assertIn("ECC 圖表再利用規則", SOURCE.read_text(encoding="utf8"))

    def test_mobile_branches_stack(self):
        self.assertIn(".acls-f-pair{grid-template-columns:minmax(0,1fr)", self.css)
        self.assertIn(".acls-f-option{min-width:0", self.css)
        self.assertIn(".acls-flowchart-body{padding:", self.css)

if __name__ == "__main__":
    unittest.main()
