"""EPQC release evidence regressions. No test pretends to grade clinical meaning."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from semantic_gate import (is_teaching_page, git_blob_sha, reading_units,
                           validate_semantic_gate)

PATH = "content/xiaoma-internal-medicine/lessons/new-reasoning.md"
ARTICLE = """# 從低血壓到灌流推論

血壓很低是循環失衡的線索，卻無法單獨指出低心輸出、血管擴張或相對容量不足是哪一個機轉。

下一步必須整合末梢灌流、尿量、肺部積液與床邊超音波，因為單一血壓值不告訴我們哪個環節出問題。

即使接受初始輸液後血壓升高，若組織灌流仍然不足，還要重新評估升壓劑、心肌收縮與持續失血等其他可能。
"""


def valid_review(text):
    data = text.encode("utf-8")
    return {
        "content_blob": git_blob_sha(data),
        "reviewer_context": "independent_ai_pass",
        "reviewer_reference": "tests/isolated-independent-review-run",
        "core_reader_question": "血壓為何不能單獨解釋器官灌流變化，以及哪些資訊能真正縮小機轉？如果只讀一個數值，會錯過什麼重要的臨床機制與反例？",
        "new_understanding": "分開壓力與有效器官灌流，用其他床邊資料區分低心輸出和血管阻力，並從資訊更新的方向說明為什麼處置不能只看血壓上升。",
        "strongest_counterargument": "此段落或許只是常見重症評估用語，需要確認不是換句話說的重複句；若內容沒有明確增量，應刪除，而不是自動給予高分。",
        "epqc_scores": {k: 4 for k in "ABCDEFG"},
        "hard_stops": {k: False for k in (
            "unsafe_claim", "fabricated_evidence", "broken_causal_bridge",
            "internal_metadata", "unresolved_source_conflict")},
        "paragraphs": {
            u["id"]: {
                "role": "causal_bridge",
                "reader_gain": f"讀完第{i}個單元，讀者會把血壓數值和器官灌流原因分開推理。",
                "nonredundancy_reason": f"第{i}段獨立承擔判斷鏈的不同部分，不能由前段直接取代。",
                "verdict": "keep",
            } for i, u in enumerate(reading_units(text), 1)
        }
    }


class SemanticGateContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for d in ("content/xiaoma-internal-medicine/lessons", "audit"):
            (self.root / d).mkdir(parents=True, exist_ok=True)
        self.source = self.root / PATH
        self.source.write_text(ARTICLE, encoding="utf-8")
        self.row = {"source": PATH, "kind": "ai_integrated"}
        self.frozen = {}
        self.reviews = {}
        self.write()

    def write(self):
        (self.root / "audit/editorial-semantic-baseline.json").write_text(
            json.dumps({"schema_version": 1, "legacy_blobs": self.frozen}), encoding="utf-8")
        (self.root / "audit/editorial-semantic-reviews.json").write_text(
            json.dumps({"schema_version": 1, "reviews": self.reviews}), encoding="utf-8")

    def errors(self):
        self.write()
        return validate_semantic_gate(self.root, [self.row])

    def test_new_article_fails_closed(self):
        self.assertIn("SEMANTIC_HOLD", " ".join(self.errors()))

    def test_complete_distinct_review_passes_evidence_gate(self):
        self.reviews[PATH] = valid_review(ARTICLE)
        self.assertEqual([], self.errors())

    def test_partial_review_cannot_pass(self):
        review = valid_review(ARTICLE)
        review["paragraphs"].pop(next(iter(review["paragraphs"])))
        self.reviews[PATH] = review
        self.assertIn("uncovered paragraphs", " ".join(self.errors()))

    def test_content_edit_invalidates_old_review(self):
        self.reviews[PATH] = valid_review(ARTICLE)
        self.source.write_text(ARTICLE + "\n新出現的臨床證據還要調整原本假設，而非用舊答案取代全部判斷。\n", encoding="utf-8")
        self.assertIn("stale", " ".join(self.errors()))

    def test_self_assigned_or_fail_score_does_not_pass(self):
        review = valid_review(ARTICLE)
        review["reviewer_context"] = "same_drafter"
        review["epqc_scores"]["C"] = 2
        review["hard_stops"]["unsafe_claim"] = True
        self.reviews[PATH] = review
        errors = " ".join(self.errors())
        for signal in ("separate editorial context", "EPQC below", "unresolved EPQC"):
            self.assertIn(signal, errors)

    def test_duplicate_rationales_rejected(self):
        review = valid_review(ARTICLE)
        for p in review["paragraphs"].values():
            p["reader_gain"] = "任何段落都能讓讀者學到非常有用的東西但此評語沒有獨特定位"
        self.reviews[PATH] = review
        self.assertIn("duplicate paragraph", " ".join(self.errors()))

    def test_frozen_baseline_not_claimed_as_review(self):
        self.frozen[PATH] = git_blob_sha(ARTICLE.encode("utf-8"))
        self.assertEqual([], self.errors())
        self.source.write_text(ARTICLE + "\n新段落改動後必須重審這篇文章，不因舊版存在就放行。\n", encoding="utf-8")
        self.assertIn("SEMANTIC_HOLD", " ".join(self.errors()))

    def test_source_pages_and_historical_original_not_blocked(self):
        self.assertFalse(is_teaching_page({"source": "content/xiaoma-reading/vte-sources.md"}))
        self.assertFalse(is_teaching_page({"source": "content/xiaoma-reading/originals/hcm.md", "kind": "historical_original"}))
        self.assertTrue(is_teaching_page(self.row))

    def test_reader_units_ignore_svg_and_code_but_cover_paragraphs(self):
        text = ARTICLE + """
<figure id="x">
<svg><text>不進入語義段落檢查</text></svg>
</figure>

```python
clinical_script = "internal"
```

- 病人的新資料如果會改變診斷機率，就不該把第一次印象當作最終的結果。
"""
        units = reading_units(text)
        self.assertEqual(4, len(units))
        self.assertFalse(any("clinical_script" in p["excerpt"] for p in units))


    def test_reader_units_preserve_numeric_less_than_threshold(self):
        # Clinical decision thresholds must survive HTML cleanup in review packets.
        # The old /<[^>]*>/ pattern swallowed everything from <2,000 to >ULN.
        text = (
            "若 HBV DNA <2,000 IU/mL 且 ALT >ULN，應先排查其他肝損傷原因，"
            "再評估是否符合抗病毒治療條件。<strong>不能只靠一次檢驗。</strong>"
        )
        excerpt = reading_units(text)[0]["excerpt"]
        self.assertIn("<2,000 IU/mL", excerpt)
        self.assertIn(">ULN", excerpt)
        self.assertIn("不能只靠一次檢驗", excerpt)
        self.assertNotIn("<strong>", excerpt)


    def test_reader_units_preserve_symbolic_threshold_and_next_comparator(self):
        # A letter-prefixed less-than comparator is not an HTML element.
        text = (
            "若 Hb <LLN 且 K >ULN，不能因為這段比較出現英文字母，就把"
            "不同檢驗條件在審查封包中一同抹掉。<strong>必須保留分界。</strong>"
        )
        excerpt = reading_units(text)[0]["excerpt"]
        self.assertIn("Hb <LLN 且 K >ULN", excerpt)
        self.assertIn("必須保留分界", excerpt)
        self.assertNotIn("<strong>", excerpt)

    def test_reader_units_strip_actual_inline_tag_with_attributes(self):
        text = (
            "若 serum Na <LLN，<span class='important'>應重新檢查</span>；"
            "另外 ECG 與真實電解質的方向可能不一致，不能機械套用單一數值。"
        )
        excerpt = reading_units(text)[0]["excerpt"]
        self.assertIn("serum Na <LLN", excerpt)
        self.assertIn("應重新檢查", excerpt)
        self.assertNotIn("<span", excerpt)
        self.assertNotIn("</span>", excerpt)

    def test_reader_units_do_not_strip_comparison_until_next_real_tag(self):
        text = (
            "如果 ALT <ULN 且 HBV DNA >2,000，就仍需要依臨床情境"
            "尋找其他解釋，不能把比較式刪到只剩一個數值。<em>重新評估。</em>"
        )
        excerpt = reading_units(text)[0]["excerpt"]
        self.assertIn("ALT <ULN 且 HBV DNA >2,000", excerpt)
        self.assertIn("重新評估", excerpt)
        self.assertNotIn("<em>", excerpt)


if __name__ == "__main__":
    unittest.main()
