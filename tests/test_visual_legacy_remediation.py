"""Track fixed visual QA observability without conferring editorial approval."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DCM = ROOT / "content/xiaoma-reading/integrated/2026-10-21-dcm.md"
HYPOX = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-21-hypoxemia.md"
COPD = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-26-copd-emptying.md"

class PreviouslyUntrackedVisuals(unittest.TestCase):
    def test_dcm_figures_have_stable_unique_ids(self):
        text = DCM.read_text("utf-8")
        figures = re.findall(r"<figure\b[^>]*>", text)
        ids = re.findall(r'<figure\b[^>]*\bid="([^"]+)"', text)
        self.assertEqual(len(figures), len(ids))
        self.assertEqual(len(ids), len(set(ids)))
        for fid in ("dcm-literature-pv-loop", "dcm-literature-functional-mr",
                    "dcm-literature-ischemic-cmr"):
            self.assertIn(fid, ids)

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
        self.assertIn("本站暫不內嵌此圖", content)

if __name__ == "__main__":
    unittest.main()
