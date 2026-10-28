#!/usr/bin/env python3
"""Private Chromium release QA for U01; layout/link checks, NOT medical approval."""
import argparse
import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
LESSON = "xiaoma-20261028-urosepsis-esbl-first-dose.html"
SOURCES = "xiaoma-urosepsis-esbl-first-dose-sources.html"
EXAMS = "xiaoma-exams.html"
PAGES = (LESSON, SOURCES, EXAMS)
FIGURE_PDFS = (
    "clinical-question-1-figure-1.1.pdf",
    "clinical-question-1-table-1.1.pdf",
    "clinical-question-2-figure-1.2.pdf",
    "clinical-question-3-figure-1.3..pdf",
)


def verify(page, name, width):
    issues = []
    dom = page.evaluate("""() => ({
        vw: innerWidth,
        docw: document.documentElement.scrollWidth,
        bodyw: document.body.scrollWidth,
        mainText: (document.querySelector('article')?.innerText || '').length,
        headings: document.querySelectorAll('article h2').length,
        tables: document.querySelectorAll('article table').length,
        links: document.querySelectorAll('article a[href]').length,
        minFont: Math.min(...[...document.querySelectorAll('article p')].map(
            el => parseFloat(getComputedStyle(el).fontSize)).filter(Number.isFinite))
    })""")
    if dom["docw"] > width + 3 or dom["bodyw"] > width + 3:
        issues.append("page-level horizontal overflow")
    if dom["mainText"] < 350:
        issues.append("reader text unexpectedly empty")
    if name == LESSON:
        if dom["mainText"] < 7000 or dom["headings"] < 6:
            issues.append("full U01 clinical narrative not rendered")
        if dom["tables"] < 2:
            issues.append("risk/first-dose decision tables missing")
        if "合成病例" not in page.locator("article").inner_text():
            issues.append("synthetic-case disclosure missing")
        if "NOT VERIFIED" not in page.locator("article").inner_text():
            issues.append("order-ready dose boundary missing")
        if page.locator('a[href*="' + SOURCES + '"]').count() < 1:
            issues.append("lesson has no local source-review link")
        if page.locator('a[href*="' + EXAMS + '"]').count() < 1:
            issues.append("lesson has no reciprocal exam archive link")
        if dom["minFont"] < 15:
            issues.append("body paragraph font below 15px")
    elif name == SOURCES:
        for fragment in FIGURE_PDFS:
            if page.locator('a[href*="' + fragment + '"]').count() == 0:
                issues.append("missing original IDSA figure/table link: " + fragment)
        if page.locator('a[href*="111080"]').count() == 0:
            issues.append("official 111-2 Q60 source link missing")
    else:
        if page.locator('a[href*="' + LESSON + '"]').count() == 0:
            issues.append("exam-year archive lacks U01 Q60 article backlink")
    return {"page": name, "width": width, "dom": dom,
            "passed": not issues, "issues": issues}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    parser.add_argument("--output", type=Path, default=ROOT / "visual-qa-artifacts/u01")
    parser.add_argument("--widths", nargs="+", type=int, default=[360, 375, 390, 1280])
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for name in PAGES:
        if not (args.dist / name).is_file():
            parser.error("Expected registered U01 page missing: " + name)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(args.dist))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:" + str(server.server_port)
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                for width in args.widths:
                    context = browser.new_context(viewport={"width": width, "height": 820},
                                                  device_scale_factor=1)
                    page = context.new_page()
                    for name in PAGES:
                        page.goto(base + "/" + name, wait_until="networkidle", timeout=30000)
                        page.screenshot(path=str(args.output / (
                            name.removesuffix(".html") + "-" + str(width) + ".png")),
                            full_page=(width in (375, 1280) and name == LESSON))
                        result = verify(page, name, width)
                        results.append(result)
                        print(("PASS" if result["passed"] else "FAIL"), name, width,
                              "; ".join(result["issues"]))
                    context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    ok = all(r["passed"] for r in results)
    (args.output / "report.json").write_text(json.dumps({
        "scope": "U01 registered-reader layout, links, typography, and mobile overflow",
        "medical_review": False,
        "human_screenshot_review": False,
        "status": "pass" if ok else "fail",
        "results": results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
