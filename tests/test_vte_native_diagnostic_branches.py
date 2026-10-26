"""Prevent regression to pseudo-charts or wrong DVT/PE stop conditions."""
from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-reading/integrated/2026-10-26-vte-visual.md"
CSS = ROOT / "site/styles.css"

class VTENativeBranchFigure(unittest.TestCase):
    def test_vector_and_mobile_are_native_and_medically_bounded(self):
        s = ARTICLE.read_text(encoding="utf-8")
        self.assertIn('id="vte-native-diagnostic-pathways"', s)
        self.assertEqual(s.count('class="vte-branch-svg"'), 2)
        self.assertEqual(s.count('class="vte-branch-mobile"'), 2)
        self.assertEqual(s.count('marker-end="url(#arrow-dvt)"'), 6)
        self.assertEqual(s.count('marker-end="url(#arrow-pe)"'), 6)
        for token in ("DVT likely：Wells ≥ 2", "PE likely：Wells &gt; 4",
                      "D-dimer 陰性", "D-dimer 陽性", "6–8 天",
                      "重複 proximal ultrasound", "CTPA", "clinical probability",
                      "血流動力學", "NICE NG158"):
            self.assertIn(token, s)
        self.assertNotIn("www.jkms.org/ViewImage.php", s)
    def test_mobile_does_not_shrink_desktop_svg(self):
        s = CSS.read_text(encoding="utf-8")
        self.assertIn("@media(max-width:850px)", s)
        self.assertIn(".vte-pathways-panel svg{display:none}", s)
        self.assertIn(".vte-branch-mobile{display:block}", s)
        self.assertIn(".vte-m-pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))", s)

if __name__ == "__main__":
    unittest.main()
