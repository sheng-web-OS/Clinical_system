# Real incident memory retrieval pilot — decision record (2026-10-27)

**Evidence grade:** Retrospective engineering development pilot, NOT independent LLM retrieval/comprehension or clinical validation. Decision owner: PR #155, existing single incident ledger [issue #133](https://github.com/sheng-web-OS/Clinical_system/issues/133); no second ledger and no change to public articles.

## Actual source and procedure

Read the current canonical *private* GitHub issue #133 through the linked GitHub read-only connector during this turn. At evaluation it contained **5,738 Unicode characters** and **six recognizable incident sections** (`F-001`–`F-004`, `EVAL-001`, `EVAL-002`). Each F-row was capped at 1,800 characters and each EVAL-section at 18 lines / 1,800 characters, matching the corresponding `select_experiences` excerpt and exact-term ranking rules in `tools/autonomy_quality_lab.py`. The counting experiment was executed against the real issue body (not synthesized source text); it used a JavaScript mirror of the Python matching and ranking semantics and therefore is *not* a separately authenticated production Python trace.

Seven task queries, six based on incidents already known to the experimenter and one irrelevant negative control, were manually selected from exposed issue history. They are NOT a hidden dataset, and their labels are NOT independent reviewer opinions. Same terms and original source were used for every retrieval comparison. Baseline: load entire canonical issue for every task. Treatment v0: load three best matching incident excerpts by count of exact query terms.

| Case | Task cue terms | Known target | Top-three v0 result | Correct target retrieved? |
|---|---|---|---|---|
| M01 | ECG, 手機 | F-001 | F-001 | Yes |
| M02 | metadata, 編輯 | F-002 | F-002, F-003 | Yes; 1 extraneous |
| M03 | 歷史原稿, 分類 | F-003 | F-003, EVAL-002 | Yes; 1 extraneous |
| M04 | 並行, PR | F-004 | EVAL-001, EVAL-002, F-001 | **No** |
| M05 | worker, trace | EVAL-001 | EVAL-001 | Yes |
| M06 | 天花板, 試跑 | EVAL-002 | EVAL-001, EVAL-002 | Yes; 1 extraneous |
| M07 | 藥物過敏, 時間順序 | no incident | none | Correct negative |

## Measured output and its meaning

- **5/6 relevant known incidents present in top-three retrieval** (83.3% recall on these selected cues; not the chance an AI correctly detects a defect).
- **4/7 query outputs contained an irrelevant incident** (M02/M03/M04/M06); across positive queries there were 5 relevant hits in 11 returned excerpts (45.5% returned-item precision in this exposed set).
- **Mean 1,051 excerpt characters per query vs. 5,738 characters** for the complete source, approximately **81.7% fewer task-memory characters** with v0 exact matching. This is not token, model-billing, latency or human-minute savings.
- **Failure mechanism:** M04's meaning-bearing `並行` did not literally occur in the incident row, which uses `平行`. The generic `PR` occurred in multiple other records, displacing F-004. A full log contains F-004 but does **not** guarantee an LLM will find it.

## Experiment-driven decision (implemented in owning PR)

**REJECT:** Automatically treating a top-three lexical match as a sufficient autonomous failure memory. A demonstrated known-case miss is unacceptable for release or safety screening even though it saves characters.

**KEEP, with fail-open-to-evidence escalation:** The existing lightweight snippet preview can remain an *optional task context aid*, but when there is no **unique incident containing every requested exact term**, `select_experiences` now returns `requires_full_issue_review=true`, and callers must fall back to reviewing the complete canonical #133 issue. Independently, it always returns `memory_adequacy_verified=false` because token overlap cannot prove relevance or medical accuracy. A unique exact match merely permits a compact preview; it is not medical/semantic acceptance.

The same seven exposed queries predict narrow previews for M01/M03/M05 and full-issue escalation for M02/M04/M06/M07; **4/7 would escalate**. This is a *same-data engineering guardrail*, not an independent performance improvement or new-model A/B. Fallback means the source is available, **not** that F-004 was autonomously recognized. A new, unexposed synonym/latent-dependency evaluation is required before switching off that fallback.

**Owner cost decision:** #133 is currently short (5,738 characters). Do **not** deploy a vector DB, persistent Claim Graph, synonym taxonomy or new retrieval service to chase marginal compression. Reassess if issue volume, task costs and independent retrieval quality warrant it.

## Separate upcoming quality acceptance

This experiment does not compare original article reviewing quality across prompt arms. The pinned real-article `3×2×3` packet pilot only establishes input reproducibility; no model calls or clinician-adjudicated scores are claimed. Existing preregistered protocol/task hashes must not be silently replaced. PR remains Draft, no merge/publish, no increase in #137 autonomy rating.
