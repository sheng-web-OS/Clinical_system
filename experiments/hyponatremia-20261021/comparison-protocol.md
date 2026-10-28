# Clinical OS v5.1 — Retest Protocol (Pre-registration Draft)
Date: 2026-10-21
Purpose: determine whether the deployed editorial contract adds measurable value beyond current-model native reasoning, not whether the editor can write a good essay.

## Conditions
A. **Native agent**: topic, same Pocket Medicine 9e pages, same primary research/guidelines, neutral request: "Produce your best medically precise clinical teaching article"; do not provide quality contract or prior completed author text.
B. **Clinical OS**: same inputs + current EPQC and evidence/figure contract, no prior author examples; the agent must independently choose a concept, build causal transitions and self-revise.
C. **Optional ablation**: Native agent + evidence lookup alone, no EPQC, separating "more source reading" from "better editorial judgment."

## Noncontamination
- Independent conversation and isolated tool/context environments, same model and capability configuration where feasible.
- No prior articles or topic-specific examples to either arm.
- Reviewer unaware of arm, title styling unified. A no-system control must receive identical tool access / source packet.
- State the exposure limitation if the EPQC inherently includes HCM examples or conversation memory cannot be removed.
- Select 3 unseen topics of divergent nature: one pathophysiology-focused, one medication/safety-focused and one decision-threshold focused.

## Precommit metrics
- P0/P1 safety mistake => automatic hold.
- Source-verifiable critical claims, original Figure/Table and footnote accuracy, and corrected errors.
- EPQC seven axes, each >=3 and average >=3.3 for provisional editorial pass; not independent adjudication.
- Novel counterfactual clinical scenarios answered correctly with reasons (blinded answer key).
- Time to reach understanding/clinical transfer, and subjective cognitive burden in actual readers.
- Human intervention count, duration, and tool/system maintenance costs (model runtime accounted for).
- Meaningful failure detection without prompting, and revision fidelity.

## Current trial
This hyponatremia article is B-like *demonstration*, not independent A/B evidence. The prior PE article differs in topic and context and must not be interpreted as matched control. NO publish decision.
