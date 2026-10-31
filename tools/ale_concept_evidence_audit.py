#!/usr/bin/env python3
"""ALE-01: owner-local, read-only event->Concept Family evidence audit.

A confirmed Anki card direction can supply a *recall* observation. It never
supplies unseen transfer, inferred diagnosis, mastery or automatic card edits.
This file contains no credentials, personal identifiers or public telemetry.
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

from ale_anki_drive_sync import (
    BASE, CONFIG_NAME, Sheets, audit_private_sheet, authorized_session, load_json
)

MAP_TAB = "Card_Concept_Map"
MAP_HEADER = ["stable_note_id", "anki_note_id", "anki_card_ids", "concept_id",
              "claim_type", "relation", "card_state", "source_ref",
              "last_review_event_id", "last_observed", "confirmed_mapping"]


def _str(value) -> str:
    return str(value).strip() if value is not None else ""


def _filled(rows: list[list]) -> list[list]:
    if not isinstance(rows, list):
        raise RuntimeError("Invalid private sheet row collection")
    if any(not isinstance(row, list) for row in rows):
        raise RuntimeError("Invalid private sheet row")
    return [row for row in rows if any(_str(cell) for cell in row)]


def _datetime(value: str):
    from datetime import datetime
    try:
        result = datetime.fromisoformat(_str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise RuntimeError("Invalid private mapping or event time") from exc
    if result.tzinfo is None:
        raise RuntimeError("Private time lacks timezone")
    return result


def inspect_evidence(events: list[list], mappings: list[list],
                     concept_ids: list[str]) -> dict:
    """Join exactly one owner-confirmed source event, without retroactive mastery.

    Review history lacks a content snapshot. A later verified *current* card
    question can yield a RETROSPECTIVE ASSOCIATION, not proof of its past text.
    """
    valid = {_str(c) for c in concept_ids if _str(c)}
    if len(valid) != len([c for c in concept_ids if _str(c)]):
        raise RuntimeError("Duplicate concept identifier in private taxonomy")
    if not valid:
        raise RuntimeError("No recognized concepts; cannot confirm a family")
    all_mappings: dict[str, dict] = {}
    seen_confirmed: set[tuple[str, str, str]] = set()
    for row in _filled(mappings):
        if len(row) != len(MAP_HEADER):
            raise RuntimeError("Invalid private mapping row width")
        state = _str(row[10])
        if state != "OWNER_CONFIRMED_SINGLE_CARD":
            continue
        note, card, concept = _str(row[1]), _str(row[2]), _str(row[3])
        if not (note.isdigit() and card.isdigit()):
            raise RuntimeError("Confirmed card mapping missing exact note/card ID")
        if concept not in valid:
            raise RuntimeError("Confirmed card mapping to unrecognized concept")
        if (_str(row[5]) != "TESTS_THIS_CARD_DIRECTION_ONLY"
            or _str(row[4]) != "OWNER_CONFIRMED_LOCAL"
            or _str(row[7]) != "OWNER_VERIFIED_ANKI_QUESTION_LOCALLY"):
            raise RuntimeError("Confirmed mapping lacks local semantic attestation")
        anchor = _str(row[8])
        match = re.fullmatch(r"anki-revlog:(\d+):(\d+)", anchor)
        if not match or match.group(2) != card:
            raise RuntimeError("Confirmed card mapping has wrong source-review anchor")
        confirmed_at = _datetime(row[9])
        record_id = (card, note, concept)
        if record_id in seen_confirmed:
            raise RuntimeError("Duplicate confirmed private card mapping")
        seen_confirmed.add(record_id)
        if card in all_mappings:
            raise RuntimeError("Conflicting private mapping for the same card")
        all_mappings[card] = {
            "note": note, "concept": concept, "anchor": anchor,
            "confirmed_at": confirmed_at,
        }

    seen: set[str] = set()
    events_by_key: dict[str, list] = {}
    counts: Counter[str] = Counter()
    retrospectively_associated_concepts: set[str] = set()
    for row in _filled(events):
        if len(row) != 14:
            raise RuntimeError("Invalid private event row width")
        key, card, note = _str(row[0]), _str(row[2]), _str(row[3])
        match = re.fullmatch(r"anki-revlog:(\d+):(\d+)", key)
        if not match or match.group(2) != card or _str(row[11]) != match.group(1):
            raise RuntimeError("Private event identity mismatch")
        if key in seen:
            raise RuntimeError("Duplicate private event")
        seen.add(key)
        events_by_key[key] = row
        if _str(row[12]) != "SYNCED_READ_ONLY":
            raise RuntimeError("Unverified private review sync state")
        if _str(row[5]) not in {"1", "2", "3", "4"}:
            raise RuntimeError("Invalid private Anki button")
        if not note:
            counts["missing_note_identity"] += 1
            continue
        linked = all_mappings.get(card)
        if linked is None:
            counts["unmapped"] += 1
            continue
        if note != linked["note"]:
            raise RuntimeError("Confirmed card mapping conflicts with event note ID")
        if key != linked["anchor"]:
            # The same card may have been rewritten or changed directions since
            # the last owner-confirmed source review: never blindly backfill.
            counts["other_review_without_versioned_context"] += 1
            continue
        event_at = _datetime(row[1])
        from datetime import datetime, timezone
        recorded_at = datetime.fromtimestamp(int(match.group(1)) / 1000, tz=timezone.utc)
        if abs((event_at - recorded_at).total_seconds()) > 0.001:
            raise RuntimeError("Review timestamp does not match its revlog identity")
        if event_at > linked["confirmed_at"]:
            raise RuntimeError("Concept mapping confirmed before its anchor review")
        if _str(row[4]):
            # concept_family_id != concept_id: no family graph edge established.
            counts["family_relation_needs_verification"] += 1
        counts["retrospective_concept_links"] += 1
        retrospectively_associated_concepts.add(linked["concept"])

    # A confirmed mapping whose asserted anchor is not present in the actual
    # private review ledger is ungrounded and must not be counted.
    for link in all_mappings.values():
        anchor_row = events_by_key.get(link["anchor"])
        if anchor_row is None:
            raise RuntimeError("Confirmed mapping anchor absent from private reviews")
        if _str(anchor_row[3]) != link["note"]:
            raise RuntimeError("Confirmed mapping anchor note identity mismatch")

    return {
        "event_count": len(seen),
        "owner_confirmed_anchor_links": counts["retrospective_concept_links"],
        "retrospective_concept_links": counts["retrospective_concept_links"],
        "other_review_without_versioned_context": counts["other_review_without_versioned_context"],
        # Do not relabel retrospective association as independently verified
        # historical recall: revlog does not preserve the card's old question.
        "mapped_recall_only": 0,
        "verified_historical_concept_recall": 0,
        "unmapped": counts["unmapped"],
        "missing_note_identity": counts["missing_note_identity"],
        "family_relation_needs_verification": counts["family_relation_needs_verification"],
        "distinct_tested_concepts": 0,
        "retrospectively_associated_concepts": len(retrospectively_associated_concepts),
        "causal_diagnoses_verified": 0,
        "unseen_transfer_passes_verified": 0,
        "concept_mastery_upgrades": 0,
        "anki_mutations": 0,
        "recommendation": (
            "MAPPING_REQUIRED" if counts["unmapped"] or counts["missing_note_identity"]
            else "HISTORICAL_CARD_VERSION_NOT_ATTESTED"
        ),
    }


def inspect_remote(sheet: Sheets) -> dict:
    """Read-only Google Sheets inspection; returns only aggregate counts."""
    integrity = audit_private_sheet(sheet)
    header = sheet.get(f"{MAP_TAB}!A1:K1")
    if not header or [_str(x) for x in header[0]] != MAP_HEADER:
        raise RuntimeError("Card_Concept_Map header mismatch")
    concepts_header = sheet.get("Concepts!A1:J1")
    if not concepts_header or _str(concepts_header[0][0]) != "concept_id":
        raise RuntimeError("Concepts header mismatch")
    events = sheet.get("Error_Events!A2:N")
    mappings = sheet.get(f"{MAP_TAB}!A2:K")
    concepts = sheet.get("Concepts!A2:J")
    report = inspect_evidence(events, mappings, [row[0] for row in concepts if row])
    if report["event_count"] != integrity["events"]:
        raise RuntimeError("Private event changed between reads; retry later")
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-dir", type=Path, default=BASE)
    args = parser.parse_args(argv)
    base = args.private_dir.expanduser()
    config = load_json(base / CONFIG_NAME, required=True)
    if config.get("tab") != "Error_Events":
        raise RuntimeError("Unexpected private spreadsheet target")
    sheet = Sheets(authorized_session(base), config["spreadsheet_id"])
    report = inspect_remote(sheet)
    for key, value in report.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
