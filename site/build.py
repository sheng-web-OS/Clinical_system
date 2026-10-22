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

BASE = Path(__file__).resolve().parents[1]
DIST = BASE / "dist"
PAGES = load_pages(BASE)
FILES = [(row["source"], row["output"], row["title"], row["subtitle"]) for row in PAGES]
class Renderer(mistune.HTMLRenderer):
    def __init__(self):
        super().__init__(escape=False)
        self.headings=[]
        self.h2=0
    def heading(self, text, level, **attrs):
        if level==2:
            self.h2+=1
            ident="part-"+str(self.h2)
            self.headings.append((ident,re.sub(r"<[^>]+>","",text)))
            return '<h2 id="'+ident+'">'+text+'</h2>'
        return '<h'+str(level)+'>'+text+'</h'+str(level)+'>'

OUTPUT_BY_SOURCE = {name: output for name, output, _, _ in FILES}

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

def render_reader(page, body, headings):
    """Reader-facing teaching, with routes and editorial records in separate pages."""
    is_lesson = bool(page.get("date")) or page["source"] == "content/tamponade.md"
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
    mode = "lesson-page" if is_lesson or page["source"] == "content/tamponade.md" else "directory-page"
    if not is_xiaoma:
        mode += " clinical-page"
    active = page["output"]
    references = page.get("references") or ("xiaoma-sources.html" if page.get("collection") == "xiaoma-internal-medicine" else None)
    reference_link = '<a href="'+html.escape(references,quote=True)+'">來源與延伸閱讀</a>' if references else ''
    lessons = sorted((row for row in PAGES if row.get("collection") == page.get("collection") and row.get("date")), key=lambda row: (row["date"], row["output"]))
    number = next((str(i).zfill(2) for i, row in enumerate(lessons, 1) if row["output"] == active), "")
    destinations = ([("index.html", "首頁"), ("knowledge-atlas.html", "知識脈絡"), ("xiaoma-reading.html", "小麻閱讀"), ("xiaoma-internal-medicine.html", "內科國考"), ("xiaoma-plan.html", "閱讀路線")]
                    if is_archive else
                    [("index.html", "首頁"), ("knowledge-atlas.html", "知識脈絡"), ("xiaoma-internal-medicine.html", "內科國考"), ("xiaoma-reading.html", "小麻閱讀"), ("xiaoma-plan.html", "閱讀路線")])
    top_links = ''.join('<a'+(' aria-current="page"' if active == dest else '')+' href="'+html.escape(dest,quote=True)+'">'+label+'</a>' for dest, label in destinations)
    brand = '<a class="reader-brand" href="index.html"><span class="brand-mark" aria-hidden="true">小</span>小麻閱讀<span>MEDICAL READING</span></a>'
    original_note = ('<aside class="original-reading-end"><a href="xiaoma-reading.html">← 回到小麻閱讀</a><p>本文保留 '+html.escape(page.get("date", "").replace("-", "."))+' 原稿。臨床處置請一併核對所附來源與現行指引。</p></aside>') if page.get("kind") == "historical_original" else ''
    return '''<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="'''+html.escape(page["title"]+' · '+page["subtitle"],quote=True)+'''">
<title>'''+title+' · '+site_name+'''</title><link rel="stylesheet" href="styles.css"></head><body class="reader-page '''+mode+'''">
<a class="skip-link" href="#reading-content">跳到正文</a><div class="floating" aria-hidden="true"></div>
<header class="reader-header">'''+brand+'''<nav aria-label="主要導覽">'''+top_links+'''</nav><details class="reader-search"><summary>搜尋</summary><div><label for="search">搜尋教材</label><input id="search" class="searchbox" type="search" placeholder="輸入主題或問題…"><div class="results" id="results" aria-live="polite"></div></div></details><div class="reader-tools"><button id="fontminus" aria-label="縮小字體">A−</button><button id="fontplus" aria-label="放大字體">A+</button><button id="theme" aria-label="切換明暗主題">◐</button></div></header>
<div class="reader-shell"><aside class="reader-rail"><a class="back-link" href="'''+home+'''">← 教材目錄</a><span class="rail-label">'''+('本篇脈絡' if is_lesson else '本頁導覽')+'''</span><nav class="reader-outline" aria-label="章節導覽">'''+outline+'''</nav><div class="rail-bottom"><a href="xiaoma-reading.html">以往小麻閱讀 ↗</a><a href="xiaoma-plan.html">完整閱讀路線 ↗</a><a href="index.html">其他臨床教材 ↗</a></div></aside>
<main class="reader-main" id="reading-content"><div class="reader-hero"><p class="reader-kicker">'''+section+('　 /　 '+number if is_lesson else '')+'''</p><h1>'''+title+'''</h1><p class="reader-deck">'''+subtitle+'''</p></div>
<details class="mobile-outline"><summary>本篇章節</summary><nav aria-label="行動版章節導覽">'''+outline+'''</nav></details>
<article class="article reading-prose">'''+body+'''</article>'''+original_note+'''<footer class="reader-footer"><a href="'''+home+'''">'''+site_name+'''</a><span>把問題想通，再往下一步。</span>'''+reference_link+'''</footer></main></div>
<script src="site-index.js"></script><script src="app.js" defer></script></body></html>'''

def render(md_file, output, page_title, subtitle):
    raw=(BASE/md_file).read_text(encoding="utf-8")
    current=next(row for row in PAGES if row["output"]==output)
    # Preserve the chat-supplied original bytes on disk; only suppress a
    # duplicate plain-text first-line title in the rendered HTML, as for # H1.
    if current.get("kind") == "historical_original":
        head, _, tail = raw.partition("\n")
        if head.strip() == current["title"] and tail:
            raw = tail.lstrip("\n")
    if "<!-- XIAOMA_READING_ORIGINALS -->" in raw:
        originals=sorted((row for row in PAGES if row.get("kind")=="historical_original" and row.get("collection")==current.get("collection")),key=lambda row:row["date"])
        cards='<div class="original-list">'+''.join(
            '<a class="original-card" href="'+html.escape(row["output"],quote=True)+'"><span class="original-date">'+html.escape(row["date"].replace("-","."))+' · 完整原稿</span><strong>'+html.escape(row["title"])+'</strong><span>'+html.escape(row["subtitle"])+'</span><span class="read-link">開始閱讀 <span aria-hidden="true">→</span></span></a>' for row in originals)+'</div>'
        raw=raw.replace("<!-- XIAOMA_READING_ORIGINALS -->",cards)
    if "<!-- XIAOMA_PUBLISHED_LESSONS -->" in raw:
        lessons = sorted((row for row in PAGES if row.get("collection") == "xiaoma-internal-medicine" and row.get("date")), key=lambda row: row["date"])
        # Links use output paths already, so the public list needs no source-file exposure.
        cards = '<div class="lesson-list">' + ''.join(
            '<a class="lesson-card" href="' + html.escape(row["output"], quote=True) + '"><span class="lesson-date">' + html.escape(row.get("section", "內科閱讀")) + '　 /　 ' + html.escape(row["date"]) + '</span><strong>' + html.escape(row["title"]) + '</strong><p>' + html.escape(row["subtitle"]) + '</p><span class="lesson-card-end">進入閱讀 <span aria-hidden="true">↗</span></span></a>'
            for row in lessons) + '</div>'
        raw = raw.replace("<!-- XIAOMA_PUBLISHED_LESSONS -->", cards)
    raw=re.sub(r'<!-- (U0[1-8]) -->',lambda m:'<a class="chapter-anchor" id="'+m.group(1).lower()+'"></a>',raw)
    rr=Renderer()
    parser=mistune.create_markdown(renderer=rr,plugins=["table","strikethrough","url"])
    body=parser(raw)
    body=re.sub(r"^<h1>[^<]*</h1>", "", body, count=1)  # accessible single H1 in page hero
    body=re.sub(r'<pre><code class="language-mermaid">([\s\S]*?)</code></pre>',render_mechanism,body)
    body=rewrite_internal_links(body,md_file)
    current=next(row for row in PAGES if row["output"]==output)
    website = render_reader(current, body, rr.headings)
    (DIST/output).write_text(website,encoding="utf-8")
    return {"title":page_title,"url":output,"text":re.sub(r"\s+"," ",re.sub(r"<[^>]*>"," ",body))[:60000]}
def main():
    if DIST.exists():shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for name in ("styles.css","home.css","app.js"):
        shutil.copyfile(BASE/"site"/name,DIST/name)
    rows=[render(*entry) for entry in FILES]
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
    (DIST/"index.html").write_text(render_home(PAGES), encoding="utf-8")
    searchable=json.dumps(rows,ensure_ascii=False)
    (DIST/"site-index.json").write_text(searchable,encoding="utf-8")
    (DIST/"site-index.js").write_text("window.CLINICAL_INDEX = "+searchable+";",encoding="utf-8")
    (DIST/".nojekyll").touch()
    if any(p["output"] == "xiaoma-reading-dcm-integrated.html" for p in PAGES):
        import subprocess
        subprocess.run([sys.executable, str(BASE / "tools/fetch_dcm_figures.py"), str(DIST)], check=True)
    validate_output_links()
    for path in DIST.iterdir():
        print(path.name,path.stat().st_size)
if __name__=="__main__":main()
