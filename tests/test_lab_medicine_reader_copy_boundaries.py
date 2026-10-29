"""Keep editorial work logs out of Lab Medicine reader-facing draft copy.

This regression covers only the new AI-authored Lab Medicine 2026-10-27
pilot. It is not a clinical truth or independent semantic reviewer.
"""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate import public_copy_leak_errors

# Beyond the existing public-page gate, catch known worklog phrases that
# escaped because the four private drafts were not in site/pages.json.
WORKLOG = re.compile(
    r"(?:\bDraft\s*/\s*HOLD\b|本輪\s*AI|"
    r"本次.{0,40}(?:目視核對|QA|尚未核實|尚未讀取)|"
    r"本庫五年二階國考結構化資料|"
    r"正式發布前須獨立核查)",
    re.IGNORECASE,
)


class LabReaderCopyBoundariesTest(unittest.TestCase):
    def test_unpublished_lab_drafts_have_no_editorial_worklog(self):
        paths = sorted((ROOT / "content/xiaoma-internal-medicine/lessons")
                       .glob("2026-10-27-lab-medicine-*.md"))
        self.assertEqual(4, len(paths), "Pilot set must remain four distinct articles")
        for path in paths:
            with self.subTest(article=path.name):
                source = str(path.relative_to(ROOT))
                body = path.read_text(encoding="utf-8")
                self.assertFalse(public_copy_leak_errors(source, body))
                self.assertIsNone(WORKLOG.search(body))


if __name__ == "__main__":
    unittest.main()
