#!/usr/bin/env python3
"""Inspect an unpublished, temporary compiled pleural release candidate."""
import argparse
import hashlib
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGES = {
    "xiaoma-20261028-pleural-effusion-decision.html": ("56 歲", "piperacillin/tazobactam", "未報告", "7.42"),
    "xiaoma-pleural-effusion-decision-sources.html": ("BTS 2023 Appendix 1", "Pocket Medicine 9E", "112"),
    "xiaoma-exams.html": ("112", "114", "115"),
}
ARTICLE = "xiaoma-20261028-pleural-effusion-decision.html"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    css = (args.site / "styles.css").read_text()
    app = (args.site / "app.js").read_text()
    reports = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for name, tokens in PAGES.items():
                document = (args.site / name).read_text()
                tag = '<link rel="stylesheet" href="styles.css">'
                if document.count(tag) != 1:
                    raise AssertionError("Candidate stylesheet missing " + name)
                document = document.replace(tag, "<style>" + css + "</style>", 1)
                for width in (360, 375, 390, 1280):
                    for theme in ("light", "dark"):
                        page = browser.new_page(viewport={"width": width, "height": 860},
                                                color_scheme=theme,
                                                is_mobile=width < 400, has_touch=width < 400)
                        try:
                            page.route("**/*", lambda route: route.abort())
                            page.set_content(document, wait_until="domcontentloaded")
                            page.add_script_tag(content=app)
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
                            if name == "xiaoma-exams.html" and not any(
                                x and ARTICLE in x for x in state["links"]):
                                raise AssertionError("Exam archive has no backlink to candidate")
                            if width == 375:
                                page.screenshot(path=str(args.output / f"{name}-{theme}-375.png"))
                            reports.append({"page":name,"width":width,"theme":theme,
                                            "page_width":state["scroll"],"source_and_links":True})
                        finally:
                            page.close()
        finally:
            browser.close()
    report = {"mode":"PRIVATE_TEMPORARY_RELEASE_PREFLIGHT_NOT_DEPLOYMENT",
              "checks":reports,"failures":[],
              "article_html_sha256":hashlib.sha256((args.site/ARTICLE).read_bytes()).hexdigest()}
    (args.output/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"checks":len(reports),"failures":[]}))


if __name__ == "__main__":
    main()
