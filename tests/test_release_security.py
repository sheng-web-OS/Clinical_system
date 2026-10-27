"""Security release regression: fake secrets are blocked; medical prose stays public."""
from pathlib import Path
import tempfile
import unittest

from tools.check_release_security import scan_dist


class ReleaseSecurityGateTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dist = Path(self.temp.name)
        self.page = self.dist / "index.html"
        self.page.write_text("<h1>Physiology</h1><p>PaCO2 45 mmHg.</p>", encoding="utf8")

    def test_safe_medical_prose_and_public_analytics_id_pass(self):
        self.page.write_text(
            "<p>OPENAI_API_KEY is an environment variable name, never paste credentials.</p>"
            '<template data-cf-beacon=\'{"token":"c6bb7055c62648c39f440da91304c99e"}\'></template>',
            encoding="utf8",
        )
        self.assertEqual([], scan_dist(self.dist))

    def test_fake_github_token_is_blocked_without_ever_echoing_value(self):
        token = "ghp_" + "F" * 36
        self.page.write_text("accidental=" + token, encoding="utf8")
        errors = scan_dist(self.dist)
        self.assertTrue(any("GitHub credential" in error for error in errors))
        self.assertNotIn(token, str(errors))

    def test_fake_openai_token_is_blocked(self):
        self.page.write_text("sk-proj-" + "A" * 32, encoding="utf8")
        self.assertTrue(any("OpenAI credential" in error for error in scan_dist(self.dist)))

    def test_fake_private_key_header_is_blocked(self):
        self.page.write_text("-----BEGIN OPENSSH PRIVATE KEY-----\\nnot-a-real-key", encoding="utf8")
        self.assertTrue(any("private key header" in error for error in scan_dist(self.dist)))

    def test_fake_api_assignment_is_blocked(self):
        self.page.write_text("CF_API_TOKEN=" + "T" * 32, encoding="utf8")
        self.assertTrue(any("API credential assignment" in error for error in scan_dist(self.dist)))

    def test_html_encoded_private_agent_marker_is_blocked(self):
        self.page.write_text(
            "<p>This is the PRIVATE source-of-truth repositor&#121;</p>", encoding="utf8"
        )
        self.assertTrue(any("private agent" in error for error in scan_dist(self.dist)))

    def test_private_file_copy_is_blocked(self):
        (self.dist / "AGENTS.md").write_text("just a filename fixture", encoding="utf8")
        self.assertTrue(any("private file/path" in error for error in scan_dist(self.dist)))

    def test_private_directory_is_blocked(self):
        (self.dist / ".github").mkdir()
        (self.dist / ".github" / "config").write_text("fixture", encoding="utf8")
        self.assertTrue(any("private file/path" in error for error in scan_dist(self.dist)))

    def test_symlink_must_not_point_outside_publish_root(self):
        (self.dist / "private-link").symlink_to(self.page)
        self.assertTrue(any("symlink forbidden" in error for error in scan_dist(self.dist)))

    def test_empty_build_fails_closed(self):
        self.page.unlink()
        self.assertTrue(scan_dist(self.dist))


if __name__ == "__main__":
    unittest.main()
