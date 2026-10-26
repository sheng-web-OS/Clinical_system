"""Sitewide visual-debt inventory and fail-closed gate for NEW or CHANGED figures.

The original source-provenance figure gate does not measure instructional quality.
A baseline entry is explicitly unreviewed debt, NEVER equivalent to acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
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
        images = re.findall(r"<img\\b[^>]*>", markup, re.I)
        svgs = re.findall(r"<svg\\b[^>]*>", markup, re.I)
        kind = ("embedded_image" if images else "svg" if svgs else "html_css")
        image_sources = all(re.search(r"""\\bsrc\\s*=\\s*["']\\S+["']""", tag, re.I) for tag in images)
        image_descriptions = all(re.search(r"""\\balt\\s*=\\s*["'][^"']+["']""", tag, re.I) for tag in images)
        svg_named = bool(svgs) and all(
            re.search(r"""\\baria-(?:label|labelledby)\\s*=\\s*["'][^"']+["']""", tag, re.I)
            or re.search(r"<title\\b[^>]*>[^<]+</title>", markup, re.I)
            for tag in svgs
        )
        rows.append({
            "id": figure_id,
            "fingerprint": fingerprint(markup),
            "kind": kind,
            "line": text.count("\n", 0, m.start()) + 1,
            "has_caption": bool(re.search(r"<figcaption\b", markup, re.I)),
            "has_alt": bool(re.search(r"<img\b[^>]*\balt\s*=", markup, re.I)),
            "has_svg_label": bool(re.search(r"<svg\\b[^>]*(?:aria-label|aria-labelledby|role)\\s*=", markup, re.I)),
            "images_have_source": image_sources,
            "images_described": image_descriptions,
            "svg_named": svg_named,
            "cards": len(re.findall(r"<section\b", markup, re.I)),
        })
    return rows


def read_json(path: Path, *, default=None):
    if not path.is_file():
        if default is not None:
            return default
        raise ValueError(f"Missing visual audit contract: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def screenshot_filename(key: str, figure_fingerprint: str, viewport: int) -> str:
    """Stable figure-and-version-bound evidence name; matches browser screenshot width."""
    identity = hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]
    return f"{identity}-{figure_fingerprint}-{viewport}.png"


def screenshot_check(root: Path, raw: str, *, key: str | None = None,
                     figure_fingerprint: str | None = None,
                     viewport: int | None = None) -> bool:
    """Check the actual PNG dimensions, not just a misleading .png file name.

    Dimensions and file identity are structural evidence only, not proof that a
    human can read the image or that the medical inference is sound.
    """
    if not isinstance(raw, str) or not raw.startswith("audit/visual-evidence/"):
        return False
    path = (root / raw).resolve()
    folder = (root / "audit/visual-evidence").resolve()
    if not path.is_relative_to(folder) or path.suffix.lower() != ".png":
        return False
    if key is not None:
        if figure_fingerprint is None or viewport is None:
            return False
        if path.name != screenshot_filename(key, figure_fingerprint, viewport):
            return False
    if not path.is_file() or path.stat().st_size < 120:
        return False
    header = path.open("rb").read(24)
    if not (header.startswith(b"\\x89PNG\\r\\n\\x1a\\n") and header[12:16] == b"IHDR"):
        return False
    width, height = struct.unpack(">II", header[16:24])
    if width < 120 or height < 64:
        return False
    if viewport is not None and width > viewport:
        return False
    return True


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
    for field, viewport in (
        ("mobile_360_screenshot", 360),
        ("mobile_390_screenshot", 390),
        ("desktop_screenshot", 1280),
    ):
        if not screenshot_check(root, record.get(field), key=key,
                                figure_fingerprint=figure["fingerprint"], viewport=viewport):
            expected = screenshot_filename(key, figure["fingerprint"], viewport)
            return False, f"missing verified {field}: expected audit/visual-evidence/{expected}"
    if not figure["has_caption"]:
        return False, "new visual is missing a caption"
    if figure["kind"] == "embedded_image" and not figure["images_have_source"]:
        return False, "clinical source image has no src"
    if figure["kind"] == "embedded_image" and not figure["images_described"]:
        return False, "clinical source image needs nonempty alt text"
    if figure["kind"] == "svg" and not figure["svg_named"]:
        return False, "SVG lacks a readable title or aria-label"
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
