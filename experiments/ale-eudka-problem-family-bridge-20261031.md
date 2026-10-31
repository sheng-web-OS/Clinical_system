# ALE｜Problem-centered Concept Family + cross-family reasoning bridge: euDKA, CKD, MI

> **2026-10-31 Q3 correction / version 0.1.1** — This document captures the original source-backed v0 construction (its original numerical counts are historical), but the **current machine-readable graph now has 12 Concepts, 12 typed edges and 7 Q3 controls**. A second model-driven source challenge detected and repaired E3/E6/E7 wrong inference targets, added C_MI_CLASSIFICATION and E11/E12, and limited the MI biomarker rule with the type 3 fatal-presentation exception. See [the complete edge adjudication and source record](./ale-eudka-bridge-q3-semantic-audit-20261031.md) and [the revised JSON](./ale-eudka-problem-family-bridge-20261031.json). This is still NOT independent medical QA, learner improvement, or autonomous semantic discovery.\n\n
Date: 2026-10-31 (Asia/Taipei) | **SOURCE-LINKED CANDIDATE / MEDICAL QA PENDING / NO PROMOTION**

This is the first bounded **real-source-backed, typed Concept Family candidate graph** following the confirmed #258 owner rule: `Knowledge Context → smallest testable Concept → clinical problem-centered Family → higher-order bridge`. Higher-order concepts must **connect** clinical families, never erase their individual mechanisms. The machine-readable, candidate-only payload is [the paired JSON](./ale-eudka-problem-family-bridge-20261031.json). It is **not** a new canonical ontology or database. No personal owner answers, Anki identifiers, medical records, unpublished cases, paid API, site mutations or deployment.

## 1. What new knowledge decision is being tested?

Hypothesis: **Evidence sufficiency depends on the exact proposition under test.** A marker may be sufficient for a *narrower* conclusion (troponin >99th URL = myocardial injury; GFR <60 persisting ≥3 months = CKD criterion; beta-hydroxybutyrate documents ketonemia), while insufficient for a *broader* disease/etiologic classification that requires different evidence. This does **not** mean that "all tests are only proxies" or "no lab alone can diagnose anything."

- Source [S_DKA24] 2024 adult consensus distinguishes D/K/A diagnostic criteria, simultaneous mixed disorders, and endpoint evaluation.
- Source [S_MASK24] 2024 original Hillock case supports clinically important ketone-associated acid burden despite normal pH/HCO3 through concurrent vomiting-associated alkalosis. **The case report's clinical label of DKA is not a literal proof that its measured 2024 consensus A criterion was fulfilled.**
- Source [S_KDIGO24] KDIGO 2024 requires CKD chronicity ≥3 months. The specific exception is persistence of GFR <60, which **does** satisfy one CKD criterion.
- Source [S_MI18] Fourth Universal Definition: elevated troponin suffices for myocardial injury, rise/fall for acuity, while acute ischemic MI requires more.
- Source [S_IBCC25] IBCC expert bedside approach is explicitly a different heuristic, not replacement of the formal multisociety definition.

## 2. Three distinct clinical problem-centered Families

### Family A — CF_EUDKA_DECISION_V0
**Question:** With modest glucose, how do we separate current glycemia, ongoing ketogenesis, measured acidemia, mixed acid-base physiology, and the operational adult DKA gate?

**Evidence → causal chain → discriminating steps:**
1. SGLT2 glucose loss + reduced food intake or relative insulin deficiency permits modest glucose to coexist with ketogenesis. **Low glucose cannot veto direct ketone testing** when the clinical context warrants it (C_EUDKA_GLUCOSE_AXIS).
2. **Formal classification:** D (diabetes history or glucose ≥200 mg/dL), K (beta-OHB ≥3 mmol/L or urine ketones ≥2+), A (pH <7.3 and/or HCO3 <18 mmol/L). A high beta-OHB alone does not automatically satisfy all three (C_DKA24_THREE_COMPONENTS).
3. **Competing-process evidence:** vomiting-associated metabolic alkalosis can offset a ketoacid process, leaving measured pH and HCO3 near normal (C_EUDKA_MASKED_PH). Anion gap and beta-OHB strengthen concern but AG is not etiologically unique (C_EUDKA_KETONE_NOT_ETIOLOGY).
4. **Do not fuse cases:** published Cai/Fu/Tan 2026 case in the existing website was frankly acidemic; Hillock 2024 case is separate, with pH 7.37, bicarbonate 26, AG 23, beta-OHB 7.1. Its narrative glucose 186 mg/dL and Table 1 glucose 283/266 lack a proven shared timepoint. Preserve discrepancy, **no invented time series**.

**Typed boundary:** `C_EUDKA_MASKED_PH --challenges_equivalence--> C_DKA24_THREE_COMPONENTS`. It does **not** say the formal A criterion is satisfied by a hidden acid burden; it says bedside pathophysiologic concern and operational membership must not be silently merged. Independent clinical reviewer must judge the terminology.

### Family B — CF_CKD_CHRONICITY_V0
**Question:** Is a low eGFR a transient kidney problem or chronic kidney disease?

- `C_CKD_SINGLE_EGFR --insufficient_without(chronicity)--> C_CKD_CHRONICITY_CRITERION`: one measurement cannot by itself prove duration; AKI or AKD remain possible.
- `C_CKD_PERSISTENCE_SUFFICIENT --satisfies_criterion--> C_CKD_CHRONICITY_CRITERION`: GFR <60 mL/min/1.73m² sustained ≥3 months is a CKD criterion. **Neither albuminuria nor another lesion is mandatory in addition to that GFR criterion.** Whether a cause has been established is a separate question.
- KDIGO 2024 Table 1 was visually inspected on the official guideline PDF page S137. Historic evidence, imaging and other data can document chronicity; a single sample cannot be retrospectively assumed to represent months.

### Family C — CF_TROPONIN_MI_V0
**Question:** When troponin increases, what exactly is established, and what distinguishes injury from infarction?

- Troponin >99th percentile → myocardial injury (C_TROPONIN_INJURY).
- Rise/fall of troponin → acute injury pattern (C_TROPONIN_ACUITY).
- **Acute MI** requires acute injury *plus* evidence of acute myocardial ischemia; values alone do not assign infarction or ischemic etiology (C_MI_ISCHEMIC_EVIDENCE).
- No claim that troponin is meaningless; it is diagnostic **for a narrower proposition**.

## 3. Higher-order CF_EVIDENCE_SCOPE_BRIDGE_V0 (cross-family, not a parent disease)

The common **inference structure** is `measured finding → target-specific criterion → supported conclusion` with explicit missing-context checks. This is a *bridge among three different problem networks*, not a declaration that DKA, CKD, and MI share mechanisms or are one taxonomic disease. Edges E8/E9/E10 are `illustrates_shared_reasoning_pattern`, never `is_a`, `causes`, `part_of` or an automatic merge.

**Q3 adversarial guardrails** (see Q3_A–E in JSON):
- An elevated troponin **does** establish myocardial injury; a universal "markers never diagnose" abstraction is false.
- Sufficiently persistent reduced GFR **does** satisfy a CKD criterion; the *time dimension* changes sufficiency.
- A normal pH and HCO3 in Hillock's case do **not** fulfill the measured 2024 DKA A component, but neither safely exclude an important ketone-associated metabolic process.
- Elevated beta-OHB / AG are not unique proof of diabetic cause; starvation or other acid sources require consideration.
- The Hillock glucose narrative/table discrepancy is unresolved. Do not import a false euglycemic time course.

**Recursive Q1:** exactly which claim is being tested, and what is directly observed?
**Recursive Q2:** which criterion, mechanism or temporal bridge changes the inference for this family?
**Recursive Q3:** find the smallest verified counterexample where the same observation is sufficient for one claim but insufficient for the proposed broader claim. If the abstraction fails, narrow its scope while keeping the local families intact.

## 4. Practical evaluation: source audit → graph audit → teaching decision

**Source/medical gate:** Independent reviewer must check the official DKA diagnostic definition, mixed acid-base case, KDIGO chronicity exception, and myocardial injury versus MI boundary; review each E1–E10 directional edge rather than approving an entire family as one block. A reviewer must especially challenge the DKA wording when acidemia is masked, and whether a formal diagnosis can be equated with a physiologic process.

**Graph audit:** Ensure all 11 stable candidate concept IDs exist, three separate clinical families persist, higher-order bridge uses typed `illustrates_shared_reasoning_pattern` not `is_a`, every edge has at least one actual source locator and a conditional boundary, and five explicit Q3 controls remain. A tag-only baseline must not silently merge disease families. If the reviewer judges the bridge banal or false, revise/abandon it; do not optimize output volume.

**Learner endpoint (private, not executed):** Use a vetted owner-unseen source-derived discrimination requiring: (a) troponin-injury versus MI, (b) single low eGFR versus proven persistent low GFR, and (c) normal pH with substantial ketones/anion gap vs the literal DKA A criterion. Compare against a no-card / static-outline approach for genuinely unseen reasoning, delayed recall, study minutes, review burden and owner nudges. **No learner test or improvement is claimed.**

**Autonomy endpoint (not met):** The current graph was manually assembled by a model with external sources at owner request. The deterministic #260 clustering code cannot discover these medically correct nodes and edges from raw literature; a separate held-out text-to-concept and scope-evaluation experiment is required.

## 5. Provenance and scope
- S_DKA24: https://doi.org/10.2337/dci24-0032 (adult consensus, diagnostic Fig. 2A, mixed disorders).
- S_MASK24: https://doi.org/10.1093/omcr/omae071 (case presentation and conflicting glucose values Table 1).
- S_IBCC25: https://emcrit.org/ibcc/dka/ (expert heuristic, not consensus criteria).
- S_KDIGO24: https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf (definition/Table 1 p. S137 and chronicity).
- S_MI18: https://doi.org/10.1093/eurheartj/ehy462 (injury vs infarction definition).
- Existing real clinical teaching context: https://github.com/sheng-web-OS/Clinical_system/blob/main/content/xiaoma-internal-medicine/lessons/2026-10-29-eudka-real-case.md
- Prior G1 research: [the first euDKA source-gap pilot](./ale-gap-eudka-first-real-source-pilot-20261031.md).

**Verdict:** `REAL_SOURCE_GRAPH_ARTIFACT / PROPOSED_TYPED_EDGES / Q3_CHALLENGED / MEDICAL_INDEPENDENT_REVIEW_PENDING / NO_CANONICAL_PROMOTION / NO_LEARNER_OUTCOME`. Outside early-terminated frozen #137 cohort. No merge, medical publication, Anki/FSRS mutation or private data persistence.
