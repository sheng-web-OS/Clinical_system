"""Regression tests: a Figure/Table audit cannot be replaced by a token or empty claim."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "site"))
from catalog import load_pages
from figure_gate import _blob_sha, audit_coverage

SOURCE = "content/lessons/example.md"
EVIDENCE = "content/figure-review.md"
BODY = """# Clinical learning
This article makes the mechanism concrete.
[回讀原始圖表與查核頁](../figure-review.md)

<figure id="main-map"><svg role="img"><title>模型</title></svg>
<figcaption>原書 9E PDF 第 180 頁原表，本站用自主整理的臨床推理圖解釋。</figcaption></figure>
"""
EVIDENCE_TEXT = """# 核對記錄
Pocket Medicine 9E PDF 第 180 頁「Approach to Diuresis」原表。
原書的圖表用途和應用範圍均經比對。
"""
ITEM = {
    "locator": "Pocket Medicine 9E PDF 180, Table: Approach to Diuresis",
    "source_token": "Approach to Diuresis",
    "mode": "illustrated",
    "anchor": "main-map",
    "caption_token": "原書 9E PDF 第 180 頁",
    "teaching_role": "分開不同治療反應瓶頸，讓讀者理解何時該加量、改給藥頻率、檢查遠端代償，而非照抄固定順序。",
    "scope_limit": "屬於簡化教學模型；不能當作所有病人通用的處方流程，也無法推定介入後長期死亡率的改變。"
}


class FigurePublicationGate(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.root = Path(d.name)
        for folder in ("site", "audit", "content/lessons"):
            (self.root / folder).mkdir(parents=True)
        (self.root / SOURCE).write_text(BODY, encoding="utf8")
        (self.root / EVIDENCE).write_text(EVIDENCE_TEXT, encoding="utf8")
        self.rows = [
            {"source": SOURCE, "output": "example.html", "title": "Example",
             "subtitle": "Learning", "collection": "xiaoma-internal-medicine",
             "date": "2026-10-23", "review": "author_source_check"},
            {"source": EVIDENCE, "output": "review.html", "title": "Evidence",
             "subtitle": "Provenance", "collection": "xiaoma-internal-medicine"}
        ]
        (self.root / "site/pages.json").write_text(json.dumps(self.rows), encoding="utf8")
        self.payload = {"legacy_frozen": {},
                        "reviews": {SOURCE: {
                            "status": "represented",
                            "source_review": EVIDENCE,
                            "items": [dict(ITEM)]
                        }}}
        self.write_audit()

    def write_audit(self):
        (self.root / "audit/figure-gate.json").write_text(
            json.dumps(self.payload, ensure_ascii=False), encoding="utf8")

    def test_valid_publication_with_rendered_figure_and_public_source(self):
        self.assertEqual(load_pages(self.root)[0]["output"], "example.html")
        self.assertEqual(audit_coverage(self.root, self.rows)["source_reviewed"], 1)

    def test_missing_audit_fails_closed(self):
        del self.payload["reviews"][SOURCE]
        self.write_audit()
        with self.assertRaisesRegex(ValueError, "MISSING"):
            load_pages(self.root)

    def test_pending_not_a_passing_status(self):
        self.payload["reviews"][SOURCE]["status"] = "pending"
        self.write_audit()
        with self.assertRaisesRegex(ValueError, "HOLD"):
            load_pages(self.root)

    def test_no_real_figure_cannot_pass(self):
        (self.root / SOURCE).write_text(BODY.replace('<figure id="main-map">', '<div id="main-map">'), encoding="utf8")
        with self.assertRaisesRegex(ValueError, "missing illustrated figure"):
            load_pages(self.root)

    def test_caption_provenance_missing_fails(self):
        (self.root / SOURCE).write_text(BODY.replace("原書 9E PDF 第 180 頁", "無任何來源"), encoding="utf8")
        with self.assertRaisesRegex(ValueError, "caption omits"):
            load_pages(self.root)

    def test_source_claim_must_be_in_separate_evidence_document(self):
        self.payload["reviews"][SOURCE]["items"][0]["source_token"] = "Imaginary Figure 99"
        self.write_audit()
        with self.assertRaisesRegex(ValueError, "locator is absent"):
            load_pages(self.root)

    def test_public_reader_must_link_its_audit(self):
        (self.root / SOURCE).write_text(BODY.replace("[回讀原始圖表與查核頁](../figure-review.md)", ""), encoding="utf8")
        with self.assertRaisesRegex(ValueError, "no source review link"):
            load_pages(self.root)

    def test_legacy_frozen_is_not_assumed_reviewed_and_blocks_changes(self):
        self.payload = {"legacy_frozen": {SOURCE: _blob_sha(self.root / SOURCE)}, "reviews": {}}
        self.write_audit()
        self.assertEqual(audit_coverage(self.root, load_pages(self.root))["legacy_pending"], 1)
        (self.root / SOURCE).write_text(BODY + "\nRevised.\n", encoding="utf8")
        with self.assertRaisesRegex(ValueError, "LEGACY_CHANGED"):
            load_pages(self.root)

    def test_negative_visual_result_requires_evidence_and_reason(self):
        self.payload["reviews"][SOURCE] = {
            "status": "no_relevant_visual", "source_review": EVIDENCE,
            "examined_pages": "Pocket Medicine 9E PDF 第 180 頁",
            "source_token": "Approach to Diuresis",
            "rationale": "已檢查原頁與圖表、註腳，該處不存在會改變本篇核心推理的相關原始圖表或表格，已在來源頁說明範圍與未查部分。"
        }
        self.write_audit()
        self.assertEqual(load_pages(self.root)[0]["output"], "example.html")
        self.payload["reviews"][SOURCE]["rationale"] = "沒有圖。"
        self.write_audit()
        with self.assertRaisesRegex(ValueError, "inadequate rationale"):
            load_pages(self.root)


if __name__ == "__main__":
    unittest.main()
