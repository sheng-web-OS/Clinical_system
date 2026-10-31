#!/usr/bin/env python3
"""Read-only, fail-closed reconciliation for the GitHub shadow dispatcher.

This makes no API/model calls and performs no writes. Gate observations MUST
be assembled from fresh, independently checked Issue/PR/CI facts; they are
untrusted assertions until the ChatGPT worker independently verifies them.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from tools.dispatch_selector import DispatchError, load_manifest, select_tasks

GATE_STATES = {"actionable", "waiting", "complete", "approval_needed"}
OWNERS = {"unclaimed", "dispatcher", "other_worker"}
RECEIPT_STATES = {
    "CONTINUING", "HANDOFF_ACTIVE_WRITER", "VERIFIED_COMPLETE",
    "APPROVAL_NEEDED", "SECURITY_HOLD", "BLOCKED"
}
GATE_FIELDS = {"issue_number", "gate_id", "evidence_revision",
               "gate_state", "owner", "last_receipt"}
RECEIPT_FIELDS = {"gate_id", "fingerprint", "status", "next_gate_id"}
GATE_ID = re.compile(r"[a-z][a-z0-9-]{2,100}")
REVISION = re.compile(r"(?:sha:[a-f0-9]{40}|artifacts:[a-f0-9]{64}|comment:[1-9][0-9]*|ci:[1-9][0-9]*:[a-f0-9]{40})")


def require(condition, code):
    if not condition:
        raise DispatchError(code)


def gate_fingerprint(target, gate_id, evidence_revision):
    """Stable across wake-ups; changes ONLY for real next steps / new evidence."""
    return hashlib.sha256(
        json.dumps([target, gate_id, evidence_revision],
                   separators=(",", ":"), ensure_ascii=True).encode()
    ).hexdigest()


def validate_gate(target, gate):
    require(type(gate) is dict and set(gate) == GATE_FIELDS,
            "INVALID_GATE_SCHEMA")
    require(type(gate["issue_number"]) is int and
            gate["issue_number"] == int(target.split(":")[1]),
            "GATE_TARGET_MISMATCH")
    require(type(gate["gate_id"]) is str and
            GATE_ID.fullmatch(gate["gate_id"]) is not None,
            "INVALID_GATE_ID")
    require(type(gate["evidence_revision"]) is str and
            REVISION.fullmatch(gate["evidence_revision"]) is not None,
            "INVALID_EVIDENCE_REVISION")
    require(type(gate["gate_state"]) is str and
            gate["gate_state"] in GATE_STATES and
            type(gate["owner"]) is str and gate["owner"] in OWNERS,
            "INVALID_GATE_STATE")
    receipt = gate["last_receipt"]
    if receipt is not None:
        require(type(receipt) is dict and set(receipt) == RECEIPT_FIELDS,
                "INVALID_RECEIPT_SCHEMA")
        require(type(receipt["gate_id"]) is str and
                GATE_ID.fullmatch(receipt["gate_id"]) is not None and
                type(receipt["fingerprint"]) is str and
                re.fullmatch(r"[a-f0-9]{64}", receipt["fingerprint"])
                and type(receipt["status"]) is str and
                receipt["status"] in RECEIPT_STATES and
                (receipt["next_gate_id"] is None or
                 (type(receipt["next_gate_id"]) is str and
                  GATE_ID.fullmatch(receipt["next_gate_id"]) is not None)),
                "INVALID_RECEIPT_VALUES")
    current_fingerprint = gate_fingerprint(
        target, gate["gate_id"], gate["evidence_revision"])
    # A receipt claiming completion of *this* gate must identify this gate.
    # Do not reject a historical receipt for an earlier fingerprint: it may
    # legitimately name the previous gate of a CONTINUING handoff.
    if receipt is not None and receipt["fingerprint"] == current_fingerprint:
        require(receipt["gate_id"] == gate["gate_id"],
                "INVALID_RECEIPT_VALUES")
    return current_fingerprint


def reconcile(config, issue_snapshot, gate_snapshot):
    """Plan ONLY. Never turns a GitHub observation into an authorization."""
    # Global configuration/source-shape failures stop the plan. An unavailable
    # single Issue/gate must not starve unrelated, independently verified work.
    require(type(issue_snapshot) is dict, "INVALID_ISSUE_SNAPSHOT")
    require(type(gate_snapshot) is dict, "GATE_SNAPSHOT_MISSING")
    expected = {t["target"] for t in config["tasks"] if t["enabled"]}
    require(set(gate_snapshot).issubset(expected), "UNEXPECTED_GATE_TARGET")
    eligible, skipped, blocked = [], [], []
    tasks = sorted(config["tasks"], key=lambda t: (-t["priority"], t["id"]))
    for task in tasks:
        try:
            single = dict(config, tasks=[task])
            preliminary = select_tasks(single, issue_snapshot)
            skipped.extend(preliminary["skipped"])
            if not preliminary["candidates"]:
                continue
            require(task["target"] in gate_snapshot, "GATE_SNAPSHOT_MISSING")
            gate = gate_snapshot[task["target"]]
            fingerprint = validate_gate(task["target"], gate)
        except DispatchError as exc:
            blocked.append({"id": task["id"], "reason": str(exc)})
            continue
        target = task["target"]
        why = None
        if gate["owner"] == "other_worker":
            why = "ACTIVE_OTHER_OWNER"
        elif gate["gate_state"] == "waiting":
            why = "WAITING_NO_NEW_GATE"
        elif gate["gate_state"] == "complete":
            why = "GATE_COMPLETE"
        elif gate["gate_state"] == "approval_needed":
            why = "APPROVAL_NEEDED"
        receipt = gate["last_receipt"]
        if not why and receipt and receipt["fingerprint"] == fingerprint:
            why = ("ALREADY_VERIFIED" if
                   receipt["status"] == "VERIFIED_COMPLETE"
                   else "DUPLICATE_UNCHANGED_GATE")
        if why:
            skipped.append({"id": task["id"], "reason": why})
            continue
        # A genuine resume is the next STEP of a prior incomplete job, not
        # repeatedly doing the same step because the issue is still open.
        resumed = bool(receipt and receipt["status"] == "CONTINUING" and
                       receipt["next_gate_id"] == gate["gate_id"] and
                       receipt["gate_id"] != gate["gate_id"])
        eligible.append({
            "id": task["id"], "target": target, "kind": task["kind"],
            "priority": task["priority"], "gate_id": gate["gate_id"],
            "fingerprint": fingerprint,
            "decision": "RESUME_NEXT_GATE" if resumed else "NEW_GATE",
        })
    # Delivery-first tie-break for independently observed next steps: keep
    # priority-100 P0 gates ahead of all lower-severity work, then prefer a
    # genuine RESUME_NEXT_GATE over starting another non-P0 workstream.
    # This remains a shadow plan, not evidence of completion or permission.
    eligible.sort(key=lambda item: (
        0 if item["priority"] == 100 else 1,
        0 if item["decision"] == "RESUME_NEXT_GATE" else 1,
        -item["priority"], item["id"]))
    return {"status": ("HOLD_TASKS_BLOCKED" if blocked and not eligible
                       else "SHADOW_RECONCILED_NO_ACTION"),
            "execution_authorized": False, "model_calls": 0,
            "write_actions": 0, "selected": eligible[:1],
            "eligible_count": len(eligible), "skipped": skipped,
            "blocked": blocked, "all_tasks_observed": not blocked,
            "requires_live_source_verification": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default="ops/dispatch.json")
    parser.add_argument("--issues", required=True,
                        help="Fresh issue metadata snapshot, as for dispatch_selector")
    parser.add_argument("--gates", required=True,
                        help="Fresh, verified Issue/PR/CI gate+receipt observations")
    args = parser.parse_args()
    try:
        config = load_manifest(args.manifest)
        issues = json.loads(Path(args.issues).read_text(encoding="utf-8"))
        gates = json.loads(Path(args.gates).read_text(encoding="utf-8"))
        result = reconcile(config, issues, gates)
    except (DispatchError, OSError, ValueError, TypeError) as exc:
        reason = str(exc) if isinstance(exc, DispatchError) else "INVALID_INPUT"
        print(json.dumps({"status": "HOLD", "reason": reason}))
        return 2
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
