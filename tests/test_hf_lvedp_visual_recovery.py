"""HF/LVEDP figure recovery must preserve historical originals and truthful image provenance."""
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"site"))
from catalog import load_pages

class HeartFailureFigureAudit(unittest.TestCase):
    def test_legacy_originals_unchanged(self):
        pages = load_pages(ROOT)
        for slug in ("heart-failure", "lvedp"):
            name = f"2026-07-12-{slug}.md"
            source = next(x for x in pages if x["source"].endswith("originals/"+name))
            self.assertEqual(hashlib.sha256((ROOT/source["source"]).read_bytes()).hexdigest(), source["source_sha256"])

    def test_two_figures_have_real_source_records_and_in_article_explanations(self):
        pages = load_pages(ROOT)
        path = "content/xiaoma-reading/integrated/2026-10-23-hf-lvedp-figures.md"
        row = next(x for x in pages if x["source"] == path)
        self.assertEqual(row["kind"], "ai_integrated")
        self.assertEqual(row["references"], "xiaoma-reading-hf-lvedp-figure-sources.html")
        article = (ROOT/path).read_text("utf8")
        sources = (ROOT/"content/xiaoma-reading/hf-lvedp-figure-sources.md").read_text("utf8")
        for ident in ("hf-phenotype-matrix", "lv-filling-branches"):
            self.assertIn(f'id="{ident}"', article)
        self.assertEqual(article.count("<figure"), 2)
        self.assertEqual(article.count("</figure>"), 2)
        self.assertIn("PDF 第 37 頁", sources)
        self.assertIn("PDF 第 35 頁", sources)
        self.assertIn("Figure 1-2", sources)
        self.assertIn("Warm & Dry", sources)
        self.assertIn("不是原書圖像截圖", article)
        self.assertIn("LVEDV", article)
        self.assertIn("PCWP", article)

    def test_unverified_renal_perfusion_still_pending(self):
        record = json.loads((ROOT/"audit/figure-gate.json").read_text("utf8"))
        pending = "content/xiaoma-internal-medicine/lessons/2026-10-22-exam108-renal-perfusion.md"
        self.assertIn(pending, record["legacy_frozen"])
        self.assertNotIn(pending, record["reviews"])
        restored = "content/xiaoma-internal-medicine/lessons/2026-10-22-exam108-renal-foundations.md"
        self.assertIn(restored, record["reviews"])
        self.assertNotIn(restored, record["legacy_frozen"])

if __name__ == "__main__":
    unittest.main()
