"""Tests prove that legacy debt is not approved and new/edited visuals fail closed."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "site"))
from visual_quality import audit, extract_figures, fingerprint

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
        with self.assertRaisesRegex(ValueError, "desktop_screenshot"):
            audit(self.root)

    def test_screenshots_are_not_approvable_by_unrelated_text_files(self):
        self.assertFalse(__import__("visual_quality").screenshot_check(self.root, "README.md"))
        self.assertFalse(__import__("visual_quality").screenshot_check(self.root, "audit/visual-evidence/nonexistent.png"))

    def test_unicode_version_fingerprint_and_source_location(self):
        r = extract_figures("第一行\n" + OLD)
        self.assertEqual(r[0]["line"], 2)
        self.assertEqual(r[0]["fingerprint"], fingerprint(OLD))


if __name__ == "__main__":
    unittest.main()
