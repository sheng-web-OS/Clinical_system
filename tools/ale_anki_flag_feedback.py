#!/usr/bin/env python3
"""Owner-Mac-only Anki red flag -> private quality-feedback signal bridge.

No Anki mutation, no flag clearing, no card text, no FSRS changes. A red flag
is an owner quality-review request, NOT a verified medical/cognitive error.
Private event rows go only to the already configured owner's private Sheet.
Public GitHub/CI must never process actual card identifiers or user records.
"""
from __future__ import annotations
from datetime import datetime, timezone
import fcntl
import os
from pathlib import Path
import sys
from urllib.parse import quote

from ale_anki_readonly import check_version, invoke
from ale_anki_drive_sync import (
    BASE, CONFIG_NAME, LOCK_NAME, Sheets, authorized_session, checked_json,
    load_json, private_dir, private_write,
)

TAB = "Card_Feedback"
STATE_FILE = "red_flag_feedback_state.json"
HEADER = [
    "event_key", "first_detected_utc", "anki_card_id", "anki_note_id",
    "owner_signal", "cause_code", "review_state", "concept_family_id",
    "diagnosis_confidence", "provenance",
]
SOURCE = "OWNER_ANKI_RED_FLAG_1"

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def read_flagged_cards(max_cards=2000) -> dict[str, int]:
    """Query only red flags; card->note link is card-level, not sibling-level."""
    check_version()
    ids = invoke("findCards", query="flag:1")
    if not isinstance(ids, list) or len(ids) > max_cards:
        raise RuntimeError("Red-flag inventory invalid or exceeds bounded capacity")
    if any(type(cid) is not int or cid <= 0 for cid in ids) or len(ids) != len(set(ids)):
        raise RuntimeError("Red-flag card identity invalid or duplicated")
    mapping: dict[str, int] = {}
    for start in range(0, len(ids), 100):
        batch = ids[start:start + 100]
        infos = invoke("cardsInfo", cards=batch)
        if not isinstance(infos, list) or len(infos) != len(batch):
            raise RuntimeError("Incomplete Anki cardsInfo batch; no cursor advanced")
        for c in infos:
            if not isinstance(c, dict):
                raise RuntimeError("Invalid Anki cardInfo object")
            cid, note = c.get("cardId"), c.get("note")
            if type(cid) is not int or cid not in batch or type(note) is not int or note <= 0:
                raise RuntimeError("Anki flagged card/note identity mismatch")
            if "flags" in c and c["flags"] != 1:
                raise RuntimeError("Flag changed during snapshot; retry next scan")
            if str(cid) in mapping:
                raise RuntimeError("Duplicate Anki cardsInfo identity")
            mapping[str(cid)] = note
    if set(mapping) != {str(cid) for cid in ids}:
        raise RuntimeError("Anki flagged inventory incomplete")
    return mapping

def plan_events(prior: dict, flagged: dict[str, int], now: str) -> tuple[dict, list[list[str]]]:
    """One event per new observed red-flag interval, never a guessed flag timestamp.

    Clearing a flag is not equivalent to QA resolution. Re-flagging after an
    observed absence creates a new cycle. Intermediate toggles may be missed.
    """
    if prior and (prior.get("schema") != 1 or not isinstance(prior.get("cards"), dict)):
        raise RuntimeError("Invalid private red-flag checkpoint")
    old = prior.get("cards", {})
    cards = {}
    events = []
    for cid, record in old.items():
        if not cid.isdigit() or not isinstance(record, dict) or type(record.get("cycle")) is not int or record["cycle"] < 1 or type(record.get("active")) is not bool:
            raise RuntimeError("Invalid private card checkpoint record")
        cards[cid] = dict(record)
        if cid not in flagged:
            cards[cid]["active"] = False
    for cid, note in sorted(flagged.items(), key=lambda x: int(x[0])):
        prev = cards.get(cid)
        if prev and prev["active"]:
            if prev.get("note_id") != note:
                raise RuntimeError("Anki card-note identity changed; manual investigation required")
            continue
        cycle = (prev["cycle"] if prev else 0) + 1
        cards[cid] = {"cycle": cycle, "active": True, "note_id": note, "first_detected_utc": now}
        events.append([
            "anki-red-flag:%s:%s" % (cid, cycle), now, cid, str(note),
            "QUALITY_REVIEW_REQUEST", "UNKNOWN", "PENDING_DIAGNOSIS",
            "UNMAPPED", "NOT_ASSESSED", SOURCE,
        ])
    return {"schema": 1, "cards": cards, "last_scan_utc": now}, events

def _api_root(sheet: Sheets) -> str:
    if not sheet.root.startswith("https://sheets.googleapis.com/v4/spreadsheets/") or not sheet.root.endswith("/values"):
        raise RuntimeError("Unexpected private spreadsheet endpoint")
    return sheet.root[:-7]

def ensure_feedback_tab(sheet: Sheets) -> None:
    """Bootstrap ONLY a new tab in the existing configured private spreadsheet."""
    root = _api_root(sheet)
    metadata = checked_json(sheet.session.get(root, params={"fields": "sheets.properties.title"}, timeout=20))
    tabs = metadata.get("sheets")
    if not isinstance(tabs, list):
        raise RuntimeError("Spreadsheet tab inventory not verified")
    existing = {str(s.get("properties", {}).get("title")) for s in tabs if isinstance(s, dict)}
    if TAB not in existing:
        checked_json(sheet.session.post(
            root + ":batchUpdate",
            json={"requests": [{"addSheet": {"properties": {"title": TAB}}}]},
            timeout=30,
        ))
        metadata = checked_json(sheet.session.get(root, params={"fields": "sheets.properties.title"}, timeout=20))
        existing = {str(s.get("properties", {}).get("title")) for s in metadata.get("sheets", [])}
        if TAB not in existing:
            raise RuntimeError("Private feedback tab creation not confirmed")
    header = sheet.get(TAB + "!A1:J1")
    if not header:
        response = checked_json(sheet.session.put(
            sheet.root + "/" + quote(TAB + "!A1:J1", safe="!:"),
            params={"valueInputOption": "RAW"},
            json={"majorDimension": "ROWS", "values": [HEADER]}, timeout=30,
        ))
        if response.get("updatedCells") != len(HEADER):
            raise RuntimeError("Private feedback header write not confirmed")
        header = sheet.get(TAB + "!A1:J1")
    if header != [HEADER]:
        raise RuntimeError("Existing private feedback schema differs; no event append")

def remote_index(sheet: Sheets) -> dict[str, list]:
    records = sheet.get(TAB + "!A2:J")
    seen = {}
    for raw in records:
        if not isinstance(raw, list):
            raise RuntimeError("Invalid feedback row")
        if not raw or not any(str(x) for x in raw):
            continue
        if len(raw) != len(HEADER) or not str(raw[0]):
            raise RuntimeError("Incomplete feedback record; no checkpoint")
        key = str(raw[0])
        if key in seen:
            raise RuntimeError("Duplicate feedback event key; no checkpoint")
        seen[key] = raw
    return seen

def sync_event_rows(sheet: Sheets, events: list[list[str]]) -> tuple[int, int]:
    """Readback rows and normalize events to their durable first-observed time.

    A prior append may have succeeded before ACK/local checkpoint loss. Only
    the timestamp can be reconciled; identity, signal and provenance must match.
    The caller persists the normalized observation after successful readback.
    """
    existing = remote_index(sheet)
    immutable = (0, 1, 2, 3, 4, 9)
    for expected in events:
        saved = existing.get(expected[0])
        if saved is None:
            continue
        if any(str(saved[i]) != expected[i] for i in immutable if i != 1):
            raise RuntimeError("Private red-flag readback mismatch; no checkpoint")
        try:
            def observation_time(value):
                if type(value) is not str or len(value) > 40:
                    raise ValueError
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if parsed.tzinfo is None or parsed.utcoffset() is None:
                    raise ValueError
                return parsed
            if observation_time(saved[1]) > observation_time(expected[1]):
                raise ValueError
        except (ValueError, TypeError, OverflowError):
            raise RuntimeError("Invalid or future feedback timestamp; no checkpoint") from None
        expected[1] = saved[1]
    def verify(rows):
        for expected in events:
            saved = rows.get(expected[0])
            if saved is None or any(str(saved[i]) != expected[i] for i in immutable):
                raise RuntimeError("Private red-flag readback mismatch; no checkpoint")
    fresh = [r for r in events if r[0] not in existing]
    for r in fresh:
        answer = checked_json(sheet.session.post(
            sheet.root + "/" + quote(TAB + "!A:J", safe="!:") + ":append",
            params={"valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS"},
            json={"majorDimension": "ROWS", "values": [r]}, timeout=30,
        ))
        if answer.get("updates", {}).get("updatedRows") != 1:
            raise RuntimeError("Feedback append unconfirmed; retry reconciles event key")
    after = remote_index(sheet)
    if not set(existing).issubset(after):
        raise RuntimeError("Existing feedback records disappeared; no checkpoint")
    verify(after)
    return len(fresh), len(events) - len(fresh)

def run(base: Path) -> tuple[int, int, int]:
    private_dir(base)
    conf = load_json(base / CONFIG_NAME, required=True)
    if conf.get("tab") != "Error_Events" or not conf.get("spreadsheet_id"):
        raise RuntimeError("Private ALE sheet target invalid")
    fd = os.open(str(base / LOCK_NAME), os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        prior = load_json(base / STATE_FILE)
        flagged = read_flagged_cards()
        next_state, events = plan_events(prior, flagged, utc_now())
        sheet = Sheets(authorized_session(base), conf["spreadsheet_id"])
        ensure_feedback_tab(sheet)
        added, duplicates = sync_event_rows(sheet, events)
        for event in events:
            next_state["cards"][event[2]]["first_detected_utc"] = event[1]
        # Commit local observation only after remote readback.
        private_write(base / STATE_FILE, next_state)
    finally:
        os.close(fd)
    return len(flagged), added, duplicates

if __name__ == "__main__":
    try:
        flagged, added, duplicates = run(BASE)
        print("ALE_FLAG_FEEDBACK_SYNC_OK | currently_red_flagged=%d | new_private_requests=%d | deduplicated=%d" % (flagged, added, duplicates))
        print("Quality issues queued for analysis; no cards, flags, notes or scheduling changed")
    except Exception:
        print("ALE_FLAG_FEEDBACK_NOT_VERIFIED | inspect private Mac diagnostics", file=sys.stderr)
        raise SystemExit(1)
