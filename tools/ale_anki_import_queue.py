#!/usr/bin/env python3
"""Owner-Mac-only, opt-in, add-only Anki imports from an owner-private Google Sheet.

Never executes in GitHub Actions or cloud; no public card text or personal IDs.
Requires a separately reviewed, released card row; never edits existing Anki notes.
The existing read-only uploader remains unchanged and independent.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import fcntl
from pathlib import Path
from urllib.parse import quote
import urllib.request

from ale_anki_drive_sync import (
    BASE, CONFIG_NAME, LOCK_NAME, Sheets, authorized_session,
    checked_json, load_json, private_dir, private_write,
)

TAB = "Card_Import_Queue"
HEADER = [
    "card_key", "front_html", "back_html", "tags", "deck", "source_ref",
    "independent_review_ref", "qa_status", "release_status", "import_status",
    "anki_note_id", "content_sha256",
]
CONFIG = "anki_import_optin.json"
ANKI_ENDPOINT = "http://127.0.0.1:8765"
KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{4,63}$")
SAFE_TAG = re.compile(r"^[A-Za-z0-9:_-]{1,80}$")
SAFE_DECK = re.compile(r"^ClinicalOS::ALE(?:[A-Za-z0-9_:-]{0,80})$")
SOURCE = re.compile(r"^https://(?:www\.)?(?:pubmed\.ncbi\.nlm\.nih\.gov|"
                    r"pmc\.ncbi\.nlm\.nih\.gov|doi\.org|kdigo\.org|"
                    r"nice\.org\.uk|aasld\.org|acc\.org|heart\.org|"
                    r"diabetesjournals\.org)/[^\s<>]+$")
REVIEW = re.compile(r"^https://github\.com/sheng-web-OS/Clinical_system/(?:issues|pull)/\d+(?:#issuecomment-\d+)?$")
BAD_HTML = re.compile(r"(?is)<\s*/?\s*(?:script|iframe|object|embed|form|input|audio|video|link|style)\b|"
                      r"\bon[a-z]+\s*=|javascript\s*:|data\s*:|<\s*img\b")
ALLOWED_ACTIONS = {"version", "findNotes", "notesInfo", "deckNames", "modelNames", "createDeck", "addNote"}
# Deliberately bounded to non-nested native Cloze syntax. Do not silently flatten
# malformed/nested clozes into a Basic note: that would test the wrong skill.
CLOZE_RE = re.compile(r"\{\{c([1-9][0-9]*)::([^{}]+?)\}\}", re.DOTALL)
MAX_PER_RUN = 10
MAX_QUEUE_ROWS = 300
MAX_HTML = 12000


def digest(front, back):
    data = json.dumps([front, back], ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def note_tag(key):
    if not KEY_RE.fullmatch(key):
        raise ValueError("Invalid card key")
    return "ale::card::" + key


def note_payload(front, back):
    """Determine native Anki note type from immutable, QA-reviewed text.

    Private queue schema A:L remains unchanged: for Cloze, front_html is Text
    and back_html is Extra. Existing non-cloze Basic rows remain compatible.
    Nested and multi-index syntaxes are deliberately held for review rather
    than being interpreted incorrectly by an older Mac Anki installation.
    """
    if "{{" in back or "}}" in back:
        raise ValueError("Template tokens in answer/Extra are not supported")
    matches = list(CLOZE_RE.finditer(front))
    remaining = CLOZE_RE.sub("", front)
    if "{{" in remaining or "}}" in remaining:
        raise ValueError("Malformed/unsupported Anki cloze expression")
    if not matches:
        return "Basic", {"Front": front, "Back": back}
    for match in matches:
        segments = match.group(2).split("::")
        if len(segments) > 2 or not segments[0].strip():
            raise ValueError("Empty or malformed cloze answer")
        if len(segments) == 2:
            hint = segments[1].strip()
            if not hint:
                raise ValueError("Empty cloze hint")
            # Structural anti-leak check only; independent semantic review is
            # still required to reject indirect or overly specific hints.
            normalize = lambda value: re.sub(r"\\s+", "", value).casefold()
            if normalize(hint) == normalize(segments[0]):
                raise ValueError("Cloze hint reveals the exact answer")
    # A naked deletion is not a self-contained retrieval problem. Require at
    # least a small amount of visible context after every target is masked.
    visible = re.sub(r"(?s)<!--.*?-->|<[^>]*>", " ", remaining)
    if len(re.findall(r"\\w", visible)) < 8:
        raise ValueError("Cloze prompt lacks visible contextual information")
    return "Cloze", {"Text": front, "Extra": back}


def local_anki(action, **params):
    if action not in ALLOWED_ACTIONS:
        raise ValueError("Anki action not allowed")
    payload = {"action": action, "version": 6, "params": params}
    if os.environ.get("ANKI_CONNECT_API_KEY"):
        payload["key"] = os.environ["ANKI_CONNECT_API_KEY"]
    req = urllib.request.Request(
        ANKI_ENDPOINT, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=12) as response:
        answer = json.load(response)
    if not isinstance(answer, dict) or set(answer) != {"result", "error"}:
        raise RuntimeError("Unexpected local AnkiConnect response")
    if answer["error"] is not None:
        raise RuntimeError("Local AnkiConnect action failed: " + action)
    return answer["result"]


def verify_header(sheet):
    rows = sheet.get(TAB + "!A1:L1")
    if rows != [HEADER]:
        raise RuntimeError("Private queue schema mismatch; importer stopped")


def parse_row(raw, index):
    if len(raw) > len(HEADER):
        raise ValueError("Queue row too wide")
    row = [str(x) for x in raw] + [""] * (len(HEADER) - len(raw))
    data = dict(zip(HEADER, row))
    data["_row"] = index
    return data


def validate_ready(row):
    """Only validated, released rows can be written. No per-card confirmation."""
    key = row["card_key"]
    tag = note_tag(key)
    front, back = row["front_html"], row["back_html"]
    if not front.strip() or not back.strip() or len(front) > MAX_HTML or len(back) > MAX_HTML:
        raise ValueError("Card content empty or too long")
    if BAD_HTML.search(front) or BAD_HTML.search(back):
        raise ValueError("Unsafe card HTML")
    if not row["source_ref"] or not SOURCE.fullmatch(row["source_ref"]):
        raise ValueError("Missing qualified medical source")
    if not REVIEW.fullmatch(row["independent_review_ref"]):
        raise ValueError("Missing independent QA evidence link")
    if row["qa_status"] != "INDEPENDENT_MEDICAL_QA_PASS":
        raise ValueError("No independent medical QA attestation")
    if row["release_status"] != "READY_TO_IMPORT" or row["import_status"] != "PENDING":
        raise ValueError("Card not released for automatic import")
    if row["anki_note_id"]:
        raise ValueError("Pending card has conflicting imported note ID")
    if row["content_sha256"] != digest(front, back):
        raise ValueError("Card body digest mismatch")
    if not SAFE_DECK.fullmatch(row["deck"]):
        raise ValueError("Unexpected target deck")
    tags = row["tags"].split()
    if len(tags) > 20 or any(not SAFE_TAG.fullmatch(t) for t in tags):
        raise ValueError("Invalid card tags")
    model, fields = note_payload(front, back)
    return tag, list(dict.fromkeys(tags + [tag])), model, fields


def verify_note(note_id, row):
    notes = local_anki("notesInfo", notes=[note_id])
    if not isinstance(notes, list) or len(notes) != 1 or not isinstance(notes[0], dict):
        raise RuntimeError("Anki note readback missing")
    note = notes[0]
    model, expected = note_payload(row["front_html"], row["back_html"])
    if note.get("modelName") != model:
        raise RuntimeError("Anki note type differs; no overwrite or migration")
    fields = note.get("fields", {})
    if any(not isinstance(fields.get(key), dict) or
           fields[key].get("value") != value
           for key, value in expected.items()):
        raise RuntimeError("Anki note exists but content differs; no overwrite")
    return note


def existing_note(row, stable_tag):
    hits = local_anki("findNotes", query="tag:" + stable_tag)
    if not isinstance(hits, list) or len(hits) > 1:
        raise RuntimeError("Anki stable tag collision")
    if hits:
        note_id = hits[0]
        note = verify_note(note_id, row)
        if stable_tag not in note.get("tags", []):
            raise RuntimeError("Anki stable tag readback mismatch")
        return note_id
    # Compatibility with previously manually imported 2026-10-31 pilot TSV,
    # whose Front embeds an ALE key but whose Tags predate the stable-id tag.
    if row["card_key"].startswith("ALE26-"):
        legacy = local_anki("findNotes", query="tag:ALE::pilot")
        if not isinstance(legacy, list) or len(legacy) > 250:
            raise RuntimeError("Legacy pilot inventory too large or invalid")
        if legacy:
            candidates = local_anki("notesInfo", notes=legacy)
            if not isinstance(candidates, list) or len(candidates) != len(legacy):
                raise RuntimeError("Legacy pilot readback incomplete")
            matched = [n for n in candidates
                       if isinstance(n, dict) and
                       "<!--" + row["card_key"] + "-->" in str(
                           n.get("fields", {}).get("Front", {}).get("value", ""))]
            if len(matched) > 1:
                raise RuntimeError("Duplicate legacy pilot key; no write")
            if matched:
                candidate_id = matched[0].get("noteId")
                if not isinstance(candidate_id, int):
                    raise RuntimeError("Legacy pilot note ID unverified")
                verify_note(candidate_id, row)
                return candidate_id
    return None


def current_row(sheet, index, original):
    rows = sheet.get("%s!A%d:L%d" % (TAB, index, index))
    if len(rows) != 1:
        raise RuntimeError("Private queue item disappeared")
    fresh = parse_row(rows[0], index)
    # Entire release payload must remain the same, including QA assertion.
    if any(fresh[k] != original[k] for k in HEADER):
        raise RuntimeError("Private queue changed during import; stopped")
    return fresh


def write_receipt(sheet, index, note_id, sha):
    a1 = "%s!J%d:L%d" % (TAB, index, index)
    result = checked_json(sheet.session.put(
        "%s/%s" % (sheet.root, quote(a1, safe="!:")),
        params={"valueInputOption": "RAW"},
        json={"range": a1, "majorDimension": "ROWS",
              "values": [["IMPORTED", str(note_id), sha]]},
        timeout=30,
    ))
    if result.get("updatedCells") != 3:
        raise RuntimeError("Private import receipt not confirmed")
    read = sheet.get(a1)
    if len(read) != 1 or [str(x) for x in read[0]] != ["IMPORTED", str(note_id), sha]:
        raise RuntimeError("Private import receipt readback mismatch")


def process(sheet, max_cards=MAX_PER_RUN):
    verify_header(sheet)
    raw = sheet.get(TAB + "!A2:L")
    if len(raw) > MAX_QUEUE_ROWS:
        raise RuntimeError("Queue exceeds bounded import limit")
    if len(raw) != len([r for r in raw if isinstance(r, list) and r]):
        raise RuntimeError("Queue contains empty or malformed rows")
    entries = [parse_row(row, i) for i, row in enumerate(raw, 2)]
    seen = set()
    for row in entries:
        key = row["card_key"]
        if not key or key in seen or not KEY_RE.fullmatch(key):
            raise RuntimeError("Duplicate or invalid private card key")
        seen.add(key)
    pending = [row for row in entries
               if row["import_status"] == "PENDING" and row["release_status"] == "READY_TO_IMPORT"]
    if not pending:
        return 0, 0
    pending = pending[:max_cards]
    # Whole bounded batch preflight before any Anki write.
    approved = [(row, *validate_ready(row)) for row in pending]
    version = local_anki("version")
    if not isinstance(version, int) or version < 6:
        raise RuntimeError("AnkiConnect v6 unavailable")
    models = local_anki("modelNames")
    if not isinstance(models, list) or any(
            model not in models for _, _, _, model, _ in approved):
        raise RuntimeError("Required Anki Basic/Cloze note type unavailable")
    decks = local_anki("deckNames")
    if not isinstance(decks, list):
        raise RuntimeError("Local Anki decks unavailable")
    imported, recovered = 0, 0
    for row, stable_tag, tags, model, fields in approved:
        current_row(sheet, row["_row"], row)
        old = existing_note(row, stable_tag)
        if old is not None:
            note_id = old
            recovered += 1
        else:
            if row["deck"] not in decks:
                local_anki("createDeck", deck=row["deck"])
                decks.append(row["deck"])
            note_id = local_anki("addNote", note={
                "deckName": row["deck"], "modelName": model,
                "fields": fields,
                "tags": tags, "options": {"allowDuplicate": False},
            })
            if not isinstance(note_id, int) or note_id <= 0:
                raise RuntimeError("Anki addNote did not return a valid note ID")
            confirmed = verify_note(note_id, row)
            if stable_tag not in confirmed.get("tags", []):
                raise RuntimeError("New Anki stable-tag readback failed")
            imported += 1
        # If cloud write fails after local add, next run recovers the Anki note.
        write_receipt(sheet, row["_row"], note_id, row["content_sha256"])
    return imported, recovered


def private_sheet(base):
    config = load_json(base / CONFIG_NAME, required=True)
    if config.get("tab") != "Error_Events":
        raise RuntimeError("Existing private Sheet target differs")
    return Sheets(authorized_session(base), config["spreadsheet_id"]), config["spreadsheet_id"]


def ensure_tab(sheet, sid):
    # One-time init, only inside the already configured owner's spreadsheet.
    root = "https://sheets.googleapis.com/v4/spreadsheets/" + quote(sid, safe="")
    meta = checked_json(sheet.session.get(root, params={"fields": "sheets.properties.title"}, timeout=20))
    titles = [x.get("properties", {}).get("title") for x in meta.get("sheets", [])]
    if TAB not in titles:
        checked_json(sheet.session.post(root + ":batchUpdate",
            json={"requests": [{"addSheet": {"properties": {"title": TAB}}}]}, timeout=30))
        a1 = TAB + "!A1:L1"
        result = checked_json(sheet.session.put(
            sheet.root + "/" + quote(a1, safe="!:"),
            params={"valueInputOption": "RAW"},
            json={"range": a1, "majorDimension": "ROWS", "values": [HEADER]},
            timeout=30))
        if result.get("updatedCells") != len(HEADER):
            raise RuntimeError("Private queue header creation not confirmed")
    verify_header(sheet)


def run(base, action):
    private_dir(base)
    if action == "disable":
        private_write(base / CONFIG, {"schema": 1, "enabled": False})
        return "ALE_AUTOIMPORT_DISABLED"
    if action == "status":
        optin = load_json(base / CONFIG)
        return "ALE_AUTOIMPORT_ENABLED" if optin.get("enabled") is True else "ALE_AUTOIMPORT_DISABLED"
    if action == "enable":
        sheet, sid = private_sheet(base)
        ensure_tab(sheet, sid)
        private_write(base / CONFIG, {"schema": 1, "enabled": True})
        return "ALE_AUTOIMPORT_ENABLED | owner-private queue verified"
    if action != "run":
        raise ValueError("Unknown action")
    if load_json(base / CONFIG).get("enabled") is not True:
        return "ALE_AUTOIMPORT_DISABLED | no Anki write"
    fd = os.open(str(base / LOCK_NAME), os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        sheet, _ = private_sheet(base)
        new, recovered = process(sheet)
    finally:
        os.close(fd)
    return "ALE_AUTOIMPORT_VERIFIED | new=%d | reconciled=%d" % (new, recovered)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Opt-in private ALE queue -> local Anki add-only import")
    parser.add_argument("action", choices=["enable", "disable", "status", "run"])
    parser.add_argument("--private-dir", type=Path, default=BASE)
    args = parser.parse_args(argv)
    try:
        print(run(args.private_dir.expanduser(), args.action))
        return 0
    except Exception:
        # Never print private card bodies, medical notes, or remote Sheet IDs.
        print("ALE_AUTOIMPORT_NOT_VERIFIED | inspect owner-private setup", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
