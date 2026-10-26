"""DCM publisher imagery: deterministic, byte-identical original figures only."""
import hashlib
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("fetch_dcm_figures", ROOT / "tools/fetch_dcm_figures.py")
fetcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fetcher)


class DCMArchivedSourceTest(unittest.TestCase):
    def test_complete_publisher_archive_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(fetcher, "fetch", side_effect=AssertionError("network must not be used")):
                with patch.object(sys, "argv", ["fetch_dcm_figures.py", tmp]):
                    fetcher.main()
            for name, digest in fetcher.ARCHIVED_SHA256.items():
                image = (Path(tmp) / "assets" / name).read_bytes()
                self.assertEqual(hashlib.sha256(image).hexdigest(), digest)
                self.assertTrue(fetcher.is_image(image, Path(name).suffix))

    def test_tampered_archive_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "archive"
            archive.mkdir()
            for name in fetcher.IMAGES:
                shutil.copyfile(fetcher.ARCHIVE / name, archive / name)
            damaged = archive / "dcm-secondary-mr.png"
            damaged.write_bytes(damaged.read_bytes() + b"corrupted")
            with patch.object(fetcher, "ARCHIVE", archive):
                with patch.object(fetcher, "fetch", side_effect=AssertionError("no network fallback on tampering")):
                    with patch.object(sys, "argv", ["fetch_dcm_figures.py", str(Path(tmp) / "dist")]):
                        with self.assertRaisesRegex(RuntimeError, "archived original DCM figure modified"):
                            fetcher.main()


if __name__ == "__main__":
    unittest.main()
