"""Prevent CABG draft mobile QA from regressing to the 4-minute browser bootstrap.

This checks CI prerequisites only; it is not medical or visual approval.
"""
import unittest
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/pages.yml"


class CABGMobileWorkflowRegression(unittest.TestCase):
    def test_chromium_bootstrap_is_bounded_and_recoverable(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("      - name: Install Chromium for image layout QA", workflow)
        bootstrap = workflow.split("      - name: Install Chromium for image layout QA", 1)[1].split("\n      - name:", 1)[0]
        self.assertIn("timeout-minutes: 12", bootstrap,
                      "Four minutes was too short for upstream browser dependency stalls")
        self.assertIn("python -m playwright install chromium", bootstrap)
        self.assertIn("python -m playwright install-deps chromium", bootstrap,
                      "Missing dependency fallback must not silently skip browser QA")
        self.assertIn("p.chromium.launch(headless=True)", bootstrap,
                      "A successful download is not proof that Chromium launches")
        self.assertIn("--widths 360 375 390 1280", workflow,
                      "The CABG figure must include the 375px phone viewport")


if __name__ == "__main__":
    unittest.main()
