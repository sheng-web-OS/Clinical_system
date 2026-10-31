"""U01 reader-facing counterfactual heading must match its enumerated branches.

This is a structural L0 regression check, not medical validation.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "archive/pgy-antibiotics/u01/lesson.md"


class U01CounterfactualCountTest(unittest.TestCase):
    def test_heading_count_matches_actual_branches(self):
        article = LESSON.read_text(encoding="utf-8")
        section = article.split("## 反事實測試：", 1)[1].split(
            "## 真正的二階國考對題", 1
        )[0]
        title, body = section.split("\n", 1)
        declared = re.search(r"([一二三四五六七八九十]+)個改動", title)
        self.assertIsNotNone(declared, "Counterfactual count must be stated")
        chinese_counts = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5}
        expected = chinese_counts.get(declared.group(1))
        self.assertIsNotNone(expected, "Unrecognized count in heading")
        branches = re.findall(r"^\*\*([A-Z])｜", body, flags=re.MULTILINE)
        self.assertEqual(len(branches), expected,
                         f"Heading promises {expected} but presents {branches}")
        self.assertEqual(branches, list("ABCD"),
                         "Keep four distinct decision counterfactuals")


if __name__ == "__main__":
    unittest.main()
