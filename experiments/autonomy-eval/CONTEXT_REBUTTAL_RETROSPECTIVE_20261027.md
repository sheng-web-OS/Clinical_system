# Context rebuttal gate — retrospective real-model pilot

**Date:** 2026-10-27 · **Status:** REPRODUCIBLE RETROSPECTIVE DEVELOPMENT TEST, not an independent efficacy result.

## Why this test exists

The previous genuine Workers AI comparison produced four responses from the **same full frozen DCM article**: Lite twice, Baseline twice, **16 suggested edits in total**. A direct source inspection exposed repeated false-positive *risks* in negative and quantifier scope (`不是所有`, `並不是`, `不代表`, `至少`). The gate described here was designed **after seeing those particular failures**. Therefore the same source/output pair is a **development set**, NOT an independently held-out evaluation, and no medical correctness or owner-time improvement can be claimed.

**Frozen source and output:** [raw original model responses](WORKERS_AI_DCM_PILOT_20261027_RAW.json) and article `content/xiaoma-reading/integrated/2026-10-21-dcm.md` at source commit `c5898a22636b265da3bc99aec387c346e7f6c386` (Git blob `f16eced854467e5c8e43a063ef5d34b93f0d1d15`). All four provider responses were valid and supplied actual model identity and usage.

## Method and exact counts

**Existing comparison (pre-gate):** 16/16 proposed findings received for review; proposal volume = eight per arm. There are only **nine unique quoted source locations** across the 16 suggestions. Existing source-checking located **13/16** as exact contiguous spans and **16/16** when ignoring whitespace/newline joins; the long combined-quotation mismatch is not automatically a fabricated claim.

**New *post-hoc* deterministic cue:** For each numbered model finding, match its `原文` quote to the **complete original article** (whitespace-insensitive, preserving source character positions), extract an adjacent source window, compare risk-bearing quantifier language in that quote to the `問題機制` critique. On high-risk scope mismatch, return `HOLD_FOR_CONTEXT_REVIEW`, with quote, original source location and nearby paragraphs. On absent source span, HOLD as well. A non-matching cue does **not** clear the finding: `REVIEW_REQUIRED_NOT_CLEARED`. No auto-accept or auto-reject is permitted. Implemented in `tools/autonomy_quality_lab.py:triage_revision_claims`; CLI `context`.

Measured on the original **16 real model-suggested changes**, the narrowly defined **scope-reversal cue** selected **7/16** for prioritized source-context rebuttal: 

| Original run | Proposed issues | Scope-reversal cues | Identification |
|---|---:|---:|---|
| Lite-1 | 4 | 2 | #2: `不是所有` criticized as `所有`; #3: `不代表` criticized as `不會影響` |
| Baseline-1 | 4 | 3 | #2: `不是所有`; #3: `不代表`; #4: `並不是` / "單獨" |
| Baseline-2 | 4 | 0 | All remain unverified and require ordinary context review |
| Lite-2 | 4 | 2 | #2: `不代表` / "直接關係"; #4: `至少` read as `只需要` |
| **Total** | **16** | **7** | Four repeated underlying source-caveat areas |

This is **43.75% triage flagging**, not precision, recall, clinically verified false-positive reduction, automatically suppressed edits, reader benefit, API-cost saving or owner-time saving. There were **zero automatically accepted and zero automatically rejected** suggestions; all 16 still require a trustworthy editorial decision. The gate detects a plausible mechanism for some obvious misreads, but the content's ground truth was not independently labeled and the developer had already seen those examples.

## Controlled counterexamples and engineering validation

`tests/test_editorial_context_rebuttal.py` adds ten adversarial tests, including four scope-reversal families; a quote with `不是所有` that **legitimately lacks a clinical explanation**, which must **not** be automatically rejected; a clean no-defect reply; a nearby existing causal explanation; cross-paragraph source quotes; an invented source span; and the **same 16 previously saved real model suggestions** (explicitly a regression, not new hidden validation).

At commit `07450d1c2ba6829664b0d79fc42658eb9abf7daa`, [GitHub Actions 40480941953](https://github.com/sheng-web-OS/Clinical_system/actions/runs/40480941953) completed **PASS**, with **217 Python unit/regression tests**, full site evidence checks and browser-image QA workflow success. The preceding commit `fc797a26a897fea6da4107d15cf41cadb34c2497` had [run 40479652949](https://github.com/sheng-web-OS/Clinical_system/actions/runs/40479652949) **FAIL** because Chromium installation exceeded the four-minute step timeout, not because of the editorial regression tests. The newer pass establishes that this install stall was not reproducible on the next run. It does not justify eliminating visual QA.

## Decision and authority

**KEEP ONLY AS DRAFT AGENT-INTERNAL TRIAGE:** Require the agent to check its own quotes against the complete original/nearby context *before* escalating a change. Scope-reversal cues or unknown quote origins must trigger a source-based rebuttal; do **not** silently accept, reject or publish a fix. Do not create an extra review request for the user merely because the lexical cue fired. Prefer autonomous non-writing source reinspection; human clinician involvement remains required for truly consequential medicine/release.

**REJECT CLAIM OF SUPERIORITY:** This was tuned after observing the same 16 failures. It proves a deterministic guard can flag known bad patterns, **not** that it will find unknown ones, avoid missed real issues, or save owner minutes. No new Cloudflare model calls were attempted because the previous independent grader was unusable and the account had returned HTTP 429 daily-free-allocation exhausted.

**Next falsifier when runtime/model quota is confirmed without paid change:** A previously unseen real article with both known valid missing-premise cases and clean passages, model outputs obtained under matching conditions, arm-blinded expert-calibrated judgment, costs and owner attention tracked. If correct proposals are blocked, unresolved false positives remain unchanged, or review effort increases, **remove/disable this extra triage**. Do not silently promote the prompt or claim autonomous medical quality from this pilot.

**State:** Draft PR #155 only; no production/article changes, no merge, no deployment, no new scheduled job, no new permanent memory database.
