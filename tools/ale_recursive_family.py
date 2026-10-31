#!/usr/bin/env python3
"""Public-safe, deterministic gate for AI-proposed higher-order Concept Families.

This does NOT infer semantic truth, inspect private learner data, approve clinical
claims, rewrite concept graphs, or promote candidates. It challenges proposals
against explicit evidence and traces possible downstream dependencies.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

MAX_DEPTH = 3


def _required(obj: dict, key: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"missing or invalid {key}")
    return value.strip()


def _ids(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(v, str) or not v for v in value):
        raise ValueError(f"{field} must be a list of nonempty strings")
    if len(set(value)) != len(value):
        raise ValueError(f"{field} contains duplicate IDs")
    return value


def dependency_impact(start_ids: list[str], nodes: list[dict], max_depth: int = MAX_DEPTH) -> list[dict]:
    """Return possible dependents, not an assertion that a conclusion is false."""
    reverse: dict[str, set[str]] = defaultdict(set)
    for node in nodes:
        node_id = _required(node, "id")
        for prerequisite in _ids(node.get("depends_on", []), "depends_on"):
            reverse[prerequisite].add(node_id)
    frontier = deque((item, 0) for item in start_ids)
    seen = set(start_ids)
    impacted: list[dict] = []
    while frontier:
        current, depth = frontier.popleft()
        if depth >= max_depth:
            continue
        for dependent in sorted(reverse.get(current, set())):
            if dependent in seen:
                continue
            seen.add(dependent)
            impacted.append({"claim_id": dependent, "depth": depth + 1,
                             "action": "RECHECK_NOT_AUTO_INVALIDATE"})
            frontier.append((dependent, depth + 1))
    return impacted


def evaluate(packet: dict) -> dict:
    """Propose, falsify, and scope-check. Never emit PROMOTED or mastery claims."""
    if not isinstance(packet, dict):
        raise ValueError("input must be a JSON object")
    observations = packet.get("observations", [])
    proposals = packet.get("proposals", [])
    dependencies = packet.get("dependencies", [])
    if not all(isinstance(x, list) for x in (observations, proposals, dependencies)):
        raise ValueError("observations, proposals, dependencies must be lists")

    evidence: dict[str, dict] = {}
    for obs in observations:
        if not isinstance(obs, dict):
            raise ValueError("observation must be an object")
        oid = _required(obs, "id")
        _required(obs, "family_id")
        _required(obs, "pattern")
        if obs.get("role", "support") not in ("support", "counterexample"):
            raise ValueError("observation role must be support or counterexample")
        if oid in evidence:
            raise ValueError("duplicate observation id")
        evidence[oid] = obs

    results = []
    for proposal in proposals:
        if not isinstance(proposal, dict):
            raise ValueError("proposal must be an object")
        pid = _required(proposal, "id")
        pattern = _required(proposal, "pattern")
        label = _required(proposal, "label")
        boundary = _required(proposal, "boundary")
        case_ids = _ids(proposal.get("support_ids", []), "support_ids")
        acknowledged = _ids(proposal.get("acknowledged_counterexample_ids", []),
                            "acknowledged_counterexample_ids")
        blockers: list[str] = []
        missing = [oid for oid in case_ids + acknowledged if oid not in evidence]
        if missing:
            blockers.append("UNKNOWN_EVIDENCE_ID")
        supports = [evidence[oid] for oid in case_ids if oid in evidence]
        family_ids = sorted({s["family_id"] for s in supports
                             if s.get("role", "support") == "support"
                             and s["pattern"] == pattern})
        if len(family_ids) < 2:
            blockers.append("INSUFFICIENT_DISTINCT_FAMILIES")
        if any(s.get("role", "support") != "support" or s["pattern"] != pattern for s in supports):
            blockers.append("UNRELATED_OR_NEGATIVE_SUPPORT")
        if any(not s.get("source_ref") or s.get("source_check") != "checked" for s in supports):
            blockers.append("SUPPORT_SOURCE_NOT_CHECKED")

        counters = [obs for obs in observations
                    if obs["pattern"] == pattern and obs.get("role") == "counterexample"]
        missing_counters = sorted(c["id"] for c in counters if c["id"] not in acknowledged)
        if missing_counters:
            blockers.append("UNADDRESSED_COUNTEREXAMPLE")
        acknowledged_obs = [evidence[oid] for oid in acknowledged if oid in evidence]
        if any(c.get("role") != "counterexample" or c["pattern"] != pattern
               for c in acknowledged_obs):
            blockers.append("INVALID_COUNTEREXAMPLE_ACKNOWLEDGEMENT")
        if any(not c.get("source_ref") or c.get("source_check") != "checked"
               for c in acknowledged_obs):
            blockers.append("COUNTEREXAMPLE_SOURCE_NOT_CHECKED")
        if not case_ids:
            blockers.append("NO_SUPPORT")

        if blockers:
            status = "HOLD_REVISION_REQUIRED"
        elif acknowledged:
            status = "CHALLENGED_PENDING_INDEPENDENT_QA"
        else:
            status = "PROPOSED_PENDING_INDEPENDENT_QA"
        results.append({
            "id": pid, "label": label, "pattern": pattern, "boundary": boundary,
            "status": status, "blockers": sorted(set(blockers)),
            "supporting_families": family_ids,
            "support_ids": case_ids, "counterexample_ids": sorted(c["id"] for c in counters),
            "unaddressed_counterexamples": missing_counters,
            "proposed_parent_id": "candidate/" + pid,
            "proposed_links": [{"family_id": family_id, "relation": "PROPOSED_EXPLAINS"}
                               for family_id in family_ids] if not blockers else [],
            "dependency_recheck": dependency_impact(case_ids, dependencies) if not blockers else [],
            "promotion_authorized": False,
            "reason": "Source-check flags are input assertions, not independent verification."
        })
    return {
        "schema": "ale-recursive-family-v0",
        "classification": "PUBLIC_SYNTHETIC_ONLY",
        "results": results,
        "mutations_performed": 0,
        "private_learner_state_read": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Public-safe JSON packet")
    args = parser.parse_args()
    packet = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(evaluate(packet), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
