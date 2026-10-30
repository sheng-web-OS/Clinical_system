# A02-01｜Clinical OS growth-evaluation leakage boundary (isolated research)

**Status:** OWNER_DIRECTED_RESEARCH / DEVELOPMENT / NOT IN ORIGINAL 72h COHORT / HOLD.
**Inputs reviewed:** public GitHub `#137` (2026-10-27 five-axis ratings), `#225` (development-only three-arm comparator); separately received `clinical_os_handoff.zip` (rights: no public redistribution of source package, synthetic methods only).
**Scope:** inspect **whether evaluation evidence could misleadingly certify gains**; do not re-grade a real model, rewrite the original benchmark, restart paused events, or assert clinical correctness. This is new original research code; no external source archive is included.

## Preliminary findings: no numerical promotion or demotion

The existing `#225` evaluator binds suite/pack/Skill digests, checks all arm-case pairs, reviewer/worker context separation, first-pass flags and development-only qualification. These are useful safeguards. However, its public suite data has `case.id`, `role`, `source_sha256`, but no independently verified `canonical_family_id`, three-way train/development/holdout partition contract, `decision_at`, `evidence_available_at`, `evidence_observed_at` and training-label maturity at fit. This is a **research/evidence-contract gap, not proof a real contaminated trial occurred**. Existing visible fixtures do not demonstrate unseen-case generalization and cannot upgrade a score.

The six baseline growth dimensions currently have the following audit standing (the original numbers remain unchanged):

| #137 dimension | 2026-10-27 baseline | What is evidenced | What would justify upgrading |
| --- | --- | --- | --- |
| Long-term retention/versioning | 3/5 (provisional) | Document/version assets and provenance exist | Independent correctness, canonical/rights continuity and cross-run recovery |
| Teaching/output | 2/5 (provisional) | Production and draft outputs plus failures/QA contracts | Frozen first-pass quality with independent P0/P1, real reader/render checks and denominator |
| Knowledge integration | 2/5 (provisional) | Related-exam links and taxonomy fixes | Correct bidirectional links and unseen-case reasoning gain |
| Self-quality monitoring | 1/5 (provisional) | Failure ledger and isolated reviewer contracts | Unprompted defect discovery/repair, lower recurrence, independent same-SHA QA |
| Unattended autonomous delivery | 1/5 (provisional) | Partial schedules/engineering, unresolved real wake/repair evidence | Actual unnudged Run A -> Run B -> independent QA at exact HEAD, measured attention |
| External reader outcomes | N/A | Analytics mixed with testing, no clean controlled reader result | Preregistered isolated reader cohort and delayed transfer outcomes |

A `1/5` remains a baseline judgment based on available evidence, **not** an observed 0% autonomy success rate. `3/5` version retention is not a medical knowledge accuracy score. Do not average these numbers or claim unmeasured change.

## Synthetic counterexample protocol

Run `python -m unittest -v test_growth_leakage.py`; the 16 tests include one legitimate three-way cohort, invalid clock order, future/late source, observed-before-availability, train label maturity leak, train↔holdout and development↔holdout family overlaps, invalid/duplicate IDs, empty holdout, timezone errors and a clock-offset positive control.

The new `audit_growth_leakage.audit()` accepts an intentionally **small schema** and returns `REJECT` or `STRUCTURALLY_ELIGIBLE_NOT_VALIDATED`; it **never** authenticates a submitted family mapping, genuine platform activity, hidden outcome or medical skill. It always sets `growth_score_change_authorized=false`. This is an independent prototype: do **not** integrate it into `#225`, existing scorer, original `#137` window, scheduling or public website before separate review and fresh holdout design.

A later genuinely blind expert should retain an *independent* canonical case-family map to catch paraphrases and shared cases across admissions/hospitals; visible ids and timestamps alone can be forged. Pretraining contamination, reviewer bias, access-control leaks and multiple-comparison selection also remain outside this code. Without this separation, passing the 16 tests is **not** evidence of real anti-leak effectiveness.

## Decision and next gates

1. Freeze intended Clinical OS evaluation unit: case, family, source snapshot, model/Skill revision, test-window clock, reviewer decision and outcome maturity. Determine legitimate historical test cases and a reviewer-owned hidden paraphrase/overlap ledger.
2. Replay **only synthetic** known-invalid and legitimate cases against the current evaluation contract. Record true positives, false rejects and unhandled categories with denominators. The current `#225` source lacks a three-way group/temporal split verifier; do not mislabel unimplemented checks as existing confirmed test failures.
3. Independent reviewer verifies schema semantics and challenge sets; do not expose hidden answer keys to candidate workers.
4. Compare against existing native evaluation without changing fixed thresholds after seeing results. Stop if it adds no net detectable violations or raises false rejection/maintenance cost beyond preregistered limits.
5. Only after the originally registered 72-hour experiment closes, consider a separate optional integration into a new frozen cohort, with owner authorization and distinct reviewer. No automatic skill promotion, merges or publication.

**Success evidence presently:** 16 local synthetic tests pass. **Not established:** independently hidden-case audit, genuine model transfer improvement, reduction in actual false certifications, independent QA, platform runtime or human attention minutes.