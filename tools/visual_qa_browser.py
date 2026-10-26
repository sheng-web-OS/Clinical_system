#!/usr/bin/env python3
"""Render changed public teaching figures in Chromium; retain legacy debt separately.

Run after 'bash tools/build_site.sh' with Playwright Chromium installed.
Failures are screenshot-and-DOM observations, not an AI readability score.
Artifacts are for human/medical review; passing does not certify pedagogy.
"""
import argparse
import functools
import http.server
import json
import os
import re
import subprocess
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIGURE_OPEN = re.compile(r"<figure\b([^>]*)>", re.IGNORECASE)
FIGURE_ID = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""", re.IGNORECASE)


def discover_pages(root: Path) -> dict:
    """Read the public allowlist, finding figure ids without a hand-maintained page map.

    A figure lacking an id is not silently skipped: fix the figure source first.
    This is structural discovery only, not medical or visual approval.
    """
    catalog = json.loads((root / "site/pages.json").read_text(encoding="utf-8"))
    pages = {}
    for entry in catalog:
        source = entry["source"]
        body = (root / source).read_text(encoding="utf-8")
        ids = []
        for index, match in enumerate(FIGURE_OPEN.finditer(body), 1):
            found = FIGURE_ID.search(match.group(1))
            # Existing articles contain legacy unlabelled figures. Include them in
            # the screenshot inventory, but mark their QA as HOLD until corrected.
            name = found.group(1) if found else f"__unnamed_{index:02d}"
            if name in ids:
                raise ValueError("Visual QA duplicate figure id: " + source + "#" + name)
            ids.append(name)
        if ids:
            slug = Path(entry["output"]).stem
            if slug in pages:
                raise ValueError("Visual QA duplicate output slug: " + slug)
            pages[slug] = (entry["output"], ids)
    return pages


def changed_pages(root: Path, base_ref: str, page_map: dict | None = None) -> list[str]:
    """Limit PR visual rendering to changed PUBLIC teaching pages.

    Git errors must not become a false green zero-pages scan. Page CSS/build
    changes need a separate whole-site visual audit and are reported by CI.
    """
    if not re.fullmatch(r"[A-Za-z0-9_./-]+", base_ref) or ".." in base_ref:
        raise ValueError("Invalid git base ref for visual QA")
    selected = discover_pages(root) if page_map is None else page_map
    command = ["git", "diff", "--name-only", "--diff-filter=ACMR", base_ref + "...HEAD", "--"]
    result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=True)
    changes = set(result.stdout.splitlines())
    allowlist = json.loads((root / "site/pages.json").read_text(encoding="utf-8"))
    if "site/pages.json" in changes:
        # New entries may point at untouched files. Scan the whole public figure inventory.
        return sorted(selected)
    return sorted(Path(page["output"]).stem for page in allowlist
                  if page["source"] in changes and Path(page["output"]).stem in selected)


FIGURE_BLOCK = re.compile(r"<figure\b[^>]*>[\s\S]*?</figure>", re.IGNORECASE)


def figure_versions(body: str) -> dict[str, str]:
    """Return each figure's complete markup for narrow content-diff QA."""
    result = {}
    for index, match in enumerate(FIGURE_BLOCK.finditer(body), 1):
        opening_tag = match.group(0).split(">", 1)[0]
        found = FIGURE_ID.search(opening_tag)
        key = found.group(1) if found else f"__unnamed_{index:02d}"
        if key in result:
            raise ValueError("Visual QA duplicate figure id: " + key)
        result[key] = match.group(0)
    return result


def changed_figures(root: Path, base_ref: str, page_map: dict | None = None) -> dict:
    """Run blocking render tests on newly published or changed figure markup.

    Global layout/CSS regressions go to a separate, non-blocking full-site
    legacy-debt report; known historic failures must not make unrelated PRs red.
    """
    selected = discover_pages(root) if page_map is None else page_map
    changed_names = set(subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR",
         base_ref + "...HEAD", "--"], cwd=root, capture_output=True,
        text=True, check=True).stdout.splitlines())
    catalog_changed = "site/pages.json" in changed_names
    old_public = set()
    if catalog_changed:
        old = subprocess.run(["git", "show", base_ref + ":site/pages.json"],
                             cwd=root, capture_output=True, text=True)
        if old.returncode == 0:
            old_public = {(page["source"], page["output"])
                          for page in json.loads(old.stdout)}
    visible_pages = changed_pages(root, base_ref, selected)
    catalog = json.loads((root / "site/pages.json").read_text(encoding="utf-8"))
    source_by_slug = {Path(row["output"]).stem: row["source"] for row in catalog}
    assets = {Path(path).name for path in changed_names
              if Path(path).suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}}
    result = {}
    for slug, (page_path, _) in selected.items():
        source = source_by_slug[slug]
        current = figure_versions((root / source).read_text(encoding="utf-8"))
        selected_ids = set()
        if catalog_changed and (source, page_path) not in old_public:
            selected_ids.update(current)
        if assets:
            for fid, html in current.items():
                if any(name in html for name in assets):
                    selected_ids.add(fid)
        if slug in visible_pages and selected_ids != set(current):
            old = subprocess.run(["git", "show", base_ref + ":" + source],
                                 cwd=root, capture_output=True, text=True)
            previous = figure_versions(old.stdout) if old.returncode == 0 else {}
            selected_ids.update(fid for fid, html in current.items()
                                if previous.get(fid) != html)
        if selected_ids:
            result[slug] = (page_path, [fid for fid in current if fid in selected_ids])
    return result


def inspect(page, figure_id, result_dir, slug, width):
    if figure_id.startswith("__unnamed_"):
        # Index mirrors source-order <figure> tags within the rendered article.
        figure = page.locator("article figure").nth(int(figure_id.rsplit("_", 1)[1]) - 1)
        problems = ["figure has no stable id; legacy QA HOLD"]
    else:
        figure = page.locator("#" + figure_id)
        problems = []
    if figure.count() != 1:
        return {"figure": figure_id, "passed": False, "problems": ["figure missing or duplicated"]}
    figure.scroll_into_view_if_needed()
    for img in figure.locator("img").all():
        if not img.is_visible():
            continue
        img.scroll_into_view_if_needed()
        try:
            img.evaluate("(el) => el.decode()", timeout=13000)
        except Exception:
            pass
        info = img.evaluate("""el => ({
           src: el.currentSrc || el.src, complete:el.complete,
           naturalWidth:el.naturalWidth, displayWidth:el.getBoundingClientRect().width
        })""")
        if not info["naturalWidth"]:
            problems.append("image failed to load: " + info["src"][:180])
    # A figure with an off-screen SVG inside a horizontal scroll region is
    # not "responsive" just because the document itself fits the viewport.
    hidden_panels = figure.evaluate("""root => [...root.querySelectorAll('*')]
        .filter(el => {
            const style = getComputedStyle(el);
            return ['auto', 'scroll'].includes(style.overflowX)
              && el.scrollWidth > el.clientWidth + 3;
        }).length""")
    if hidden_panels:
        problems.append("figure hides important content behind horizontal scrolling")
    figure.scroll_into_view_if_needed()
    image_path = result_dir / (slug + "-" + figure_id + "-" + str(width) + ".png")
    try:
        figure.screenshot(path=str(image_path),timeout=20000)
    except Exception as exc:
        problems.append("screenshot failed: " + str(exc)[:160])
    return {"figure": figure_id, "passed": not problems, "problems": problems,
            "screenshot": image_path.name}


def write_review_summary(output: Path, reports: list[dict]) -> None:
    """Compact GitHub Actions summary, never a medical or pedagogic approval."""
    total = sum(len(entry.get("figures", [])) for entry in reports)
    failures = sum(not fig.get("passed") for entry in reports
                   for fig in entry.get("figures", []))
    lines = [
        "### Figure rendering QA — NOT medical/content approval",
        "",
        f"Captured figure/viewport pairs: **{total}**; rendering holds: **{failures}**.",
        "A visually loaded picture may still be medically misleading, unreadable, "
        "inappropriate for its paragraph, or used without sufficient rights.",
        "",
        "| Published page | Width | Figure | Render | Problems | Screenshot |",
        "|---|---:|---|---|---|---|",
    ]
    for entry in reports:
        page = entry.get("page", "unknown")
        width = entry.get("viewport", "?")
        for fig in entry.get("figures", []):
            msg = "; ".join(fig.get("problems", [])) or "—"
            shot = fig.get("screenshot", "—")
            lines.append(f"| {page} | {width}px | {fig.get('figure', '?')} | "
                         f"{'PASS' if fig.get('passed') else 'HOLD'} | {msg} | {shot} |")
        if not entry.get("figures"):
            msg = "; ".join(entry.get("problems", [])) or "No figures"
            lines.append(f"| {page} | {width}px | — | HOLD | {msg} | — |")
    if not reports:
        lines.append("| No changed public figures | — | — | SKIP | — | — |")
    content = "\n".join(lines) + "\n"
    (output / "visual-qa-summary.md").write_text(content, encoding="utf-8")
    gh_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if gh_summary:
        with Path(gh_summary).open("a", encoding="utf-8") as stream:
            stream.write(content + "\n")


def run(dist, output, slugs, widths, page_map=None):
    # Local Playwright import keeps lightweight manifest-discovery tests dependency-free.
    from playwright.sync_api import sync_playwright
    page_map = discover_pages(ROOT) if page_map is None else page_map
    output.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(dist))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    origin = "http://127.0.0.1:" + str(httpd.server_port)
    reports = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                for slug in slugs:
                    path, figures = page_map[slug]
                    for width in widths:
                        page = browser.new_page(viewport={"width": width, "height": 870},
                                                device_scale_factor=1,
                                                is_mobile=width <= 650, has_touch=width <= 650)
                        try:
                            page.goto(origin + "/" + path, wait_until="domcontentloaded", timeout=25000)
                            page.locator("article").first.wait_for(timeout=10000)
                            dims = page.evaluate("""() => ({
                             doc:document.documentElement.scrollWidth, viewport:window.innerWidth,
                             title:document.title
                            })""")
                            problems = []
                            if dims["doc"] > dims["viewport"] + 3:
                                problems.append("page overflows viewport: " + str(dims))
                            results = [inspect(page, fig, output, slug, width) for fig in figures]
                            reports.append({"page": path, "viewport": width,
                                            "passed": not problems and all(f["passed"] for f in results),
                                            "problems": problems, "figures": results})
                        except Exception as exc:
                            reports.append({"page": path, "viewport": width, "passed": False,
                                            "problems": [str(exc)[:300]], "figures": []})
                        finally:
                            page.close()
            finally:
                browser.close()
    finally:
        httpd.shutdown()
    (output / "visual-qa-report.json").write_text(
        json.dumps({
            "scope": "render_and_layout_only",
            "certifies_medical_correctness": False,
            "certifies_figure_educational_value": False,
            "results": reports,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    write_review_summary(output, reports)
    for entry in reports:
        print(("PASS" if entry["passed"] else "HOLD"), entry["page"], entry["viewport"],
              entry["problems"] + [p for f in entry["figures"] for p in f["problems"]])
    return 0 if reports and all(e["passed"] for e in reports) else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", type=Path, default=ROOT / "dist")
    ap.add_argument("--output", type=Path, default=ROOT / "visual-qa-artifacts")
    ap.add_argument("--pages", nargs="+", default=None, help="Published output stems to render")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--all", action="store_true",
                      help="Discover all public <figure> blocks; expensive audit")
    mode.add_argument("--changed-from", default="",
                      help="Git base ref to auto-render only modified published articles")
    ap.add_argument("--widths", nargs="+", type=int, default=[360, 390, 768, 1280])
    a = ap.parse_args()
    page_map = discover_pages(ROOT)
    if a.pages is not None:
        slugs = a.pages
    elif a.changed_from:
        page_map = changed_figures(ROOT, a.changed_from, page_map)
        slugs = list(page_map)
    else:
        slugs = list(page_map)
    unknown = sorted(set(slugs) - set(page_map))
    if unknown:
        ap.error("Unknown page slug(s): " + ", ".join(unknown))
    if not slugs:
        a.output.mkdir(parents=True, exist_ok=True)
        (a.output / "visual-qa-report.json").write_text(
            json.dumps({"scope": "render_and_layout_only",
                        "certifies_medical_correctness": False,
                        "certifies_figure_educational_value": False,
                        "results": [], "status": "no_changed_public_figures"},
                       ensure_ascii=False, indent=2), encoding="utf-8")
        write_review_summary(a.output, [])
        print("SKIP: no modified allowlisted pages containing figure blocks")
        raise SystemExit(0)
    raise SystemExit(run(a.dist, a.output, slugs, a.widths, page_map))
