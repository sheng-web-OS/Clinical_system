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
        self.assertIn("\n\n**數列已回答", troponin)
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


    def test_procedure_mi_box5_clinical_entry_precedes_and_or_confirmation(self):
        """UDMI5 Box 5: clinical/ECG trigger plus acute injury precede confirmatory imaging."""
        intro = self.body.split("## 一、先弄懂 ACS", 1)[1].split("## 二、病人抵達", 1)[0]
        paragraph = next(p for p in intro.split("\n\n") if p.startswith("**第三條分岔"))
        for cue in ("急性心肌傷害", "缺血症狀", "新缺血性 ECG", "鎮靜", "術前基線"):
            self.assertIn(cue, paragraph)
        self.assertLess(paragraph.index("急性心肌傷害"), paragraph.index("正式確認需要"))
        self.assertIn("AND／OR", paragraph)



    def test_post_mi_acute_mr_distinguishes_immediate_dysfunction_from_delayed_rupture(self):
        """AHA 2021 mechanical complications: immediate MR is not synonymous with rupture."""
        section = self.body.split("## 十、導管已經成功", 1)[1].split("## 十一、讓歷屆國考", 1)[0]
        self.assertIn("乳突肌缺血性功能失調", section)
        self.assertIn("乳突肌破裂通常", section)
        self.assertIn("數日", section)
        self.assertLess(section.index("乳突肌缺血性功能失調"), section.index("乳突肌破裂通常"))
        case = self.body.split("## 十二、三次反事實", 1)[1]
        self.assertIn("剛完成 PCI", case)
        self.assertIn("數日後", case)


    def test_stemi_j_point_thresholds_and_non_exclusion_boundary(self):
        """2025 ACC/AHA Table 3 / ESC 2023: sex-age-specific STE criteria are not a rule-out."""
        section = self.body.split("## 三、ECG", 1)[1].split("## 四、Troponin", 1)[0]
        for cue in ("J-point", "至少兩個相鄰導程", "≥2.5 mm", "≥2 mm",
                    "≥1.5 mm", "≥1 mm", "LVH", "LBBB",
                    "不能排除", "2025 ACC/AHA", "2023 ESC"):
            self.assertIn(cue, section)
        self.assertLess(section.index("J-point"), section.index("de Winter pattern"))

if __name__ == "__main__":
    unittest.main()
