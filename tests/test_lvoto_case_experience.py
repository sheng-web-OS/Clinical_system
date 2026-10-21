"""Regression gates for the LVOTO case learning pilot.

Static and interactive versions are reader facing; learning gains remain untested.
"""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
INTERACTIVE = ROOT / "content/clinical-os/lvoto-case-interactive.md"
STATIC = ROOT / "content/clinical-os/lvoto-case-static.md"
ATLAS = ROOT / "content/clinical-os/index.md"
PAGES = ROOT / "site/pages.json"
JS = ROOT / "site/app.js"


class LVOTOCasePilot(unittest.TestCase):
    def test_same_source_in_both_reading_modes(self):
        interactive = INTERACTIVE.read_text(encoding="utf-8")
        static = STATIC.read_text(encoding="utf-8")
        for fact in ("37 mm", "80%", "98 mmHg", "2,515", "369", "620",
                     "10.3978/j.issn.2072-1439.2015.09.22"):
            with self.subTest(fact=fact):
                self.assertIn(fact, interactive)
                self.assertIn(fact, static)
        self.assertIn("不是原病例", interactive)
        self.assertIn("不是原病例", static)

    def test_case_stages_have_consistent_answer_keys(self):
        text = INTERACTIVE.read_text(encoding="utf-8")
        stages = re.findall(
            r'<section class="case-step" data-case-stage="(\d+)" '
            r'data-case-correct="([abc])"[^>]*>(.*?)</section>',
            text, re.S
        )
        self.assertEqual(len(stages), 4)
        self.assertEqual([int(stage[0]) for stage in stages], list(range(4)))
        correct = []
        expect = ["尚不能由水腫", "符合動態 LVOTO",
                  "優先重估", "分別判定兩人的機轉"]
        for (_, key, body), marker in zip(stages, expect):
            values = re.findall(r'<input type="radio"[^>]*value="([abc])"', body)
            self.assertEqual(values, ["a", "b", "c"])
            matched = re.search(
                r'<input type="radio"[^>]*value="' + key
                + r'"><span>(.*?)</span>', body, re.S
            )
            self.assertIsNotNone(matched)
            self.assertIn(marker, matched.group(1))
            self.assertIn('data-case-rationale', body)
            self.assertIn('data-case-next', body)
            correct.append(key)
        self.assertGreater(len(set(correct)), 1)

    def test_progressive_disclosure_has_full_text_fallback(self):
        text = INTERACTIVE.read_text(encoding="utf-8")
        script = JS.read_text(encoding="utf-8")
        self.assertEqual(text.count("<!-- CASE_ANALYSIS_START -->"), 1)
        self.assertEqual(text.count("<!-- CASE_ANALYSIS_END -->"), 1)
        self.assertIn("原始證據", text)
        self.assertIn("case-sequence-enabled", script)
        self.assertIn("stage.dataset.caseCorrect", script)
        self.assertIn("data-case-skip", text)
        self.assertIn("noscript", text)
        self.assertIn("Figure 2", text)

    def test_public_entry_points_and_private_evaluation(self):
        pages = json.loads(PAGES.read_text(encoding="utf-8"))
        output_to_source = {p["output"]: p["source"] for p in pages}
        self.assertEqual(
            output_to_source["lvoto-case-interactive.html"],
            "content/clinical-os/lvoto-case-interactive.md"
        )
        self.assertEqual(
            output_to_source["lvoto-case-static.html"],
            "content/clinical-os/lvoto-case-static.md"
        )
        atlas = ATLAS.read_text(encoding="utf-8")
        self.assertIn("(lvoto-case-interactive.md)", atlas)
        self.assertIn("(lvoto-case-static.md)", atlas)
        self.assertFalse(any(p["source"].startswith(("audit/", "experiments/"))
                             for p in pages))


if __name__ == "__main__":
    unittest.main()
