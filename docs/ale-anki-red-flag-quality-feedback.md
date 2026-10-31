# ALE-01 | Anki red flag -> private card-quality feedback

Owner decision (2026-10-31, Asia/Taipei): **Anki native red flag is the default user feedback gesture.** The owner should not need to open ChatGPT or type a problem classification after flagging. This increment implements **local capture and owner-only event relay**, NOT a validated automatic medical diagnosis, autonomous revision or Anki update.

## Scope and semantics

- Anki's documented search `flag:1` selects **red-flagged cards**, unlike note-wide tags. Sibling cards are not implicitly flagged.
- `Again/Hard/Good/Easy` = memory/review evidence. **Red flag** = owner request for card-quality review. Neither individually proves a mistaken clinical fact or learner misconception.
- Trigger **one durable event per observed red-flag interval** (key `anki-red-flag:{card_id}:{cycle}`), independent of whether that card was just reviewed. Existing pre-feature flags enter as undated first observations; timestamps are **first detected by Mac** and not the time owner tapped the flag.
- A repeated scan does not duplicate an event. Observed absence does not mean a defect was resolved. A later re-flag creates the next cycle. Toggling away and back between scans is unobservable.
- Bounded AnkiConnect `findCards` + `cardsInfo` read-only calls; flag status and card/note linkage checked before any private row submission. No question/answer text or deck name is stored or sent.
- Use **existing** configured owner-private spreadsheet and OAuth grant. Program creates a separate `Card_Feedback` tab if missing, then verifies its exact 10-column header. Never publishes personal card identity or review behavior to GitHub/CI, never broadens sheet access, and never creates another cloud store.
- Append-only immutable observation metadata, with editable diagnostic fields. The Mac upload never overwrites a diagnosis/review status. Remote row counts and immutable keys are read back before saving a private local checkpoint. Duplicate or truncated remote records fail closed.
- Existing Mac `ale_anki_unattended_run.sh` now attempts quality feedback after review-sync and concept-candidate steps. It runs only when the **pre-existing** Mac LaunchAgent runs and local Anki Desktop/AnkiConnect is available. This does not wake a sleeping Mac, force iPhone/AnkiWeb/Mac sync, or create a ChatGPT automation.

Private tab exact columns: `event_key | first_detected_utc | anki_card_id | anki_note_id | owner_signal | cause_code | review_state | concept_family_id | diagnosis_confidence | provenance`.

Initial diagnostic fields must be `UNKNOWN / PENDING_DIAGNOSIS / UNMAPPED / NOT_ASSESSED`. **Do not infer** a quality issue subtype, Concept Family or medical correctness merely from the flag.

## Next autonomous agent handoff (NOT YET VALIDATED)

A compatible **existing** owner-private scheduled teaching/QA task must actually have authorized access to `Card_Feedback`. On genuinely new `PENDING_DIAGNOSIS` items:
1. Read only necessary owner-private card content and Concept Family evidence, within granted access. No invisible Mac Anki access from a cloud task.
2. Diagnose `single-card defect / ambiguous answer / duplicate / unsafe clinical claim / underlying graph defect / insufficient evidence`. Apply recursive three questions and source-backed Q3 counterexamples **where they are decision-relevant**, not on every trivial typo.
3. Generate a reversible **candidate** revised card; source-check medicine separately and compare old/new ability to test exactly one inference, scope and counterexample.
4. Notify owner in existing trusted private channel with plain-language outcome. Leave unresolved cases visibly pending. Never silently alter owner Anki cards, clear flags, change FSRS or publish medicine.
5. When **several independent confirmed** defects share a causal mechanism in one Concept Family, escalate to an upstream graph/retrieval/generation-rule audit. Count repeated events from one card only once for upstream clustering.

Crucial: the Mac event bridge alone is **not** evidence that a scheduled AI can access the private tab, diagnose a defect or commit a correction. Keep `AUTONOMOUS_CARD_REPAIR_NOT_VALIDATED` until full end-to-end live evidence exists.

## Tests and handoff

Public synthetic tests: `python -m unittest discover -s tests -p 'test_ale_anki_flag_feedback.py' -v`. They cover the read-only `flag:1` query, card-level mapping, race/identity failures, idempotency, no assumed QA resolution, reflag cycle, private-tab bootstrap, schema errors, source identity/readback and no duplicate remote insertion. They do **not** use private Anki or OAuth.

First live test (owner-Mac; only after local checkout receives this code): after ordinary Anki sync, flag one **known non-sensitive** test card and let the existing LaunchAgent run. Verify in the **owner-only** Sheet that `Card_Feedback` contains exactly one `PENDING_DIAGNOSIS` row; rerun and confirm zero new rows, unflag and later reflag to validate the next cycle; ensure card text and FSRS unchanged. Never paste actual identifiers or sheet URL into GitHub.

Second live test (cloud): a scheduled instance that truly has authenticated private Sheet access must read the new row, perform a source-backed diagnosis, draft one safe reversible correction, and report to the owner **without an additional owner chat prompt**. Measure actual trigger→diagnosis→proposal latency, owner interventions, clinically substantive false positives and source-fidelity. If this cannot be demonstrated, status stays partial and repair autonomy is **NOT** claimed.

Link existing #258/#259/#254. No new schedule, paid API, public site deployment, automatic release, new database, or mutation of #137 history.

## Owner correction: ZERO wasted repetitions; agent owns red flags and quarantine

**The original red-flag-only design was insufficient.** A red flag does not stop a bad card from being served. The intended loop is **agent-led quality screening -> automatic red quality flag when diagnosis is qualified -> immediate reversible card-level suspension -> source-backed repair -> qualified resumption**. Manual flagging is an optional override, NOT the main burden on the learner.

AnkiMobile cannot run the Mac AnkiConnect bridge inside the iOS app or receive a new custom "AI red flag" pop-up from this Python file. For an *immediate* fallback on the iPhone, configure a swipe or tap zone in AnkiMobile Preferences -> Review -> Swipes/Taps to **Suspend Card** (one gesture; leaves card out of subsequent reviews), or use **Mark & Suspend** (marks the note and suspends the card, but does not set a per-card red flag). This is the only verified immediate behavior without an iOS add-on or online background inference. If no such gesture is configured, the built-in card menu's Suspend Card works. On next ordinary iPhone/AnkiWeb/Mac sync, the Mac can observe existing flags but cannot magically infer the gesture from a review event.

New scoped Mac implementation on existing #259 Draft:
- `tools/ale_anki_quality_quarantine.py` is a **reversible quality hold**, not an LLM classifier. First run baselines previously flagged cards (so other historic uses of red flags are not mass-suspended). Subsequent newly observed red flags are automatically **suspended at the exact card level** after existing owner-only quality-event capture. The script never suspends unrelated sibling cards.
- A private decision file may additionally nominate a card for automatic **red flag + suspend**, but ONLY with a distinct, independently reviewed `QUALITY_QUARANTINE` decision, exact card/note ID and SHA-256 of the privately inspected question/answer, explicit defect reason and evidence reference. Stale/missing/colliding decisions are rejected. The labels and references in this file are *claims*, not cryptographic proof of an independent clinical reviewer; live acceptance requires checking their provenance outside this deterministic gate.
- The Mac uploader calls this bounded routine with `--apply` **only on a checkout where the owner opted into the existing LaunchAgent and imported the Draft code**. Public CI runs entirely synthetic. Neither the repository nor interactive ChatGPT can reach the user's sleeping Mac or actively stop an on-screen AnkiMobile review.
- **No automatic reactivation**: a medically correct and pedagogically acceptable revised card needs independently verifiable QA and targeted re-enable policy; until then, suspension is deliberately persistent. The QA event remains open until verified, never closed merely because the flag was cleared or the card got suspended.
- Never alter `Due`, `interval`, `FSRS`, review counts, note fields, content, or any non-red pre-existing flag.

Next actual semantic deliverable: connect an authorized private content reviewer to the existing ALE decision channel, propose **one** independently reviewed defect against an actual owned card, check 1-card stale-content protection, then verify agent-initiated `setFlag` and `suspend` on owner Mac with no owner intervention in between. Count avoided repeated displays and falsely quarantined valid cards, with observed denominators. Until then the correct status is `SCOPED_QUARANTINE_CODE / AI_AUTOMATIC_DETECTION_NOT_VALIDATED / MAC_NOT_DEPLOYED`.
