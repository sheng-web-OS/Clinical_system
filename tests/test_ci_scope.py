"""Regression tests: private intake CI cannot become a publication bypass."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from classify_ci_scope import classify, parse_nul_paths, private_intake_path


class CIScopeTest(unittest.TestCase):
    def test_private_intake_only_avoids_redundant_site_build(self):
        self.assertEqual(classify([
            "archive/xiaoma-reading/intake/2026-07-19-hbv.md",
            "archive/xiaoma-reading/intake/2026-10-21-chat-manuscripts.md",
        ]), "private_intake")

    def test_no_changes_fails_closed(self):
        self.assertEqual(classify([]), "full_site")

    def test_any_public_page_or_manifest_requires_full_build(self):
        for path in [
            "content/xiaoma-reading/integrated/example.md",
            "site/pages.json", "site/styles.css", "site/figure_gate.py",
            "audit/figure-gate.json", "audit/visual-qa-reviews.json",
            ".github/workflows/pages.yml", "tools/check_corpus_inventory.py",
            "tests/test_ci_scope.py", "docs/publication.md",
        ]:
            with self.subTest(path=path):
                self.assertEqual(classify([
                    "archive/xiaoma-reading/intake/2026-07-19-hbv.md", path,
                ]), "full_site")

    def test_private_name_prefix_must_be_exact_and_safe(self):
        for path in [
            "archive/xiaoma-reading/intake", "archive/xiaoma-reading/intake/",
            "archive/xiaoma-reading/intake-other/example.md",
            "archive/xiaoma-reading/intake/../other.md",
            "/archive/xiaoma-reading/intake/test.md",
            "archive/xiaoma-reading/intake\\test.md",
            "archive/xiaoma-reading/intake/test.md\nsite/pages.json",
        ]:
            with self.subTest(path=path):
                self.assertFalse(private_intake_path(path))
                self.assertEqual(classify([path]), "full_site")

    def test_nul_delimited_unicode(self):
        path = "archive/xiaoma-reading/intake/肝硬化.md"
        self.assertEqual(parse_nul_paths((path + "\0").encode("utf8")), [path])
        with self.assertRaises(ValueError):
            parse_nul_paths(b"archive/xiaoma-reading/intake/test.md")


if __name__ == "__main__":
    unittest.main()
