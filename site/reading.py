"""Daily discovery and complete atlas index, both from the publication catalog."""
from collections import defaultdict
from datetime import datetime, timezone
from html import escape
from zoneinfo import ZoneInfo


def taipei_day(now=None):
    return (now or datetime.now(timezone.utc)).astimezone(ZoneInfo("Asia/Taipei")).date().isoformat()


def articles(pages):
    return [p for p in pages if p.get("date")]


def is_reference_page(row):
    """Source/provenance pages are citations, not independent reading recommendations."""
    return (row.get("review") == "source_audit"
            or row.get("kind") == "source_reference"
            or row.get("source", "").endswith("-sources.md"))


def is_current_lesson(row):
    """Discovery eligibility is editorial, not implied by a publication date."""
    collection = row.get("collection")
    # Editorial articles in Clinical OS are genuine teaching readings too.
    # Exam question compilations and provenance remain separate discovery paths.
    eligible_collection = (collection == "xiaoma-internal-medicine"
                           or (collection == "clinical-os"
                               and row.get("kind") == "ai_integrated"))
    return (bool(row.get("date"))
            and eligible_collection
            and row.get("kind") not in ("historical_original", "exam_compilation")
            and "/exams/" not in row.get("source", "")
            and not row.get("exam")
            and not is_reference_page(row)
            and "練習" not in row.get("section", ""))


def render_today_updates(pages, today=None):
    today = today or taipei_day()
    rows = [p for p in articles(pages)
            if is_current_lesson(p) and p.get("updated", p["date"]) == today]
    cards = []
    for row in sorted(rows, key=lambda p: (p.get("section", ""), p["title"])):
        cards.append('<a class="lesson-card" data-updated="' + today + '" href="' +
                     escape(row["output"], quote=True) + '"><span class="lesson-date">' +
                     escape(row.get("section", "內科閱讀")) + ' / 更新 ' + today +
                     '</span><strong>' + escape(row["title"]) + '</strong><p>' +
                     escape(row["subtitle"]) + '</p><span class="lesson-card-end">進入閱讀 ↗</span></a>')
    return ('<div data-today-updates><p>今日更新 · <time data-today-label>' + today +
            '</time>（台灣時間）</p><div class="lesson-list">' + ''.join(cards) +
            '</div><p data-today-empty' + (' hidden' if cards else '') +
            '>今日尚無文章更新。</p><p><a href="knowledge-atlas.html#article-index">到知識地圖查找全部文章與閱讀順序 →</a></p></div>')


def _group(row):
    if row.get("exam") or row.get("kind") == "exam_compilation" or "練習" in row.get("section", ""):
        return "國考詳解與練習"
    section = row.get("section", "")
    if any(key in section for key in ("胸腔", "呼吸", "酸鹼", "重症")):
        return "呼吸、酸鹼與重症"
    if any(key in section for key in ("神經", "癲癇")):
        return "神經與急症"
    if "心律" in section:
        return "心律與急救"
    if "血栓" in section:
        return "血栓與診斷"
    if any(key in section for key in ("心", "瓣膜", "利尿")):
        return "心臟、循環與利尿"
    if any(key in section for key in ("肝", "膽", "腸", "消化", "胰")):
        return "消化與肝膽"
    return section or "其他閱讀"


def primary_versions(pages):
    """Explicit approved new-reading -> preserved-source pairs; topic alone never implies replacement."""
    by_output = {p["output"]: p for p in pages}
    original_to_primary = {}
    for current in pages:
        old_output = current.get("replaces_original")
        if not old_output:
            continue
        old = by_output.get(old_output)
        if (old is None or old.get("kind") != "historical_original"
                or current.get("kind") != "ai_integrated"
                or current.get("collection") != old.get("collection")
                or _group(current) != _group(old)):
            raise ValueError("Invalid canonical reading / preserved original pairing: " + current["output"])
        if old_output in original_to_primary:
            raise ValueError("Original has competing primary readings: " + old_output)
        original_to_primary[old_output] = current
    return original_to_primary


def render_original_versions(pages, collection):
    """Compact provenance lookup, not a parallel article directory."""
    primary = primary_versions(pages)
    originals = sorted((p for p in pages
                        if p.get("kind") == "historical_original"
                        and p.get("collection") == collection),
                       key=lambda p: (p["date"], p["title"]))
    lines = ['<ul class="archive-version-list">']
    for row in originals:
        current = primary.get(row["output"])
        label = (' · <a href="' + escape(current["output"], quote=True) +
                 '">閱讀整合版</a>') if current else ' · 目前尚無完整整合版'
        lines.append('<li><a href="' + escape(row["output"], quote=True) + '">' +
                     escape(row["title"]) + '</a><small>原稿版本' + label + '</small></li>')
    lines.append('</ul>')
    return ''.join(lines)


def render_article_index(pages):
    groups = defaultdict(list)
    primary = primary_versions(pages)
    for row in articles(pages):
        if is_reference_page(row):
            continue  # Provenance is reached from its lesson, never a standalone article.
        if row["output"] in primary:
            continue  # Archived source stays as a small link attached to its current reading.
        groups[_group(row)].append(row)
    result = ['<div class="atlas-article-index">']
    for label in sorted(groups):
        rows = groups[label]
        result.append('<details><summary>' + escape(label) + ' · ' + str(len(rows)) + ' 篇</summary><ul>')
        for row in sorted(rows, key=lambda p: (p["date"], p["title"])):
            if row.get("replaces_original"):
                version = (' <small class="atlas-source-link">版本對照：<a href="' +
                           escape(row["replaces_original"], quote=True) + '">原稿</a></small>')
            elif row.get("kind") == "historical_original":
                version = ' <small class="atlas-origin-note">原稿・尚無完整整合版</small>'
            else:
                version = ''
            result.append('<li><a href="' + escape(row["output"], quote=True) + '">' +
                          escape(row["title"]) + '</a>' + version + '</li>')
        result.append('</ul></details>')
    result.append('</div>')
    return ''.join(result)
