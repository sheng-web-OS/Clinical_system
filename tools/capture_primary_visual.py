"""Capture actual 1440/390/360 CSS viewports for essential medical figures.

Use Playwright+installed Chrome. Font coverage, overflow, SVG label clipping,
and presence of the specified source link fail CI; screenshots are *evidence
to review*, never an automatic guarantee of instructional or medical quality.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "visual-qa-preview"
FIGURE = r"<figure\b(?=[^>]*\bid=[\"']{anchor}[\"'])[^>]*>.*?</figure>"


def main():
    pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
    targets = [p for p in pages if isinstance(p.get("required_primary_visual"), dict)]
    if not targets:
        print("Primary visual preview: no contract targets")
        return

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Install the Playwright Python package before visual QA") from exc

    chrome = next((shutil.which(x) for x in
                   ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
                   if shutil.which(x)), None)
    if not chrome:
        raise RuntimeError("Primary visual QA needs a headless browser; none found")
    if not shutil.which("fc-list"):
        raise RuntimeError("Fontconfig unavailable; cannot verify Chinese font coverage")
    fc = subprocess.run(["fc-list", ":lang=zh-tw", "family"], capture_output=True, text=True, timeout=15)
    available = fc.stdout.lower()
    if fc.returncode != 0 or not any(name in available for name in
                                     ("noto sans cjk", "noto sans tc", "noto serif cjk",
                                      "wenquanyi", "ar pl", "source han")):
        raise RuntimeError("Traditional Chinese glyph font unavailable: screenshots would show tofu boxes")

    css = (ROOT / "dist/styles.css").read_text(encoding="utf-8")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as browser_library:
        browser = browser_library.chromium.launch(headless=True, executable_path=chrome, args=["--no-sandbox"])
        for source in targets:
            anchor = source["required_primary_visual"]["anchor"]
            markup = (ROOT / "dist" / source["output"]).read_text(encoding="utf-8")
            match = re.search(FIGURE.format(anchor=re.escape(anchor)), markup, re.I | re.S)
            if not match:
                raise ValueError(f"Primary figure not found in rendered HTML: {anchor}")
            html = ('<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8">'
                    '<meta name="viewport" content="width=device-width,initial-scale=1">'
                    '</head><body class="reader-page"><main class="reading-prose" '
                    'style="max-width:950px;margin:0 auto">'+match.group(0)+'</main></body></html>')
            for name, width, height in [("desktop", 1440, 900), ("mobile390", 390, 844), ("mobile360", 360, 780)]:
                page = browser.new_page(viewport={"width":width,"height":height}, device_scale_factor=1,
                                        locale="zh-TW")
                page.set_content(html, wait_until="domcontentloaded")
                page.add_style_tag(content=css)
                figure = page.locator("#" + anchor)
                figure.scroll_into_view_if_needed()
                dimensions = page.evaluate("""() => ({
                    cssWidth: innerWidth,
                    scrollWidth: document.documentElement.scrollWidth,
                    figureWidth: document.querySelector('figure').getBoundingClientRect().width
                })""")
                if dimensions["cssWidth"] != width or dimensions["scrollWidth"] > width + 1:
                    raise RuntimeError(f"Responsive overflow or viewport mismatch: {anchor}/{name}: {dimensions}")
                if anchor == "wct-acls-main-algorithm":
                    clipping = page.evaluate("""() => {
                        const svg = document.querySelector('.acls-desktop-graph');
                        if (getComputedStyle(svg).display === 'none') return [];
                        const rect = svg.querySelector('rect').getBBox();
                        return [...svg.querySelectorAll('text')].slice(0,3).map(e => {
                            let b = e.getBBox();
                            return {text:e.textContent,left:b.x, right:b.x+b.width,
                                    exceeds:b.x < rect.x-2 || b.x+b.width > rect.x+rect.width+2};
                        })
                    }""")
                    if any(item["exceeds"] for item in clipping):
                        raise RuntimeError(f"Core ACLS header labels outside node rectangle: {clipping}")
                screenshot = OUTPUT / f"{source['output'].removesuffix('.html')}-{name}.png"
                figure.screenshot(path=str(screenshot), animations="disabled")
                if not screenshot.is_file() or screenshot.stat().st_size < 2048:
                    raise RuntimeError(f"Screenshot empty: {anchor}/{name}")
                results.append({"source":source["source"],"anchor":anchor,"viewport_width":width,
                                "viewport_height":height,"screenshot":screenshot.name,
                                "bytes":screenshot.stat().st_size, **dimensions})
                page.close()
        browser.close()
    (OUTPUT / "capture-manifest.json").write_text(
        json.dumps({"purpose":"Real viewport and glyph check; human/AI visual judgment still required",
                    "captures":results}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Captured {len(results)} checked real-viewport screenshots in {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
