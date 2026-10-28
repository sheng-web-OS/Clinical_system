"""Year-first registry for verified national physician exam questions.

Exam identity (ROC year, sitting, stage, paper, number) is immutable metadata.
Publication date is independent and cannot stand in for the exam year.
"""
from collections import defaultdict
from html import escape, unescape
import hashlib
from pathlib import Path
import re


IDENTITY_FIELDS = ("year_roc", "sitting", "stage", "subject", "question_number")


def question_key(exam):
    return tuple(exam[k] for k in IDENTITY_FIELDS)


def question_anchor(exam):
    paper = hashlib.sha256(exam["subject"].encode("utf8")).hexdigest()[:10]
    return "exam-{}-{}-{}-{}-q-{}".format(exam["year_roc"], exam["sitting"], exam["stage"], paper, exam["question_number"])


def archive_anchor(record):
    return "catalog-" + record["page"]["output"][:-5] + "-" + record["anchor"]


def question_records(pages):
    """Derive every official question from the one publication manifest."""
    records = []
    for page in pages:
        exam = page.get("exam")
        if exam:
            for number in exam["question_numbers"]:
                identity = {k: exam[k] for k in IDENTITY_FIELDS[:-1]}
                identity["question_number"] = number
                records.append({"exam": identity, "page": page, "anchor": "q-" + str(number),
                                "topic": page.get("exam_topics", {}).get(str(number), page["title"])})
        for question in page.get("exam_questions", []):
            identity = {k: question[k] for k in IDENTITY_FIELDS}
            records.append({"exam": identity, "page": page, "anchor": question_anchor(identity), "embedded": question,
                            "topic": question.get("topic", page["title"])})
    return records


def _validate_identity(exam):
    # Reuse the established year/paper validation for singular question records.
    year, sitting, stage, subject, number = question_key(exam)
    if type(year) is not int or not 90 <= year <= 150:
        raise ValueError("Exam ROC year must be a real integer")
    if type(sitting) is not int or not 1 <= sitting <= 4:
        raise ValueError("Exam sitting must be 1–4")
    if type(stage) is not int or stage not in (1, 2):
        raise ValueError("Exam stage must be 1 or 2")
    if not isinstance(subject, str) or not subject.strip() or subject != subject.strip() or len(subject) > 50:
        raise ValueError("Exam subject must be an exact nonempty paper name")
    if type(number) is not int or not 1 <= number <= 200:
        raise ValueError("Exam question_number must be a numeric ID")


def _headings(root, page, level):
    return re.findall(r"(?m)^" + "#" * level + r" (.+)$", (root / page["source"]).read_text("utf8"))


def _validate_heading_identity(question):
    heading = question["question_heading"]
    number = re.search(r"第\s*(\d+)\s*題", heading)
    year = re.search(r"(\d+)\s*年", heading)
    sitting = re.search(r"第([一二三四])次", heading)
    if ((number and int(number[1]) != question["question_number"]) or
            (year and int(year[1]) != question["year_roc"]) or
            (sitting and "一二三四".index(sitting[1]) + 1 != question["sitting"])):
        raise ValueError("Exam identity disagrees with question heading: " + heading)


def concept_url(page, link, root):
    heading = link.get("concept_heading")
    if heading is None:
        return page["output"] + "#reading-content"
    headings = _headings(root, page, 2)
    if headings.count(heading) != 1:
        raise ValueError("Related exam concept heading missing or ambiguous: " + page["source"] + " / " + str(heading))
    return page["output"] + "#part-" + str(headings.index(heading) + 1)


def validate_exam_catalog(pages, root=None):
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
    for page in pages:
        topics = page.get("exam_topics")
        if topics is not None:
            numbers = page.get("exam", {}).get("question_numbers", [])
            if (not isinstance(topics, dict) or not numbers or set(topics) - {str(n) for n in numbers}
                    or any(not isinstance(label, str) or not label.strip() or len(label) > 50 for label in topics.values())):
                raise ValueError("Exam topics must label existing question numbers with short text")
        embedded = page.get("exam_questions", [])
        if not isinstance(embedded, list):
            raise ValueError("exam_questions must be a list")
        if embedded and (not page.get("date") or page.get("collection") != "xiaoma-internal-medicine" or page.get("exam")):
            raise ValueError("Embedded official questions require a published concept lesson")
        heading_names = []
        if root is not None and embedded:
            heading_names = sum((_headings(root, page, level) for level in range(2, 5)), [])
        for question in embedded:
            required = set(IDENTITY_FIELDS) | {"question_heading"}
            if not isinstance(question, dict) or not required <= set(question) or set(question) - required - {"concept_heading", "focus", "topic"}:
                raise ValueError("Invalid embedded exam question metadata")
            _validate_identity(question)
            heading = question["question_heading"]
            if not isinstance(heading, str) or not heading.strip() or (root is not None and heading_names.count(heading) != 1):
                raise ValueError("Embedded exam question heading missing or ambiguous: " + page["source"])
            _validate_heading_identity(question)
            for field in ("concept_heading", "focus", "topic"):
                if field in question and (not isinstance(question[field], str) or not question[field].strip()):
                    raise ValueError("Embedded exam " + field + " must be nonempty text")
            if root is not None and question.get("concept_heading"):
                concept_url(page, question, root)
            key = question_key(question)
            if key in seen:
                raise ValueError("Duplicate exam question identity: " + repr(key))
            seen.add(key)
    records = {question_key(record["exam"]): record for record in question_records(pages)}
    for page in pages:
        links = page.get("related_exams", [])
        if not isinstance(links, list):
            raise ValueError("related_exams must be a list")
        if links and not page.get("date"):
            raise ValueError("Only published articles can carry related_exams")
        used = set()
        for link in links:
            required = set(IDENTITY_FIELDS) | {"focus"}
            if not isinstance(link, dict) or not required <= set(link) or set(link) - required - {"concept_heading", "question_heading", "embed"}:
                raise ValueError("Invalid related exam metadata")
            _validate_identity(link)
            if "embed" in link and not isinstance(link["embed"], bool):
                raise ValueError("Related exam embed flag must be a boolean")
            key = question_key(link)
            if key not in records:
                raise ValueError("Related exam is not a published official question: " + repr(key))
            if key in used:
                raise ValueError("Duplicate related exam within article: " + page["output"])
            used.add(key)
            if records[key]["page"]["output"] == page["output"]:
                raise ValueError("Use embedded question concept_heading for a question's own article")
            if not isinstance(link["focus"], str) or not link["focus"].strip():
                raise ValueError("Related exam must explain its learning connection")
            if root is not None:
                concept_url(page, link, root)
                if "question_heading" in link:
                    headings = sum((_headings(root, page, level) for level in range(2, 5)), [])
                    if headings.count(link["question_heading"]) != 1:
                        raise ValueError("Related exam question heading missing or ambiguous: " + page["source"])
                    _validate_heading_identity(link)
    return seen


def by_year(pages):
    validate_exam_catalog(pages)
    groups = defaultdict(lambda: defaultdict(list))
    lessons = {}
    for record in question_records(pages):
        e, page = record["exam"], record["page"]
        key = (page["output"], e["year_roc"], e["sitting"], e["stage"], e["subject"])
        if key not in lessons:
            row = dict(page, exam={k: e[k] for k in IDENTITY_FIELDS[:-1]})
            row["exam"]["question_numbers"] = []
            row["questions"] = []
            lessons[key] = row
            groups[e["year_roc"]][(e["sitting"], e["stage"], e["subject"])].append(row)
        lessons[key]["exam"]["question_numbers"].append(e["question_number"])
        lessons[key]["questions"].append(record)
    return groups


def question_connections(pages, root):
    links = defaultdict(list)
    for page in pages:
        for link in page.get("related_exams", []):
            links[question_key(link)].append({"page": page, "href": concept_url(page, link, root), "focus": link["focus"]})
        for question in page.get("exam_questions", []):
            if question.get("concept_heading"):
                links[question_key(question)].append({"page": page, "href": concept_url(page, question, root), "focus": question.get("focus", question["concept_heading"])})
    return links


def render_concept_links(connections, compact=False):
    if not connections:
        return ""
    if compact:
        items = ''.join('<li><a href="' + escape(link["href"], quote=True) + '">' + escape(link["page"]["title"]) + '</a></li>' for link in connections)
        return ('<details class="exam-catalog-materials"><summary>教材 ' + str(len(connections)) +
                '</summary><nav class="exam-concept-links" aria-label="對應教材"><ul>' + items + '</ul></nav></details>')
    items = ''.join('<li><a href="' + escape(link["href"], quote=True) + '">' + escape(link["page"]["title"]) +
                    '</a><small>' + escape(link["focus"]) + '</small></li>' for link in connections)
    return '<nav class="exam-concept-links" aria-label="對應教材"><span>回讀教材</span><ul>' + items + '</ul></nav>'


def render_exam_archive(pages, root=None):
    """Static reader-facing archive. No JavaScript or editorial internal metadata."""
    groups = by_year(pages)
    connections = question_connections(pages, root or Path(__file__).resolve().parents[1])
    if not groups:
        return '<p class="exam-archive-empty">目前尚未收錄完成題號與考選部原卷對應的正式真題詳解。</p>'
    pieces = ['<nav class="exam-year-jumps" aria-label="選擇考試年份">' + ''.join(
        '<a href="#year-' + str(year) + '">' + str(year) + ' 年</a>' for year in sorted(groups, reverse=True)) + '</nav>']
    for year in sorted(groups, reverse=True):
        total = sum(len(page["exam"]["question_numbers"]) for rows in groups[year].values() for page in rows)
        papers = len(groups[year])
        piece = ['<section class="exam-year" id="year-' + str(year) + '">',
                 '<h2>' + str(year) + ' 年（' + str(year+1911) + '）<span>' + str(total) + ' 題 · ' + str(papers) + ' 份試卷</span></h2>']
        for sitting, stage, subject in sorted(groups[year], key=lambda k:(k[0], k[1], k[2])):
            session_label = {1:"第一次",2:"第二次",3:"第三次",4:"第四次"}[sitting]
            rows = groups[year][(sitting, stage, subject)]
            stage_label = '醫師第一階段' if stage == 1 else '醫師第二階段'
            piece += ['<section class="exam-paper">',
                      '<h3><span>' + session_label + ' · ' + escape(subject) + '</span><small>' + stage_label + '</small></h3>',
                      '<div class="exam-question-list">']
            questions = sorted((record for row in rows for record in row["questions"]), key=lambda r: r["exam"]["question_number"])
            for record in questions:
                number = record["exam"]["question_number"]
                materials = connections.get(question_key(record["exam"]), [])
                data = ' data-materials="' + str(len(materials)) + '"' if materials else ''
                piece.append('<div class="exam-catalog-question" id="' + archive_anchor(record) + '"' + data +
                             '><a class="exam-question-entry" href="' + escape(record["page"]["output"], quote=True) + '#' + record["anchor"] +
                             '"><span class="exam-question-number">Q' + str(number) + '</span><span class="exam-question-topic">' +
                             escape(record["topic"]) + '</span></a>' + render_concept_links(materials, compact=True) + '</div>')
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


def question_bounds(body, record):
    """Read the rendered canonical question through its next peer heading."""
    headings = list(re.finditer(r'<h([2-6])\b[^>]*>.*?</h\1>', body, re.DOTALL))
    marker = 'id="' + record["anchor"] + '"'
    selected = [m for m in headings if marker in m.group()]
    if len(selected) != 1:
        raise ValueError("Official question anchor missing or repeated: " + record["page"]["output"] + "#" + record["anchor"])
    start = selected[0]
    if len(record["page"].get("exam", {}).get("question_numbers", [])) == 1:
        # Single-question lessons often put crucial bedside qualifications in
        # following H2 sections. They belong to this answer and must be retained.
        return start.start(), len(body)
    end = next((m.start() for m in headings if m.start() > start.start() and int(m.group(1)) <= int(start.group(1))), len(body))
    # Historical per-question bookmark spans precede their next heading.
    # Keep them with that next question rather than ahead of the previous footer.
    trailing_anchors = re.search(r'(?:\s*<span\b[^>]*\bid="[^"]+"[^>]*></span>)+\s*$', body[:end])
    if trailing_anchors:
        end = trailing_anchors.start()
    return start.start(), end


def scope_embedded_question(markup, record):
    """Keep SVG/MathML IDs unique and same-question links local to the embed."""
    prefix = "embed-" + archive_anchor(record) + "-"
    identifiers = set(re.findall(r'\bid="([^"]+)"', markup))
    markup = re.sub(r'\bid="([^"]+)"', lambda m: 'id="' + prefix + m[1] + '"', markup)
    canonical = record["page"]["output"]
    def fragment(match):
        target = unescape(match[1])
        return 'href="' + escape(("#" + prefix + target) if target in identifiers else (canonical + "#" + target), quote=True) + '"'
    markup = re.sub(r'href="#([^"]+)"', fragment, markup)
    markup = re.sub(r'\b(aria-labelledby|aria-describedby)="([^"]+)"',
                    lambda m: m[1] + '="' + ' '.join(prefix + ident if ident in identifiers else ident for ident in m[2].split()) + '"', markup)
    markup = re.sub(r'url\(#([^\)]+)\)', lambda m: 'url(#' + prefix + m[1] + ')' if m[1] in identifiers else m[0], markup)
    return re.sub(r'<(/?)h([2-5])\b', lambda m: '<' + m[1] + 'h' + str(int(m[2]) + 1), markup)


EXAM_NOTICE = "資料來源：考選部。本官方網站資料歡迎連結使用；引用時應註明來源、保持完整（包括本項宣示在內），不得任意增刪。"


def render_related_questions(page, records, rendered):
    cards = []
    for link in page.get("related_exams", []):
        if link.get("question_heading") or link.get("embed", True) is False:
            continue  # Link exam to the lesson without duplicating the full question bank.
        record = records[question_key(link)]
        origin = record["page"]
        body = rendered[origin["output"]]["body"]
        start, end = question_bounds(body, record)
        question = scope_embedded_question(body[start:end], record)
        exam = record["exam"]
        label = '{} 年 · 第{}次 · 醫師第{}階段 · {} · Q{}'.format(exam["year_roc"], "一二三四"[exam["sitting"]-1], "一二"[exam["stage"]-1], exam["subject"], exam["question_number"])
        source = origin.get("references")
        source_link = ('<a href="' + escape(source, quote=True) + '">官方原卷、答案與來源</a>') if source else ''
        cards.append('<section class="related-exam-card"><p class="related-exam-label">' + escape(label) +
                     '</p><p class="related-exam-focus">' + escape(link["focus"]) +
                     '</p><details class="related-exam-content"><summary>展開題目導讀與詳解</summary><div class="embedded-exam-body">' + question +
                     '<p class="exam-source-notice">' + EXAM_NOTICE + '</p></div></details><nav class="related-exam-actions" aria-label="題目導覽"><a href="' +
                     escape(origin["output"] + '#' + record["anchor"], quote=True) + '">開啟原詳解頁 →</a><a href="xiaoma-exams.html#' +
                     archive_anchor(record) + '">回到年份題目頁 →</a>' + source_link + '</nav></section>')
    if not cards:
        return ""
    return '<section class="article reading-prose related-exams" id="related-exams" aria-labelledby="related-exams-title"><h2 id="related-exams-title">相關國考題</h2>' + ''.join(cards) + '</section>'


def connect_exam_reading(pages, rendered, root):
    """Return decorated bodies and supplements; original Markdown stays intact."""
    records = question_records(pages)
    catalog = {question_key(record["exam"]): record for record in records}
    connections = question_connections(pages, root)
    by_page = defaultdict(list)
    for record in records:
        by_page[record["page"]["output"]].append(record)
    for page in pages:
        for link in page.get("related_exams", []):
            if link.get("question_heading"):
                canonical = catalog[question_key(link)]
                by_page[page["output"]].append(dict(canonical, page=page, anchor=question_anchor(link), canonical=canonical))
    results = {}
    for page in pages:
        body = rendered[page["output"]]["body"]
        inserts = []
        for record in by_page[page["output"]]:
            _, end = question_bounds(body, record)
            links = render_concept_links(connections.get(question_key(record["exam"]), []))
            canonical = record.get("canonical", record)
            year = '<a class="exam-year-return" href="xiaoma-exams.html#' + archive_anchor(canonical) + '">回到年份題目頁 →</a>'
            if "canonical" in record:
                year += '<a class="exam-year-return" href="' + canonical["page"]["output"] + '#' + canonical["anchor"] + '">開啟完整原詳解 →</a>'
            inserts.append((end, '<aside class="exam-question-return">' + links + year + '</aside>'))
        for end, markup in sorted(inserts, reverse=True):
            body = body[:end] + markup + body[end:]
        supplement = render_related_questions(page, catalog, rendered)
        if inserts or supplement:
            results[page["output"]] = (body, supplement)
    return results
