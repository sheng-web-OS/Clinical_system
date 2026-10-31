"""Narrative and evidence provenance regression for rewritten ESBL public reader."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-28-urosepsis-esbl-first-dose.md"
SOURCE = ROOT / "content/xiaoma-internal-medicine/urosepsis-esbl-first-dose-sources.md"


class U01PublicReaderCandidateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = READER.read_text(encoding="utf8")
        cls.sources = SOURCE.read_text(encoding="utf8")

    def test_case_one_symptoms_evaluation_and_day_three_ast_not_backfilled(self):
        t = self.text
        for cue in ("28 歲女性", "83/44", "HR 117", "CVA tenderness",
                    "妊娠陰性", "CT", "ceftriaxone", "第 3 天", "ESBL",
                    "meropenem", "第 4 天", "第 5 天", "沒有對照組"):
            with self.subTest(cue=cue):
                self.assertIn(cue, t)
        self.assertLess(t.index("83/44"), t.index("第 3 天"))
        self.assertIn("https://www.mdpi.com/2079-6382/10/5/533", t)

    def test_case_two_advance_therapy_does_not_replace_source_control(self):
        s = self.text.split("## 第二問｜", 1)[1].split("## 第三問｜", 1)[0]
        for cue in ("81 歲日本女性", "68/36", "UPJ", "PCN",
                    "cefcapene pivoxil", "carbapenem", "第 4 天",
                    "第 65 天", "hydrocortisone", "PMX-DHP", "不是",
                    "感染源控制"):
            with self.subTest(cue=cue):
                self.assertIn(cue, s)
        self.assertIn("academic.oup.com/omcr/article/", s)
        self.assertIn("cefcapene pivoxil", self.sources)
        self.assertIn("沒有報告一份在本次入院前已知 ESBL", self.sources)

    def test_no_prior_esbl_ast_fabricated_in_either_real_case(self):
        t = self.text
        for cue in ("兩例都沒有提供首劑前已知 ESBL 舊培養 AST",
                    "既往 cephalosporin", "本次菌必然相同",
                    "當次 AST 未知", "條件性"):
            with self.subTest(cue=cue):
                self.assertIn(cue, t)
        self.assertNotIn("病例為人工合成", t)

    def test_empiric_vs_definitive_and_board_question(self):
        t = self.text
        for cue in ("IDSA 2025 cUTI", "IDSA 2026 AMR Guidance",
                    "經驗性", "確定性治療", "超出", "MERINO",
                    "111 年第二次", "醫學（三）第 60 題",
                    "../urosepsis-esbl-first-dose-sources.md"):
            with self.subTest(cue=cue):
                self.assertIn(cue, t)
        for cue in ("IDSA 2026", "IDSA 2025", "SSC 2026",
                    "KDIGO 2012", "MERINO", "t=Q", "t=S", "t=M"):
            with self.subTest(source_cue=cue):
                self.assertIn(cue, self.sources)

    def test_article_title_matches_catalog_and_no_order_ready_examples(self):
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        rows = [p for p in pages if p.get("source") == str(READER.relative_to(ROOT))]
        self.assertEqual(len(rows), 1)
        self.assertEqual(self.text.splitlines()[0], "# " + rows[0]["title"])
        self.assertIn("第三問｜那麼，真正遇到", rows[0]["exam_questions"][0]["concept_heading"])
        for bad in ("Draft/HOLD", "PR #", "Issue #", "site/pages.json",
                    "meropenem 1 g q8h", "500 mL bolus", "<box></box>"):
            self.assertNotIn(bad, self.text)


if __name__ == "__main__":
    unittest.main()
