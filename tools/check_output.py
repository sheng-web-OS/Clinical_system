#!/usr/bin/env python3
"""Validate the public build whitelist and navigation; does not certify clinical medicine."""
from pathlib import Path
from html.parser import HTMLParser
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from catalog import load_pages
PAGES = load_pages(ROOT)
DIST = ROOT / "dist"
EXPECTED = {
    "styles.css", "home.css", "index.html",
    "app.js", "site-index.json", "site-index.js", ".nojekyll",
} | {row["output"] for row in PAGES}
if any(p["output"] == "xiaoma-reading-dcm-integrated.html" for p in PAGES):
    EXPECTED.update(['assets/dcm-pv.webp','assets/dcm-secondary-mr.png','assets/dcm-ischemic-cmr.webp'])
actual = {p.relative_to(DIST).as_posix() for p in DIST.rglob("*") if p.is_file()} if DIST.is_dir() else set()
errors = []
if actual != EXPECTED:
    errors.append(f"Output whitelist mismatch. Missing: {sorted(EXPECTED-actual)}; Unexpected: {sorted(actual-EXPECTED)}")

class Outline(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = []
        self.links = []
        self.h1_count = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        ident = a.get("id")
        if ident:
            if ident in self.ids: self.duplicates.append(ident)
            self.ids.add(ident)
        if tag in ("a","link","img","script"):
            target = a.get("src" if tag in ("img","script") else "href")
            if target: self.links.append(target)
        if tag == "h1": self.h1_count += 1

if not errors:
    outlines = {}
    for filename in sorted(EXPECTED):
        if not filename.endswith(".html"): continue
        html = (DIST / filename).read_text("utf8")
        dom = Outline()
        dom.feed(html)
        outlines[filename] = dom
        if dom.h1_count != 1: errors.append(f"{filename}: expected 1 H1, got {dom.h1_count}")
        if dom.duplicates: errors.append(f"{filename}: repeated IDs {dom.duplicates}")
        for href in dom.links:
            if href.startswith(("http://","https://","mailto:","tel:","//","#","data:")): continue
            path = href.split("#",1)[0]
            if not (DIST / path).is_file(): errors.append(f"{filename}: broken local asset {href}")
    # Validate local fragments as well as file existence on every published page.
    for filename, dom in outlines.items():
        for href in dom.links:
            if href.startswith(("http://","https://","mailto:","tel:","//","data:")): continue
            path, _, fragment = href.partition("#")
            target = outlines.get(path or filename)
            if fragment and target is not None and fragment not in target.ids:
                errors.append(f"{filename}: missing fragment {href}")
    for filename in actual:
        if filename.startswith("assets/"): continue
        content = (DIST / filename).read_text("utf8")
        for private_token in ("libfile_", "5824859", "Z639", "plan-20261021.md", "七大核心學習檔案"):
            if private_token in content: errors.append(f"{filename}: private plan data in public build: {private_token}")
    front = (DIST/"index.html").read_text("utf8")
    if "小麻閱讀" not in front or "library-grid" not in front:
        errors.append("Missing editorial library landing page")
    try:
        index = json.loads((DIST / "site-index.json").read_text("utf8"))
        if not isinstance(index, list) or not all(isinstance(row, dict) and isinstance(row.get("url"), str) for row in index):
            raise ValueError("Search index must be a list of page records")
        urls = [row["url"] for row in index]
        if len(urls) != len(PAGES) or set(urls) != {row["output"] for row in PAGES}:
            errors.append("Search index does not match the public catalog")
        inline = (DIST / "site-index.js").read_text("utf8").strip()
        prefix = "window.CLINICAL_INDEX = "
        if not inline.startswith(prefix) or not inline.endswith(";"):
            raise ValueError("Inline search payload has an unexpected format")
        if json.loads(inline[len(prefix):-1]) != index:
            errors.append("Inline search payload differs from the JSON search index")
    except (ValueError, TypeError) as exc:
        errors.append("Invalid search index: " + str(exc))
    if 'href="https://github.com/sheng-web-OS/Clinical_system"' in front:
        errors.append("Private repository direct link should not appear in public nav")

if errors:
    print("\n".join("FAIL: "+e for e in errors))
    sys.exit(1)
print("PASS: static site whitelist, single H1, unique DOM IDs, local assets, matching search indexes, private repo nav boundary.")
print("NOTE: this is structural QA, not full clinical validation or live HTTPS verification.")
