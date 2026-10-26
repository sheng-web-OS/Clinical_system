"""A single clinical atlas owns concept relations and reading routes."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "site/pages.json"
ATLAS = ROOT / "content/clinical-os/index.md"
ROUTES = (
    "dyspnea", "perfusion", "chest", "kidney", "infection", "time"
)

class UnifiedClinicalAtlas(unittest.TestCase):
    def test_one_published_map_and_a_legacy_alias_not_a_second_catalog_entry(self):
        pages = json.loads(CATALOG.read_text("utf8"))
        by_output = {row["output"]: row for row in pages}
        self.assertIn("knowledge-atlas.html", by_output)
        self.assertEqual(by_output["knowledge-atlas.html"]["source"],
                         "content/clinical-os/index.md")
        self.assertNotIn("xiaoma-plan.html", by_output)
        self.assertNotIn("content/xiaoma-internal-medicine/learning-map.md",
                         {row["source"] for row in pages})
        self.assertNotIn("content/xiaoma-internal-medicine/plan.md",
                         {row["source"] for row in pages})

    def test_clinical_question_map_contains_concept_branches_learning_paths_and_exam_validation(self):
        body = ATLAS.read_text("utf8")
        for question in ROUTES:
            with self.subTest(question=question):
                self.assertIn('id="' + question + '"', body)
                self.assertIn('href="#' + question + '"', body)
        for heading in ("建議順序", "驗證", "跨篇關係", "改判"):
            self.assertIn(heading, body)
        self.assertIn("108", body)
        self.assertIn("先備", body)
        # The public atlas is not a dated personal learning calendar.
        self.assertNotIn("2027/1/10", body)
        self.assertNotIn("| 日期 | 核心主題 |", body)

    def test_promoted_navigation_does_not_advertise_old_map(self):
        compiler = (ROOT / "site/build.py").read_text("utf8")
        homepage = (ROOT / "site/home.py").read_text("utf8")
        self.assertNotIn('("xiaoma-plan.html", "閱讀路線")', compiler)
        self.assertNotIn('href="xiaoma-plan.html"', homepage)
        self.assertIn("knowledge-atlas.html", homepage)
        self.assertIn('atlas, old_map = "knowledge-atlas.html", "xiaoma-plan.html"', compiler)
        self.assertIn('meta http-equiv="refresh"', compiler)
        self.assertIn('OUTPUT_BY_SOURCE["content/xiaoma-internal-medicine/learning-map.md"] = "knowledge-atlas.html"', compiler)

if __name__ == "__main__":
    unittest.main()
