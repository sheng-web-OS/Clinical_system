"""Track fixed visual QA observability without conferring editorial approval."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DCM = ROOT / "content/xiaoma-reading/integrated/2026-10-21-dcm.md"
HYPOX = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-21-hypoxemia.md"
COPD = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-26-copd-emptying.md"
COPD_SOURCES = ROOT / "content/xiaoma-internal-medicine/copd-sources.md"

class PreviouslyUntrackedVisuals(unittest.TestCase):
    def test_dcm_legacy_figures_are_not_misrepresented_as_approved(self):
        # Original file is protected by figure_gate's frozen blob fingerprint.
        # QA discovery assigns synthetic names to its three legacy figures.
        # Never edit the source just to silence the visual inventory.
        text = DCM.read_text("utf-8")
        self.assertEqual(len(re.findall(r"<figure\b[^>]*>", text)), 3)
        self.assertNotIn("dcm-literature-pv-loop", text)

    def test_hypoxemia_figures_are_identifiable_not_declared_approved(self):
        text = HYPOX.read_text("utf-8")
        figures = re.findall(r"<figure\b[^>]*>", text)
        ids = re.findall(r'<figure\b[^>]*\bid="([^"]+)"', text)
        self.assertEqual(len(figures), len(ids))
        self.assertEqual(len(set(ids)), len(ids))
        for fid in ("hypoxemia-ventilation-dead-space", "hypoxemia-vq-vs-shunt",
                    "hypoxemia-oxygen-delivery-chain"):
            self.assertIn(fid, ids)

    def test_copd_does_not_embed_failed_mdpi_image_as_visual_evidence(self):
        content = COPD.read_text("utf-8")
        self.assertNotIn("medicina-55-00065-g001.png", content)
        self.assertNotIn('id="copd-case-ct-2019"', content)
        self.assertIn("PMC6473594", content)
        self.assertIn("原始 CT 圖 A–D 與完整圖說", content)
        self.assertNotIn("本站暫不內嵌此圖", content)
        sources = COPD_SOURCES.read_text("utf-8")
        self.assertIn("網站圖檔製作紀錄", sources)
        self.assertIn("未能穩定呈現", sources)

    def test_copd_reader_footer_does_not_expose_editorial_workflow(self):
        # Source/audit rights records stay in COPD_SOURCES, not the public lesson.
        content = COPD.read_text("utf-8")
        for leaked in (
            "四張小麻來源圖對讀及公開權利 HOLD",
            "本稿為私人閱讀修訂",
            "尚未獲得獨立醫學審查",
        ):
            with self.subTest(phrase=leaked):
                self.assertNotIn(leaked, content)
        self.assertIn("[原圖來源與使用限制](../copd-sources.md)", content)
        self.assertIn("PMC6473594", content)
        self.assertIn("goldcopd.org/2026-gold-report-and-pocket-guide/", content)
        self.assertIn("pubmed.ncbi.nlm.nih.gov/37924830/", content)
        self.assertIn("原書圖表未在本站重製", content)

if __name__ == "__main__":
    unittest.main()
