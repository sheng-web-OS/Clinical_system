"""Historical physician exam questions must be organized by exam year, not writing date."""
import copy
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from catalog import load_pages
from exam_archive import validate_exam_catalog, render_exam_archive, render_exam_year_teasers, question_records, archive_anchor

class ExamArchiveContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = load_pages(ROOT)

    def test_108_first_stage_two_med3_includes_fourth_batch_without_duplicates(self):
        rows = [p for p in self.pages if p.get("exam") and
                (p["exam"]["year_roc"], p["exam"]["sitting"], p["exam"]["stage"], p["exam"]["subject"]) ==
                (108, 1, 2, "醫學（三）")]
        self.assertGreaterEqual(len(rows), 6)
        for p in rows:
            exam = p["exam"]
            self.assertEqual((exam["year_roc"], exam["sitting"], exam["stage"], exam["subject"]),
                             (108, 1, 2, "醫學（三）"))
            body = (ROOT / p["source"]).read_text("utf8")
            headings = {int(x) for x in re.findall(r"(?m)^## 第 (\d+) 題", body)}
            self.assertEqual(headings, set(exam["question_numbers"]))
        baseline = {key for key in validate_exam_catalog(self.pages)
                    if key[:4] == (108, 1, 2, "醫學（三）")}
        self.assertTrue({(108, 1, 2, "醫學（三）", q)
                         for q in (2, 8, 11, 12, 17, 22, 23, 25, 26, 27, 28, 61, 63, 75, 76, 78)}
                        .issubset(baseline),
                        "Previously published official question identities must remain")

    def test_all_published_exam_question_headings_match_deep_links(self):
        """Every official Q anchor must exist exactly once, across every exam year."""
        for page in self.pages:
            exam = page.get("exam")
            if not exam:
                continue
            body = (ROOT / page["source"]).read_text("utf8")
            headings = [int(n) for n in re.findall(r"(?m)^## 第\s*(\d+)\s*題", body)]
            self.assertCountEqual(headings, exam["question_numbers"],
                                  "Broken #q-N reader anchors: " + page["source"])

    def test_year_archive_does_not_use_publication_year(self):
        index = render_exam_archive(self.pages)
        teaser = render_exam_year_teasers(self.pages)
        self.assertIn('id="year-108"', index)
        self.assertIn("108 年（2019）", index)
        self.assertIn("醫師第二階段", index)
        self.assertIn("醫學（三）", index)
        self.assertNotIn('id="year-2026"', index)
        self.assertIn('href="xiaoma-exams.html#year-108"', teaser)
        self.assertEqual(index.count('class="exam-catalog-question"'), len(question_records(self.pages)))
        for q in (2, 8, 11, 12, 17, 22, 23, 25, 26, 27, 28, 61, 63, 75, 76, 78):
            self.assertIn("#q-" + str(q) + '"', index)

    def test_heart_sounds_29_plus_20_are_visible_in_correct_exam_years(self):
        """A published article alone cannot stand in for canonical year-archive entries."""
        canonical = next(p for p in self.pages if p["source"] ==
                         "content/xiaoma-internal-medicine/lessons/2026-10-27-heart-sounds-cross-discipline-exams.md")
        supplement = next(p for p in self.pages if p["source"] ==
                          "content/xiaoma-internal-medicine/exams/heart-sounds-cross-specialty-expanded-111-115.md")
        first = canonical.get("exam_questions", [])
        second = supplement.get("exam_questions", [])
        self.assertEqual(len(first), 29, "Original 29 official questions must be year-indexed")
        self.assertEqual(len(second), 20, "Supplement must contain 20 nonduplicating questions")
        identity = lambda q: tuple(q[k] for k in
                                   ("year_roc", "sitting", "stage", "subject", "question_number"))
        original_keys = {identity(q) for q in first}
        additional_keys = {identity(q) for q in second}
        self.assertEqual(len(original_keys), 29)
        self.assertEqual(len(additional_keys), 20)
        self.assertTrue(original_keys.isdisjoint(additional_keys))
        self.assertEqual({key[0] for key in original_keys | additional_keys},
                         {111, 112, 113, 114, 115})

        archive = render_exam_archive(self.pages, ROOT)
        for page, entries in ((canonical, first), (supplement, second)):
            for q in entries:
                # Year archive must deep-link to the question itself, not just the article top.
                record = next(r for r in question_records(self.pages)
                              if r["page"]["source"] == page["source"] and identity(r["exam"]) == identity(q))
                self.assertIn('id="' + archive_anchor(record) + '"', archive)
                self.assertIn('href="' + page["output"] + '#' + record["anchor"] + '"', archive)
        self.assertIn("ASD 與 Eisenmenger：官方更正 B 或 D", archive)
        self.assertIn("原圖待核", archive, "Image-dependent questions cannot masquerade as verified figures")


    def test_all_heart_sounds_cross_specialty_questions_have_readable_material_links(self):
        """Both cross-specialty question collections must expose a real topic section from each year-list row."""
        from exam_archive import question_connections, concept_url, question_key

        sources = {
            "content/xiaoma-internal-medicine/lessons/2026-10-27-heart-sounds-cross-discipline-exams.md",
            "content/xiaoma-internal-medicine/exams/heart-sounds-cross-specialty-expanded-111-115.md",
        }
        connections = question_connections(self.pages, ROOT)
        archive = render_exam_archive(self.pages, ROOT)
        records = {question_key(record["exam"]): record for record in question_records(self.pages)}
        checked = 0
        for page in self.pages:
            if page["source"] not in sources:
                continue
            for question in page["exam_questions"]:
                with self.subTest(source=page["source"], question=question["question_heading"]):
                    self.assertIn("concept_heading", question, "This question has no linked learning context")
                    self.assertNotEqual(question["concept_heading"], question["question_heading"])
                    key = question_key(question)
                    expected = concept_url(page, question, ROOT)
                    self.assertTrue(any(link["href"] == expected for link in connections[key]))
                    marker = '<div class="exam-catalog-question" id="' + archive_anchor(records[key]) + '"'
                    self.assertIn(marker, archive)
                    row = archive.split(marker, 1)[1].split("</div>", 1)[0]
                    self.assertIn('data-materials="', row)
                    self.assertIn('class="exam-catalog-materials"', row)
                    self.assertIn('href="' + expected + '"', row)
                    self.assertNotEqual(expected, page["output"] + "#" + records[key]["anchor"])
                    checked += 1
        self.assertEqual(checked, 49)

    def test_heart_sounds_deep_material_links_are_per_question_and_not_embedded(self):
        """Previously missed release requirement: year-page '教材' resolves to real deep sections."""
        from exam_archive import (
            question_connections, question_key, concept_url, render_related_questions
        )
        lesson = next(p for p in self.pages if p["output"] ==
                      "xiaoma-20261027-heart-sounds-structural-exam.html")
        materials = lesson.get("related_exams", [])
        self.assertEqual(len(materials), 33, "A deep lesson must not ship with zero year-archive mappings")
        self.assertTrue(all(link.get("embed") is False for link in materials),
                        "Do not inject dozens of full exam explanations into the clinical lesson")
        connections = question_connections(self.pages, ROOT)
        archive = render_exam_archive(self.pages, ROOT)
        records = {question_key(r["exam"]): r for r in question_records(self.pages)}
        for link in materials:
            key = question_key(link)
            with self.subTest(identity=key):
                self.assertIn(key, records, "Cannot link nonexistent exam IDs")
                expected = concept_url(lesson, link, ROOT)
                self.assertRegex(expected, r"#part-[1-8]$")
                self.assertEqual(sum(row["href"] == expected for row in connections[key]), 1)
                anchor = archive_anchor(records[key])
                row = archive.split('id="' + anchor + '"', 1)[1].split('</div>', 1)[0]
                self.assertIn('href="' + expected + '"', row)
                self.assertIn("心音與結構性心臟病", row)
        # All 49 old official identities remain; 33 get this additional, relevant topic link.
        self.assertEqual(sum(len(p.get("exam_questions", [])) for p in self.pages if
                             "heart-sounds-cross" in p["source"]), 49)
        self.assertEqual(render_related_questions(lesson, records, {}),
                         "", "Metadata links must not turn the main lesson back into an exam bank")
        from exam_archive import add_lesson_exam_backlinks
        headings = re.findall(r"(?m)^## (.+)$", (ROOT / lesson["source"]).read_text("utf8"))
        stub = "".join('<h2 id="part-' + str(i) + '">' + title + '</h2><p>Content</p>'
                       for i, title in enumerate(headings, 1))
        decorated = add_lesson_exam_backlinks(lesson, records, stub, ROOT)
        self.assertEqual(decorated.count('class="lesson-exam-backlinks"'), 8)
        self.assertEqual(decorated.count('href="xiaoma-exams.html#catalog-'), 33)
        for link in materials:
            record = records[question_key(link)]
            return_href = 'href="xiaoma-exams.html#' + archive_anchor(record) + '"'
            section = concept_url(lesson, link, ROOT).split("#part-", 1)[1]
            part = decorated.split('data-section="part-' + section + '"', 1)[1].split("</details>", 1)[0]
            self.assertIn(return_href, part)


    def test_related_exam_embed_flag_requires_boolean(self):
        pages = copy.deepcopy(self.pages)
        article = next(p for p in pages if p["output"] ==
                       "xiaoma-20261027-heart-sounds-structural-exam.html")
        article["related_exams"][0]["embed"] = "false"
        with self.assertRaisesRegex(ValueError, "embed flag must be a boolean"):
            validate_exam_catalog(pages)

    def test_future_year_sorts_above_108_automatically(self):
        pages = copy.deepcopy(self.pages)
        newer = copy.deepcopy(next(p for p in pages if p.get("exam")))
        newer["exam"] = {**newer["exam"], "year_roc": 109, "question_numbers": [1]}
        newer["exam_topics"] = {"1": "未來年度的題目"}
        newer["source"] = "content/example-future.md"
        newer["output"] = "example-future.html"
        pages.append(newer)
        html = render_exam_archive(pages)
        self.assertLess(html.index('id="year-109"'), html.index('id="year-108"'))
        self.assertIn("109 年（2020）", html)

    def test_question_collisions_fail_closed(self):
        pages = copy.deepcopy(self.pages)
        same = copy.deepcopy(next(p for p in pages if p.get("exam")))
        same["source"] = "content/other.md"
        same["output"] = "other.html"
        pages.append(same)
        with self.assertRaisesRegex(ValueError, "Duplicate exam question identity"):
            validate_exam_catalog(pages)

    def test_invalid_exam_identity_cannot_enter_archive(self):
        for key, val in (("year_roc", 2026), ("sitting", 0), ("stage", 3),
                         ("question_numbers", [0]), ("question_numbers", [2,2]), ("subject", "")):
            with self.subTest(key=key, value=val):
                pages = copy.deepcopy(self.pages)
                page = next(p for p in pages if p.get("exam"))
                page["exam"][key] = val
                with self.assertRaises(ValueError):
                    validate_exam_catalog(pages)

    def test_archive_has_a_public_page_and_keeps_old_links(self):
        outputs = {p["output"] for p in self.pages}
        for output in ("xiaoma-exams.html", "xiaoma-108a-cardiac-reasoning.html",
                       "xiaoma-exam108-renal-foundations.html", "xiaoma-exam108-renal-perfusion.html"):
            self.assertIn(output, outputs)
        markdown = (ROOT / "content/xiaoma-internal-medicine/exams/index.md").read_text("utf8")
        self.assertIn("XIAOMA_EXAM_ARCHIVE", markdown)
        portal = (ROOT / "content/xiaoma-internal-medicine/index.md").read_text("utf8")
        self.assertIn("XIAOMA_EXAM_YEAR_TEASERS", portal)
        self.assertIn("exams/index.md", portal)

if __name__=="__main__":
    unittest.main()
