#!/usr/bin/env python3
"""ALE-01: Mac-only Anki (read-only) -> owner-private Google Sheet bridge.

Do NOT execute in public GitHub Actions or in Codex Cloud. This script does not
modify Anki, call AnkiWeb sync, or expose a local AnkiConnect port remotely.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.parse import quote

from ale_anki_readonly import invoke, recent_reviews, check_version

BASE = Path.home() / "Library" / "Application Support" / "ClinicalOS-ALE"
CONFIG_NAME = "drive_sync_config.json"
CLIENT_NAME = "google_oauth_client.json"
TOKEN_NAME = "google_oauth_token.json"
STATE_NAME = "drive_sync_state.json"
LOCK_NAME = "drive_sync.lock"
SCOPE = "https://www.googleapis.com/auth/spreadsheets"
TAB = "Error_Events"
HEADER = [
    "event_key", "review_timestamp", "anki_card_id", "anki_note_id",
    "concept_family_id", "rating", "cause_code", "cause_source",
    "actual_exposures", "diagnosis_status", "intervention_type",
    "source_review_id", "sync_status", "recorded_at",
]
SHEET_URL_RE = re.compile(r"^https://docs\.google\.com/spreadsheets/d/([A-Za-z0-9_-]+)(?:/.*)?$")
ID_RE = re.compile(r"^[A-Za-z0-9_-]{20,}$")


def private_dir(base: Path) -> None:
    if base.is_symlink():
        raise RuntimeError("Private data directory must not be a symlink")
    base.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(base, 0o700)


def private_write(path: Path, payload: dict) -> None:
    private_dir(path.parent)
    if path.exists() and path.is_symlink():
        raise RuntimeError("Private file must not be a symlink")
    temp = path.with_name(path.name + ".tmp")
    if temp.exists() and temp.is_symlink():
        raise RuntimeError("Temporary file must not be a symlink")
    fd = os.open(str(temp), os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
        os.chmod(path, 0o600)
    finally:
        if temp.exists():
            temp.unlink()


def load_json(path: Path, required=False) -> dict:
    if not path.exists():
        if required:
            raise RuntimeError("Local setup missing; run configure / authorize")
        return {}
    if path.is_symlink() or (path.stat().st_mode & 0o077):
        raise RuntimeError("Private credential/config file permissions are too open")
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError("Invalid private local JSON state")
    return obj


def parse_spreadsheet_id(raw: str) -> str:
    raw = raw.strip()
    match = SHEET_URL_RE.match(raw)
    sid = match.group(1) if match else raw
    if not ID_RE.fullmatch(sid):
        raise ValueError("Enter an existing native Google Sheet URL or spreadsheet ID")
    return sid


def configure(base: Path, sheet_url: str | None, client_path: str | None) -> None:
    private_dir(base)
    sheet_url = sheet_url or input("Paste the owner-only Google Sheet URL: ")
    sid = parse_spreadsheet_id(sheet_url)
    client_file = Path(client_path).expanduser() if client_path else Path(input("Path to Google Desktop OAuth client JSON: ").strip()).expanduser()
    if not client_file.is_file():
        raise RuntimeError("Desktop OAuth JSON file not found")
    client = json.loads(client_file.read_text(encoding="utf-8"))
    if "installed" not in client or "client_id" not in client["installed"]:
        raise RuntimeError("Google OAuth client must be of type Desktop app (installed)")
    previous = load_json(base / CONFIG_NAME)
    if previous.get("spreadsheet_id") and previous["spreadsheet_id"] != sid:
        raise RuntimeError("Different spreadsheet target requires explicit migration")
    dest = base / CLIENT_NAME
    if dest.is_symlink():
        raise RuntimeError("OAuth credentials destination cannot be symlink")
    fd = os.open(str(dest), os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(client, handle)
    os.chmod(dest, 0o600)
    private_write(base / CONFIG_NAME, {"schema": 1, "spreadsheet_id": sid, "tab": TAB})
    print("LOCAL_CONFIG_OK | OAuth client and sheet target stored on this Mac only")


def credentials(base: Path, interactive: bool):
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError as exc:
        raise RuntimeError("Install dependencies from tools/requirements-ale.txt") from exc
    token_path = base / TOKEN_NAME
    client_path = base / CLIENT_NAME
    if not client_path.is_file():
        raise RuntimeError("OAuth Desktop client missing; run configure")
    if token_path.exists():
        load_json(token_path, required=True)  # enforce private file permissions
    creds = Credentials.from_authorized_user_file(str(token_path), [SCOPE]) if token_path.exists() else None
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif interactive:
        flow = InstalledAppFlow.from_client_secrets_file(str(client_path), scopes=[SCOPE])
        creds = flow.run_local_server(host="127.0.0.1", port=0, open_browser=True,
            access_type="offline", prompt="consent")
    else:
        raise RuntimeError("OAuth is not ready; run authorize on this Mac")
    if not creds or not creds.valid:
        raise RuntimeError("OAuth credential invalid")
    private_write(token_path, json.loads(creds.to_json()))
    return creds


def authorized_session(base: Path):
    from google.auth.transport.requests import AuthorizedSession
    return AuthorizedSession(credentials(base, interactive=False))


def checked_json(response):
    if response.status_code >= 400:
        raise RuntimeError(f"Google Sheets request failed (HTTP {response.status_code})")
    return response.json()


class Sheets:
    """One configured spreadsheet; cannot list files in Drive."""
    def __init__(self, session, sheet_id: str):
        self.session = session
        self.root = f"https://sheets.googleapis.com/v4/spreadsheets/{quote(sheet_id, safe='')}/values"

    def get(self, a1: str) -> list:
        result = checked_json(self.session.get(
            f"{self.root}/{quote(a1, safe='!:')}",
            params={"valueRenderOption": "UNFORMATTED_VALUE"}, timeout=20))
        rows = result.get("values", [])
        if not isinstance(rows, list):
            raise RuntimeError("Invalid Google Sheets response")
        return rows

    def append(self, rows: list[list[str]]) -> None:
        if not rows:
            return
        result = checked_json(self.session.post(
            f"{self.root}/{quote(TAB+'!A:N', safe='!:')}:append",
            params={"valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS"},
            json={"majorDimension": "ROWS", "values": rows}, timeout=30))
        if result.get("updates", {}).get("updatedRows") != len(rows):
            raise RuntimeError("Append count unconfirmed; retry reconciles event keys")

    def verify_schema(self) -> None:
        rows = self.get(f"{TAB}!A1:N1")
        if not rows or [str(x) for x in rows[0]] != HEADER:
            raise RuntimeError("Private Error_Events schema does not match 14-column contract")

    def existing_ids(self) -> list[str]:
        return [str(row[0]) for row in self.get(f"{TAB}!A2:A") if row and row[0]]


def event_key(row: list) -> str:
    if len(row) != 9 or not isinstance(row[0], int) or not isinstance(row[1], int):
        raise RuntimeError("Invalid Anki review event shape")
    return f"anki-revlog:{row[0]}:{row[1]}"


def event_rows(events: list[list], note_ids: dict[int, int | None], now_iso: str) -> list[list[str]]:
    rows = []
    for ev in events:
        stamp, card_id, _, button = ev[:4]
        if not isinstance(button, int) or button not in (1, 2, 3, 4):
            raise RuntimeError("Invalid Anki review button")
        note = note_ids.get(card_id)
        rows.append([
            event_key(ev), datetime.fromtimestamp(stamp / 1000, tz=timezone.utc).isoformat(),
            str(card_id), str(note) if note else "", "", str(button), "UNKNOWN",
            "NOT_COLLECTED", "", "NOT_DIAGNOSED", "", str(stamp),
            "SYNCED_READ_ONLY", now_iso
        ])
    return rows


def note_mapping(events: list[list]) -> dict[int, int | None]:
    cids = sorted({ev[1] for ev in events})
    mapping: dict[int, int | None] = {x: None for x in cids}
    for i in range(0, len(cids), 100):
        info = invoke("cardsInfo", cards=cids[i:i + 100])
        if not isinstance(info, list):
            raise RuntimeError("Anki cardsInfo response invalid")
        for card in info:
            if not isinstance(card, dict):
                raise RuntimeError("Anki card structure invalid")
            cid, note = card.get("cardId"), card.get("note")
            if cid in mapping and isinstance(note, int):
                mapping[cid] = note
    return mapping


def synchronize(base: Path, sheet: Sheets, lookback_days=7) -> dict:
    private_dir(base)
    state_path = base / STATE_NAME
    state = load_json(state_path)
    check_version()
    decks = invoke("deckNames")
    if not isinstance(decks, list):
        raise RuntimeError("Invalid Anki deck inventory")
    now_ms = int(time.time() * 1000)
    previous = int(state.get("last_verified_review_ms", 0))
    start_ms = max(0, previous - 1) if previous else now_ms - int(lookback_days * 86400000)
    events = recent_reviews(decks, start_ms)
    if len(events) > 12000:
        raise RuntimeError("Too many review events; reduce initial lookback")
    sheet.verify_schema()
    old_ids = sheet.existing_ids()
    if len(old_ids) != len(set(old_ids)):
        raise RuntimeError("Private sheet contains duplicate event keys; stop and reconcile")
    old_set = set(old_ids)
    fresh = [e for e in events if event_key(e) not in old_set]
    linked = 0
    if fresh:
        mapping = note_mapping(fresh)
        linked = sum(note is not None for note in mapping.values())
        now_iso = datetime.now(timezone.utc).isoformat()
        rows = event_rows(fresh, mapping, now_iso)
        for i in range(0, len(rows), 200):
            sheet.append(rows[i:i+200])
        after = sheet.existing_ids()
        if len(after) != len(set(after)) or not {r[0] for r in rows}.issubset(set(after)):
            raise RuntimeError("Google Sheets readback mismatch; cursor NOT advanced")
    if events:
        previous = max(previous, max(ev[0] for ev in events))
    private_write(state_path, {"schema": 1, "last_verified_review_ms": previous,
        "last_completed_at": datetime.now(timezone.utc).isoformat()})
    return {"new_events_uploaded": len(fresh),
            "already_present": len(events) - len(fresh),
            "unique_cards_linked_to_notes": linked}



def audit_private_sheet(sheet: Sheets) -> dict:
    """Read-only integrity gate; emits aggregate counts only, no private IDs."""
    sheet.verify_schema()
    rows = sheet.get(f"{TAB}!A2:N")
    seen = set()
    unmapped = 0
    for row in rows:
        if not isinstance(row, list) or len(row) != len(HEADER):
            raise RuntimeError("Invalid private review row width")
        key, review_at, card_id, note_id, family_id, rating = row[:6]
        if not isinstance(key, str):
            raise RuntimeError("Invalid private review event key")
        match = re.fullmatch(r"anki-revlog:(\d+):(\d+)", key)
        if not match or str(row[11]) != match.group(1) or str(card_id) != match.group(2):
            raise RuntimeError("Private review event identity mismatch")
        if key in seen:
            raise RuntimeError("Duplicate private review event detected")
        seen.add(key)
        if not str(card_id).isdigit() or (str(note_id) and not str(note_id).isdigit()):
            raise RuntimeError("Invalid private Anki identifiers")
        if str(rating) not in ("1", "2", "3", "4"):
            raise RuntimeError("Invalid private review rating")
        if str(row[12]) != "SYNCED_READ_ONLY":
            raise RuntimeError("Unverified private sync status")
        try:
            review_dt = datetime.fromisoformat(str(review_at).replace("Z", "+00:00"))
            written_dt = datetime.fromisoformat(str(row[13]).replace("Z", "+00:00"))
        except ValueError as exc:
            raise RuntimeError("Invalid private review timestamps") from exc
        if review_dt.tzinfo is None or written_dt.tzinfo is None or written_dt < review_dt:
            raise RuntimeError("Private review timestamps out of order")
        if not str(family_id):
            unmapped += 1
    return {"events": len(rows), "unique_events": len(seen), "unmapped_family": unmapped}


def command_audit(base: Path) -> None:
    config = load_json(base / CONFIG_NAME, required=True)
    if config.get("tab") != TAB:
        raise RuntimeError("Config target tab mismatch")
    sheet = Sheets(authorized_session(base), config["spreadsheet_id"])
    result = audit_private_sheet(sheet)
    print("OWNER_PRIVATE_AUDIT_PASS | events=" + str(result["events"])
          + " | duplicates=0 | missing_family_links=" + str(result["unmapped_family"]))
    print("Private event/card IDs and record contents are not displayed.")


def command_sync(base: Path, lookback_days: int) -> None:
    config = load_json(base / CONFIG_NAME, required=True)
    if config.get("tab") != TAB:
        raise RuntimeError("Config target tab mismatch")
    sheet = Sheets(authorized_session(base), config["spreadsheet_id"])
    private_dir(base)
    fd = os.open(str(base / LOCK_NAME), os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        result = synchronize(base, sheet, lookback_days)
    except BlockingIOError as exc:
        raise RuntimeError("Another local ALE sync is running") from exc
    finally:
        os.close(fd)
    print("OWNER_PRIVATE_SYNC_OK | new_review_events=" + str(result["new_events_uploaded"]))
    print("DUPLICATE_SAFE | already_recorded=" + str(result["already_present"]))
    print("Concept Family mapping and GPT decisions are NOT yet implemented")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Mac-only Anki -> owner-private Google Sheet sync")
    parser.add_argument("command", choices=("configure", "authorize", "sync", "audit", "status"))
    parser.add_argument("--oauth-json", help="Google Desktop OAuth JSON; configure only")
    parser.add_argument("--sheet", help="Existing owner-only Google Sheet URL; configure only")
    parser.add_argument("--lookback-days", type=int, default=7)
    parser.add_argument("--private-dir", type=Path, default=BASE)
    args = parser.parse_args(argv)
    base = args.private_dir.expanduser()
    try:
        if args.command == "configure":
            configure(base, args.sheet, args.oauth_json)
        elif args.command == "authorize":
            load_json(base / CONFIG_NAME, required=True)
            credentials(base, interactive=True)
            print("LOCAL_GOOGLE_OAUTH_OK | Token stored only on owner Mac")
        elif args.command == "audit":
            command_audit(base)
        elif args.command == "sync":
            if not 1 <= args.lookback_days <= 90:
                raise ValueError("lookback-days must be 1 to 90")
            command_sync(base, args.lookback_days)
        else:
            c, s = load_json(base / CONFIG_NAME), load_json(base / STATE_NAME)
            print("LOCAL_STATUS | configured=" + str(bool(c)) + " | synced_once=" + str(bool(s)))
        return 0
    except Exception as exc:
        print("ALE_SYNC_NOT_VERIFIED | " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
