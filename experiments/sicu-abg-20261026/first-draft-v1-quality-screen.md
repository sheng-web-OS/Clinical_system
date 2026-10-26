# CTICU ABG Pilot 01 — first-draft frozen QA screen

Date: 2026-10-26 Asia/Taipei
Immutable baseline: `first-draft-v1-cabg-lactate.md` first created at commit **b9f5ee1c9ab0719da4f657d7990c1a199c28cf92**. Do not edit or rewrite this initial file; use a separately versioned V2 for repairs.
QA type: **non-blinded AI editor screening** following first draft; NOT independent assessment, not proof of medical safety, not a validated learner score.

## Provisional 100-point quality estimate (not a scientific measurement)

| Pre-registered axis | Provisional points | Concrete observed evidence / weakness |
| --- | ---: | --- |
| Core thesis & editorial focus (20) | 17 | One strong CABG contrast, lactate vs ScvO₂ vs BE; still largely a lactate–hemodynamics article rather than a complete ABG interpretation article |
| Prerequisites & causal bridge (20) | 17 | Defines arterial/venous sample, BE, lactate, DO₂, ScvO₂ and production/clearance; needs deeper exemplified connection to ABG pH/PaCO₂ from an actual cardiac case |
| Bedside decision safety & counterfactuals (20) | 17 | Explicit bleeding/LCOS/tamponade and avoidance of reflexive fluid bolus; limited clinically measured decision timepoints and no physician-vetted algorithm |
| Real-case / source fidelity (15) | 14 | PDF Table 1 and Figure 1 verified on original rendered pages; case-specific T0–T5 and treatment support documented; no complete original ABG series, so cannot teach all four ABG variables from this one case |
| Figures & 375–390px comprehension (10) | **4** | Time-series numerical table and Mermaid branch included, but no responsive labeled chart, no visual mobile/screenreader acceptance or original Pocket re-check this turn |
| Language & cognitive load (10) | 8 | Narrative mostly contiguous, some overlong sections, sparse temporal explanation of interventions |
| Minimal cross-lesson links & provenance (5) | 4 | Clear relationship to acid-base/hypoxemia and 4 primary sources, but not wired to actual site navigation (as appropriate for a private draft) |
| **Total** | **81 / 100 (provisional AI self-screen)** | **HOLD** vs pre-registered >=90; AI assessment has unknown reliability |

Medical hard gate: no *identified* definite P0/P1 in this non-blinded reading; **NOT VERIFIED** by independent physician. No physician review; no independent clinical case study reader; no source-wide figure QA. A high self-score would never override medical uncertainty.

## Most important first-draft misses to preserve as feedback

1. **Central topic is ABG but primary case report lacks complete pH/PaCO₂/PaO₂/ABG time series.** Correctly disclosed missingness, but this limits what the first paper can teach; supplement with a second verified post-cardiac case with complete ABG or narrow the section title to ‘lactate + venous saturation + BE’ and use ABG as a transition. Do NOT fill the CABG case's missing values from another paper.
2. **Real visual explanation still incomplete.** Add an accurate, mobile-first original timeline of actual lactate, BE and ScvO₂ values (prefer aligned time axes with separate scales); audit original Pocket 9E p158–162 figures / caption when formally publishing. Merely pasting Mermaid or a Markdown table is not a reader-facing figure pass.
3. **No independent blind review yet.** Must have a second independently structured clinical assessment before claiming first-draft quality. Future reviewer should specifically challenge whether ScvO₂/CI-based reassurance is overstated, whether evidence allows Type B classification, and whether bedside causes were prioritized correctly.
4. **Temporal evidence → decision linkage** should become more concrete: what data are contemporaneous versus only a snapshot; which new measurement would change immediate treatment and why. Do not give ungrounded fluid/inotrope protocols.
5. **2026 cohort** currently verified only via PubMed abstract; do not cite numeric risk cutoffs as decision thresholds or claim detailed methods reviewed.

## What counts next

Initial V1 score remains 81 as an internal estimate regardless of future improved drafts. Improvement may be documented separately as V2, including actual user-raised issues and minutes; never retroactively change the V1 evidence. For series ability claims, repeat on thoracic-case and ventilator-case prompts with frozen first drafts; measure first-pass >=90, P0/P1, source/figure fidelity and user correction burden.

Current publication states: private V1 artifact CREATED; primary CABG article Table1 and Fig1 visually CHECKED; Pocket figure reinspection PENDING; medical independent review PENDING; site Figure Gate PENDING; responsive graphics PENDING; main merge / deploy / HTTPS NOT DONE; human learning experiment NOT DONE.
