"""Guard against publishing unusable image links masquerading as original figures."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-reading/integrated/2026-10-26-vte-visual.md"
SOURCE = ROOT / "content/xiaoma-reading/vte-sources.md"
PAGES = ROOT / "site/pages.json"
AUDIT = ROOT / "audit/figure-gate.json"
VERIFIED_FLOW = "https://thrombosisuk.org/wp-content/uploads/2024/12/WellsScore.pdf"
BAD_FIGURE_ENDPOINTS = (
    "https://www.jkms.org/ViewImage.php",
    "https://www.nice.org.uk/guidance/ng158/resources/visual-summary-pdf-11193380893",
    "https://www.heart.org/-/media/Files/Health-Topics/Pulmonary-Embolism/What-is-a-PE.pdf",
)


class VTEOriginalFigureLinkPolicy(unittest.TestCase):
    def test_reader_only_promises_the_verified_original_chart(self):
        article = ARTICLE.read_text(encoding="utf-8")
        self.assertIn(VERIFIED_FLOW, article)
        self.assertIn("Thrombosis UK", article)
        for bad in BAD_FIGURE_ENDPOINTS:
            self.assertNotIn(bad, article)
        self.assertNotIn("原始四面板影像，可點開放大", article)
        self.assertEqual(article.count("<figure"), 2)
        self.assertIn('id="vte-d-dimer-bayes"', article)

    def test_source_and_seo_do_not_claim_unusable_image_links(self):
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn("圖像的原始身分與可閱讀範圍", source)
        self.assertIn("不以不穩定直連當作圖像已交付", source)
        self.assertIn(VERIFIED_FLOW, source)
        self.assertNotIn("https://www.jkms.org/ViewImage.php", source)
        pages = json.loads(PAGES.read_text(encoding="utf-8"))
        vte = next(p for p in pages if p.get("source","").endswith("2026-10-26-vte-visual.md"))
        self.assertNotIn("AHA、NICE 與真實病例原圖", vte["subtitle"])

    def test_source_gate_agrees_with_published_urls(self):
        data = json.loads(AUDIT.read_text(encoding="utf-8"))
        items = data["reviews"]["content/xiaoma-reading/integrated/2026-10-26-vte-visual.md"]["items"]
        external = [i["url"] for i in items if i.get("mode") == "source_link"]
        self.assertEqual(external, [VERIFIED_FLOW])


if __name__ == "__main__":
    unittest.main()
