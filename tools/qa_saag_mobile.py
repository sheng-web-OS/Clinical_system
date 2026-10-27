#!/usr/bin/env python3
"""Visual regression of the official SAAG comparison at mobile/desktop widths.

This checks rendered visibility and measured overflow, not clinical correctness.
"""
import argparse
import functools
import http.server
import json
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = "xiaoma-20261027-gi-liver-national-exam-trio.html"
VALUES = [
    ["A", "3.1", "2.1", "2.3", "1.0"],
    ["B", "4.3", "2.6", "3.0", "1.7"],
    ["C", "2.8", "2.0", "2.8", "0.8"],
    ["D", "2.8", "1.2", "2.0", "1.6"],
]
LABELS = ["血清 albumin", "腹水 albumin", "腹水 total protein", "SAAG（計算值）"]


def run(dist: Path, out: Path) -> int:
    from playwright.sync_api import sync_playwright
    out.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(dist))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    url = "http://127.0.0.1:" + str(httpd.server_port) + "/" + OUTPUT
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                for width in (320, 375, 390, 430, 1024):
                    page = browser.new_page(viewport={"width": width, "height": 844},
                                            device_scale_factor=1,
                                            is_mobile=width < 761, has_touch=width < 761)
                    problems = []
                    try:
                        page.goto(url, wait_until="domcontentloaded", timeout=25000)
                        table = page.locator("article.reading-prose > table")
                        if table.count() != 1:
                            raise ValueError("Expected one teaching table")
                        observed = page.evaluate("""() => {
                            const t = document.querySelector('article.reading-prose > table');
                            const rows = [...t.querySelectorAll('tbody tr')];
                            const cells = rows.map(tr => [...tr.querySelectorAll('td')].map(td => {
                                const rect = td.getBoundingClientRect();
                                return {value: td.textContent.trim(), left: rect.left,
                                    right: rect.right, label: getComputedStyle(td, '::before').content};
                            }));
                            return {bodyScroll: document.documentElement.scrollWidth, vw: innerWidth,
                                tableWidth: t.clientWidth, tableScroll: t.scrollWidth,
                                rowDisplay: getComputedStyle(rows[0]).display,
                                headVisible: getComputedStyle(t.querySelector('thead')).clipPath === 'none', cells,
                                sourceLink: !!document.querySelector('article a[href="xiaoma-exam-gi-liver-three-sources.html"]'),
                                metadataLeak: document.querySelector('main').innerText.includes('本篇來源與版本界線')
                                    || document.querySelector('main').innerText.includes('原始資料使用：考選部')};
                        }""")
                        if [[c["value"] for c in row] for row in observed["cells"]] != VALUES:
                            problems.append("Official source table or computed SAAG values changed")
                        if observed["bodyScroll"] > observed["vw"] + 2:
                            problems.append("Document overflows viewport")
                        if not observed["sourceLink"] or observed["metadataLeak"]:
                            problems.append("Evidence link missing or editorial metadata leaked")
                        if width < 761:
                            if observed["rowDisplay"] != "grid" or observed["headVisible"]:
                                problems.append("Mobile table did not switch to complete row cards")
                            if observed["tableScroll"] > observed["tableWidth"] + 2:
                                problems.append("Table requires horizontal scrolling")
                            if any(c["left"] < -1 or c["right"] > observed["vw"] + 1
                                   for row in observed["cells"] for c in row):
                                problems.append("One or more cells are clipped by phone width")
                            for row in observed["cells"]:
                                for i, label in enumerate(LABELS, 1):
                                    if label not in row[i]["label"]:
                                        problems.append("Missing visible mobile label: " + label)
                        elif observed["rowDisplay"] != "table-row" or not observed["headVisible"]:
                            problems.append("Desktop five-column table lost its visible header")
                        if width in (320, 390, 1024):
                            table.screenshot(path=str(out / f"saag-{width}px.png"))
                    except Exception as exc:
                        problems.append(str(exc)[:350])
                    finally:
                        page.close()
                    results.append({"width": width, "pass": not problems, "issues": problems})
            finally:
                browser.close()
    finally:
        httpd.shutdown()
    (out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf8")
    for item in results:
        print(("PASS" if item["pass"] else "HOLD"), "SAAG", item["width"], item["issues"])
    return 0 if all(r["pass"] for r in results) else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    parser.add_argument("--output", type=Path, default=ROOT / "visual-qa-artifacts/saag")
    args = parser.parse_args()
    raise SystemExit(run(args.dist, args.output))
