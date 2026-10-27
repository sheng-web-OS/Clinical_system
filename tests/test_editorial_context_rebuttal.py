"""Failure-directed safety checks: triage is only evidence routing, not medical review."""
import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("autonomy_quality_lab", ROOT / "tools/autonomy_quality_lab.py")
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


def review(quote, problem, proposed="先核對原文。"):
    return f"1. 原文：「{quote}」\n   問題機制：{problem}\n   最小改法：{proposed}\n"


class ContextRebuttalSafety(unittest.TestCase):
    def test_qualified_all_reversed_by_model_requires_rebuttal(self):
        source = "病程不同。這不是所有 DCM 都必然遵循的單一病程。後文說個體差異。"
        answer = review("這不是所有 DCM 都必然遵循的單一病程。",
                        "這可能使人以為所有DCM病人都會形成惡性循環。")
        result = lab.triage_revision_claims(source, answer)
        self.assertEqual(result["scope_reversal_review_flags"], 1)
        self.assertEqual(result["findings"][0]["risk_signals"], ["universal_scope"])
        self.assertEqual(result["findings"][0]["decision"], "HOLD_FOR_CONTEXT_REVIEW")
        self.assertFalse(result["public_edit_allowed"])

    def test_not_alone_is_misread_as_alone(self):
        source = "這些影像特徵並不是單憑一種 LGE pattern 就能完成病因診斷。"
        ans = review(source, "恐讓人以為可以單獨完成病因診斷。")
        self.assertEqual(lab.triage_revision_claims(source, ans)
                         ["findings"][0]["risk_signals"], ["single_test_overreach"])

    def test_at_least_is_not_only(self):
        source = "治療時至少要處理三個層次。"
        ans = review(source, "讓讀者誤以為只需要處理三個層次。")
        self.assertEqual(lab.triage_revision_claims(source, ans)
                         ["findings"][0]["risk_signals"], ["minimum_as_maximum"])

    def test_not_imply_can_be_misread_as_unrelated(self):
        source = "EF 下降不代表每次心跳的輸出量都立刻大幅降低。"
        ans = review(source, "讀者可能認為 EF 與血流量沒有關係。")
        self.assertEqual(lab.triage_revision_claims(source, ans)
                         ["findings"][0]["risk_signals"], ["negated_implication"])

    def test_real_missing_explanation_never_auto_rejected(self):
        source = "這不是所有病人都會發生。\n（此處沒有說明分層的臨床原因。）"
        ans = review("這不是所有病人都會發生。", "欠缺誰會發生的分層與理由。")
        res = lab.triage_revision_claims(source, ans)
        self.assertEqual(res["scope_reversal_review_flags"], 0)
        self.assertEqual(res["automatic_rejections"], 0)
        self.assertEqual(res["automatic_accepts"], 0)
        self.assertFalse(res["medical_quality_verified"])

    def test_normal_clean_passage_is_not_forced_into_a_finding(self):
        res = lab.triage_revision_claims("沒有編輯問題的普通段落。", "無需修改。")
        self.assertEqual(res["finding_count"], 0)
        self.assertTrue(res["unparseable_or_absent_findings"])
        self.assertEqual(res["review_parse_status"], "NO_FINDINGS_DECLARED_NOT_VALIDATED")
        self.assertFalse(res["public_edit_allowed"])

    def test_unparseable_model_text_cannot_masquerade_as_clean(self):
        res = lab.triage_revision_claims("有待檢視的教材。", "1. Probably a flaw here, but no source quote.")
        self.assertEqual(res["finding_count"], 0)
        self.assertEqual(res["review_parse_status"], "UNPARSEABLE_REVIEW_HOLD")
        self.assertFalse(res["medical_quality_verified"])

    def test_preflight_records_full_exact_source_and_answer_hashes(self):
        import hashlib
        source = "病例 A 原文。"
        answer = review("病例 A 原文。", "文內未交代必要機制。")
        found = lab.triage_revision_claims(source, answer)
        self.assertEqual(found["source_sha256_utf8"],
                         hashlib.sha256(source.encode("utf-8")).hexdigest())
        self.assertEqual(found["answer_sha256_utf8"],
                         hashlib.sha256(answer.encode("utf-8")).hexdigest())
        self.assertEqual(found["review_parse_status"], "NUMBERED_FINDINGS_FOR_CONTEXT_REVIEW")
        altered = lab.triage_revision_claims(source + " 後續增補。", answer)
        self.assertNotEqual(found["source_sha256_utf8"], altered["source_sha256_utf8"])
        self.assertEqual(found["automatic_accepts"], 0)

    def test_causal_context_is_returned_even_if_quote_looks_unqualified(self):
        source = "首先 EF 並非血流量。\n\n" + "X" * 70 + "EF 降低不一定立刻代表 SV 下降。\n\n因為 EDV 上升可以暫時代償。"
        ans = review("EF 降低不一定立刻代表 SV 下降。", "為何維持SV沒有解釋。")
        res = lab.triage_revision_claims(source, ans)
        self.assertIn("EDV 上升可以暫時代償", res["findings"][0]["source_context_excerpt"])
        self.assertFalse(res["findings"][0]["context_rebuttal_required"])
        self.assertEqual(res["findings"][0]["decision"], "REVIEW_REQUIRED_NOT_CLEARED")

    def test_cross_paragraph_citation_located_without_claiming_validity(self):
        source = "定義包含兩個層次。\n\n第一個是表型。\n\n第二個是排除負荷。"
        ans = review("定義包含兩個層次。第一個是表型。第二個是排除負荷。",
                     "或許不完整。")
        res = lab.triage_revision_claims(source, ans)
        self.assertEqual(res["located_count"], 1)
        self.assertFalse(res["findings"][0]["exact_contiguous_quote"])
        self.assertFalse(res["medical_quality_verified"])

    def test_unlocated_citation_is_held(self):
        res = lab.triage_revision_claims("沒有這段原文。", review("杜撰的原文。", "解釋缺失。"))
        self.assertEqual(res["located_count"], 0)
        self.assertEqual(res["context_rebuttal_required_count"], 1)
        self.assertEqual(res["findings"][0]["decision"], "HOLD_FOR_CONTEXT_REVIEW")

    def test_raw_four_real_completions_expose_scope_reversal_cues(self):
        """Regression of *retrospective* clues; NOT clinical truth or new-article validation."""
        path = ROOT / "experiments/autonomy-eval/WORKERS_AI_DCM_PILOT_20261027_RAW.json"
        study = json.loads(path.read_text(encoding="utf-8"))
        raw = study["recorded"]
        self.assertEqual(len(raw), 4)
        # Provide only a quote-string corpus here. This test checks cue extraction;
        # source identity and full original-context QA are separate experiments.
        quotes = re.findall(r"原文\s*[：:]\s*「([^」]+)」",
                            "\n".join(row["answer"] for row in raw))
        self.assertEqual(len(quotes), 16)
        quote_corpus = "\n".join(quotes)
        counts = {}
        for row in raw:
            report = lab.triage_revision_claims(quote_corpus, row["answer"])
            self.assertEqual(report["finding_count"], 4)
            self.assertEqual(report["located_count"], 4)
            self.assertEqual(report["automatic_accepts"], 0)
            self.assertEqual(report["automatic_rejections"], 0)
            counts[row["id"]] = report["scope_reversal_review_flags"]
        self.assertEqual(counts, {"lite-1": 2, "baseline-1": 3,
                                 "baseline-2": 0, "lite-2": 2})


if __name__ == "__main__":
    unittest.main()
