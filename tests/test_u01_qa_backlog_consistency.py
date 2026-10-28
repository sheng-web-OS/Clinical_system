"""U01 private QA backlog must not re-open already implemented counterfactuals.

Keep CI status tied to the current HEAD rather than a permanently stale
"not run" statement. This test does not validate medical content.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "archive/pgy-antibiotics/u01/sources-qa.md"
LESSON = ROOT / "archive/pgy-antibiotics/u01/lesson.md"
TEST = ROOT / "archive/pgy-antibiotics/u01/case-test.md"


class U01QABacklogConsistencyTest(unittest.TestCase):
    def test_completed_counterfactual_not_left_as_next_action(self):
        qa = QA.read_text(encoding="utf-8")
        lesson = LESSON.read_text(encoding="utf-8")
        transfer = TEST.read_text(encoding="utf-8")
        self.assertIn("**D｜改成另一位 38 歲患者", lesson)
        self.assertIn("**T5：**", transfer)
        self.assertNotIn("加第二個 full counterfactual", qa)
        self.assertIn("D／T5", qa)

    def test_ci_gate_is_version_specific_not_permanently_unrun(self):
        qa = QA.read_text(encoding="utf-8")
        self.assertNotIn("尚未執行／未取得 head-specific results", qa)
        self.assertIn("最新 HEAD", qa)


if __name__ == "__main__":
    unittest.main()
