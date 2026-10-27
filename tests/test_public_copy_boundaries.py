"""Regression: a public medical page must not expose editorial operations."""
import unittest

from tools.validate import public_copy_leak_errors


class PublicCopyBoundariesTest(unittest.TestCase):
    def test_operational_metadata_is_blocked(self):
        for phrase in (
            "本次新增獨立題號（113 Q6、114 Q6）",
            "隨文題目與獨立詳解不重複計數。",
            "原已收錄於基礎二十題。",
            "ACLS 決策主圖已透過 PR #96 發布",
            "GitHub Issue #79 要繼續驗收",
            "GitHub Actions run 40367245047",
            "Cloudflare production commit b39373c28",
            "PR #123 Draft/HOLD",
        ):
            with self.subTest(phrase=phrase):
                self.assertTrue(public_copy_leak_errors("content/reader.md", phrase))

    def test_necessary_medical_limitations_are_not_blocked(self):
        for phrase in (
            "cTn 超過 99th percentile 並不能單獨證明 MI。",
            "這項來源只核對 Table 1，未完成全篇獨立醫師審查。",
            "依當年考選部官方答案作答，但治療須對讀 2025 指引。",
            "Figure 2-3 的陰性影像需要和前測機率一起理解。",
            "目前尚無足夠證據排除高風險 PE。",
        ):
            with self.subTest(phrase=phrase):
                self.assertEqual([], public_copy_leak_errors("content/reader.md", phrase))

    def test_preserved_author_original_is_unchanged(self):
        text = "使用者原始文章逐字保留，即使內有 PR #17 字樣。"
        self.assertEqual([], public_copy_leak_errors("content/xiaoma-reading/originals/example.md", text))

    def test_line_precise_error(self):
        errors = public_copy_leak_errors("content/example.md", "臨床結論。\n本輪新增六道題。")
        self.assertEqual(1, len(errors))
        self.assertIn("content/example.md:2", errors[0])


if __name__ == "__main__":
    unittest.main()
