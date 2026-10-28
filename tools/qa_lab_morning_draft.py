#!/usr/bin/env python3
"""Private prepublication mobile QA of the actual Clinical_system reader renderer.

This script deliberately does NOT add a page to site/pages.json and does NOT
claim editorial/medical approval. It renders the unapproved Markdown through
site/build.py:Renderer and render_reader, using the actual site stylesheet,
then saves screenshots in a private GitHub Actions artifact.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import mistune
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
import build  # noqa: E402

SOURCE = "content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md"
TITLE = "早晨一張 Lab sheet：從真實病例與原始研究，判斷數字究竟能告訴我們什麼"
FIGURE = "#lab-three-clocks"


def render_private_draft():
    source = (ROOT / SOURCE).read_text(encoding="utf-8")
    rr = build.Renderer()
    parser = mistune.create_markdown(renderer=rr,
                                     plugins=["table", "strikethrough", "url"])
    body = parser(source)
    body = re.sub(r"^<h1>[^<]*</h1>", "", body, count=1)
    body = build.rewrite_internal_links(body, SOURCE)
    row = {
        "source": SOURCE,
        "output": "xiaoma-20261028-lab-morning-sheet.html",
        "title": TITLE,
        "subtitle": "真實 AML 檢體時序、急診重抽研究與腎功能推論的證據界線",
        "collection": "xiaoma-internal-medicine",
        "layout": "reader",
        "section": "Lab Medicine｜值班與病房",
        "date": "2026-10-28",
        "navigation": False,
        "references": "xiaoma-20261028-lab-morning-sheet-sources.html",
    }
    html = build.render_reader(row, body, rr.headings)
    style = (ROOT / "site/styles.css").read_text(encoding="utf-8")
    key = '<link rel="stylesheet" href="styles.css">'
    if html.count(key) != 1:
        raise AssertionError("Cannot locate canonical reader CSS link")
    html = html.replace(key, "<style>" + style + "</style>", 1)
    return html


def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("--output", type=Path,
                     default=ROOT / "visual-qa-artifacts" / "lab-morning-draft")
    args = arg.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    document = render_private_draft()
    findings = []
    failures = []
    with sync_playwright() as driver:
        browser = driver.chromium.launch(headless=True)
        try:
            for width in (360, 375, 390, 1280):
                page = browser.new_page(
                    viewport={"width": width, "height": 860},
                    device_scale_factor=1,
                    is_mobile=width <= 390, has_touch=width <= 390)
                try:
                    page.set_content(document, wait_until="domcontentloaded")
                    page.locator("article.article").wait_for()
                    figure = page.locator(FIGURE)
                    if figure.count() != 1:
                        raise AssertionError("Exactly one evidence-comparison figure required")
                    # Check actual original-case chronology and the independent evidence groups.
                    rows = page.locator("article.article table")
                    if rows.count() < 2:
                        raise AssertionError("Expected real AML sample-method table and cross-panel evidence table")
                    # This is source-based AML evidence, not the old synthetic four-timepoint panel.
                    required_panel_cues = ("20:03", "20:48", "23:37", "6.7", "7.8", "3.6")
                    numeric_tables = [rows.nth(k).inner_text()
                                      for k in range(rows.count())]
                    if not any(all(cue in table for cue in required_panel_cues)
                               for table in numeric_tables):
                        raise AssertionError("Missing published AML Table 1 method-and-treatment chronology")
                    arms = figure.locator("div[style*='border:1px']")
                    if arms.count() != 3:
                        raise AssertionError("Expected three distinct published evidence-source units")
                    figure_text = figure.inner_text()
                    if not all(cue in figure_text for cue in
                               ("AML 病例", "6.7", "7.8", "n=66", "3.9", "n=2,440", "864", "並非同一位病人")):
                        raise AssertionError("Evidence figure conflates case report and study denominators")
                    observed = page.evaluate("""() => ({
                      viewport: document.documentElement.clientWidth,
                      pageWidth: document.documentElement.scrollWidth,
                      title: document.querySelector('h1')?.innerText ?? '',
                      evidence: document.querySelector('#lab-three-clocks')?.innerText ?? '',
                      articleText: document.querySelector('article.article')?.innerText.length ?? 0,
                      tableOverflows: [...document.querySelectorAll('article.article table')].map(t =>
                        ({scrollWidth:t.scrollWidth,clientWidth:t.clientWidth})),
                      footerSource: [...document.querySelectorAll('footer a')].some(a =>
                        a.innerText.includes('來源') && a.getAttribute('href')?.includes('xiaoma-20261028-lab-morning-sheet-sources.html')),
                      fontCheckPassed: document.fonts.check('16px "Noto Sans TC"', '臨床抽血腎臟鉀')
                    })""")
                    observed["width"] = width
                    # Horizontal scrolling *inside* long lab tables is acceptable;
                    # horizontal overflow of the entire phone page is not.
                    if observed["pageWidth"] > observed["viewport"] + 2:
                        failures.append(f"{width}px global overflow: "
                                        f"{observed['pageWidth']}>{observed['viewport']}")
                    if observed["title"] != TITLE:
                        failures.append(f"{width}px incorrect public-facing title")
                    if (observed["articleText"] < 4000 or "K 6.3" not in observed["evidence"]
                            or "n=66" not in observed["evidence"]
                            or "n=2,440" not in observed["evidence"]):
                        failures.append(f"{width}px missing full case or figure evidence")
                    if not observed["footerSource"]:
                        failures.append(f"{width}px missing source navigation")
                    if not observed["fontCheckPassed"]:
                        failures.append(f"{width}px browser font readiness check failed")
                    # Capture true top-of-article BEFORE the figure locator scrolls.
                    if width == 375:
                        page.screenshot(path=str(args.output / "reading-top-375.png"))
                    figure.screenshot(path=str(args.output / f"evidence-figure-{width}.png"))
                    # A viewport capture is independently useful: Chromium can
                    # include off-viewport fixed skip links in element screenshots.
                    # Do not misdiagnose this as an actual in-viewport overlap.
                    if width == 375:
                        page.screenshot(path=str(args.output / "evidence-in-viewport-375.png"))
                    findings.append(observed)
                finally:
                    page.close()
        finally:
            browser.close()
    report = {"mode": "PRIVATE_DRAFT_RENDER_NOT_PUBLICATION",
              "source": SOURCE, "findings": findings, "failures": failures,
              "note": "Real reader renderer/CSS, not live Cloudflare, no medical or EPQC approval."}
    (args.output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    if failures:
        raise SystemExit("Lab Morning private reader QA failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
