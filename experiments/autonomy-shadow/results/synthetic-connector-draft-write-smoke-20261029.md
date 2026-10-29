# Synthetic Draft PR write smoke test — 2026-10-29

**Status:** DRAFT / HOLD. This document is entirely synthetic control metadata, not a medical article, source copy, reviewer receipt, or release approval.

## Independently observed read prerequisite

- Repository: `sheng-web-OS/Clinical_system`, PUBLIC; `main` branch protected when tested.
- Read-only GitHub Actions run: https://github.com/sheng-web-OS/Clinical_system/actions/runs/40813334428
- Run's exact main commit: `472f38562c09a4d06c8fcf7d5ea0cebd42777b81`.
- Actual sanitized agent result: `{"ai_decision":true,"decision":"READ","drive_read_verified":true,"mode":"synthetic-read","autonomy_certified":false}`.
- Google OIDC and synthetic Drive marker check succeeded. In **that** run the `draft` job was SKIPPED because the Draft write gate was not enabled.

## This one-time write test

This file and its Draft PR are written **through the authenticated ChatGPT GitHub connector**, on a branch scoped to this test, after checking the previous run. This verifies the connector's ability to make a reviewable, non-main Git commit and open a Draft PR. **It is NOT evidence that GitHub Actions' draft job executed, nor that a model autonomously wrote this PR.** Do not describe it as an end-to-end Actions execution.

The file deliberately contains **no Drive contents, file IDs, patient data, restricted material, model prompts, secrets, or private evaluations**. It is outside the site publication allowlist. The PR stays unmerged and unapproved.

## Boundary and next science question

This smoke test establishes write mechanics, not clinical capability or causal benefit. Subsequent work should use existing Draft/HOLD PR #225 to test selective source retrieval and first-pass decision improvement on genuinely unfamiliar cases, keeping source/review materials outside this public repository. Compare Native, Native + the same source pack, and Native + source pack + narrowly triggered Skill; include normal and boundary controls. Independently assess retrieval choice, evidence-linked decision pivots, P0/P1 errors, false positives, new-case transfer, provider cost and measured owner intervention time. Never count a green CI or self-evaluation as a clinical-learning success.

**Release gate:** no merge, no automatic deployment, no scheduling, no medical approval.
