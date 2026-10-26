#!/usr/bin/env python3
"""Derive manuscript intake and publishing state from live repository files.

Not a medical review, author approval check, or public deployment check.
Historical checkpoints are deliberately ignored: they are not live state.
"""
import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from catalog import load_pages

INTAKE = "archive/xiaoma-reading/intake/2026-10-21-chat-manuscripts.md"
ORIGINALS = "content/xiaoma-reading/originals"


def read_intake(root):
    lines = (root / INTAKE).read_text(encoding="utf8").splitlines()
    start = next((i for i, line in enumerate(lines)
                  if line.startswith("| 日期（文章自述） | 原始題名 |")), -1)
    if start < 0:
        raise ValueError("Intake table header is absent")
    records = []
    for line in lines[start + 1:]:
        if not line.startswith("|"):
            if records:
                break
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            raise ValueError("Expected four intake columns")
        if cells[0].startswith("---"):
            continue
        records.append(dict(zip(("date", "title", "series", "status"), cells)))
    if not records:
        raise ValueError("No intake records")
    return records


def inspect_inventory(root):
    root = root.resolve()
    errors = []
    try:
        rows = read_intake(root)
        pages = load_pages(root)
    except (OSError, ValueError, KeyError) as exc:
        return None, [str(exc)]

    published = {x["source"] for x in pages
                 if x.get("kind") == "historical_original"}
    actual = {p.relative_to(root).as_posix()
              for p in (root / ORIGINALS).glob("*.md") if p.is_file()}
    imported, snapshots, pending = set(), set(), set()
    titles = set()
    for row in rows:
        title, status = row["title"], row["status"]
        if not title or not row["series"]:
            errors.append("Empty title or series")
        if title in titles:
            errors.append("Duplicate title needs a version-specific intake entry: " + title)
        titles.add(title)
        if status == "conversation_only":
            pending.add(title)
            continue
        # A source snapshot is recovered text, not an approved original or release.
        # Accept legacy bold status labels and an optional explanatory note after ；.
        m = re.fullmatch(
            r"(?:\*\*)?(imported|source_snapshot_archived)(?:\*\*)? → \x60([^\x60]+)\x60(?:；[^|]*)?",
            status)
        if not m:
            errors.append("Unknown intake state for " + title + ": " + status)
            continue
        state, path_text = m.groups()
        source = PurePosixPath(path_text)
        expected_prefix = (ORIGINALS + "/" if state == "imported"
                           else "archive/xiaoma-reading/intake/")
        if (source.is_absolute() or ".." in source.parts or
                source.suffix != ".md" or not path_text.startswith(expected_prefix)):
            errors.append("Unsafe source: " + path_text)
            continue
        path = (root / path_text).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append("Missing or escaped source: " + path_text)
            continue
        destination = imported if state == "imported" else snapshots
        if path_text in imported or path_text in snapshots:
            errors.append("Duplicate archived source: " + path_text)
        destination.add(path_text)

    outside = sorted(p for p in published if not p.startswith(ORIGINALS + "/"))
    errors.extend("Published historical original outside originals folder: " + p for p in outside)
    if len(imported) + len(snapshots) + len(pending) != len(rows):
        errors.append("Intake row with unverified/missing status")

    result = {
        "input_ledger": INTAKE,
        "scope": "files + publication manifest; not author canonical or clinical review",
        "intake_total": len(rows),
        "intake_imported": len(imported),
        "intake_source_snapshots": len(snapshots),
        "source_snapshot_paths": sorted(snapshots),
        "intake_conversation_only": len(pending),
        "original_files": len(actual),
        "published_originals": len(published),
        "imported_published": len(imported & published),
        "published_paths": sorted(published),
        "unpublished_original_paths": sorted(actual - published),
        "imported_unpublished_paths": sorted(imported - published),
        "limits": [
            "Conversation-only records are not recovered files.",
            "Source snapshots preserve conversation-provided text, not verified published originals.",
            "A file and SHA do not prove correspondence to a Facebook published edition.",
            "Manifest inclusion does not prove clinical review or Cloudflare delivery.",
            "Do not derive counts from historical checkpoint snapshots."
        ]
    }
    return result, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report, errors = inspect_inventory(args.root)
    if args.json:
        print(json.dumps({"inventory": report, "errors": errors}, ensure_ascii=False, indent=2))
    elif report:
        print("PASS" if not errors else "FAIL", "Corpus inventory:",
              report["intake_total"], "intake;",
              report["intake_imported"], "imported;",
              report["intake_source_snapshots"], "source snapshots;",
              report["intake_conversation_only"], "conversation-only;",
              report["original_files"], "source files;",
              report["published_originals"], "published originals.")
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
