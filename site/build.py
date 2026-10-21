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

def render(md_file, output, page_title, subtitle):
    raw=(BASE/md_file).read_text(encoding="utf-8")
    current=next(row for row in PAGES if row["output"]==output)
    reading=current.get("layout", "").startswith("reading-")
    original=current.get("kind")=="historical_original"
    if "<!-- XIAOMA_READING_ORIGINALS -->" in raw:
        originals=sorted((row for row in PAGES if row.get("kind")=="historical_original" and row.get("collection")==current.get("collection")),key=lambda row:row["date"])
        cards='<div class="original-list">'+''.join(
            '<a class="original-card" href="'+html.escape(row["output"],quote=True)+'"><span class="original-date">'+html.escape(row["date"].replace("-","."))+' · 完整原稿</span><strong>'+html.escape(row["title"])+'</strong><span>'+html.escape(row["subtitle"])+'</span><span class="read-link">開始閱讀 <span aria-hidden="true">→</span></span></a>' for row in originals)+'</div>'
        raw=raw.replace("<!-- XIAOMA_READING_ORIGINALS -->",cards)
    if "<!-- XIAOMA_PUBLISHED_LESSONS -->" in raw:
        lessons = sorted((row for row in PAGES if row.get("collection") == "xiaoma-internal-medicine" and row.get("date")), key=lambda row: row["date"])
        # Links use output paths already, so the public list needs no source-file exposure.
        cards = '<div class="lesson-list">' + ''.join(
            '<a class="lesson-card" href="' + html.escape(row["output"], quote=True) + '"><span class="lesson-date">' + html.escape(row["date"]) + '</span><strong>' + html.escape(row["title"]) + '</strong><span>核心脈絡 · 必讀段落 · 國考題與解析 →</span></a>'
            for row in lessons) + '</div>'
        raw = raw.replace("<!-- XIAOMA_PUBLISHED_LESSONS -->", cards)
    raw=re.sub(r'<!-- (U0[1-8]) -->',lambda m:'<a class="chapter-anchor" id="'+m.group(1).lower()+'"></a>',raw)
    rr=Renderer()
    parser=mistune.create_markdown(renderer=rr,plugins=["table","strikethrough","url"])
    body=parser(raw)
    body=re.sub(r"^<h1>[^<]*</h1>", "", body, count=1)  # accessible single H1 in page hero
    body=re.sub(r'<pre><code class="language-mermaid">([\s\S]*?)</code></pre>',render_mechanism,body)
    body=rewrite_internal_links(body,md_file)
    toc=''.join('<a href="#'+ident+'">'+html.escape(txt)+'</a>' for ident,txt in rr.headings)
    header_stamp=html.escape(current.get("date", "Clinical System"))
    top_stamp="小麻閱讀" if reading else header_stamp+" · Medical education · Source-traceable"
    eyebrow="歷史閱讀文章" if original else ("閱讀・理解・再判斷" if reading else "Clinical reasoning / Evidence / Review")
    description=html.escape(subtitle)+("。" if reading else "。由版本化 Markdown 自動產生，原始資料與推論分離。")
    if original:
        toc_markup='<details class="reading-toc"><summary>閱讀段落 <span>'+str(len(rr.headings))+' 節</span></summary><div class="toclinks">'+toc+'</div></details>'
    elif reading:
        toc_markup=''
    else:
        toc_markup='<div class="toc"><strong>本頁章節</strong><div class="toclinks">'+toc+'</div></div>'
    end_note=('<div class="reading-end"><a href="xiaoma-reading.html">← 回到小麻閱讀</a><details><summary>原稿與本次收錄</summary><p>保留 '+html.escape(current.get("date","").replace("-","."))+' 完整稿。原文與本次編輯註記分開呈現；收錄不代表全篇已完成最新指引重審。</p><a href="xiaoma-reading-recovery.html">來源核對與編輯註記 →</a></details></div>') if original else ''
    nav=''.join('<a class="'+("active" if row["output"]==output or (row.get("collection") and row.get("collection")==current.get("collection")) else "")+'" href="'+row["output"]+'">'+html.escape(row["title"])+'</a>' for row in PAGES if row.get("navigation",True))
    website='''<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="'''+html.escape(page_title+' · '+subtitle,quote=True)+'''">
<title>'''+html.escape(page_title)+''' · Clinical Knowledge</title><link rel="stylesheet" href="styles.css"></head><body class="'''+('reading-layout' if reading else '')+'''">
<div class="floating"></div><div class="layout"><aside class="sidebar"><button class="mobile-menu" id="mobilemenu" aria-label="展開導覽">選單</button>
<a class="brand" href="index.html">CLINICAL / KNOWLEDGE<small>Master Prompt v5.1 · Evidence-Gated Publishing</small></a>
<label class="side-label" for="search">全文搜尋</label><input id="search" class="searchbox" type="search" placeholder="搜尋教材與審查…"><div class="results" id="results" aria-live="polite"></div>
<span class="side-label">學習與審查</span><nav class="menu">'''+nav+'''</nav>
<span class="side-label">正式來源</span><nav class="menu"><span class="private-source">內容來源：私人 GitHub</span><a href="https://doi.org/10.1093/eurheartj/ehaf192" target="_blank" rel="noopener">2025 ESC Guideline ↗</a></nav></aside>
<main class="main"><header class="top"><span>'''+top_stamp+'''</span>
<div class="tools"><button id="fontminus" aria-label="縮小字體">A−</button><button id="fontplus" aria-label="放大字體">A+</button><button id="theme">明暗切換</button></div></header>
<section class="page"><div class="hero"><span class="eyebrow">'''+eyebrow+'''</span><h1>'''+html.escape(page_title)+'''</h1><p class="lede">'''+description+'''</p></div>
'''+toc_markup+'''
<article class="article">'''+body+'''</article>'''+end_note+'''<footer>研究與專業學習用途。未經真人專科醫師審查；請依個別病人狀況與最新來源作臨床判斷。<br>Source of truth: GitHub / Markdown · No third-party analytics</footer></section></main></div><script src="site-index.js"></script><script src="app.js" defer></script></body></html>'''
    (DIST/output).write_text(website,encoding="utf-8")
    return {"title":page_title,"url":output,"text":re.sub(r"\s+"," ",re.sub(r"<[^>]*>"," ",body))[:60000]}
def main():
    if DIST.exists():shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for name in ("styles.css","app.js"):
        shutil.copyfile(BASE/"site"/name,DIST/name)
    rows=[render(*entry) for entry in FILES]
    searchable=json.dumps(rows,ensure_ascii=False)
    (DIST/"site-index.json").write_text(searchable,encoding="utf-8")
    (DIST/"site-index.js").write_text("window.CLINICAL_INDEX = "+searchable+";",encoding="utf-8")
    (DIST/".nojekyll").touch()
    validate_output_links()
    for path in DIST.iterdir():
        print(path.name,path.stat().st_size)
if __name__=="__main__":main()

