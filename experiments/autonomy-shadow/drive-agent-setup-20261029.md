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
      https://raw.githubusercontent.com/sheng-web-OS/Clinical_system/cc0ec4f8218b3bdb8038084590d8072e4ff553ae/tools/setup_drive_agent_wif.sh
    bash /tmp/setup-clinical-os-wif.sh YOUR_GOOGLE_CLOUD_PROJECT_ID

This URL pins the reviewed shell script to a specific commit rather than mutable branch HEAD. Review the script before running. It enables Google IAM/STS/Drive APIs and creates a dedicated SA and OIDC provider. It scopes trust to GitHub immutable numeric repository ID 1427690253, main branch and exact workflow_ref, then binds Workload Identity User to that narrow principalSet. It does not create downloadable SA keys or assign generic project Viewer/Editor roles to the Service Account.

The verified WIF provider path and Service Account email from the successful owner Cloud Shell output are now pinned in the synthetic-only workflow file in PR #222. No GitHub variables are needed for those non-secret identifiers. Do not configure long-lived Google keys.

## Phase 2: restrict the Drive source
Open the existing synthetic-only sandbox folder in Google Drive. Share ONLY that folder with the Service Account email as **Viewer**, and remove/downgrade any direct Writer access to the child document. Do not share the rest of My Drive. The non-secret synthetic folder ID is pinned inside the branch workflow so a GitHub Secret is not required for it; folder ACL is the access boundary. Never apply this pattern to private/clinical source identifiers. Do not add patient or restricted sources to this test folder.

**Verified Google Drive metadata (2026-10-29):** the synthetic sandbox folder and its single synthetic Google Doc both list the dedicated Service Account as **reader** (Viewer); no extra writer permission is listed. This verifies owner-side ACL configuration only. GitHub Actions OIDC authenticated access remains NOT_TESTED until model key, main protection and workflow activation are complete.

## Phase 3: model key and spend
In OpenAI Platform, create a **dedicated project** for Clinical OS Drive Agent. In its Limits settings, enable a **monthly hard spend limit** and alerts (suggest $5 USD/month hard limit and $2 alert initially), and restrict model/rate as needed. Hard spend enforcement is not instantaneous and can exceed the configured threshold slightly. Create a project API key with only required Responses API access. In GitHub Actions Secrets set:
- CLINICAL_OS_OPENAI_API_KEY (paste the new key only into GitHub's secret UI, never chat or PR)

The synthetic model is pinned to `gpt-5-mini` in the workflow for this test. Only the following repository Variables are required after owner approval:
- CLINICAL_OS_AGENT_ENABLED = true **only after all controls verified** (leave absent/false meanwhile)
- CLINICAL_OS_DRAFT_WRITES_ENABLED = true **only if the Draft PR scope remains approved** (leave absent/false meanwhile)

The existing ChatGPT Drive connector and ChatGPT subscription do not provide GitHub Actions with Google or model API credentials.

## Phase 4: enforce GitHub branch safety before enabling
As of the latest verification on 2026-10-29, GitHub API reports repository visibility PUBLIC and `main.protected=true`, after owner-side configuration. However, the Rulesets collection is empty and the connected GitHub integration receives HTTP 403 on branch-protection detail endpoints, so the exact PR requirements, `build` required-check designation, bypass identities, force-push and deletion prohibitions are **NOT_VERIFIED**. The runtime's preflight checks protected=true, which is necessary but not a substitute for auditing rule details.

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

## Owner-reported Cloud Shell result (2026-10-29)
Owner pasted successful output for Google project `instant-land-430112-t2`: pool `clinical-os-pool`, OIDC provider `github-drive-agent`, service account `clinical-os-drive-agent@instant-land-430112-t2.iam.gserviceaccount.com`, and IAM policy updated. This is a user-supplied execution log, not an independently authenticated Google Cloud IAM readback. GitHub Actions still has no verified WIF/Drive access. Sandbox Drive sharing remains owner-only; do not enable any credentialed workflow or merge until explicit main protection and correct secrets/variables are confirmed.

## 2026-10-29 reduction of manual account configuration
Pinned the owner-verified non-sensitive Google Cloud project number/provider, dedicated service account email, chosen synthetic sandbox folder ID and model name directly in the Draft PR workflow. Remaining manual GitHub setup is confined to branch protection, separate OpenAI API secret, and two explicit post-verification enable flags. These public synthetic IDs are not authentication material: no real source names or confidential file IDs may be substituted into the public repo. Verification must include a Google Drive folder-level Viewer ACL with no direct Writer override on its child document.

## 2026-10-29 branch and API-key checkpoint
- User reports the dedicated OpenAI project key has been saved to GitHub Actions Secret `CLINICAL_OS_OPENAI_API_KEY` with spending controls. Secret value, existence and API functionality cannot be read through this GitHub integration and remain runtime-NOT_TESTED.
- Owner Cloud Shell created OIDC provider/SA. Google Drive metadata readback verifies service account **reader** role on synthetic sandbox folder and child Doc. Actual GitHub Actions Google OIDC token exchange/Drive export remains NOT_TESTED.
- PR #227 was merged in main, replacing direct stage-II exam archive pushes with Draft PR and separate public-redistribution authorization gate. Its exact-main commit and check results were verified; agent #222 remains Draft and unmerged.
- To test, independently review this exact PR head; owner manually merges #222, then adds action variables `CLINICAL_OS_AGENT_ENABLED=true` and (after test and approval) `CLINICAL_OS_DRAFT_WRITES_ENABLED=true`. Run manual `shadow` first to test model without Drive; then `synthetic-read` to test Google OIDC + Drive and a Draft-only branch. Scheduled wake-up and any generated PR must remain bounded by synthetic-only allowlist, main protection, evidence check, and no auto merge/deploy.
