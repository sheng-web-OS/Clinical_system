"""Publication regression for the 108/1 medical(III) worked explanations."""
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "content/xiaoma-internal-medicine/lessons"
EXPECTED = {
    "2026-10-22-exam108-renal-foundations.md": {27: "B", 2: "D", 25: "C", 28: "B"},
    "2026-10-22-exam108-renal-perfusion.md": {17: "C", 22: "A", 23: "A", 26: "A"},
}


class Exam108Publication(unittest.TestCase):
    def test_questions_and_source_links_are_present(self):
        pages = json.loads((ROOT / "site/pages.json").read_text("utf8"))
        for filename, answers in EXPECTED.items():
            with self.subTest(filename=filename):
                text = (LESSONS / filename).read_text("utf8")
                headings = {int(n) for n in re.findall(r"(?m)^## 第 (\d+) 題", text)}
                self.assertEqual(headings, set(answers))
                for q, answer in answers.items():
                    self.assertRegex(text, rf"(?m)^\| {q} \| {answer}(?:\b|（| |\|)")
                self.assertIn("exam108-sources.md", text)
                self.assertNotRegex(text, r"你的選項|你選|個人作答|個人選|原個人|使用者.{0,12}原始|48 頁錯題附件")
                row = next(x for x in pages if x["source"].endswith(filename))
                self.assertEqual(row["references"], "xiaoma-exam108-sources.html")
                self.assertEqual(row["date"], "2026-10-22")

    def test_source_index_is_public_but_personal_record_is_not(self):
        pages = json.loads((ROOT / "site/pages.json").read_text("utf8"))
        outputs = {x["output"] for x in pages}
        self.assertIn("xiaoma-exam108-sources.html", outputs)
        references = (ROOT / "content/xiaoma-internal-medicine/exam108-sources.md").read_text("utf8")
        self.assertIn("Pocket Medicine", references)
        self.assertIn("考選部", references)
        self.assertTrue({"xiaoma-exam108-renal-foundations.html",
                         "xiaoma-exam108-renal-perfusion.html"} <= outputs)
        self.assertTrue(all(x["source"].startswith("content/") for x in pages))


if __name__ == "__main__":
    unittest.main()
