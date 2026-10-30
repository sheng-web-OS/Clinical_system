#!/usr/bin/env python3
"""ACS-specific Chromium structural/mobile smoke check (not medical approval).

Render the actual generated ACS lesson at 360/375/390 px and desktop,
check that the long-form main reading and six exam links remain available,
that no page-level horizontal scroll is required, and that core text is legible.
Store screenshots only in private GitHub Actions artifacts.
"""
import argparse
import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGE = "acs-reading.html"
EXAM_PAGES = (
    "xiaoma-exam-113-2-med3-acs-q6.html",
    "xiaoma-exam-114-2-med3-acs-q6-q9.html",
    "xiaoma-exam-115-2-med3-acs-q11-q13.html",
)
TERMS = ("de Winter", "Wellens", "2026", "troponin", "VSR", "reperfusion")


def verify(page, width):
    report = page.evaluate("""() => {
      const article = document.querySelector('article');
      const paragraphs = [...(article?.querySelectorAll('p') || [])];
      const fontSizes = paragraphs.map(p => parseFloat(getComputedStyle(p).fontSize))
          .filter(Number.isFinite);
      const h2 = [...(article?.querySelectorAll('h2') || [])];
      const links = [...(article?.querySelectorAll('a[href]') || [])]
          .map(a => a.getAttribute('href'));
      const table = article?.querySelector('table');
      // Catch missing Traditional Chinese fallback fonts: two different Hanzi
      // must not rasterize into the same generic missing-glyph box.
      const canvas = document.createElement('canvas');
      canvas.width = 90;
      canvas.height = 72;
      const ctx = canvas.getContext('2d');
      const fontFamily = getComputedStyle(article).fontFamily;
      function glyphPixels(c) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.font = '40px ' + fontFamily;
        ctx.textBaseline = 'top';
        ctx.fillStyle = '#000';
        ctx.fillText(c, 8, 8);
        return new Uint8ClampedArray(ctx.getImageData(0, 0, 90, 72).data);
      }
      const glyphA = glyphPixels('中');
      const glyphB = glyphPixels('醫');
      let glyphDifferences = 0;
      for (let i = 0; i < glyphA.length; i++) {
        if (glyphA[i] !== glyphB[i]) glyphDifferences++;
      }
      return {
        cjkGlyphRasterDifference: glyphDifferences,
        viewport: innerWidth,
        documentWidth: document.documentElement.scrollWidth,
        bodyWidth: document.body.scrollWidth,
        paragraphs: paragraphs.length,
        characters: article?.innerText.length || 0,
        headings: h2.map(el => ({id: el.id, text: el.innerText})),
        links,
        minFontPx: Math.min(...fontSizes),
        tableCount: article?.querySelectorAll('table').length || 0,
        tableWidth: table?.scrollWidth || 0,
        tableClientWidth: table?.clientWidth || 0,
        text: article?.innerText || '',
      };
    }""")
    issues = []
    if report["cjkGlyphRasterDifference"] < 100:
        issues.append("Traditional Chinese appears as identical missing-glyph tofu boxes")
    if report["documentWidth"] > width + 3 or report["bodyWidth"] > width + 3:
        issues.append("document extends past the viewport")
    if report["characters"] < 5000 or report["paragraphs"] < 24:
        issues.append("deep ACS reader content is missing or truncated")
    if len(report["headings"]) < 12:
        issues.append("ACS reasoning sections are missing")
    for i, heading in enumerate(report["headings"], 1):
        if heading["id"] != f"part-{i}":
            issues.append("incorrect H2 navigation anchor: " + str(i))
    if width <= 390 and report["minFontPx"] < 14:
        issues.append("main paragraph text below 14px")
    if report["tableCount"] and report["tableWidth"] > report["tableClientWidth"] + 3:
        issues.append("ACS examination table requires horizontal scrolling")
    for term in TERMS:
        if term not in report["text"]:
            issues.append("critical reasoning content absent: " + term)
    for path in EXAM_PAGES:
        if not any(path in href for href in report["links"]):
            issues.append("missing exam link to " + path)
    report.pop("text")
    report.pop("links")
    return {"width": width, "passed": not issues, "issues": issues, "dom": report}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    parser.add_argument("--output", type=Path, default=ROOT / "visual-qa-artifacts" / "acs")
    parser.add_argument("--widths", nargs="+", type=int, default=[360, 375, 390, 1280])
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if not (args.dist / PAGE).is_file():
        parser.error("Missing built ACS page: " + PAGE)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(args.dist))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:" + str(server.server_port)
    reports = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                for width in args.widths:
                    context = browser.new_context(viewport={"width": width, "height": 820})
                    page = context.new_page()
                    page.goto(base + "/" + PAGE, wait_until="networkidle", timeout=30000)
                    page.screenshot(path=str(args.output / f"acs-first-screen-{width}.png"))
                    headings = page.locator("article h2")
                    if headings.count() >= 11:
                        headings.nth(10).scroll_into_view_if_needed()
                        page.screenshot(path=str(args.output / f"acs-exams-{width}.png"))
                    result = verify(page, width)
                    reports.append(result)
                    print(("PASS" if result["passed"] else "FAIL"), width, result["issues"])
                    context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    success = all(row["passed"] for row in reports)
    (args.output / "report.json").write_text(json.dumps({
        "scope": "ACS reader Chromium structural/mobile QA only",
        "status": "pass" if success else "fail",
        "medical_approval": False,
        "readability_user_study": False,
        "screenshots_human_reviewed": False,
        "results": reports,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
