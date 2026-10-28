#!/usr/bin/env python3
"""Inspect an unpublished, temporary compiled pleural release candidate."""
import argparse
import functools
import hashlib
import http.server
import json
from pathlib import Path
import subprocess
import sys
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from catalog import load_pages
from exam_archive import archive_anchor, concept_url, question_key, question_records

PAGES = {
    "xiaoma-20261028-pleural-effusion-decision.html": ("56 歲", "piperacillin/tazobactam", "未報告", "7.42"),
    "xiaoma-pleural-effusion-decision-sources.html": ("BTS 2023 Appendix 1", "Pocket Medicine 9E", "112"),
    "xiaoma-exams.html": ("112", "114", "115"),
}
ARTICLE = "xiaoma-20261028-pleural-effusion-decision.html"
EXPECTED = {(112, 1, 2, "醫學（三）", 45),
            (114, 1, 2, "醫學（三）", 48),
            (115, 2, 2, "醫學（三）", 49)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    font = subprocess.check_output(["fc-match", "-f", "%{family}", "Noto Sans TC"], text=True)
    if "Noto Sans TC" not in font:
        raise AssertionError("Traditional Chinese font is unavailable")
    records = {question_key(r["exam"]): r for r in question_records(load_pages(ROOT))
               if r["page"]["output"] == ARTICLE}
    if set(records) != EXPECTED:
        raise AssertionError("Candidate must contain all three exact official question identities")
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0),
        functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(args.site.resolve())))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = "http://127.0.0.1:" + str(server.server_port) + "/"
    reports = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for name, tokens in PAGES.items():
                for width in (360, 375, 390, 1280):
                    for theme in ("light", "dark"):
                        page = browser.new_page(viewport={"width": width, "height": 860},
                                                color_scheme=theme,
                                                is_mobile=width < 400, has_touch=width < 400)
                        try:
                            page.route("**/*", lambda route: route.continue_()
                                       if route.request.url.startswith(origin) else route.abort())
                            response = page.goto(origin + name, wait_until="domcontentloaded")
                            if response.status != 200:
                                raise AssertionError("Candidate page is unavailable " + name)
                            page.evaluate("document.fonts.ready")
                            if theme == "dark":
                                page.locator("#theme").click()
                            # The exam hub uses a different layout; only reader
                            # headers carry reader-brand and its color transition.
                            page.wait_for_function("""() => {
                              const b = document.querySelector('.reader-brand');
                              return !b || getComputedStyle(b).color ===
                                getComputedStyle(document.body).color;
                            }""")
                            state = page.evaluate("""() => ({
                              width:document.documentElement.clientWidth,
                              scroll:document.documentElement.scrollWidth,
                              text:document.body.innerText,
                              dark:document.body.classList.contains('dark'),
                              links:[...document.querySelectorAll('a')].map(a => a.getAttribute('href')),
                              glyphs:document.fonts.check('16px "Noto Sans TC"', '胸水國考')
                            })""")
                            if state["scroll"] > state["width"] + 2:
                                raise AssertionError(f"{name} {width} global overflow")
                            if not all(t in state["text"] for t in tokens):
                                raise AssertionError(f"{name} missing source-backed evidence")
                            if state["dark"] != (theme == "dark") or not state["glyphs"]:
                                raise AssertionError(f"{name} theme/font state invalid")
                            if name == ARTICLE and "xiaoma-pleural-effusion-decision-sources.html" not in state["links"]:
                                raise AssertionError("Compiled article cannot navigate to its source page")
                            if name == ARTICLE and not all("xiaoma-exams.html#" + archive_anchor(r)
                                    in state["links"] for r in records.values()):
                                raise AssertionError("Article is missing an exact official exam return link")
                            if name == "xiaoma-pleural-effusion-decision-sources.html" and ARTICLE not in state["links"]:
                                raise AssertionError("Source page has no article return link")
                            if width == 375:
                                page.screenshot(path=str(args.output / f"{name}-{theme}-375.png"))
                            if name == "xiaoma-exams.html":
                                for key in sorted(EXPECTED):
                                    r = records[key]
                                    row = page.locator('[id="' + archive_anchor(r) + '"]')
                                    if row.count() != 1:
                                        raise AssertionError("Official question row missing or duplicated " + str(key))
                                    # The Q entry itself opens the canonical clinical
                                    # explanation. Its own article is not an extra "教材".
                                    href = r["page"]["output"] + "#" + r["anchor"]
                                    link = row.locator('a.exam-question-entry[href="' + href + '"]')
                                    if link.count() != 1:
                                        raise AssertionError("Official Q does not open its exact answer " + str(key))
                                    if row.locator("details.exam-catalog-materials").count():
                                        raise AssertionError("Own answer incorrectly repeated as 教材 " + str(key))
                                    bounds = row.bounding_box()
                                    if bounds["x"] < -2 or bounds["x"] + bounds["width"] > width + 2:
                                        raise AssertionError("Official question row is clipped " + str(key))
                                    if width == 375:
                                        page.screenshot(path=str(args.output / f"exam-{key[0]}-{key[1]}-q{key[4]}-{theme}-375.png"))
                                    link.click()
                                    page.wait_for_url(origin + href)
                                    fragment = href.split("#", 1)[1]
                                    if page.locator('[id="' + fragment + '"]').count() != 1:
                                        raise AssertionError("Official question answer target missing " + str(key))
                                    page.goto(origin + name, wait_until="domcontentloaded")
                            reports.append({"page":name,"width":width,"theme":theme,
                                            "page_width":state["scroll"],"source_and_links":True})
                        finally:
                            page.close()
        finally:
            browser.close()
            server.shutdown()
            server.server_close()
    report = {"mode":"PRIVATE_TEMPORARY_RELEASE_PREFLIGHT_NOT_DEPLOYMENT",
              "checks":reports,"failures":[],
              "official_exam_links":{"identities":[list(k) for k in sorted(EXPECTED)],
                  "bidirectional":True,"browser_clicks":24},
              "article_html_sha256":hashlib.sha256((args.site/ARTICLE).read_bytes()).hexdigest()}
    (args.output/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"checks":len(reports),"failures":[]}))


if __name__ == "__main__":
    main()

