"""Reader-facing source identity must not invite invented acronym expansions."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-27-cticu-abg-cabg-lactate.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/cticu-abg-cabg-sources.md"


class CTICUCABGSourceIdentityTests(unittest.TestCase):
    def test_ibcc_is_expanded_correctly_at_first_reader_mention(self):
        lesson = LESSON.read_text("utf-8")
        self.assertIn("IBCC（Internet Book of Critical Care）", lesson)
        self.assertEqual(lesson.index("IBCC"), lesson.index("IBCC（Internet Book of Critical Care）"))
        self.assertNotIn("International Board of Cardiothoracic Critical care", lesson)
        self.assertIn("https://emcrit.org/ibcc/cts/", SOURCES.read_text("utf-8"))


if __name__ == "__main__":
    unittest.main()
