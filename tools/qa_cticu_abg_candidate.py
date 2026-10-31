"""Private CTICU ABG reader visual preflight, NOT publication or independent clinical QA.

Renders the exact proposed Markdown and original SVG in a local CSS-backed reader
shell at mobile/desktop sizes. Does not touch site/pages.json or production.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import tempfile
from pathlib import Path

import mistune
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = [
    ("03", "2026-10-29-cticu-abg-03-cpb-acidbase.md",
     "cticu-abg-03-cpb-acidbase-group-trends.svg"),
    ("04", "2026-10-29-cticu-abg-04-alphastat-phstat.md",
     "cticu-abg-04-alpha-phstat-logic.svg"),
]
LESSONS = ROOT / "content/xiaoma-internal-medicine/lessons"
WIDTHS = (360, 375, 390, 1280)


def build_private_preview(folder: Path, label: str, mdname: str, svgname: str):
    article = (LESSONS / mdname).read_text(encoding="utf-8")
    svg = (LESSONS / svgname).read_text(encoding="utf-8")
    assert svg.strip().startswith("<svg ") and "<desc" in svg and "</svg>" in svg
    assert f'src="{svgname}"' in article
    assert "figcaption" in article
    parser = mistune.create_markdown(escape=False, plugins=["table", "strikethrough", "url"])
    body = parser(article)
    (folder / svgname).write_text(svg, encoding="utf-8")
    css = (ROOT / "site/styles.css").read_text(encoding="utf-8")
    (folder / "styles.css").write_text(css, encoding="utf-8")
    title = html.escape(article.splitlines()[0].lstrip("# "))
    source = folder / f"abg-{label}.html"
    source.write_text(f"""<!doctype html><html lang="zh-Hant"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{title} | Unpublished private QA</title><link rel="stylesheet" href="styles.css">
    <style>body.reader-page{{margin:0}}.reader-shell{{display:block;max-width:1100px;margin:auto}}
    .reader-main{{max-width:100%;min-width:0;margin:0 auto;padding:16px}}
    .reading-prose{{max-width:760px;margin:0 auto}}</style></head>
    <body class="reader-page"><div class="reader-shell"><main class="reader-main">
    <article class="article reading-prose">{body}</article></main></div></body></html>""",
                      encoding="utf-8")
    return source, folder / svgname


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--output", required=True)
    args = cli.parse_args()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix="cticu-abg-private-") as td:
        folder = Path(td)
        articles = [(*build_private_preview(folder, *entry), entry[0]) for entry in ASSETS]
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for doc, svg, label in articles:
                    for width in WIDTHS:
                        page = browser.new_page(viewport={"width": width, "height": 900},
                                                device_scale_factor=1)
                        page.goto(doc.as_uri(), wait_until="load", timeout=20000)
                        # Native loading="lazy" images below the fold do not load at
                        # document.readyState=complete. Emulate a reader scrolling.
                        page.screenshot(path=str(out / f"abg-{label}-{width}-intro.png"), full_page=False, timeout=15000)
                        page.locator("img").first.scroll_into_view_if_needed(timeout=12000)
                        page.wait_for_function(
                            "() => [...document.images].every(i => i.complete)",
                            timeout=10000)

                        measurements = page.evaluate("""() => ({
                            scrollWidth: document.documentElement.scrollWidth,
                            clientWidth: document.documentElement.clientWidth,
                            images: [...document.querySelectorAll('img')].map(x => ({
                                src: x.getAttribute("src"),
                                complete: x.complete,
                                naturalWidth: x.naturalWidth,
                                naturalHeight: x.naturalHeight,
                                width: x.getBoundingClientRect().width
                            }))
                        })""")
                        expected = [x for x in measurements["images"] if x["naturalWidth"] > 0]
                        ok = (measurements["scrollWidth"] <= measurements["clientWidth"] + 2
                              and len(expected) == len(measurements["images"])
                              and len(expected) > 0
                              and all(x["width"] <= width for x in expected))
                        page.screenshot(path=str(out / f"abg-{label}-{width}-chart-viewport.png"), full_page=False, timeout=15000)
                        page.locator("figure").first.screenshot(path=str(out / f"abg-{label}-{width}-figure.png"), timeout=15000)
                        if label in {"03", "04"}:
                            # Both long figures must offer a functioning, reader-initiated
                            # independently zoomable native SVG on narrow screens.
                            zoom_link = page.locator('figure a[href$=".svg"]')
                            zoom_ok = zoom_link.count() == 1
                            if zoom_ok:
                                with page.expect_popup(timeout=10000) as opened:
                                    zoom_link.click(timeout=10000)
                                zoom_page = opened.value
                                zoom_page.wait_for_load_state("load", timeout=10000)
                                zoom_ok = (zoom_page.url.endswith(svg.name)
                                           and zoom_page.locator("svg").count() == 1)
                                if zoom_ok:
                                    zoom_page.screenshot(
                                        path=str(out / f"abg-{label}-{width}-zoom-opened.png"),
                                        full_page=False, timeout=15000)
                                zoom_page.close()
                            ok = ok and zoom_ok
                            measurements["native_svg_zoom_link"] = "PASS" if zoom_ok else "FAIL"
                        results.append({"article": label, "viewport": width,
                                        "status": "PASS" if ok else "FAIL",
                                        **measurements})
                        page.close()
                    image_page = browser.new_page(viewport={"width": 390, "height": 1100})
                    image_page.goto(svg.as_uri(), wait_until="load", timeout=20000)
                    image_bounds = image_page.evaluate("""() => {
                        const svg = document.querySelector('svg');
                        const vb = svg.viewBox.baseVal;
                        return [...svg.querySelectorAll('text')].map(t => {
                            const b=t.getBBox();
                            return {text:t.textContent, left:b.x, right:b.x+b.width,
                                    top:b.y, bottom:b.y+b.height, svgWidth:vb.width,
                                    svgHeight:vb.height};
                        });
                    }""")
                    image_page.close()
                    outliers = [x for x in image_bounds
                                if x["left"] < -1 or x["right"] > x["svgWidth"] + 1
                                or x["top"] < -1 or x["bottom"] > x["svgHeight"] + 1]
                    results.append({"article": label, "scope": "native_svg_glyph_bounds",
                                    "status": "FAIL" if outliers else "PASS",
                                    "total_text_nodes": len(image_bounds),
                                    "overflow_text_nodes": outliers})
            finally:
                browser.close()
    (out / "report.json").write_text(json.dumps(results, ensure_ascii=False, indent=2),
                                     encoding="utf-8")
    failures = [x for x in results if x["status"] != "PASS"]
    for x in results:
        print(f"CTICU ABG {x['article']} {x.get('viewport', x.get('scope'))}: {x['status']}")
    # Build UNREVIEWED exact-source-blob packets for a genuinely distinct reviewer.
    # These are prerequisites for approval, never AI-written approval receipts.
    import subprocess
    import sys
    for label, mdname, _ in ASSETS:
        relative = f"content/xiaoma-internal-medicine/lessons/{mdname}"
        packet_process = subprocess.run(
            [sys.executable, "site/semantic_gate.py", "--packet", relative],
            cwd=ROOT, check=True, capture_output=True, text=True)
        packet = json.loads(packet_process.stdout)
        assert packet["reviewer_context"] == "UNREVIEWED"
        (out / f"abg-{label}-UNREVIEWED-epqc-packet.json").write_text(
            json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"CTICU ABG {label}: UNREVIEWED packet {len(packet['paragraphs'])} reading units")
    if failures:
        raise SystemExit(f"{len(failures)} CTICU visual preflight failures: {failures!r}")
    print("PASS: PRIVATE CSS-backed preflight only; NOT production or independent medical review")


if __name__ == "__main__":
    main()
