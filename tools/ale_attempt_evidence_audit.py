#!/usr/bin/env python3
"""Owner-local aggregate audit of ALE answer provenance; never grades people.

One attempt row != an independently graded item; a group score cannot locate
a specific misconception, and post-remediation answers are not unseen tests.
Reads ONLY the owner-private existing Sheets; no Anki calls or modifications.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from ale_anki_drive_sync import BASE, CONFIG_NAME, Sheets, authorized_session, load_json

ATTEMPTS_HEADER = [
    "attempt_id", "date_taipei", "session_id", "question_id_local",
    "official_exam_identity_verified", "topic", "response",
    "answer_key_if_known", "assessment", "reasoning_signal",
    "answer_exposure", "grading_source", "source_quality", "followup"
]
CONCEPTS_HEADER = [
    "concept_id", "domain", "observed_evidence", "knowledge_state",
    "confidence", "needs_retest", "priority", "next_best_action",
    "last_observed", "do_not_overclaim"
]


def _text(value) -> str:
    return str(value).strip() if value is not None else ""


def _records(raw: list[list], width: int) -> list[list]:
    if not isinstance(raw, list) or any(not isinstance(row, list) for row in raw):
        raise RuntimeError("Invalid private sheet values")
    rows = []
    for row in raw:
        if not any(_text(v) for v in row):
            continue
        if len(row) > width:
            raise RuntimeError("Private sheet row wider than schema")
        # Sheets omits empty trailing cells in its values API.
        rows.append(row + [""] * (width - len(row)))
    return rows


def assess(attempts: list[list], concepts: list[list]) -> dict:
    """Conservative provenance counts: assessment text is not an audit receipt."""
    attempt_rows = _records(attempts, len(ATTEMPTS_HEADER))
    concept_rows = _records(concepts, len(CONCEPTS_HEADER))
    counts: Counter[str] = Counter()
    ids: set[str] = set()
    for row in attempt_rows:
        key = _text(row[0])
        if not key or key in ids:
            raise RuntimeError("Missing or duplicate private attempt ID")
        ids.add(key)
        official = _text(row[4]).upper()
        if official not in {"YES", "NO", "NOT_VERIFIED", "UNKNOWN", ""}:
            raise RuntimeError("Invalid exam identity verification marker")
        counts["official_identity_independently_unverified"] += int(official != "YES")
        counts["official_identity_claimed_verified"] += int(official == "YES")
        answer = _text(row[6])
        counts["observed_response_rows" if answer else "answer_missing_rows"] += 1
        assessment, quality = _text(row[8]).lower(), _text(row[12]).lower()
        counts["group_grade_nonattributable"] += int("group" in assessment or "group" in quality)
        counts["assessment_present_without_independent_receipt"] += int(
            bool(assessment and assessment != "unanswered")
        )
        exposure = _text(row[10]).lower()
        counts["post_remediation_or_noninitial_exposure"] += int(
            bool(exposure and exposure != "initial attempt")
        )
    concepts_seen: set[str] = set()
    for row in concept_rows:
        cid = _text(row[0])
        if not cid or cid in concepts_seen:
            raise RuntimeError("Missing or duplicate private concept ID")
        concepts_seen.add(cid)
        counts["concept_retest_pending"] += int(_text(row[5]).upper() == "YES")

    return {
        "attempt_rows": len(attempt_rows),
        "observed_response_rows": counts["observed_response_rows"],
        "answer_missing_rows": counts["answer_missing_rows"],
        "official_identity_independently_unverified":
            counts["official_identity_independently_unverified"],
        "official_identity_claimed_verified_not_external_proof":
            counts["official_identity_claimed_verified"],
        "group_grade_nonattributable": counts["group_grade_nonattributable"],
        "assessment_present_without_independent_receipt":
            counts["assessment_present_without_independent_receipt"],
        "post_remediation_or_noninitial_exposure":
            counts["post_remediation_or_noninitial_exposure"],
        "concept_nodes": len(concept_rows),
        "concept_retest_pending": counts["concept_retest_pending"],
        # No authenticated examiner/key audit receipt exists in current schema.
        "independently_verified_item_grades": 0,
        "unseen_transfer_passes_proven_by_this_audit": 0,
        "mastery_upgrades_authorized": 0,
        "quality_verdict": "OBSERVATIONS_VALID_FOR_HYPOTHESIS_ONLY",
    }


def inspect_remote(sheet: Sheets) -> dict:
    attempt_head = sheet.get("Attempts!A1:N1")
    concept_head = sheet.get("Concepts!A1:J1")
    if not attempt_head or [_text(v) for v in attempt_head[0]] != ATTEMPTS_HEADER:
        raise RuntimeError("Private Attempts header mismatch")
    if not concept_head or [_text(v) for v in concept_head[0]] != CONCEPTS_HEADER:
        raise RuntimeError("Private Concepts header mismatch")
    return assess(sheet.get("Attempts!A2:N"), sheet.get("Concepts!A2:J"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-dir", type=Path, default=BASE)
    args = parser.parse_args(argv)
    conf = load_json(args.private_dir.expanduser() / CONFIG_NAME, required=True)
    if conf.get("tab") != "Error_Events":
        raise RuntimeError("Unexpected private Sheet target")
    sheet = Sheets(authorized_session(args.private_dir.expanduser()), conf["spreadsheet_id"])
    report = inspect_remote(sheet)
    for key, value in report.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
