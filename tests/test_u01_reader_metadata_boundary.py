"""U01 public reader prose must not expose editorial release-workflow metadata.

The synthetic-case and not-order-ready clinical safety boundary MUST remain.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "archive/pgy-antibiotics/u01/lesson.md"


class U01ReaderMetadataBoundaryTest(unittest.TestCase):
    def test_reader_has_no_internal_release_workflow_status(self):
        article = ARTICLE.read_text(encoding="utf-8")
        for internal in (
            "教學候選稿 v0.2",
            "Draft/HOLD",
            "原始 Figure/表註腳對照",
            "建置/手機端與正式網站驗收",
        ):
            with self.subTest(internal=internal):
                self.assertNotIn(internal, article)

    def test_clinical_and_synthetic_boundaries_survive(self):
        article = ARTICLE.read_text(encoding="utf-8")
        for required in (
            "病例為人工合成",
            "並非真實病例報告",
            "不能",
            "當院",
            "藥師",
            "劑量",
        ):
            with self.subTest(required=required):
                self.assertIn(required, article)


if __name__ == "__main__":
    unittest.main()
