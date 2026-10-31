#!/usr/bin/env python3
"""Read-only, one-question-or-abstain gate for saved ALE candidate memory.

This is a deterministic, public-safe *shadow* triage aid, NOT autonomous
semantic inference, clinical advice, automatic prompt injection or promotion.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from ale_learning_checkpoint import load, validate

ROLE = re.compile(r"[a-z][a-z0-9_]{1,63}")
SIGNATURE_FIELDS = ("from_role", "to_role", "missing_bridge_role")
PUBLIC_INPUTS = {"PUBLIC_SYNTHETIC_ONLY", "PUBLIC_SOURCE_LINKED"}


def _role(value: Any) -> bool:
    return type(value) is str and ROLE.fullmatch(value) is not None


def _roles(value: Any, field: str) -> list[str]:
    if (type(value) is not list or len(value) > 16
            or any(not _role(x) for x in value)
            or len(set(value)) != len(value)):
        raise ValueError("invalid bounded role list: " + field)
    return value


def _signature(value: Any) -> dict:
    if (type(value) is not dict or set(value) != set(SIGNATURE_FIELDS)
            or any(not _role(value[k]) for k in SIGNATURE_FIELDS)):
        raise ValueError("invalid reasoning signature")
    return value


def probe_next_q0(state: dict, point: dict) -> dict:
    """Return at most one conditional question, or explicitly abstain.

    All role annotations and materiality come from the caller. The checkpoint
    supplies a previously retained, unverified scope hypothesis. No real-world
    evidence or causal consequences are independently verified here.
    """
    validate(state)
    if type(point) is not dict or set(point) != {
            "source_classification", "phase", "materiality",
            "reasoning_signature", "original_question_roles"}:
        raise ValueError("invalid decision-point schema")
    if point["source_classification"] not in PUBLIC_INPUTS:
        raise ValueError("private or unclassified decision input is prohibited")
    if point["phase"] not in ("PRE_ACTION", "POST_ACTION"):
        raise ValueError("invalid decision phase")
    if point["materiality"] not in ("MATERIAL", "LOW"):
        raise ValueError("invalid decision materiality")
    signature = _signature(point["reasoning_signature"])
    originally_asked = set(_roles(point["original_question_roles"],
                                  "original_question_roles"))
    abstain = {
        "decision": "ABSTAIN", "verified": False, "promotion_authorized": False,
        "checkpoint_sha256": state["checkpoint_sha256"],
    }
    if point["phase"] != "PRE_ACTION" or point["materiality"] != "MATERIAL":
        return dict(abstain, reason="NOT_A_MATERIAL_PRE_ACTION_BOUNDARY")
    saved = state.get("candidate_memory", {})
    if saved.get("state") != "PUBLIC_CANDIDATE_SNAPSHOT_UNVERIFIED":
        return dict(abstain, reason="NO_PUBLIC_CANDIDATE_MEMORY")
    candidates = saved.get("candidates")
    if type(candidates) is not list:
        raise ValueError("invalid saved candidate list")
    possible = []
    for candidate in candidates:
        if type(candidate) is not dict:
            raise ValueError("invalid candidate")
        if candidate.get("reasoning_signature") != signature:
            continue
        # A known scoped counterexample is needed. Unscoped analogies abstain.
        guard = _roles(candidate.get("scope_guard"), "scope_guard")
        if (not guard or candidate.get("promotion_authorized") is not False
                or candidate.get("scope_verified") is not False
                or type(candidate.get("support_family_count")) is not int
                or candidate["support_family_count"] < 2):
            continue
        still_unasked = [x for x in guard if x not in originally_asked]
        if still_unasked:
            possible.append((candidate.get("candidate_id", ""),
                             still_unasked[0]))
    if not possible:
        return dict(abstain, reason="NO_UNASKED_DECISION_CRITICAL_GUARD")
    # Stable deterministic choice; no expensive retrieval cascade.
    candidate_id, guard_role = sorted(possible)[0]
    if not _role(guard_role) or type(candidate_id) is not str:
        raise ValueError("invalid candidate reference")
    return {
        "decision": "PROPOSE_ONE_Q0_SHADOW",
        "question_q0": (
            "Before acting, does '" + guard_role + "' hold, and would the "
            "inference from '" + signature["from_role"] + "' to '"
            + signature["to_role"] + "' change if it did not?"
        ),
        "candidate_id": candidate_id,
        "unasked_guard_role": guard_role,
        "predicted_effect_if_absent": "REOPEN_OR_DEFER_PARENT_INFERENCE",
        "predicted_effect_if_present": "REVIEW_CONDITIONAL_BRIDGE_EVIDENCE",
        "basis": "CALLER_ANNOTATIONS_PLUS_UNVERIFIED_SAVED_SCOPE",
        "verified": False,
        "promotion_authorized": False,
        "checkpoint_sha256": state["checkpoint_sha256"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--decision-point", type=Path, required=True)
    args = parser.parse_args()
    point = json.loads(args.decision_point.read_text(encoding="utf-8"))
    print(json.dumps(probe_next_q0(load(args.checkpoint), point),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
