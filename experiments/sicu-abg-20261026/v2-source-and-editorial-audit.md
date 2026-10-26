# CTICU ABG article 01 — V2 source / first-rewrite audit

Date: 2026-10-26 Asia/Taipei. Status **DRAFT/HOLD**. The V1 stays frozen at creation commit `b9f5ee1c9ab0719da4f657d7990c1a199c28cf92`. The article's changed V2 is `first-draft-v2-cabg-lactate-rewrite.md`, not the first-draft baseline. The new SVG is `cabg-case3-v2-timeline.svg`. The figure is original work based on measured Table 1 numbers, not the author's own Figure 1.

## Real source checks completed this turn

1. **Wardhana & Kurniawaty 2025**, publisher-hosted 10-page PDF at https://macc.perdatin.org/index.php/my-journal/article/download/429/365/ . Original print **p278, PDF 0-based p3**, visually inspected:
   - Third patient age 69, EF 45%, CPB 108 min, cross-clamp 91 min, ischemia 82 min.
   - Post CPB dobutamine 5, norepinephrine 0.05, epinephrine 0.05, nitroglycerine 0.5 mcg/kg/min; clinically unstable / pacing.
   - Postop TTE EF 45%, CO 5.1 L/min, CI 3.1 L/min/m², SVR 580 dyn·s/cm⁵, regional hypokinesis.
   - Case 3 T0–T5: lactate 3.6/14.8/14.8/8/2.8/1.9; BE -7.69/-15.7/-7.9/-3.8/2.92/2.0; ScvO₂ 92.6/95/92.1/82.0/N/A/N/A; glucose 237/340/277/200/138/154 mg/dL.
   - Source Table 1 has no complete pH, PaCO₂, PaO₂, HCO₃⁻, Hb, albumin/chloride sequence. Despite the source describing the panel as 'arterial blood gas analyses', **V2 appropriately avoids generating such numbers**.
   - Original print **p279, PDF 0-based p4**, visually inspected Figure 1. It labels **T6** despite Table 1 giving no T6 column or time definition: unresolved internal source discrepancy. V2 redraws only original Table 1 T0–T5. No source figure is reproduced or cropped. 
2. **Smyth et al. 2021**, full Oxford/ICVTS source https://academic.oup.com/icvts/article/33/3/494/6271397 read:
   - Separate CABG 54-year-old patient on dapagliflozin; pH 7.45 **after anesthetic induction**, not the later metabolic acidaemia.
   - Later base deficit −15.8 mmol/L, arterial lactate 0.9 mmol/L, SvO₂ 68%, PaCO₂ 2.9 kPa, blood glucose 6.5 mmol/L, blood ketones 4.9 mmol/L / urinary 3+. EuDKA course recurred after therapy withdrawn early. No simultaneous later complete pH/Na/Cl/HCO3 given to compute exact AG, so V2 does not make one.
   - The paper's author's recommendation to hold SGLT2i five days is 2021 opinion, not a current authoritative cardiac surgery protocol. Current 3–4 day stop recommendations were checked for **2024 ADA** / **AHA/ACC noncardiac surgery**; note cardiac vs noncardiac scope.
3. **IBCC Farkas** `cts` 2025-01-05, `agma` 2024-06-29, live HTML read:
   - Cardiothoracic postop initial assessments: drains, A-line, pressors, exam/perfusion, gas/CBC/coagulation, ECG, echo; differential: bleeding, pump failure, obstruction, vasoplegia, rhythm.
   - Targets in IBCC are explicitly **rough**; CVP/PAWP pressures do not establish fluid responsiveness, ScvO₂ and SvO₂ are distinct.
   - IBCC AGMA simplification computes **uncorrected AG**, whereas existing Pocket/other guidelines may require albumin correction. Explain context and avoid declaring one version always right.
4. **2024 EACTS/EACTAIC/EBCP CPB guidelines** open-source HTML at https://pmc.ncbi.nlm.nih.gov/articles/PMC11947607/ or https://pmc.ncbi.nlm.nih.gov/articles/PMC11826095/; searched normative CPB DO₂, monitoring, and LCOS. Normothermic **on-CPB** DO₂ thresholds and post-CPB intensive care are different contexts. Do not transpose CPB GDP target into after-CPB fluid orders.
5. **Minton/Sidebotham 2017** https://pmc.ncbi.nlm.nih.gov/articles/PMC5347225/; review confirms hypoxic and nonhypoxic postoperative hyperlactatemia mechanisms but is older explanatory support, not proof of this case's epinephrine causation.

## Provisional editorial read of *rewrite*, not first draft

The prior V1's AI screen **81/100 remains frozen**. Following actual re-read of V2, provisional non-blinded AI estimates (must not be represented as independently verified):

| V2 editorial axis | provisional pts |
| --- | ---: |
| Thesis & focus /20 | 18 |
| Prerequisite chain /20 | 19 |
| Bedside decisions and condition changes /20 | 18 |
| Source and real-case fidelity /15 | 15 |
| Functional figures and actual mobile experience /10 | **7** |
| Language and cognitive cost /10 | 8 |
| Cross-links and provenance /5 | 4 |
| **Total (provisional only)** | **89/100, HOLD against 90/100 gate** |

EPQC A–G internal read: A4 B4 C4 D4 E3 F4 G3 (total 26/28). This is a non-blinded writer-side review, not the independent reviewer required for a reliable score.

V2 does **materially** improve V1: immediacy of postoperative diagnosis, term definitions before advanced inference (ABG/HCO3/BE/ScvO2 vs SvO2/DO2), source-protected lactate-vs-BE timepoint comparison, a true CABG euDKA contrast with low lactate, and device-agnostic flow without assuming a Swan-Ganz catheter.

## Unclosed release checks

- SVG **source file created and statically checked** for role/accessible title/desc, separate axes, 12 actual lactate and BE observation markers, ScvO₂ N/A preservation, relative image link. It has **not yet been screenshot-inspected at actual 375–390px mobile viewport** nor screenreader tested. No claim of Figure Gate pass.
- Need re-view Pocket Medicine 9E actual p158–162 Table, Figure 4-1 and footnotes during this revision. Existing `acid-base-sources.md` records older audit only; do not transmute into current run verification.
- Need independent clinician reviewer on complex CTICU statements: negative BE interpretation with unknown pH, source inference of vasoplegia vs medication-driven SVR, possible localized post-cardiotomy tamponade despite nondiagnostic TTE, and the narrative's separation of true whole-body DO2 from microvascular oxygen use.
- A next rewrite should reduce repeated disclaimers while preserving safety boundaries; consider a small second original mechanism image only if it reduces comprehension burden.
- At publication, move citations/audit into standard site source page, adjust internal links, check all rights, test 375–390px graphics, run repo clinical figure gate / CI, and only then add to `site/pages.json`.
- No medical reader comprehension test, no independent blind native-model comparison, no final HTTPS deployment. This file is a quality *screen* only and must not be treated as evidence the series now has a 90+ first-draft success rate.

**Outcome:** First-draft V1 remains unsuccessful 81; reworked V2 is complete and source-backed, provisional 89; no merge to main or public publishing.
