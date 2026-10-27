# Agent autonomy and owner-attention SOP (private)

Status: **operational policy proposal** (2026-10-27, Asia/Taipei). This is for the private repository / agent entrypoint, **not public medical teaching text**. It makes the existing T0–T6 integration contract actionable without another database, orchestration service, daily form or schedule.

## North star and non-negotiable gates

**Optimize validated clinical/educational value per minute of owner attention.** A higher article count cannot compensate for unchanged or worse medical correctness, comprehension, severe escaped defects, or owner fatigue. Medical P0/P1, source fidelity, rights/privacy, independent reasoning-continuity review, figure usability, and publish authority are hard constraints, not weights in one composite score.

Canonical evaluation and human-development rubric: [issue #137](https://github.com/sheng-web-OS/Clinical_system/issues/137). Single failure/recurrence source: [issue #133](https://github.com/sheng-web-OS/Clinical_system/issues/133). Content-versioned independent editorial receipts: [editorial-semantic-release-gate.md](editorial-semantic-release-gate.md). Do not mirror the datasets in this document.

## Execution loop: discover → repair → verify → learn

1. **De-duplicate before writing.** Identify affected canonical source and current `main` SHA; inspect overlapping open PRs and the designated implementation owner. If another PR owns the same paragraph / visual / exam relation, use its review thread or owner handoff instead of opening a competing patch.
2. **Independently inspect scope.** Reproduce the observed defect, reconstruct the reader's missing concept → causal evidence → decision → narrative handoff, and sample sibling pages of the same failure class. Distinguish confirmed defects, suspected defects, and negative controls. Do not call keyword hits proof of a clinical error.
3. **Run reversible correction.** If within permitted low-risk scope, research, revise on the designated feature branch, run the smallest relevant unit/regression and full applicable site build/visual checks, then save evidence. The owner should not need to prompt each substep. If the original gate required the broken behavior, repair that gate with a negative regression rather than reinstating the reader defect.
4. **Review with separation.** The authoring pass may not certify its own clinical accuracy or narrative continuity. For newly changed teaching prose use the existing paragraph packet and reviewer context, independently check the four continuity break types and P0/P1 safety. Unavailable original figures, ambiguous case attribution or unverified primary evidence remain explicitly HOLD.
5. **Close the loop, not just the PR.** For escaped serious defects update #133 with affected SHA, original failure, root-cause confidence, failed escape gate, regression fixture, remediation, and CI vs production evidence. Do not mark production fixed until the exact deployed page has been inspected. In the next weekly review, actively test whether the same root cause recurred on new work.
6. **Report exceptions, not noise.** Escalate only genuinely unresolved owner decisions with a short decision question and recommended choice. No repeated unchanged hourly messages; no silent suppression of unresolved significant risks. Record the actual next check in the existing hourly or Friday monitoring task; this document alone does not schedule execution.

## Authority decision table

| Situation | Default action | What may be claimed |
| --- | --- | --- |
| Routine, reversible, authorized copy/layout/tooling defect | Agent inspects, fixes and tests on owning branch; requests no routine approval | Branch fix and specific checks only |
| Material medical P0/P1 ambiguity, original-source mismatch, figure rights or privacy risk | HOLD, independently investigate; request a **specific** owner/specialist choice when unresolved | Pending/verified facts; no medical PASS |
| Conflicting existing PR ownership or stale `main` | STOP overlapping edits; reconcile exact files and SHA with responsible owner | Coordination pending, not "resolved" |
| Merge, formal publication or outward-facing high-impact changes | Follow explicit existing authorization and all release gates; otherwise request permission | Only the reached source/CI/deploy/HTTP state |
| User report of repeated similar defects | Trace root cause, search siblings, add minimal negative regression, independently retest | "Prevented recurrence" only after later fresh-case observation |

## Evidence and measurement contract (weekly, same seven-day window)

The existing Friday report should read events from #133 and publication/review evidence from the repository instead of asking the owner to maintain another spreadsheet. For each metric include numerator, eligible denominator, the audited coverage, report window, and traceable PR/issue/SHA. If unknown, use `NOT_MEASURED` or `N/A`; do not silently substitute zero.

- **Owner attention**: actual minutes spent on corrections, decisions, explanations and chasing stalled work; separately count interruptions / repeat "continue" prompts. This is the **primary outcome**, subject to the quality guardrails. Where only a 3–5-task sample is available, report sample size and coverage, not a fabricated population mean.
- **Independent first-pass acceptance**: changed, eligible teaching units passing independent medical/pedagogical gate at V1 / all independently evaluated eligible V1 units. Preserve V1 before repair; don't relabel V2 as first pass.
- **Autonomous severe-defect interception**: independently detected eligible P0/P1 defects before public exposure / all verified eligible P0/P1 defects whose discovery source is known. Break down author-discovered vs agent-discovered; if discovery attribution or coverage is unknown, do not report a rate.
- **Same-root-cause recurrence**: new verified incidents linked to an earlier repaired root cause / eligible subsequent cases with documented screening for that cause. If no screening coverage exists, report incident counts only.
- **Quality guards**: escaped medical/teaching/visual/metadata P0/P1, source/figure rights, real mobile render, release authority, and actual independent reader transfer when measured. Never combine source, CI, production and reader understanding into one green tick.

**Weekly decision rule:** if apparent owner-time reduction comes with rising severe defects, decreased sampled teaching validity, or less audit coverage, the system has *not* matured. Prefer repairing the failing common gate and slowing content expansion. Only upgrade the #137 developmental stage after new cross-task evidence, not because this SOP was committed.

## Acceptance cases for future Agent runs

- **A — Metadata escape**: a reader reports `Draft/HOLD` in published prose. Correct owning article, check same-class pages, preserve essential medical limitations, make the existing reader-copy regression fail on the old bad state, and verify rendered site separately.
- **B — Abrupt clinical attribution**: a CABG lactate paragraph invokes epinephrine before actual measurements. Restore the case time course before possible mechanism, maintain association-vs-causation limits, obtain a distinct reviewer receipt, and check sibling transitions.
- **C — False technical pass**: CI green but iPhone figure has no readable clinical data. Keep visual gate `NOT_VERIFIED/HOLD` until 360/390px asset and semantics are checked; do not count as resolved or lower notification volume by hiding it.
- **D — Ambiguous harm**: new paragraph recommends a high-risk intervention without applicable population or evidence. HOLD, investigate source, request the narrow medical decision if still ambiguous; never turn it into a routine auto-merge.
- **E — Unmeasured savings**: tasks completed without owner-time logs. Report output/defect evidence while owner minutes stay `NOT_MEASURED`; neither "0 minutes" nor a higher maturity score is allowed.

Completion of this document and its PR is **policy adoption only**. Actual autonomy, medical correctness, attention savings, and lower recurrence require independently observed executions and comparable later samples.
