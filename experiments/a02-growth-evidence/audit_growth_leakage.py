#!/usr/bin/env python3
"""Standalone, synthetic-only, fail-closed development data boundary audit.

Independent Clinical OS research prototype. No external assets, clinical cases,
model calls, authenticated provenance claims, or main/scheduler modifications.
"""
from collections import Counter, defaultdict
from datetime import datetime
import json
import sys

SPLITS = frozenset(('train', 'development', 'holdout'))
FIELDS = frozenset(('id', 'family_id', 'split', 'decision_at',
                    'evidence_available_at', 'evidence_observed_at',
                    'label_mature_at'))


def clock(value):
    if not isinstance(value, str):
        raise ValueError('TIMESTAMP_MUST_BE_STRING')
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ValueError('TIMESTAMP_INVALID') from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError('TIMESTAMP_TIMEZONE_MISSING')
    return parsed


def audit(payload):
    if not isinstance(payload, dict) or set(payload) != {
        'schema_version', 'protocol_frozen_at', 'model_fit_at',
        'evaluation_started_at', 'cases'} or type(payload['schema_version']) is not int or payload['schema_version'] != 1:
        raise ValueError('AUDIT_SCHEMA_INVALID')
    frozen = clock(payload['protocol_frozen_at'])
    fit = clock(payload['model_fit_at'])
    started = clock(payload['evaluation_started_at'])
    if not frozen <= fit <= started:
        raise ValueError('PROTOCOL_FIT_EVAL_CLOCK_ORDER')
    cases = payload['cases']
    if not isinstance(cases, list) or len(cases) < 3:
        raise ValueError('CASE_SET_INSUFFICIENT')
    seen_ids = set()
    families = defaultdict(set)
    counts = Counter()
    violations = []
    for row_index, case in enumerate(cases):
        if not isinstance(case, dict) or set(case) != FIELDS:
            raise ValueError('CASE_SCHEMA_INVALID')
        for k in ('id','family_id'):
            if not isinstance(case[k], str) or not case[k].strip() or case[k].strip() != case[k]:
                raise ValueError('CASE_KEY_INVALID')
        if case['id'] in seen_ids:
            raise ValueError('CASE_ID_DUPLICATE')
        seen_ids.add(case['id'])
        split = case['split']
        if not isinstance(split, str) or split not in SPLITS:
            raise ValueError('SPLIT_INVALID')
        counts[split] += 1
        families[case['family_id']].add(split)
        decision = clock(case['decision_at'])
        available = clock(case['evidence_available_at'])
        observed = clock(case['evidence_observed_at'])
        mature = clock(case['label_mature_at'])
        if available > decision or observed > decision:
            violations.append({'case_id':case['id'], 'code':'FUTURE_OR_LATE_EVIDENCE'})
        if available > observed:
            violations.append({'case_id':case['id'], 'code':'OBSERVATION_BEFORE_AVAILABILITY'})
        if mature <= decision:
            violations.append({'case_id':case['id'], 'code':'LABEL_NOT_POST_DECISION'})
        if split == 'train' and mature > fit:
            violations.append({'case_id':case['id'], 'code':'TRAIN_LABEL_NOT_MATURE_AT_FIT'})
    for family_id, groups in sorted(families.items()):
        if len(groups) != 1:
            violations.append({'family_id':family_id,'code':'FAMILY_CROSS_SPLIT'})
    for split in SPLITS:
        if counts[split] == 0:
            violations.append({'split':split,'code':'SPLIT_EMPTY'})
    return {
        'evidence_level':'SYNTHETIC_STRUCTURAL_AUDIT_ONLY',
        'status': 'REJECT' if violations else 'STRUCTURALLY_ELIGIBLE_NOT_VALIDATED',
        'cases_checked':len(cases),
        'split_counts':{k:counts[k] for k in sorted(SPLITS)},
        'violations':violations,
        'clinical_validated':False,
        'independent_holdout_authenticated':False,
        'growth_score_change_authorized':False,
        'limitations':('Family IDs and timestamps are caller-provided and not authenticated. '
                       'This does not detect paraphrase aliases, pretraining contamination, '
                       'judge bias, held-out answer exposure, or actual model behavior.')
    }


def main(argv):
    if len(argv) != 2:
        print('Usage: python audit_growth_leakage.py input.json', file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding='utf-8') as stream:
            result = audit(json.load(stream))
    except (ValueError, TypeError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({'status':'INVALID_INPUT','reason':str(exc)}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['status'] == 'REJECT' else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

