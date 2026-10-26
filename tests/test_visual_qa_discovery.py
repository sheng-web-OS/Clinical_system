"""Regression tests for publication-allowlist figure screenshot discovery.

These structural tests do not certify medical meaning or pixel-level readability.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from visual_qa_browser import discover_pages, changed_pages, changed_figures, figure_versions, write_review_summary


class VisualQADiscoveryTest(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        (self.root / "site").mkdir()
        (self.root / "content").mkdir()
        (self.root / "content/lesson.md").write_text(
            '# Lesson\n<figure id="decision"><svg></svg></figure>\n'
            '<figure id="source-ecg"><img src="ecg.png"></figure>',
            encoding="utf-8")
        (self.root / "content/plain.md").write_text(
            "# This published page has no figure", encoding="utf-8")
        (self.root / "content/private.md").write_text(
            '<figure id="not-public"></figure>', encoding="utf-8")
        (self.root / "site/pages.json").write_text(json.dumps([
            {"source": "content/lesson.md", "output": "reader-lesson.html"},
            {"source": "content/plain.md", "output": "reader-plain.html"},
        ]), encoding="utf-8")

    def test_finds_figures_only_in_published_pages(self):
        self.assertEqual(discover_pages(self.root), {
            "reader-lesson": ("reader-lesson.html", ["decision", "source-ecg"])
        })

    def test_legacy_unnamed_figure_is_included_for_qa_hold(self):
        p = self.root / "content/lesson.md"
        p.write_text('<figure><svg></svg></figure>', encoding="utf-8")
        self.assertEqual(discover_pages(self.root), {
            "reader-lesson": ("reader-lesson.html", ["__unnamed_01"])
        })

    def test_duplicate_id_fails(self):
        p = self.root / "content/lesson.md"
        p.write_text('<figure id="repeat"></figure><figure id="repeat"></figure>',
                     encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate figure id"):
            discover_pages(self.root)


    @patch("visual_qa_browser.subprocess.run")
    def test_only_modified_public_article_is_rendered(self, git):
        git.return_value = subprocess.CompletedProcess([], 0, "content/lesson.md\ncontent/private.md\n", "")
        self.assertEqual(changed_pages(self.root, "origin/main"), ["reader-lesson"])
        self.assertIn("origin/main...HEAD", git.call_args.args[0])

    @patch("visual_qa_browser.subprocess.run")
    def test_unlisted_changes_do_not_trigger_fictitious_public_figures(self, git):
        git.return_value = subprocess.CompletedProcess([], 0, "content/private.md\n", "")
        self.assertEqual(changed_pages(self.root, "origin/main"), [])

    @patch("visual_qa_browser.subprocess.run")
    def test_catalog_change_inspects_all_public_figures(self, git):
        git.return_value = subprocess.CompletedProcess([], 0, "site/pages.json\n", "")
        self.assertEqual(changed_pages(self.root, "origin/main"), ["reader-lesson"])

    @patch("visual_qa_browser.subprocess.run")
    def test_git_diff_failure_cannot_silently_skip_visual_checks(self, git):
        git.side_effect = subprocess.CalledProcessError(128, "git diff")
        with self.assertRaises(subprocess.CalledProcessError):
            changed_pages(self.root, "origin/main")

    def test_rejects_unsafe_git_ref(self):
        with self.assertRaisesRegex(ValueError, "Invalid git base"):
            changed_pages(self.root, "main..evil")

    @patch("visual_qa_browser.subprocess.run")
    def test_prose_only_edit_does_not_recheck_unchanged_figures(self, git):
        original = (self.root / "content/lesson.md").read_text(encoding="utf-8")
        (self.root / "content/lesson.md").write_text("New introduction\n" + original, encoding="utf-8")
        diff = subprocess.CompletedProcess([], 0, "content/lesson.md\n", "")
        git.side_effect = [diff, diff, subprocess.CompletedProcess([], 0, original, "")]
        self.assertEqual(changed_figures(self.root, "origin/main"), {})

    @patch("visual_qa_browser.subprocess.run")
    def test_one_modified_figure_only_rechecks_that_figure(self, git):
        original = (self.root / "content/lesson.md").read_text(encoding="utf-8")
        (self.root / "content/lesson.md").write_text(
            original.replace("<svg></svg>", "<svg><title>changed</title></svg>"),
            encoding="utf-8")
        diff = subprocess.CompletedProcess([], 0, "content/lesson.md\n", "")
        git.side_effect = [diff, diff, subprocess.CompletedProcess([], 0, original, "")]
        self.assertEqual(changed_figures(self.root, "origin/main"),
                         {"reader-lesson": ("reader-lesson.html", ["decision"])})

    @patch("visual_qa_browser.subprocess.run")
    def test_new_article_figures_cannot_skip_when_base_version_missing(self, git):
        diff = subprocess.CompletedProcess([], 0, "content/lesson.md\n", "")
        git.side_effect = [diff, diff, subprocess.CompletedProcess([], 128, "", "missing")]
        self.assertEqual(changed_figures(self.root, "origin/main"),
                         {"reader-lesson": ("reader-lesson.html", ["decision", "source-ecg"])})

    def test_figure_version_scanner_detects_nested_content_changes(self):
        self.assertNotEqual(
            figure_versions('<figure id="decision"><svg></svg></figure>'),
            figure_versions('<figure id="decision"><svg><title>new</title></svg></figure>'))

    @patch("visual_qa_browser.subprocess.run")
    def test_changed_image_asset_invalidates_unchanged_figure_markup(self, git):
        changed = subprocess.CompletedProcess([], 0, "site/source_images/ecg.png\n", "")
        git.side_effect = [changed, changed]
        self.assertEqual(changed_figures(self.root, "origin/main"),
                         {"reader-lesson": ("reader-lesson.html", ["source-ecg"])})

    @patch("visual_qa_browser.subprocess.run")
    def test_shared_style_change_does_not_fail_on_unchanged_legacy_figures(self, git):
        git.return_value = subprocess.CompletedProcess([], 0, "site/styles.css\n", "")
        self.assertEqual(changed_figures(self.root, "origin/main"), {})

    @patch("visual_qa_browser.subprocess.run")
    def test_newly_allowlisted_page_requires_all_figures_checked(self, git):
        old_catalog = json.dumps([{"source": "content/plain.md", "output": "reader-plain.html"}])
        diff = subprocess.CompletedProcess([], 0, "site/pages.json\n", "")
        git.side_effect = [diff, subprocess.CompletedProcess([], 0, old_catalog, ""),
                           diff]
        self.assertEqual(changed_figures(self.root, "origin/main"),
                         {"reader-lesson": ("reader-lesson.html", ["decision", "source-ecg"])})



if __name__ == "__main__":
    unittest.main()
