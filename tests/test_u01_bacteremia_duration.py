"""Guard the distinct 2025 IDSA cUTI duration recommendation for GN bacteremia."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "archive/pgy-antibiotics/u01/lesson.md"


class U01BacteremiaDurationSafetyTest(unittest.TestCase):
    def test_bacteremia_branch_has_conditional_seven_day_boundary(self):
        article = LESSON.read_text(encoding="utf-8")
        section = article.split("### T+72｜", 1)[1].split("## 反事實測試", 1)[0]
        for cue in ("Gram-negative bacteremia", "7 天", "14 天", "條件性", "低", "臨床改善"):
            with self.subTest(cue=cue):
                self.assertIn(cue, section, "Bacteremic cUTI is a distinct conditional guideline branch, not universal 7d")


if __name__ == "__main__":
    unittest.main()
