#!/usr/bin/env python3
"""Bounded, read-only ALE knowledge-gap research triage.

Operates ONLY on public-safe abstract role tokens. It does not read private
learner records, infer medical truth from tags, open sources, or authorize
clinical decisions / publication / changes to Anki.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TOKEN = re.compile(r"[a-z][a-z0-9_-]{1,63}\Z")
ORIGINS = {
    "SOURCE_CONTRADICTION", "REASONING_FAILURE", "MISSING_PREREQUISITE",
    "COVERAGE_GAP", "TAG_ONLY", "PASSIVE_READING", "REVIEW_RATING_ONLY",
}
IMPACTS = {"CRITICAL", "BLOCKING", "TRANSFER", "LOW"}
SCOPES = {"CURRENT", "NEARBY", "OUT_OF_SCOPE"}
SOURCE_STATES = {"SOURCE_ATTESTED", "PENDING", "ABSENT"}
EFFORTS = {"SMALL", "LARGE", "UNKNOWN"}
WEAK_OBSERVATIONS = {"TAG_ONLY", "PASSIVE_READING", "REVIEW_RATING_ONLY"}
GAP_KEYS = {"id", "origin", "impact", "scope", "source_state",
            "linked_family_count", "research_effort"}
IMPACT_RANK = {"CRITICAL": 0, "BLOCKING": 1, "TRANSFER": 2, "LOW": 3}
EFFORT_RANK = {"SMALL": 0, "UNKNOWN": 1, "LARGE": 2}


def _validate(gaps: object) -> list[dict]:
    if type(gaps) is not list or len(gaps) > 32:
        raise ValueError("gaps must be a bounded list (at most 32)")
    known = set()
    for gap in gaps:
        if type(gap) is not dict or set(gap) != GAP_KEYS:
            raise ValueError("invalid gap schema; no unclassified text or private data")
        gid = gap["id"]
        if type(gid) is not str or TOKEN.fullmatch(gid) is None or gid in known:
            raise ValueError("invalid or duplicate gap id")
        known.add(gid)
        for key, values in (
            ("origin", ORIGINS), ("impact", IMPACTS), ("scope", SCOPES),
            ("source_state", SOURCE_STATES), ("research_effort", EFFORTS),
        ):
            if type(gap[key]) is not str or gap[key] not in values:
                raise ValueError("invalid role: " + key)
        reach = gap["linked_family_count"]
        if type(reach) is not int or not 0 <= reach <= 16:
            raise ValueError("invalid linked_family_count")
    return gaps


def _priority(gap: dict) -> tuple:
    # Ordering is a declared, unvalidated initial policy; NOT a causal score.
    return (IMPACT_RANK[gap["impact"]],
            0 if gap["scope"] == "CURRENT" else 1,
            -gap["linked_family_count"],
            EFFORT_RANK[gap["research_effort"]], gap["id"])


def triage(packet: dict) -> dict:
    """Sort evidence-annotated gaps into action, queue, uncertainty, or diagnostic.

    CRITICAL items that exceed the one active research slot remain explicit
    unresolved holds, never silently demoted to harmless unknowns.
    """
    if type(packet) is not dict or set(packet) != {
            "source_classification", "gaps", "max_active_research"}:
        raise ValueError("invalid public-safe packet")
    if packet["source_classification"] != "PUBLIC_SYNTHETIC_ONLY":
        raise ValueError("private or unreviewed real-world packets forbidden")
    capacity = packet["max_active_research"]
    if type(capacity) is not int or not 0 <= capacity <= 3:
        raise ValueError("invalid research capacity")
    gaps = _validate(packet["gaps"])
    active = 0
    decisions = []
    for gap in sorted(gaps, key=_priority):
        origin, impact, scope = gap["origin"], gap["impact"], gap["scope"]
        if origin in WEAK_OBSERVATIONS:
            decision, reason = ("DIAGNOSTIC_FIRST",
                "Metadata or activity is not evidence of a conceptual or medical gap")
        elif scope == "OUT_OF_SCOPE" and impact == "CRITICAL":
            decision, reason = ("SCOPE_CONFLICT_HOLD",
                "Declared critical risk conflicts with out-of-scope classification")
        elif scope == "OUT_OF_SCOPE" or impact == "LOW":
            decision, reason = ("PRESERVE_UNKNOWN",
                "No current decision-relevant reason to spend scarce research effort")
        elif impact in {"CRITICAL", "BLOCKING"}:
            if active < capacity:
                decision, reason = ("RESEARCH_NOW",
                    "A current safety-relevant or inference-blocking gap needs investigation")
                active += 1
            elif impact == "CRITICAL":
                decision, reason = ("CRITICAL_UNRESOLVED_HOLD",
                    "Critical uncertainty exceeds current research capacity; do not proceed")
            else:
                decision, reason = ("QUEUE_RESEARCH",
                    "Blocking gap awaits capacity; original inference remains unverified")
        elif impact == "TRANSFER" and gap["linked_family_count"] >= 2:
            decision, reason = ("QUEUE_RESEARCH",
                "Potential cross-family transfer value warrants later source checking")
        else:
            decision, reason = ("PRESERVE_UNKNOWN",
                "No sufficient present impact or cross-family leverage")
        next_gate = (
            "OBSERVE_DISCRIMINATING_ANSWER_OR_QUESTION"
            if decision == "DIAGNOSTIC_FIRST"
            else "RECONCILE_SCOPE_BEFORE_ACTION"
            if decision == "SCOPE_CONFLICT_HOLD"
            else "REQUIRE_SOURCE_VERIFICATION"
            if decision in {"RESEARCH_NOW", "QUEUE_RESEARCH",
                            "CRITICAL_UNRESOLVED_HOLD"}
            else "REOPEN_ON_MATERIAL_NEW_EVIDENCE"
        )
        decisions.append({
            "id": gap["id"], "decision": decision, "reason": reason,
            "next_gate": next_gate, "source_state": gap["source_state"],
            "source_verified_independently": False,
            "ontology_mutation_authorized": False,
        })
    return {
        "schema": "ale-gap-triage-v0",
        "classification": "PUBLIC_SYNTHETIC_ONLY",
        "policy_status": "DETERMINISTIC_UNVALIDATED_BASELINE",
        "decisions": decisions,
        "active_research": active,
        "critical_unresolved": sum(d["decision"] in {
            "CRITICAL_UNRESOLVED_HOLD", "SCOPE_CONFLICT_HOLD"}
                                   for d in decisions),
        "concept_promotions": 0,
        "personal_state_accessed": False,
        "external_research_executed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    packet = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(triage(packet), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
