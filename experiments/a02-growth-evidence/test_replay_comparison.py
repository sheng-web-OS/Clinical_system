"""Supplemental synthetic replay tests. These do NOT execute a real #225 model."""
import copy
import tempfile
import unittest
from pathlib import Path

from audit_growth_leakage import audit
from replay_comparison import fixture, mutations, old_module


class A02ReplayRegression(unittest.TestCase):
    def test_synthetic_boundaries_are_stable(self):
        expectations={
            'clean':True,
            'same_public_source_different_cases':True,
            'train_holdout_overlap':False,
            'dev_holdout_overlap':False,
            'future_publication':False,
            'late_observation':False,
            'immature_train_label':False,
            'naive_timestamp':False,
            'forged_family_alias':True,
            'retrospective_holdout_without_attested_seal':True,
            'hinted_worker':True,
            'native_arm_retrieval':True,
        }
        observed={}
        for scenario, _category, change in mutations():
            s,r,a=copy.deepcopy(fixture())
            change(s,r,a)
            try:
                observed[scenario]=audit(a)['status']!='REJECT'
            except ValueError:
                observed[scenario]=False
        self.assertEqual(expectations,observed)

    def test_declared_family_and_timestamps_are_not_authenticated(self):
        _s,_r,a=fixture()
        report=audit(a)
        self.assertFalse(report['independent_holdout_authenticated'])
        self.assertFalse(report['growth_score_change_authorized'])
        self.assertEqual('STRUCTURALLY_ELIGIBLE_NOT_VALIDATED',report['status'])

    def test_forged_or_changed_baseline_source_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'compare_skill_transfer.py'
            path.write_text('print("fake")\n',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'OLD_EVALUATOR_BLOB_MISMATCH'):
                old_module(path)


if __name__=='__main__':
    unittest.main()
