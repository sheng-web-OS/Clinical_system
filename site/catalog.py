"""Explicit publication list shared by the compiler and output checks."""
import json
import hashlib
import re
from datetime import date
from pathlib import PurePosixPath


def load_pages(root):
    pages = json.loads((root / "site/pages.json").read_text("utf8"))
    if not isinstance(pages, list) or not pages:
        raise ValueError("Publication list must be a non-empty array")
    sources, outputs = set(), set()
    for row in pages:
        for key in ("source", "output", "title", "subtitle"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError("Missing publication field: " + key)
        source = PurePosixPath(row["source"])
        if (source.is_absolute() or ".." in source.parts or
                source.parts[0] != "content" or
                source.suffix != ".md"):
            raise ValueError("Public source must be reader-facing content/ Markdown; internal audit/ stays private")
        if source.as_posix() == "content/tamponade.md":
            raise ValueError("Internal Tamponade pilot stays private")
        path = (root / row["source"]).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError("Missing or escaped publication source: " + row["source"])
        if path.relative_to(root.resolve()).parts[0] != "content":
            raise ValueError("Public source resolves into a private directory")
        if path.relative_to(root.resolve()).as_posix() == "content/tamponade.md":
            raise ValueError("Internal Tamponade pilot stays private")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.html", row["output"]):
            raise ValueError("Output must be a flat HTML filename")
        if row["source"] in sources or row["output"] in outputs:
            raise ValueError("Duplicate publication source or output")
        sources.add(row["source"])
        outputs.add(row["output"])
        if "/lessons/" in row["source"]:
            date.fromisoformat(row.get("date", ""))
            if row.get("review") not in ("author_source_check", "ai_editorial_review", "independent_ai_review", "human_review"):
                raise ValueError("Lesson must disclose its actual review type")
        if row.get("kind") == "historical_original":
            date.fromisoformat(row.get("date", ""))
            if row.get("review") != "source_recovery_only":
                raise ValueError("Recovered original must disclose the source recovery review")
            fingerprint = row.get("source_sha256", "")
            if not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
                raise ValueError("Recovered original requires its source fingerprint")
            if hashlib.sha256(path.read_bytes()).hexdigest() != fingerprint:
                raise ValueError("Recovered original changed: " + row["source"])
    # Essential source algorithms are part of the visible reader experience, not a buried citation.
    for row in pages:
        contract = row.get("required_primary_visual")
        if contract is None:
            continue
        if not isinstance(contract, dict):
            raise ValueError("Primary visual contract must be an object: " + row["source"])
        ident, url = contract.get("anchor"), contract.get("official_source_url")
        if (not isinstance(ident, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", ident)
                or not isinstance(url, str) or not url.startswith("https://")):
            raise ValueError("Invalid primary visual contract: " + row["source"])
        content = (root / row["source"]).read_text(encoding="utf-8")
        pat = r'<figure\b(?=[^>]*\bid=["\x27]' + re.escape(ident) + r'["\x27])[^>]*>(.*?)</figure>'
        match = re.search(pat, content, flags=re.IGNORECASE | re.DOTALL)
        if not match:
            raise ValueError("PRIMARY_VISUAL_MISSING: " + row["source"] + " #" + ident)
        figure = match.group(1)
        if url not in figure or not re.search(r"<figcaption\b", figure, re.IGNORECASE):
            raise ValueError("PRIMARY_VISUAL_SOURCE_HIDDEN: " + row["source"] + " #" + ident)
        if not re.search(r"<(?:svg|img|table)\b", figure, re.IGNORECASE):
            raise ValueError("PRIMARY_VISUAL_IS_TEXT_ONLY: " + row["source"] + " #" + ident)
        if contract.get("require_desktop_and_mobile_variants"):
            if ("acls-desktop-graph" not in figure or "acls-mobile-graph" not in figure):
                raise ValueError("PRIMARY_VISUAL_MOBILE_MISSING: " + row["source"] + " #" + ident)

    # Mandatory diagram/table provenance check: new teaching pages must disclose actual source review.
    from figure_gate import validate_figure_gate
    from exam_archive import validate_exam_catalog
    validate_figure_gate(root, pages)
    validate_exam_catalog(pages, root)
    return pages

