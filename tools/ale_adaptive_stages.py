#!/usr/bin/env python3
"""Deterministic, read-only ALE stage selector for PUBLIC SYNTHETIC packets.

It selects one MCQ/CLOZE stage *within* a Concept note for next diagnostic
assessment; it does not author questions, inspect private records, schedule
FSRS/Anki, infer clinical facts, or certify durable learning.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TOKEN = re.compile(r"[a-z][a-z0-9_-]{1,63}\Z")
MODES = {"MCQ", "CLOZE", "NUMERIC", "TRANSFER", "EXPLANATION"}
OUTCOMES = {"PASS", "FAIL", "UNSURE"}
CONFIDENCES = {"CONFIDENT", "LOW", "GUESS"}
STAGE_KEYS = {"id", "mode", "requires"}
EVENT_KEYS = {"event_id", "stage_id", "item_id", "day_index", "outcome",
              "confidence", "unhinted", "learner_unseen", "reasoning_supported",
              "source_verified", "answer_exposed_before"}
PACKET_KEYS = {"classification", "concept_id", "stages", "evidence", "review_day"}


def _token(value: object, field: str) -> str:
    if type(value) is not str or TOKEN.fullmatch(value) is None:
        raise ValueError("invalid " + field)
    return value


def _day(value: object, field: str) -> int:
    if type(value) is not int or not 0 <= value <= 99999:
        raise ValueError("invalid " + field)
    return value


def validate(packet: dict) -> None:
    if type(packet) is not dict or set(packet) != PACKET_KEYS:
        raise ValueError("invalid packet shape or unclassified data")
    if packet["classification"] != "PUBLIC_SYNTHETIC_ONLY":
        raise ValueError("private learner data forbidden in public prototype")
    _token(packet["concept_id"], "concept_id")
    review_day = _day(packet["review_day"], "review_day")
    stages = packet["stages"]
    if type(stages) is not list or not 1 <= len(stages) <= 16:
        raise ValueError("stages must have 1 to 16 entries")
    stage_ids = set()
    for stage in stages:
        if type(stage) is not dict or set(stage) != STAGE_KEYS:
            raise ValueError("invalid stage shape")
        sid = _token(stage["id"], "stage.id")
        if sid in stage_ids:
            raise ValueError("duplicate stage id")
        if stage["mode"] not in MODES:
            raise ValueError("invalid stage mode")
        reqs = stage["requires"]
        if type(reqs) is not list or len(set(map(str, reqs))) != len(reqs):
            raise ValueError("invalid stage dependencies")
        for req in reqs:
            _token(req, "stage.requires")
            if req not in stage_ids:
                raise ValueError("dependencies must precede dependent stages")
        stage_ids.add(sid)

    events = packet["evidence"]
    if type(events) is not list or len(events) > 256:
        raise ValueError("evidence must be bounded list")
    event_ids = set()
    for event in events:
        if type(event) is not dict or set(event) != EVENT_KEYS:
            raise ValueError("invalid evidence shape; raw answers or personal data forbidden")
        eid = _token(event["event_id"], "event_id")
        if eid in event_ids:
            raise ValueError("duplicate event id")
        event_ids.add(eid)
        if _token(event["stage_id"], "event.stage_id") not in stage_ids:
            raise ValueError("event stage not present")
        _token(event["item_id"], "event.item_id")
        if _day(event["day_index"], "day_index") > review_day:
            raise ValueError("future evidence event")
        if event["outcome"] not in OUTCOMES or event["confidence"] not in CONFIDENCES:
            raise ValueError("invalid assessment roles")
        for key in ("unhinted", "learner_unseen", "reasoning_supported",
                    "source_verified", "answer_exposed_before"):
            if type(event[key]) is not bool:
                raise ValueError("invalid flag: " + key)


def _qualified(event: dict) -> bool:
    return (event["outcome"] == "PASS"
            and event["confidence"] == "CONFIDENT"
            and all(event[k] for k in ("unhinted", "learner_unseen",
                                        "reasoning_supported", "source_verified"))
            and not event["answer_exposed_before"])


def summarize(stages: list[dict], evidence: list[dict]) -> dict[str, dict]:
    grouped = {stage["id"]: [] for stage in stages}
    for event in evidence:
        grouped[event["stage_id"]].append(event)
    states = {}
    for stage in stages:
        sid = stage["id"]
        history = sorted(grouped[sid], key=lambda e: (e["day_index"], e["event_id"]))
        if not history:
            status = "NOT_OBSERVED"
        else:
            last = history[-1]
            if last["outcome"] == "FAIL":
                status = "OBSERVED_GAP"
            elif last["outcome"] == "UNSURE":
                status = "UNCERTAIN"
            elif not _qualified(last):
                status = "WEAK_PASS_NEEDS_DIAGNOSIS"
            else:
                # A delayed PASS needs a different, independently unseen item
                # at least one calendar day earlier; not a mastery claim.
                prior = any(_qualified(e) and e["day_index"] < last["day_index"]
                            and e["item_id"] != last["item_id"]
                            for e in history[:-1])
                status = "DELAYED_PASS_OBSERVED" if prior else "NEAR_PASS_OBSERVED"
        states[sid] = {"status": status,
                       "last_day": history[-1]["day_index"] if history else None,
                       "last_item_id": history[-1]["item_id"] if history else None,
                       "observed_events": len(history)}
    return states


def choose(packet: dict) -> dict:
    """Choose one informative stage; no unobserved stage becomes a pass.

    Explicit gaps outrank coverage checks; missing prerequisites to a failed
    target are inspected first. Otherwise fill unknown stages in dependency
    order, then run delayed rechecks when eligible, or defer to Anki/FSRS.
    """
    validate(packet)
    stages = packet["stages"]
    states = summarize(stages, packet["evidence"])
    by_id = {stage["id"]: stage for stage in stages}
    pass_states = {"NEAR_PASS_OBSERVED", "DELAYED_PASS_OBSERVED"}
    delay_states = {"NEAR_PASS_OBSERVED"}
    target = None
    reason = None

    def earliest_unsupported(root_id: str) -> str | None:
        for parent in by_id[root_id]["requires"]:
            upstream = earliest_unsupported(parent)
            if upstream:
                return upstream
            if states[parent]["status"] not in pass_states:
                return parent
        return None

    # A failure is real observed evidence but its underlying cause is unknown.
    for stage in stages:
        if states[stage["id"]]["status"] == "OBSERVED_GAP":
            upstream = earliest_unsupported(stage["id"])
            target = upstream or stage["id"]
            reason = "CHECK_UNSUPPORTED_PREREQUISITE" if upstream else "RECHECK_OBSERVED_GAP"
            break

    if target is None:
        for stage in stages:
            sid = stage["id"]
            if states[sid]["status"] in {"UNCERTAIN", "WEAK_PASS_NEEDS_DIAGNOSIS"}:
                target = earliest_unsupported(sid) or sid
                reason = "DIAGNOSE_UNCERTAIN_OR_EXPOSED_ANSWER"
                break

    if target is None:
        for stage in stages:
            sid = stage["id"]
            if states[sid]["status"] == "NOT_OBSERVED":
                target = earliest_unsupported(sid) or sid
                reason = "COVER_UNOBSERVED_STAGE"
                break

    if target is None:
        # Prefer the highest-level transfer check if its evidence is stale;
        # do not repeat same-day near passes simply to finish a card.
        eligible = [stage["id"] for stage in stages
                    if states[stage["id"]]["status"] in delay_states
                    and packet["review_day"] > states[stage["id"]]["last_day"]]
        if eligible:
            target = eligible[-1]
            reason = "DELAYED_UNSEEN_TRANSFER_PROBE"

    if target is None:
        action = "DEFER_TO_ANKI_FSRS"
    else:
        action = "ASSESS_ONE_STAGE"

    return {
        "schema": "ale-adaptive-stage-selection-v0",
        "classification": packet["classification"],
        "concept_id": packet["concept_id"],
        "stage_states": states,
        "decision": {"action": action, "stage_id": target,
                     "mode": by_id[target]["mode"] if target else None,
                     "reason_code": reason if target else "NO_DIAGNOSTIC_STAGE_DUE"},
        "assertion": "Selected test is a policy suggestion, not proven optimal.",
        "mastery_claim_authorized": False,
        "private_state_read": False,
        "anki_or_sheet_mutations": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    packet = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(choose(packet), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
