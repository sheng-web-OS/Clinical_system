"""Resilience of pinned open-license ECG originals without silent source substitution."""
import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/fetch_arrhythmia_figures.py"
spec = importlib.util.spec_from_file_location("fetch_arrhythmia_figures", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class OriginalECGCache(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / "tools").mkdir()
        fake = self.root / "tools/fetch_arrhythmia_figures.py"
        self.image = (
            bytes.fromhex("ffd8ffc0001108") +
            (536).to_bytes(2, "big") + (753).to_bytes(2, "big") +
            bytes([3, 1, 0x11, 0, 2, 0x11, 0, 3, 0x11, 0]) +
            b"X" * 8000 + bytes.fromhex("ffd9"))
        self.sha = hashlib.sha256(self.image).hexdigest()
        self.filename = "test-reference-ecg.jpg"
        self.fake_module = str(fake)
        self.original = (module.__file__, module.FIGURES, module.EXPECTED_SHA256)
        module.__file__ = self.fake_module
        module.FIGURES = {self.filename: ("https://source.example/image", (753,536))}
        module.EXPECTED_SHA256 = {self.filename: self.sha}
        self.addCleanup(self.restore)

    def restore(self):
        module.__file__, module.FIGURES, module.EXPECTED_SHA256 = self.original

    def test_pinned_cache_avoids_network(self):
        cache = self.root / ".figure-cache" / "silverman2018"
        cache.mkdir(parents=True)
        (cache / self.filename).write_bytes(self.image)
        with patch.object(module, "original_figure", side_effect=AssertionError("network not permitted")):
            with patch.object(sys, "argv", ["fetch_arrhythmia_figures.py", str(self.root / "dist")]):
                module.main()
        self.assertEqual((self.root / "dist/assets" / self.filename).read_bytes(), self.image)

    def test_corrupted_cache_never_bypasses_hash_validation(self):
        cache = self.root / ".figure-cache" / "silverman2018"
        cache.mkdir(parents=True)
        (cache / self.filename).write_bytes(self.image[:-3] + b"YZZ")
        with patch.object(module, "original_figure", return_value=self.image) as network:
            with patch.object(sys, "argv", ["fetch_arrhythmia_figures.py", str(self.root / "dist")]):
                module.main()
        network.assert_called_once()
        self.assertEqual((cache / self.filename).read_bytes(), self.image)


if __name__ == "__main__":
    unittest.main()
