# Clinical_system real-model prompt pilot: decision report

**Date:** 2026-10-27, Asia/Taipei  
**Evidence:** [frozen protocol](WORKERS_AI_DCM_PILOT_20261027_PROTOCOL.json) committed at `401d593718556397101d76543f4e03be39da049a` **before** the review calls; [raw original four model completions](WORKERS_AI_DCM_PILOT_20261027_RAW.json) committed at `37b52621c65087c2a69263f96875aa4e255901bf`. This is **exploratory real AI inference**, not the older 3×2×3 preregistered blinded experiment, not independent clinician review, and not public-site proof.

## Actual execution and controls

- The **same complete 11,661-character DCM teaching article** from Git commit `c5898a22636b265da3bc99aec387c346e7f6c386`, Git blob `f16eced854467e5c8e43a063ef5d34b93f0d1d15`, was included in every request. Already-public text only; original article unchanged.
- Worker endpoint: connected Cloudflare Workers AI `@cf/meta/llama-3.3-70b-instruct-fp8-fast`, stateless requests. Provider **reported** `@cf/meta/llama-3.3-70b-instruct-sd` in all four actual completions; the discrepancy between requested and reported suffix is preserved and **must not be silently called an exact model-version pin**.
- Fixed temperature 0.2, 1,400-token maximum, identical common prompt and exact article; only baseline vs Lite addition differed. In advance, order was frozen as Lite-1, Baseline-1, Baseline-2, Lite-2. All four requests returned structurally valid, non-empty model content with model identity and provider-reported usage. This is four distinct API calls, NOT proof of four fully isolated agent workspaces or independent physician judgments.
- Per arm, two reviews returned four proposed issues each. Raw answers have full text and source locators. Identical prompts/temperature across repetitions do not guarantee independent stochastic draws, and model sampling/serving internals were not exposed.

| Measure | Baseline (two calls) | Lite (two calls) |
|---|---:|---:|
| Valid model replies | 2/2 | 2/2 |
| Candidate findings | 8 | 8 |
| Exact contiguous claimed source quotes | 6/8 | 7/8 |
| Claimed quotes found if paragraph whitespace removed | 8/8 | 8/8 |
| Provider prompt tokens | 12,890 | 13,016 |
| Provider completion tokens | 1,065 | 1,095 |
| Provider total tokens | 13,955 | 14,111 |
| Provider neurons (usage) | ~561.864 | ~571.368 |
| Expert-confirmed actionable unique teaching defects | **NOT_MEASURED** | **NOT_MEASURED** |
| Owner intervention minutes | **NOT_MEASURED** | **NOT_MEASURED** |

Total four worker calls: **28,066 tokens**, 16 candidate findings anchored to **nine unique underlying quoted locations** across both arms. Three long quotes stitched originally separate paragraphs into one line; this is a *contiguity violation*, **not proof that the underlying words were invented**. All 16 were found after whitespace-insensitive matching. The evidence-checking function `audit_generated_finding_quotes` distinguishes those cases and never grants medical correctness or editing authority.

## Observed failure pattern (source-based textual cross-check; not clinician-adjudicated ground truth)

Both arms repeatedly flagged problems that the same article already explicitly limits or explains. These examples require no external medical claim:

1. **Direct scope reversal (Lite-1 and Baseline-1):** the original says `這不是所有 DCM 都必然遵循的單一病程`; both workers criticize it for allegedly implying *all* DCM patients share one inevitable path. The proposed explanation is already in the quoted sentence.
2. **Existing mechanism ignored (all four responses):** the original says `EF 下降，不代表每一次心跳送出去的血液必然立刻大幅減少`, immediately presents `EF = (EDV − ESV) / EDV`, and explains larger EDV maintaining stroke volume temporarily. All four responses suggest more explanation or claim the mechanism is missing.
3. **Explicit imaging boundary ignored (Baseline-1):** the original says `並不是單憑一種 LGE pattern 就能完成病因診斷`; the worker alleges readers may think LGE alone completes the diagnosis and recommends stating the same caution.
4. **Figure legend rephrased (Baseline-2 and Lite-2):** the same caption already describes ESPVR (systolic mechanical property) versus EDPVR (passive filling pressure at different volumes), while the responses suggest adding essentially those descriptions.
5. **'At least' misread as 'only' (Lite-2):** the original says `治療 DCM 時，至少要同時處理三個層次`; the model recommends clarifying that there can be more than those three.

Other claims concern the two-layer explanation of the DCM definition, taxonomy and the three investigative considerations. They may be legitimate editorial preferences in some cases, but no evaluator has established a genuine missing prerequisite or medical defect; they cannot be credited as recovered important issues. **No diagnosis or treatment text was modified in response to these flags.**

### Blind adjudication and quota limits

- Before grading, committed [blind grading protocol](WORKERS_AI_DCM_PILOT_20261027_JUDGE_PROTOCOL.json) to anonymize all sixteen findings and rate in forward/reverse order with a different model. The first requested Gemma-4 grader produced **2,450 output tokens but empty visible content**; `0/1` usable ratings. Preserved raw identity/usage in [JUDGE_RAW.json](WORKERS_AI_DCM_PILOT_20261027_JUDGE_RAW.json).
- After openly committing a [post-hoc judge substitution amendment](WORKERS_AI_DCM_PILOT_20261027_JUDGE_AMENDMENT.json), an attempt to call Mistral as a cross-model grader failed with **Cloudflare HTTP 429 / code 4006: daily free allocation of 10,000 neurons exhausted**. This account-wide quota may include other activity; do **not** attribute the entire 10,000-neuron budget to these study calls. Saved [MISTRAL_JUDGE_RAW.json](WORKERS_AI_DCM_PILOT_20261027_MISTRAL_JUDGE_RAW.json). **No usable independent blind grades were obtained**, and no further model calls were made. Do not silently upgrade the account, switch paid providers, or repeatedly retry.
- Provider token usage and neurons are actual reported quantities for the four worker responses; these are **not** a validated monetary bill. Real editor minutes / medically verified severity remain NOT_MEASURED.

## Decision — act on measured evidence, not rhetoric

**STOP / DO NOT PROMOTE:** neither baseline nor Lite exhibited evidenced, independently verified advantage in useful error discovery on this DCM pilot. Lite's 8 candidates are not more useful by observable anchor metrics, despite its modestly larger prompt and output budgets. Both arms exhibit conspicuous and repeated **already-explained / negation-scope false-positive risk**. Four replies with four findings each despite explicit permission to find no defect is a candidate overproduction warning, not proof that the article has zero real defects.

**KEEP:** genuinely working read-only Cloudflare model inference interface and source-pinned experiment packets as *experimental* components, with exact response identity/usage capture and no site mutation.

**INTRODUCE GUARDRAIL IN BRANCH, NOT PROD:** `tools/autonomy_quality_lab.py audit` checks literal evidence spans, paragraph-break normalization and warning qualifiers (`不是所有`, `不代表`, `至少` etc.), returns `medical_quality_verified=false` and `public_edit_allowed=false`. This does **not** automatically determine whether a proposal is correct; independent review against full adjacent context and relevant clinical evidence is necessary. Added synthetic adversarial tests.

**COST AND OPERABILITY STOP:** daily Workers AI free allocation was exhausted before any independent model verdict. Suspend further inference and reject paid quota change without separate approval; first optimize scoped evaluation, constrained outputs and measurement quality, not whole-site repeated LLM scans.

**REQUIRED BEFORE MATURITY INCREASE:** fresh unhinted *new-article* holdout, matched clean controls, clinician-calibrated double-blind adjudication of medical/teaching importance, valid provider identity/usage, zero P0/P1 regression, repeatable account quota/operating budget, and owner-minute reduction. None is currently validated. Repo stays Draft; no merge/deploy/release.

## Maintenance safeguard

Original one-time source-pinned packet replay test moved from always-on `tests/` into an opt-in `experiments/autonomy-eval/test_real_corpus_packets.py`, because a normal future article edit should not make unrelated production CI fail merely for diverging from a frozen 2026-10-27 experiment. Keep immutable input identity *in experimental records*, not as a permanent prohibition on editing the website.
