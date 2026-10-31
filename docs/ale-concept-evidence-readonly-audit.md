# ALE-01 | Confirmed card → concept evidence join (owner-local, read only)

This is a minimal executable follow-on to #259's local `ale_anki_concept_map.py`. It does not create a second learner-state system.

**Run after the owner has actually confirmed a specific reviewed card's concept in Anki Desktop:**

```bash
cd "$HOME/ClinicalOS-ALE-bridge"
git fetch origin
# Only use this command once this patch is merged/cherry-picked into your local bridge;
# do NOT reset the owner-local checkout or replace OAuth credentials.
"$HOME/Library/Application Support/ClinicalOS-ALE/venv/bin/python3" tools/ale_concept_evidence_audit.py
```

It reads only the owner's existing `Error_Events`, `Card_Concept_Map`, and `Concepts` tabs using the already-configured local OAuth bridge. Every output is an aggregate count; review IDs, note/card IDs, answers, private URLs and concept IDs never print.

**Exact trust semantics:** only `OWNER_CONFIRMED_SINGLE_CARD` mappings whose note/card identifiers and exact source-review anchor match, whose local attestation is present, and whose concept ID exists in the private Concepts taxonomy, contribute to `retrospective_concept_links` (**not** `mapped_recall_only`). Other draft records are NOT confirmed mappings. Duplicate/conflicting confirmed card mappings, event identities or unknown concepts fail closed. Multiple sibling cards of one note cannot inherit a mapping from another card. A filled `concept_family_id` in Error_Events is not assumed to equal an atomic `concept_id`.

Output is a **retrospective card-to-concept identity association**, not a contemporaneously verified recall of that specific content. It never establishes a clinical error diagnosis, learner-unseen pass or mastery. It does not write private decisions, modify Anki/FSRS, or delete any card. The current contract always reports `verified_historical_concept_recall=0`, `mapped_recall_only=0` and `HISTORICAL_CARD_VERSION_NOT_ATTESTED` for otherwise mapped events.

The current first owner-private revlog event may legitimately be `MAPPING_REQUIRED`; it cannot be forced to match one of the three draft candidate card rows. A genuine owner-local link and readback is the separate next validation, and the original #259 owner remains responsible for the local concept-map UI.

**Synthetic regression command:** `python -m unittest discover -s tests -p 'test_ale_concept_evidence_audit.py' -v`.

This file and its tests are public-safe, with no owner-specific identifiers or data. #137's 72-hour cohort remains unchanged.

## Why an exact historical card ID is not enough

Anki revlog does not provide the rendered question content at its historical review timestamp. The owner may confirm what a card **currently** tests, but the card could have been edited in between. The auditor therefore requires exact source-review anchoring, current note/card and concept identity, local owner-attestation fields and a valid chronological timestamp; it **does not** apply that mapping to unrelated earlier or later reviews. Even the anchored review is graded as a retrospective association, not historically version-proven understanding.

Before ever upgrading this evidence, a separate trustworthy content/version lineage would be needed; a model-provided claim or hash calculated only today is not evidence that the old question was identical. No new owner intervention, card mutation or private data exposure is required by this patch.


## Answer-key provenance audit (supplemental read-only Mac command)

Run `tools/ale_attempt_evidence_audit.py` against the existing private OAuth configuration. It inspects only the owner-private `Attempts` and `Concepts` sheets and prints **aggregate counts**. It never reads Anki card content, modifies answers, grades questions, accesses hidden exams, writes new rows or publishes raw answer/weakness data.

- One `Attempts` row represents an *attempt record*, not necessarily an independently graded question.
- `official_exam_identity_verified=YES` is just a **sheet declaration**; the present schema has no independently authenticated examiner/key receipt. Therefore `independently_verified_item_grades=0` deliberately remains the conservative ceiling, not a claim that an independently validated question is impossible.
- A group-level score cannot prove which individual question was incorrect. An assistant-generated answer key remains provisional; a correct post-remediation response does not become learner-unseen transfer.
- All concept mastery upgrades remain **zero** until source-specific evidence and a genuinely unseen/delayed assessment are linked independently. The auditor refuses duplicate attempt or concept IDs and malformed schema; Sheets' omitted trailing blank cells are permitted.
- The program does not log private concept names, question IDs, answer strings or underlying event IDs to GitHub. `tests/test_ale_attempt_evidence_audit.py` uses only synthetic fixtures.

Exact runnable command on a Mac with its existing authenticated virtualenv after safely incorporating this PR:

```bash
"$HOME/Library/Application Support/ClinicalOS-ALE/venv/bin/python3" tools/ale_attempt_evidence_audit.py
```

The **next substantive validation** is to obtain a source-verified *individual* unseen question response with a reviewable key and time/exposure provenance. A numerical increase in candidate cards or marked-correct rows without that evidence does not satisfy ALE learning success.
