"""Release QA regression: registered U01 must have real phone-browser checks."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class U01MobileGateTest(unittest.TestCase):
    def test_registered_u01_has_browser_gate(self):
        manifest = (ROOT / "site/pages.json").read_text("utf-8")
        if "xiaoma-20261028-urosepsis-esbl-first-dose.html" not in manifest:
            self.skipTest("U01 publication candidate not yet registered")
        script = ROOT / "tools/qa_u01_mobile.py"
        self.assertTrue(script.is_file(), "Registered U01 needs a dedicated reader mobile QA")
        workflow = (ROOT / ".github/workflows/pages.yml").read_text("utf-8")
        self.assertIn("python tools/qa_u01_mobile.py", workflow)
        self.assertIn("360 375 390 1280", workflow)


if __name__ == "__main__":
    unittest.main()
