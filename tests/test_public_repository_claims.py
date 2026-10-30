"""Regression: PUBLIC GitHub access must not be described as private CI storage.

This checks security-facing claims, not artifact contents or repository permissions.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublicRepositoryClaimsTests(unittest.TestCase):
    def test_site_output_pass_does_not_certify_private_git_access(self):
        source = (ROOT / "tools/check_output.py").read_text(encoding="utf-8")
        self.assertIn("GitHub repository PUBLIC", source)
        self.assertIn("public GitHub sources, PRs, Actions logs/artifacts are NOT private", source)
        self.assertNotIn("private repo nav boundary", source)
        self.assertNotIn("Private repository direct link", source)

    def test_visual_qa_scripts_do_not_promise_private_artifacts(self):
        for path in ("tools/qa_lab_morning_draft.py",
                     "tools/qa_acs_mobile.py", "tools/qa_sepsis_mobile.py"):
            with self.subTest(path=path):
                source = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("PUBLIC", source.split('"""', 2)[1])
                self.assertNotIn("private GitHub Actions artifact", source)
                self.assertNotIn("private CI", source)


if __name__ == "__main__":
    unittest.main()
