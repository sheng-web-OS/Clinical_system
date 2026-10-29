"""Credential-free adversarial checks for the opt-in real-model adapter."""
import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'experiments/eth-falsification-probe/openai_model_adapter.py'
spec = importlib.util.spec_from_file_location('openai_eth_probe_adapter', MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class Response:
    def __init__(self, data):
        self.data = json.dumps(data).encode()
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def read(self, amount):
        return self.data


def packet(with_claims=True):
    p = {
        'schema_version': 1, 'case_id': 'synthetic_hidden_77',
        'probe_id': 'trial_opaque', 'packet_sha256': 'a' * 64,
        'task': 'Assess the synthetic document.',
        'case_text': '[Eabc] The document is verified as signed.',
        'candidate_questions': {'Qabc': 'Does it have a valid signature?',
                                'Qdef': 'What is its cover color?'},
        'candidate_decisions': {'Dabc': 'Transfer', 'Ddef': 'Hold', 'Dghi': 'Verify'},
        'available_evidence_ids': ['Eabc'], 'available_review_flag_ids': [],
    }
    if with_claims:
        p['candidate_claims'] = {'Cabc': 'Signature is verified.'}
        p['available_support_statuses'] = ['sufficient', 'insufficient']
    return p


def answer(p):
    a = {'probe_id': p['probe_id'], 'packet_sha256': p['packet_sha256'],
         'question_id': 'Qabc', 'evidence_ids': ['Eabc'],
         'decision_id': 'Dabc', 'review_flags': []}
    if 'candidate_claims' in p:
        a['claim_statuses'] = {'Cabc': 'supported'}
        a['support_status'] = 'sufficient'
    return a


class ModelAdapterTests(unittest.TestCase):
    def test_no_key_no_request(self):
        with self.assertRaisesRegex(mod.ProbeModelError, 'OPENAI_KEY_MISSING'):
            mod.model_inference(packet(), 'native', 'gpt-5-mini', '')

    def test_private_data_blocked_by_default(self):
        p = packet(); p['case_id'] = 'real_case_2026'
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(mod.ProbeModelError, 'EXTERNAL_DATA_NOT_AUTHORIZED'):
                mod.check_packet(p)

    def test_explicit_external_data_optin(self):
        p = packet(); p['case_id'] = 'real_case_2026'
        with patch.dict(os.environ, {'PROBE_APPROVED_EXTERNAL_DATA':'true'}):
            self.assertEqual(mod.check_packet(p), p)

    def test_gold_leak_rejected(self):
        p = packet(); p['answers'] = {'secret': 'gold'}
        with self.assertRaisesRegex(mod.ProbeModelError, 'GOLD_IN_MODEL_PACKET'):
            mod.check_packet(p)

    def test_store_false_no_tools_and_dynamic_schema(self):
        p = packet()
        payload = mod.request_body(p, 'native', 'gpt-5-mini')
        self.assertIs(payload['store'], False)
        self.assertNotIn('tools', payload)
        self.assertNotIn('previous_response_id', payload)
        s = payload['text']['format']['schema']
        self.assertEqual(s['properties']['question_id']['enum'], ['Qabc', 'Qdef'])
        self.assertEqual(s['properties']['claim_statuses']['required'], ['Cabc'])
        self.assertTrue(s['additionalProperties'] is False)
        self.assertNotIn('clinical', payload['instructions'].lower())

    def test_lite_is_distinct_but_same_budget(self):
        p = packet()
        a = mod.request_body(p, 'native', 'gpt-5-mini')
        b = mod.request_body(p, 'clinical_lite', 'gpt-5-mini')
        self.assertNotEqual(a['instructions'], b['instructions'])
        self.assertEqual(a['max_output_tokens'], b['max_output_tokens'])
        self.assertEqual(a['input'], b['input'])
        self.assertEqual(a['text'], b['text'])

    def test_empty_review_flag_domain_has_no_empty_enum(self):
        p = packet()
        item = mod.schema_for(p)["properties"]["review_flags"]["items"]
        self.assertEqual(item, {"type": "string"})

    def test_model_success_and_usage(self):
        p = packet()
        captured = {}
        def opener(req, timeout):
            captured['req'] = req; captured['timeout'] = timeout
            return Response({'status': 'completed', 'output': [
                {'type': 'message', 'content': [{'type': 'output_text', 'text': json.dumps(answer(p))}]}],
                'usage': {'input_tokens': 45, 'output_tokens': 36, 'total_tokens': 81,
                          'unsafe_field': 'never store'}})
        reply, usage = mod.model_inference(p, 'native', 'gpt-5-mini', 'fictional-key', opener)
        self.assertEqual(reply, answer(p))
        self.assertEqual(usage, {'input_tokens': 45, 'output_tokens': 36, 'total_tokens': 81})
        sent=json.loads(captured['req'].data)
        self.assertEqual(sent['model'], 'gpt-5-mini')
        self.assertIn('Bearer fictional-key',captured['req'].get_header('Authorization'))
        self.assertNotIn('fictional-key',json.dumps(sent))
        self.assertFalse(sent['store'])

    def test_rejects_wrong_packet_binding(self):
        p = packet(); wrong=answer(p); wrong['packet_sha256']='0'*64
        def opener(req, timeout):
            return Response({'status':'completed','output':[{'type':'message','content':[
                {'type':'output_text','text':json.dumps(wrong)}]}]})
        with self.assertRaisesRegex(mod.ProbeModelError, 'MODEL_PACKET_MISMATCH'):
            mod.model_inference(p,'native','gpt-5-mini','key',opener)

    def test_incomplete_output_refused(self):
        p = packet()
        def opener(req, timeout):
            return Response({'status':'incomplete','output':[], 'incomplete_details':{'reason':'max_output_tokens'}})
        with self.assertRaisesRegex(mod.ProbeModelError,'MODEL_NOT_COMPLETED'):
            mod.model_inference(p,'native','gpt-5-mini','key',opener)

    def test_fabricated_label_refused(self):
        p = packet(); bad=answer(p); bad['evidence_ids']=['fake']
        def opener(req, timeout):
            return Response({'output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(bad)}]}]})
        with self.assertRaisesRegex(mod.ProbeModelError,'MODEL_INVALID_LIST'):
            mod.model_inference(p,'native','gpt-5-mini','key',opener)

    def test_new_api_schema_handles_no_claims(self):
        p=packet(with_claims=False)
        s=mod.schema_for(p)
        self.assertNotIn('support_status',s['properties'])
        self.assertNotIn('claim_statuses',s['properties'])

    def test_http_errors_sanitized(self):
        import urllib.error
        p=packet()
        def opener(req, timeout):
            raise urllib.error.HTTPError('https://api.openai.com/v1/responses',429,'UNSAFE_ACCOUNT_DATA',{},None)
        with self.assertRaisesRegex(mod.ProbeModelError,r'^MODEL_HTTP_429$'):
            mod.model_inference(p,'native','gpt-5-mini','key',opener)

    def test_parent_runner_captures_usage_without_gold_access(self):
        import tempfile
        sys.path.insert(0, str(ROOT / 'tools'))
        from falsification_probe import prepare, run_adapter
        spec = ROOT / 'experiments/eth-falsification-probe/synthetic-routing.json'
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            reviewer = work / 'packets'
            prepare(spec, reviewer, work / 'private/key.json')
            toy = work / 'usage_adapter.py'
            toy.write_text("""import json,sys
p=json.load(sys.stdin)
a={'probe_id':p['probe_id'],'packet_sha256':p['packet_sha256'],
'question_id':list(p['candidate_questions'])[0],
'decision_id':list(p['candidate_decisions'])[0],
'evidence_ids':[],'review_flags':[]}
print(json.dumps(a))
print('PROBE_USAGE {\"input_tokens\":10,\"output_tokens\":20}',file=sys.stderr)
""")
            dest = work/'responses.json'
            result=run_adapter(reviewer,dest,toy)
            record=json.loads(dest.read_text())
            self.assertEqual(result['usage_rows'],3)
            self.assertEqual(set(record['provider_usage']),{'baseline','p01','p02'})
            self.assertTrue(all(v['input_tokens']==10 for v in record['provider_usage'].values()))
            self.assertEqual(record['usage_source'],'ADAPTER_REPORTED_NOT_BILLING_VERIFIED')

    def test_no_unexpected_output_fields(self):
        p=packet(); bad=answer(p);bad['status']='AUTONOMY_PASSED'
        def opener(req, timeout):
            return Response({'output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(bad)}]}]})
        with self.assertRaisesRegex(mod.ProbeModelError,'MODEL_OUTPUT_FIELDS_INVALID'):
            mod.model_inference(p,'native','gpt-5-mini','key',opener)


if __name__ == '__main__':
    unittest.main()
