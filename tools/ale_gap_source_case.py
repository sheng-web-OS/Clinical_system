#!/usr/bin/env python3
"""Run existing ALE gap triage on *public* PubMed-linked role annotations.

This is a safe adapter, not literature search, source verification or clinical
semantic inference. It must not receive user/Anki/Drive/private material.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

from ale_gap_triage import triage, GAP_KEYS

PMID = re.compile(r"pmid_[1-9][0-9]{6,8}\Z")


def triage_public_sources(packet: dict) -> dict:
    if type(packet) is not dict or set(packet) != {
            "source_classification", "max_active_research", "gaps"}:
        raise ValueError("invalid public source-linked packet schema")
    if packet["source_classification"] != "PUBLIC_SOURCE_LINKED":
        raise ValueError("owner-private/unclassified content is prohibited")
    gaps = packet["gaps"]
    if type(gaps) is not list:
        raise ValueError("invalid gap collection")
    safe_gaps, refs = [], {}
    for gap in gaps:
        if type(gap) is not dict or set(gap) != GAP_KEYS | {"source_ids"}:
            raise ValueError("unexpected source-linked gap fields; no private text")
        ids = gap["source_ids"]
        if (type(ids) is not list or not 1 <= len(ids) <= 8
                or any(type(x) is not str or PMID.fullmatch(x) is None for x in ids)
                or len(set(ids)) != len(ids)):
            raise ValueError("only nonduplicate public PubMed citation IDs permitted")
        if gap["origin"] == "SOURCE_CONTRADICTION" and len(ids) < 2:
            raise ValueError("claimed source disagreement needs at least two source IDs")
        safe_gaps.append({key:gap[key] for key in GAP_KEYS})
        refs[gap["id"]] = ids
    baseline = triage({
        "source_classification": "PUBLIC_SYNTHETIC_ONLY",
        "max_active_research": packet["max_active_research"],
        "gaps":safe_gaps,
    })
    baseline["classification"] = "PUBLIC_SOURCE_LINKED_METADATA_ONLY"
    baseline["source_research_status"] = (
        "MODEL_ANNOTATED_REFERENCES_NOT_INDEPENDENTLY_VERIFIED")
    for decision in baseline["decisions"]:
        decision["source_ids"] = refs[decision["id"]]
        decision["same_estimand_confirmed"] = False
        decision["literature_read_by_program"] = False
    return baseline


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, type=Path)
    args = ap.parse_args()
    packet = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(triage_public_sources(packet), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
