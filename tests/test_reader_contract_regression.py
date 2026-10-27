"""Mechanical regressions for the reader boundary; no clinical/model efficacy claims."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE_ROOT = Path(__file__).resolve().parents[1]


class ReaderContractRegression(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for directory in ("site", "tools", "content", "audit", "dist"):
            (self.root / directory).mkdir()
        for relative in ("site/catalog.py", "site/figure_gate.py", "site/exam_archive.py", "tools/check_output.py", "tools/validate.py"):
            shutil.copyfile(SOURCE_ROOT / relative, self.root / relative)
        (self.root / "content/example.md").write_text("# Public engineering fixture\n", encoding="utf8")
        self.page = {"source": "content/example.md", "output": "example.html", "title": "Example", "subtitle": "Teaching"}
        self.set_catalog([self.page])
        for name in ("styles.css", "home.css", "app.js", ".nojekyll"):
            (self.root / "dist" / name).write_text("", encoding="utf8")
        # Canonical pages carry an inert beacon config; runtime JS loads it
        # only for non-owners, after checking the local browser marker.
        beacon = """<template id="clinical-analytics-config" data-src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token":"fixture"}'></template>
<script>if (localStorage.getItem("clinical-analytics-owner-v1") === "1") return;
document.head.appendChild(beacon);</script>"""
        (self.root / "dist/index.html").write_text('<h1>小麻閱讀</h1><div class="library-grid"></div>' + beacon, encoding="utf8")
        (self.root / "dist/example.html").write_text("<h1>Public engineering fixture</h1>" + beacon, encoding="utf8")
        shutil.copyfile(SOURCE_ROOT / "site/owner-mode.html", self.root / "dist/owner-mode.html")
        self.index = [{"title": "Example", "url": "example.html", "text": "Public engineering fixture"}]
        self.set_search(self.index)

    def set_catalog(self, rows):
        (self.root / "site/pages.json").write_text(json.dumps(rows), encoding="utf8")

    def set_search(self, rows, inline=None):
        (self.root / "dist/site-index.json").write_text(json.dumps(rows), encoding="utf8")
        (self.root / "dist/site-index.js").write_text("window.CLINICAL_INDEX = " + json.dumps(rows if inline is None else inline) + ";", encoding="utf8")

    def check(self):
        return subprocess.run([sys.executable, str(self.root / "tools/check_output.py")], capture_output=True, text=True, timeout=10)

    def assert_blocked(self, reason):
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(reason, result.stdout + result.stderr)

    def test_public_catalog_does_not_require_private_pilot(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_canonical_page_without_analytics_beacon_is_blocked(self):
        (self.root / "dist/example.html").write_text("<h1>Public engineering fixture</h1>", encoding="utf8")
        self.assert_blocked("expected 1 analytics beacon(s), found 0")

    def test_duplicate_analytics_beacon_is_blocked(self):
        path = self.root / "dist/example.html"
        document = path.read_text("utf8")
        beacon = document[document.index("<template"):]
        path.write_text(document + beacon, encoding="utf8")
        self.assert_blocked("expected 1 analytics beacon(s), found 2")

    def test_public_source_validation_does_not_require_private_pilot(self):
        result = subprocess.run([sys.executable, str(self.root / "tools/validate.py")], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_explicit_private_pilot_validation_keeps_source_requirements(self):
        result = subprocess.run([sys.executable, str(self.root / "tools/validate.py"), "--private-pilot"], capture_output=True, text=True, timeout=10)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("tamponade.md", result.stdout + result.stderr)

    def test_audit_cannot_enter_public_catalog(self):
        (self.root / "audit/status.md").write_text("Private editorial fixture", encoding="utf8")
        self.set_catalog([dict(self.page, source="audit/status.md")])
        self.assert_blocked("internal audit/ stays private")

    def test_private_pilot_cannot_enter_hidden_navigation(self):
        (self.root / "content/tamponade.md").write_text("Private pilot fixture", encoding="utf8")
        self.set_catalog([dict(self.page, source="content/tamponade.md", navigation=False)])
        self.assert_blocked("Internal Tamponade pilot stays private")

    def test_symlink_into_private_audit_is_rejected(self):
        (self.root / "audit/status.md").write_text("Private editorial fixture", encoding="utf8")
        (self.root / "content/leak.md").symlink_to(self.root / "audit/status.md")
        self.set_catalog([dict(self.page, source="content/leak.md")])
        self.assert_blocked("Public source resolves into a private directory")

    def test_symlink_to_private_pilot_is_rejected(self):
        (self.root / "content/tamponade.md").write_text("Private pilot fixture", encoding="utf8")
        (self.root / "content/leak.md").symlink_to(self.root / "content/tamponade.md")
        self.set_catalog([dict(self.page, source="content/leak.md")])
        self.assert_blocked("Internal Tamponade pilot stays private")

    def test_search_index_cannot_list_private_destination(self):
        self.set_search([dict(self.index[0], url="tamponade.html")])
        self.assert_blocked("Search index does not match the public catalog")

    def test_inline_search_must_match_json(self):
        self.set_search(self.index, inline=[dict(self.index[0], url="tamponade.html")])
        self.assert_blocked("Inline search payload differs")

    def test_public_page_cannot_disappear_from_search(self):
        self.set_search([])
        self.assert_blocked("Search index does not match the public catalog")

    def test_unexpected_output_remains_blocked(self):
        (self.root / "dist/internal.html").write_text("<h1>Private fixture</h1>", encoding="utf8")
        self.assert_blocked("Output whitelist mismatch")

    def test_broken_local_links_remain_blocked(self):
        (self.root / "dist/example.html").write_text('<h1>Example</h1><a href="absent.html">Missing</a>', encoding="utf8")
        self.assert_blocked("broken local asset")


if __name__ == "__main__":
    unittest.main()
