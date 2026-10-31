#!/usr/bin/env python3
"""Clinical OS ALE-01: read-only iPhone -> AnkiWeb -> Mac review proof.

Only reads a locally running AnkiConnect on 127.0.0.1. It does not sync,
modify, delete, create cards, or upload private information. Local identifiers
are written only to a private folder on this Mac, never to GitHub.
"""
import argparse
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

ENDPOINT = "http://127.0.0.1:8765"
API_VERSION = 6
READ_ONLY_ACTIONS = frozenset({"version", "deckNames", "cardReviews", "cardsInfo", "findCards"})
DEFAULT_STATE = pathlib.Path.home() / "Library" / "Application Support" / "ClinicalOS-ALE" / "iphone_anki_probe.json"


def invoke(action, **params):
    if action not in READ_ONLY_ACTIONS:
        raise ValueError("Write or unapproved Anki action refused")
    payload = {"action": action, "version": API_VERSION, "params": params}
    key = os.environ.get("ANKI_CONNECT_API_KEY")
    if key:
        payload["key"] = key
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            reply = json.load(resp)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(
            "Cannot reach local AnkiConnect. Open Anki Desktop and install/enable the add-on."
        ) from exc
    if not isinstance(reply, dict) or "result" not in reply or "error" not in reply:
        raise RuntimeError("Unexpected AnkiConnect response structure")
    if reply["error"]:
        raise RuntimeError(f"AnkiConnect rejected {action}: {reply['error']}")
    return reply["result"]


def save_private(path, data):
    """Atomic private local write, no card texts or source account IDs."""
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(str(tmp), os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        os.chmod(path, 0o600)
    finally:
        if tmp.exists():
            tmp.unlink()


def check_version():
    version = invoke("version")
    if not isinstance(version, int) or version < API_VERSION:
        raise RuntimeError("AnkiConnect API v6 is required for this probe")
    return version


def begin(path):
    check_version()
    decks = invoke("deckNames")
    if not isinstance(decks, list):
        raise RuntimeError("Invalid deck inventory")
    started = int(time.time() * 1000)
    save_private(path, {"schema": 1, "started_at_ms": started, "last_verified": None})
    print("BASELINE_OK | decks_detected=" + str(len(decks)))
    print("Next: review one card in AnkiMobile, sync iPhone, then sync Mac Anki.")
    print("Finally run: python3 ale_anki_readonly.py verify")
    return 0


def recent_reviews(decks, started_at_ms):
    """Dedup reviews across potentially overlapping parent/child deck queries."""
    seen = {}
    for deck in decks:
        rows = invoke("cardReviews", deck=deck, startID=max(0, started_at_ms - 1000))
        if not isinstance(rows, list):
            raise RuntimeError("cardReviews returned unexpected data")
        for row in rows:
            if not isinstance(row, (list, tuple)) or len(row) != 9:
                raise RuntimeError("Unexpected cardReviews row")
            event_ms, card_id = row[0], row[1]
            if not isinstance(event_ms, int) or not isinstance(card_id, int):
                raise RuntimeError("Invalid review event identity")
            if event_ms >= started_at_ms:
                seen[(event_ms, card_id)] = row
    return sorted(seen.values(), key=lambda x: (x[0], x[1]))


def verify(path):
    if not path.is_file():
        raise RuntimeError("No baseline. First run: python3 ale_anki_readonly.py baseline")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        started = int(data["started_at_ms"])
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        raise RuntimeError("Baseline file missing or invalid") from exc
    check_version()
    decks = invoke("deckNames")
    if not isinstance(decks, list):
        raise RuntimeError("Invalid deck inventory")
    events = recent_reviews(decks, started)
    if not events:
        print("NO_NEW_REVIEWS | Check iPhone AnkiWeb sync and Mac Anki sync.")
        return 2
    latest = events[-1]
    card_id = latest[1]
    info = invoke("cardsInfo", cards=[card_id])
    if not isinstance(info, list) or len(info) != 1:
        raise RuntimeError("Could not resolve reviewed card")
    card = info[0]
    if not isinstance(card, dict) or card.get("cardId") != card_id:
        raise RuntimeError("Card ID mismatch")
    note_id = card.get("note")
    if not isinstance(note_id, int):
        raise RuntimeError("Cannot resolve reviewed note ID")
    # Private event identity only: do not write question/answer, tags, deck names.
    data["last_verified"] = {
        "review_event_id_ms": latest[0],
        "anki_card_id": card_id,
        "anki_note_id": note_id,
        "anki_rating_button": latest[3],
        "event_count_since_baseline": len(events),
        "verified_at_ms": int(time.time() * 1000),
    }
    save_private(path, data)
    print("REVIEW_LINK_OK | new_review_events=" + str(len(events)))
    print("CARD_NOTE_LINK_OK | local note/card identifiers verified")
    print("No card content, deck name, note/card ID, or credentials printed or uploaded.")
    print("Next gate: map this reviewed note to a verified Concept Family ID.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="ALE-01 local Anki read-only sync proof")
    parser.add_argument("command", choices=("baseline", "verify"))
    args = parser.parse_args(argv)
    path = pathlib.Path(os.environ.get("ALE_ANKI_PROBE_STATE", DEFAULT_STATE)).expanduser()
    try:
        return begin(path) if args.command == "baseline" else verify(path)
    except Exception as exc:
        print("PROBE_NOT_VERIFIED | " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
