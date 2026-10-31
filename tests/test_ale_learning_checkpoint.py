"""Durability, replay and CAS checks for proposal-only ALE checkpoints."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from ale_learning_checkpoint import advance, initialize, load, persist

SIGNATURE = {'from_role': 'metric', 'to_role': 'decision',
             'missing_bridge_role': 'context'}


def sample(evidence_id, family, features):
    return {'id': evidence_id, 'family_id': family,
            'reasoning_signature': dict(SIGNATURE),
            'source_ref': 'synthetic-public/' + evidence_id,
            'source_check': 'checked', 'context_features': list(features)}


def versions():
    first = {'examples': [sample('a', 'software', ['proxy', 'needs_context']),
                          sample('b', 'finance', ['proxy', 'needs_context'])],
             'challenges': []}
    second = copy.deepcopy(first)
    second['challenges'].append(sample('c', 'other', ['narrow_target']))
    third = copy.deepcopy(second)
    third['challenges'].append(sample('d', 'other', ['proxy', 'needs_context']))
    return first, second, third


class DurableLearningCheckpointTests(unittest.TestCase):
    def test_checkpoint_survives_readback_and_two_new_processes(self):
        a, b, c = versions()
        with tempfile.TemporaryDirectory() as home:
            root = Path(home)
            for name, packet in [('a', a), ('b', b), ('c', c)]:
                (root / (name + '.json')).write_text(json.dumps(packet), encoding='utf-8')
            path = root / 'state.json'
            cli = str(ROOT / 'tools' / 'ale_learning_checkpoint.py')
            def run(*args):
                result = subprocess.run([sys.executable, cli,
                                         '--checkpoint', str(path), *args],
                                        capture_output=True, text=True, check=True)
                return json.loads(result.stdout)
            initial = run('--initialize', '--before', str(root / 'a.json'), '--write')
            self.assertEqual(initial['sequence'], 0)
            self.assertEqual(load(path)['checkpoint_sha256'], initial['checkpoint_sha256'])
            following = run('--before', str(root / 'a.json'),
                            '--after', str(root / 'b.json'),
                            '--expected-sha256', initial['checkpoint_sha256'], '--write')
            self.assertEqual(following['sequence'], 1)
            self.assertIn('PROPOSE_SCOPED_HYPOTHESIS',
                          [a['action'] for a in following['last_delta']['actions']])
            final = run('--before', str(root / 'b.json'),
                        '--after', str(root / 'c.json'),
                        '--expected-sha256', following['checkpoint_sha256'], '--write')
            self.assertEqual(final['sequence'], 2)
            self.assertEqual(final['previous_checkpoint_sha256'], following['checkpoint_sha256'])
            self.assertIn('WITHDRAW_SCOPE_HYPOTHESIS',
                          [a['action'] for a in final['last_delta']['actions']])
            self.assertEqual(load(path), final)
            self.assertFalse(final['independent_semantic_verification'])
            self.assertEqual(final['learning_gain'], 'NOT_MEASURED')
            self.assertEqual(final['memory_promotions_performed'], 0)

    def test_repeat_evidence_is_noop_not_artificial_new_learning(self):
        a, _, _ = versions()
        first = initialize(a)
        self.assertIs(advance(first, a, copy.deepcopy(a), first['checkpoint_sha256']), first)

    def test_reject_stale_expected_sha_and_wrong_before_packet(self):
        a, b, c = versions()
        initial = initialize(a)
        with self.assertRaisesRegex(ValueError, 'stale checkpoint'):
            advance(initial, a, b, '0' * 64)
        with self.assertRaisesRegex(ValueError, 'does not match before'):
            advance(initial, c, b, initial['checkpoint_sha256'])

    def test_reject_tampered_checkpoint_before_interpreting_it(self):
        a, _, _ = versions()
        with tempfile.TemporaryDirectory() as home:
            path = Path(home) / 'checkpoint.json'
            initial = initialize(a)
            persist(path, initial, None)
            broken = json.loads(path.read_text())
            broken['stage'] = 'VERIFIED_MASTERY'
            path.write_text(json.dumps(broken))
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                load(path)

    def test_cas_prevents_overwrite_and_detects_stale_branch(self):
        a, b, _ = versions()
        with tempfile.TemporaryDirectory() as home:
            path = Path(home) / 'checkpoint.json'
            old = initialize(a)
            persist(path, old, None)
            new = advance(old, a, b, old['checkpoint_sha256'])
            persist(path, new, old['checkpoint_sha256'])
            with self.assertRaisesRegex(ValueError, 'already exists'):
                persist(path, old, None)
            with self.assertRaisesRegex(ValueError, 'CAS conflict'):
                persist(path, new, old['checkpoint_sha256'])
            self.assertEqual(load(path), new)

    def test_existing_lock_blocks_concurrent_writer(self):
        a, _, _ = versions()
        with tempfile.TemporaryDirectory() as home:
            path = Path(home) / 'state.json'
            lock = Path(home) / 'state.json.lock'
            lock.write_text('other writer', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                persist(path, initialize(a), None)
            self.assertFalse(path.exists())
            self.assertEqual(lock.read_text(), 'other writer')

    def test_metadata_only_change_keeps_gain_unverified(self):
        a, _, _ = versions()
        b = copy.deepcopy(a)
        b['description'] = 'Documentation-only'
        initial = initialize(a)
        next_state = advance(initial, a, b, initial['checkpoint_sha256'])
        self.assertEqual(next_state['last_delta']['state'],
                         'METADATA_CHANGED_NO_DECISION_DELTA')
        self.assertEqual(next_state['last_delta']['action_count'], 0)
        self.assertEqual(next_state['learning_gain'], 'NOT_MEASURED')


if __name__ == '__main__':
    unittest.main()
