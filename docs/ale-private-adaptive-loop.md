# ALE private adaptive loop (owner-directed implementation pilot)

The target is **new, verified learner gain per minute**, not more agent reports.
This is an additive, reversible Draft stack on the hardened owner-private
Anki bridge (#259 -> #261 -> #262). No public Anki or learner records are
included or needed to run the offline tests.

## What this branch actually implements

- The existing macOS 30-minute LaunchAgent runs the verified read-only
  AnkiConnect -> private Sheets sync. **After** successful sync, it calls the
  owner-local candidate discovery script; no additional schedule or paid API.
- It honors every previously skipped card across concept-catalog revisions,
  without modifying the original owner-private skip file. A prior skip is never
  silently undone by a renamed/reordered concept catalog.
- For a **new, not-skipped, not-already-mapped** review only, exact local Anki
  card/note identity and exactly one structured `ale::concept::<concept_id>`
  tag that appears in the private `Concepts` catalog yield an **UNCONFIRMED**
  mapping candidate. It appends only minimal identifiers/provenance to the
  existing private `Card_Concept_Map` tab and re-reads the row. It does not
  read or upload card question/answer text; it does not create/update Anki tags.
- Missing notes, ambiguous tags, common-language tags, skipped cards and
  rating-only signals **abstain**. Proposals are never owner-confirmed mappings,
  causes of confusion, mastery, transfer, learning gain or permission for
  card deletion / FSRS mutation.
- The pure `choose_next_lesson` policy consults the private **existing**
  `Next_Actions` queue and `Concepts` evidence (not a public user profile).
  Incomplete exam-source verification results in
  `VERIFY_SOURCE_BEFORE_COLD_ATTEMPT`, not an invented official question or
  an assumed incorrect answer. It never claims a lesson was completed.
  The existing 09:00 Writer is the cloud lesson orchestrator and must actually
  read private Sheets during its scheduled run before claiming any adjustment.

## What is deliberately NOT yet proven

The locally-installed Mac checkout will continue running its old checked-out
script until a safe, normal local code update. Committing this GitHub PR does
**not** remotely modify the owner's Mac, Google credentials or LaunchAgent.
No actual owner-private review data has been committed or analyzed by
public CI. No claimed new concept mapping or learner gain is made here.
No automatic background 30-minute wake nor scheduled cloud private
read has been independently demonstrated as fully unattended. A successful
GitHub test is not an owner-Mac, cloud-learning, or learner-gain acceptance.

## Acceptance sequence

1. Offline tests: old uploader readback, persistent owner skip, missing/ambiguous
   tags, single exact-tag provisional candidate, duplicate suppression,
   source-verification-gated next lesson, no observed learner gain.
2. Owner-Mac when code becomes locally available: existing skip remains skipped;
   no changes to Anki/FSRS; background run produces no spurious mappings.
   On a genuinely new unskipped event with an existing exact tag, append one
   unconfirmed candidate once with private full-row readback.
3. Scheduled cloud Writer **independently** reads owner-private Sheets and
   shows a real before/after change to `Next_Actions` only if new reliable
   evidence warrants it; otherwise abstains and maintains daily complete
   article requirement.
4. Later, learner-unseen cold/delayed item with independently checked sources
   measures improvement per study minute. Until then report `NOT_MEASURED`.

No public CI job may request OAuth tokens, sheet IDs or review records. Do not
merge or publish without the original independent and medical/rights gates.
Frozen 72-hour experiment #137 is unchanged and this is owner-directed,
out-of-cohort engineering, not an autonomous success numerator.
