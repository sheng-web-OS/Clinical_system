from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEXT = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-26-copd-emptying.md"


class COPDReaderConsistencyTests(unittest.TestCase):
    def test_tlc_caption_does_not_claim_a_removed_80_percent_figure_rule(self):
        text = TEXT.read_text("utf-8")
        self.assertNotIn("圖中使用的 TLC <80% predicted", text)
        self.assertIn("LLN", text)

    def test_source_note_does_not_claim_an_absent_reproduced_table(self):
        text = TEXT.read_text("utf-8")
        self.assertNotIn("下方小麻表取自 GOLD 2024 脈絡，保留原列與註腳", text)
        self.assertIn('id="copd-treatment-targets"', text)
        self.assertIn("GOLD 2024", text)

    def test_bedside_paragraph_has_real_newlines(self):
        text = TEXT.read_text("utf-8")
        self.assertNotIn(r"\n\n床邊", text)
        self.assertIn("flow–time curve", text)


if __name__ == "__main__":
    unittest.main()
