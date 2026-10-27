"""Regression: Sepsis public figure provenance must be independently navigable.

This test validates traceability and catalog wiring only, not clinical correctness.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = "content/clinical-os/2026-10-27-sepsis-from-infection-to-resuscitation.md"
SOURCE = "content/clinical-os/sepsis-visual-evidence-and-sources.md"
ORIGINAL_FIGURE = "https://link.springer.com/article/10.1186/s12245-025-00958-5#Fig1"


class SepsisFigureSourceGate(unittest.TestCase):
    def test_original_figure_and_public_source_are_linked(self):
        article = (ROOT / ARTICLE).read_text(encoding="utf-8")
        self.assertIn(ORIGINAL_FIGURE, article)
        self.assertIn("sepsis-visual-evidence-and-sources.md", article)
        source = (ROOT / SOURCE).read_text(encoding="utf-8")
        self.assertIn("Fig 1", source)
        self.assertIn(ORIGINAL_FIGURE, source)
        self.assertIn("Case 1", source)

    def test_catalog_and_figure_gate_cover_sepsis(self):
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        catalog_sources = {p["source"] for p in pages}
        self.assertIn(ARTICLE, catalog_sources)
        self.assertIn(SOURCE, catalog_sources)
        figure = json.loads((ROOT / "audit/figure-gate.json").read_text(encoding="utf-8"))
        record = figure["reviews"][ARTICLE]
        self.assertEqual(record["status"], "represented")
        self.assertEqual(record["source_review"], SOURCE)
        self.assertTrue(any(
            item.get("mode") == "source_link"
            and item.get("url") == ORIGINAL_FIGURE
            for item in record["items"]
        ))


    def test_q48_is_one_canonical_question_with_sepsis_backlink(self):
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        key = (113, 1, 2, "醫學（三）", 48)
        canonical = []
        for page in pages:
            for q in page.get("exam_questions", []):
                identity = tuple(q[k] for k in ("year_roc", "sitting", "stage", "subject", "question_number"))
                if identity == key:
                    canonical.append(page["source"])
        self.assertEqual(canonical, ["content/xiaoma-internal-medicine/lessons/2026-10-23-acid-base.md"])
        sepsis_exam = next(p for p in pages if p["source"] == "content/xiaoma-internal-medicine/exams/sepsis-core-112-114-med3.md")
        self.assertTrue(any(
            tuple(q[k] for k in ("year_roc", "sitting", "stage", "subject", "question_number")) == key
            for q in sepsis_exam.get("related_exams", [])
        ))


    def test_q57_is_one_canonical_question_with_sepsis_backlink(self):
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        key = (114, 1, 2, "醫學（三）", 57)
        canonical = []
        for page in pages:
            for q in page.get("exam_questions", []):
                identity = tuple(q[k] for k in ("year_roc", "sitting", "stage", "subject", "question_number"))
                if identity == key:
                    canonical.append(page["source"])
        self.assertEqual(canonical, ["content/xiaoma-internal-medicine/lessons/2026-10-22-baseline-twenty.md"])
        sepsis_exam = next(p for p in pages if p["source"] == "content/xiaoma-internal-medicine/exams/sepsis-core-112-114-med3.md")
        self.assertTrue(any(
            tuple(q[k] for k in ("year_roc", "sitting", "stage", "subject", "question_number")) == key
            for q in sepsis_exam.get("related_exams", [])
        ))


    def test_mermaid_edges_reference_renderer_supported_nodes(self):
        # Site's native flowchart renderer only recognizes boxed nodes and plain arrows.
        import re
        article = (ROOT / ARTICLE).read_text(encoding="utf-8")
        blocks = re.findall(r"~~~mermaid\n([\s\S]*?)\n~~~", article)
        self.assertGreaterEqual(len(blocks), 2)
        for index, block in enumerate(blocks):
            nodes = {name for name, _ in re.findall(r'([A-Z])\["([^"]+)"\]', block)}
            edges = re.findall(r'\b([A-Z])(?:\["[^"]+"\])?\s*-->\s*([A-Z])', block)
            self.assertTrue(edges, "Diagram %d has no parseable edges" % index)
            self.assertTrue(all(a in nodes and b in nodes for a, b in edges),
                            "Diagram %d has edges to unsupported or undefined nodes" % index)


if __name__ == "__main__":
    unittest.main()
