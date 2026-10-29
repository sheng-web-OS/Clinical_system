# Clinical OS selective Drive Agent — selected authorization / execution contract

Date: 2026-10-29. Status: DRAFT/HOLD. Public repository; only synthetic fixtures. The user selected: keyless GitHub OIDC to dedicated Google Service Account; access to the one synthetic Google Drive folder; independent OpenAI API key with spend controls; agent may read, repair synthetic fixture and create a Draft PR, never merge or deploy.

## Already configured (verified)
- A synthetic-only Google Doc was written and read back using the existing ChatGPT Google Drive connector, then moved under the synthetic-only sandbox folder. This is not proof that GitHub Actions can access Drive.
- GitHub PR #222 contains a synthetic source-gap fixture, model decision planner, deterministic fail-closed READ/SKIP/HOLD, source marker checker, isolated Draft PR writer, and keyless WIF setup script.
- PR tests must pass on the exact SHA; verification runs can test only no-secret fixture mode until owner completes external permissions.
- The runtime cannot install GitHub Secrets, create Google Cloud IAM, share the folder to a new service account, establish an OpenAI project budget, or place a key into GitHub without owner's account-level authorization.

## Phase 1: owner setup in Google Cloud Shell (not in GitHub Actions)
Create or select a **dedicated** Google Cloud project. Download the reviewed repository script once, or open its contents and run in Cloud Shell:

    curl -fsSLo /tmp/setup-clinical-os-wif.sh \
      https://raw.githubusercontent.com/sheng-web-OS/Clinical_system/e65063cc4820239c9fbf7e049ae5222565f069e4/tools/setup_drive_agent_wif.sh
    bash /tmp/setup-clinical-os-wif.sh YOUR_GOOGLE_CLOUD_PROJECT_ID

This URL pins the reviewed shell script to a specific commit rather than mutable branch HEAD. Review the script before running. It enables Google IAM/STS/Drive APIs and creates a dedicated SA and OIDC provider. It scopes trust to GitHub immutable numeric repository ID 1427690253, main branch and exact workflow_ref, then binds Workload Identity User to that narrow principalSet. It does not create downloadable SA keys or assign generic project Viewer/Editor roles to the Service Account.

Copy the two output values into GitHub Actions Variables:
- CLINICAL_OS_WIF_PROVIDER
- CLINICAL_OS_GCP_SERVICE_ACCOUNT

DO NOT configure long-lived Google keys.

## Phase 2: restrict the Drive source
Open the existing synthetic-only sandbox folder in Google Drive. Share that folder with the output Service Account email as **Viewer**; do not share the rest of My Drive. In GitHub Repo Settings → Secrets and variables → Actions add the secret:
- CLINICAL_OS_DRIVE_FIXTURE_FOLDER_ID = the synthetic-only folder ID from the verified folder URL.

The folder ID is not a password, but put it in an Actions Secret to minimize unnecessary identifier exposure. Do not add any patient or restricted sources to this test folder.

## Phase 3: model key and spend
In OpenAI Platform, create a **dedicated project** for Clinical OS Drive Agent. In its Limits settings, enable a **monthly hard spend limit** and alerts (suggest $5 USD/month hard limit and $2 alert initially), and restrict model/rate as needed. Hard spend enforcement is not instantaneous and can exceed the configured threshold slightly. Create a project API key with only required Responses API access. In GitHub Actions Secrets set:
- CLINICAL_OS_OPENAI_API_KEY (paste the new key only into GitHub's secret UI, never chat or PR)

In Actions Variables set:
- CLINICAL_OS_AGENT_MODEL = gpt-5-mini (change only after checking currently allowed model and rate)
- CLINICAL_OS_AGENT_ENABLED = true **only after all controls verified**
- CLINICAL_OS_DRAFT_WRITES_ENABLED = true **only if the selected Draft PR scope remains approved**

The existing ChatGPT Drive connector and ChatGPT subscription do not provide GitHub Actions with Google or model API credentials.

## Phase 4: enforce GitHub branch safety before enabling
As of configuration date, GitHub API reports repo visibility PUBLIC, main protected=false, and no rulesets. The runtime's preflight **will refuse to use model or Drive credentials** until main is protected.

GitHub Repo → Settings → Branches → Add branch protection rule (or Rulesets) for main:
- Require a Pull Request before merging; enforce review by another authorized account where feasible.
- Require passing CI/status checks; prevent force pushes and branch deletion.
- Do not grant bypass to automation. Limit direct push permissions.
- Under Settings → Actions → General, review Workflow permissions; if needed enable "Allow GitHub Actions to create and approve pull requests" to allow **draft creation**, not approval/merge. Script never requests approval or merging.

Once branch protections, Google SA sharing, WIF, and spending limits are verified, **the user must manually merge** the reviewed PR #222 into main to make the new workflow dispatch/schedule active. No automatic merge is authorized.

## Actions runtime and roles
- Pull request: run only no-credential regression fixtures. No model, Drive, or write access.
- Daily scheduled wake-up or owner workflow_dispatch: preflight looks for existing proof in main, existing open bot PR, and main branch protection. If no gap, SKIP without calling AI or Drive.
- Agent phase: model receives a short **synthetic, non-sensitive** gap record, decides SKIP/READ/HOLD. A deterministic gate blocks all non-allowlisted sources. A READ may trigger an OIDC-authenticated read in the *same read-only job*. It exports ONLY a boolean read_verified via GITHUB_OUTPUT.
- Draft phase: a **separate job with no OpenAI Key or Google credentials** may create one idempotent synthetic Draft PR from a fixed non-sensitive template when read_verified=true; it never writes source content or merges. If GitHub declines Actions-created PRs, fail closed and check repository Actions settings.
- A GITHUB_TOKEN-created Draft PR may not trigger all PR workflows automatically; verify exact-head CI explicitly. Do not represent Draft or green CI as medical review or approval.

## Measurable acceptance
1. PR exact-head fixture tests and syntax check pass.
2. Owner completes external permission setup and manual merge after code review.
3. First trusted main run with shadow: actual model invocation, no Drive read.
4. Second trusted main run with synthetic-read: actual OIDC-authenticated file read, verified marker, separate synthetic Draft PR; record GitHub run ID, PR and exact SHA.
5. Negative-control "source already present" and "draft already open" must SKIP and avoid wasted model or Drive accesses.
6. This only validates technical orchestration. Blind/unknown-source reasoning, user intervention minutes, clinical quality and autonomy-transfer criteria remain governed by PR #159 and existing independent medical, privacy, copyright and publication gates.

NO restricted materials, patient data, confidential titles/IDs or copyrighted full sources should ever enter GitHub, public CI logs or the published site.

## 2026-10-29 WIF pool-name regression
A real Cloud Shell run found that the Google Workload Identity Pool display name (34 characters) violated the 32-character maximum; the provider display name was also 36 characters. The script was fixed to use 24/18-character names. The already-downloaded old version can be repaired locally by sed replacements. No claim is made that Cloud Shell creation succeeded until actual Google output is inspected.
