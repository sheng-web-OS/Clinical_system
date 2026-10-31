#!/usr/bin/env python3
"""ALE no-pre-ranked-impact, read-only source-linked concept graph gap probe.

This tool accepts model-authored bounded *typed relations*, not prose or
private records. It derives attention priority from graph structure and a
declared investigation focus, rather than taking caller-assigned CRITICAL /
BLOCKING impact labels. It does NOT extract medical semantics or verify sources.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TOKEN = re.compile(r"[a-z][a-z0-9_-]{2,63}\Z")
REF = re.compile(r"(?:ada_2026|ngsp_2026|ngsp_methods_2026|niddk_a1c|existing_dka_article|"
                 r"cdc_co_guidance_2026|fda_pulseox|pmid_[1-9][0-9]{6,8})\Z")
KINDS = {"MEASUREMENT", "INTERPRETATION", "CONTEXT", "DECISION", "MECHANISM"}
ROLES = {"VALIDITY_PREREQUISITE", "MEASUREMENT_INTERFERENCE",
         "BIOLOGICAL_MODIFIER", "DIAGNOSTIC_CONFIRMATION", "ASSOCIATION",
         "CONTRAST", "IS_A"}
STATES = {"EXISTING_CONTEXT", "CANDIDATE_CONTEXT", "EXTERNAL_ONLY"}
WEAK = {"ASSOCIATION", "CONTRAST", "IS_A"}
PK = {"source_classification", "focus", "nodes", "established_edges", "candidate_edges"}
NK = {"id", "kind", "status"}
EK = {"from", "to", "role"}
CK = EK | {"source_ids"}


def _valid_token(value: Any) -> bool:
    return type(value) is str and TOKEN.fullmatch(value) is not None


def _edge_key(edge: dict) -> tuple[str, str, str]:
    return edge["from"], edge["to"], edge["role"]


def _validate(packet: dict) -> dict[str, dict]:
    if type(packet) is not dict or set(packet) != PK:
        raise ValueError("invalid graph packet: only structured public-safe fields")
    if packet["source_classification"] != "PUBLIC_SOURCE_LINKED":
        raise ValueError("private and unclassified evidence is prohibited")
    if not _valid_token(packet["focus"]):
        raise ValueError("invalid focus")
    nodes = packet["nodes"]
    if type(nodes) is not list or not 2 <= len(nodes) <= 24:
        raise ValueError("invalid bounded nodes")
    known = {}
    for n in nodes:
        if type(n) is not dict or set(n) != NK or not _valid_token(n["id"]):
            raise ValueError("invalid node (free text forbidden)")
        if n["kind"] not in KINDS or n["status"] not in STATES:
            raise ValueError("invalid node classification")
        if n["id"] in known:
            raise ValueError("duplicate node")
        known[n["id"]] = n
    if packet["focus"] not in known:
        raise ValueError("unknown focus node")
    for field, keys, upper in (("established_edges", EK, 64), ("candidate_edges", CK, 24)):
        edges = packet[field]
        if type(edges) is not list or len(edges) > upper:
            raise ValueError("unbounded relation list")
        seen = set()
        for e in edges:
            if (type(e) is not dict or set(e) != keys
                    or e["from"] not in known or e["to"] not in known
                    or e["from"] == e["to"] or e["role"] not in ROLES):
                raise ValueError("invalid typed relation")
            key = _edge_key(e)
            if key in seen:
                raise ValueError("duplicate typed relation")
            seen.add(key)
            if field == "candidate_edges":
                refs = e["source_ids"]
                if (type(refs) is not list or not 1 <= len(refs) <= 8
                        or any(type(x) is not str or REF.fullmatch(x) is None for x in refs)
                        or len(set(refs)) != len(refs)):
                    raise ValueError("invalid public source identifiers")
    return known


def _reachable(start: str, goal: str, edges: list[dict], max_hops: int = 3) -> bool:
    frontier = {start}
    visited = {start}
    for _ in range(max_hops):
        neighbors = {e["to"] for e in edges if e["from"] in frontier
                     and e["role"] != "CONTRAST"}
        if goal in neighbors:
            return True
        frontier = neighbors - visited
        if not frontier:
            break
        visited.update(frontier)
    return False


def probe(packet: dict) -> dict:
    """Rank missing *relations*, not study topics or private learner needs."""
    nodes = _validate(packet)
    focus = packet["focus"]
    established = packet["established_edges"]
    existing = {_edge_key(e) for e in established}
    decisions = []
    for e in packet["candidate_edges"]:
        key = _edge_key(e)
        # The candidate graph annotations are a hypothesis, not a verified map.
        already = key in existing
        reach = (e["to"] == focus or
                 _reachable(e["to"], focus, established))
        relevant = (e["from"] == focus or e["to"] == focus or reach)
        if already:
            status = "EXISTING_RELATION"
            reason = "Exactly matching typed edge already present in context"
        elif not relevant:
            status = "PRESERVE_UNKNOWN"
            reason = "No supported path to declared focus within three hops"
        elif e["role"] in WEAK:
            status = "ABSTAIN_RELATION"
            reason = "Associative or hierarchical labels do not prove a missing inferential prerequisite"
        elif e["role"] in {"VALIDITY_PREREQUISITE", "DIAGNOSTIC_CONFIRMATION"}:
            status = "PRIORITY_RELATION_REVIEW"
            reason = "Missing proposed validity/confirmation premise on a focus-linked inference"
        else:
            status = "QUEUE_RELATION_REVIEW"
            reason = "Potential mechanism or measurement modifier; review separately"
        # This is structural attention order, not a clinical risk truth score.
        rank = (0 if status == "PRIORITY_RELATION_REVIEW"
                and e["role"] == "VALIDITY_PREREQUISITE" else
                1 if status == "PRIORITY_RELATION_REVIEW" else
                2 if status == "QUEUE_RELATION_REVIEW" else
                3 if status == "ABSTAIN_RELATION" else
                4 if status == "PRESERVE_UNKNOWN" else 5)
        relation_kind = (
            "LINK_EXISTING_CONTEXT" if nodes[e["from"]]["status"] == "EXISTING_CONTEXT"
            and nodes[e["to"]]["status"] == "EXISTING_CONTEXT"
            else "SOURCE_CONTEXT_EXTENSION_CANDIDATE"
        )
        decisions.append({
            "edge": {"from": e["from"], "to": e["to"], "role": e["role"]},
            "decision": status, "priority_order": rank,
            "context_operation_candidate": relation_kind,
            "reason": reason, "source_ids": e["source_ids"],
            "clinical_truth_verified": False,
            "source_read_by_program": False,
            "concept_promotion_authorized": False,
        })
    decisions.sort(key=lambda d: (d["priority_order"],
                                 d["edge"]["from"], d["edge"]["to"], d["edge"]["role"]))
    active = next((d for d in decisions if d["decision"] == "PRIORITY_RELATION_REVIEW"), None)
    return {
        "schema": "ale-unranked-gap-probe-v0",
        "focus": focus,
        "source_classification": "PUBLIC_SOURCE_LINKED_MODEL_ANNOTATIONS",
        "impact_labels_received": False,
        "most_urgent_candidate": active["edge"] if active else None,
        "candidates": decisions, "research_executed": False,
        "independent_source_qa": False,
        "medical_semantics_inferred_from_raw_prose": False,
        "concept_promotions": 0,
        "private_data_accessed": False,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, type=Path)
    args = ap.parse_args()
    packet = json.loads(args.input.read_text(encoding="utf8"))
    print(json.dumps(probe(packet), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
