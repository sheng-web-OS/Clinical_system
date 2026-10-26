"""Sitewide visual-debt inventory and fail-closed gate for NEW or CHANGED figures.

The original source-provenance figure gate does not measure instructional quality.
A baseline entry is explicitly unreviewed debt, NEVER equivalent to acceptance.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FIGURE = re.compile(r"<figure\b[^>]*>[\s\S]*?</figure>", re.I)
ID = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""", re.I)
LEGACY = "audit/visual-legacy-baseline.json"
REVIEWS = "audit/visual-qa-reviews.json"
MASK = (1 << 64) - 1


def fingerprint(s: str) -> str:
    """64-bit FNV-1a over Unicode code points, for change detection (not security)."""
    h = 0xCBF29CE484222325
    for c in s:
        h ^= ord(c)
        h = (h * 0x100000001B3) & MASK
    return f"{h:016x}"


def extract_figures(text: str) -> list[dict]:
    rows = []
    for i, m in enumerate(FIGURE.finditer(text), 1):
        markup = m.group(0)
        name = ID.search(markup.split(">", 1)[0])
        figure_id = name.group(1) if name else f"__unnamed_{i:02d}"
        kind = ("embedded_image" if re.search(r"<img\b", markup, re.I) else
                "svg" if re.search(r"<svg\b", markup, re.I) else "html_css")
        rows.append({
            "id": figure_id,
            "fingerprint": fingerprint(markup),
            "kind": kind,
            "line": text.count("\n", 0, m.start()) + 1,
            "has_caption": bool(re.search(r"<figcaption\b", markup, re.I)),
            "has_alt": bool(re.search(r"<img\b[^>]*\balt\s*=", markup, re.I)),
            "has_svg_label": bool(re.search(r"<svg\b[^>]*(?:aria-label|aria-labelledby|role)\s*=", markup, re.I)),
            "cards": len(re.findall(r"<section\b", markup, re.I)),
        })
    return rows


def read_json(path: Path, *, default=None):
    if not path.is_file():
        if default is not None:
            return default
        raise ValueError(f"Missing visual audit contract: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def screenshot_check(root: Path, raw: str) -> bool:
    if not isinstance(raw, str) or not raw.startswith("audit/visual-evidence/"):
        return False
    path = (root / raw).resolve()
    folder = (root / "audit/visual-evidence").resolve()
    if not path.is_relative_to(folder) or path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        return False
    if not path.is_file() or path.stat().st_size < 8:
        return False
    header = path.open("rb").read(12)
    return ((path.suffix.lower() == ".png" and header.startswith(b"\x89PNG\r\n\x1a\n")) or
            (path.suffix.lower() in {".jpg", ".jpeg"} and header.startswith(b"\xff\xd8\xff")) or
            (path.suffix.lower() == ".webp" and header[:4] == b"RIFF" and header[8:12] == b"WEBP"))


def approved(root: Path, key: str, figure: dict, record: dict | None) -> tuple[bool, str]:
    if not isinstance(record, dict) or record.get("status") != "approved":
        return False, "missing visual QA approval"
    if record.get("fingerprint") != figure["fingerprint"]:
        return False, "visual QA approved a different figure version"
    if record.get("reviewer_type") not in {"independent_ai", "qualified_human"}:
        return False, "independent visual review missing"
    for field, minimum in [
        ("reader_misconception", 30), ("unique_visual_insight", 30),
        ("deletion_test", 30), ("medical_source_and_limits", 40),
        ("desktop_findings", 35), ("mobile_findings", 35),
        ("counterexample_check", 25),
    ]:
        if not isinstance(record.get(field), str) or len(record[field].strip()) < minimum:
            return False, f"missing substantive {field}"
    for screenshot in ("desktop_screenshot", "mobile_screenshot"):
        if not screenshot_check(root, record.get(screenshot)):
            return False, f"missing verified {screenshot}"
    if figure["kind"] != "embedded_image" and not figure["has_caption"]:
        return False, "new visual is missing a caption"
    if figure["id"].startswith("__unnamed_"):
        return False, "new visual needs a stable figure id"
    return True, "reviewed with versioned visual evidence"


def audit(root: Path, *, enforce: bool = True) -> dict:
    pages = read_json(root / "site/pages.json")
    baseline = read_json(root / LEGACY)["figures"]
    reviews = read_json(root / REVIEWS, default={}).get("reviews", {})
    rows = []
    used = set()
    errors = []
    for page in pages:
        source = page["source"]
        current = extract_figures((root / source).read_text(encoding="utf-8"))
        frozen = {f["id"]: f for f in baseline.get(source, [])}
        ids = set()
        for figure in current:
            key = f"{source}#{figure['id']}"
            if figure["id"] in ids:
                errors.append(f"Duplicate figure id in {source}: {figure['id']}")
            ids.add(figure["id"])
            used.add(key)
            legacy = frozen.get(figure["id"])
            unchanged = bool(legacy and legacy.get("fingerprint") == figure["fingerprint"])
            ok, reason = (False, "Legacy figure: never certified") if unchanged else approved(root, key, figure, reviews.get(key))
            status = "legacy_unreviewed" if unchanged else ("qa_passed" if ok else "qa_required")
            if status == "qa_required":
                errors.append(f"Visual QA HOLD: {key}: {reason}")
            risks = []
            if figure["kind"] == "html_css":
                risks.append("text_only_structure_needs_value_review")
            if figure["id"].startswith("__unnamed_"):
                risks.append("unstable_figure_id")
            if not figure["has_caption"]:
                risks.append("missing_caption")
            if figure["kind"] == "svg" and not figure["has_svg_label"]:
                risks.append("svg_accessibility_unverified")
            rows.append({"source": source, "output": page["output"], **figure,
                         "qa_status": status, "risks": risks, "reason": reason})
    # A manifest cannot certify figures that are absent from the public source list.
    for key in reviews:
        if key not in used:
            errors.append(f"Visual QA orphan review: {key}")
    stats = {
        "pages_inspected": len(pages), "figures": len(rows),
        "article_pages_with_figures": len({r["source"] for r in rows}),
        "by_kind": {k: sum(x["kind"] == k for x in rows) for k in ("html_css", "svg", "embedded_image")},
        "legacy_pending": sum(x["qa_status"] == "legacy_unreviewed" for x in rows),
        "approved": sum(x["qa_status"] == "qa_passed" for x in rows),
        "hold": sum(x["qa_status"] == "qa_required" for x in rows),
        "errors": errors,
    }
    result = {"summary": stats, "figures": rows}
    if enforce and errors:
        raise ValueError("\n".join(errors))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--report", default="")
    parser.add_argument("--no-enforce", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    result = audit(root, enforce=not args.no_enforce)
    if args.report:
        path = Path(args.report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
