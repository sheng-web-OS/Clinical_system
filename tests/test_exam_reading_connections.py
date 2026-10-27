"""Prevent wrong-year joins, duplicate practice identities and drifting reading links."""
import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from catalog import load_pages
from exam_archive import (validate_exam_catalog, question_records, question_key,
                          question_anchor, archive_anchor, render_exam_archive,
                          question_connections, scope_embedded_question, question_bounds)


class ExamReadingConnections(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = load_pages(ROOT)

    def test_existing_in_article_questions_are_cataloged_once(self):
        keys = [question_key(r["exam"]) for r in question_records(self.pages)]
        self.assertEqual(len(keys), len(set(keys)))
        expected = {(115, 2, 2, "醫學（三）", 3), (111, 1, 2, "醫學（三）", 51),
                    (114, 2, 2, "醫學（三）", 25), (113, 1, 2, "醫學（三）", 50),
                    (115, 2, 2, "醫學（三）", 6)}
        self.assertTrue(expected.issubset(keys))
        # The respiratory-practice page repeats the first two; it is not a second canonical question.
        self.assertEqual(keys.count((111, 1, 2, "醫學（三）", 51)), 1)

    def test_same_number_in_different_years_and_sittings_stays_distinct(self):
        records = {question_key(r["exam"]): r for r in question_records(self.pages)}
        asthma = records[(113, 1, 2, "醫學（三）", 50)]
        copd = records[(113, 2, 2, "醫學（三）", 50)]
        self.assertNotEqual(asthma["page"]["output"], copd["page"]["output"])
        self.assertNotEqual(archive_anchor(asthma), archive_anchor(copd))

    def test_archive_carries_exact_question_and_concept_destinations(self):
        archive = render_exam_archive(self.pages, ROOT)
        connections = question_connections(self.pages, ROOT)
        for record in question_records(self.pages):
            self.assertIn('id="' + archive_anchor(record) + '"', archive)
            self.assertIn('href="' + record["page"]["output"] + '#' + record["anchor"] + '"', archive)
        for values in connections.values():
            for link in values:
                self.assertIn('href="' + link["href"] + '"', archive)

    def test_relation_focus_is_private_authoring_input_not_reader_copy(self):
        from unittest.mock import patch
        from exam_archive import render_concept_links, render_related_questions

        private_focus = "INTERNAL_RELATION_MARKER: concept edge awaiting prose synthesis"
        url = "clinical-concept.html#part-1"
        links = [{"href": url, "page": {"title": "完整臨床教材"}, "focus": private_focus}]
        reader_nav = render_concept_links(links)
        self.assertIn('href="' + url + '"', reader_nav)
        self.assertNotIn(private_focus, reader_nav)

        exam = {"year_roc": 114, "sitting": 2, "stage": 2,
                "subject": "醫學（三）", "question_number": 3}
        page = {"related_exams": [{**exam, "focus": private_focus}]}
        record = {"exam": exam,
                  "page": {"output": "exam-example.html", "references": "sources.html"},
                  "anchor": "q-3"}
        body = "<h2>題目</h2><p>完整詳解</p>"
        with patch("exam_archive.question_bounds", return_value=(0, len(body))), \\
                patch("exam_archive.scope_embedded_question", side_effect=lambda text, _: text):
            reader_card = render_related_questions(
                page, {question_key(exam): record},
                {"exam-example.html": {"body": body}}
            )
        self.assertIn("Q3", reader_card)
        self.assertIn("完整詳解", reader_card)
        self.assertIn("開啟原詳解頁", reader_card)
        self.assertNotIn(private_focus, reader_card)
        self.assertNotIn("related-exam-focus", reader_card)

    def test_unknown_or_unpublished_question_cannot_be_linked(self):
        pages = copy.deepcopy(self.pages)
        page = next(p for p in pages if p.get("related_exams"))
        page["related_exams"][0]["year_roc"] = 150
        with self.assertRaisesRegex(ValueError, "not a published official question"):
            validate_exam_catalog(pages, ROOT)

    def test_missing_question_and_concept_headings_fail_before_rendering(self):
        for field in ("question_heading", "concept_heading"):
            with self.subTest(field=field):
                pages = copy.deepcopy(self.pages)
                question = next(p for p in pages if p.get("exam_questions"))["exam_questions"][0]
                question[field] = "A section that was removed"
                with self.assertRaisesRegex(ValueError, "heading missing or ambiguous"):
                    validate_exam_catalog(pages, ROOT)

    def test_duplicate_embedded_identity_is_rejected(self):
        pages = copy.deepcopy(self.pages)
        page = next(p for p in pages if p.get("exam_questions"))
        page["exam_questions"].append(copy.deepcopy(page["exam_questions"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate exam question identity"):
            validate_exam_catalog(pages, ROOT)

    def test_metadata_cannot_silently_relabel_an_existing_question_year(self):
        pages = copy.deepcopy(self.pages)
        page = next(p for p in pages if p["output"] == "xiaoma-20261024-asthma-variable-airflow.html")
        page["exam_questions"][0]["year_roc"] = 112
        with self.assertRaisesRegex(ValueError, "identity disagrees"):
            validate_exam_catalog(pages, ROOT)

    def test_single_question_keeps_later_clinical_qualifications(self):
        record = next(r for r in question_records(self.pages) if r["page"]["output"] == "xiaoma-exam-112-2-med3-q46.html")
        body = '<h2><span id="q-46"></span>Question</h2><p>Answer</p><h2>Clinical limits</h2><p>Not every dyspneic COPD patient should receive ICS.</p>'
        start, end = question_bounds(body, record)
        self.assertIn('Not every dyspneic', body[start:end])

    def test_next_question_bookmark_stays_after_previous_question_footer(self):
        record = next(r for r in question_records(self.pages) if r["exam"]["year_roc"] == 115 and r["exam"]["question_number"] == 6)
        body = '<h3><span id="' + record["anchor"] + '"></span>Question</h3><p>Answer</p>\n<span id="baseline-q02"></span>\n<h3>Next question</h3>'
        _, end = question_bounds(body, record)
        self.assertTrue(body[end:].lstrip().startswith('<span id="baseline-q02">'))

    def test_embedded_svg_ids_and_links_do_not_collide_or_escape(self):
        record = question_records(self.pages)[0]
        markup = '<h2 id="part-1"><span id="q-8"></span>Q8</h2><svg aria-labelledby="label"><title id="label">Title</title><path id="shape" fill="url(#shape)"/></svg><a href="#label">Local</a><a href="#part-9">Elsewhere</a>'
        embedded = scope_embedded_question(markup, record)
        self.assertNotIn('id="label"', embedded)
        self.assertNotIn('href="#label"', embedded)
        self.assertIn(record["page"]["output"] + '#part-9', embedded)
        self.assertNotIn('<h2', embedded)
        self.assertNotIn('url(#shape)', embedded)


if __name__ == "__main__":
    unittest.main()
