"""Regression: Sepsis public figure provenance must be independently navigable.

This test validates traceability and catalog wiring only, not clinical correctness.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = "content/clinical-os/2026-10-27-sepsis-from-infection-to-resuscitation.md"
SOURCE = "content/clinical-os/sepsis-sources-20261027.md"
ORIGINAL_FIGURE = "https://link.springer.com/article/10.1186/s12245-025-00958-5/figures/1"


class SepsisFigureSourceGate(unittest.TestCase):
    def test_original_figure_and_public_source_are_linked(self):
        article = (ROOT / ARTICLE).read_text(encoding="utf-8")
        self.assertIn(ORIGINAL_FIGURE, article)
        self.assertIn("sepsis-sources-20261027.md", article)
        source = (ROOT / SOURCE).read_text(encoding="utf-8")
        self.assertIn("Fig. 1", source)
        self.assertIn(ORIGINAL_FIGURE, source)
        self.assertIn("Case 1", source)

    def test_catalog_and_figure_gate_cover_sepsis(self):
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        catalog_sources = {p["source"] for p in pages}
        self.assertIn(ARTICLE, catalog_sources)
        self.assertIn(SOURCE, catalog_sources)
        figure = json.loads((ROOT / "audit/figure-gate.json").read_text(encoding="utf-8"))
        record = figure["reviews"][ARTICLE]
        self.assertEqual(record["status"], "represented")
        self.assertEqual(record["source_review"], SOURCE)
        self.assertTrue(any(
            item.get("mode") == "source_link"
            and item.get("url") == ORIGINAL_FIGURE
            for item in record["items"]
        ))


if __name__ == "__main__":
    unittest.main()
