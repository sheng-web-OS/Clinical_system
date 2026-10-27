"""PR visual QA must actually cover the user's three iPhone widths."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/pages.yml"


class PericardialMobileReleaseContract(unittest.TestCase):
    def test_changed_figures_render_at_360_375_390_and_desktop(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertRegex(
            workflow,
            r"python tools/visual_qa_browser\\.py --changed-from origin/main --widths 360 375 390 1280\\b",
            "A 375px browser render is required, not just 360/390 and a claim of mobile QA.",
        )


if __name__ == "__main__":
    unittest.main()
