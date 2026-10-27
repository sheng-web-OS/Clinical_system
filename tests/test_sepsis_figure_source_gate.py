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


    def test_official_q48_copd_mismatch_is_removed_from_sepsis(self):
        # Official 113-1 醫學（三） Q48 asks about COPD treatment, NOT
        # bicarbonate in sepsis. A matching answer letter is not provenance.
        # Official original: https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=113020&q=1&s=11&t=Q
        article = (ROOT / ARTICLE).read_text(encoding="utf-8")
        exam = (ROOT / "content/xiaoma-internal-medicine/exams/sepsis-core-112-114-med3.md").read_text(encoding="utf-8")
        self.assertNotIn("113-1 醫學（三）第 48 題", article)
        self.assertNotIn("113-1 醫學（三）第 48 題", exam)
        self.assertNotIn('<a id="q-113-1-48"></a>', exam)
        self.assertIn('<a id="q-112-1-65"></a>', exam)
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        for source in (ARTICLE, "content/xiaoma-internal-medicine/exams/sepsis-core-112-114-med3.md"):
            page = next(p for p in pages if p["source"] == source)
            linked = page.get("exam_questions", []) + page.get("related_exams", [])
            self.assertFalse(any(q.get("year_roc") == 113 and q.get("sitting") == 1
                                 and q.get("question_number") == 48 for q in linked))
            self.assertTrue(any(q.get("year_roc") == 112 and q.get("sitting") == 1
                                and q.get("question_number") == 65 for q in linked))

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
            if index == 0:
                self.assertIn(("A", "J"), edges, "Infection source must visibly connect to source-control intervention")
                self.assertIn(("F", "K"), edges, "Perfusion deficit must visibly connect to circulation support")


    def test_first_use_of_critical_abbreviations_is_reader_friendly(self):
        # First use must define the term before introducing the shorthand.
        # This is a reader clarity check, not a clinical correctness verdict.
        article = (ROOT / ARTICLE).read_text(encoding="utf-8")
        exam = (ROOT / "content/xiaoma-internal-medicine/exams/sepsis-core-112-114-med3.md").read_text(encoding="utf-8")
        for name, text, expansions in (
            ("Sepsis article", article, {
                "IBCC": "Internet Book of Critical Care（IBCC）",
                "SSC": "Surviving Sepsis Campaign（SSC）",
                "IVC": "inferior vena cava，IVC",
                "HFNC": "high-flow nasal cannula，HFNC",
            }),
            ("Sepsis exam reader", exam, {
                "SSC": "Surviving Sepsis Campaign（SSC）",
            }),
        ):
            for abbreviation, expansion in expansions.items():
                with self.subTest(document=name, abbreviation=abbreviation):
                    first = text.find(abbreviation)
                    self.assertGreaterEqual(first, 0, "Abbreviation must occur in the reader")
                    self.assertIn(expansion, text[:first + len(abbreviation) + 2],
                                  "Expand %s at first use, not in a later source note" % abbreviation)


    def test_exam_reader_has_no_duplicate_auto_generated_anchor_ids(self):
        # The site renderer inserts official exam-* IDs for canonical embedded questions.
        # Keep stable q-* links for the Sepsis narrative but never pre-emit exam-*.
        exam = (ROOT / "content/xiaoma-internal-medicine/exams/sepsis-core-112-114-med3.md").read_text(encoding="utf-8")
        self.assertNotIn('<a id="exam-', exam)
        for key in ("q-112-1-33", "q-112-1-64", "q-113-1-48", "q-114-1-51", "q-114-1-57"):
            self.assertIn('<a id="' + key + '"></a>', exam)


if __name__ == "__main__":
    unittest.main()
