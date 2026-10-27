"""Regress the observed CI deadlock: semantic HOLD skipped CABG figure screenshots.

This tests workflow ordering and trust boundaries, NOT image readability or
clinical correctness. Keep deployment/medical gates mandatory and independent.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/pages.yml"


class PrivateVisualBeforeReleaseGate(unittest.TestCase):
    def setUp(self):
        self.source = WORKFLOW.read_text(encoding="utf-8")

    def test_pr_figure_qa_precedes_semantic_release_gate(self):
        steps = [
            "Run editorial and publication regression tests",
            "Render unapproved PR draft for private visual QA only",
            "Install Chromium for image layout QA",
            "Block newly added or changed figures with broken rendering",
            "Retain browser visual QA screenshots and reports",
            "Evidence-gated site build",
            "Save verified static site",
        ]
        places = [self.source.index("- name: " + step) for step in steps]
        self.assertEqual(places, sorted(places),
                         "A missing semantic review must not suppress private figure screenshots")

    def test_unapproved_preview_only_runs_for_pr_with_output_boundary_check(self):
        step = self.source.split(
            "- name: Render unapproved PR draft for private visual QA only", 1)[1]
        step = step.split("\n      - name:", 1)[0]
        self.assertIn("if: github.event_name == 'pull_request'", step)
        self.assertIn("python site/build.py", step)
        self.assertIn("python tools/check_output.py", step)
        self.assertNotIn("continue-on-error: true", step)
        installer = self.source.split("- name: Install Chromium for image layout QA", 1)[1]
        installer = installer.split("\n      - name:", 1)[0]
        timeout = re.search(r"(?m)^\\s*timeout-minutes:\\s*(\\d+)\\b", installer)
        self.assertIsNotNone(timeout, "Browser bootstrap must stay time-bounded")
        self.assertLessEqual(int(timeout.group(1)), 12, "Do not allow unbounded package downloads")
        self.assertGreaterEqual(int(timeout.group(1)), 4, "Allow enough time for a cold browser install")
        self.assertIn("python -m playwright install chromium", installer)
        self.assertIn("p.chromium.launch(headless=True)", installer)
        self.assertNotIn("upload-artifact", step)

    def test_semantic_gate_still_unconditional_before_verified_site_artifact(self):
        gate = "- name: Evidence-gated site build\n        run: bash tools/build_site.sh"
        self.assertIn(gate, self.source)
        released = self.source.split("- name: Save verified static site", 1)[1]
        self.assertIn("name: clinical-system-static-site", released)
        self.assertIn("path: dist/", released)
        self.assertNotIn("if: always()", released)
        self.assertNotIn("continue-on-error:", released)
        self.assertIn("branches: [main]", self.source)
        self.assertNotIn("pages deploy", self.source.lower())

    def test_browser_screenshots_are_kept_if_semantic_gate_fails(self):
        screenshot = self.source.split(
            "- name: Retain browser visual QA screenshots and reports", 1)[1]
        screenshot = screenshot.split("\n      - name:", 1)[0]
        self.assertIn("if: always()", screenshot)
        self.assertIn("path: visual-qa-artifacts/", screenshot)
        self.assertNotIn("path: dist/", screenshot)


if __name__ == "__main__":
    unittest.main()
