# 無人督導能力：可驗證的 Shadow Evaluation（暫未達標）

This is an evaluation gate, **not** an autonomous AI runner and not evidence of clinical safety. It reuses [#133](https://github.com/sheng-web-OS/Clinical_system/issues/133), [#137](https://github.com/sheng-web-OS/Clinical_system/issues/137) and [PR #155](https://github.com/sheng-web-OS/Clinical_system/pull/155); no new failure ledger, dashboard, scheduler or publish authority.

## What counts

Before any future scheduled execution, register a fixed cohort task in `registry.json`: `id`, `issue`, and (initially absent) `trigger_run`, `pull_request`, `ci_run`. Update these IDs only when events actually occur, and retain unfinished tasks in the denominator. Register the task issue *before* the automated run; a user-requested / manually dispatched workflow never counts as unprompted autonomy.

The read-only evaluator verifies GitHub evidence: a successful scheduled run, issue created before the run, draft PR created by a bot after scheduling, exactly the approved `main` target, **only `tools/` or `tests/` changes**, complete file list, successful CI on the exact PR head SHA, and an approving review from a different GitHub account tied to that SHA. Any missing, stale, unauthorized, or invalid condition fails closed. A GitHub `APPROVED` event establishes *distinct GitHub identity*, **not** reviewer medical expertise, blind independence, or that the owner never prompted the bot in another channel. No automatic merges or production deployment.

Run locally or in read-only CI:

```bash
GITHUB_TOKEN=... python tools/autonomy_shadow_eval.py \
  --registry experiments/autonomy-shadow/registry.json \
  --out autonomy-shadow-report.json
python -m unittest discover -s tests -p 'test_autonomy_shadow_eval.py'
```

Never commit a token or identifiable patient content. The token needs **read-only** repository/Actions/PR access. GitHub Actions can supply `secrets.GITHUB_TOKEN`; the evaluator issues only GET requests. The report is a disposable CI artifact, not a public medical page.

## Distinct truth claims

- `VERIFIED_SHADOW_DELIVERY` means **limited technical delivery on a scheduled bot-driven engineering task**, not proof of autonomous reasoning, medical accuracy, teaching outcome, user attention savings, or genuine freedom from off-platform prompting.
- `NOT_VERIFIED` includes missing evidence, incomplete work, changed SHA and unsafe changes. Never silently remove unsuccessful registered tasks from denominator.
- `owner_time=NOT_MEASURED` until a separate, low-friction independent owner-time sample is collected. Never infer 0 minutes from a bot PR.
- `clinical_quality`, `pedagogy`, `real_world_unprompted` remain `NOT_VERIFIED` without separate observation and independent assessment; don't turn one green CI into a clinical pass.

**Next independent trial**: #157 is the first preregistered trial and is **NOT_STARTED**. The phase-1 runner is not yet implemented. Eventually register at least 20 representative tasks in a fixed cohort (engineering, evidence, visual and narrative defects). Phase 1 only permits read-only discovery and reversible engineering draft work; clinical edits are graded separately under EPQC/continuity/source/figure gates. Compare before/after real owner minutes, interruption counts, undisclosed severe failures, and first-pass independent acceptance across comparable tasks. Predeclared failures count. Any unapproved publication, P0/P1 escape, or identity/rights breach halts autonomy escalation. No autonomy promotion based on fixture unit tests alone.

**2026-10-27 baseline**: **1 preregistered task, 0 executed**, therefore no evidence of successful unsupervised work; owner minutes and clinical/teaching safety remain **NOT_MEASURED/NOT_VERIFIED**. Unit tests only show that the verifier rejects common false passes. This document does not activate a scheduler or declare any real AI agent has been tested.
