# A02-03｜Independent challenge preregistration — NOT EXECUTED

**Owner-directed research / PR #249 / Draft-HOLD / no change to original #137 72h cohort.**
Registered on 2026-10-30, before any new independent challenge packet is received or scored. This document is public **method and acceptance only**. It contains no hidden prompts, case/source records, answers, peer ZIP, private keys, or restricted data.

## 1. Fixed target and falsifiable question

**Hypothesis:** a point-in-time + family-partition structural guard adds correctly rejected data-integrity violations beyond the existing three-arm comparator, without incorrectly rejecting legitimate shared-source or sealed-retrospective evaluations.

Immutable code artifact identities (blobs; Git SHA-1 of exact file bytes):
- Baseline PR #225 `tools/compare_skill_transfer.py`: `65645acf9d8df981c1ea6d359588c7075cb479aa`.
- A02 PR #249 `audit_growth_leakage.py`: `3e1ead7bbe7a4e0b3efa7313e7fbaecb107483e4`.
- A02-02 replay script: `c16ac43797a73423be225d411ed32f96dc0b7c4f` (development-only reference; **not** an independent challenge).
- Candidate previously exercised at exact commit `62a34dee17a37428c623544106d683b7ef8fb4f9`; [CI run 41072609320](https://github.com/sheng-web-OS/Clinical_system/actions/runs/41072609320) completed SUCCESS. Subsequent documentation commits do not alter these code blobs. Freeze **these code blobs**, not a moving branch pointer. Any candidate behavior change starts a new pre-registered cohort; do not patch the old score retroactively.

**No promotion** of #225 skills, #249 A02, #137 growth scores, or autonomous completion from this study.

## 2. Author/reviewer isolation and case provenance

- Challenger must operate in a genuinely **different execution/review context from the A02 author**, and prepare the case packet without reading any author-created development examples as seed material. Knowing this publicly frozen protocol is acceptable; viewing the old 12 authored cases is exposure and must be declared.
- Challenger alone maintains source-to-family provenance, identity aliases, case history, verified evidence availability/observation times and truth labels. Prefer independently auditable, rights-cleared, non-patient or properly authorized source histories. Do not invent provenance just to fill required fields.
- **Before candidate evaluation**, challenger freezes case count, byte-identical input packet, label map, immutable source references and eligibility rules in a **separately access-controlled location**, records trustworthy timestamp/independent custodian and case-set commitment. A self-reported timestamp or a publicly visible hash by itself does not prove non-exposure. Avoid publicizing small enumerable holdout fingerprints, which can leak content by guessing.
- Runner must not see labels, aliases, rationale, reviewer notes, source metadata withheld by the original policy, historical candidate outputs, or the challenger packet before its permitted evaluation call. Reviewer assesses first-pass results only; same model context or same GitHub account is **not** sufficient independence evidence.
- Preserve challenge creation and review event provenance without claiming a model has never seen the subject during pretraining; impossible to establish from this interface alone.
- Public GitHub receives only non-sensitive protocol, code-blob binding, anonymized aggregated counts, reviewer independence status, and HOLD reasons. No hidden material or clinical identifiable data in PR comments, Actions artifacts or public branches.

## 3. Fixed challenge axes and judgments

Challenger constructs an **unseen, separately authored** pilot of **18 independently supported cases** (six per axis). Each axis should include at least two confirmed violations, two demonstrably legitimate controls, and two cases with insufficient or conflicted provenance. Balance is a **prospective design**, not a report of observed cases; if adequate reliable evidence cannot be found, register fewer with `INSUFFICIENT_CHALLENGES` and do not claim this preregistered pilot passed. Do not substitute the publicly known A02-02 examples.

**Axis F: family lineage** — actually shared underlying case/source lineage despite distinct reporter IDs vs genuinely independent cases drawing on a shared journal, guideline or common text vs provenance insufficient to decide. Text similarity alone is not a gold label.

**Axis R: retrospective eligibility** — independently sealed retrospective sampling with fixed inclusion criteria vs outcome-informed post-hoc selection vs self-declared sealing with no verifiable custody/access evidence. Historical mature outcomes are **not** themselves proof of leakage.

**Axis T: evidence clocks** — independently sourced availability and access/observation history vs true future/late evidence vs user-edited/backfilled/ambiguous time claims. Source publication, historical decision, actual worker observation, and label maturity are distinct clocks.

Ground-truth action: `REJECT_CONFIRMED` (proven invalid), `RETAIN_LEGITIMATE` (supported valid), or `HOLD_UNVERIFIED` (insufficient trusted provenance). **Not all unverified cases are proven leaks.**

## 4. Blind comparison (do not change thresholds after seeing cases)

Evaluate each case using fixed original #225 rules and unchanged A02-01 rules; report mechanically expressible checks separately from proof requiring external lineage/provenance. A02 results `REJECT`, `INVALID_INPUT`, `STRUCTURALLY_ELIGIBLE_NOT_VALIDATED` are **structural**: the last value is never a blind or authenticity PASS. A01/A02 must not treat caller-supplied family IDs and timestamps as authenticated.

An independent adjudicator maps the observed first-pass outcomes to `DETECTED_INVALID`, `PRESERVED_VALID`, `HELD_UNVERIFIABLE`, `FALSE_REJECT`, `FALSE_CERTIFICATION`, or `NOT_COVERED_BY_RULE`, using source evidence not shown to the candidate. Keep `NOT_COVERED_BY_RULE` visible; do not count reviewer intervention as automated A02 detection.

For each axis, publish *separately*:
- confirmed-invalid denominator, automatically detected numerator, and critical misses;
- legitimate denominator and false rejections;
- unverifiable denominator and unsupported certification vs correctly withheld claims;
- missing/unsupported data and attempted/failed cases (no selective exclusions);
- distinct reviewer/author provenance and whether any challenger examples were previously exposed;
- time/tool/owner attention overhead where observed; otherwise `NOT_MEASURED`.

No global accuracy from mixed classes; no pretending that n=18 gives reliable generalization.

## 5. Precommitted decision and stops

- **First-pass shadow pilot only:** All six independently confirmed critical violations must be surfaced by the combined admissible workflow (with attribution to automated guard vs reviewer), all six legitimate controls must avoid false `REJECT`, and all six unsupported-provenance cases must avoid being **certified**. Any failure -> `HOLD_RESEARCH` with exact error classification, no silent rescore on rewritten held-out cases. If missing reliable reviewer/custodian, seal or denominators -> `INCONCLUSIVE`, not `PASS`.
- **Automation value specifically:** A02 cannot be promoted as an independent family/provenance authenticator if success depends on the reviewer resolving aliases or seal history; record those as *human/external assurance required*, and compare incremental guard-only detection.
- **Adoption gate:** even a perfect first blinded pilot remains `PILOT`. Adoption into a new Clinical OS evaluator cohort requires independent repeat on previously unseen material, documented false-exclusion risk, measured incremental owner/tool overhead, secure provenance, no medical/QA regression, and owner-approved integration after existing 72h study closeout. The original study window ends **2026-11-01T06:20:15Z**; do not touch its registry, tasks, prompts, denominator, scoring or scheduling.
- **Abort:** any withheld answer exposure, compromised reviewer independence, use of patient-identifying/confidential materials on public GitHub, reusing previous challenge cases, original code-blob drift or owner permission conflict -> `HOLD_COMPROMISED`. Retain the failure; restart only with separately registered new cases, never recycle contaminated holdout as unseen.

## 6. Current evidence/status

**Actual independent case packet:** NOT_RECEIVED.
**Independent challenger / adjudicator identity:** NOT_VERIFIED.
**External pre-run seal and access record:** NOT_VERIFIED.
**Unseen challenge outcomes and incremental real-world rate:** NOT_MEASURED.
**A02-03 outcome:** INCONCLUSIVE / PRE-REGISTERED ONLY.
**#249:** Draft/HOLD. No merger, release, new schedule, paid model call or tampering with the original 72-hour experiment.

A pre-registered protocol is not execution. The existing 18:30 QA slot may be a suitable **separate review context** only if its run identity is independently verifiable and its existing authorization covers this work; this file does **not** change or run the automation, and a posted PR comment does not prove a scheduled pickup.
