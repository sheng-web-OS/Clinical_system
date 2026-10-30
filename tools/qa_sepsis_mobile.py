#!/usr/bin/env python3
"""Visual smoke gate for the Sepsis release reader; not a medical QA verdict.

Serves locally built dist/ in private CI, captures three mobile widths, verifies
no page-level horizontal overflow, six exam anchors, and causal-map presence.
All screenshots remain in private GitHub Actions artifacts.
"""
import argparse
import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "clinical-sepsis-infection-to-shock.html",
    "xiaoma-exam-sepsis-112-114-five-questions.html",
    "clinical-sepsis-evidence.html",
)
QUESTION_ANCHORS = (
    "q-112-1-33", "q-112-1-64", "q-112-1-65",
    "q-113-1-48", "q-114-1-51", "q-114-1-57",
)


def verify(page, filename, width):
    issues = []
    dom = page.evaluate("""() => ({
        viewport: innerWidth,
        docWidth: document.documentElement.scrollWidth,
        bodyWidth: document.body.scrollWidth,
        title: document.title,
        mainText: (document.querySelector('article')?.innerText || '').length,
        mapCount: document.querySelectorAll('figure.causal-map').length,
        headings: document.querySelectorAll('article h2').length,
        tableCount: document.querySelectorAll('article table').length,
        cards: [...document.querySelectorAll('figure.causal-map')].map(fig => ({
          scrollWidth: fig.scrollWidth, visibleWidth: fig.clientWidth,
          cardCount: fig.querySelectorAll('.causal-card').length
        }))
    })""")
    if dom["docWidth"] > width + 3 or dom["bodyWidth"] > width + 3:
        issues.append("document overflows viewport horizontally")
    if dom["mainText"] < 450:
        issues.append("reader content is unexpectedly empty")
    if filename == PAGES[0]:
        if dom["mapCount"] < 2:
            issues.append("two causal explanations are missing")
        for idx, fig in enumerate(dom["cards"], 1):
            if fig["cardCount"] < 3:
                issues.append(f"causal-map {idx} missing mechanism nodes")
            if fig["scrollWidth"] > fig["visibleWidth"] + 3:
                issues.append(f"causal-map {idx} hides content horizontally")
        if page.locator('a[href*="xiaoma-exam-sepsis-112-114-five-questions.html"]').count() == 0:
            issues.append("lesson missing exam cross-link")
    elif filename == PAGES[1]:
        if page.locator('a[href*="clinical-sepsis-infection-to-shock.html"]').count() == 0:
            issues.append("exam reader missing lesson backlink")
        for key in QUESTION_ANCHORS:
            if page.locator("#" + key).count() != 1:
                issues.append("exam anchor missing/duplicate: " + key)
        if dom["headings"] < len(QUESTION_ANCHORS):
            issues.append("six question headings are not rendered")
    else:
        if page.locator('a[href*="10.1186/s12245-025-00958-5"]').count() == 0:
            issues.append("original case source figure link is absent")
    return {"page": filename, "width": width, "dom": dom, "passed": not issues,
            "issues": issues}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    parser.add_argument("--output", type=Path, default=ROOT / "visual-qa-artifacts" / "sepsis")
    parser.add_argument("--widths", nargs="+", type=int, default=[360, 375, 390])
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for name in PAGES:
        if not (args.dist / name).is_file():
            parser.error("Expected built page missing: " + name)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(args.dist))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = "http://127.0.0.1:" + str(server.server_port)
    results = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                for width in args.widths:
                    context = browser.new_context(viewport={"width": width, "height": 820},
                                                  device_scale_factor=1)
                    page = context.new_page()
                    for filename in PAGES:
                        page.goto(base + "/" + filename, wait_until="networkidle", timeout=30000)
                        page.screenshot(path=str(args.output / (filename.removesuffix(".html") + "-" + str(width) + ".png")))
                        result = verify(page, filename, width)
                        results.append(result)
                        print(("PASS" if result["passed"] else "FAIL"), filename, width,
                              "; ".join(result["issues"]))
                    context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    overall = all(r["passed"] for r in results)
    (args.output / "report.json").write_text(json.dumps({
        "scope": "Sepsis release structural/mobile rendering only",
        "medically_certified": False,
        "screenshots_human_viewed": False,
        "status": "pass" if overall else "fail",
        "results": results
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
