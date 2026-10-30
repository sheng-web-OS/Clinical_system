"""Synthetic-only regression and negative controls for a research prototype."""
import copy
import unittest
from audit_growth_leakage import audit


def sample():
    return {
        'schema_version':1,
        'protocol_frozen_at':'2026-10-01T00:00:00+00:00',
        'model_fit_at':'2026-10-02T00:00:00+00:00',
        'evaluation_started_at':'2026-10-03T00:00:00+00:00',
        'cases':[
            {'id':'train-1','family_id':'f1','split':'train',
             'decision_at':'2026-09-01T00:00:00+00:00',
             'evidence_available_at':'2026-08-31T00:00:00+00:00',
             'evidence_observed_at':'2026-08-31T06:00:00+00:00',
             'label_mature_at':'2026-09-10T00:00:00+00:00'},
            {'id':'dev-1','family_id':'f2','split':'development',
             'decision_at':'2026-09-11T00:00:00+00:00',
             'evidence_available_at':'2026-09-10T00:00:00+00:00',
             'evidence_observed_at':'2026-09-10T06:00:00+00:00',
             'label_mature_at':'2026-09-14T00:00:00+00:00'},
            {'id':'held-1','family_id':'f3','split':'holdout',
             'decision_at':'2026-09-17T00:00:00+00:00',
             'evidence_available_at':'2026-09-16T00:00:00+00:00',
             'evidence_observed_at':'2026-09-16T06:00:00+00:00',
             'label_mature_at':'2026-09-20T00:00:00+00:00'}
        ]}


class GrowthLeakageContract(unittest.TestCase):
    def setUp(self):
        self.p=sample()
    def rejects(self, code):
        report=audit(self.p)
        self.assertEqual('REJECT',report['status'])
        self.assertIn(code,[e['code'] for e in report['violations']])
        self.assertFalse(report['growth_score_change_authorized'])
    def test_valid_is_not_growth_certification(self):
        report=audit(self.p)
        self.assertEqual('STRUCTURALLY_ELIGIBLE_NOT_VALIDATED',report['status'])
        self.assertFalse(report['independent_holdout_authenticated'])
        self.assertFalse(report['growth_score_change_authorized'])
    def test_future_source(self):
        self.p['cases'][1]['evidence_available_at']='2026-09-12T00:00:00+00:00'
        self.rejects('FUTURE_OR_LATE_EVIDENCE')
    def test_late_observation(self):
        self.p['cases'][1]['evidence_observed_at']='2026-09-12T00:00:00+00:00'
        self.rejects('FUTURE_OR_LATE_EVIDENCE')
    def test_observed_before_publication(self):
        self.p['cases'][1]['evidence_observed_at']='2026-09-09T00:00:00+00:00'
        self.rejects('OBSERVATION_BEFORE_AVAILABILITY')
    def test_train_outcome_matures_after_fit(self):
        self.p['cases'][0]['label_mature_at']='2026-10-02T01:00:00+00:00'
        self.rejects('TRAIN_LABEL_NOT_MATURE_AT_FIT')
    def test_same_family_train_holdout(self):
        self.p['cases'][2]['family_id']='f1'
        self.rejects('FAMILY_CROSS_SPLIT')
    def test_same_family_dev_holdout(self):
        self.p['cases'][2]['family_id']='f2'
        self.rejects('FAMILY_CROSS_SPLIT')
    def test_invalid_protocol_order(self):
        self.p['protocol_frozen_at']='2026-10-04T00:00:00+00:00'
        with self.assertRaisesRegex(ValueError,'PROTOCOL_FIT_EVAL_CLOCK_ORDER'):
            audit(self.p)
    def test_missing_timezone(self):
        self.p['cases'][1]['decision_at']='2026-09-11T00:00:00'
        with self.assertRaisesRegex(ValueError,'TIMESTAMP_TIMEZONE_MISSING'):
            audit(self.p)
    def test_duplicate_trial_id(self):
        self.p['cases'][2]['id']='train-1'
        with self.assertRaisesRegex(ValueError,'CASE_ID_DUPLICATE'):
            audit(self.p)
    def test_no_holdout(self):
        self.p['cases'][2]['split']='development'
        self.rejects('SPLIT_EMPTY')
    def test_invalid_family(self):
        self.p['cases'][2]['family_id']=' '
        with self.assertRaisesRegex(ValueError,'CASE_KEY_INVALID'):
            audit(self.p)
    def test_bool_schema_version(self):
        self.p['schema_version']=True
        with self.assertRaisesRegex(ValueError,'AUDIT_SCHEMA_INVALID'):
            audit(self.p)
    def test_label_before_decision(self):
        self.p['cases'][1]['label_mature_at']='2026-09-10T00:00:00+00:00'
        self.rejects('LABEL_NOT_POST_DECISION')
    def test_missing_case_fields_fail_closed(self):
        del self.p['cases'][1]['family_id']
        with self.assertRaisesRegex(ValueError,'CASE_SCHEMA_INVALID'):
            audit(self.p)
    def test_timestamp_offsets_compare(self):
        self.p['cases'][0]['evidence_available_at']='2026-08-31T08:00:00+08:00'
        self.assertEqual('STRUCTURALLY_ELIGIBLE_NOT_VALIDATED',audit(self.p)['status'])


if __name__=='__main__':
    unittest.main()

