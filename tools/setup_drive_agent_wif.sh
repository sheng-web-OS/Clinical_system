#!/usr/bin/env bash
# One-time, owner-run Google Cloud Shell setup; NO service-account keys.
# Usage: bash tools/setup_drive_agent_wif.sh YOUR_GCP_PROJECT_ID
set -euo pipefail
PROJECT_ID="${1:?Provide a Google Cloud project ID as the first argument}"
REPO_ID="1427690253"
REPO="sheng-web-OS/Clinical_system"
POOL="clinical-os-pool"
PROVIDER="github-drive-agent"
SA_NAME="clinical-os-drive-agent"
WORKFLOW="${REPO}/.github/workflows/drive-source-agent.yml@refs/heads/main"
if [[ ! "$PROJECT_ID" =~ ^[a-z][a-z0-9-]{4,28}[a-z0-9]$ ]]; then
  echo "Invalid Google Cloud project ID" >&2
  exit 2
fi
gcloud config set project "$PROJECT_ID" >/dev/null
PROJECT_NUMBER="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')"
test -n "$PROJECT_NUMBER"
gcloud services enable iam.googleapis.com iamcredentials.googleapis.com sts.googleapis.com drive.googleapis.com --project "$PROJECT_ID"
if ! gcloud iam workload-identity-pools describe "$POOL" --location=global --project="$PROJECT_ID" >/dev/null 2>&1; then
  gcloud iam workload-identity-pools create "$POOL" --location=global --project="$PROJECT_ID" --display-name="Clinical OS GitHub synthetic agent"
fi
if gcloud iam workload-identity-pools providers describe "$PROVIDER" \
  --workload-identity-pool="$POOL" --location=global --project="$PROJECT_ID" >/dev/null 2>&1; then
  echo "Existing provider found; STOP. Verify issuer, mapping and conditions before reusing." >&2
  exit 2
fi
gcloud iam workload-identity-pools providers create-oidc "$PROVIDER" \
  --project="$PROJECT_ID" --location=global --workload-identity-pool="$POOL" \
  --display-name="GitHub Actions synthetic Drive agent" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository_id=assertion.repository_id,attribute.ref=assertion.ref,attribute.workflow_ref=assertion.workflow_ref" \
  --attribute-condition="assertion.repository_id=='${REPO_ID}' && assertion.ref=='refs/heads/main' && assertion.workflow_ref=='${WORKFLOW}'"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
if ! gcloud iam service-accounts describe "$SA_EMAIL" --project "$PROJECT_ID" >/dev/null 2>&1; then
  gcloud iam service-accounts create "$SA_NAME" --project "$PROJECT_ID" --display-name="Clinical OS synthetic Drive Viewer"
fi
MEMBER="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL}/attribute.repository_id/${REPO_ID}"
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" --project="$PROJECT_ID" \
  --role="roles/iam.workloadIdentityUser" --member="$MEMBER" >/dev/null
cat <<OUTPUT

Google Cloud OIDC configured. No credentials created.
GitHub variable CLINICAL_OS_WIF_PROVIDER:
projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL}/providers/${PROVIDER}
GitHub variable CLINICAL_OS_GCP_SERVICE_ACCOUNT:
${SA_EMAIL}

NEXT: Share ONLY the synthetic Google Drive sandbox folder with this Service Account email as VIEWER.
NEXT: Configure GitHub repo Actions variables and Secrets; owner must enable only after reviewing.
OUTPUT
