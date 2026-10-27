"""Adversarial tests for evidence-backed autonomy gate; not evidence of agent skill."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from autonomy_shadow_eval import REPOSITORY, evaluate_manifest, evaluate_task

SHA = 'a' * 40
BASE = '/repos/' + REPOSITORY
TASK = {'id': 'U-001', 'issue': 200, 'trigger_run': 100, 'pull_request': 300, 'ci_run': 400}


def snapshot():
    return {
        BASE + '/issues/200': {'created_at': '2026-10-27T09:00:00Z'},
        BASE + '/actions/runs/100': {'event': 'schedule', 'conclusion': 'success', 'created_at': '2026-10-27T10:00:00Z'},
        BASE + '/pulls/300': {'head': {'sha': SHA}, 'user': {'login': 'github-actions[bot]', 'type': 'Bot'},
                              'base': {'ref': 'main'}, 'merged': False, 'draft': True, 'state': 'open',
                              'created_at': '2026-10-27T10:05:00Z', 'changed_files': 1},
        BASE + '/actions/runs/400': {'conclusion': 'success', 'head_sha': SHA},
        BASE + '/pulls/300/reviews?per_page=100': [{'state': 'APPROVED', 'commit_id': SHA,
                                                    'user': {'login': 'independent-reviewer'}}],
        BASE + '/pulls/300/files?per_page=100': [{'filename': 'tests/test_sample.py'}],
    }


class StubAPI:
    def __init__(self, rows):
        self.rows = rows
    def get(self, path):
        return self.rows[path]


class AutonomyShadowGateTests(unittest.TestCase):
    def eval(self, change=None):
        rows = snapshot()
        if change:
            change(rows)
        return evaluate_task(TASK, StubAPI(rows))

    def assert_rejected(self, change, cause):
        row = self.eval(change)
        self.assertEqual('NOT_VERIFIED', row['technical_autonomy'])
        self.assertIn(cause, row['reason'])

    def test_clean_remote_evidence_only_proves_technical_delivery(self):
        result = self.eval()
        self.assertEqual('VERIFIED_SHADOW_DELIVERY', result['technical_autonomy'])
        self.assertEqual('NOT_MEASURED', result['owner_minutes'])
        self.assertEqual('NOT_VERIFIED', result['clinical_quality'])

    def test_human_prompted_workflow_is_not_unsupervised(self):
        self.assert_rejected(lambda r: r[BASE + '/actions/runs/100'].update(event='workflow_dispatch'), 'NO_VERIFIED_SCHEDULED_TRIGGER')

    def test_nonbot_pr_is_not_unsupervised(self):
        self.assert_rejected(lambda r: r[BASE + '/pulls/300']['user'].update(login='human', type='User'), 'NO_AUTOMATED_PR_AUTHOR')

    def test_changed_head_invalidates_ci_and_review(self):
        self.assert_rejected(lambda r: r[BASE + '/actions/runs/400'].update(head_sha='b'*40), 'CI_NOT_GREEN_FOR_EXACT_SHA')
        self.assert_rejected(lambda r: r[BASE + '/pulls/300/reviews?per_page=100'][0].update(commit_id='b'*40), 'NO_DISTINCT_SHA_BOUND_APPROVAL')

    def test_author_cannot_self_approve(self):
        self.assert_rejected(lambda r: r[BASE + '/pulls/300/reviews?per_page=100'][0]['user'].update(login='github-actions[bot]'), 'NO_DISTINCT_SHA_BOUND_APPROVAL')

    def test_public_content_edit_fails_shadow_scope(self):
        self.assert_rejected(lambda r: r[BASE + '/pulls/300/files?per_page=100'][0].update(filename='content/clinical-os/tamponade.md'), 'OUT_OF_SCOPE_FILES')

    def test_merged_pr_does_not_count_as_safe_shadow(self):
        self.assert_rejected(lambda r: r[BASE + '/pulls/300'].update(merged=True), 'NOT_ISOLATED_DRAFT_PR')

    def test_register_after_start_is_invalid(self):
        self.assert_rejected(lambda r: r[BASE + '/issues/200'].update(created_at='2026-10-27T11:00:00Z'), 'TASK_NOT_REGISTERED_BEFORE_TRIGGER')

    def test_missing_task_is_in_denominator(self):
        report = evaluate_manifest({'schema_version': 1, 'repository': REPOSITORY,
                                     'cohort': 'pilot', 'tasks': [{**TASK, 'id': 'U-001'}, {'id': 'U-002'}]},
                                   StubAPI(snapshot()))
        self.assertEqual((1, 2), (report['verified'], report['denominator']))
        self.assertEqual('NOT_MEASURED', report['owner_time'])

    def test_empty_registry_does_not_claim_perfect_score(self):
        report = evaluate_manifest({'schema_version': 1, 'repository': REPOSITORY,
                                    'cohort': 'pilot', 'tasks': []}, StubAPI({}))
        self.assertEqual('NOT_MEASURED_NO_PREREGISTERED_TASKS', report['status'])

    def test_duplicate_tasks_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_manifest({'schema_version': 1, 'repository': REPOSITORY, 'tasks': [TASK, TASK]}, StubAPI({}))


if __name__ == '__main__':
    unittest.main()
