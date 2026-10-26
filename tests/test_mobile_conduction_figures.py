"""Visual regressions drawn from the 2026-10-27 clipped WPW screenshot.

These static tests are *not* replacements for real 375/390px browser screenshots.
They prevent reverting a sourced ECG figure to a fixed-width made-up SVG.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WPW = "content/xiaoma-reading/integrated/2026-10-26-wpw-conduction-mechanism.md"
AF = "content/xiaoma-reading/integrated/2026-10-26-preexcited-af.md"


def figure(path, identifier):
    body = (ROOT / path).read_text(encoding="utf8")
    for match in re.finditer(r"<figure\b[^>]*>.*?</figure>", body, re.S | re.I):
        text = match.group(0)
        if ('id="' + identifier + '"') in text:
            return text
    raise AssertionError("Missing figure " + identifier)


class MobileConductionFigureRegression(unittest.TestCase):
    def test_wpw_keeps_real_primary_medical_figure_not_clipped_svg(self):
        f = figure(WPW, "wpw-pathway-figure")
        self.assertIn("<img ", f)
        self.assertIn("Electrocardiographic_features_of_pre_excitation", f)
        self.assertIn('alt="', f)
        self.assertIn("CC BY 4.0", f)
        self.assertNotIn('<svg ', f)
        self.assertNotIn('overflow-x:auto', f)
        self.assertIn("<figcaption>", f)

    def test_af_mechanism_not_fixed_width_or_hidden_off_screen(self):
        f = figure(AF, "af-two-exits")
        self.assertNotIn('width="780"', f)
        self.assertNotIn('overflow-x:auto', f)
        for content in ("decremental conduction", "pre-excited AF", "2023 AF guideline"):
            self.assertIn(content, f)
        self.assertIn("<figcaption>", f)

    def test_mobile_specific_reading_styles_exist(self):
        css = (ROOT / "site/styles.css").read_text(encoding="utf8")
        self.assertIn(".article .wpw-af-paths", css)
        self.assertIn("@media(max-width:520px)", css)


if __name__ == "__main__":
    unittest.main()
