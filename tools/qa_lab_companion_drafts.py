#!/usr/bin/env python3
"""PRIVATE draft browser QA for Lab 02/03; never registers or publishes pages.

Render each unpublished Markdown with the actual reader renderer and stylesheet,
then inspect real phone/desktop Chromium output. Layout QA is NOT a medical or
independent semantic review. No production site, tokens or patient records.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import mistune

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
import build  # noqa: E402

LESSONS = {
    "specimen": {
        "images": ["https://cdn.ncbi.nlm.nih.gov/pmc/blobs/835d/11947505/3ba234534955/cureus-0017-00000081211-i01.jpg"],
        "path": "content/xiaoma-internal-medicine/lessons/2026-10-27-lab-medicine-specimen-artifacts.md",
        "tokens": ("7.4", "8.4", "103", "77", "218", "血片", "競爭"),
        "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11947505/",
        "tables": 2,
    },
    "aki": {
        "images": ["https://cdn.ncbi.nlm.nih.gov/pmc/blobs/b3ab/12358086/fd38f5d2ea9a/cureus-0017-00000088144-i01.jpg","https://cdn.ncbi.nlm.nih.gov/pmc/blobs/b3ab/12358086/323897deafa2/cureus-0017-00000088144-i02.jpg","https://cdn.ncbi.nlm.nih.gov/pmc/blobs/b3ab/12358086/cc356ef900af/cureus-0017-00000088144-i03.jpg"],
        "path": "content/xiaoma-internal-medicine/lessons/2026-10-27-lab-medicine-aki-creatinine-urine.md",
        "tokens": ("375", "558", "618", "122", "6,170", "FENa", "hydronephrosis"),
        "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12358086/",
        "tables": 1,
    },
}


def private_render(slug, cfg):
    raw = (ROOT / cfg["path"]).read_text(encoding="utf-8")
    title_match = re.match(r"^# ([^\n]+)\n", raw)
    if not title_match:
        raise AssertionError(f"{slug}: missing single Markdown title")
    title = title_match.group(1)
    rr = build.Renderer()
    markdown = mistune.create_markdown(renderer=rr, plugins=["table", "strikethrough", "url"])
    rendered = markdown(build.compile_math(raw))
    if rendered.count("<h1>") != 1:
        raise AssertionError(f"{slug}: ambiguous H1")
    body = re.sub(r"^<h1>.*?</h1>\s*", "", rendered, count=1, flags=re.S)
    body = build.rewrite_internal_links(body, cfg["path"])
    row = {
        "source": cfg["path"],
        "output": f"private-lab-{slug}-preview.html",
        "title": title,
        "subtitle": "真實病例與檢驗測量的臨床推理｜私人未發布驗收",
        "collection": "xiaoma-internal-medicine",
        "layout": "reader",
        "section": "Lab Medicine",
        "date": "2026-10-29",
        "navigation": False,
        "references": cfg["source"],
    }
    document = build.render_reader(row, body, rr.headings)
    css_link = '<link rel="stylesheet" href="styles.css">'
    if document.count(css_link) != 1:
        raise AssertionError(f"{slug}: missing canonical stylesheet")
    document = document.replace(css_link, "<style>" +
        (ROOT / "site/styles.css").read_text(encoding="utf-8") + "</style>", 1)
    return raw, title, document


def main():
    from playwright.sync_api import sync_playwright
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    results, errors = [], []
    app_js = (ROOT / "site/app.js").read_text(encoding="utf-8")
    with sync_playwright() as driver:
        browser = driver.chromium.launch(headless=True)
        try:
            for slug, cfg in LESSONS.items():
                raw, title, document = private_render(slug, cfg)
                for width in (360, 375, 390, 1280):
                    for theme in ("light", "dark"):
                        page = browser.new_page(viewport={"width": width, "height": 860},
                            device_scale_factor=1, is_mobile=width <= 390,
                            has_touch=width <= 390, color_scheme=theme)
                        try:
                            # One real-network image proof per lesson: do not claim
                            # CC BY originals loaded from their source just because
                            # HTML, links or viewport dimensions exist.
                            verify_original_pixels = width == 375 and theme == "light"
                            allowed_images = set(cfg["images"]) if verify_original_pixels else set()
                            page.route("**/*", lambda route: (
                                route.continue_() if route.request.url in allowed_images
                                else route.abort()))
                            page.set_content(document, wait_until="domcontentloaded")
                            image_urls = page.locator("article.article figure img").evaluate_all(
                                "els => els.map(i => i.src)")
                            if image_urls != cfg["images"]:
                                raise AssertionError(f"{slug}: missing/reordered CC BY originals or wrong image URL")
                            if verify_original_pixels:
                                page.locator("article.article figure img").evaluate_all(
                                    "els => els.forEach(i => { i.loading = 'eager'; i.fetchPriority = 'high' })")
                                page.wait_for_function("""() =>
                                  [...document.querySelectorAll('article.article figure img')]
                                    .every(i => i.complete)""", timeout=30000)
                                broken = page.locator("article.article figure img").evaluate_all(
                                    "els => els.filter(i => i.naturalWidth < 100 || i.naturalHeight < 100).map(i => i.src)")
                                if broken:
                                    raise AssertionError(f"{slug}: original source image did not decode: {broken}")
                                page.locator("article.article figure img").first.scroll_into_view_if_needed()
                                page.screenshot(path=str(args.output / f"{slug}-original-figure-mobile-375.png"))
                            page.add_script_tag(content=app_js)
                            page.locator("article.article").wait_for()
                            if theme == "dark":
                                page.locator("#theme").click()
                            page.evaluate("document.fonts.ready")
                            data = page.evaluate("""() => {
                              const article=document.querySelector('article.article');
                              const tables=[...article.querySelectorAll('table')];
                              const h1=[...document.querySelectorAll('h1')];
                              const content=article.innerText;
                              const boxes=tables.map(t=>{
                                const b=t.getBoundingClientRect();
                                return {width:b.width, left:b.left, right:b.right,
                                  containerWidth:t.parentElement.getBoundingClientRect().width};
                              });
                              return {viewport:document.documentElement.clientWidth,
                                pageWidth:document.documentElement.scrollWidth,
                                title:h1[0]?.textContent || '', h1Count:h1.length,
                                articleText:content, tableCount:tables.length, tableBoxes:boxes,
                                hasSource:[...article.querySelectorAll('a')].some(a=>
                                  a.href.includes('pmc.ncbi.nlm.nih.gov/articles/PMC')),
                                dark:document.body.classList.contains('dark'),
                                font:document.fonts.check('16px "Noto Sans TC"', '繁體中文醫學'),
                                minimumParagraphFont:Math.min(...[...article.querySelectorAll('p')].
                                  map(p=>parseFloat(getComputedStyle(p).fontSize)))};
                            }""")
                            detail = {
                                "lesson":slug, "width":width, "theme":theme,
                                "viewport":data["viewport"], "pageWidth":data["pageWidth"],
                                "h1Count":data["h1Count"], "tableCount":data["tableCount"],
                                "fontReady":data["font"], "dark":data["dark"],
                                "articleSha256":hashlib.sha256(raw.encode()).hexdigest(),
                            }
                            results.append(detail)
                            if data["viewport"] != width or data["pageWidth"] > width + 2:
                                errors.append(f"{slug}/{width}/{theme}: horizontal overflow")
                            if data["title"] != title or data["h1Count"] != 1:
                                errors.append(f"{slug}/{width}/{theme}: incorrect heading")
                            if data["tableCount"] < cfg["tables"] or not data["hasSource"]:
                                errors.append(f"{slug}/{width}/{theme}: evidence table or source missing")
                            if any(t not in data["articleText"] for t in cfg["tokens"]):
                                errors.append(f"{slug}/{width}/{theme}: essential case detail missing")
                            if data["dark"] != (theme == "dark") or not data["font"]:
                                errors.append(f"{slug}/{width}/{theme}: theme or Chinese font missing")
                            if data["minimumParagraphFont"] < 15:
                                errors.append(f"{slug}/{width}/{theme}: prose font too small")
                            if width in (375, 1280):
                                page.screenshot(path=str(args.output / f"{slug}-{theme}-{width}-top.png"))
                                table = page.locator("article.article table").first
                                table.scroll_into_view_if_needed()
                                page.screenshot(path=str(args.output / f"{slug}-{theme}-{width}-table-viewport.png"))
                        except Exception as exc:
                            errors.append(f"{slug}/{width}/{theme}: {exc}")
                        finally:
                            page.close()
        finally:
            browser.close()
    report = {
        "mode": "PRIVATE_DRAFT_VISUAL_QA_NOT_PRODUCTION_OR_MEDICAL_APPROVAL",
        "tested": results, "failures": errors,
        "scope": "Real reader renderer/CSS, two unregistered Lab lesson drafts, responsive/typographic evidence only.",
        "original_images_tested": "real CDN source JPEG decode at 375px light; other layout modes block remote network",
        "independent_medical_review": False,
        "independent_semantic_review": False,
        "human_screenshot_review": False,
    }
    (args.output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"tested": len(results), "failures": errors}, ensure_ascii=False))
    if errors:
        raise SystemExit("Lab 02/03 draft browser QA failed")


if __name__ == "__main__":
    main()
