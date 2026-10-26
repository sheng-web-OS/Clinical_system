"""Regression contract for VTE figure: numeric, source-bounded, no fake diagnosis flow."""
import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-reading/integrated/2026-10-26-vte-visual.md"
SOURCES = ROOT / "content/xiaoma-reading/vte-sources.md"


class VTEDecisionFigureContract(unittest.TestCase):
    def test_only_one_meaningful_editorial_figure(self):
        article = ARTICLE.read_text(encoding="utf-8")
        self.assertEqual(article.count("<figure"), 1)
        self.assertIn('id="vte-d-dimer-bayes"', article)
        self.assertIn("<figcaption>", article)
        for rejected in (
            "vte-shared-substrate",
            "vte-competing-hypotheses",
            "vte-diagnostic-stop-rules",
            "vte-decision-resolution",
            "vte-anatomic-evidence",
        ):
            self.assertNotIn('id="' + rejected + '"', article)

    def test_assumed_bayes_values_and_clinical_limits(self):
        article = ARTICLE.read_text(encoding="utf-8")
        sources = SOURCES.read_text(encoding="utf-8")
        odds_after_low = (0.05 / 0.95) * 0.10
        odds_after_high = (0.50 / 0.50) * 0.10
        posterior = lambda o: 100 * o / (1 + o)
        self.assertAlmostEqual(posterior(odds_after_low), 0.52, delta=0.01)
        self.assertAlmostEqual(posterior(odds_after_high), 9.09, delta=0.01)
        for value in ["5%", "0.52%", "50%", "9.09%", "LR− = 0.10"]:
            self.assertIn(value, article)
        self.assertIn("假設", article)
        self.assertIn("不是", article)
        self.assertIn("NICE NG158", article)
        self.assertIn("Bayesian", sources)
        self.assertIn("0.52356%", sources)
        self.assertIn("9.09091%", sources)


if __name__ == "__main__":
    unittest.main()
