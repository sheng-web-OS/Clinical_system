"""Prevent direct main pushes from the medical exam archive workflow."""
from pathlib import Path
import unittest

WORKFLOW = Path(".github/workflows/archive-physician-stage2.yml")


class ArchiveWorkflowSafetyTests(unittest.TestCase):
    def test_archive_uses_draft_pr_not_direct_main_push(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertNotIn("git push origin HEAD:main", text)
        self.assertNotIn("git push origin HEAD:refs/heads/main", text)
        self.assertIn("gh pr create", text)
        self.assertIn("--draft", text)
        self.assertIn('git push origin "HEAD:refs/heads/$branch"', text)

    def test_duplicate_and_stale_source_fail_closed(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("gh pr list", text)
        self.assertIn("git ls-remote --heads", text)
        self.assertIn("git rev-parse origin/main", text)
        self.assertIn("git diff --cached --quiet", text)

    def test_write_scope_no_auto_merge(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("pull-requests: write", text)
        self.assertIn("contents: write", text)
        self.assertIn("archive/national-exam/physician-stage2-2022-2026", text)
        self.assertNotIn("gh pr merge", text)

    def test_public_raw_archive_opt_in_required(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("CLINICAL_OS_ARCHIVE_PUBLIC_SOURCE_APPROVED", text)
        self.assertIn("if: vars.CLINICAL_OS_ARCHIVE_PUBLIC_SOURCE_APPROVED == 'true'", text)


if __name__ == "__main__":
    unittest.main()
