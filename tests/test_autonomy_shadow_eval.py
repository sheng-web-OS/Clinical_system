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
        BASE + '/actions/runs/100': {'event': 'schedule', 'conclusion': 'success', 'created_at': '2026-10-27T10:00:00Z',
                                            'updated_at': '2026-10-27T10:10:00Z',
                                            'path': '.github/workflows/autonomy-shadow-runner.yml',
                                            'head_branch': 'main',
                                            'head_repository': {'full_name': REPOSITORY}},
        BASE + '/pulls/300': {'head': {'sha': SHA, 'ref': 'shadow/U-001/run-100',
                                    'repo': {'full_name': REPOSITORY}}, 'user': {'login': 'github-actions[bot]', 'type': 'Bot'},
                              'base': {'ref': 'main', 'repo': {'full_name': REPOSITORY}}, 'number': 300,
                              'merged': False, 'draft': True, 'state': 'open',
                              'created_at': '2026-10-27T10:05:00Z', 'changed_files': 1},
        BASE + '/actions/runs/400': {'conclusion': 'success', 'head_sha': SHA, 'event': 'pull_request',
                                     'pull_requests': [{'number': 300}],
                                     'head_repository': {'full_name': REPOSITORY}},
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

    def test_pending_cohort_cannot_claim_observed_autonomy(self):
        report = evaluate_manifest({'schema_version': 1, 'repository': REPOSITORY,
                                    'cohort': 'pilot', 'tasks': [{'id': 'U-pending', 'issue': 200}]},
                                   StubAPI(snapshot()))
        self.assertEqual('NO_VERIFIED_UNSUPERVISED_RUNS', report['status'])
        self.assertEqual(0, report['verified'])

    def test_duplicate_tasks_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_manifest({'schema_version': 1, 'repository': REPOSITORY, 'tasks': [TASK, TASK]}, StubAPI({}))


    def test_unrelated_scheduled_job_cannot_certify_bot_pr(self):
        self.assert_rejected(lambda r: r[BASE + '/actions/runs/100'].update(
            path='.github/workflows/nightly-smoke.yml'), 'WRONG_AUTONOMY_RUNNER')

    def test_non_default_branch_scheduled_run_is_rejected(self):
        self.assert_rejected(lambda r: r[BASE + '/actions/runs/100'].update(
            head_branch='feature/manual'), 'NOT_PROTECTED_RUNNER_CONTEXT')

    def test_pr_must_be_bound_to_registered_trial_and_runner(self):
        self.assert_rejected(lambda r: r[BASE + '/pulls/300']['head'].update(
            ref='unrelated-bot-change'), 'PR_NOT_BOUND_TO_SCHEDULED_TRIAL')

    def test_pr_after_scheduled_run_is_not_runner_output(self):
        self.assert_rejected(lambda r: r[BASE + '/pulls/300'].update(
            created_at='2026-10-27T11:00:00Z'), 'PR_OUTSIDE_RUN_WINDOW')

    def test_ci_must_belong_to_same_pr_not_merely_same_sha(self):
        self.assert_rejected(lambda r: r[BASE + '/actions/runs/400'].update(
            pull_requests=[{'number': 301}]), 'CI_NOT_BOUND_TO_PR')
        self.assert_rejected(lambda r: r[BASE + '/actions/runs/400'].update(
            event='workflow_dispatch'), 'CI_NOT_BOUND_TO_PR')

    def test_cross_repo_pr_cannot_claim_same_owner_shadow(self):
        self.assert_rejected(lambda r: r[BASE + '/pulls/300']['head']['repo'].update(
            full_name='attacker/repo'), 'PR_WRONG_REPOSITORY')

    def test_reused_pr_or_trigger_cannot_count_twice_in_cohort(self):
        tasks = [TASK, {**TASK, 'id': 'U-002', 'issue': 201}]
        rows = snapshot()
        rows[BASE + '/issues/201'] = {'created_at': '2026-10-27T09:00:00Z'}
        report = evaluate_manifest({'schema_version': 1, 'repository': REPOSITORY,
                                    'cohort': 'pilot', 'tasks': tasks}, StubAPI(rows))
        self.assertEqual(2, report['denominator'])
        self.assertEqual(0, report['verified'])
        self.assertTrue(all('REUSED_EVIDENCE' in x['reason'] for x in report['results']))

if __name__ == '__main__':
    unittest.main()
