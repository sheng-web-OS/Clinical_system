#!/usr/bin/env python3
"""Compare two public-safe, versioned ALE concept-evidence snapshots.

This proposes decisions when evidence changes; it does not update learner memory,
certify semantic truth, mutate Concept Families or count agent-learning wins.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from ale_candidate_discovery import discover


def _sha256(packet: dict) -> str:
    data = json.dumps(packet, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _proposals(output: dict) -> dict[str, dict]:
    return {x["id"]: x for x in output["gate"]["results"]}


def _scopes(output: dict) -> dict[str, dict]:
    return {x["candidate_id"]: x for x in output["recursive_scope_refinements"]}


def compare_updates(before: dict, after: dict) -> dict:
    """Derive bounded changes. Do not interpret a changed policy as learned truth."""
    initial = discover(before)
    latest = discover(after)
    old, new = _proposals(initial), _proposals(latest)
    old_scopes, new_scopes = _scopes(initial), _scopes(latest)
    actions = []

    for cid in sorted(set(old) | set(new)):
        prior, current = old.get(cid), new.get(cid)
        if current is None:
            actions.append({"candidate_id": cid, "action": "WITHDRAW_PARENT_PROPOSAL",
                            "before": prior["status"], "after": "ABSENT"})
        elif prior is None:
            actions.append({"candidate_id": cid, "action": "NEW_PARENT_PROPOSAL",
                            "before": "ABSENT", "after": current["status"]})
        elif (prior["status"] != current["status"]
              or prior["blockers"] != current["blockers"]
              or prior["support_ids"] != current["support_ids"]
              or prior["counterexample_ids"] != current["counterexample_ids"]):
            actions.append({"candidate_id": cid, "action": "RECHECK_PARENT_EVIDENCE",
                            "before": prior["status"], "after": current["status"]})

    for cid in sorted(set(old_scopes) | set(new_scopes)):
        prior, current = old_scopes.get(cid), new_scopes.get(cid)
        if current is None:
            actions.append({"candidate_id": cid, "action": "WITHDRAW_SCOPE_HYPOTHESIS",
                            "previous_guard": prior["required_context_features"]})
        elif prior is None:
            actions.append({"candidate_id": cid, "action": "PROPOSE_SCOPED_HYPOTHESIS",
                            "proposed_guard": current["required_context_features"]})
        elif (prior["required_context_features"] != current["required_context_features"]
              or prior["known_excluded_counterexamples"]
              != current["known_excluded_counterexamples"]):
            actions.append({"candidate_id": cid, "action": "RECHECK_SCOPED_HYPOTHESIS",
                            "previous_guard": prior["required_context_features"],
                            "proposed_guard": current["required_context_features"]})

    before_sha, after_sha = _sha256(before), _sha256(after)
    state = ("NO_EVIDENCE_CHANGE" if before_sha == after_sha else
             "EVIDENCE_CHANGED_NO_DECISION_DELTA" if not actions else
             "REVIEW_CANDIDATE_UPDATES")
    return {
        "schema": "ale-learning-delta-v0",
        "state": state,
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "actions": actions,
        "action_count": len(actions),
        "learning_gain": "NOT_MEASURED",
        "independent_semantic_verification": False,
        "promotion_authorized": False,
        "memory_mutations_performed": 0,
        "actual_model_inference": False,
        "reason": "A changed structured proposal is not independently verified learning."
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--before", required=True, type=Path)
    ap.add_argument("--after", required=True, type=Path)
    opts = ap.parse_args()
    before = json.loads(opts.before.read_text(encoding="utf-8"))
    after = json.loads(opts.after.read_text(encoding="utf-8"))
    print(json.dumps(compare_updates(before, after), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
