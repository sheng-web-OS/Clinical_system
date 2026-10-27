#!/usr/bin/env python3
"""Browser QA: 111 first sitting exam links actually open the right study section.

Visual/interaction QA only; does not certify answer accuracy or teaching depth.
"""
import argparse
import functools
import http.server
import json
import subprocess
from pathlib import Path
import sys
import threading

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from catalog import load_pages
from exam_archive import archive_anchor, concept_url, question_key, question_records

EXPECTED = [
    (111, 1, 2, "醫學（五）", 26),
    (111, 1, 2, "醫學（五）", 30),
    (111, 1, 2, "醫學（六）", 6),
    (111, 1, 2, "醫學（四）", 31),
    (111, 1, 2, "醫學（四）", 32),
    (111, 1, 2, "醫學（四）", 33),
]


def run(dist: Path, out: Path) -> int:
    from playwright.sync_api import sync_playwright

    # Headless layout passing with tofu glyphs is a false green. Confirm the
    # Linux runner has genuine Taiwan Traditional Chinese glyph coverage.
    font = subprocess.run(["fc-match", "-f", "%{family}", "Noto Sans TC"],
                          text=True, capture_output=True, check=True)
    if "Noto Sans TC" not in font.stdout:
        raise RuntimeError("HOLD: no readable Traditional Chinese font installed for phone screenshots")

    out.mkdir(parents=True, exist_ok=True)
    records = {question_key(record["exam"]): record for record in question_records(load_pages(ROOT))}
    missing = set(EXPECTED) - records.keys()
    if missing:
        raise ValueError("Missing published official questions: " + repr(missing))

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(dist))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = "http://127.0.0.1:" + str(server.server_port) + "/"
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                for width in (360, 375, 390, 1280):
                    page = browser.new_page(viewport={"width": width, "height": 844},
                                            device_scale_factor=1,
                                            is_mobile=width <= 390, has_touch=width <= 390)
                    problems = []
                    try:
                        page.goto(origin + "xiaoma-exams.html#year-111", wait_until="domcontentloaded", timeout=30000)
                        for k in EXPECTED:
                            record = records[k]
                            row = page.locator('[id="' + archive_anchor(record) + '"]')
                            if row.count() != 1:
                                problems.append("Question missing or duplicated: " + str(k))
                                continue
                            expected_href = concept_url(record["page"], record["embedded"], ROOT)
                            detail = row.locator("details.exam-catalog-materials")
                            if detail.count() != 1 or not detail.locator("summary").is_visible():
                                problems.append("Study-materials control missing: " + str(k))
                                continue
                            detail.locator("summary").click()
                            links = detail.locator("nav.exam-concept-links a")
                            hrefs = links.evaluate_all("(nodes) => nodes.map(n => n.getAttribute('href'))")
                            if expected_href not in hrefs:
                                problems.append("Wrong material link: " + str(k))
                                continue
                            bounds = row.evaluate("""el => {
                                const rect = el.getBoundingClientRect();
                                return {left:rect.left,right:rect.right,
                                    summaryText:el.querySelector('summary').innerText};
                            }""")
                            if bounds["left"] < -2 or bounds["right"] > width + 2:
                                problems.append("Clipped question row: " + str(k))
                            if "教材" not in bounds["summaryText"]:
                                problems.append("Materials label not visible: " + str(k))
                            dest = browser.new_page(viewport={"width": width, "height": 844},
                                                    is_mobile=width <= 390)
                            try:
                                dest.goto(origin + expected_href, wait_until="domcontentloaded", timeout=30000)
                                fragment = expected_href.split("#", 1)[1]
                                if dest.locator('[id="' + fragment + '"]').count() != 1:
                                    problems.append("Target section missing: " + str(k))
                            finally:
                                dest.close()
                        overflow = page.evaluate("document.documentElement.scrollWidth > innerWidth + 2")
                        if overflow:
                            problems.append("Year catalog has horizontal viewport overflow")
                        if width in (360, 390, 1280):
                            row = page.locator('[id="' + archive_anchor(records[EXPECTED[4]]) + '"]')
                            if row.count():
                                row.scroll_into_view_if_needed()
                                page.screenshot(path=str(out / ("year111-materials-" + str(width) + ".png")))
                    except Exception as exc:
                        problems.append(type(exc).__name__ + ": " + str(exc)[:350])
                    finally:
                        page.close()
                    results.append({"width": width, "passed": not problems, "issues": problems})
            finally:
                browser.close()
    finally:
        server.shutdown()
    (out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf8")
    for item in results:
        print("PASS" if item["passed"] else "HOLD", "111 first sitting exam materials", item)
    return 0 if all(item["passed"] for item in results) else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    parser.add_argument("--output", type=Path, default=ROOT / "visual-qa-artifacts/exam-year")
    args = parser.parse_args()
    raise SystemExit(run(args.dist, args.output))
