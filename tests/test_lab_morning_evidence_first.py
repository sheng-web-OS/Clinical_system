"""Real-case source identity and reader-facing topic coherence; not learning validation."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/lab-morning-sheet-sources.md"


class LabEvidenceFirstIdentity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = ARTICLE.read_text(encoding="utf-8")
        cls.sources = SOURCES.read_text(encoding="utf-8")

    def test_real_case_identity_and_treatment_confounding(self):
        for cue in ("AML", "206.8", "90% blasts", "12:00", "20:03",
                    "20:48", "23:37", "6.7", "7.8", "3.6", "氣送管",
                    "降鉀治療", "30 分鐘", "運送改變", "治療作用"):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.body)
        self.assertIn("link.springer.com/article/10.1186/s12245-024-00734-x", self.body)
        self.assertIn("PMC11462689", self.sources)

    def test_thrombocytosis_is_separate_case_not_aml_invented_platelets(self):
        for cue in ("62 歲", "essential thrombocythemia", "1305",
                    "6.3", "4.6", "3.4", "plasma", "serum"):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.body)
        self.assertIn("PMC5806620", self.sources)

    def test_two_separate_cohorts_have_correct_selection(self):
        for cue in ("66", "399", "95%", "6%", "2,440", "1,576",
                    "864", "597", "重抽"):
            with self.subTest(cue=cue):
                self.assertIn(cue, self.sources)
        self.assertIn("PMC7673871", self.body)
        self.assertIn("PMC11908522", self.body)
        self.assertIn("不能搬來保證", self.body)

    def test_old_synthetic_patient_and_metadata_do_not_reappear(self):
        for bad in ("Cr 1.16", "75 kg", "本篇不必自行捏造",
                    "從原表抽出", "舊版用一名 AI", "## 後段合成練習"):
            with self.subTest(bad=bad):
                self.assertNotIn(bad, self.body)
        self.assertIn("檢體", self.body)
        self.assertIn("危險", self.body)

    def test_scope_and_public_title_match(self):
        self.assertIn("第一篇", self.body.splitlines()[0])
        self.assertIn("先確認數字是否真的代表病人", self.body.splitlines()[0])
        self.assertIn("獨立教材", self.body)
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        rows = [r for r in pages if r.get("source") == str(ARTICLE.relative_to(ROOT))]
        self.assertEqual(len(rows), 1)
        self.assertEqual(self.body.splitlines()[0], "# " + rows[0]["title"])
        self.assertTrue(rows[0].get("references"))
        qa = (ROOT / "tools/qa_lab_morning_draft.py").read_text(encoding="utf-8")
        self.assertIn("canonical_row()", qa)
        self.assertIn("Article H1 differs from site/pages.json title", qa)

    def test_source_page_agrees_with_primary_evidence(self):
        for locator in ("PMC11462689", "PMC7673871", "PMC11908522"):
            with self.subTest(locator=locator):
                self.assertIn(locator, self.sources)
        self.assertIn("補充案例（非目前文章主故事）", self.sources)


if __name__ == "__main__":
    unittest.main()
