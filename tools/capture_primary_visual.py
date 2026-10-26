"""Capture documented primary teaching figures on 1440px and mobile 390/360px.

This captures *real Chrome-rendered previews* for reviewer inspection.
It does not independently judge medical meaning or declare visual QA passed.
Run after site/build.py generates dist/. Needs Google Chrome/Chromium.
"""
import html
import json
import os
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
    chrome = next((shutil.which(x) for x in
                   ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
                   if shutil.which(x)), None)
    if not chrome:
        raise RuntimeError("Primary visual QA needs a headless browser; none found")
    # Fail closed when the CI image can only draw missing-glyph squares for Chinese.
    if shutil.which("fc-list"):
        fc = subprocess.run(["fc-list", ":lang=zh-tw", "family"], capture_output=True, text=True, timeout=15)
        available = fc.stdout.lower()
        if fc.returncode != 0 or not any(name in available for name in
                                             ("noto sans cjk", "noto sans tc", "noto serif cjk",
                                              "wenquanyi", "ar pl", "source han")):
            raise RuntimeError("Traditional Chinese glyph font unavailable: rendered visual QA would show tofu boxes")
    else:
        raise RuntimeError("Fontconfig unavailable; cannot verify Chinese font coverage")
    css = (ROOT / "dist/styles.css").read_text(encoding="utf-8")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    results = []
    for page in targets:
        anchor = page["required_primary_visual"]["anchor"]
        markup = (ROOT / "dist" / page["output"]).read_text(encoding="utf-8")
        match = re.search(FIGURE.format(anchor=re.escape(anchor)), markup, re.I | re.S)
        if not match:
            raise ValueError(f"Primary figure not found in rendered HTML: {anchor}")
        # Isolated reader prose, no external dependencies, no third-party rehost.
        probe = OUTPUT / (page["output"].removesuffix(".html") + "-probe.html")
        probe.write_text(
            '<!doctype html><html lang="zh-Hant"><head>'
            '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<style>' + css + '</style></head><body class="reader-page">'
            '<main class="reading-prose" style="max-width:950px;margin:0 auto">'
            + match.group(0) + "</main></body></html>", encoding="utf-8")
        for name, width, height in [("desktop", 1440, 1600), ("mobile390", 390, 2600), ("mobile360", 360, 2800)]:
            target = OUTPUT / f"{page['output'].removesuffix('.html')}-{name}.png"
            result = subprocess.run([
                chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
                "--hide-scrollbars", "--force-device-scale-factor=1",
                "--no-first-run", "--disable-background-networking",
                "--disable-extensions", f"--window-size={width},{height}",
                f"--screenshot={target.resolve()}", probe.resolve().as_uri()
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
            if result.returncode or not target.is_file() or target.stat().st_size < 2048:
                raise RuntimeError(f"Chrome screenshot failed for {anchor}/{name}: {result.stderr[-1000:]}")
            results.append({"source":page["source"],"anchor":anchor,"viewport_width":width,"viewport_height":height,
                            "screenshot":target.name,"bytes":target.stat().st_size})
    (OUTPUT / "capture-manifest.json").write_text(
        json.dumps({"purpose":"Render evidence only; medical/visual judgment separate","captures":results},
                   ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Captured {len(results)} visual review screenshots in {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
