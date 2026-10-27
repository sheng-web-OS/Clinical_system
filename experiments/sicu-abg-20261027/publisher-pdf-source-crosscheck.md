# CTICU 02 — original publisher PDF cross-check (2026-10-27)

**Status: HOLD.** Additive source audit; V1 79/100 and V2 85/100 untouched. Original publisher: https://www.cureus.com/articles/446799-advanced-metabolic-guided-perfusion-concepts-in-an-obese-patient-undergoing-cardiac-surgery-a-case-report.pdf (7-page PDF, DOI 10.7759/cureus.99447).

## Source checks

- PDF printed page 4 (PDF p4, zero-index 3), Table 2: CPB mean pump flow 5.4±0.25 L/min; SaO2 98±0.5%; PaO2 230±25 mmHg; SvO2 76±2%; DO2i 295±10; DO2i <280 duration 8.5 min; CPB 156 min. Table 2 is an aggregate, not synchronous nadir measurements.
- PDF printed page 5 (PDF p5, zero-index 4), Table 3: Hb 13.4 preoperative, 10.4 CPB(Pump), 11.2 post-30 min, 9.7 post-12 h; at post-12 h pH 7.38, PaO2 99.4, PaCO2 43.2, lactate 1.1. Table 3 does not establish simultaneous postoperative SaO2 or CO.
- Narrative at PDF printed page 3 says DO2i <280 for 8.5 min; narrative at printed page 4 says time <300 for less than 5 min. Mathematically contradictory under common interval definition. Do not infer duration, AUC, or oxygen debt from this pair.
- Narrative CPB initiation Hb 8.2 and later 7.9 do not reconcile to Table 3 CPB Hb 10.4 without explicit timing. Mark unresolved; no synthetic sampling timeline.
- **Additional newly identified inconsistency:** anticoagulation narrative (printed page 2) states initial heparin 300 IU/kg, while Table 4 (printed page 5) reports heparin 400 U/kg. This does not alter the oxygen transport formula, but raises source reporting-fidelity concerns. Do not present either as an established actual dose without caveat.
- **Additional caution:** PDF describes CPB at 30°C with both 37°C-referenced and temperature-corrected DO2i; it is not clear which displayed DO2i series underlies every narrative event. Do not directly compare temperature-corrected event figures with normothermic CPB guideline thresholds as though identical definitions.
- The case report's claim that lactate and favorable recovery prove absence of tissue oxygen debt or efficacy of a DO2-guided strategy is a causal overinterpretation of one uncontrolled case. Retain observed outcomes, not causal proof.

## Verified source evidence and remaining gates

**Publisher PDF visual verification complete (2026-10-27):** original Cureus source PDF pages 4 and 5 were opened as full-page images. Tables 2, 3 and 4 were checked visually rather than relying on extracted text alone. Numerical inconsistencies recorded above remain source limitations, not repaired source data.

**Other source checks completed:** 2024 EACTS/EACTAIC PBM original PDF printed page 32 Table 11 and a/b/c footnotes visually inspected. The contemporaneous CPB guideline Tables 43 and 45 were checked in full-text publication; CPB context must not be used as a universal postoperative ICU transfusion rule. Pocket Medicine 9E PDF parsed pages 32 and 374 checked for Fick and 1.36 O2/g Hb; original book page-images 32/374 remain unavailable, although p33 image preview is visible.

**SVG check completed in a different renderer, not the website:** at 375 and 390px CairoSVG previews exposed a missing-glyph box for Unicode subscript ₂. Commit `b3229de5` replaced that unsupported literal in the SVG. Byte-identical corrected source (blob `aaf1d5ddaf073b8b69d74f84ca5129e82989e2f4`) rendered at both sizes without observed clipping. Actual Chromium reader-layout QA is still required.

**Release still HOLD** until an independent medical review, the page-included full-site CI and browser visual checks, production merge/deployment and HTTPS readback. A green CI result for a draft branch that does *not* register this teaching page is insufficient. Human intervention time is unobserved, not zero.
