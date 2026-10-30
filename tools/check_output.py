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
POCKET_SOURCE_ASSETS = ({
    "pocket-medicine-9e-fig2-5-hypoxemia.png",
    "pocket-medicine-9e-high-paco2.png",
} if any("2026-10-25-hypoxemia-mechanisms.md" in p["source"] for p in PAGES) else set())
EXPECTED = {
    "styles.css", "home.css", "index.html",
    "app.js", "site-index.json", "site-index.js", "owner-mode.html", ".nojekyll",
} | POCKET_SOURCE_ASSETS | {row["output"] for row in PAGES}
if any(page["output"] == "xiaoma-20261027-cticu-oxygen-delivery.html" for page in PAGES):
    EXPECTED.add("cticu-oxygen-delivery-two-paths.svg")
# Only release-registered CTICU ABG lessons may ship their reviewed SVG assets.
for article_output, svg_name in (
    ("xiaoma-20261029-cticu-abg-03-cpb-acidbase.html", "cticu-abg-03-cpb-acidbase-group-trends.svg"),
    ("xiaoma-20261029-cticu-abg-04-alphastat-phstat.html", "cticu-abg-04-alpha-phstat-logic.svg"),
):
    if any(page["output"] == article_output for page in PAGES):
        EXPECTED.add(svg_name)

HAS_DCM_RELEASE = (
    any(p["output"] == "xiaoma-reading-dcm-integrated.html" for p in PAGES)
    and any(p["output"] == "xiaoma-reading-20260710-dcm-original.html" for p in PAGES)
)
if HAS_DCM_RELEASE:
    EXPECTED.add("xiaoma-reading-20260710-dcm.html")  # legacy reader redirect
if any(p["output"] == "knowledge-atlas.html" for p in PAGES):
    EXPECTED.add("xiaoma-plan.html")  # unindexed legacy alias, not a duplicate map
if any(p["output"] == "xiaoma-reading-dcm-integrated.html" for p in PAGES):
    EXPECTED.update(['assets/dcm-pv.webp','assets/dcm-secondary-mr.png','assets/dcm-ischemic-cmr.webp'])
# Only the three medically source-verified ECGs for the published AF/WCT
# lessons are allowed; these bytes are fetched, checked and bundled at build.
if any(p["output"] in ("xiaoma-reading-preexcited-af.html","xiaoma-reading-wct-acls-decision.html") for p in PAGES):
    EXPECTED.update({f"assets/silverman-2018-fig{n}.jpg" for n in (1, 2, 3)})
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
        # Canonical reading pages must contain one beacon; redirects must contain none.
        canonical = filename == "index.html" or filename in {page["output"] for page in PAGES}
        expected = 1 if canonical else 0
        actual_beacons = html.count("https://static.cloudflareinsights.com/beacon.min.js")
        if actual_beacons != expected:
            errors.append(f"{filename}: expected {expected} analytics beacon(s), found {actual_beacons}")
        if canonical and 'data-cf-beacon=' not in html:
            errors.append(f"{filename}: analytics site token metadata missing")
        if canonical:
            if 'id="clinical-analytics-config"' not in html or 'clinical-analytics-owner-v1' not in html:
                errors.append(f"{filename}: owner opt-out guard missing")
            if '<script defer src="https://static.cloudflareinsights.com/beacon.min.js"' in html:
                errors.append(f"{filename}: unguarded static analytics beacon detected")
        if filename == "owner-mode.html":
            if 'name="robots" content="noindex,nofollow"' not in html or 'localStorage.setItem(key, "1")' not in html:
                errors.append("Owner-mode activation is missing or publicly indexable")
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
    for filename in POCKET_SOURCE_ASSETS:
        payload = (DIST / filename).read_bytes()
        if not payload.startswith(b"\x89PNG\r\n\x1a\n") or len(payload) < 4000:
            errors.append(f"{filename}: malformed source figure PNG")
    for filename in actual:
        if filename.startswith("assets/") or filename in POCKET_SOURCE_ASSETS: continue
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
        errors.append("Repository source link must not appear in site navigation (output policy, not GitHub privacy)")

    if "knowledge-atlas.html" in {p["output"] for p in PAGES}:
        legacy_map = (DIST / "xiaoma-plan.html").read_text("utf8")
        if 'http-equiv="refresh"' not in legacy_map or 'url=knowledge-atlas.html' not in legacy_map:
            errors.append("Old learning-map route must redirect to the single clinical atlas")
        if "xiaoma-plan.html" in [p["output"] for p in PAGES] or "xiaoma-plan.html" in (DIST / "site-index.json").read_text("utf8"):
            errors.append("Retired map must not have a second public search/listing identity")
        if 'href="xiaoma-plan.html"' in front or 'href="xiaoma-plan.html"' in (DIST / "knowledge-atlas.html").read_text("utf8"):
            errors.append("Home and atlas may not promote duplicate learning map")
        atlas_body = (DIST / "knowledge-atlas.html").read_text("utf8")
        originals = [row for row in PAGES if row.get("kind") == "historical_original"]
        from reading import _group, primary_versions
        primary = primary_versions(PAGES)
        if "<summary>歷史原稿典藏" in atlas_body:
            errors.append("Historical provenance must not be a clinical atlas category")
        if any(not row.get("section") or _group(row) in ("歷史原稿典藏", "其他閱讀") for row in originals):
            errors.append("Every published original must have a clinical topic")
        atlas_index = atlas_body.split('<div class="atlas-article-index">', 1)[-1].split('</div>', 1)[0]
        if atlas_index.count('class="atlas-origin-note">原稿・尚無完整整合版</small>') != len(originals) - len(primary):
            errors.append("Original-only articles must remain findable until a full integrated replacement exists")
        for original_output, current in primary.items():
            primary_link = 'href="' + current["output"] + '"'
            old_link = 'href="' + original_output + '"'
            paired_rows = [item for item in atlas_index.split('<li>')[1:]
                           if primary_link in item.split('</li>', 1)[0]]
            if (len(paired_rows) != 1 or
                    old_link not in paired_rows[0].split('</li>', 1)[0] or
                    'class="atlas-source-link">版本對照：' not in paired_rows[0]):
                errors.append("Current reading must own a secondary version link: " + original_output)
            if any(old_link in item.split('</li>', 1)[0] and primary_link not in item.split('</li>', 1)[0]
                   for item in atlas_index.split('<li>')[1:]):
                errors.append("Superseded original appears as a competing atlas article: " + original_output)
            archive_page = (DIST / original_output).read_text("utf8")
            if 'class="original-reading-primary"' not in archive_page or primary_link not in archive_page:
                errors.append("Preserved original does not link back to current reading: " + original_output)
        original_page = (DIST / "xiaoma-reading.html").read_text("utf8")
        if 'class="archive-version-list"' not in original_page:
            errors.append("Preserved originals must have a compact provenance list")
        indexed_urls = [entry["url"] for entry in index] if isinstance(index, list) else []
        if any(indexed_urls.index(current["output"]) >= indexed_urls.index(original)
               for original, current in primary.items()
               if original in indexed_urls and current["output"] in indexed_urls):
            errors.append("Full-text search must prioritize canonical reading over preserved original")
        for target in ("dyspnea", "perfusion", "chest", "kidney", "infection", "time"):
            if 'id="' + target + '"' not in atlas_body:
                errors.append("Clinical atlas missing problem-first branch " + target)

    if HAS_DCM_RELEASE:
        # Release regression: the old DCM URL, homepage, library index, and
        # search must lead to the current integrated article by default.
        latest = "xiaoma-reading-dcm-integrated.html"
        legacy = "xiaoma-reading-20260710-dcm.html"
        archive = "xiaoma-reading-20260710-dcm-original.html"
        if not (DIST / archive).is_file():
            errors.append("Preserved 2026-07-10 DCM archive is missing")
        old_route = (DIST / legacy).read_text("utf8")
        if 'http-equiv="refresh"' not in old_route or 'url=' + latest not in old_route:
            errors.append("Old public DCM URL must open the current integrated article")
        if not (DIST / latest).is_file() or "當心臟變大" not in (DIST / latest).read_text("utf8"):
            errors.append("Current DCM content is missing")
        if front.find('href="' + latest + '"') < 0:
            errors.append("Home does not link to the current DCM reading")
        else:
            first_card = front.find('<a class="library-card')
            first_new = front.find('href="' + latest + '"')
            if first_card < 0 or first_new != front.find('href="', first_card):
                errors.append("Current reading is not the first homepage card")
        reading_index = (DIST / "xiaoma-reading.html").read_text("utf8")
        new_entry = reading_index.find('href="' + latest + '"')
        archived_entry = reading_index.find('href="' + archive + '"')
        if new_entry < 0 or archived_entry < 0 or new_entry >= archived_entry:
            errors.append("Reading library displays archived DCM ahead of current reading")
        indexed_urls = [row["url"] for row in index] if isinstance(index, list) else []
        if latest not in indexed_urls or archive not in indexed_urls or indexed_urls.index(latest) >= indexed_urls.index(archive):
            errors.append("Search results prioritize archived DCM over the current article")

if errors:
    print("\n".join("FAIL: "+e for e in errors))
    sys.exit(1)
print("PASS: static site whitelist, single H1, unique DOM IDs, local assets, matching search indexes, no repository source link in site navigation (GitHub repository PUBLIC).")
print("NOTE: output-only structural QA; public GitHub sources, PRs, Actions logs/artifacts are NOT private. Clinical/rights review and production verification are separate.")
