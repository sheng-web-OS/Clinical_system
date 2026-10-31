# ALE｜Adaptive Progressive Concept Card (synthetic engine v0)

**Owner decision, 2026-11-01:** One Concept Family may have one integrated Anki note with progressive MCQ, Cloze, numeric and transfer stages. Do not force the learner to answer all stages on every review. ALE chooses the smallest useful diagnostic stage from evidence and returns the next stage, or defers to Anki/FSRS.

## Runnable public-safe implementation
- Selector: `tools/ale_adaptive_stages.py`
- Regression tests: `python -m unittest discover -s tests -p 'test_ale_adaptive_stages.py' -v`
- The engine accepts only `PUBLIC_SYNTHETIC_ONLY` role-token JSON. No real learner answers, course history, private Drive rows, Anki card IDs or hidden questions are permitted in public fixtures.
- Output is **one stage** and an explainable reason, plus the status of every stage. It does not write to any service.

## Stage contract
Packet keys: `classification`, `concept_id`, `stages`, `evidence`, `review_day`.

Each stage: `id`, `mode` (MCQ/CLOZE/NUMERIC/TRANSFER/EXPLANATION), `requires` (earlier stage IDs).

Each synthetic evidence item: `event_id`, `stage_id`, `item_id`, `day_index`, `outcome` (PASS/FAIL/UNSURE), `confidence` (CONFIDENT/LOW/GUESS), `unhinted`, `learner_unseen`, `reasoning_supported`, `source_verified`, `answer_exposed_before`. All flags are explicit booleans. Day indexes represent synthetic relative days, not real event timestamps.

State machine: `NOT_OBSERVED`, `OBSERVED_GAP`, `UNCERTAIN`, `WEAK_PASS_NEEDS_DIAGNOSIS`, `NEAR_PASS_OBSERVED`, `DELAYED_PASS_OBSERVED`. A delayed pass requires at least two source-verified, confident, unhinted, learner-unseen responses with reason support using **different items on different days**. This is a provisional observation rule, **not validation of durable mastery**.

Selection priority:
1. A documented failure; if a prerequisite has no qualified observation, diagnose the prerequisite first, otherwise recheck the failed stage using a fresh variant.
2. A guess, low-confidence response, weak explanation or exposed answer: test that stage diagnostically; never label it mastery.
3. Untested stages: assess in dependency order. `NOT_OBSERVED` must not silently become PASS when skipped.
4. Once every stage has at least a near-pass, prefer a higher-level delayed unseen-transfer test after an elapsed day. Do not repeat same-day passes simply to complete all blanks.
5. No diagnostic stage due: return `DEFER_TO_ANKI_FSRS`. ALE does not replace Anki scheduling.

The policy is deterministic and intentionally conservative. It makes no claim to optimum information gain, semantic error-diagnosis accuracy, clinical source validation or improved learning outcomes. A wrong answer does not prove which mechanism failed; subsequent stage choice is a **diagnostic hypothesis**.

## Minimal public synthetic example
```json
{
  "classification": "PUBLIC_SYNTHETIC_ONLY",
  "concept_id": "illustrative-bayes",
  "stages": [
    {"id": "phenomenon", "mode": "MCQ", "requires": []},
    {"id": "mechanism", "mode": "CLOZE", "requires": ["phenomenon"]},
    {"id": "transfer", "mode": "TRANSFER", "requires": ["mechanism"]}
  ],
  "evidence": [],
  "review_day": 0
}
```
Save to a local file and run `python tools/ale_adaptive_stages.py --input /path/to/fixture.json`.

## Required before practical Anki integration
1. Owner-private bridge reads the authorized Google Sheet as the source of learner state; do not replicate personal rows into this public repo.
2. Verified event ingestion must retain item/answer exposure and detailed rationale at the **private boundary**. Anki's Hard/Good/Easy ratings alone cannot identify which reasoning stage failed.
3. Design a **single-note interactive renderer** with stage-level answer capture, cross-device persistence and deliberate controls. Native Anki Cloze `c1/c2/c3` normally generates separate sibling cards, so native Cloze fields alone do not satisfy this concept.
4. Freeze the exact tested content contract and SHA256 after stage wording, answer key and provenance have been independently checked; until then no `IMMUTABLE` or `SYNCED` claim.
5. Pilot with unseen variants and matched static-review baseline. Compare learner-unseen transfer, delayed outcome, study minutes, wrong diagnostic branches and manual interventions. No automated card import or medical publication before acceptance.

## Integration / scope
Continue the existing ALE chain in #258 and Draft #260, with #254 controlling competing priorities. Public code only. No new scheduler, no paid API, no Anki/FSRS mutation, no Google Sheet edit, no change to frozen #137 historical attribution. Synthetic tests support the *engineering rule implementation*, not a real private teaching closed loop.
