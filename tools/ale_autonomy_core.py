"""Private ALE decision primitives. Pure functions; no network or Anki writes.

Evidence hierarchy: an exact structured tag is an *unconfirmed* candidate;
review ratings never establish a cognitive cause, mastery or learning gain.
"""
from __future__ import annotations
import re

TAG_PREFIX = 'ale::concept::'


def persistent_skipped_ids(state: dict) -> set[str]:
    """A prior explicit skip survives any future change to the concept catalog."""
    if not state:
        return set()
    raw = state.get('skipped_cards', [])
    if not isinstance(raw, list) or any(not isinstance(v, str) or not v.isdigit() for v in raw):
        raise ValueError('Invalid private skip state; stop rather than erase skips')
    return set(raw)


def exact_tag_candidate(event: list, card: dict, allowed: set[str],
                        skipped: set[str], already_seen: set[str]) -> dict | None:
    """Only link this exact card direction, with an unconfirmed provenance label."""
    if len(event) < 14 or not re.fullmatch(r'anki-revlog:\d+:\d+', str(event[0])):
        return None
    card_id, note_id = str(event[2]), str(event[3])
    if not card_id.isdigit() or not note_id.isdigit():
        return None
    if card_id in skipped or card_id in already_seen:
        return None
    if str(card.get('cardId')) != card_id or str(card.get('note')) != note_id:
        return None
    tags = card.get('tags')
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        return None
    matching = {t[len(TAG_PREFIX):] for t in tags
                if t.lower().startswith(TAG_PREFIX) and t[len(TAG_PREFIX):] in allowed}
    if len(matching) != 1:
        return None
    return {'card_id': card_id, 'note_id': note_id, 'event_key': str(event[0]),
            'concept_id': next(iter(matching)),
            'basis': 'EXACT_ANKI_TAG_ONLY', 'confirmation': 'UNCONFIRMED_CANDIDATE'}


def choose_next_lesson(concept_rows: list[list], action_rows: list[list]) -> dict:
    """Choose a concrete next *step* without treating an unanswered task as a miss.

    Sheets rows are private. Caller must never print/commit the returned payload
    to a public CI log, PR, issue or artifact.
    """
    concepts = {str(r[0]): r for r in concept_rows if len(r) >= 10 and str(r[0])}
    pending = []
    for row in action_rows:
        if len(row) < 7 or str(row[6]).strip().lower() != 'queued':
            continue
        cid = str(row[1]).strip()
        if not cid:
            continue
        try:
            rank = int(row[0])
        except (TypeError, ValueError):
            continue
        pending.append((rank, cid, row))
    pending.sort(key=lambda x: x[0])
    if pending:
        _, cid, row = pending[0]
        eligibility = str(row[4]).lower()
        if 'source check' in eligibility or 'source verify' in eligibility:
            stage = 'VERIFY_SOURCE_BEFORE_COLD_ATTEMPT'
        elif 'restore question context' in eligibility:
            stage = 'RECOVER_ORIGINAL_CONTEXT_FIRST'
        else:
            stage = 'PREPARE_LEARNER_UNSEEN_ACTION'
        state = str(concepts.get(cid, [''] * 10)[3])
        return {'status': 'PROPOSED_NOT_COMPLETED', 'concept_id': cid,
                'action': str(row[3]), 'gate': stage,
                'knowledge_state': state or 'NOT_OBSERVED',
                'learner_gain': 'NOT_MEASURED', 'source': 'OWNER_PRIVATE_NEXT_ACTIONS'}
    # No queued actions: only an explicitly documented reasoning gap may seed
    # a repair proposal, never fabricate a wrong exam response.
    for r in concept_rows:
        if len(r) >= 10 and str(r[3]) == 'reasoning_gap' and str(r[5]).upper() == 'YES':
            return {'status': 'PROPOSED_NOT_COMPLETED', 'concept_id': str(r[0]),
                    'action': 'mechanism_repair_then_unseen_test',
                    'gate': 'RECOVER_ORIGINAL_CONTEXT_FIRST',
                    'knowledge_state': 'reasoning_gap', 'learner_gain': 'NOT_MEASURED',
                    'source': 'OWNER_PRIVATE_CONCEPTS'}
    return {'status': 'NO_VERIFIED_NEXT_STEP', 'learner_gain': 'NOT_MEASURED'}
