#!/usr/bin/env python3
"""Persist ALE *candidate* learning deltas across independent invocations.

Never confuses a stored proposal with verified knowledge or learner mastery.
The caller owns the storage path; do not put private records on public GitHub.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from ale_learning_delta import compare_updates

SCHEMA = 'ale-learning-checkpoint-v0'


def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False,
                         separators=(',', ':'), allow_nan=False).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def _finalize(state: dict) -> dict:
    value = dict(state)
    value['checkpoint_sha256'] = _digest(value)
    return value


def validate(state: dict) -> None:
    if not isinstance(state, dict) or state.get('schema') != SCHEMA:
        raise ValueError('invalid checkpoint schema')
    expected = state.get('checkpoint_sha256')
    if not isinstance(expected, str) or len(expected) != 64:
        raise ValueError('missing checkpoint checksum')
    content = {k: v for k, v in state.items() if k != 'checkpoint_sha256'}
    if _digest(content) != expected:
        raise ValueError('checkpoint checksum mismatch')
    if (not isinstance(state.get('sequence'), int) or
            isinstance(state['sequence'], bool) or state['sequence'] < 0):
        raise ValueError('invalid sequence')
    if state.get('stage') != 'CANDIDATE_ONLY_PENDING_SEMANTIC_QA':
        raise ValueError('verified status is not supported by this gate')
    if not isinstance(state.get('evidence_sha256'), str) or len(state['evidence_sha256']) != 64:
        raise ValueError('invalid evidence reference')


def initialize(before: dict) -> dict:
    # Validate structure at the first observation, without promoting concepts.
    compare_updates(before, before)
    return _finalize({
        'schema': SCHEMA,
        'sequence': 0,
        'evidence_sha256': _digest(before),
        'previous_checkpoint_sha256': None,
        'stage': 'CANDIDATE_ONLY_PENDING_SEMANTIC_QA',
        'last_delta': None,
        'independent_semantic_verification': False,
        'learning_gain': 'NOT_MEASURED',
        'memory_promotions_performed': 0,
    })


def advance(state: dict, before: dict, after: dict, expected_sha256: str) -> dict:
    validate(state)
    if expected_sha256 != state['checkpoint_sha256']:
        raise ValueError('stale checkpoint lease / expected SHA mismatch')
    if _digest(before) != state['evidence_sha256']:
        raise ValueError('checkpoint does not match before evidence')
    diff = compare_updates(before, after)
    if diff['before_sha256'] != state['evidence_sha256']:
        raise ValueError('delta and checkpoint evidence mismatch')
    if diff['before_sha256'] == diff['after_sha256']:
        return state  # no write or new artificial learning event
    return _finalize({
        'schema': SCHEMA,
        'sequence': state['sequence'] + 1,
        'evidence_sha256': diff['after_sha256'],
        'previous_checkpoint_sha256': state['checkpoint_sha256'],
        'stage': 'CANDIDATE_ONLY_PENDING_SEMANTIC_QA',
        'last_delta': {
            'state': diff['state'],
            'actions': diff['actions'],
            'action_count': diff['action_count'],
        },
        'independent_semantic_verification': False,
        'learning_gain': 'NOT_MEASURED',
        'memory_promotions_performed': 0,
    })


def load(path: Path) -> dict:
    state = json.loads(path.read_text(encoding='utf-8'))
    validate(state)
    return state


def persist(path: Path, candidate: dict, expected_sha256: str | None) -> None:
    """Non-forcing exclusive lock and compare-and-swap plus atomic replace.

    Creates only local caller-selected files. Never silently steals a stale lock.
    """
    validate(candidate)
    path = Path(path)
    if not path.parent.is_dir():
        raise ValueError('checkpoint parent directory must exist')
    lock = path.with_name(path.name + '.lock')
    fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.close(fd)
        exists = path.exists()
        if expected_sha256 is None:
            if exists:
                raise ValueError('checkpoint already exists; refuse overwrite')
            if candidate['sequence'] != 0:
                raise ValueError('initial checkpoint must be sequence zero')
        else:
            if not exists:
                raise ValueError('expected checkpoint is missing')
            current = load(path)
            if current['checkpoint_sha256'] != expected_sha256:
                raise ValueError('checkpoint changed: CAS conflict')
            if candidate['previous_checkpoint_sha256'] != expected_sha256:
                raise ValueError('candidate does not extend expected checkpoint')
            if candidate['sequence'] != current['sequence'] + 1:
                raise ValueError('checkpoint sequence must advance exactly once')
        scratch = None
        try:
            with tempfile.NamedTemporaryFile('w', encoding='utf-8',
                    dir=str(path.parent), prefix=path.name + '.tmp-',
                    delete=False) as out:
                scratch = Path(out.name)
                os.chmod(scratch, 0o600)
                json.dump(candidate, out, ensure_ascii=False, indent=2, allow_nan=False)
                out.write('\n')
                out.flush()
                os.fsync(out.fileno())
            # Do not follow existing symlinks or replace another unexpected file.
            if path.is_symlink():
                raise ValueError('checkpoint path cannot be symlink')
            os.replace(scratch, path)
            scratch = None
        finally:
            if scratch is not None:
                scratch.unlink(missing_ok=True)
    finally:
        lock.unlink(missing_ok=True)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checkpoint', type=Path, required=True)
    p.add_argument('--before', type=Path, required=True)
    p.add_argument('--after', type=Path)
    p.add_argument('--expected-sha256', type=str)
    p.add_argument('--initialize', action='store_true')
    p.add_argument('--write', action='store_true',
                   help='Explicitly save proposal-only state to the local path')
    args = p.parse_args()
    before = json.loads(args.before.read_text(encoding='utf-8'))
    if args.initialize:
        if args.after is not None or args.expected_sha256 is not None:
            p.error('initialize accepts only --before')
        result = initialize(before)
        expected = None
    else:
        if not args.after or not args.expected_sha256:
            p.error('update requires --after and --expected-sha256')
        previous = load(args.checkpoint)
        result = advance(previous, before,
                         json.loads(args.after.read_text(encoding='utf-8')),
                         args.expected_sha256)
        expected = args.expected_sha256
    if args.write:
        if not args.initialize and result['checkpoint_sha256'] == expected:
            print(json.dumps({'state': 'NO_CHANGE', 'checkpoint_sha256': expected}))
            return
        persist(args.checkpoint, result, expected)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
