#!/usr/bin/env python3
"""Owner-local pilot: confirm one Anki card -> concept relationship privately.

Uses an existing read-only AnkiConnect + owner-private Google OAuth bridge.
Never uploads Anki note HTML, card text, account IDs, or credentials to GitHub.
Only the actual selected card direction is linked (not every sibling card).
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import html
import hashlib
import re
from pathlib import Path
import sys
from urllib.parse import quote

from ale_anki_readonly import invoke, check_version
from ale_anki_drive_sync import (BASE, CONFIG_NAME, LOCK_NAME, Sheets,
                                authorized_session, checked_json, load_json, private_dir, private_write)
import fcntl
import os

SKIP_NAME = "concept_map_skips.json"
MAP_TAB = "Card_Concept_Map"
MAP_HEADER = ["stable_note_id", "anki_note_id", "anki_card_ids", "concept_id",
              "claim_type", "relation", "card_state", "source_ref",
              "last_review_event_id", "last_observed", "confirmed_mapping"]


def latest_unlinked_review(reviews: list, mappings: list, skipped: set[str] | None = None) -> tuple | None:
    skipped = skipped or set()
    linked_cards = set()
    for m in mappings:
        if len(m) >= 11 and str(m[10]).startswith("OWNER_CONFIRMED"):
            linked_cards.update(s.strip() for s in str(m[2]).split(",") if s.strip())
    for row in reversed(reviews):
        if len(row) >= 14 and str(row[2]).isdigit() and str(row[3]).isdigit():
            if (str(row[2]) not in linked_cards and str(row[2]) not in skipped
                    and re.fullmatch(r"anki-revlog:\d+:\d+", str(row[0]))):
                return row
    return None


def catalog_signature(ids: list[str]) -> str:
    """Catalog fingerprint is metadata; explicit skips persist across catalog changes."""
    return hashlib.sha256("\n".join(sorted(ids)).encode("utf-8")).hexdigest()


def skipped_for_catalog(base: Path, ids: list[str]) -> set[str]:
    data = load_json(base / SKIP_NAME)
    # Owner chose to preserve skipped cards across catalog versions.
    # Catalog changes must not silently revoke a prior explicit skip.
    if not data:
        return set()
    raw = data.get("skipped_cards", [])
    if not isinstance(raw, list) or not all(isinstance(x, str) and x.isdigit() for x in raw):
        raise RuntimeError("Invalid local concept skip state")
    return set(raw)


def remember_skip(base: Path, ids: list[str], card_id: int) -> None:
    skipped = skipped_for_catalog(base, ids)
    skipped.add(str(card_id))
    private_write(base / SKIP_NAME, {
        "schema": 1, "signature": catalog_signature(ids),
        "skipped_cards": sorted(skipped),
    })


def local_question_preview(card: dict) -> str:
    # Only display on the owner's Terminal, never send in Sheets or logs.
    q = str(card.get("question", ""))
    q = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>", " ", q)
    q = re.sub(r"(?s)<[^>]+>", " ", q)
    q = html.unescape(q)
    q = re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", q)
    q = re.sub(r"\s+", " ", q).strip()
    return q[:160] if q else "[Question preview unavailable; check the Anki Browser]"


def suggested_concepts(card: dict, allowed: list[str]) -> list[str]:
    tags = card.get("tags", [])
    if not isinstance(tags, list):
        return []
    present = {str(x).lower() for x in tags}
    return [cid for cid in allowed if f"ale::concept::{cid}".lower() in present]


def mapping_row(event: list, concept_id: str, reviewed_at: str) -> list[str]:
    if len(event) < 14 or not str(event[2]).isdigit() or not str(event[3]).isdigit():
        raise ValueError("Unverified review/card/note linkage")
    if not re.fullmatch(r"anki-revlog:\d+:\d+", str(event[0])):
        raise ValueError("Invalid review source identity")
    if not concept_id or any(ch.isspace() for ch in concept_id):
        raise ValueError("Invalid concept ID")
    return ["", str(event[3]), str(event[2]), concept_id,
            "OWNER_CONFIRMED_LOCAL", "TESTS_THIS_CARD_DIRECTION_ONLY",
            "ACTIVE_MAPPING_PROPOSAL", "OWNER_VERIFIED_ANKI_QUESTION_LOCALLY",
            str(event[0]), reviewed_at, "OWNER_CONFIRMED_SINGLE_CARD"]


def validate_map_header(sheet: Sheets):
    headers = sheet.get(f"{MAP_TAB}!A1:K1")
    if not headers or [str(x) for x in headers[0]] != MAP_HEADER:
        raise RuntimeError("Private Card_Concept_Map schema differs; no writes")


def append_private_mapping(sheet: Sheets, row: list) -> None:
    if len(row) != 11:
        raise ValueError("Invalid private mapping shape")
    result = checked_json(sheet.session.post(
        f"{sheet.root}/{quote(MAP_TAB+'!A:K', safe='!:')}:append",
        params={"valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS"},
        json={"majorDimension": "ROWS", "values": [row]}, timeout=30))
    if result.get("updates", {}).get("updatedRows") != 1:
        raise RuntimeError("Private mapping append unconfirmed; retry will read back")


def execute(base: Path) -> str:
    private_dir(base)
    config = load_json(base / CONFIG_NAME, required=True)
    if config.get("tab") != "Error_Events":
        raise RuntimeError("Unexpected private spreadsheet config")
    session = authorized_session(base)
    sheet = Sheets(session, config["spreadsheet_id"])
    sheet.verify_schema()
    validate_map_header(sheet)
    events = sheet.get("Error_Events!A2:N")
    existing = sheet.get(f"{MAP_TAB}!A2:K")
    concepts = sheet.get("Concepts!A2:J")
    ids = sorted({str(r[0]) for r in concepts if r and str(r[0]).strip()})
    if not ids:
        return "NO_VERIFIED_CONCEPT_OPTIONS | Private Concepts has no options"
    skipped = skipped_for_catalog(base, ids)
    eligible = latest_unlinked_review(events, existing, skipped)
    if eligible is None:
        return "NO_ELIGIBLE_REVIEW | No unskipped card for current concept catalog"
    card_id, note_id = int(eligible[2]), int(eligible[3])
    check_version()
    cards = invoke("cardsInfo", cards=[card_id])
    if not isinstance(cards, list) or len(cards) != 1:
        raise RuntimeError("The review card is no longer locally available; no mapping")
    card = cards[0]
    if card.get("cardId") != card_id or card.get("note") != note_id:
        raise RuntimeError("Anki local card/note mismatch; no mapping")
    suggestions = suggested_concepts(card, ids)
    print("This Anki question is displayed only on your Mac (never uploaded):")
    print(local_question_preview(card))
    if suggestions:
        print("Structured Anki tag suggests one or more concepts; confirm semantics before mapping.")
    print("Choose the *single* concept specifically tested by THIS card direction; 0 = skip.")
    for i, cid in enumerate(ids, start=1):
        print(f"{i}: {cid}" + (" [tag suggestion]" if cid in suggestions else ""))
    selected = input("Concept number (0 to skip): ").strip()
    if selected in ("", "0"):
        remember_skip(base, ids, card_id)
        return "OWNER_SKIPPED | No mapping written; local skip recorded for this catalog"
    if not selected.isdigit() or not (1 <= int(selected) <= len(ids)):
        raise ValueError("Invalid concept choice")
    concept_id = ids[int(selected) - 1]
    confirm = input("Does the local Anki question actually test this concept? type YES to confirm: ").strip()
    if confirm != "YES":
        return "OWNER_DID_NOT_CONFIRM | No mapping written"
    proposal = mapping_row(eligible, concept_id, datetime.now(timezone.utc).isoformat())
    # Recheck within a Mac-local exclusive lock before append and remote readback.
    fd = os.open(str(base / LOCK_NAME), os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        latest = sheet.get(f"{MAP_TAB}!A2:K")
        matches = [r for r in latest if len(r) >= 11 and str(r[2]) == str(card_id) and str(r[10]).startswith("OWNER_CONFIRMED")]
        if matches:
            if len(matches) == 1 and str(matches[0][3]) == concept_id:
                return "ALREADY_LINKED | No duplicate mapping written"
            raise RuntimeError("Conflicting owner-private card mapping; manual reconciliation required")
        append_private_mapping(sheet, proposal)
        fresh = sheet.get(f"{MAP_TAB}!A2:K")
        confirmed = [r for r in fresh if len(r) >= 11 and str(r[1]) == str(note_id) and str(r[2]) == str(card_id) and str(r[3]) == concept_id and str(r[10]) == "OWNER_CONFIRMED_SINGLE_CARD"]
        if len(confirmed) != 1:
            raise RuntimeError("Private mapping write-readback mismatch; no success claim")
    finally:
        os.close(fd)
    return "OWNER_PRIVATE_CONCEPT_LINK_OK | exactly_one_card_mapped=1 | Anki_unchanged=true"


def main(argv=None):
    p = argparse.ArgumentParser(description="Owner-local one-card semantic concept mapping")
    p.add_argument("--private-dir", type=Path, default=BASE)
    args = p.parse_args(argv)
    try:
        print(execute(args.private_dir.expanduser()))
        return 0
    except (EOFError, KeyboardInterrupt):
        print("OWNER_MAPPING_CANCELLED | No confirmed result", file=sys.stderr)
        return 2
    except Exception as exc:
        print("CONCEPT_LINK_NOT_VERIFIED | " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
