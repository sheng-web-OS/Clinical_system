"""Protect the clinical comparison that the original 900px SVG failed to teach."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WPW = ROOT / "content/xiaoma-reading/integrated/2026-10-26-wpw-conduction-mechanism.md"
STYLE = ROOT / "site/styles.css"
BROWSER_QA = ROOT / "tools/visual_qa_browser.py"
WORKFLOW = ROOT / ".github/workflows/pages.yml"


class SourceFigurePhoneReading(unittest.TestCase):
    def test_three_activation_states_are_readable_as_distinct_source_views(self):
        article = WPW.read_text(encoding="utf-8")
        start = article.index('<figure id="wpw-pathway-figure"')
        figure = article[start:article.index("</figure>", start)]
        self.assertEqual(figure.count('class="wpw-focus-case"'), 3)
        self.assertEqual(figure.count('role="img"'), 3)
        for value in ("Sinus pre-excitation", "Orthodromic AVRT", "Antidromic AVRT",
                      "fusion", "delta wave", "regular narrow QRS", "regular wide QRS",
                      "不能排除 VT"):
            self.assertIn(value, figure)
        # The same source image is used for all three views; none is generated
        # or substituted as a claimed clinical ECG recording.
        srcs = re.findall(r'<img src="([^"]+)"', figure)
        self.assertEqual(len(srcs), 4)
        self.assertEqual(len(set(srcs)), 1)
        self.assertIn("不是 Khan 病例的實測心電圖", figure)
        self.assertIn("第三方", figure)
        self.assertIn("局部裁切顯示", figure)
        self.assertNotIn("<svg", figure)

    def test_mobile_view_has_nonhorizontal_source_panels(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn(".article .wpw-original-overview{display:none}", css)
        self.assertIn(".article .wpw-mobile-focus{display:grid", css)
        for name in ("wpw-crop-1", "wpw-crop-2", "wpw-crop-3"):
            self.assertIn(name, WPW.read_text(encoding="utf-8"))
        self.assertIn("aspect-ratio:250 / 446", css)
        self.assertIn("max-width:none!important", css)

    def test_af_pathway_counterfactual_is_visible_without_scroll_svg(self):
        af = (ROOT / "content/xiaoma-reading/integrated/2026-10-26-preexcited-af.md").read_text(encoding="utf-8")
        start = af.index('id="af-two-exits"')
        figure = af[start:af.index("</figure>", start)]
        self.assertIn('class="af-causal-counterfactual"', figure)
        self.assertEqual(figure.count("class=\"af-causal-path "), 2)
        self.assertIn("Decremental conduction", figure)
        self.assertIn("阻斷 AV node", figure)
        self.assertIn("圖 3｜示意，不是 ECG。", figure)
        self.assertNotIn("overflow-x", figure)
        self.assertNotIn("<svg", figure)
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn(".article .af-causal-paths{display:grid", css)
        self.assertIn("figure hides important content behind horizontal scrolling",
                      BROWSER_QA.read_text(encoding="utf-8"))

    def test_actual_browser_acceptance_is_not_optional_on_pr(self):
        script = BROWSER_QA.read_text(encoding="utf-8")
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for value in ("naturalWidth", "screenshot", "scrollWidth", "390"):
            self.assertIn(value, script + workflow)
        self.assertIn("python tools/visual_qa_browser.py", workflow)


if __name__ == "__main__":
    unittest.main()
