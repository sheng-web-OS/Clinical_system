"""Executable synthetic adapter tests; no model or provider network involved."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from falsification_probe import (
    InvalidProbe, build_packets, compare_rescue, prepare,
    prepare_rescue, run_adapter, score,
)

BASE = Path(__file__).resolve().parents[1]
SPEC = BASE / 'experiments/eth-falsification-probe/synthetic-routing.json'

# Synthetic toy rule, not a language model, no gold file access.
TOY = '''#!/usr/bin/env python3
import json
import sys
packet = json.loads(sys.stdin.read())
signed = "[F1] signed by its submitter" in packet["case_text"]
out = {"probe_id":packet["probe_id"],"packet_sha256":packet["packet_sha256"],
       "question_id":"q_signature","evidence_ids":["F1"],
       "decision_id":"accept" if signed else "hold", "review_flags":[]}
print(json.dumps(out))
'''

class ExecutableProbeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.reviewer = self.root / 'public-fixture-packets'
        self.key_path = self.root / 'coordinator' / 'key.json'
        prepare(SPEC, self.reviewer, self.key_path)
        self.adapter = self.root / 'fake_adapter.py'
        self.adapter.write_text(TOY, encoding='utf-8')
        self.adapter.chmod(0o700)
        self.responses = self.root / 'responses.json'

    def test_real_subprocess_executes_all_variants_and_scores(self):
        status = run_adapter(self.reviewer, self.responses, self.adapter)
        self.assertEqual(status['executed'], 3)
        self.assertEqual(status['isolation'], 'NOT_VERIFIED')
        key = json.loads(self.key_path.read_text())
        responses = json.loads(self.responses.read_text())
        self.assertTrue(score(key, responses)['passed'])

    def test_known_probe_id_shortcut_was_real_but_is_now_blocked(self):
        # The pre-fix runner scored this 3/3 although it NEVER read case_text.
        # This regression checks the actual subprocess, not just the rubric.
        shortcut = '''#!/usr/bin/env python3
import json,sys
p=json.load(sys.stdin)
choice={'baseline':'accept','p01':'hold','p02':'accept'}.get(p['probe_id'],'hold')
print(json.dumps({'probe_id':p['probe_id'],'packet_sha256':p['packet_sha256'],
  'question_id':'q_signature','evidence_ids':['F1'],'decision_id':choice,
  'review_flags':[]}))
'''
        self.adapter.write_text(shortcut, encoding='utf-8')
        status = run_adapter(self.reviewer, self.responses, self.adapter)
        self.assertTrue(status['opaque_ids'])
        self.assertEqual(status['status'], 'ADAPTER_EXECUTED_ACCESS_NOT_VERIFIED')
        frozen = json.loads(self.responses.read_text())
        self.assertEqual(len(frozen['transport_audit']), 3)
        self.assertTrue(all(item['opaque_probe_id'].startswith('trial_')
                            for item in frozen['transport_audit'].values()))
        result = score(json.loads(self.key_path.read_text()), frozen)
        self.assertFalse(result['passed'])
        self.assertTrue(any('S3_decision' in row['failed_stages']
                            for row in result['results']))

    def test_transport_ids_rotate_across_reruns_and_do_not_change_gold(self):
        one = run_adapter(self.reviewer, self.responses, self.adapter)
        second_path = self.root / 'responses_second.json'
        two = run_adapter(self.reviewer, second_path, self.adapter)
        self.assertEqual(one['adapter_sha256'], two['adapter_sha256'])
        raw_one = json.loads(self.responses.read_text())
        raw_two = json.loads(second_path.read_text())
        a = {v['opaque_probe_id'] for v in raw_one['transport_audit'].values()}
        b = {v['opaque_probe_id'] for v in raw_two['transport_audit'].values()}
        self.assertFalse(a & b)
        self.assertEqual(len(a), 3)
        self.assertTrue(all('baseline' not in alias and 'p01' not in alias
                            and 'p02' not in alias for alias in a | b))
        key = json.loads(self.key_path.read_text())
        self.assertTrue(score(key, raw_one)['passed'])
        self.assertTrue(score(key, raw_two)['passed'])

    def test_adapter_cannot_inspect_original_packet_filenames_via_cwd(self):
        adapter = '''#!/usr/bin/env python3
import json,sys,os
p=json.load(sys.stdin)
if os.listdir('.') or p['probe_id'] in ('baseline','p01','p02'):
    sys.exit(4)
signed='[F1] signed by its submitter' in p['case_text']
print(json.dumps({'probe_id':p['probe_id'],'packet_sha256':p['packet_sha256'],
 'question_id':'q_signature','evidence_ids':['F1'],
 'decision_id':'accept' if signed else 'hold','review_flags':[]}))
'''
        self.adapter.write_text(adapter, encoding='utf-8')
        run_adapter(self.reviewer, self.responses, self.adapter)
        self.assertTrue(score(json.loads(self.key_path.read_text()),
                              json.loads(self.responses.read_text()))['passed'])

    def test_run_fails_closed_without_overwriting(self):
        run_adapter(self.reviewer, self.responses, self.adapter)
        with self.assertRaisesRegex(InvalidProbe, 'overwrite'):
            run_adapter(self.reviewer, self.responses, self.adapter)

    def test_does_not_write_partial_results_after_adapter_failure(self):
        self.adapter.write_text('#!/usr/bin/env python3\nimport sys\nsys.exit(3)\n')
        with self.assertRaisesRegex(InvalidProbe, 'nonzero'):
            run_adapter(self.reviewer, self.responses, self.adapter)
        self.assertFalse(self.responses.exists())

    def test_changed_packet_content_without_rehash_fails_before_adapter(self):
        path = self.reviewer / 'baseline.json'
        packet = json.loads(path.read_text())
        packet['case_text'] = 'tampered'
        path.write_text(json.dumps(packet))
        with self.assertRaisesRegex(InvalidProbe, 'altered packet'):
            run_adapter(self.reviewer, self.responses, self.adapter)
        self.assertFalse(self.responses.exists())

    def test_wrong_json_schema_adapter_is_rejected(self):
        self.adapter.write_text('#!/usr/bin/env python3\nprint("{}")\n')
        with self.assertRaisesRegex(InvalidProbe, 'unexpected response'):
            run_adapter(self.reviewer, self.responses, self.adapter)

    def test_timeout_and_environment_are_fail_closed(self):
        self.adapter.write_text('#!/usr/bin/env python3\nimport time\ntime.sleep(2)\n')
        with self.assertRaisesRegex(InvalidProbe, 'timeout'):
            run_adapter(self.reviewer, self.responses, self.adapter, timeout=1)
        self.assertFalse(self.responses.exists())
        with self.assertRaisesRegex(InvalidProbe, 'invalid allow-env'):
            run_adapter(self.reviewer, self.responses, self.adapter, allowed_env=('INVALID=HELLO',))

    def test_relabelled_labels_and_order_preserve_fact_reading_result(self):
        """A source-reading adapter generalizes to unseen option/evidence IDs."""
        adapter = BASE / 'experiments/eth-falsification-probe/toy_adapter.py'
        before_path = self.root / 'normal_answers.json'
        normal = run_adapter(self.reviewer, before_path, adapter)
        altered = run_adapter(self.reviewer, self.responses, adapter, relabel=True)
        self.assertFalse(normal['relabelled'])
        self.assertTrue(altered['relabelled'])
        key = json.loads(self.key_path.read_text())
        a = json.loads(before_path.read_text())
        b = json.loads(self.responses.read_text())
        self.assertTrue(score(key, a)['passed'])
        self.assertTrue(score(key, b)['passed'])
        self.assertEqual({row['probe_id']: row['decision_id'] for row in a['responses']},
                         {row['probe_id']: row['decision_id'] for row in b['responses']})
        audit = b['transport_audit']
        for pid, record in audit.items():
            self.assertTrue(record['relabelled'])
            self.assertEqual(set(record['reverse_labels']), {
                'candidate_questions', 'candidate_decisions',
                'available_evidence_ids', 'available_review_flag_ids'})
            self.assertNotIn('F1', record['reverse_labels']['available_evidence_ids'])
            self.assertNotIn('q_signature', record['reverse_labels']['candidate_questions'])
            self.assertNotEqual(record['wire_packet_sha256'],
                                key['answers'][pid]['packet_sha256'])

    def test_fixed_option_label_adapter_is_rejected_under_relabel(self):
        """A memorized answer label is not evidence of reasoning."""
        # Unlike the prior probe-ID cheat, this adapter checks case text but
        # treats option/evidence IDs as fixed constants.
        self.adapter.write_text(TOY, encoding='utf-8')
        run_adapter(self.reviewer, self.responses, self.adapter)
        self.assertTrue(score(json.loads(self.key_path.read_text()),
                              json.loads(self.responses.read_text()))['passed'])
        relabel_out = self.root / 'relabelled.json'
        with self.assertRaisesRegex(InvalidProbe, 'invalid question label'):
            run_adapter(self.reviewer, relabel_out, self.adapter, relabel=True)
        self.assertFalse(relabel_out.exists())

    def test_relabelled_rescue_hints_reference_new_labels(self):
        hints = self.root / 'hints.json'
        hints.write_text(json.dumps({'question_hint':'Signature question q_signature',
                                      'evidence_hint':'Use F1 and not F2.'}))
        packet_root, key_root, output_root = (self.root / x for x in ('arms', 'keys', 'out'))
        prepare_rescue(SPEC, hints, packet_root, key_root)
        adapter = BASE / 'experiments/eth-falsification-probe/toy_adapter.py'
        output_root.mkdir()
        for arm in ('N','Q','E','QE'):
            status = run_adapter(packet_root / arm, output_root / (arm+'.json'),
                                 adapter, relabel=True)
            self.assertTrue(status['relabelled'])
        result = compare_rescue(key_root, output_root)
        self.assertTrue(all(a['passed'] for a in result['arms'].values()))
        # The evaluator stores only the relabel map; the live adapter sees
        # changed evidence/question IDs in its one wire packet.
        for arm in ('Q', 'E', 'QE'):
            data = json.loads((output_root / (arm+'.json')).read_text())
            self.assertTrue(all(v['relabelled']
                                for v in data['transport_audit'].values()))

    def test_rescue_gold_separated_and_only_hints_vary(self):
        hints = self.root / 'hints.json'
        hints.write_text(json.dumps({'question_hint':'Focus on signature validity.',
                                      'evidence_hint':'Signature fact F1 is decision-relevant.'}))
        packets_root = self.root / 'rescue'
        keys_root = self.root / 'rescue_gold'
        manifest = prepare_rescue(SPEC, hints, packets_root, keys_root)
        self.assertEqual(set(manifest['arms']), {'N','Q','E','QE'})
        p = {arm: json.loads((packets_root / arm / 'baseline.json').read_text())
             for arm in ('N','Q','E','QE')}
        self.assertNotIn('research_aids', p['N'])
        self.assertEqual(set(p['Q']['research_aids']), {'question_hint'})
        self.assertEqual(set(p['E']['research_aids']), {'evidence_hint'})
        self.assertEqual(set(p['QE']['research_aids']), {'question_hint','evidence_hint'})
        self.assertEqual(len({x['packet_sha256'] for x in p.values()}), 4)
        self.assertFalse(any('gold' in str(list((packets_root / arm).iterdir())) for arm in p))
        with self.assertRaisesRegex(InvalidProbe, 'overwrite'):
            prepare_rescue(SPEC, hints, packets_root, keys_root)

    def test_execute_and_compare_all_four_rescue_arms(self):
        hints = self.root / 'hints.json'
        hints.write_text(json.dumps({'question_hint':'Is signature present?',
                                      'evidence_hint':'Look at F1, not F2.'}))
        packet_root, key_root, output_root = (self.root / x for x in ('arms','keys','out'))
        prepare_rescue(SPEC, hints, packet_root, key_root)
        output_root.mkdir()
        for arm in ('N','Q','E','QE'):
            run_adapter(packet_root / arm, output_root / (arm+'.json'), self.adapter)
        report = compare_rescue(key_root, output_root)
        self.assertEqual(report['status'], 'DIAGNOSTIC_RESCUE_NOT_A_CAUSAL_ROOT')
        self.assertEqual({a:v['passed'] for a,v in report['arms'].items()},
                         {a:True for a in ('N','Q','E','QE')})

if __name__ == '__main__':
    unittest.main()
