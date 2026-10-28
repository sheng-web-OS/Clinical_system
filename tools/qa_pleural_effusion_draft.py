#!/usr/bin/env python3
"""Private PR188 reader QA, with no publication registration or medical approval."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "archive/xiaoma-internal-medicine/drafts/2026-10-28-pleural-effusion-decision.md"
TITLE = "胸水不是診斷：什麼時候該抽、抽出來又何時必須放胸管？"
PRIMARY = "https://assets.cureus.com/uploads/case_report/pdf/222237/20240126-32324-1eaex2m.pdf"


def render_private():
    import mistune
    sys.path.insert(0, str(ROOT / "site"))
    import build
    raw = (ROOT / SOURCE).read_text(encoding="utf-8")
    renderer = build.Renderer()
    parser = mistune.create_markdown(renderer=renderer,
                                     plugins=["table", "strikethrough", "url"])
    body = re.sub(r"^<h1>.*?</h1>", "", parser(raw), count=1, flags=re.S)
    body = build.rewrite_internal_links(body, SOURCE)
    # A temporary reader row selects the real lesson layout; it is never saved
    # in site/pages.json, dist, a release receipt, or a public route.
    row = {
        "source": "content/xiaoma-internal-medicine/lessons/2026-10-28-pleural-effusion-decision.md",
        "output": "private-pleural-effusion-preview.html",
        "title": TITLE, "subtitle": "真實病例的症狀、胸膜空間與兩次取樣",
        "collection": "xiaoma-internal-medicine", "layout": "reader",
        "section": "胸腔內科", "date": "2026-10-28", "navigation": False,
        "references": PRIMARY,
    }
    document = build.render_reader(row, body, renderer.headings)
    css_tag = '<link rel="stylesheet" href="styles.css">'
    if document.count(css_tag) != 1:
        raise AssertionError("Canonical reader stylesheet link changed")
    document = document.replace(css_tag, "<style>" +
                                (ROOT / "site/styles.css").read_text(encoding="utf-8") +
                                "</style>", 1)
    return raw, document


def main():
    from playwright.sync_api import sync_playwright
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    raw, document = render_private()
    app_script = (ROOT / "site/app.js").read_text(encoding="utf-8")
    (args.output / "private-reader.html").write_text(document, encoding="utf-8")
    failures, findings = [], []
    with sync_playwright() as driver:
        browser = driver.chromium.launch(headless=True)
        try:
            for width in (360, 375, 390, 1280):
                for theme in ("light", "dark"):
                    page = browser.new_page(viewport={"width": width, "height": 860},
                                            device_scale_factor=1,
                                            is_mobile=width < 400, has_touch=width < 400,
                                            color_scheme=theme)
                    try:
                        page.route("**/*", lambda route: route.abort())
                        page.set_content(document, wait_until="domcontentloaded")
                        page.locator("article.article").wait_for()
                        page.add_script_tag(content=app_script)
                        if theme == "dark":
                            page.locator("#theme").click()
                        observed = page.evaluate("""() => {
                          const article = document.querySelector('article.article');
                          const svg = document.querySelector('#pleural-case-evidence svg');
                          return {
                            viewport: document.documentElement.clientWidth,
                            darkThemeApplied: document.body.classList.contains('dark'),
                            pageWidth: document.documentElement.scrollWidth,
                            title: document.querySelector('h1')?.innerText,
                            headingCount: document.querySelectorAll('h1').length,
                            text: article.innerText,
                            tableCount: article.querySelectorAll('table').length,
                            sourceLink: [...article.querySelectorAll('a')].some(a =>
                              a.href.includes('10.7759') || a.href.includes('222237/')),
                            officialLinks: [...article.querySelectorAll('a')].filter(a =>
                              a.href.includes('wwwq.moex.gov.tw')).length,
                            figureWidth: svg?.getBoundingClientRect().width || 0,
                            minFigureFont: svg ? Math.min(...[...svg.querySelectorAll('text')].map(t =>
                              parseFloat(getComputedStyle(t).fontSize) *
                              svg.getBoundingClientRect().width / svg.viewBox.baseVal.width)) : 0,
                            minProseFont: Math.min(...[...article.querySelectorAll(':scope > p')].map(p =>
                              parseFloat(getComputedStyle(p).fontSize))),
                            fontReady: document.fonts.check('16px "Noto Sans TC"', '胸膜腔檢體')
                          };
                        }""")
                        observed.update(width=width, theme=theme)
                        text = observed.pop("text")
                        required = ("56 歲", "Day 3", "Day 5", "未報告", "7.42", "Figure 2B", "獨立假想反事實")
                        if any(token not in text for token in required):
                            failures.append(f"{width}/{theme}: source chronology missing")
                        if observed["darkThemeApplied"] != (theme == "dark"):
                            failures.append(f"{width}/{theme}: actual site theme not applied")
                        if observed["pageWidth"] > observed["viewport"] + 2:
                            failures.append(f"{width}/{theme}: global overflow")
                        if observed["title"] != TITLE or observed["headingCount"] != 1:
                            failures.append(f"{width}/{theme}: wrong title")
                        if observed["tableCount"] < 3 or not observed["sourceLink"] or observed["officialLinks"] < 9:
                            failures.append(f"{width}/{theme}: evidence tables/source/official links missing")
                        if observed["minFigureFont"] < 14 or observed["minProseFont"] < 16:
                            failures.append(f"{width}/{theme}: unreadable text")
                        if not observed["fontReady"]:
                            failures.append(f"{width}/{theme}: Traditional Chinese font unavailable")
                        if width == 375:
                            page.screenshot(path=str(args.output / f"reader-top-{theme}-375.png"))
                        page.locator("#pleural-case-evidence").screenshot(
                            path=str(args.output / f"evidence-{theme}-{width}.png"))
                        findings.append(observed)
                    finally:
                        page.close()
        finally:
            browser.close()
    report = {
        "mode": "PRIVATE_DRAFT_NOT_PUBLICATION_NOT_MEDICAL_APPROVAL",
        "source": SOURCE,
        "source_sha256": hashlib.sha256(raw.encode()).hexdigest(),
        "findings": findings, "failures": failures,
        "scope": "Real reader renderer/CSS; no analytics, network, public manifest or production QA."
    }
    (args.output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                           encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    if failures:
        raise SystemExit("Pleural private QA failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
