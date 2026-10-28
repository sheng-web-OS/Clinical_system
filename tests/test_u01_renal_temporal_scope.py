"""Safety regression: a two-week-old SCr reference must not be used to assert KDIGO AKI.

This deterministic test guards the educational wording, not clinical truth.
Medical review requires primary KDIGO and the patient timeline.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "archive/pgy-antibiotics/u01/lesson.md"
ORDER = ROOT / "archive/pgy-antibiotics/u01/order-worked-example.md"
CASE = ROOT / "archive/pgy-antibiotics/u01/case-test.md"
QA = ROOT / "archive/pgy-antibiotics/u01/sources-qa.md"

class U01RenalTemporalBoundaryTest(unittest.TestCase):
    def test_aki_not_confirmed_from_old_two_week_value(self):
        text = LESSON.read_text(encoding="utf-8")
        self.assertIn("尚不足以單憑兩筆數值確認 KDIGO AKI", text)
        self.assertIn("48 小時", text)
        self.assertIn("7 天", text)
        self.assertIn("尿量", text)
        self.assertIn("高度懷疑", text)
        self.assertNotIn("CKD 上再有 AKI", text)
        self.assertNotIn("意識改變、低血壓、AKI、乳酸上升", text)
    def test_bp_must_be_interpreted_as_more_than_map_65(self):
        text = LESSON.read_text(encoding="utf-8")
        self.assertIn("MAP 約 68 mmHg", text)
        self.assertIn("不代表灌流必定充分", text)
        self.assertIn("65 歲以上", text)
    def test_order_and_testing_preserve_temporal_uncertainty(self):
        order = ORDER.read_text(encoding="utf-8")
        case = CASE.read_text(encoding="utf-8")
        self.assertIn("疑似 AKI", order)
        self.assertIn("AKI 尚未證實", case)
        self.assertIn("AKI 尚未證實", QA.read_text(encoding="utf-8"))
    def test_dosing_remains_unverified(self):
        order = ORDER.read_text(encoding="utf-8")
        self.assertIn("NOT_VERIFIED", order)
        self.assertIn("不可貼到 EMR", order)

if __name__ == "__main__":
    unittest.main()
