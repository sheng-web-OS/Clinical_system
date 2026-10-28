# Clinical Discussion Depth｜Unhinted review calibration (pre-registered design, not a result)

**Owner**: Existing #203 / PR #205; cross-project failure ledger #133 and growth/attention KPI #137. Reuse `experiments/README.md` and PR #155 autonomy evaluation where applicable; **do not create a second runner, dashboard, scheduler or duplicate shared evaluator**.

**Research question:** Is the dominant constraint truly a *missing review perspective*, rather than missing clinical knowledge? Can a fresh reviewer **unprompted** identify the central clinical deficiency in the original 2026-09 BA aneurysm CBD, *while preserving accurately bounded content*? Does the full Clinical Discussion SOP add incremental discovery or only extra prompt/maintenance cost?

## 1. Separate three claims

1. **Writer ability after cue**: Given the defect, can AI repair? The prior author-side RED and revised EVD sample demonstrate an attempt, **not** reliable autonomy.
2. **Unhinted detection ability**: Without being told what is wrong, can a reviewer identify the serious issue, prioritize it above cosmetic errors, quote location and explain the decision consequence? **UNTESTED**.
3. **Real-world prevention**: Does that review reliably block poor reports before the user notices, without overrejecting good work or increasing owner minutes? Requires repeated previously unseen source cases. **UNTESTED**.

A reviewer that always says `HOLD` has perfect sensitivity on a defect-only suite but unacceptable precision. A reviewer that copies an earlier RED list has not demonstrated independent detection.

## 2. Controlled comparison (one small pilot, existing evaluation governance)

Same frozen transcript, available sources, effort/model/tools and pre-set output budget; separate fresh reviewer contexts, no author critique, prior defect locations, issue #203 text, prompt answer key, or other arm's output:

| Arm | Role instruction | Hypothesis |
| --- | --- | --- |
| A — native review | Neutral task: evaluate a neurosurgery clerkship Discussion for clinical rigor | Modern GPT may already find major gaps |
| B — perspective switch | Same + short instruction: act as a skeptical neurosurgery attending who may reject a technically correct overview, interrogate competing options and clinical evidence | The *change of lens* may provide most of the gain at very low cost |
| C — SOP | Same + minimal existing Q/D/E/R Discussion SOP, **not** the author-side RED answer/fixtures | Full contract may or may not improve on B |

The reviewer-visible **neutral baseline packet** is [`audit/clinical-discussion-neutral-reviewer-packet.md`](clinical-discussion-neutral-reviewer-packet.md). Coordinator or evaluator stores arm labels and expected outcomes **privately and separately**. The author must not see new challenge questions before answering.

This original historical case is already discussed extensively by the initiating writer; all **same-context analyses are contaminated** for independent-effect claims. A distinct review context must record its own prior exposure. Different turns or merely renaming roles does **not** establish isolation. If context separation cannot be shown, use `NOT_INDEPENDENT` rather than fabricate a review.

## 3. Matched protected controls (avoid false-positive factory)

For the historical manuscript, score **claims** in addition to overall depth. Use exact positions from the frozen transcript and verify with cited original source; do not advertise the list to the reviewer:

| Source | Bounded content worth preserving | Expected reviewer behavior |
| --- | --- | --- |
| Slide 2 | Posterior circulation coiling preference is conditional on *amenable to coiling*, and urgent clot evacuation is a separate decision | Preserve qualifiers; may criticize that comparative outcome evidence is missing |
| Slide 5–6 | Coiling and EVD have different treatment targets; EVD-before-vs-after securing has no universal sequence | Do not treat these caveats as errors; probe what evidence distinguishes actual timing |
| Slide 8 | Angiographic vasospasm is not identical to clinical DCI | Preserve distinction; may ask for other mechanisms and patient-relevant evidence |
| Slide 9 | Follow-up imaging is recommended; specified years are an expert consensus rather than a universal AHA mandatory interval | Preserve guideline-versus-consensus boundary |

**These are positive *claim-preservation controls*, NOT a proven high-quality positive *whole report*.** This original talk can have valid qualifiers and still fail depth. A later blinded multi-case evaluation must include truly adequate Discussion manuscripts in the same specialty/task class (pre-adjudicated independently), or calibration cannot claim a low whole-report false-positive rate.

A reviewer who invents a missing item already explicitly present in surrounding text is scored as a **false positive**; check adjacent paragraphs, qualification and temporal context before flagging. A reviewer who says nothing is wrong with an actual depth failure is a **false negative**. Neither should be relabeled after seeing the model output.

## 4. Evaluation rules and stopping

Before any independent run, freeze:
- Source transcript blob `afe6acddeb9d8ca5d677724635b7431100d07a68`; neutral review packet; comparison arms and prompt hashes; model/effort/tool budgets; selected material and adjudication key kept hidden.
- A predefined **critical defect**: a clinically consequential argument has competing paths but never distinguishes them with evidence, mechanism, a change-of-decision condition, or applicability to available patient facts; overview or decorative cites alone are not enough.
- A predefined **critical valid control**: an appropriately limited/qualified claim from the table above, allowing the reviewer to preserve it while identifying surrounding missing depth.
- Report **clinical error or unjustified patient attribution separately from depth**; don't award compensating aggregate scores.
- Do not let writer / candidate alter a rubric or pass threshold after seeing verdicts.

One trial may be used to debug packet integrity, **not** to claim validity. Repeat with new, unseen real clinical discussions (including adequate and inadequate manuscripts) to estimate unhinted detection, false positives, correct issue prioritization and transfer; avoid a synthetic suite where the defect is pre-cued. This is the same experiment philosophy already in PR #155; do not copy its entire SOP text as an extra production prompt unless measured benefit survives cost comparison.

**Minimum measured fields**: candidate identity/exposure, manuscript hash, first-pass top-ranked clinical contradiction, explicit source quotes, P0/P1 defect findings, true-positive / false-positive adjudication, untouched justified statements, reviewer questions, corrections/new harms, runs/retries, actual time/token where available, and **human intervention minutes**. Unknowns are `NOT_MEASURED`. Distinguish `SOP_DRAFTED`, `BLIND_REVIEW_RUN`, `MULTICASE_VALIDATED`, and `INDEPENDENT_MEDICAL_APPROVAL`; no status substitution.

## 5. Feasible immediate result and current limitations

- Existing **author-side** historical analysis is a non-blind feasibility aid only.
- Reviewer packet prepared; **no isolated model review has been executed in this workstream**.
- No pre-adjudicated whole-report positive control is currently present for a comparable neurosurgical CBD; claim-preservation controls exist, but overall specificity is **NOT_MEASURED**.
- Clinical facts absent from the original case cannot be hallucinated to make Back-to-patient PASS.
- An independently verified `HOLD` on original + accurate preservation of bounded claims + no extra severe false positives would be *promising*, not proof of stable prevention. Publication remains separate and blocked by existing gates.

**DoD**: Outcome must be traceable to fixed source, independent reviewer transcript and evaluator judgments; show actual improvement at comparable cost and unchanged medical safety. If B performs like C, prefer the cheaper perspective-switch instruction; if neither independently detects risk, do not broaden SOP or claim success.
