#!/usr/bin/env python3
"""Deterministic static-site compiler. Markdown is the sole editorial source."""
from pathlib import Path
import html
import json
import re
import shutil
import sys
import mistune
from catalog import load_pages
from home import render_home
from reading import render_today_updates, render_article_index, render_original_versions, primary_versions, is_current_lesson
from math_render import compile_math
from exam_archive import render_exam_archive, render_exam_year_teasers, question_anchor, connect_exam_reading

BASE = Path(__file__).resolve().parents[1]
DIST = BASE / "dist"
PAGES = load_pages(BASE)
FILES = [(row["source"], row["output"], row["title"], row["subtitle"]) for row in PAGES]
# Single source of truth for the privacy-preserving Cloudflare Web Analytics beacon.
# The token is a public site identifier, not an API credential.
# Owner opt-out is browser-local, applied before the analytics script can load.
# An inert config tag keeps the token in one location and avoids a beacon for owners.
WEB_ANALYTICS_BEACON = """<template id="clinical-analytics-config" data-src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token":"c6bb7055c62648c39f440da91304c99e"}'></template>
<script>
(function () {
  try {
    if (localStorage.getItem("clinical-analytics-owner-v1") === "1") return;
  } catch (error) { /* Private browsing or disabled storage: retain normal analytics. */ }
  var config = document.getElementById("clinical-analytics-config");
  var beacon = document.createElement("script");
  beacon.src = config.getAttribute("data-src");
  beacon.setAttribute("data-cf-beacon", config.getAttribute("data-cf-beacon"));
  beacon.async = true;
  document.head.appendChild(beacon);
}());
</script>"""

def install_web_analytics():
    """Instrument canonical published pages once; never count legacy redirects twice."""
    published = {"index.html"} | {page["output"] for page in PAGES}
    for filename in sorted(published):
        path = DIST / filename
        document = path.read_text(encoding="utf-8")
        if document.count("</head>") != 1 or "static.cloudflareinsights.com/beacon.min.js" in document:
            raise ValueError("Cannot install exactly one analytics beacon into " + filename)
        path.write_text(document.replace("</head>", WEB_ANALYTICS_BEACON + "</head>", 1), encoding="utf-8")

class Renderer(mistune.HTMLRenderer):
    def __init__(self, question_anchors=None):
        super().__init__(escape=False)
        self.headings=[]
        self.h2=0
        self.question_anchors = question_anchors or {}
    def heading(self, text, level, **attrs):
        key = html.unescape(re.sub(r"<[^>]+>", "", text))
        question_id = self.question_anchors.get(key)
        embedded_anchor = '<span class="exam-question-anchor" id="' + question_id + '"></span>' if question_id else ''
        if level==2:
            self.h2+=1
            ident="part-"+str(self.h2)
            self.headings.append((ident,re.sub(r"<[^>]+>","",text)))
            question = re.match(r"^第\s*(\d+)\s*題", re.sub(r"<[^>]+>", "", text))
            anchor = ('<span class="exam-question-anchor" id="q-' + str(int(question.group(1))) + '"></span>') if question else ''
            return '<h2 id="'+ident+'">'+anchor+embedded_anchor+text+'</h2>'
        return '<h'+str(level)+'>'+embedded_anchor+text+'</h'+str(level)+'>'

OUTPUT_BY_SOURCE = {name: output for name, output, _, _ in FILES}
# Old Markdown links resolve to the single public atlas, not to an unpublished twin.
OUTPUT_BY_SOURCE["content/xiaoma-internal-medicine/learning-map.md"] = "knowledge-atlas.html"

def rewrite_internal_links(markup, source_path):
    """Map source-Markdown links to destination HTML pages; keep external refs unchanged."""
    source_folder = (BASE/source_path).parent
    def replace(match):
        href = html.unescape(match.group(1))
        if href.startswith(("http:", "https:", "mailto:", "tel:", "//", "#", "data:")):
            return match.group(0)
        location, _, fragment = href.partition("#")
        try:
            resolved = (source_folder/location).resolve().relative_to(BASE).as_posix()
        except ValueError:
            raise ValueError("Local link escapes repository: "+href)
        destination = OUTPUT_BY_SOURCE.get(resolved)
        if destination is None:
            return match.group(0)
        return 'href="' + html.escape(destination + (("#"+fragment) if fragment else ""),quote=True) + '"'
    return re.sub(r'href="([^"]+)"',replace,markup)

def render_mechanism(match):
    """Render a simple native HTML flowchart from the source Mermaid topology."""
    source = html.unescape(match.group(1))
    pairs = re.findall(r'([A-Z])\["([^"]+)"\]',source)
    nodes=dict(pairs)
    edges=re.findall(r'\b([A-Z])(?:\["[^"]+"\])?\s*-->\s*([A-Z])',source)
    if not nodes or not edges:
        raise ValueError("Mermaid diagram not parseable; block unsafe silent fallback")
    levels={name:0 for name in nodes}
    for _ in range(len(nodes)):
        new=dict(levels)
        for a, z in edges:
            if a not in levels or z not in levels:
                raise ValueError("Mermaid edge has missing node")
            new[z]=max(new[z],levels[a]+1)
        if new==levels: break
        levels=new
    sections=[]
    for level in sorted(set(levels.values())):
        if sections: sections.append('<div class="causal-down" aria-hidden="true">↓</div>')
        names=[n for n in nodes if levels[n]==level]
        cards=''.join('<div class="causal-card">'+html.escape(nodes[n])+'</div>' for n in names)
        sections.append('<div class="causal-tier">'+cards+'</div>')
    label=' · '.join(html.escape(v) for v in nodes.values())
    note=re.search(r'\b([A-Z])\s*-\.\s*"([^"]+)"\s*\.-\>\s*([A-Z])',source)
    foot=('<figcaption>'+html.escape(nodes[note.group(1)]+' → '+nodes[note.group(3)]+': '+note.group(2))+'</figcaption>') if note else ''
    return '<figure class="causal-map" role="group" aria-label="臨床生理因果關係">'+''.join(sections)+foot+'</figure>'

def validate_output_links():
    """Gate the generated site itself; source-only checking misses rebasing defects."""
    for path in DIST.glob("*.html"):
        contents=path.read_text(encoding="utf8")
        for link in re.findall(r'(?:href|src)="([^"]+)"',contents):
            if link.startswith(("http:","https:","mailto:","tel:","//","#","data:")): continue
            target=link.split("#",1)[0]
            if not target:continue
            if not (DIST/target).is_file():
                raise ValueError("Generated HTML broken link: "+path.name+" => "+link)

def render_reader(page, body, headings, related_questions=""):
    """Reader-facing teaching, with routes and editorial records in separate pages."""
    is_lesson = is_current_lesson(page) or page["source"] == "content/tamponade.md"
    is_archive = page.get("collection") == "xiaoma-reading"
    is_xiaoma = page.get("collection", "").startswith("xiaoma-")
    home = "xiaoma-reading.html" if is_archive else ("xiaoma-internal-medicine.html" if is_xiaoma else "index.html")
    site_name = "小麻閱讀" if is_archive else ("小麻內科國考" if is_xiaoma else "臨床閱讀")
    items = []
    for index, (ident, title) in enumerate(headings, 1):
        short = re.sub(r"^\d+\s*", "", title)
        items.append('<a href="#'+ident+'"><span>'+str(index).zfill(2)+'</span>'+html.escape(short)+'</a>')
    outline = ''.join(items)
    title = html.escape(page["title"])
    subtitle = html.escape(page["subtitle"])
    section = html.escape(page.get("section", "小麻閱讀" if is_archive else "臨床推理"))
    exam = page.get("exam")
    exam_label = ('<div class="reader-exam-origin"><span>官方歷屆真題</span><a href="xiaoma-exams.html#year-' + str(exam["year_roc"]) + '">' +
                  str(exam["year_roc"]) + ' 年（' + str(exam["year_roc"] + 1911) + '） · ' +
                  {1: '第一次', 2: '第二次', 3: '第三次', 4: '第四次'}[exam["sitting"]] +
                  ' · 醫師' + ('第一階段' if exam["stage"] == 1 else '第二階段') + ' · ' + html.escape(exam["subject"]) +
                  ' · Q' + '、'.join(str(q) for q in sorted(exam["question_numbers"])) + ' →</a></div>') if exam else ''
    mode = "lesson-page" if is_lesson or page["source"] == "content/tamponade.md" else "directory-page"
    if not is_xiaoma:
        mode += " clinical-page"
    active = page["output"]
    references = page.get("references") or ("xiaoma-sources.html" if page.get("collection") == "xiaoma-internal-medicine" else None)
    reference_link = '<a href="'+html.escape(references,quote=True)+'">來源與延伸閱讀</a>' if references else ''
    lessons = sorted((row for row in PAGES if row.get("collection") == page.get("collection") and is_current_lesson(row)), key=lambda row: (row["date"], row["output"]))
    number = next((str(i).zfill(2) for i, row in enumerate(lessons, 1) if row["output"] == active), "")
    destinations = ([("index.html", "首頁"), ("knowledge-atlas.html", "知識地圖"), ("xiaoma-reading.html", "小麻閱讀"), ("xiaoma-internal-medicine.html", "內科國考") ]
                    if is_archive else
                    [("index.html", "首頁"), ("knowledge-atlas.html", "知識地圖"), ("xiaoma-internal-medicine.html", "內科國考"), ("xiaoma-reading.html", "小麻閱讀") ])
    top_links = ''.join('<a'+(' aria-current="page"' if active == dest else '')+' href="'+html.escape(dest,quote=True)+'">'+label+'</a>' for dest, label in destinations)
    brand = '<a class="reader-brand" href="index.html"><span class="brand-mark" aria-hidden="true">小</span>小麻閱讀<span>MEDICAL READING</span></a>'
    original_note = ('<aside class="original-reading-end"><a href="xiaoma-reading.html">← 回到小麻閱讀</a><p>本文保留 '+html.escape(page.get("date", "").replace("-", "."))+' 原稿。臨床處置請一併核對所附來源與現行指引。</p></aside>') if page.get("kind") == "historical_original" else ''
    primary = primary_versions(PAGES).get(active) if page.get("kind") == "historical_original" else None
    original_primary_note = ('<p class="original-reading-primary">這是保存的原稿版本。主要閱讀請看 <a href="' +
                             html.escape(primary["output"], quote=True) + '">' +
                             html.escape(primary["title"]) + '</a>。</p>') if primary else ''
    return '''<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="'''+html.escape(page["title"]+' · '+page["subtitle"],quote=True)+'''">
<title>'''+title+' · '+site_name+'''</title><link rel="stylesheet" href="styles.css"></head><body class="reader-page '''+mode+'''">
<a class="skip-link" href="#reading-content">跳到正文</a><div class="floating" aria-hidden="true"></div>
<header class="reader-header">'''+brand+'''<nav aria-label="主要導覽">'''+top_links+'''</nav><details class="reader-search"><summary>搜尋</summary><div><label for="search">搜尋教材</label><input id="search" class="searchbox" type="search" placeholder="輸入主題或問題…"><div class="results" id="results" aria-live="polite"></div></div></details><div class="reader-tools"><button id="fontminus" aria-label="縮小字體">A−</button><button id="fontplus" aria-label="放大字體">A+</button><button id="theme" aria-label="切換明暗主題">◐</button></div></header>
<div class="reader-shell"><aside class="reader-rail"><a class="back-link" href="'''+home+'''">← 教材目錄</a><span class="rail-label">'''+('本篇脈絡' if is_lesson else '本頁導覽')+'''</span><nav class="reader-outline" aria-label="章節導覽">'''+outline+'''</nav><div class="rail-bottom"><a href="xiaoma-reading.html">以往小麻閱讀 ↗</a><a href="knowledge-atlas.html">臨床知識地圖 ↗</a><a href="index.html">其他臨床教材 ↗</a></div></aside>
<main class="reader-main" id="reading-content"><div class="reader-hero"><p class="reader-kicker">'''+section+('　 /　 '+number if number else '')+'''</p><h1>'''+title+'''</h1><p class="reader-deck">'''+subtitle+'''</p>'''+exam_label+'''</div>
<details class="mobile-outline"><summary>本篇章節</summary><nav aria-label="行動版章節導覽">'''+outline+'''</nav></details>
<div class="article reading-prose">'''+original_primary_note+'''</div><article class="article reading-prose">'''+body+'''</article>'''+original_note+related_questions+'''<footer class="reader-footer"><a href="'''+home+'''">'''+site_name+'''</a><span>把問題想通，再往下一步。</span>'''+reference_link+'''</footer></main></div>
<script src="site-index.js"></script><script src="app.js" defer></script></body></html>'''


def embed_inline_source_figure(body, page):
    """Insert a sourced visual in the rendered page; never mutate archived author text."""
    figure = page.get("inline_source_figure")
    if not figure:
        return body
    marker = "<p>" + html.escape(figure["before_text"], quote=False)
    if body.count(marker) != 1:
        raise ValueError("Inline source figure insertion point missing/ambiguous: " + page["output"])
    image_url = html.escape(figure["image_url"], quote=True)
    source_url = html.escape(figure["official_source_url"], quote=True)
    alt = html.escape(figure["alt"], quote=True)
    caption = html.escape(figure["caption"])
    qualification = html.escape(figure["qualification"])
    block = ('<figure class="inline-source-figure" id="aes-cse-2016-figure">'
             '<a class="inline-source-image" href="' + image_url + '" target="_blank" rel="noopener noreferrer" '
             'aria-label="開啟完整 AES 2016 status epilepticus 流程圖">'
             '<img src="' + image_url + '" width="753" height="998" loading="lazy" decoding="async" alt="' + alt + '"></a>'
             '<figcaption><span>' + caption + '</span> '
             '<a href="' + source_url + '" target="_blank" rel="noopener noreferrer">AES 官方完整 PDF</a>'
             '<small>' + qualification + '</small></figcaption></figure>')
    return body.replace(marker, block + marker, 1)

def render(md_file, output, page_title, subtitle, rendered=None):
    raw=(BASE/md_file).read_text(encoding="utf-8")
    current=next(row for row in PAGES if row["output"]==output)
    # Preserve the chat-supplied original bytes on disk; only suppress a
    # duplicate plain-text first-line title in the rendered HTML, as for # H1.
    if current.get("kind") == "historical_original":
        head, _, tail = raw.partition("\n")
        if head.strip() == current["title"] and tail:
            raw = tail.lstrip("\n")
    if "<!-- XIAOMA_READING_ORIGINALS -->" in raw:
        raw=raw.replace("<!-- XIAOMA_READING_ORIGINALS -->",
                        render_original_versions(PAGES, current.get("collection")))
    if "<!-- XIAOMA_EXAM_YEAR_TEASERS -->" in raw:
        raw = raw.replace("<!-- XIAOMA_EXAM_YEAR_TEASERS -->", render_exam_year_teasers(PAGES))
    if "<!-- XIAOMA_EXAM_ARCHIVE -->" in raw:
        raw = raw.replace("<!-- XIAOMA_EXAM_ARCHIVE -->", render_exam_archive(PAGES, BASE))
    if "<!-- XIAOMA_TODAY_UPDATES -->" in raw:
        raw = raw.replace("<!-- XIAOMA_TODAY_UPDATES -->", render_today_updates(PAGES))
    if "<!-- XIAOMA_ATLAS_ARTICLES -->" in raw:
        raw = raw.replace("<!-- XIAOMA_ATLAS_ARTICLES -->", render_article_index(PAGES))
    raw=re.sub(r'<!-- (U0[1-8]) -->',lambda m:'<a class="chapter-anchor" id="'+m.group(1).lower()+'"></a>',raw)
    # Compile MathML from authored TeX before Mistune consumes \\[...\\] as escapes.
    raw=compile_math(raw)
    question_entries = current.get("exam_questions", []) + current.get("related_exams", [])
    rr=Renderer({q["question_heading"].replace("**", ""): question_anchor(q) for q in question_entries if q.get("question_heading")})
    parser=mistune.create_markdown(renderer=rr,plugins=["table","strikethrough","url"])
    body=parser(raw)
    body=re.sub(r"^<h1>[^<]*</h1>", "", body, count=1)  # accessible single H1 in page hero
    body=re.sub(r'<pre><code class="language-mermaid">([\s\S]*?)</code></pre>',render_mechanism,body)
    body=rewrite_internal_links(body,md_file)
    body=embed_inline_source_figure(body,current)
    if rendered is not None:
        rendered[output] = {"body": body, "headings": rr.headings}
    current=next(row for row in PAGES if row["output"]==output)
    website = render_reader(current, body, rr.headings)
    (DIST/output).write_text(website,encoding="utf-8")
    return {"title":page_title,"url":output,"text":re.sub(r"\s+"," ",re.sub(r"<[^>]*>"," ",body))[:60000]}
def main():
    if DIST.exists():shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for name in ("styles.css","home.css","app.js","owner-mode.html"):
        shutil.copyfile(BASE/"site"/name,DIST/name)
    # Exact source screenshots are checked-in binary files, not transient CDN URLs.
    # Copy only the two reviewed Pocket Medicine extracts into the site root.
    for image_name in ("pocket-medicine-9e-fig2-5-hypoxemia.png", "pocket-medicine-9e-high-paco2.png"):
        source_image = BASE / "site" / "source_figure_images" / image_name
        if not source_image.is_file():
            raise FileNotFoundError("Reviewed source figure missing: " + str(source_image))
        shutil.copyfile(source_image, DIST / image_name)
    # Bundle reviewed CTICU SVG alongside its generated flat reader route.
    if any(page["output"] == "xiaoma-20261027-cticu-oxygen-delivery.html" for page in PAGES):
        oxygen_figure = BASE / "content/xiaoma-internal-medicine/lessons/cticu-oxygen-delivery-two-paths.svg"
        if not oxygen_figure.is_file():
            raise FileNotFoundError("CTICU oxygen delivery figure missing: " + str(oxygen_figure))
        shutil.copyfile(oxygen_figure, DIST / oxygen_figure.name)
    # New CTICU ABG artwork is shipped only with a fully approved catalog entry.
    # Unapproved source files on a draft PR must not leak into the public dist.
    cticu_figures = {
        "xiaoma-20261029-cticu-abg-03-cpb-acidbase.html": "cticu-abg-03-cpb-acidbase-group-trends.svg",
        "xiaoma-20261029-cticu-abg-04-alphastat-phstat.html": "cticu-abg-04-alpha-phstat-logic.svg",
    }
    for page_output, image_name in cticu_figures.items():
        if any(page["output"] == page_output for page in PAGES):
            candidate_image = BASE / "content/xiaoma-internal-medicine/lessons" / image_name
            if not candidate_image.is_file():
                raise FileNotFoundError("CTICU release figure missing: " + str(candidate_image))
            shutil.copyfile(candidate_image, DIST / image_name)
    rendered = {}
    rows=[render(*entry, rendered=rendered) for entry in FILES]
    connected = connect_exam_reading(PAGES, rendered, BASE)
    for page in PAGES:
        if page["output"] not in connected:
            continue
        body, supplement = connected[page["output"]]
        headings = rendered[page["output"]]["headings"] + ([("related-exams", "相關國考題")] if supplement else [])
        (DIST / page["output"]).write_text(render_reader(page, body, headings, supplement), encoding="utf8")
    # Former published DCM link must open the current approved reading, not
    # silently strand returning readers in the preserved historical manuscript.
    legacy, current = "xiaoma-reading-20260710-dcm.html", "xiaoma-reading-dcm-integrated.html"
    if not (DIST/current).is_file() or (DIST/legacy).exists():
        raise ValueError("DCM reading version targets missing or in conflict")
    redirect = ('<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                '<meta http-equiv="refresh" content="0; url='+current+'">'
                '<meta name="robots" content="noindex,follow">'
                '<link rel="canonical" href="'+current+'">'
                '<title>心肌病變｜請閱讀新版</title><link rel="stylesheet" href="styles.css"></head>'
                '<body class="reader-page"><main style="max-width:42rem;margin:12vh auto;padding:2rem">'
                '<h1>心肌病變已更新</h1><p>此網址已改為新版文章入口。'
                '如未自動跳轉，請<a href="'+current+'">閱讀最新整合版</a>。</p>'
                '</main></body></html>')
    (DIST/legacy).write_text(redirect, encoding="utf-8")
    # Keep returning readers' bookmarks but retire the duplicate reading-map page.
    # A standalone, non-indexed HTML alias mirrors the existing DCM migration.
    atlas, old_map = "knowledge-atlas.html", "xiaoma-plan.html"
    if not (DIST/atlas).is_file() or (DIST/old_map).exists():
        raise ValueError("Clinical atlas redirect target missing or in conflict")
    atlas_redirect = ('<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8">'
                      '<meta name="viewport" content="width=device-width,initial-scale=1">'
                      '<meta http-equiv="refresh" content="0; url='+atlas+'">'
                      '<meta name="robots" content="noindex,follow">'
                      '<link rel="canonical" href="'+atlas+'">'
                      '<title>內科學習地圖已整合</title><link rel="stylesheet" href="styles.css"></head>'
                      '<body class="reader-page"><main style="max-width:42rem;margin:12vh auto;padding:2rem">'
                      '<h1>閱讀路線已整合到臨床知識地圖</h1>'
                      '<p>原有文章與歷屆題目仍保留。如未自動跳轉，請<a href="'+atlas+'">開啟臨床知識地圖</a>。</p>'
                      '</main></body></html>')
    (DIST/old_map).write_text(atlas_redirect, encoding="utf-8")
    (DIST/"index.html").write_text(render_home(PAGES), encoding="utf-8")
    # Searching full source text remains possible, but current integrated lessons are presented first.
    originals = {p["output"] for p in PAGES if p.get("kind") == "historical_original"}
    search_rows = sorted(rows, key=lambda row: row["url"] in originals)
    searchable=json.dumps(search_rows,ensure_ascii=False)
    (DIST/"site-index.json").write_text(searchable,encoding="utf-8")
    (DIST/"site-index.js").write_text("window.CLINICAL_INDEX = "+searchable+";",encoding="utf-8")
    (DIST/".nojekyll").touch()
    if any(p["output"] == "xiaoma-reading-dcm-integrated.html" for p in PAGES):
        import subprocess
        subprocess.run([sys.executable, str(BASE / "tools/fetch_dcm_figures.py"), str(DIST)], check=True)
    if any(page["output"] in {"xiaoma-reading-preexcited-af.html", "xiaoma-reading-wct-acls-decision.html"} for page in PAGES):
        # Download the licensed original ECGs during the build and publish
        # validated image bytes with the site, never as runtime CDN hotlinks.
        import subprocess
        subprocess.run([sys.executable, str(BASE / "tools/fetch_arrhythmia_figures.py"), str(DIST)], check=True)
    install_web_analytics()
    validate_output_links()
    for path in DIST.iterdir():
        print(path.name,path.stat().st_size)
if __name__=="__main__":main()
