"""Tests prove that legacy debt is not approved and new/edited visuals fail closed."""
import json
import struct
import sys
import zlib
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "site"))
from visual_quality import audit, extract_figures, fingerprint, screenshot_filename

SOURCE = "content/lesson.md"
OLD = '<figure id="map"><section>概念一</section><figcaption>來源</figcaption></figure>'
NEW = '<figure id="map"><svg role="img" aria-label="方向"><path d="M1 1L2 2"/></svg><figcaption>證據</figcaption></figure>'


class SiteVisualQualityAudit(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        for name in ("content", "site", "audit/visual-evidence"):
            (self.root / name).mkdir(parents=True)
        (self.root / SOURCE).write_text(OLD, encoding="utf-8")
        (self.root / "site/pages.json").write_text(json.dumps([{"source": SOURCE, "output": "lesson.html"}]), encoding="utf-8")
        self.baseline = {"figures": {SOURCE: [{
            "id": "map", "fingerprint": fingerprint(OLD), "kind": "html_css",
            "status": "legacy_unreviewed"}]}}
        (self.root / "audit/visual-legacy-baseline.json").write_text(json.dumps(self.baseline), encoding="utf-8")
        self.reviews = {"reviews": {}}
        self.save_reviews()

    def save_reviews(self):
        (self.root / "audit/visual-qa-reviews.json").write_text(json.dumps(self.reviews), encoding="utf-8")

    def test_old_card_is_debt_not_quality_certification(self):
        result = audit(self.root)
        self.assertEqual(result["summary"]["legacy_pending"], 1)
        self.assertEqual(result["summary"]["approved"], 0)
        self.assertEqual(result["figures"][0]["kind"], "html_css")

    def test_modified_card_cannot_reuse_legacy_exception(self):
        (self.root / SOURCE).write_text(NEW, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Visual QA HOLD"):
            audit(self.root)

    def test_new_figure_cannot_be_certified_by_text_claim_alone(self):
        (self.root / SOURCE).write_text(NEW, encoding="utf-8")
        self.reviews["reviews"][SOURCE + "#map"] = {
            "status": "approved", "fingerprint": fingerprint(NEW),
            "reviewer_type": "independent_ai",
            "reader_misconception": "This is a long statement explaining an actual reading error.",
            "unique_visual_insight": "This is a long claim about how the diagram helps inference.",
            "deletion_test": "Removing this diagram would remove a concrete unique insight.",
            "medical_source_and_limits": "This is a source-based bounded statement identifying the diagnostic limits of this chart.",
            "desktop_findings": "Labels and chart are readable at desktop viewport.",
            "mobile_findings": "Labels and diagram are readable at mobile viewport.",
            "counterexample_check": "Checked conditions when inference fails.",
        }
        self.save_reviews()
        with self.assertRaisesRegex(ValueError, "mobile_360_screenshot"):
            audit(self.root)

    def test_screenshots_are_not_approvable_by_unrelated_text_files(self):
        self.assertFalse(__import__("visual_quality").screenshot_check(self.root, "README.md"))
        self.assertFalse(__import__("visual_quality").screenshot_check(self.root, "audit/visual-evidence/nonexistent.png"))

    def test_unicode_version_fingerprint_and_source_location(self):
        r = extract_figures("第一行\n" + OLD)
        self.assertEqual(r[0]["line"], 2)
        self.assertEqual(r[0]["fingerprint"], fingerprint(OLD))


    def save_png(self, name, width, height=240):
        """Create a tiny *valid* PNG; screenshot QA still requires a real visual review."""
        def chunk(tag, data):
            return (struct.pack(">I", len(data)) + tag + data +
                    struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))
        raw = (b"\x00" + b"\x52\x86\xa1" * width) * height
        png = (b"\x89PNG\r\n\x1a\n" +
               chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) +
               chunk(b"IDAT", zlib.compress(raw)) +
               chunk(b"tEXt", b"visual-evidence\x00" + b"fixture" * 36) +
               chunk(b"IEND", b""))
        (self.root / "audit/visual-evidence" / name).write_bytes(png)

    def approve_fixture(self, markup=NEW):
        (self.root / SOURCE).write_text(markup, encoding="utf-8")
        fp = fingerprint(markup)
        key = SOURCE + "#map"
        record = {
            "status": "approved", "fingerprint": fp,
            "reviewer_type": "independent_ai",
            "reader_misconception": "The reader may confuse a categorization with a treatment decision.",
            "unique_visual_insight": "The diagram makes the conditional branching visible in context.",
            "deletion_test": "Removing this diagram loses the explicit counterfactual decision branch.",
            "medical_source_and_limits": "This teaching model is a simulation and is not a patient observation or clinical prescription.",
            "desktop_findings": "Verified the exact figure in context at a desktop width using real rendered pixels.",
            "mobile_findings": "Verified at both 360 and 390px and inspected readability of the labels.",
            "counterexample_check": "Changed the condition and verified the decision is different.",
        }
        for field, viewport, image_width in (
            ("mobile_360_screenshot", 360, 320),
            ("mobile_390_screenshot", 390, 340),
            ("desktop_screenshot", 1280, 760),
        ):
            name = screenshot_filename(key, fp, viewport)
            self.save_png(name, image_width)
            record[field] = "audit/visual-evidence/" + name
        self.reviews["reviews"][key] = record
        self.save_reviews()
        return record

    def test_viewport_version_bound_evidence_allows_structural_acceptance(self):
        self.approve_fixture()
        result = audit(self.root)
        self.assertEqual(result["summary"]["approved"], 1)
        # Not certification of actual pedagogy: this fixture simply proves the gate works.

    def test_same_screenshot_cannot_stand_in_for_two_phone_viewports(self):
        record = self.approve_fixture()
        record["mobile_390_screenshot"] = record["mobile_360_screenshot"]
        self.save_reviews()
        with self.assertRaisesRegex(ValueError, "mobile_390_screenshot"):
            audit(self.root)

    def test_mobile_screenshot_larger_than_viewport_fails(self):
        record = self.approve_fixture()
        file = self.root / record["mobile_360_screenshot"]
        self.save_png(file.name, 500)
        with self.assertRaisesRegex(ValueError, "mobile_360_screenshot"):
            audit(self.root)

    def test_figure_change_invalidates_screen_capture(self):
        self.approve_fixture()
        (self.root / SOURCE).write_text(NEW.replace("方向", "另一種方向"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "different figure version"):
            audit(self.root)

    def test_source_image_requires_nonempty_alt(self):
        markup = ('<figure id="map"><img src="/real-ecg.png" alt="">'
                  '<figcaption>真實來源心電圖</figcaption></figure>')
        self.approve_fixture(markup)
        with self.assertRaisesRegex(ValueError, "nonempty alt text"):
            audit(self.root)

    def test_role_alone_does_not_name_svg(self):
        markup = ('<figure id="map"><svg role="img"><path d="M1 1L2 2"/></svg>'
                  '<figcaption>來源</figcaption></figure>')
        self.approve_fixture(markup)
        with self.assertRaisesRegex(ValueError, "SVG lacks"):
            audit(self.root)



if __name__ == "__main__":
    unittest.main()
