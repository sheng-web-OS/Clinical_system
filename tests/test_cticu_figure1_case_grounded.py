"""CABG Figure 1 regression against the reported abstract-card/double-arrow defect.

This is source/markup QA, not independent medical approval or screenshot review.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-27-cticu-abg-cabg-lactate.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/cticu-abg-cabg-sources.md"


def figure_one() -> str:
    document = ARTICLE.read_text(encoding="utf-8")
    tag = '<figure id="cticu-measurement-layers"'
    assert document.count(tag) == 1, "CABG figure 1 must have one stable identity"
    start = document.index(tag)
    stop = document.index("</figure>", start)
    return document[start:stop + len("</figure>")]


class CABGFigureOneContract(unittest.TestCase):
    def test_real_case_and_inference_boundaries_not_four_abstract_cards(self):
        fig = figure_one()
        for cue in ("CABG 病例 3", "14.8", "95%", "實測", "不能直接推出",
                    "Hb × SaO₂", "CaO₂ × CO → DO₂", "本病例 T1 沒有同期完整"):
            self.assertIn(cue, fig)
        self.assertNotIn("四個不能互換的觀察層次", fig)
        self.assertNotIn("SaO₂ + Hb + PaO₂", fig)

    def test_one_transition_arrow_and_stacked_phone_columns(self):
        fig = figure_one()
        transition = fig.split("共同缺的是因果證據", 1)[1].split(
            "血液每分鐘能送出多少氧？", 1)[0]
        self.assertEqual(transition.count("↓"), 1)
        self.assertIn('aria-hidden="true"', transition)
        self.assertIn("minmax(min(100%,235px),1fr)", fig)
        self.assertNotIn("↓　兩個數字", fig)

    def test_published_reader_names_correct_cabg_patient(self):
        document = ARTICLE.read_text(encoding="utf-8")
        self.assertIn("所以第三名病人的 ScvO₂ 95%", document)
        self.assertNotIn("所以第一名病人的 ScvO₂ 95%", document)

    def test_table_one_source_and_missing_data_disclosed(self):
        fig = figure_one()
        self.assertIn("Wardhana", fig)
        self.assertIn("原始研究 Table 1", fig)
        self.assertIn("不是</strong>已算出的病人數值", fig)
        self.assertIn("Wardhana", SOURCES.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
