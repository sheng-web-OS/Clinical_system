"""Evidence-driven READ/SKIP/HOLD using actual synthetic files, not source_state."""
import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.synthetic_evidence_gap_probe import probe


class RepoEvidenceProbeTests(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        (self.root / "lesson.md").write_text(
            "Synthetic lesson: see Figure F7 for the invented sample.\n", encoding="utf-8")
        (self.root / "captions").mkdir()

    def run_probe(self, article="lesson.md", captions="captions"):
        return probe(self.root, article, captions)

    def caption(self, body="Figure F7: Sample size: 12 synthetic observations\n",
                digest=True):
        path = self.root / "captions/F7.txt"
        path.write_text(body, encoding="utf-8")
        if digest:
            (self.root / "captions/F7.sha256").write_text(
                hashlib.sha256(path.read_bytes()).hexdigest(), encoding="utf-8")
        return path

    def test_missing_caption_identified_from_actual_article_not_source_flag(self):
        out = self.run_probe()
        self.assertEqual(out["decision"], "READ")
        self.assertEqual(out["reason"], "LOCAL_CAPTION_MISSING")
        self.assertEqual(out["figure"], "F7")
        self.assertEqual(out["model_calls"], 0)
        self.assertEqual(out["external_reads"], 0)

    def test_existing_anchored_caption_skips_paid_calls(self):
        self.caption()
        out = self.run_probe()
        self.assertEqual(out["decision"], "SKIP")
        self.assertEqual(out["reason"], "LOCAL_CAPTION_INTEGRITY_MATCH")
        self.assertFalse(out["clinical_provenance_verified"])
        self.assertFalse(out["autonomy_certified"])

    def test_no_figure_cue_skips_unneeded_work(self):
        (self.root / "lesson.md").write_text("Nothing about figures.\n",
                                            encoding="utf-8")
        self.assertEqual(self.run_probe()["decision"], "SKIP")

    def test_unanchored_local_source_is_held_not_assumed_verified(self):
        self.caption(digest=False)
        self.assertEqual(self.run_probe()["reason"], "INCOMPLETE_LOCAL_EVIDENCE")

    def test_missing_caption_with_orphan_hash_is_held(self):
        (self.root / "captions/F7.sha256").write_text("0" * 64)
        self.assertEqual(self.run_probe()["decision"], "HOLD")

    def test_changed_caption_after_anchor_is_held(self):
        path = self.caption()
        path.write_text("Figure F7: changed but unreviewed.\n", encoding="utf-8")
        self.assertEqual(self.run_probe()["reason"], "LOCAL_INTEGRITY_MISMATCH")

    def test_invalid_hash_format_is_held(self):
        self.caption()
        (self.root / "captions/F7.sha256").write_text("not-a-digest")
        self.assertEqual(self.run_probe()["reason"], "BAD_INTEGRITY_ANCHOR")

    def test_wrong_figure_caption_is_held(self):
        self.caption("Figure F8: This is not F7.\n")
        self.assertEqual(self.run_probe()["reason"], "CAPTION_CUE_MISSING")

    def test_conflicting_candidates_are_held(self):
        self.caption()
        (self.root / "captions/F7-copy.txt").write_text("Figure F7: conflicting copy\n")
        self.assertEqual(self.run_probe()["reason"], "CONFLICTING_LOCAL_CANDIDATES")

    def test_multiple_figures_are_held_not_blindly_read(self):
        (self.root / "lesson.md").write_text("Figure F7 and Figure F8 appear.\n",
                                            encoding="utf-8")
        self.assertEqual(self.run_probe()["reason"], "MULTIPLE_FIGURES_UNSUPPORTED")

    def test_parent_traversal_is_held(self):
        self.assertEqual(self.run_probe("../lesson.md")["reason"], "UNSAFE_PATH")

    def test_invalid_article_extension_is_held(self):
        (self.root / "lesson.txt").write_text("Figure F7\n", encoding="utf-8")
        self.assertEqual(self.run_probe("lesson.txt")["reason"], "UNSAFE_PATH")

    def test_outside_symlink_is_held(self):
        (self.root / "external.md").symlink_to("/etc/hosts")
        self.assertEqual(self.run_probe("external.md")["reason"], "UNSAFE_PATH")

    def test_oversized_article_is_held(self):
        (self.root / "lesson.md").write_text("Figure F7 " + ("x" * 70000))
        self.assertEqual(self.run_probe()["reason"], "SOURCE_UNREADABLE")

    def test_bad_utf8_is_held(self):
        (self.root / "lesson.md").write_bytes(b"\xff\xfe")
        self.assertEqual(self.run_probe()["reason"], "SOURCE_UNREADABLE")


if __name__ == "__main__":
    unittest.main()
