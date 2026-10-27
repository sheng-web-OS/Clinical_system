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

    def test_source_verification_appendix_stays_out_of_teaching_chapters(self):
        for phrase in (
            "### 本篇來源與版本界線",
            "## 原卷逐頁核對紀錄",
            "原始資料使用：考選部 112 年第一次醫學（三）",
        ):
            with self.subTest(phrase=phrase):
                self.assertTrue(public_copy_leak_errors(
                    "content/xiaoma-internal-medicine/lessons/gi-liver.md", phrase
                ))

    def test_verification_belongs_in_source_page_not_teaching_body(self):
        provenance = "### 本篇來源與版本界線\n原始資料使用：考選部官方試卷"
        self.assertEqual([], public_copy_leak_errors(
            "content/xiaoma-internal-medicine/exam-gi-liver-three-sources.md", provenance
        ))
        self.assertEqual([], public_copy_leak_errors(
            "content/xiaoma-internal-medicine/lessons/gi-liver.md",
            "官方答案 D（未更正）；單次 ceruloplasmin 低不能確診 Wilson disease。"
        ))

    def test_published_gi_liver_lesson_excludes_editorial_footer(self):
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        page = root / "content/xiaoma-internal-medicine/lessons/2026-10-27-gi-liver-exam-trio.md"
        content = page.read_text(encoding="utf8")
        self.assertNotIn("本篇來源與版本界線", content)
        self.assertEqual([], public_copy_leak_errors(str(page.relative_to(root)), content))
        self.assertIn("../exam-gi-liver-three-sources.md", content)
        for topic in ("Wilson disease", "Child–Pugh", "SAAG"):
            self.assertIn(topic, content)

    def test_preserved_author_original_is_unchanged(self):
        text = "使用者原始文章逐字保留，即使內有 PR #17 字樣。"
        self.assertEqual([], public_copy_leak_errors("content/xiaoma-reading/originals/example.md", text))

    def test_line_precise_error(self):
        errors = public_copy_leak_errors("content/example.md", "臨床結論。\n本輪新增六道題。")
        self.assertEqual(1, len(errors))
        self.assertIn("content/example.md:2", errors[0])


if __name__ == "__main__":
    unittest.main()
