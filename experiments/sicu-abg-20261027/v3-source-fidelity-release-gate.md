# CTICU 02 — V3 source-fidelity correction and release gate (2026-10-27)

Status: HOLD. This is an additive QA record; V1 79/100 and V2 85/100 remain immutable. No retrospective score change.

## Verified against the V2 manuscript and existing source-gate record

1. CPB Table 2 reports aggregate SaO2 98±0.5%, PaO2 230±25 mmHg, pump flow 5.4±0.25 L/min, DO2i 295±10 mL/min/m2, SvO2 76±2%. These are not synchronized values at the reported DO2i nadirs.
2. The two described episodes (DO2i 260 with impaired venous return; DO2i ~275 with hemodilution/Hb 7.9) are during CPB. No inference of postoperative low cardiac output or tissue hypoxia is justified.
3. The source narrative's <280 for 8.5 minutes versus <300 for less than 5 minutes is internally inconsistent if both refer to the same interval. Do not construct a timeline or oxygen debt from those durations. CPB starting Hb 8.2 vs Table 3 CPB Hb 10.4 has unresolved sampling definitions.
4. Table 3 postoperative 12-hour Hb 9.7, PaO2 99.4, pH 7.38 does not include simultaneous measured SaO2 and CO; postoperative CaO2 and DO2 cannot be established for this patient.
5. CPB DO2i target 280–300 mL/min/m2 in the 2024 EACTS/EACTAIC/EBCP guideline is context-specific to normothermic CPB; it is not a universal postoperative ICU transfusion or inotrope trigger.
6. The 2004 retracted study must remain excluded from positive evidence. Okamoto 2026 retrospective CVICU SvO2 study does not establish transfusion benefit or a 69% threshold.

## Required before publication

- Original publisher PDF Table 2/3: a previous conversation turn reported visual inspection of pages 4–5 and confirmed the displayed table values; this QA record does not independently reproduce that inspection. Preserve unresolved narrative/table sampling and duration inconsistencies; original visual proof must be attached to the release audit before marking this gate PASS.
- Pocket Medicine 9E p32/p374 original-page inspection and 2024 PBM Table 11 captions/footnotes; public figures remain original/link-only.
- Render original SVG at 375 and 390 CSS px in the actual site, inspect text, clipping, and captions.
- Separate medical review evidence from AI editorial screening; complete EPQC/Figure Gate and actual CI, production Cloudflare deployment, HTTPS readback.
- No site/pages.json inclusion, merge, or publication before these checks pass. PR #56 is obsolete; preserve PR #72 on main.

Human interventions: no user correction during this QA step; elapsed human minutes not observed (unknown, not zero). No independent physician review has been performed.

## 2026-10-27 subsequent gate audit

- V2 SVG source inspected directly: viewBox 440×840; two separate CPB episodes; explicit average-versus-event caveat; no invented duration or postoperative CO. Static SVG markup alone does **not** establish 375/390px rendered legibility or absence of clipping.
- Figure text at native width includes 12–14px caveats; at 375px responsive width these scale to approximately 10.2–11.9px. This is a potential mobile legibility failure and warrants a redesign or verified larger-format presentation before release.
- Distinguish direct evidence checked in this audit (GitHub V2 text/SVG) from previous-turn reported PDF visual inspection. No false PASS for unobserved browser tests.
