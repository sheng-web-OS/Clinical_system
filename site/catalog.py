"""Explicit publication list shared by the compiler and output checks."""
import json
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
                source.parts[0] not in ("content", "audit") or
                source.suffix != ".md"):
            raise ValueError("Public source must be approved content/ or audit/ Markdown")
        path = (root / row["source"]).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError("Missing or escaped publication source: " + row["source"])
        if path.relative_to(root.resolve()).parts[0] not in ("content", "audit"):
            raise ValueError("Public source resolves into a private directory")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.html", row["output"]):
            raise ValueError("Output must be a flat HTML filename")
        if row["source"] in sources or row["output"] in outputs:
            raise ValueError("Duplicate publication source or output")
        sources.add(row["source"])
        outputs.add(row["output"])
        if "/lessons/" in row["source"]:
            date.fromisoformat(row.get("date", ""))
            if row.get("review") not in ("author_source_check", "independent_ai_review", "human_review"):
                raise ValueError("Lesson must disclose its actual review type")
    return pages
