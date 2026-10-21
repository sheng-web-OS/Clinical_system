#!/usr/bin/env python3
"""Validate the public build whitelist and navigation; does not certify clinical medicine."""
from pathlib import Path
from html.parser import HTMLParser
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
EXPECTED = {
    "index.html", "esc-audit.html", "audit-log.html", "styles.css",
    "app.js", "site-index.json", "site-index.js", ".nojekyll",
}
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
    for filename in ("index.html","esc-audit.html","audit-log.html"):
        html = (DIST / filename).read_text("utf8")
        dom = Outline()
        dom.feed(html)
        if dom.h1_count != 1: errors.append(f"{filename}: expected 1 H1, got {dom.h1_count}")
        if dom.duplicates: errors.append(f"{filename}: repeated IDs {dom.duplicates}")
        for href in dom.links:
            if href.startswith(("http://","https://","mailto:","tel:","//","#","data:")): continue
            path = href.split("#",1)[0]
            if not (DIST / path).is_file(): errors.append(f"{filename}: broken local asset {href}")
    front = (DIST/"index.html").read_text("utf8")
    if "Cardiac Tamponade Mimicking Sepsis" not in front: errors.append("Missing case title")
    for i in range(1,9):
        if f'id="u{i:02}"' not in front: errors.append(f"Missing U{i:02} chapter anchor")
    if 'href="https://github.com/sheng-web-OS/Clinical_system"' in front:
        errors.append("Private repository direct link should not appear in public nav")

if errors:
    print("\n".join("FAIL: "+e for e in errors))
    sys.exit(1)
print("PASS: static site whitelist, single H1, unique DOM IDs, local assets, eight source anchors, private repo nav boundary.")
print("NOTE: this is structural QA, not full clinical validation or live HTTPS verification.")
