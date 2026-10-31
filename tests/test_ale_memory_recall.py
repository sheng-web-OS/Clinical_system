"""Across-process evidence-update to candidate-recall tests, public synthetic only."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from ale_learning_checkpoint import initialize, advance, candidate_memory, recall_candidate

SIG = {'from_role': 'proxy_signal', 'to_role': 'decision_claim', 'missing_bridge_role': 'target_validation'}


def item(name, family, features):
    return {'id': name, 'family_id': family, 'reasoning_signature': SIG.copy(),
            'source_ref': 'synthetic-public/' + name, 'source_check': 'checked',
            'context_features': features}


def packet():
    return {'classification': 'PUBLIC_SYNTHETIC_ONLY',
            'examples': [item('a', 'software', ['proxy_only', 'requires_context']),
                         item('b', 'finance', ['proxy_only', 'requires_context'])],
            'challenges': []}


class TransferRecall(unittest.TestCase):
    def test_unclassified_content_is_never_retained(self):
        p = packet()
        del p['classification']
        state = initialize(p)
        self.assertEqual(state['candidate_memory']['state'], 'NOT_RETAINED_UNCLASSIFIED')
        self.assertEqual(state['candidate_memory']['candidates'], [])

    def test_bounded_candidate_recall_without_input_packet(self):
        before = packet()
        middle = copy.deepcopy(before)
        middle['challenges'] = [item('counter', 'other', ['narrow_target'])]
        after = copy.deepcopy(middle)
        after['challenges'].append(item('breaks_guard', 'third',
                                        ['proxy_only', 'requires_context']))
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            for name, obj in [('v0', before), ('v1', middle), ('v2', after)]:
                (folder / (name + '.json')).write_text(json.dumps(obj), encoding='utf-8')
            query = {'reasoning_signature': SIG,
                     'context_features': ['proxy_only', 'requires_context']}
            (folder / 'new_case.json').write_text(json.dumps(query), encoding='utf-8')
            state_path = folder / 'checkpoint.json'
            cli = ROOT / 'tools' / 'ale_learning_checkpoint.py'
            def call(*args):
                p = subprocess.run([sys.executable, str(cli), '--checkpoint', str(state_path), *args],
                                   text=True, capture_output=True, check=True)
                return json.loads(p.stdout)
            first = call('--initialize', '--before', str(folder / 'v0.json'), '--write')
            # No preexisting guard; no claim of verified behavior.
            initial = call('--recall-query', str(folder / 'new_case.json'))
            self.assertEqual(initial['decision'], 'UNVERIFIED_PARENT_ABSTAIN')
            second = call('--before', str(folder / 'v0.json'), '--after', str(folder / 'v1.json'),
                          '--expected-sha256', first['checkpoint_sha256'], '--write')
            recalled = call('--recall-query', str(folder / 'new_case.json'))
            self.assertEqual(recalled['decision'], 'SCOPED_HYPOTHESIS_FOR_INDEPENDENT_CHALLENGE')
            self.assertEqual(recalled['scope_guard'], ['proxy_only'])
            self.assertEqual(recalled['checkpoint_sha256'], second['checkpoint_sha256'])
            third = call('--before', str(folder / 'v1.json'), '--after', str(folder / 'v2.json'),
                         '--expected-sha256', second['checkpoint_sha256'], '--write')
            recalled_after = call('--recall-query', str(folder / 'new_case.json'))
            self.assertEqual(recalled_after['decision'], 'UNVERIFIED_PARENT_ABSTAIN')
            self.assertEqual(recalled_after['checkpoint_sha256'], third['checkpoint_sha256'])
            self.assertFalse(recalled_after['verified'])
            self.assertEqual(third['learning_gain'], 'NOT_MEASURED')

    def test_unsafe_role_tokens_deny_snapshot(self):
        p = packet()
        p['examples'][0]['reasoning_signature']['from_role'] = 'Unsafe personal narrative'
        self.assertEqual(candidate_memory(p)['state'], 'NOT_RETAINED_UNSAFE_ROLES')

    def test_unvalidated_features_do_not_enter_candidate_memory(self):
        bad_cases = [
            ['owner personal details'],
            ['valid_token', 'valid_token'],
            ['valid_token'] * 17,
            ['valid_token', 12],
        ]
        for features in bad_cases:
            with self.subTest(features=features):
                p = packet()
                p['examples'][0]['context_features'] = features
                self.assertEqual(initialize(p)['candidate_memory']['state'],
                                 'NOT_RETAINED_UNSAFE_FEATURES')

    def test_mismatched_signature_no_claim(self):
        state = initialize(packet())
        self.assertEqual(recall_candidate(state, {'reasoning_signature': {
            'from_role': 'unrelated', 'to_role': 'another', 'missing_bridge_role': 'none'},
            'context_features': []})['decision'], 'NO_MATCHING_CONCEPT')


if __name__ == '__main__':
    unittest.main()
