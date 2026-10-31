#!/usr/bin/env python3
"""Owner-Mac: strict Anki-tag -> provisional private ALE family candidate.

Only exact existing structured tags qualify, never reviews/ratings alone.
No Anki mutations, no private card/question contents in logs or public CI.
Prior owner-skipped cards are excluded across concept catalog revisions.
"""
from __future__ import annotations
from datetime import datetime, timezone
import fcntl
import os
from pathlib import Path
import sys
from urllib.parse import quote

from ale_anki_readonly import check_version, invoke
from ale_anki_drive_sync import (BASE, CONFIG_NAME, LOCK_NAME, Sheets,
    authorized_session, checked_json, load_json, private_dir)
from ale_autonomy_core import (persistent_skipped_ids, exact_tag_candidate,
    choose_next_lesson)

MAP_TAB = 'Card_Concept_Map'
MAP_HEADER = ['stable_note_id','anki_note_id','anki_card_ids','concept_id',
              'claim_type','relation','card_state','source_ref',
              'last_review_event_id','last_observed','confirmed_mapping']


def candidate_row(c: dict) -> list[str]:
    return ['', c['note_id'], c['card_id'], c['concept_id'],
        'AUTO_STRUCTURED_TAG_CANDIDATE', 'TESTS_THIS_CARD_DIRECTION_UNVERIFIED',
        'CANDIDATE_ONLY', 'LOCAL_EXACT_ANKI_TAG', c['event_key'],
        datetime.now(timezone.utc).isoformat(), 'UNCONFIRMED_AUTO_TAG']


def run(base: Path) -> tuple[int,str]:
    private_dir(base)
    conf = load_json(base / CONFIG_NAME, required=True)
    if conf.get('tab') != 'Error_Events':
        raise ValueError('Private ALE config tab mismatch')
    sheet = Sheets(authorized_session(base), conf['spreadsheet_id'])
    sheet.verify_schema()
    if sheet.get(f'{MAP_TAB}!A1:K1') != [MAP_HEADER]:
        raise ValueError('Private map header mismatch; no writes')
    events = sheet.get('Error_Events!A2:N')
    mappings = sheet.get(f'{MAP_TAB}!A2:K')
    concepts = sheet.get('Concepts!A2:J')
    actions = sheet.get('Next_Actions!A2:G')
    allowed = {str(r[0]) for r in concepts if r and str(r[0])}
    skipped = persistent_skipped_ids(load_json(base / 'concept_map_skips.json'))
    # Known mapping includes *proposals*; never duplicate a provisional entry.
    seen = {card.strip() for row in mappings if len(row) >= 3
            for card in str(row[2]).split(',') if card.strip()}
    check_version()
    candidates = []
    for event in events[-100:]:
        if len(event) < 14 or not str(event[2]).isdigit():
            continue
        cid = str(event[2])
        if cid in skipped or cid in seen:
            continue
        info = invoke('cardsInfo', cards=[int(cid)])
        if not isinstance(info,list) or len(info) != 1:
            continue
        proposed = exact_tag_candidate(event, info[0], allowed, skipped, seen)
        if proposed:
            candidates.append(proposed)
            seen.add(cid)
    # One exclusive lock covers refreshing the remote map and verified append.
    fd = os.open(str(base / LOCK_NAME), os.O_CREAT | os.O_RDWR, 0o600)
    count = 0
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        latest = sheet.get(f'{MAP_TAB}!A2:K')
        known = {c.strip() for row in latest if len(row) >= 3
                 for c in str(row[2]).split(',') if c.strip()}
        for candidate in candidates:
            if candidate['card_id'] in known:
                continue
            row = candidate_row(candidate)
            answer = checked_json(sheet.session.post(
                f"{sheet.root}/{quote(MAP_TAB+'!A:K',safe='!:')}:append",
                params={'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS'},
                json={'majorDimension':'ROWS','values':[row]},timeout=30))
            # A lost acknowledgement is not a warrant for a retry in this run.
            if answer.get('updates',{}).get('updatedRows') != 1:
                raise RuntimeError('Private candidate append unconfirmed')
            found = sheet.get(f'{MAP_TAB}!A2:K')
            if sum(len(r) >= 11 and str(r[2]) == candidate['card_id']
                   and str(r[10]) == 'UNCONFIRMED_AUTO_TAG' for r in found) != 1:
                raise RuntimeError('Private candidate readback mismatch')
            known.add(candidate['card_id'])
            count += 1
    finally:
        os.close(fd)
    # The lesson policy is computed from the live PRIVATE ledger. In this pilot,
    # the existing 09:00 Writer owns actual lesson order and private ledger edits.
    plan = choose_next_lesson(concepts, actions)
    return count, plan['status']


if __name__ == '__main__':
    try:
        count, status = run(BASE)
        print('ALE_PRIVATE_CANDIDATES_OK | added_unconfirmed=' + str(count))
        print('ALE_PRIVATE_NEXT_LESSON_PLAN | ' + status + ' | gain=NOT_MEASURED')
    except Exception:
        # No credentials, private sheet URL, IDs, tags, prompts or exception text.
        print('ALE_PRIVATE_AUTONOMY_NOT_VERIFIED | see owner-private diagnostics', file=sys.stderr)
        sys.exit(1)
