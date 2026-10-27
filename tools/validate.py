#!/usr/bin/env python3
"""Fast deterministic structural audit. It does not certify clinical correctness."""
from pathlib import Path
import argparse
import re
import sys
root=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "site"))
from catalog import load_pages


# Reader-facing source is not the GitHub editorial changelog. These patterns
# are intentionally high-confidence rather than generic terms such as
# "review", "source", "not yet", or "updated", which can be clinically essential.
# The historical author originals are immutable and not subject to this rule.
_PUBLIC_COPY_LEAK_RULES = (
    ("PR or issue bookkeeping", re.compile(r"\b(?:PR|Issue)\s*#\d+\b", re.I)),
    ("question intake accounting", re.compile(
        r"不重複計數|本次新增.{0,24}(?:題|題號)|本輪新增|"
        r"原已收錄於|本次新建.{0,24}(?:題|題號)"
    )),
    ("deployment / workflow log", re.compile(
        r"GitHub Actions run\s*\d+|Cloudflare production commit|"
        r"\b(?:Draft\s*/\s*HOLD|HOLD\s*/\s*Draft)\b", re.I
    )),
)

# Teaching chapters must not carry the source-checking editor's notebook.
# The detailed original-paper verification belongs in a dedicated *-sources.md
# reference page, while each lesson retains official paper/answer links.
_READER_EDITORIAL_FOOTER_RULES = (
    ("source-verification appendix", re.compile(
        r"^\s*#{2,6}\s*(?:本篇來源與版本界線|原卷逐頁核對紀錄|"
        r"編輯核讀與版本狀態|來源核對與版本界線)\s*$"
    )),
    ("source-verification worklog", re.compile(
        r"^\s*(?:原始資料使用|逐頁目視核對紀錄)\s*[:：]"
    )),
)


def public_copy_leak_errors(source, text):
    """Find clear editorial worklog in a published reader page (not medicine)."""
    if "/originals/" in source:
        return []
    errors = []
    is_teaching_chapter = any(part in source for part in ("/lessons/", "/integrated/", "/exams/"))
    rules = _PUBLIC_COPY_LEAK_RULES + (_READER_EDITORIAL_FOOTER_RULES if is_teaching_chapter else ())
    for line_no, line in enumerate(text.splitlines(), 1):
        for reason, expression in rules:
            if expression.search(line):
                errors.append(f"{source}:{line_no}: public editorial metadata ({reason})")
                break
    return errors


def private_pilot_errors():
    """Preserve the original private sample checks without requiring public output."""
    s=(root/"content/tamponade.md").read_text(encoding="utf8")
    e=(root/"audit/esc2025-figure-check.md").read_text(encoding="utf8")
    a=(root/"audit/audit-log.md").read_text(encoding="utf8")
    errors=[]
    for n in range(1,9):
        if s.count(f"<!-- U{n:02} -->")!=1:errors.append(f"U{n:02} marker missing or duplicated")
    for n in range(1,9):
        if f"[{n}]" not in s:errors.append(f"Reference {n} missing")
    for token in ("Figure 12","Recommendation Table 12","Recommendation Table 21","Table 17","≥6",">6","without delay","3–6","Class I"):
        if token not in s+e:errors.append("Missing high-risk source marker "+token)
    if len(re.findall(r"(?m)^## \d+\.",s))<10:errors.append("Expected 10 didactic sections")
    if re.search(r"!\[[^]]*\]\(assets/[^)]+\)",s):errors.append("Broken local asset reference")
    for path in ["site/build.py","site/styles.css","site/app.js","audit/audit-log.md","audit/esc2025-figure-check.md","archive/tamponade_r2_baseline.md"]:
        if not (root/path).exists():errors.append("Missing "+path)
    if "2026-10-21" not in a:errors.append("Audit date absent")
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-pilot",action="store_true",help="Also check the private Tamponade sample; never publish it")
    args=parser.parse_args()
    errors=[]
    try:
        pages=load_pages(root)
        for row in pages:
            name = row["source"]
            text=(root/name).read_text(encoding="utf8")
            if row.get("kind") != "historical_original":
                errors.extend(public_copy_leak_errors(name, text))
            for target in re.findall(r"\[[^]]*\]\(([^)]+)\)",text):
                if not target.startswith(("http://","https://","#")):
                    p=(root/name).parent/target.split("#")[0]
                    if not p.exists():errors.append(f"Unresolved local Markdown link {name}: {target}")
        if args.private_pilot:
            errors.extend(private_pilot_errors())
    except (OSError,ValueError) as exc:
        errors.append(str(exc))
    if errors:
        print("FAILED\n"+"\n".join(errors))
        return 1
    print("PASS: public source boundaries and local Markdown links.")
    if args.private_pilot:
        print("PASS: existing private pilot anchors, sections and evidence markers.")
    print("LIMIT: Structural verification only; does not imply guideline full-text or medical specialist validation.")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
