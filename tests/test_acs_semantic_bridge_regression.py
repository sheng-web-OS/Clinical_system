"""Pin ACS #169 independent-review repairs without pretending to medical approval.

These are narrow editorial regression tests: H2/exam bindings and the live CI,
an independent paragraph review, source/figure checks and clinical judgment
remain separate release gates.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACS = ROOT / "content/clinical-os/acs.md"


class ACSSemanticBridgeRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = ACS.read_text(encoding="utf-8")

    def test_primary_figure_is_read_before_secondary_and_neither_is_metadata(self):
        text = self.body
        a = text.index("## 一、先弄懂 ACS")
        b = text.index("## 二、病人抵達")
        intro = text[a:b]
        self.assertLess(intro.index("figure/F2/"), intro.index("figure/F4/"))
        self.assertIn("第一條分岔", intro)
        self.assertIn("第二條分岔", intro)
        self.assertIn("第三條分岔", intro)
        self.assertEqual(intro.count("figure/F2/"), 1)
        self.assertEqual(intro.count("figure/F4/"), 1)
        self.assertNotIn("即使同是 troponin 上升，plaque rupture、肺炎造成", intro)

    def test_cardiac_injury_example_precedes_a_separate_mino_causal_bridge(self):
        troponin = self.body.split("## 四、Troponin", 1)[1].split("## 五、風險", 1)[0]
        self.assertIn("純教學假設", troponin)
        self.assertIn("99th-percentile URL", troponin)
        self.assertRegex(troponin, r"12、68、145[\\s\\S]+?\\n\\n\\*\\*數列已回答")
        self.assertIn("造影仍未解因", troponin)
        self.assertIn("myocardial injury with non-obstructive coronary arteries", troponin)

    def test_procedure_related_mi_uses_timing_and_and_or_distinctions(self):
        intro = self.body.split("## 一、先弄懂 ACS", 1)[1].split("## 二、病人抵達", 1)[0]
        exam = self.body.split("## 十一、讓歷屆國考", 1)[1].split("## 十二、三次", 1)[0]
        for fragment in ("30 日內", "AND", "OR", "第 40 天"):
            self.assertIn(fragment, intro)
        self.assertIn("index procedure", intro)
        self.assertIn("113 年第二次", exam)
        self.assertIn("30 日內", exam)
        self.assertIn("40 日後", exam)
        self.assertIn("正式答案 D 不改", exam)
        self.assertIn("UDMI5 §7.2.3", intro)
        # If the old "one universal troponin multiple" logic returns, the
        # explicitly scoped objective-evidence decision must still be present.
        self.assertIn("冠脈程序併發症證據，加上新缺血性區域壁運動異常", intro)


if __name__ == "__main__":
    unittest.main()
