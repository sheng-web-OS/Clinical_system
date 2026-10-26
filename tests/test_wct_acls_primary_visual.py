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
    def test_official_algorithm_is_visible_before_acls_discussion(self):
        t = ARTICLE.read_text(encoding="utf8")
        self.assertIn('id="wct-acls-main-algorithm"', t)
        self.assertLess(t.index('id="wct-acls-main-algorithm"'),
                        t.index("## Tachycardia 是不穩定的原因"))
        match = re.search(r'<figure id="wct-acls-main-algorithm".*?</figure>', t, re.S)
        self.assertIsNotNone(match)
        fig = match.group(0)
        self.assertIn("2025 AHA", fig)
        self.assertIn("Algorithm-ACLS-Tachycardia-250514.pdf", fig)
        self.assertIn("官方完整原圖", fig)
        self.assertIn("非 AHA 原圖", fig)

    def test_clinical_decisions_have_actual_routes_not_plain_cards(self):
        t = ARTICLE.read_text(encoding="utf8")
        match = re.search(r'<figure id="wct-acls-main-algorithm".*?</figure>', t, re.S)
        fig = match.group(0)
        self.assertIn('viewBox="0 0 1120 995"', fig)
        self.assertIn('class="acls-desktop-graph"', fig)
        self.assertIn('class="acls-mobile-graph"', fig)
        self.assertGreaterEqual(fig.count('marker-end="url(#acls-arrow)"'), 5)
        self.assertIn("YES", fig)
        self.assertIn("NO", fig)
        for term in ("synchronized cardioversion", "Wide QRS", "0.12", "adenosine",
                     "regular", "monomorphic", "unsynchronized shock",
                     "pre-excited AF", "無脈搏"):
            self.assertIn(term.lower(), fig.lower())

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
