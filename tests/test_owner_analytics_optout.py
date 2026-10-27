"""Owner self-identification must opt out before any analytics beacon is loaded."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
import build


class OwnerAnalyticsOptOut(unittest.TestCase):
    def test_all_canonical_pages_use_a_guarded_beacon(self):
        with tempfile.TemporaryDirectory() as directory:
            dist = Path(directory)
            for filename in ("index.html", "example.html"):
                (dist / filename).write_text(
                    '<!doctype html><html><head><title>Test</title></head><body></body></html>',
                    encoding="utf-8",
                )
            with patch.object(build, "DIST", dist), patch.object(build, "PAGES", [{"output": "example.html"}]):
                build.install_web_analytics()
            for filename in ("index.html", "example.html"):
                markup = (dist / filename).read_text(encoding="utf-8")
                self.assertEqual(markup.count("static.cloudflareinsights.com/beacon.min.js"), 1)
                self.assertIn('<template id="clinical-analytics-config"', markup)
                self.assertIn('localStorage.getItem("clinical-analytics-owner-v1") === "1"', markup)
                self.assertNotIn('<script defer src="https://static.cloudflareinsights.com/beacon.min.js"', markup)
                self.assertLess(
                    markup.index('localStorage.getItem("clinical-analytics-owner-v1")'),
                    markup.index("document.head.appendChild(beacon)"),
                )

    def test_activation_is_untracked_and_browser_local(self):
        page = (ROOT / "site" / "owner-mode.html").read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex,nofollow"', page)
        self.assertIn('localStorage.setItem(key, "1")', page)
        self.assertIn('localStorage.removeItem(key)', page)
        self.assertIn('setOwner(true);', page)
        self.assertNotIn("static.cloudflareinsights.com", page)
        self.assertNotIn("navigator.userAgent", page)


if __name__ == "__main__":
    unittest.main()
