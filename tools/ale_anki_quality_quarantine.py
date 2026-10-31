#!/usr/bin/env python3
"""Owner-Mac Anki quality quarantine, strictly scoped and reversible.

Stage 1: explicit owner red flag -> suspend that exact card, never a sibling.
Stage 2: independently validated private AI card-quality decision -> set red flag
and suspend, if AnkiConnect supports setFlag. No content writes, auto-unsuspend,
FSRS edits, deck edits, answer ratings, or public private-data transfer.

The module is NOT an AI classifier: it enforces verified, identity-matched
decisions from a separate authorized private reviewer.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.request

from ale_anki_readonly import check_version, invoke, ENDPOINT, API_VERSION
from ale_anki_drive_sync import BASE, private_dir, private_write, load_json
from ale_anki_flag_feedback import read_flagged_cards

DECISION_PATH = BASE / "quality_quarantine_decisions.json"
AUDIT_PATH = BASE / "quality_quarantine_receipts.json"
BASELINE_PATH = BASE / "quality_red_flags_seen.json"
VALID_REASONS = frozenset({
    "BROKEN_PROMPT", "EMPTY_ANSWER", "AMBIGUOUS_PROMPT",
    "MULTIPLE_INFERENCES", "QUESTION_ANSWER_MISMATCH", "VERIFIED_FACT_ERROR",
    "DUPLICATE_INFERENCE", "LOW_YIELD_CONTENT",
})
MAX_PER_RUN = 20

def write_action(action: str, **params):
    if action not in {"suspend", "setFlag"}:
        raise ValueError("Anki write action not authorized")
    card_ids = params.get("cards")
    if not isinstance(card_ids, list) or len(card_ids) != 1 or type(card_ids[0]) is not int or card_ids[0] <= 0:
        raise ValueError("Exact one-card operation required")
    if action == "setFlag" and params.get("flag") != 1:
        raise ValueError("Only red quality flag is authorized")
    payload = {"action": action, "version": API_VERSION, "params": params}
    if os.environ.get("ANKI_CONNECT_API_KEY"):
        payload["key"] = os.environ["ANKI_CONNECT_API_KEY"]
    req = urllib.request.Request(
        ENDPOINT, method="POST", data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=12) as response:
        result = json.load(response)
    if not isinstance(result, dict) or result.get("error") is not None or "result" not in result:
        raise RuntimeError("Anki refused scoped quality action")
    return result["result"]

def check_card(cid: int, expected_note: int | None = None) -> dict:
    cards = invoke("cardsInfo", cards=[cid])
    if not isinstance(cards, list) or len(cards) != 1 or cards[0].get("cardId") != cid:
        raise RuntimeError("Card identity changed; no mutation")
    c = cards[0]
    if type(c.get("note")) is not int or (expected_note is not None and c["note"] != expected_note):
        raise RuntimeError("Note identity changed; no mutation")
    return c

def is_suspended(cid: int) -> bool:
    # is:suspended is Anki search syntax; no raw scheduler fields touched.
    matches = invoke("findCards", query="is:suspended")
    if not isinstance(matches, list):
        raise RuntimeError("Suspended state unverified")
    return cid in matches

def card_content_fingerprint(c: dict) -> str:
    # Never print/share card contents. Bind an agent decision to the exact
    # privately reviewed card rendering to prevent stale-decision suspension.
    return hashlib.sha256(json.dumps(
        {"question": c.get("question"), "answer": c.get("answer")},
        sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

def approved_decisions(payload: dict) -> list[dict]:
    if not payload:
        return []
    if payload.get("schema") != 1 or not isinstance(payload.get("decisions"), list):
        raise RuntimeError("Private decision input invalid")
    found = set()
    approved = []
    for d in payload["decisions"]:
        if not isinstance(d, dict) or d.get("decision") != "QUALITY_QUARANTINE":
            continue
        cid, nid = d.get("anki_card_id"), d.get("anki_note_id")
        if type(cid) is not int or type(nid) is not int or cid <= 0 or nid <= 0:
            raise RuntimeError("Unverified private decision identity")
        if cid in found:
            raise RuntimeError("Duplicate private quality decisions")
        found.add(cid)
        if (d.get("reason_code") not in VALID_REASONS or
            d.get("evidence_state") != "INDEPENDENTLY_REVIEWED" or
            not isinstance(d.get("evidence_ref"), str) or not d["evidence_ref"].strip() or
            not isinstance(d.get("content_sha256"), str) or
            len(d["content_sha256"]) != 64 or
            any(ch not in "0123456789abcdef" for ch in d["content_sha256"])):
            raise RuntimeError("No qualified independent quality diagnosis")
        approved.append(d)
    if len(approved) > MAX_PER_RUN:
        raise RuntimeError("Too many approved quality decisions per run")
    return approved

def apply(base: Path, *, dry_run=True) -> dict:
    check_version()
    # First run a single-card-only plan; red flags are explicit owner signals
    # even if no review buttons have been pressed.
    flagged = read_flagged_cards()
    # One-time baseline prevents mass suspension of historic non-quality flags.
    # Subsequent newly observed red flags are explicit owner quality gestures.
    seen_path = base / BASELINE_PATH.name
    had_snapshot = seen_path.exists()
    seen = load_json(seen_path)
    if seen and (seen.get("schema") != 1 or not isinstance(seen.get("flagged_ids"), list)
                 or any(not str(x).isdigit() for x in seen["flagged_ids"])):
        raise RuntimeError("Invalid private red-flag baseline")
    previously_flagged = set(str(x) for x in seen.get("flagged_ids", []))
    new_owner_flags = flagged if had_snapshot else {}
    new_owner_flags = {cid: note for cid, note in new_owner_flags.items()
                       if cid not in previously_flagged}
    decisions = approved_decisions(load_json(base / DECISION_PATH))
    candidates: dict[int, dict] = {int(cid): {"note": note, "owner_red_flag": True}
                                  for cid, note in new_owner_flags.items()}
    for d in decisions:
        cid = d["anki_card_id"]
        if cid in candidates and candidates[cid]["note"] != d["anki_note_id"]:
            raise RuntimeError("Owner flag/AI note collision")
        candidates[cid] = {"note": d["anki_note_id"], "decision": d,
                           "owner_red_flag": cid in candidates}
    if len(candidates) > MAX_PER_RUN:
        # Do not silently leave arbitrary red flags in rotation; batch next run.
        candidates = dict(sorted(candidates.items())[:MAX_PER_RUN])
    actionable = []
    already_suspended = 0
    for cid, entry in candidates.items():
        card = check_card(cid, entry["note"])
        if "decision" in entry and card_content_fingerprint(card) != entry["decision"]["content_sha256"]:
            raise RuntimeError("Stale quality decision; no mutation")
        if is_suspended(cid):
            already_suspended += 1
            continue
        if not entry["owner_red_flag"] and card.get("flags", 0) not in (0, 1):
            raise RuntimeError("Different existing flag must not be overwritten")
        actionable.append((cid, entry))
    if dry_run:
        return {"eligible_to_quarantine": len(actionable),
                "already_suspended": already_suspended, "applied": 0}
    private_dir(base)
    audit = load_json(base / AUDIT_PATH)
    if audit and (audit.get("schema") != 1 or not isinstance(audit.get("actions"), list)):
        raise RuntimeError("Invalid owner-private quality audit")
    actions = list(audit.get("actions", []))
    applied = 0
    for cid, entry in actionable:
        if not entry["owner_red_flag"]:
            # AI proactively chooses RED; only after an independently reviewed
            # version-locked private decision. If unavailable, fail closed.
            write_action("setFlag", cards=[cid], flag=1)
            if check_card(cid, entry["note"]).get("flags") != 1:
                raise RuntimeError("AI red flag not confirmed")
        write_action("suspend", cards=[cid])
        if not is_suspended(cid):
            raise RuntimeError("Anki quarantine not confirmed")
        actions.append({"card_id": cid, "note_id": entry["note"],
                        "reason": "OWNER_RED_FLAG" if entry["owner_red_flag"] else
                                  entry["decision"]["reason_code"],
                        "action": "SUSPENDED_PENDING_REVIEW"})
        private_write(base / AUDIT_PATH, {"schema": 1, "actions": actions})
        applied += 1
    # Commit seen-flag snapshot only after all proposed actions were verified.
    # On failure, the idempotent next run safely repeats rechecks.
    private_write(seen_path, {"schema": 1, "flagged_ids": sorted(flagged)})
    return {"eligible_to_quarantine": len(actionable),
            "already_suspended": already_suspended, "applied": applied}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply scoped reversible quarantine")
    args = parser.parse_args()
    try:
        out = apply(BASE, dry_run=not args.apply)
        print("ALE_QUALITY_QUARANTINE_%s | candidates=%d | suspended=%d | already_held=%d" %
              ("APPLIED" if args.apply else "DRY_RUN",
               out["eligible_to_quarantine"], out["applied"], out["already_suspended"]))
        print("No card text, card IDs or credentials printed; no auto-reenable")
    except Exception:
        print("ALE_QUALITY_QUARANTINE_NOT_VERIFIED", file=sys.stderr)
        raise SystemExit(1)
