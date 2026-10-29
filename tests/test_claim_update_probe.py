"""Behavioral regression: correct updates, preserved claims, and invalid shortcuts.

All data fictional. A passing toy program is NOT evidence of independent LLM reasoning.
"""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from falsification_probe import InvalidProbe, build_packets, score, prepare, run_adapter

SPEC=ROOT/'experiments/eth-falsification-probe/synthetic-claim-update.json'
ADAPTER=ROOT/'experiments/eth-falsification-probe/claim_update_toy_adapter.py'


class ClaimUpdateProbeTests(unittest.TestCase):
    def setUp(self):
        self.spec=json.loads(SPEC.read_text(encoding='utf-8'))
        self.packets,self.key=build_packets(self.spec)
        self.responses={'case_id':self.key['case_id'],'responses':[
            {'probe_id':pid,'packet_sha256':rec['packet_sha256'],**copy.deepcopy(rec['gold'])}
            for pid,rec in self.key['answers'].items()]}

    def mutate(self,pid,claim,state):
        reply=next(r for r in self.responses['responses'] if r['probe_id']==pid)
        reply['claim_statuses'][claim]=state

    def test_gold_never_in_packets_and_updates_are_selective(self):
        self.assertTrue(all('gold' not in p and 'claim_statuses' not in p
                            for p in self.packets))
        out=score(self.key,self.responses)
        self.assertTrue(out['passed'])
        rows={r['probe_id']:r for r in out['results']}
        self.assertEqual(rows['document_unknown']['claims_expected_update'],1)
        self.assertEqual(rows['document_unsigned']['claims_expected_stable'],2)
        self.assertEqual(rows['irrelevant_cover_color']['claims_expected_update'],1)
        self.assertEqual(rows['irrelevant_cover_color']['claims_expected_stable'],2)

    def test_correct_decision_wrong_claim_update_fails(self):
        self.mutate('document_unknown','claim_signature','supported')
        report=score(self.key,self.responses)
        self.assertFalse(report['passed'])
        row=next(x for x in report['results'] if x['probe_id']=='document_unknown')
        self.assertIn('S3_decision',row['failed_stages'])
        self.assertEqual(row['missed_claim_updates'],['claim_signature'])

    def test_correction_that_destroys_a_valid_claim_is_detected(self):
        self.mutate('document_unsigned','claim_blue','undetermined')
        row=next(x for x in score(self.key,self.responses)['results'] if x['probe_id']=='document_unsigned')
        self.assertIn('claim_blue',row['stable_claim_damage'])
        self.assertEqual(row['incorrect_claim_states'],['claim_blue'])

    def test_irrelevant_for_main_decision_still_changes_cover_claim(self):
        self.mutate('irrelevant_cover_color','claim_blue','supported')
        row=next(x for x in score(self.key,self.responses)['results'] if x['probe_id']=='irrelevant_cover_color')
        self.assertTrue(row['relation_passed'])  # transfer is unchanged
        self.assertFalse(row['passed'])  # but cover conclusion must change
        self.assertEqual(row['missed_claim_updates'],['claim_blue'])

    def test_missing_claim_response_fails_closed(self):
        del self.responses['responses'][0]['claim_statuses']
        with self.assertRaisesRegex(InvalidProbe,'claim_statuses'):
            score(self.key,self.responses)

    def test_incomplete_gold_rejected_before_packet_creation(self):
        broken=copy.deepcopy(self.spec)
        del broken['probes'][0]['gold']['claim_statuses']['claim_blue']
        with self.assertRaisesRegex(InvalidProbe,'claim_statuses must cover'):
            build_packets(broken)

    def test_toy_adapter_relabelled_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            prepare(SPEC,root/'packets',root/'key'/'gold.json')
            run=run_adapter(root/'packets',root/'answers.json',ADAPTER,relabel=True)
            self.assertEqual(run['executed'],4)
            self.assertEqual(run['isolation'],'NOT_VERIFIED')
            results=json.loads((root/'answers.json').read_text())
            report=score(json.loads((root/'key'/'gold.json').read_text()),results)
            self.assertTrue(report['passed'])
            for item in results['transport_audit'].values():
                self.assertIn('candidate_claims',item['reverse_labels'])

    def test_toy_adapter_missing_claim_field_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            prepare(SPEC,root/'packets',root/'key'/'gold.json')
            old=root/'legacy_adapter.py'
            old.write_text(ADAPTER.read_text().replace(",'claim_statuses':claim_statuses", ''),encoding='utf-8')
            with self.assertRaisesRegex(InvalidProbe,'claim_statuses|unexpected response'):
                run_adapter(root/'packets',root/'answers.json',old,relabel=True)
            self.assertFalse((root/'answers.json').exists())


if __name__=='__main__': unittest.main()
