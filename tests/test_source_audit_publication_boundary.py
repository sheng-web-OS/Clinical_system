"""A source-audit worklog must not masquerade as a dated reader article."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from catalog import load_pages


class SourceAuditPublicationBoundary(unittest.TestCase):
    def test_gi_liver_audit_worklog_is_private_but_exam_teaching_is_public(self):
        pages = json.loads((ROOT / "site/pages.json").read_text("utf8"))
        outputs = {row["output"] for row in pages}
        self.assertNotIn("xiaoma-exam-gi-liver-three-sources.html", outputs)
        self.assertIn("xiaoma-20261027-gi-liver-national-exam-trio.html", outputs)
        self.assertTrue((ROOT / "content/xiaoma-internal-medicine/exam-gi-liver-three-sources.md").is_file())

    def test_readers_retain_official_original_and_corrected_answers(self):
        article = (ROOT / "content/xiaoma-internal-medicine/lessons/"
                   "2026-10-27-gi-liver-exam-trio.md").read_text("utf8")
        self.assertNotIn("../exam-gi-liver-three-sources.md", article)
        for exam_code in ("112020", "114020", "114070"):
            self.assertIn("code=" + exam_code, article)
        self.assertEqual(article.count("t=Q"), 3)
        self.assertEqual(article.count("t=M"), 3)

    def test_source_audit_cannot_gain_date_and_become_article(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "site").mkdir()
            (root / "content").mkdir()
            (root / "content/audit.md").write_text("# Evidence only", encoding="utf8")
            (root / "site/pages.json").write_text(json.dumps([{
                "source": "content/audit.md",
                "output": "audit.html",
                "title": "Source audit",
                "subtitle": "not an article",
                "date": "2026-10-27",
                "review": "source_audit"
            }]), encoding="utf8")
            with self.assertRaisesRegex(ValueError, "Source audit cannot have article date"):
                load_pages(root)


if __name__ == "__main__":
    unittest.main()
