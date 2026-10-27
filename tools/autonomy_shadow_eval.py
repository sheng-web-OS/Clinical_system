"""Fail-closed, GitHub-backed unsupervised-agent delivery audit.

This measures observable technical autonomy, NOT clinical correctness, learning
impact, or owner-time savings. It never changes repositories or deployments.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPOSITORY = 'sheng-web-OS/Clinical_system'
SAFE_PREFIXES = ('tools/', 'tests/')  # Shadow phase: never authorize content or publishing.
TRUSTED_RUNNER = '.github/workflows/autonomy-shadow-runner.yml'
EVIDENCE_FIELDS = ('issue', 'trigger_run', 'pull_request', 'ci_run')
SHA_RE = re.compile(r'^[a-f0-9]{40}$')


def parse_time(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


class GithubReadOnly:
    def __init__(self, token):
        self.token = token

    def get(self, path):
        assert path.startswith('/repos/' + REPOSITORY + '/'), 'out of repo scope'
        request = Request('https://api.github.com' + path, headers={
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': 'Bearer ' + self.token,
            'User-Agent': 'clinical-os-autonomy-shadow-eval',
        })
        with urlopen(request, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))


def evaluate_task(task, api):
    """Derive verdict from remote evidence; never read self-awarded 'pass'."""
    task_id = task.get('id', 'INVALID_ID')
    result = {'task_id': task_id, 'technical_autonomy': 'NOT_VERIFIED',
              'owner_minutes': 'NOT_MEASURED', 'clinical_quality': 'NOT_VERIFIED',
              'pedagogical_quality': 'NOT_VERIFIED', 'reason': ''}
    for field in EVIDENCE_FIELDS:
        if not isinstance(task.get(field), int) or task[field] <= 0:
            result['reason'] = 'NOT_STARTED_OR_MISSING_' + field.upper()
            return result
    try:
        base = '/repos/' + REPOSITORY
        issue = api.get(base + '/issues/' + str(task['issue']))
        trigger = api.get(base + '/actions/runs/' + str(task['trigger_run']))
        pr = api.get(base + '/pulls/' + str(task['pull_request']))
        ci = api.get(base + '/actions/runs/' + str(task['ci_run']))
        reviewer_records = api.get(base + '/pulls/' + str(task['pull_request']) + '/reviews?per_page=100')
        changed = api.get(base + '/pulls/' + str(task['pull_request']) + '/files?per_page=100')
    except (HTTPError, URLError, ValueError, KeyError, AssertionError) as exc:
        result['reason'] = 'REMOTE_EVIDENCE_UNAVAILABLE:' + type(exc).__name__
        return result
    try:
        sha = pr['head']['sha']
        bot = pr['user']
        if trigger['event'] != 'schedule' or trigger['conclusion'] != 'success':
            raise ValueError('NO_VERIFIED_SCHEDULED_TRIGGER')
        if trigger.get('path') != TRUSTED_RUNNER:
            raise ValueError('WRONG_AUTONOMY_RUNNER')
        if (trigger.get('head_branch') != 'main' or
                trigger.get('head_repository', {}).get('full_name') != REPOSITORY):
            raise ValueError('NOT_PROTECTED_RUNNER_CONTEXT')
        if parse_time(issue['created_at']) > parse_time(trigger['created_at']):
            raise ValueError('TASK_NOT_REGISTERED_BEFORE_TRIGGER')
        if parse_time(pr['created_at']) < parse_time(trigger['created_at']):
            raise ValueError('PR_PREDATES_TRIGGER')
        if parse_time(pr['created_at']) > parse_time(trigger['updated_at']):
            raise ValueError('PR_OUTSIDE_RUN_WINDOW')
        # A matching branch name is only a trace correlation, not cryptographic
        # attestation of independent thought or of absence of owner prompts.
        expected_branch = 'shadow/' + task_id + '/run-' + str(task['trigger_run'])
        if pr['head']['ref'] != expected_branch:
            raise ValueError('PR_NOT_BOUND_TO_SCHEDULED_TRIAL')
        if (pr['head']['repo']['full_name'] != REPOSITORY or
                pr['base']['repo']['full_name'] != REPOSITORY):
            raise ValueError('PR_WRONG_REPOSITORY')
        if not (bot.get('type') == 'Bot' or bot.get('login', '').endswith('[bot]')):
            raise ValueError('NO_AUTOMATED_PR_AUTHOR')
        if pr['base']['ref'] != 'main' or pr['merged'] or not pr['draft'] or pr['state'] != 'open':
            raise ValueError('NOT_ISOLATED_DRAFT_PR')
        if not SHA_RE.fullmatch(sha):
            raise ValueError('INVALID_SHA')
        if ci['conclusion'] != 'success' or ci['head_sha'] != sha:
            raise ValueError('CI_NOT_GREEN_FOR_EXACT_SHA')
        if (ci.get('event') != 'pull_request' or
                ci.get('head_repository', {}).get('full_name') != REPOSITORY or
                not any(p.get('number') == pr['number'] for p in ci.get('pull_requests', []))):
            raise ValueError('CI_NOT_BOUND_TO_PR')
        if pr.get('changed_files', 0) != len(changed) or not changed:
            raise ValueError('FILE_LIST_UNVERIFIABLE')
        if any(not any(f['filename'].startswith(p) for p in SAFE_PREFIXES) for f in changed):
            raise ValueError('OUT_OF_SCOPE_FILES')
        if not any(r.get('state') == 'APPROVED' and r.get('commit_id') == sha
                   and r.get('user', {}).get('login') != bot.get('login')
                   for r in reviewer_records):
            raise ValueError('NO_DISTINCT_SHA_BOUND_APPROVAL')
    except (KeyError, ValueError, TypeError) as exc:
        result['reason'] = str(exc)
        return result
    result['technical_autonomy'] = 'VERIFIED_SHADOW_DELIVERY'
    result['reason'] = 'Scheduled bot PR, scoped changes, independent GitHub approval, exact-SHA CI verified'
    # GitHub alone cannot verify no human ChatGPT prompts or human minutes.
    # Separate clinical and pedagogical reviews are also required for those claims.
    return result


def evaluate_manifest(manifest, api):
    if manifest.get('schema_version') != 1 or manifest.get('repository') != REPOSITORY:
        raise ValueError('Bad registry schema or repository')
    tasks = manifest.get('tasks')
    if not isinstance(tasks, list) or not tasks:
        return {'cohort': manifest.get('cohort'), 'denominator': 0, 'verified': 0,
                'status': 'NOT_MEASURED_NO_PREREGISTERED_TASKS', 'results': []}
    ids = [t.get('id') for t in tasks]
    if not all(isinstance(x, str) and x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError('Task IDs must be unique and nonempty')
    # Never turn the same observed delivery into multiple successes by giving it
    # several task IDs. Keep invalid entries in the original denominator.
    counts = {field: {} for field in EVIDENCE_FIELDS}
    for task in tasks:
        for field in EVIDENCE_FIELDS:
            value = task.get(field)
            if isinstance(value, int) and value > 0:
                counts[field][value] = counts[field].get(value, 0) + 1
    results = []
    for task in tasks:
        repeated = [field for field in EVIDENCE_FIELDS
                    if isinstance(task.get(field), int) and
                    counts[field].get(task[field], 0) > 1]
        if repeated:
            results.append({'task_id': task['id'], 'technical_autonomy': 'NOT_VERIFIED',
                            'owner_minutes': 'NOT_MEASURED', 'clinical_quality': 'NOT_VERIFIED',
                            'pedagogical_quality': 'NOT_VERIFIED',
                            'reason': 'REUSED_EVIDENCE_' + '_'.join(repeated).upper()})
        else:
            results.append(evaluate_task(task, api))
    passed = sum(r['technical_autonomy'] == 'VERIFIED_SHADOW_DELIVERY' for r in results)
    return {'cohort': manifest.get('cohort'), 'denominator': len(tasks),
            'verified': passed, 'status': ('OBSERVED_TECHNICAL_ONLY' if passed else 'NO_VERIFIED_UNSUPERVISED_RUNS'), 'results': results,
            'owner_time': 'NOT_MEASURED', 'medical_safety': 'NOT_VERIFIED',
            'pedagogy': 'NOT_VERIFIED', 'real_world_unprompted': 'NOT_VERIFIED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registry', default='experiments/autonomy-shadow/registry.json')
    parser.add_argument('--out', default='')
    args = parser.parse_args()
    registry = json.loads(Path(args.registry).read_text(encoding='utf-8'))
    # No network calls for zero registered tasks. Other runs require token and real GitHub evidence.
    token = os.environ.get('GITHUB_TOKEN', '')
    if registry.get('tasks') and not token:
        print('GITHUB_TOKEN required: cannot certify unsupervised work without remote checks', file=sys.stderr)
        return 2
    report = evaluate_manifest(registry, GithubReadOnly(token))
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.out:
        Path(args.out).write_text(output + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
