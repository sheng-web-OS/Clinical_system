# GitHub Models real-article execution probe — FAILED CLOSED (2026-10-27)

## Question / scope

Can Clinical_system execute at least one authentic standalone model review on the same unchanged **public** DCM article through a GitHub Actions token, so the frozen baseline/Lite research can proceed without a new long-lived API credential?

**Evidence level:** failed provider-transport/execution attempt, **not** a model-performance experiment. No result is a medical, teaching, autonomy or savings measurement.

## Frozen inputs / permitted exposure

- Exact original article: `content/xiaoma-reading/integrated/2026-10-21-dcm.md`; original source commit `c5898a22636b265da3bc99aec387c346e7f6c386`; Git blob `f16eced854467e5c8e43a063ef5d34b93f0d1d15`.
- Endpoint: `https://models.github.ai/inference/chat/completions`; requested model `openai/gpt-4.1`. Provider model identity can be established **only if** a proper response actually arrives.
- Intended conditions: one API call with short task-specific Lite review, one with baseline professional review; maximum two stateless calls on an unchanged full article, output capped at 1,250 tokens per call, `temperature=0.2`. No external source grounding or expert adjudication; any success would remain a *single-article exploratory pilot*, not the previously preregistered 3×2×3 model study.
- Temporary branch-only GitHub Action used `contents:read`, `models:read`; no write permissions, deployment, repo secrets, private operational SOP or new API key. A short-lived `GITHUB_TOKEN` authenticated the request. Source copied only from the already-public teaching article.

## What actually happened

1. Original run [40476272164](https://github.com/sheng-web-OS/Clinical_system/actions/runs/40476272164) reached first Lite API call, then failed while parsing an HTTP 200 response as JSON. **No model output saved.**
2. Diagnostic run [40476389745](https://github.com/sheng-web-OS/Clinical_system/actions/runs/40476389745) reproduced the first-call failure and recorded: `NON_JSON_PROVIDER_RESPONSE 200 text/plain bytes 4 prefix b'OK\\r\\n'`. No valid `choices[0].message.content`, provider `model` field or token usage was returned. Second arm **never started**.
3. The temporary triggering workflow was **deleted** after the diagnostic. The one-shot request script was also deleted (history preserves its exact source), to avoid unattended retry/cost/security surface. Public site, main, clinical text and deployment settings unchanged.

**Result:** **0/2 valid model completions**; one failing first-arm call in each of two separate troubleshooting runs, not two paired trials. HTTP 200 proves only a transport-level response, **not** model inference. The underlying reason for this environment's `200 OK` stub is **NOT_ESTABLISHED**; it would be false to blame GitHub Models generally or claim a provider model actually ran. Billing/token usage: **NOT_MEASURED** (no provider usage object). Owner-time savings: **NOT_MEASURED**.

## Action from failure (implemented)

`tools/autonomy_quality_lab.py:validate_model_completion_response` now rejects 200 + plain text, missing model identity, missing choices, blank completions and non-JSON response bodies. Regression tests include the observed `OK` case and a structurally valid synthetic JSON example that still cannot claim clinical validation.

**Decision:** **STOP** attempts through this endpoint/environment until a genuine provider response containing explicit model identity, choices, valid text and usage evidence can be retrieved under audited short-lived, least-privilege access. Do not fabricate a success count or replace a failed arm with another provider/model without preregistering an amended comparison. The independent medical content A/B remains **NOT_EXECUTED**.

Adjacent completed engineering evidence: [memory retrieval pilot](REAL_INCIDENT_MEMORY_PILOT_20261027.md), source-pinned three-article packet tests, [PR #155](https://github.com/sheng-web-OS/Clinical_system/pull/155). No merge, publication or maturity promotion is justified by the failed inference probe.
