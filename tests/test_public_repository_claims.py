"""Regression: site output CI must not claim the PUBLIC GitHub repository is private.

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



if __name__ == "__main__":
    unittest.main()
