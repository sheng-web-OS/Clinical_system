#!/usr/bin/env python3
"""ALE read-only lexical novelty preflight against canonical atlas + deep lesson.

This only locates text markers, not clinical semantic truth. No model, web,
personal data, Anki or network access, public-site/graph writes, or promotion.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

IDENTIFIER = re.compile(r"[a-z][a-z0-9_-]{2,63}\Z")
MARKER = re.compile(r"[\w\u3400-\u9fff][\w\u3400-\u9fff\s+./-]{1,65}\Z", re.UNICODE)
ATLAS = "content/clinical-os/index.md"
ARTICLE_PREFIX = "content/xiaoma-internal-medicine/lessons/"
ALLOWED_KEYS = {"source_classification", "article_path", "candidates"}
CANDIDATE_KEYS = {"id", "source_ids", "markers", "hypothesis_status"}
REFERENCE = re.compile(r"(?:pmid_[1-9][0-9]{6,8}|agency_(?:cdc|fda)_[a-z0-9_]{3,45})\Z")


def _validate(packet: dict) -> None:
    if type(packet) is not dict or set(packet) != ALLOWED_KEYS:
        raise ValueError("invalid public-safe context packet")
    if packet["source_classification"] != "PUBLIC_SOURCE_LINKED":
        raise ValueError("owner-private or unclassified input is prohibited")
    article = packet["article_path"]
    if (type(article) is not str or not article.startswith(ARTICLE_PREFIX)
            or not article.endswith(".md") or ".." in article or "\\" in article
            or len(article) > 180):
        raise ValueError("invalid publicly published lesson path")
    items = packet["candidates"]
    if type(items) is not list or len(items) > 20:
        raise ValueError("expected at most 20 public candidates")
    seen = set()
    for item in items:
        if type(item) is not dict or set(item) != CANDIDATE_KEYS:
            raise ValueError("invalid public marker schema, free text forbidden")
        identifier = item["id"]
        if (type(identifier) is not str or IDENTIFIER.fullmatch(identifier) is None
                or identifier in seen):
            raise ValueError("invalid/duplicate candidate ID")
        seen.add(identifier)
        sources = item["source_ids"]
        markers = item["markers"]
        if (type(sources) is not list or not 1 <= len(sources) <= 8
                or any(type(s) is not str or REFERENCE.fullmatch(s) is None for s in sources)
                or len(set(sources)) != len(sources)):
            raise ValueError("invalid public source IDs")
        if (type(markers) is not list or not 1 <= len(markers) <= 6
                or any(type(s) is not str or MARKER.fullmatch(s) is None for s in markers)
                or len(set(s.casefold() for s in markers)) != len(markers)):
            raise ValueError("invalid search markers")
        if item["hypothesis_status"] != "UNVERIFIED_CANDIDATE":
            raise ValueError("semantic status cannot be assumed verified")


def _mentions(text: str, markers: list[str]) -> list[str]:
    lowered = text.casefold()
    return [m for m in markers if m.casefold() in lowered]


def compare_texts(packet: dict, atlas: str, article: str) -> dict:
    """Return grounded occurrence evidence, never an autonomous medical verdict."""
    _validate(packet)
    if type(atlas) is not str or type(article) is not str:
        raise ValueError("missing public prose")
    out = []
    for item in packet["candidates"]:
        markers = item["markers"]
        in_atlas = _mentions(atlas, markers)
        in_article = _mentions(article, markers)
        if in_article and not in_atlas:
            status = "ARTICLE_MENTION_ATLAS_ABSENT"
        elif in_atlas and in_article:
            status = "BOTH_MENTIONED"
        elif not in_article and not in_atlas:
            status = "SOURCE_ONLY_MARKER_CANDIDATE"
        else:
            status = "ATLAS_MENTION_DEEP_LESSON_ABSENT"
        out.append({
            "id": item["id"], "status": status,
            "article_markers_present": in_article,
            "atlas_markers_present": in_atlas,
            "source_ids": item["source_ids"],
            "new_concept_proven": False,
            "source_truth_verified": False,
            "next_step": "SEMANTIC_SCOPE_AND_SOURCE_REVIEW",
        })
    return {
        "schema": "ale-context-novelty-preflight-v0",
        "article_path": packet["article_path"], "atlas_path": ATLAS,
        "classification": "PUBLIC_SOURCE_LINKED_MARKERS",
        "candidates": out, "concept_promotions": 0,
        "private_data_accessed": False, "modified_public_content": False,
        "warning": "Literal occurrence is NOT semantic coverage, evidence validity, or Concept Family identity."
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    _validate(data)
    root = args.repo_root.resolve()
    atlas = (root / ATLAS).resolve(strict=True)
    article = (root / data["article_path"]).resolve(strict=True)
    for p in (atlas, article):
        if not p.is_relative_to(root):
            raise ValueError("public path escaped repository")
    result = compare_texts(data, atlas.read_text(encoding="utf-8"),
                           article.read_text(encoding="utf-8"))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
