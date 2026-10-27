"""Prevent source-link figure metadata from claiming unverified pixel inspection.

This is a provenance regression only; it does not validate figure semantics,
licensing, or independent clinical review.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ACSFigureSourceProvenance(unittest.TestCase):
    def test_source_link_does_not_claim_pixel_inspection_without_evidence(self):
        gate = json.loads((ROOT / "audit/figure-gate.json").read_text("utf-8"))
        entry = gate["reviews"]["content/clinical-os/acs.md"]
        for item in entry["items"]:
            if item.get("mode") == "source_link" and not item.get("pixel_verified", False):
                locator = item.get("locator", "").lower()
                self.assertNotIn("displayed and assessed", locator,
                    "External caption/link access is not proof of figure-pixel inspection")

if __name__ == "__main__":
    unittest.main()
