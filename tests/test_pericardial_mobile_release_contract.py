"""Regressions from an independent review of the Pericardial Tamponade lesson.

Static checks only: browser screenshots and clinical peer review remain separate gates.
"""
from pathlib import Path
import re
import unittest
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/pages.yml"
LESSON = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-27-pericardial-tamponade.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/pericardial-tamponade-sources.md"


class PericardialMobileReleaseContract(unittest.TestCase):
    def test_changed_figures_render_at_360_375_390_and_desktop(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(
            "python tools/visual_qa_browser.py --changed-from origin/main --widths 360 375 390 1280",
            workflow,
            "A 375px browser render is required, not just 360/390 and a claim of mobile QA.",
        )

    def test_pulsus_paradoxus_is_systolic_pressure_not_pulse_pressure(self):
        article = LESSON.read_text(encoding="utf-8")
        self.assertIn("吸氣時收縮壓下降的幅度異常增加", article)
        self.assertNotIn("異常擴大的脈壓變化", article)

    def test_reader_sources_do_not_publish_author_audit_log(self):
        source = SOURCES.read_text(encoding="utf-8")
        article = LESSON.read_text(encoding="utf-8")
        for text in (source, article):
            for internal in ("本次閱讀到", "實讀公開", "未宣稱用 PDF screenshot",
                             "不是編輯稽核或作者內部 metadata"):
                self.assertNotIn(internal, text)

    def test_mobile_causal_figure_has_readable_static_source_geometry(self):
        article = LESSON.read_text(encoding="utf-8")
        match = re.search(r'<figure id="tamponade-mechanism">([\s\S]*?)</figure>', article)
        self.assertIsNotNone(match, "The causal diagram must remain attached to its evidence.")
        svg_markup = re.search(r'<svg\b[\s\S]*?</svg>', match.group(1))
        self.assertIsNotNone(svg_markup)
        figure = ET.fromstring(svg_markup.group(0))
        _, _, width, height = [float(x) for x in figure.attrib["viewBox"].split()]
        self.assertLessEqual(width, 400, "Wide SVG causes unacceptably small phone text.")
        self.assertLessEqual(height, 750, "Keep the causal visual skimmable on a phone.")
        sizes = [float(t.attrib["font-size"]) for t in figure.iter()
                 if t.tag.endswith("text") and "font-size" in t.attrib]
        self.assertTrue(sizes)
        self.assertGreaterEqual(min(sizes), 14, "This static threshold does not replace real mobile visual QA.")


if __name__ == "__main__":
    unittest.main()
