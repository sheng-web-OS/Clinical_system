"""Regression contract: WCT/ACLS cannot bury its governing clinical algorithm in a footnote.

The test verifies visible structure and source linkage. It does not certify medical
truth, permissions for copying the AHA image, or actual device rendering.
"""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-reading/integrated/2026-10-26-wct-acls-decision.md"
SOURCES = ROOT / "content/xiaoma-reading/arrhythmia-sources.md"
STYLE = ROOT / "site/styles.css"
PAGES = ROOT / "site/pages.json"
SOURCE_KEY = "content/xiaoma-reading/integrated/2026-10-26-wct-acls-decision.md"


class ACLSPrimaryVisualTests(unittest.TestCase):
    def test_two_distinct_algorithms_have_right_sequence_and_sources(self):
        t = ARTICLE.read_text(encoding="utf8")
        shock = 'id="wct-acls-main-algorithm"'
        drugs = 'id="wct-acls-stable-wct-algorithm"'
        self.assertIn(shock, t)
        self.assertIn(drugs, t)
        self.assertLess(t.index(shock), t.index("## Tachycardia 是不穩定的原因"))
        self.assertLess(t.index(drugs), t.index("## Regular 與 monomorphic"))
        self.assertGreater(t.index(drugs), t.index("## 病人暫時 stable"))
        a = re.search(r'<figure id="wct-acls-main-algorithm".*?</figure>', t, re.S).group(0)
        b = re.search(r'<figure id="wct-acls-stable-wct-algorithm".*?</figure>', t, re.S).group(0)
        self.assertIn("圖 A｜什麼情況不能等確診", a)
        self.assertIn("圖 B｜Stable 之後", b)
        self.assertIn("Algorithm-ACLS-Tachycardia-250514.pdf", a)
        for chart in (a, b):
            self.assertIn('class="acls-desktop-graph"', chart)
            self.assertIn('class="acls-mobile-graph"', chart)
            self.assertIn("<figcaption>", chart)
            self.assertGreaterEqual(chart.count("marker-end="), 10)
            self.assertIn("NO", chart)
            self.assertIn("YES", chart)

    def test_shock_and_drug_safety_have_non_interchangeable_branches(self):
        t = ARTICLE.read_text(encoding="utf8")
        a = re.search(r'<figure id="wct-acls-main-algorithm".*?</figure>', t, re.S).group(0)
        b = re.search(r'<figure id="wct-acls-stable-wct-algorithm".*?</figure>', t, re.S).group(0)
        for term in ("有脈搏嗎", "polymorphic VT", "非同步高能量電擊",
                     "同步電復律", "unstable pre-excited AF", "暫時穩定"):
            with self.subTest(figure="shock", term=term):
                self.assertIn(term, a)
        for term in ("QRS ≥ 120 ms", "monomorphic", "adenosine", "Class IIb",
                     "procainamide", "ibutilide", "AV nodal blockers"):
            with self.subTest(figure="drug", term=term):
                self.assertIn(term, b)
        # Prevent the old single chart's hazardous mixing of shock and drug rules.
        self.assertNotIn("Class IIb", a)
        self.assertNotIn("unsynchronized high-energy", b)

    def test_source_url_agrees_with_published_visual_audit(self):
        rows = json.loads(PAGES.read_text(encoding="utf8"))
        row = next(x for x in rows if x["source"] == SOURCE_KEY)
        official_url = row["required_primary_visual"]["official_source_url"]
        audit = json.loads((ROOT / "audit/figure-gate.json").read_text(encoding="utf8"))
        review = audit["reviews"][SOURCE_KEY]
        figure = next(x for x in review["items"] if x["anchor"] == "wct-acls-main-algorithm")
        self.assertEqual(figure["original_source_url"], official_url)
        self.assertIn(official_url, ARTICLE.read_text(encoding="utf8"))
        self.assertIn(official_url, SOURCES.read_text(encoding="utf8"))

    def test_official_source_and_copyright_boundaries(self):
        s = SOURCES.read_text(encoding="utf8")
        for text in ("Guidelines", "copyright", "AHA", "link_or_original_only"):
            self.assertIn(text.lower(), s.lower())
        rows = json.loads(PAGES.read_text(encoding="utf8"))
        row = next(x for x in rows if x["source"] == SOURCE_KEY)
        self.assertEqual(row["required_primary_visual"]["anchor"], "wct-acls-main-algorithm")
        self.assertTrue(row["required_primary_visual"]["require_desktop_and_mobile_variants"])
        css = STYLE.read_text(encoding="utf8")
        self.assertIn("@media(max-width:920px)", css)
        self.assertIn(".acls-mobile-graph{display:block}", css)
        self.assertIn("@media(max-width:480px)", css)


if __name__ == "__main__":
    unittest.main()
