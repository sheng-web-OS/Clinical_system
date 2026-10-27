"""Regressions for the two previously screenshot-proven mobile clipped figures.

The markup tests are not a substitute for Chromium or medical review.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIURETIC = ROOT / "content/xiaoma-reading/integrated/2026-10-22-diuretics-visual.md"
ACID = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-23-acid-base.md"
CSS = ROOT / "site/styles.css"


def figure(text, figure_id):
    start = text.index('<figure', text.index('id="' + figure_id + '"') - 45)
    return text[start:text.index('</figure>', start) + len('</figure>')]


class MobileVisualRegression(unittest.TestCase):
    def test_loop_sigmoid_keeps_threshold_and_ceiling_visible_together(self):
        body = figure(DIURETIC.read_text("utf-8"), "loop-dose-response")
        self.assertIn('class="clinical-mobile-diuresis"', body)
        self.assertIn('<svg viewBox="0 0 360 340"', body)
        self.assertIn("Threshold", body)
        self.assertIn("Ceiling", body)
        self.assertIn("瞬時排鈉反應", body)
        self.assertIn("不是臨床劑量刻度", body)
        self.assertIn("無須橫向捲動", body)

    def test_same_ph_mobile_table_fixes_ph_and_varies_both_terms(self):
        body = figure(ACID.read_text("utf-8"), "same-ph-figure")
        start = body.index('class="clinical-mobile-same-ph"')
        mobile = body[start:]
        self.assertIn("三組計算的 pH 都約 7.40", mobile)
        self.assertEqual(len(re.findall(r'<tr><td>\d+</td><td>\d+</td>', mobile)), 3)
        for numerator, denominator in ((12, 20), (24, 40), (36, 60)):
            self.assertIn(f"<tr><td>{numerator}</td><td>{denominator}</td>", mobile)
            self.assertAlmostEqual(numerator / (0.03 * denominator), 20)
        self.assertIn("非病歷", mobile)
        self.assertIn("不需左右捲動", mobile)

    def test_af_phone_flow_shows_two_antegrade_routes_and_conditional_risk(self):
        af = (ROOT / "content/xiaoma-reading/integrated/2026-10-26-preexcited-af.md").read_text("utf-8")
        body = figure(af, "af-two-exits")
        self.assertIn('class="af-desktop-conduction"', body)
        self.assertIn('class="af-mobile-conduction"', body)
        self.assertIn('viewBox="0 0 360 648"', body)
        for signal in ("AV node", "Accessory pathway", "decremental conduction",
                       "僅當 AP 可順傳", "Ventricle", "AV nodal blocker",
                       "極短 RR → VF 風險", "非所有 AP 都具高危性"):
            self.assertIn(signal, body)
        self.assertIn("脈衝數量不代表真實比率", body)
        self.assertIn("仍可能順傳", body)
        self.assertIn("傳導被抑制", body)
        self.assertIn('data-qa-flow="av-node-blocked"', body)
        self.assertIn('data-qa-flow="ap-persists"', body)
        self.assertIn("01  /  BEFORE NODAL BLOCKADE", body)
        self.assertIn("02  /  COUNTERFACTUAL", body)
        self.assertNotIn('width="328" height="112"', body)  # no old mega-card
        self.assertIn("條件式機轉示意", body)
        browser = (ROOT / "tools/visual_qa_browser.py").read_text("utf-8")
        self.assertIn("AF mobile critical labels clipped or too small", browser)
        self.assertIn("AF mobile counterfactual missing blocked-vs-persisting paths", browser)
        css = CSS.read_text("utf-8")
        self.assertIn("#af-two-exits .af-desktop-conduction{display:none}", css)
        self.assertIn("#af-two-exits .af-mobile-conduction{display:block", css)

    def test_cticu_oxygen_caption_has_no_raw_markdown_and_stays_secondary_on_phone(self):
        lesson = (ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-27-cticu-oxygen-delivery.md").read_text("utf-8")
        image = figure(lesson, "cticu-do2-two-paths")
        match = re.search(r"<figcaption>(.*?)</figcaption>", image, re.S)
        self.assertIsNotNone(match)
        caption = match.group(1)
        self.assertNotIn("**", caption, "Raw Markdown is not parsed inside HTML figcaption")
        self.assertLess(len(caption), 130, "Figure caption should not repeat source-audit prose")
        self.assertIn("表格平均 SaO₂ 不是事件同期測量值", caption)
        css = CSS.read_text("utf-8")
        self.assertIn("#cticu-do2-two-paths figcaption", css)
        self.assertIn("font-size:clamp(13px,.86rem,17px)", css)

    def test_phone_css_replaces_desktop_scroll_without_affecting_other_figures(self):
        css = CSS.read_text("utf-8")
        for fig in ("loop-dose-response", "same-ph-figure"):
            self.assertIn(f"#" + fig + " .diuretic-svg-scroll", css)
        self.assertIn(".clinical-mobile-diuresis{display:block", css)
        self.assertIn(".clinical-mobile-same-ph{display:block", css)
        self.assertIn(".clinical-mobile-same-ph table{display:table", css)


if __name__ == "__main__":
    unittest.main()
