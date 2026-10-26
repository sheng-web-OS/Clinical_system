#!/usr/bin/env python3
"""Render actual published teaching figures at real viewport widths.

Run after 'bash tools/build_site.sh' with Playwright Chromium installed.
Failures are screenshot-and-DOM observations, not an AI readability score.
Artifacts are for human/medical review; passing does not certify pedagogy.
"""
import argparse
import functools
import http.server
import json
import re
import subprocess
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "wpw": ("xiaoma-reading-wpw-conduction-mechanism.html", ["wpw-pathway-figure"]),
    "preexcited-af": ("xiaoma-reading-preexcited-af.html", ["af-ecg-evidence", "af-two-exits"]),
    "wct": ("xiaoma-reading-wct-acls-decision.html", ["wct-decision-figure"]),
}


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


FIGURE_BLOCK = re.compile(r"<figure\\b[^>]*>[\\s\\S]*?</figure>", re.IGNORECASE)


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
    """Render only added/edited figure elements, not unchanged figures in revised prose.

    Catalog edits are conservatively audited across all published figures.
    Missing prior source files trigger a full scan of the new article.
    """
    selected = discover_pages(root) if page_map is None else page_map
    visible_pages = changed_pages(root, base_ref, selected)
    if not visible_pages:
        return {}
    changed_names = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR",
         base_ref + "...HEAD", "--"], cwd=root, capture_output=True,
        text=True, check=True).stdout.splitlines()
    if "site/pages.json" in changed_names:
        return {name: selected[name] for name in visible_pages}
    catalog = json.loads((root / "site/pages.json").read_text(encoding="utf-8"))
    source_by_slug = {Path(row["output"]).stem: row["source"] for row in catalog}
    result = {}
    for slug in visible_pages:
        source = source_by_slug[slug]
        current = figure_versions((root / source).read_text(encoding="utf-8"))
        old = subprocess.run(["git", "show", base_ref + ":" + source],
                             cwd=root, capture_output=True, text=True)
        previous = figure_versions(old.stdout) if old.returncode == 0 else {}
        selected_ids = [fid for fid, html in current.items()
                        if previous.get(fid) != html]
        if selected_ids:
            result[slug] = (selected[slug][0], selected_ids)
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
        elif info["displayWidth"] < 180 and figure_id == "wpw-pathway-figure":
            problems.append("too-small source image on current viewport")
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
    if figure_id == "af-two-exits":
        if figure.locator("svg[width]").count():
            problems.append("AF causal figure reverted to fixed-width SVG")
        if figure.locator(".af-causal-path").count() != 2:
            problems.append("missing the two competing conduction pathways")
        if figure.locator(".af-causal-counterfactual").count() != 1:
            problems.append("missing counterfactual AV-node blockade consequence")
    if figure_id == "wpw-pathway-figure" and width <= 650:
        focus = figure.locator(".wpw-mobile-focus .wpw-focus-case")
        if focus.count() != 3 or not all(case.is_visible() for case in focus.all()):
            problems.append("all three activation states must be individually visible on phone")
        for crop in figure.locator(".wpw-crop").all():
            if not crop.is_visible():
                problems.append("source image panel hidden")
                continue
            rect = crop.bounding_box()
            if rect and rect["width"] < 220:
                problems.append("source image crop narrower than 220px")
    figure.scroll_into_view_if_needed()
    image_path = result_dir / (slug + "-" + figure_id + "-" + str(width) + ".png")
    try:
        figure.screenshot(path=str(image_path),timeout=20000)
    except Exception as exc:
        problems.append("screenshot failed: " + str(exc)[:160])
    return {"figure": figure_id, "passed": not problems, "problems": problems,
            "screenshot": image_path.name}


def run(dist, output, slugs, widths, page_map=None):
    # Local Playwright import keeps lightweight manifest-discovery tests dependency-free.
    from playwright.sync_api import sync_playwright
    page_map = PAGES if page_map is None else page_map
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
    for entry in reports:
        print(("PASS" if entry["passed"] else "HOLD"), entry["page"], entry["viewport"],
              entry["problems"] + [p for f in entry["figures"] for p in f["problems"]])
    return 0 if reports and all(e["passed"] for e in reports) else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", type=Path, default=ROOT / "dist")
    ap.add_argument("--output", type=Path, default=ROOT / "visual-qa-artifacts")
    ap.add_argument("--pages", nargs="+", default=None, help="Page slugs (default: focused arrhythmia set)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--all", action="store_true",
                      help="Discover all public <figure> blocks; expensive audit")
    mode.add_argument("--changed-from", default="",
                      help="Git base ref to auto-render only modified published articles")
    ap.add_argument("--widths", nargs="+", type=int, default=[360, 390, 768, 1280])
    a = ap.parse_args()
    page_map = discover_pages(ROOT) if a.all or a.changed_from else PAGES
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
        print("SKIP: no modified allowlisted pages containing figure blocks")
        raise SystemExit(0)
    raise SystemExit(run(a.dist, a.output, slugs, a.widths, page_map))
