#!/usr/bin/env python3
"""Build a TEMPORARY Lab 02/03 candidate site and inspect exam links in Chromium.

No production manifest edit, publication, clinical approval, or semantic
review receipt. A successful run proves engineering navigation only.
"""
import argparse
import functools
import hashlib
import http.server
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
S02="content/xiaoma-internal-medicine/lessons/2026-10-27-lab-medicine-specimen-artifacts.md"
S03="content/xiaoma-internal-medicine/lessons/2026-10-27-lab-medicine-aki-creatinine-urine.md"
U02="xiaoma-lab-02-specimen-artifacts.html"
U03="xiaoma-lab-03-aki-creatinine.html"
H29="113 年第一次・醫學（三）Q29｜尿沉渣如何支持 intrinsic AKI？"
H28="115 年第二次・醫學（三）Q28｜治療後如何辨認恢復？"
H2="國考｜兩題其實在考兩個不同層次：定位病因，還是追蹤恢復？"
Q29=(113,1,2,"醫學（三）",29)
Q28=(115,2,2,"醫學（三）",28)
FILES=(S02,S03)

def add_candidates(worktree):
    manifest=worktree/"site/pages.json"
    pages=json.loads(manifest.read_text(encoding="utf-8"))
    outputs={p["output"] for p in pages}
    paths={p["source"] for p in pages}
    if any(x in outputs for x in (U02,U03)) or any(x in paths for x in FILES):
        raise AssertionError("Already published or duplicate Lab source/output; stop instead of overriding")
    from collections import Counter
    def exam_keys():
        for p in pages:
            for q in p.get("exam_questions",[]):
                yield tuple(q[k] for k in ("year_roc","sitting","stage","subject","question_number"))
            if p.get("exam"):
                a=p["exam"]
                for number in a["question_numbers"]:
                    yield a["year_roc"],a["sitting"],a["stage"],a["subject"],number
    ids=Counter(exam_keys())
    if ids[Q29]!=0 or ids[Q28]!=1:
        raise AssertionError("Canonical Moex 113-Q29/115-Q28 identities changed; review before candidate")
    source2=(worktree/S02).read_text("utf8")
    source3=(worktree/S03).read_text("utf8")
    title2=source2.splitlines()[0].removeprefix("# ")
    title3=source3.splitlines()[0].removeprefix("# ")
    if source2.splitlines()[0]!="# "+title2 or source3.splitlines()[0]!="# "+title3:
        raise AssertionError("Missing page H1")
    if source3.count("### "+H29)!=1 or source3.count("### "+H28)!=1 or source3.count("## "+H2)!=1:
        raise AssertionError("Exam anchor / concept not unique")
    pages.extend([
        {"source":S02,"output":U02,"title":title2,
         "subtitle":"三名真實患者：由兩種相反的溶血高鉀風險，走向抗凝管造成的計數失真",
         "collection":"xiaoma-internal-medicine","layout":"reader","section":"Lab Medicine",
         "date":"2026-10-29","navigation":False,"review":"author_source_check"},
        {"source":S03,"output":U03,"title":title3,
         "subtitle":"從陰性超音波到阻塞性 AKI，區分濾過數字、病因證據與追蹤終點",
         "collection":"xiaoma-internal-medicine","layout":"reader","section":"Lab Medicine",
         "date":"2026-10-29","navigation":False,"review":"author_source_check",
         "exam_questions":[
           {"year_roc":113,"sitting":1,"stage":2,"subject":"醫學（三）",
            "question_number":29,"question_heading":H29,
            "topic":"AKI 尿沉渣與 FENa 的證據定位",
            "focus":"granular casts 支持腎小管損傷，但不能排除 FENa 偏低的混合病因",
            "concept_heading":H2}
         ],
         "related_exams":[
           {"year_roc":115,"sitting":2,"stage":2,"subject":"醫學（三）",
            "question_number":28,"focus":"AKI 的動態追蹤與病因鑑別是不同問題",
            "concept_heading":H2,"question_heading":H28}
         ]}
    ])
    # Release requires a reader-facing source page and a real Figure/Table
    # cross-reference. Apply both only in this disposable worktree.
    pages.extend([
        {"source":"content/xiaoma-internal-medicine/lab-02-specimen-sources.md",
         "output":"xiaoma-lab-02-specimen-sources.html",
         "title":"Lab Medicine 02｜原始病例、圖表與檢驗方法",
         "subtitle":"原始患者數值、抗凝管 Figure 1 與採樣干擾條件",
         "collection":"xiaoma-internal-medicine","layout":"reader",
         "section":"Lab Medicine","date":"2026-10-29","navigation":False,
         "review":"author_source_check"},
        {"source":"content/xiaoma-internal-medicine/lab-03-aki-sources.md",
         "output":"xiaoma-lab-03-aki-sources.html",
         "title":"Lab Medicine 03｜AKI 真實病例、原始影像與國考來源",
         "subtitle":"Chen 原始 CT/US/Table、KDIGO 分期與正式國考來源",
         "collection":"xiaoma-internal-medicine","layout":"reader",
         "section":"Lab Medicine","date":"2026-10-29","navigation":False,
         "review":"author_source_check"}
    ])
    target=worktree/"audit/figure-gate.json"
    figures=json.loads(target.read_text(encoding="utf-8"))
    receipts=json.loads((worktree/"audit/lab-02-03-source-figure-candidate.json").read_text(encoding="utf-8"))
    if set(receipts)!={S02,S03} or any(s in figures["legacy_frozen"] or s in figures["reviews"] for s in receipts):
        raise AssertionError("Candidate Figure/Table receipts overlap existing reviews")
    figures["reviews"].update(receipts)
    target.write_text(json.dumps(figures,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    manifest.write_text(json.dumps(pages,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return pages

def check_pages(site, output, candidate_root):
    sys.path.insert(0,str(candidate_root/"site"))
    from catalog import load_pages
    from exam_archive import archive_anchor,question_key,question_records,question_anchor
    records={question_key(r["exam"]):r for r in question_records(load_pages(candidate_root))}
    if Q29 not in records or Q28 not in records:
        raise AssertionError("Two official exam identities not preserved")
    if records[Q29]["page"]["output"]!=U03 or records[Q28]["page"]["output"]==U03:
        raise AssertionError("Q29 must be newly canonical, Q28 must reuse pre-existing canonical answer")
    r29=records[Q29];r28=records[Q28]
    path29="xiaoma-exams.html#"+archive_anchor(r29)
    path28="xiaoma-exams.html#"+archive_anchor(r28)
    anchor29=question_anchor(r29["exam"])
    anchor28=question_anchor(r28["exam"])
    canonical28=r28["page"]["output"]+"#"+r28["anchor"]
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),
        functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(site)))
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    origin="http://127.0.0.1:"+str(server.server_port)+"/"
    samples=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
            for width in (360,375,390,1280):
                for theme in ("light","dark"):
                    page=browser.new_page(viewport={"width":width,"height":850},
                        is_mobile=width<400,has_touch=width<400,color_scheme=theme)
                    try:
                        page.route("**/*",lambda route: route.continue_()
                            if route.request.url.startswith(origin) else route.abort())
                        for name,tokens in (
                            (U02,("7.4","8.4","77","218")),
                            (U03,("375","558","618","122","FENa")),
                            ("xiaoma-exams.html",("113","115")),
                        ):
                            response=page.goto(origin+name,wait_until="domcontentloaded")
                            if response.status!=200:raise AssertionError(f"{width}/{theme}: {name} {response.status}")
                            page.evaluate("document.fonts.ready")
                            if theme=="dark" and name!="xiaoma-exams.html":
                                if not page.evaluate("document.body.classList.contains(\'dark\')"):
                                    page.locator("#theme").click()
                            state=page.evaluate("""() => ({
                                width:document.documentElement.clientWidth,
                                scroll:document.documentElement.scrollWidth,
                                text:document.body.innerText,
                                dark:document.body.classList.contains("dark"),
                                font:document.fonts.check('16px "Noto Sans TC"','腎臟血鉀'),
                                links:[...document.querySelectorAll('a')].map(a=>a.getAttribute('href'))
                            })""")
                            if state["width"]!=width or state["scroll"]>width+2:
                                raise AssertionError(f"{name}/{width}/{theme}: global overflow")
                            if not all(x in state["text"] for x in tokens):
                                raise AssertionError(f"{name}/{width}/{theme}: case text missing")
                            if not state["font"]:
                                raise AssertionError(f"{name}/{width}/{theme}: Traditional Chinese font missing")
                            if name in (U02,U03) and state["dark"]!=(theme=="dark"):
                                raise AssertionError(f"{name}/{width}/{theme}: theme broken")
                            if name==U03:
                                if not all(x in state["links"] for x in (path29,path28,canonical28)):
                                    raise AssertionError("AKI lesson missing question + original answer backlinks")
                                if page.locator(f'[id="{anchor29}"]').count()!=1 or page.locator(f'[id="{anchor28}"]').count()!=1:
                                    raise AssertionError("AKI official embedded/context H3 anchors missing")
                            if name=="xiaoma-exams.html":
                                for rec in (r29,r28):
                                    row=page.locator('[id="'+archive_anchor(rec)+'"]')
                                    if row.count()!=1:raise AssertionError("Official exam row duplicated/missing")
                                    expected=rec["page"]["output"]+"#"+rec["anchor"]
                                    if row.locator('a.exam-question-entry[href="'+expected+'"]').count()!=1:
                                        raise AssertionError("Official question answer link broken")
                                row28=page.locator('[id="'+archive_anchor(r28)+'"]')
                                if row28.locator('a[href="'+U03+'#part-9"]').count()!=1:
                                    # Avoid hardcoding H2 number; locate exact material path separately.
                                    if not any(h.startswith(U03+"#part-") for h in row28.locator("a").evaluate_all("(els)=>els.map(a=>a.getAttribute('href'))")):
                                        raise AssertionError("115 Q28 cannot navigate to AKI lesson")
                            if width==375:
                                page.screenshot(path=str(output/f"{name}-{theme}-375.png"))
                        # Actual navigations, not merely href presence.
                        page.goto(origin+path29,wait_until="domcontentloaded")
                        question=page.locator('[id="'+archive_anchor(r29)+'"] a.exam-question-entry')
                        question.click()
                        page.wait_for_url(origin+U03+"#"+anchor29)
                        if page.locator('[id="'+anchor29+'"]').count()!=1:
                            raise AssertionError("Q29 anchor absent at destination")
                        page.goto(origin+path28,wait_until="domcontentloaded")
                        row=page.locator('[id="'+archive_anchor(r28)+'"]')
                        # The catalog intentionally hides additional study materials
                        # inside a native <details>. Follow the actual reader UI.
                        row.locator("details.exam-catalog-materials > summary").click()
                        link=row.locator('a[href^="'+U03+'#part-"]').first
                        link.click()
                        if not page.url.startswith(origin+U03+"#part-"):
                            raise AssertionError("Q28 cross-article navigation failed")
                        samples.append({"width":width,"theme":theme,
                            "q29":"canonical_to_AKI","q28":"canonical_kept_and_AKI_material_link"})
                    finally:
                        page.close()
        finally:
            browser.close()
            server.shutdown()
            server.server_close()
    return samples

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    if any(x in {p.get("source") for p in json.loads((ROOT/"site/pages.json").read_text("utf8"))} for x in FILES):
        raise AssertionError("Candidate already registered in PR working tree; it must remain private")
    with tempfile.TemporaryDirectory(prefix="lab-release-preflight-") as td:
        work=Path(td)/"work"
        subprocess.run(["git","worktree","add","--detach",str(work),"HEAD"],
            check=True,cwd=ROOT,stdout=subprocess.PIPE)
        try:
            if (ROOT/".figure-cache").is_dir():
                shutil.copytree(ROOT/".figure-cache",work/".figure-cache",dirs_exist_ok=True)
            add_candidates(work)
            subprocess.run([sys.executable,"site/build.py"],cwd=work,check=True)
            subprocess.run([sys.executable,"tools/check_output.py"],cwd=work,check=True)
            samples=check_pages(work/"dist",args.output,work)
            # Generate UNREVIEWED exact-blob paragraph packets for a truly
            # separate clinical/editorial reviewer. This script NEVER signs off.
            sys.path.insert(0,str(ROOT/"site"))
            from semantic_gate import packet as semantic_packet
            reviewer_packets={}
            for number,source in (("02",S02),("03",S03)):
                review=semantic_packet(source,(ROOT/source).read_text(encoding="utf-8"))
                reviewer_packets[number]={"content_blob":review["content_blob"],
                    "paragraphs":len(review["paragraphs"]), "status":"UNREVIEWED"}
                (args.output/f"lab-{number}-unreviewed-review-packet.json").write_text(
                    json.dumps(review,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            report={"status":"PRIVATE_CANDIDATE_ENGINEERING_PASS_NOT_RELEASE_AUTHORIZATION",
                "samples":samples, "count":len(samples),
                "candidate_sources":list(FILES),
                "review_packets":reviewer_packets,
                "manifest_unmodified_in_PR":True,
                "independent_clinical_review":False,
                "independent_epqc_review":False,
                "rights_review":False,
                "production_deployment":False,
                "note":"Temporary detached worktree only; no original site/pages.json edit."}
            (args.output/"report.json").write_text(
                json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
            print(json.dumps({"status":report["status"],"samples":len(samples)},ensure_ascii=False))
        finally:
            subprocess.run(["git","worktree","remove","--force",str(work)],cwd=ROOT,check=True)

if __name__=="__main__":main()
