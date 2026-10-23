"""Year-first registry for verified national physician exam questions.

Exam identity (ROC year, sitting, stage, paper, number) is immutable metadata.
Publication date is independent and cannot stand in for the exam year.
"""
from collections import defaultdict
from html import escape
import re


def validate_exam_catalog(pages):
    seen = set()
    for page in pages:
        exam = page.get("exam")
        if exam is None:
            continue
        if not isinstance(exam, dict) or set(exam) != {"year_roc", "sitting", "stage", "subject", "question_numbers"}:
            raise ValueError("Exam metadata must provide year_roc, sitting, stage, subject, question_numbers")
        if page.get("collection") != "xiaoma-internal-medicine" or not page.get("date"):
            raise ValueError("Only published exam lessons can carry exam metadata")
        year, sitting, stage, subject, numbers = (exam[k] for k in ("year_roc", "sitting", "stage", "subject", "question_numbers"))
        if type(year) is not int or not 90 <= year <= 150:
            raise ValueError("Exam ROC year must be a real integer")
        if type(sitting) is not int or not 1 <= sitting <= 4:
            raise ValueError("Exam sitting must be 1–4")
        if type(stage) is not int or stage not in (1, 2):
            raise ValueError("Exam stage must be 1 or 2")
        if not isinstance(subject, str) or not subject.strip() or subject != subject.strip() or len(subject) > 50:
            raise ValueError("Exam subject must be an exact nonempty paper name")
        if not isinstance(numbers, list) or not numbers or any(type(n) is not int or not 1 <= n <= 200 for n in numbers):
            raise ValueError("Exam question_numbers must be nonempty numeric IDs")
        if len(numbers) != len(set(numbers)):
            raise ValueError("Duplicate question number within a lesson")
        for q in numbers:
            key = (year, sitting, stage, subject, q)
            if key in seen:
                raise ValueError("Duplicate exam question identity: " + repr(key))
            seen.add(key)
    return seen


def by_year(pages):
    validate_exam_catalog(pages)
    groups = defaultdict(lambda: defaultdict(list))
    for page in pages:
        e = page.get("exam")
        if e:
            groups[e["year_roc"]][(e["sitting"], e["stage"], e["subject"])].append(page)
    return groups


def render_exam_archive(pages):
    """Static reader-facing archive. No JavaScript or editorial internal metadata."""
    groups = by_year(pages)
    if not groups:
        return '<p class="exam-archive-empty">目前尚未收錄完成題號與考選部原卷對應的正式真題詳解。</p>'
    pieces = []
    for year in sorted(groups, reverse=True):
        total = sum(len(page["exam"]["question_numbers"]) for rows in groups[year].values() for page in rows)
        papers = len(groups[year])
        piece = ['<section class="exam-year" id="year-' + str(year) + '">',
                 '<h2>' + str(year) + ' 年（' + str(year+1911) + '）<span>' + str(total) + ' 題 · ' + str(papers) + ' 份試卷</span></h2>']
        for sitting, stage, subject in sorted(groups[year], key=lambda k:(k[0], k[1], k[2])):
            session_label = {1:"第一次",2:"第二次",3:"第三次",4:"第四次"}[sitting]
            rows = groups[year][(sitting, stage, subject)]
            piece += ['<section class="exam-paper">',
                      '<h3>' + session_label + ' · 醫師' + ('第一階段' if stage == 1 else '第二階段') + ' · ' + escape(subject) + '</h3>',
                      '<div class="exam-lesson-list">']
            for row in sorted(rows, key=lambda p: min(p["exam"]["question_numbers"])):
                nums = sorted(row["exam"]["question_numbers"])
                ident = "、".join(str(n) for n in nums)
                links = ''.join('<a href="' + escape(row["output"], quote=True) + '#q-' + str(n) +
                                '" aria-label="直接閱讀第 ' + str(n) + ' 題">Q' + str(n) + '</a>' for n in nums)
                piece.append('<article class="exam-lesson"><a class="exam-lesson-title" href="' +
                             escape(row["output"], quote=True) + '"><strong>' + escape(row["title"]) +
                             '</strong><small>' + escape(row["subtitle"]) +
                             '</small></a><nav class="exam-question-links" aria-label="各題直接入口">' +
                             links + '</nav></article>')
            piece += ['</div>', '</section>']
        piece.append('</section>')
        pieces.extend(piece)
    return '\n'.join(pieces)


def render_exam_year_teasers(pages):
    groups = by_year(pages)
    if not groups:
        return '<p>已確認的歷屆考題詳解會依考試年度建立獨立入口。</p>'
    cards = []
    for year in sorted(groups, reverse=True):
        total = sum(len(row["exam"]["question_numbers"]) for rows in groups[year].values() for row in rows)
        cards.append('<a href="xiaoma-exams.html#year-' + str(year) + '">' +
                     '<strong>' + str(year) + ' 年（' + str(year + 1911) + '）</strong>' +
                     '<span>' + str(total) + ' 題已收錄 · 依考試梯次、科目與題號查找 →</span></a>')
    return '<div class="exam-archive-entry">' + ''.join(cards) + '</div>'
