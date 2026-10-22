#!/usr/bin/env python3
"""Fast deterministic structural audit. It does not certify clinical correctness."""
from pathlib import Path
import argparse
import re
import sys
root=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "site"))
from catalog import load_pages

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
        for name in [row["source"] for row in pages]:
            text=(root/name).read_text(encoding="utf8")
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
