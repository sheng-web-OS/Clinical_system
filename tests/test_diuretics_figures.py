"""Verify the illustrated diuretics edition without mutating its historical original."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
NEW = ROOT / "content/xiaoma-reading/integrated/2026-10-22-diuretics-visual.md"
ORIGINAL = ROOT / "content/xiaoma-reading/originals/2026-07-20-diuretics.md"
SOURCES = ROOT / "content/xiaoma-reading/diuretics-sources.md"


class IllustratedDiuresisPublication(unittest.TestCase):
    def test_preserve_original_fingerprint_and_publish_separate_edition(self):
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf8"))
        historical = next(p for p in pages if p["source"].endswith("/originals/2026-07-20-diuretics.md"))
        self.assertEqual(hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(), historical["source_sha256"])
        illustration = next(p for p in pages if p["output"] == "xiaoma-reading-diuretics-visual.html")
        self.assertEqual(illustration["kind"], "ai_integrated")
        self.assertNotEqual(illustration["source"], historical["source"])
        self.assertEqual(illustration["references"], "xiaoma-reading-diuretics-sources.html")

    def test_figures_are_visible_accessible_and_attributed(self):
        t = NEW.read_text(encoding="utf8")
        self.assertEqual(t.count('<figure class="diuretic-figure"'), 2)
        self.assertEqual(t.count("</figure>"), 2)
        self.assertIn('viewBox="0 0 760 400"', t)
        self.assertIn('role="img" aria-labelledby="dose-curve-title dose-curve-desc"', t)
        for required in ("Threshold", "Ceiling", "FIGURE 01", "FIGURE 02",
                         "原書的截圖", "第 180 頁", "2021 ESC"):
            self.assertIn(required, t)
        self.assertIn("../diuretics-sources.md", t)
        self.assertNotIn("<img src=\"assets/pocket", t)

    def test_source_table_is_identified_without_unlicensed_reproduction(self):
        sources = SOURCES.read_text(encoding="utf8")
        for token in ("PDF 第 179 頁", "PDF 第 180 頁", "Approach to Diuresis",
                      "不是印出一張曲線原圖", "DOSE", "PUSH-AHF"):
            self.assertIn(token, sources)
        self.assertNotIn("data:image/", NEW.read_text(encoding="utf8"))


if __name__ == "__main__":
    unittest.main()
