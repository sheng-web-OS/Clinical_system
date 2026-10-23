"""Check both original Pocket 9E renal diagnostic branches are visible in the exam prose."""
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from catalog import load_pages

NAME = "content/xiaoma-internal-medicine/lessons/2026-10-22-exam108-renal-foundations.md"

class RenalExamVisualRegression(unittest.TestCase):
    def test_figure_sources_are_visual_and_qualify_but_do_not_copy_original(self):
        load_pages(ROOT)
        s = (ROOT / NAME).read_text(encoding="utf8")
        self.assertEqual(s.count('<figure class="renal-figure"'), 2)
        for fig in ("hypernatremia-uosm-branches", "metabolic-alkalosis-ucl-branches"):
            self.assertEqual(s.count(f'id="{fig}"'), 1)
        self.assertIn("Figure 4-5", s)
        self.assertIn("Figure 4-3", s)
        self.assertIn("UCl（mEq/L）不等於本題的 FECl（%）", s)
        self.assertIn("非原書截圖", s)
        self.assertIn("../exam108-sources.md", s)

        a = json.loads((ROOT/"audit/figure-gate.json").read_text("utf8"))
        self.assertNotIn(NAME, a["legacy_frozen"])
        record = a["reviews"][NAME]
        self.assertEqual(record["status"], "represented")
        self.assertEqual({i["anchor"] for i in record["items"]},
                         {"hypernatremia-uosm-branches","metabolic-alkalosis-ucl-branches"})

    def test_do_not_erase_existing_four_question_answers(self):
        s = (ROOT / NAME).read_text(encoding="utf8")
        for question in ("## 第 27 題", "## 第 2 題",
                         "## 第 25 題", "## 第 28 題"):
            self.assertEqual(s.count(question), 1)
        self.assertIn("| 27 | B（問何者錯誤）", s)
        self.assertIn("| 2 | D |", s)
        self.assertIn("| 25 | C |", s)
        self.assertIn("| 28 | B |", s)

if __name__ == "__main__":
    unittest.main()
