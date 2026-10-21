#!/usr/bin/env python3
"""Validate the public build whitelist and navigation; does not certify clinical medicine."""
from pathlib import Path
from html.parser import HTMLParser
import sys
import os

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from catalog import load_public_pages
PREVIEW = os.environ.get('CF_PAGES_BRANCH','') not in ('','main') or (os.environ.get('CLINICAL_SITE_PREVIEW') == '1' and os.environ.get('CF_PAGES_BRANCH') != 'main')
PAGES = load_public_pages(ROOT, preview=PREVIEW)
DIST = ROOT / "dist"
EXPECTED = {
    "styles.css", "home.css", "index.html",
    "app.js", "site-index.json", "site-index.js", ".nojekyll",
} | {row["output"] for row in PAGES}
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
        content = (DIST / filename).read_text("utf8")
        for private_token in ("libfile_", "5824859", "Z639", "plan-20261021.md", "七大核心學習檔案"):
            if private_token in content: errors.append(f"{filename}: private plan data in public build: {private_token}")
    front = (DIST/"index.html").read_text("utf8")
    if "小麻閱讀" not in front or "library-grid" not in front:
        errors.append("Missing editorial library landing page")
    if 'href="tamponade.html"' in front or "tamponade.html" in actual:
        errors.append("Internal Tamponade pilot must not be published")
    # Verify both clinical reading modes present the same verified core facts.
    interactive = (DIST / "lvoto-case-interactive.html").read_text("utf8")
    static = (DIST / "lvoto-case-static.html").read_text("utf8")
    for item in ("LVEDD 37 mm", "EF 80%", "98 mmHg", "369", "620", "torsemide", "HCM"):
        if item not in interactive or item not in static:
            errors.append(f"Clinical-case missing evidence in one reading mode: {item}")
    if interactive.count('data-case-stage="') != 4:
        errors.append("Interactive case must contain exactly four clinical decisions")
    if interactive.count('data-case-correct="') != 4 or interactive.count('data-case-rationale') != 4:
        errors.append("Interactive case lost stage answers or explanatory reasoning")
    if '<section class="case-analysis" data-case-analysis>' not in interactive:
        errors.append("Interactive case full-explanation fallback was not rendered")
    if '<!-- CASE_ANALYSIS_START -->' in interactive or '\\n</div>' in interactive:
        errors.append("Interactive case contains raw rendering artifacts")
    if 'data-case-sequence' in static:
        errors.append("Static comparison must not depend on the interactive UI")
    if 'jtd.amegroups.org/article/view/5226/html' not in interactive or 'jtd.amegroups.org/article/view/5226/html' not in static:
        errors.append("Original case and Figure 1–3 link missing")

    if 'tamponade.html' in front or 'tamponade.html' in actual:
        errors.append("Internal Tamponade pilot exposed")
    if any(t in front for t in ("RECOVER", "INTEGRATE", "VALIDATE", "audit-log.html")):
        errors.append("Private editorial workflow leaked to readers")
    if PREVIEW:
        if '編輯審查預覽' not in front:
            errors.append("Preview lacks a truthful editorial status label")
        for page in actual:
            if page.endswith(".html") and 'noindex,nofollow' not in (DIST/page).read_text("utf8"):
                errors.append(page + ": missing noindex,nofollow in preview")
    if 'href="https://github.com/sheng-web-OS/Clinical_system"' in front:
        errors.append("Private repository direct link should not appear in public nav")

if errors:
    print("\n".join("FAIL: "+e for e in errors))
    sys.exit(1)
print("PASS: static site whitelist, single H1, unique DOM IDs, local assets, internal-pilot exclusion, private repo nav boundary.")
print("NOTE: this is structural QA, not full clinical validation or live HTTPS verification.")
