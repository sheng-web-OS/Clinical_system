"""Daily discovery and complete atlas index, both from the publication catalog."""
from collections import defaultdict
from datetime import datetime, timezone
from html import escape
from zoneinfo import ZoneInfo


def taipei_day(now=None):
    return (now or datetime.now(timezone.utc)).astimezone(ZoneInfo("Asia/Taipei")).date().isoformat()


def articles(pages):
    return [p for p in pages if p.get("date")]


def render_today_updates(pages, today=None):
    today = today or taipei_day()
    rows = [p for p in articles(pages)
            if p.get("kind") != "historical_original" and not p.get("exam")
            and p.get("updated", p["date"]) == today]
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
    if row.get("kind") == "historical_original":
        return "歷史原稿典藏"
    if row.get("exam") or "練習" in row.get("section", ""):
        return "國考詳解與練習"
    section = row.get("section", "")
    if any(key in section for key in ("胸腔", "呼吸", "酸鹼", "重症")):
        return "呼吸、酸鹼與重症"
    if "心律" in section:
        return "心律與急救"
    if "血栓" in section:
        return "血栓與診斷"
    if any(key in section for key in ("心", "瓣膜", "利尿")):
        return "心臟、循環與利尿"
    if any(key in section for key in ("肝", "膽", "腸")):
        return "肝膽與腸道"
    return section or "其他閱讀"


def render_article_index(pages):
    groups = defaultdict(list)
    for row in articles(pages):
        groups[_group(row)].append(row)
    result = ['<div class="atlas-article-index">']
    for label in sorted(groups, key=lambda s: (s == "歷史原稿典藏", s)):
        rows = groups[label]
        result.append('<details><summary>' + escape(label) + ' · ' + str(len(rows)) + ' 篇</summary><ul>')
        for row in sorted(rows, key=lambda p: (p["date"], p["title"])):
            result.append('<li><a href="' + escape(row["output"], quote=True) + '">' +
                          escape(row["title"]) + '</a></li>')
        result.append('</ul></details>')
    result.append('</div>')
    return ''.join(result)
