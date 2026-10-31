# ALE knowledge-context → Concept Family｜First source-backed pilot: euDKA and masked acid-base states

Date: 2026-10-31 (Asia/Taipei). Study classification: PUBLIC_SOURCED_RESEARCH_CANDIDATE. **Not medical QA, release, canonical concept promotion, learner experiment or autonomous LLM-agent run.** This is an author-assembled **first real-source audit** to test whether a useful gap can be found and researched beyond synthetic gap routing.

## Scope / baseline

- Main already published material: [40F euDKA real-case lesson](../../content/xiaoma-internal-medicine/lessons/2026-10-29-eudka-real-case.md). Do **not** rewrite its patient or medication data. It already covers DKA D/K/A, blood ketones, glucose-vs-ketosis, acid-base discrimination, insulin/dextrose/K, endpoint, and flags vomiting-associated alkalosis as a competing acid-base effect.
- Current [clinical topic atlas](../../content/clinical-os/index.md) is structured by clinical question → physiology → discriminating evidence → reading order → test. Its current top-level kidney, perfusion and respiratory headings do not independently connect this published euDKA lesson as an explicit acid-base/ketosis Concept Family branch (observation from 2026-10-31 read, not a negative claim about every index in the repository).
- Sources have different authority: 2024 multidisciplinary DKA consensus = **formal criteria**; 2025 IBCC DKA = expert bedside heuristics and decomposition; 2024 independent published masked-euDKA case = real observational counterexample, not guideline; 2026 Cai/Fu/Tan case = distinct real euDKA scenario with frankly low pH and bicarbonate.

## Candidate source-linked reasoning spine (NOT a clinical decision algorithm)

```
[insulin action / carbohydrate intake / SGLT2 glucose excretion]
    ├─ can decouple measured glucose from continued ketogenesis
    └─→ [beta-hydroxybutyrate + circulating ketoacid load]
                 ├─→ [formal D/K/A classification gate] (source: 2024 consensus)
                 └─→ [independent ongoing acid burden]
                              ├─→ [observed pH/HCO3 altered by other processes]
                              │      └─ vomiting-driven metabolic alkalosis can mask the biochemical acid signal
                              └─→ [AG, source of unmeasured anions, beta-OHB, time trends]
[test and treatment stages]: [potassium/insulin/dextrose safety axes] → [ketone-based resolution rather than glucose alone]
```

**Typed candidates:** `glucose_is_not_proxy_for_ketogenesis` `guards_against` `false_dka_exclusion`; `formal_dka_DKA_criteria` `defines` `classification`; `vomiting_alkalosis` `can_mask` `observed_acidemia` despite independent `ketone_acid_load`. These are separate claim IDs, not tags, synonym strings, same-family-by-word-occurrence, validated prerequisites or patient-specific causal proof.

## Five real research questions; rationale and first disposition (human evidence-coded initial policy)

| Gap | Source-backed observation | Scope/impact | First disposition |
| --- | --- | --- | --- |
| G1 `masked-formal-boundary` | 2024 formal D/K/A requires **measured pH <7.3 and/or HCO3 <18** for A, while IBCC describes clinically important ketogenesis hidden by vomiting-associated alkalosis and a 2024 case reports normal pH/HCO3 with high beta-OHB/AG. Mis-merging "formal case definition" and "clinical concern for masked acid burden" teaches false exclusion or false classification. | CURRENT / BLOCKING; spans DKA, mixed acid-base, diagnostic test interpretation | **RESEARCH_NOW — actually investigated below** |
| G2 `severity-discordance` | Cai 2026 case text/table labeled moderate yet the HCO3 6.5 mmol/L is a severe biochemical indicator in 2024 consensus; all Table 2 categories do not need to match, and site of care is contextual. Already flagged in existing lesson. | CURRENT / BLOCKING but the existing article already preserves the caveat | QUEUE independent medical QA; do not assign definitive ICU level from one value |
| G3 `end-point-sampling` | 2024 consensus uses plasma ketone <0.6 plus **venous** pH ≥7.3 or HCO3 ≥18; Cai 2026 case's 72h Table gives **arterial** pH 7.356, HCO3 16.8. Original lesson notes this. | CURRENT / bounded source-information gap | **PRESERVE_UNKNOWN** for the unreported 72h venous pH; do not fabricate value, clinical recovery supported separately |
| G4 `review-2026-source-access` | 2026 ADA Table 16.1 criteria are visible in indexed ADA/PMC search content, but full publisher page/tool fetch returns 403 and PMC fresh open may challenge. No independent full-table figure QA can be claimed from snippets. | NEARBY / TRANSFER; supports DKA version trace | QUEUE legal full-text/table source inspection; 2024 fully accessible consensus currently sufficient for formal D/K/A |
| G5 `atlas-ketosis-bridge` | Published euDKA clinical narrative is not explicitly linked from the clinical reasoning atlas's topic flow, despite transfer opportunities across acid-base, potassium, respiratory compensation and treatment endpoints. | NEARBY / TRANSFER across at least 3 families | QUEUE a *proposed* atlas edge, not silent published navigation change |

**Important:** The code `tools/ale_gap_triage.py` currently only accepts `PUBLIC_SYNTHETIC_ONLY` caller-supplied abstract role tokens. This real clinical source audit was performed explicitly by an assistant using evidence, not run through that tool as if it had autonomously read the papers. Its ranking is a reasoned candidate, not an audited LLM causal utility model.

## Resolved one decision-relevant source conflict: G1

**Q1 — What is the apparent contradiction?** The 2024 multidisciplinary consensus defines adult DKA with three D/K/A requirements (diabetes/prior history or glucose ≥200 mg/dL, beta-OHB ≥3.0 mmol/L or urine ketones ≥2+, **and** pH <7.3 and/or HCO3 <18). But an actual patient can have a clinically important ketoacid burden yet net pH/HCO3 appear normal because of another concurrent acid-base disturbance. A patient with normal pH/HCO3 therefore might not strictly satisfy the *formal criteria*, while ketoacid pathology still deserves differential investigation. Those are not logically interchangeable claims.

**Q2 — How can both observations hold?** The DKA criteria describe a diagnostic classification using observable composite measures. Acid-base physiology sums concurrent processes: vomiting-related chloride depletion/metabolic alkalosis may increase net HCO3 and offset the ketoacid-induced reduction. The 2024 consensus itself acknowledges mixed acid-base disorders and vomiting-related alkalosis. A 2024 independent case report documents pH **7.37**, HCO3 **26 mmol/L**, AG **23**, beta-OHB **7.1 mmol/L**, presenting glucose **186 mg/dL** in prose; it was treated as high concern for euDKA with superimposed alkalosis. **Caution:** this case's Table 1 also lists additional glucose 283/266 mg/dL without a clear same-time mapping. Never fuse different draws or use that table alone to prove a consistently euglycemic trajectory.

**Q3 — What breaks an overgeneralized concept?**
- Wrong inference A: "If pH and HCO3 are normal, no clinically important ketoacidosis can be present." Counterexample: concurrent metabolic alkalosis with high beta-OHB/AG; examine source, timing, and differential.
- Wrong inference B: "If beta-OHB is high and glucose is not high, the 2024 *formal D/K/A criteria* are necessarily all satisfied." Counterexample: measured A criterion may be absent because of mixed disorders; it remains a clinically important **suspected masked state**, not automatic literal satisfaction of the formal definition.
- Wrong inference C: "Any high AG proves DKA." Other causes of unmeasured anions exist; ketone source, diabetic context and other acids still matter.

**Concept Family revision candidate:**
1. `dka-formal-criteria-v2024` (diagnostic operational definition, not all possible physiologic expressions)
2. `ketone-acid-load-under-mixed-disorder` (physiologic acid burden despite offsetting alkalosis)
3. proposed typed relation: `mixed_metabolic_alkalosis masks_measured_acidemia_of ketone_acid_load`;
4. explicitly **do not** encode `normal_pH implies no_ketoacidosis`; **do not** merge (1) and (2), nor assert (2) independently validates a clinical diagnosis.

**Result achieved:** a medically consequential logical **boundary was identified and source-checked**, with proposed concept split and counterexample. This is a *research candidate*, not proof of a live ALE concept-creation agent, clinical peer review, or measured learner benefit. No existing card, private mapping, publication, or published article has been modified.

## Source locator / validation specificity

- Adult 2024 consensus: Umpierrez GE et al., *Diabetes Care*. 2024;47:1257-1275. DOI https://doi.org/10.2337/dci24-0032; fully accessible sibling text https://pmc.ncbi.nlm.nih.gov/articles/PMC11272983/ . D/K/A, mixed disorders, ketone-based resolution and venous pH.
- IBCC DKA: Josh Farkas, 2025-09-30 https://emcrit.org/ibcc/dka/ — formal 2024 definition contrasted with a separately labeled IBCC expert two-part heuristic and masked alkalosis. Expert resource is a *differently scoped approach*, not replacement of consensus.
- Independent 2024 masked case: Hillock MF et al., *Oxford Medical Case Reports*. 2024;2024(7):omae071. https://doi.org/10.1093/omcr/omae071 ; pH7.37/HCO3 26/AG23/beta-OHB7.1 and note of internally mixed glucose values/timestamps.
- Distinct published euDKA case: Cai J, Fu T, Tan C., *Front Endocrinol*. 2026;17:1882272 https://doi.org/10.3389/fendo.2026.1882272 (glucose 153 mg/dL with obvious severe measured acidemia; **not** the normal-pH masked case).
- 2026 ADA hospital standards: https://doi.org/10.2337/dc26-s016 ; publisher/table full-content verification still not asserted.

## What the next independent review must test

1. Verify 2024 DKA and acid-base claims *against original source context*, especially that formal definition vs bedside high-risk state remains distinguishable without recommending inconsistent treatment.
2. Confirm no patient-specific timeline of the 2024 masked case was reconstructed from discordant glucose table cells.
3. Challenge new candidate relation with a non-DKA high-AG case: a positive ketone signal is not sufficient to assign insulin-deficient DKA without the rest of the evidence.
4. Evaluate `NO_CARD` vs a small **learner-unseen** discrimination question, rather than treating a research note as proof of learning; private owner learning data stays outside public GitHub.
5. Only after semantic independent QA propose canonical Concept identity/typed edges and atlas navigation update; publication requires existing gates. No new automation or scheduling.

**Status:** `SOURCE_GAP_G1_RESEARCHED / CONCEPT_EDGE_CANDIDATE / MEDICAL_QA_PENDING / NO_LEARNER_EVIDENCE / NO_AUTONOMOUS_SEMANTIC_AGENT_CLAIM`.
