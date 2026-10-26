"""Protect the source-specific DVT/PE logic recovered from Pocket Medicine 9E."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "content/xiaoma-reading/integrated/2026-10-26-vte-visual.md"
SOURCES = ROOT / "content/xiaoma-reading/vte-sources.md"


class VTESourceContext(unittest.TestCase):
    def test_distinct_wells_conventions_and_stopping_conditions(self):
        article = ARTICLE.read_text(encoding="utf-8")
        self.assertIn("≤0 分為 low、1–2 分為 moderate、≥3 分為 high", article)
        self.assertIn("≤4 分為 unlikely、>4 分為 likely", article)
        self.assertIn("≤1 分為 unlikely、≥2 分為 likely", article)
        self.assertIn("6–8 天後重複 proximal ultrasound", article)
        self.assertIn("不是所有陰性超音波都一律六到八天後重做", article)
        self.assertIn("影像品質與 clinical suspicion 是否一致", article)

    def test_prophylaxis_and_d_dimer_are_not_universal_recipes(self):
        article = ARTICLE.read_text(encoding="utf-8")
        self.assertIn("pharmacologic prophylaxis", article)
        self.assertIn("不能直接取代骨科手術", article)
        self.assertIn("FEU 與 DDU 並不等價", article)
        self.assertIn("不是把原圖所有寫著", article)
        self.assertIn("obstructive shock", article)

    def test_source_recovery_remains_selective(self):
        article = ARTICLE.read_text(encoding="utf-8")
        sources = SOURCES.read_text(encoding="utf-8")
        self.assertEqual(article.count("<figure"), 1)
        self.assertIn('id="vte-d-dimer-bayes"', article)
        self.assertIn("NICE NG158 官方診斷流程 PDF", article)
        self.assertIn("三張小麻原圖的選擇性脈絡回收", sources)
        self.assertIn("沒有把三張原書截圖整頁貼到正式站", sources)


if __name__ == "__main__":
    unittest.main()
