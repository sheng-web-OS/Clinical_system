"""Regression for the literal TeX shown on mobile national-exam reading pages."""
import sys
import unittest
from pathlib import Path

import mistune

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from math_render import compile_math


class MathRendering(unittest.TestCase):
    def setUp(self):
        self.markdown = mistune.create_markdown(
            renderer=mistune.HTMLRenderer(escape=False), plugins=["table", "strikethrough", "url"]
        )

    def test_all_exam_formulas_become_native_mathml_not_raw_tex(self):
        raw = (ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-22-exam108-renal-foundations.md").read_text("utf8")
        rendered = self.markdown(compile_math(raw))
        # Free water deficit, total body water, target sodium, first-day target, FENa.
        self.assertEqual(rendered.count('class="math-display"'), 5)
        self.assertGreaterEqual(rendered.count('<math xmlns="http://www.w3.org/1998/Math/MathML"'), 5)
        self.assertIn("<mfrac>", rendered)
        self.assertIn("<math ", rendered)
        self.assertIn('display="block"', rendered)
        self.assertNotIn(r"\frac", rendered)
        self.assertNotIn(r"\times", rendered)
        self.assertNotIn(r"\[", rendered)
        self.assertNotIn(r"\]", rendered)
        self.assertIn("為什麼選項 5 L 具有迷惑性", rendered)

    def test_inline_math_works_without_paragraph_break(self):
        raw = r"Cardiac output is \(CO=HR\times SV\) under these assumptions."
        body = self.markdown(compile_math(raw))
        self.assertIn('class="math-inline"', body)
        self.assertIn('display="inline"', body)
        self.assertIn("<math ", body)
        self.assertNotIn(r"\(", body)

    def test_math_environment_is_rendered_as_display(self):
        raw = "$$\n\\frac{1}{2}+x\n$$"
        rendered = self.markdown(compile_math(raw))
        self.assertIn('class="math-display"', rendered)
        self.assertIn("<mfrac>", rendered)

    def test_do_not_modify_literal_math_in_code_blocks(self):
        raw = "~~~latex\n\\[\n\\frac{1}{2}\n\\]\n~~~\n"
        rendered = self.markdown(compile_math(raw))
        self.assertIn(r"\frac{1}{2}", rendered)
        self.assertNotIn("<math ", rendered)

    def test_unmatched_display_delimiters_fail_fast(self):
        with self.assertRaisesRegex(ValueError, "Unmatched"):
            compile_math("\\[\n\\frac{1}{2}\n")

    def test_mathml_mobile_scroll_styles(self):
        css = (ROOT / "site/styles.css").read_text("utf8")
        self.assertIn(".reading-prose .math-display", css)
        self.assertIn("overflow-x:auto", css)
        self.assertIn("width:max-content", css)
        self.assertIn("-webkit-overflow-scrolling:touch", css)


if __name__ == "__main__":
    unittest.main()
