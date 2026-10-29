# Google Drive selective agent — setup candidate (2026-10-29)

Status: DRAFT/HOLD. The repository is PUBLIC. This implementation allows ONLY a synthetic fixture and does NOT publish content, auto-merge, or claim unattended agent success.

## Connected smoke test
A synthetic Google Doc exists in the new Google Drive folder:
Clinical OS Agent Sandbox — Synthetic Only.
The file was created in the user's connected Google Drive account and successfully moved to that folder. It has NOT been shared with a Google Cloud service account.

## Separation of credentials
ChatGPT's connected Google Drive permission does not transfer to GitHub Actions.
GitHub Actions must use its own dedicated identity, and the model API must use a separately authorized API key.

## Owner configuration needed after choosing authorization
1. Select or create a Google Cloud project; enable APIs required by the Workload Identity Federation setup (IAM, STS, Drive API).
2. Create a dedicated Google Cloud Service Account with no unnecessary project roles.
3. Create a Workload Identity Pool and OIDC provider with issuer https://token.actions.githubusercontent.com, mapping google.subject = assertion.sub, attribute.repository = assertion.repository, attribute.ref = assertion.ref. Restrict the condition to the exact repository, main ref and specific workflow_ref for this workflow: sheng-web-OS/Clinical_system/.github/workflows/drive-source-agent.yml@refs/heads/main.
4. Grant Workload Identity User only to the constrained provider principal on the dedicated Service Account. Prefer a repository numeric ID condition in addition to repository name where supported.
5. Share ONLY the synthetic folder with the service account as Viewer.
6. In GitHub Actions Variables configure CLINICAL_OS_WIF_PROVIDER, CLINICAL_OS_GCP_SERVICE_ACCOUNT, CLINICAL_OS_AGENT_MODEL (suggest gpt-5-mini). Do not enable the real job until owner approval: CLINICAL_OS_AGENT_ENABLED must be true for any model/Drive path.
7. In GitHub Actions Secrets configure CLINICAL_OS_DRIVE_FIXTURE_FOLDER_ID and a dedicated CLINICAL_OS_OPENAI_API_KEY. Use a separate model API project with controlled budget. Do not paste secrets into chat, PRs or commits.

This connector cannot currently edit GitHub Actions secrets or Google Cloud IAM settings. No Google Cloud account binding, token, API key or Drive folder share was configured by this PR.

## Modes
- fixture: deterministic, no AI/API/Drive; validates ten fail-closed unit tests and prints a simulation flag.
- shadow: requires authorized OpenAI API key; runs an AI decision using only synthetic public metadata; cannot read Google Drive.
- synthetic-read: requires both Google WIF + OpenAI API key, gates model decision, searches ONLY the authorized sandbox folder for one known synthetic Google Doc and checks its fixed synthetic marker without logging content.
These modes are manual workflow_dispatch only. Pull requests run the no-credential fixture tests. No trigger, schedule, agent-written PR, unattended task selection, or production use is activated yet.

## Acceptance
- Exact-head CI green: syntax/unit tests.
- With authorization, run shadow then synthetic-read; record verifiable run ID and Google authenticated read without exposing source bytes or credentials.
- Use an already-present negative-control scenario to prove SKIP, no Drive read.
- Future unseen, unattended autonomy trials are governed by existing Draft PR #159 and quality gates, not by a simulated fixture.
- Existing clinical, privacy, rights, reviewer and release HOLD gates remain unchanged.
