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
