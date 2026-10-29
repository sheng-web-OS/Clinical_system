---
name: decision-question-triage
description: Use when choosing the central reasoning question for a case-based medical discussion, CBD, case report, or decision-focused exam lesson; first determine whether the apparent question would actually change a conclusion or action. Do not use for pure definition/reference work, engineering incidents, or to invent controversy where none exists.
---

# Decision-question triage — unvalidated skill candidate

**Status:** experimental candidate. A historical correction inspired this skill, but transfer to new cases is NOT VERIFIED. Read `AGENTS.md` and the relevant clinical/evidence contracts first. Do not replace those safety gates.

## When to use

Use *before* drafting the argument when a real case-based teaching task requires selecting the most consequential and defensible clinical question. The goal is not to force a debate; an ordinary, well-supported management choice may be straightforward. If the case provides insufficient data to justify deeper causal inference, narrow the conclusion.

0. **Retrieve only what the reasoning gap needs:** inspect the case task and current sources first; then selectively recover relevant, versioned full-length Clinical_system articles or prior accepted causal arguments. Keep original author statements and AI-added bridges separate; identify the exact concept or limitation that helps here. If the apparent match is only a shared keyword or the previous article addresses a different clinical population/decision, do **not** transfer its conclusions. Do not turn a prior article into an answer key.
1. Reconstruct the **actual decision point** and exactly what the clinician could know **at that time**. Separate documented observations, documented reasons, later interpretations, and genuinely missing facts.
2. Produce a **small set of candidate questions** from the case, not a tour of guidelines or available procedures. For each ask: What real alternatives/mechanisms compete? Would different answers change diagnosis, risk, timing, or management? Which *available or obtainable* evidence could discriminate?
3. Reject **fake questions**: obvious standard-of-care choices with no realistic rival; questions whose answer is absent from the case or source; questions generated only because a topic sounds sophisticated. A descriptive foundation may still be needed, but is not a contested decision.
4. Choose **one** question with meaningful consequence and resolvable uncertainty. Explain essential mechanism, strongest alternative, discriminating case evidence, evidence-quality limits, conditional decision pivot, and *back to the patient*. If no such question exists, explicitly choose a well-scoped explanatory overview instead.
5. Before delivery, **switch perspective**: independently ask whether this was the right question, which premise would falsify the argument, and whether the case supports the conclusion. A writer's own pass is not an independent review or a clinical approval.

## Negative triggers and boundaries

- Pure physiology/terminology primer: teach the mechanism and concept boundaries without artificially inventing clinical equipoise.
- Strongly supported straightforward action: explain why, but do not manufacture a 50/50 controversy.
- Missing clinical source: state unknown; do not retrofit later results or another patient's details into a case.
- Mechanistic plausibility is not comparative effect evidence; a guideline recommendation is not evidence of the original clinical team's private motive.
- Keep patient/private reviewer information outside public GitHub; do not auto-merge, auto-publish, or call self-grading independent proof.

## Transfer test

Only claim improvement if a **first-pass**, unhinted, independently evaluated, *unseen and different-domain* task with a normal/non-applicable control improves over native AI plus relevant article retrieval at comparable cost and safety. Pilot examples and these instructions are exposed; they cannot themselves count as held-out evidence.

See `experiments/skill-transfer/README.md` and existing #133 (failures), #137 (growth), #159 (autonomy), #205 (discussion review).