"""Structural regressions for the liver-test visual rewrite.

These assertions are not substitutes for rendered mobile screenshots or physician review.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-reading/integrated/2026-10-26-liver-tests.md"
EVIDENCE = ROOT / "content/xiaoma-reading/liver-tests-sources.md"
CSS = ROOT / "site/styles.css"
AUDIT = ROOT / "audit/figure-gate.json"
PATH = "content/xiaoma-reading/integrated/2026-10-26-liver-tests.md"


class LiverFigureRegressions(unittest.TestCase):
    def test_no_recycled_text_cards(self):
        source = ARTICLE.read_text(encoding="utf-8")
        self.assertNotIn("liver-independent-axes", source)
        self.assertNotIn('class="reasoning-cards"', source)
        self.assertEqual(source.count("<figure "), 2)
        for anchor in ("liver-pattern-map", "liver-divergent-trajectories"):
            match = re.search(r'<figure id="' + anchor + r'"[^>]*>(.*?)</figure>', source, re.S)
            self.assertIsNotNone(match, anchor)
            self.assertIn("<figcaption>", match.group(1))
            self.assertIn("Pocket Medicine 9E", match.group(1))

    def test_ratio_chart_values_can_be_recomputed(self):
        """A, B and C use the same, expressly hypothetical lab ULNs."""
        cases = [(600, 180, 10), (320, 240, 4), (120, 720, 0.5)]
        for alt, alp, expected in cases:
            self.assertAlmostEqual((alt / 40) / (alp / 120), expected)
        source = ARTICLE.read_text(encoding="utf-8")
        for signal in ("15×", "1.5×", "8×", "2×", "3×", "6×",
                       "R = 10", "R = 4", "R = 0.5", "共同使用"):
            self.assertIn(signal, source)
        self.assertIn("非真實病例", source)

    def test_time_chart_is_declared_qualitative_not_patient_measurement(self):
        source = ARTICLE.read_text(encoding="utf-8")
        match = re.search(r'<figure id="liver-divergent-trajectories"[^>]*>(.*?)</figure>', source, re.S)
        self.assertIsNotNone(match)
        piece = match.group(1)
        self.assertEqual(piece.count('<svg viewBox='), 2)
        self.assertIn("非病例實測", piece)
        self.assertIn("vitamin K", piece)
        self.assertIn("DIC", piece)
        self.assertIn("INR", piece)
        self.assertIn("ALT 下降 ≠ 病情改善", piece)

    def test_styles_and_provenance_cover_each_different_teaching_role(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertIn(".liver-trend-panels{grid-template-columns:1fr}", css)
        self.assertIn("@media(max-width:680px)", css)
        evidence = EVIDENCE.read_text(encoding="utf-8")
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        entries = audit["reviews"][PATH]["items"]
        self.assertEqual({i["anchor"] for i in entries},
                         {"liver-pattern-map", "liver-divergent-trajectories"})
        for entry in entries:
            self.assertIn(entry["source_token"], evidence)
            self.assertEqual(entry["mode"], "illustrated")


if __name__ == "__main__":
    unittest.main()
