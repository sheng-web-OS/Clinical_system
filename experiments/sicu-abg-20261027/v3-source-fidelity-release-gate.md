# CTICU 02 — V3 source-fidelity correction and release gate (2026-10-27)

Status: HOLD. This is an additive QA record; V1 79/100 and V2 85/100 remain immutable. No retrospective score change.

## Verified against the V2 manuscript and existing source-gate record

1. CPB Table 2 reports aggregate SaO2 98±0.5%, PaO2 230±25 mmHg, pump flow 5.4±0.25 L/min, DO2i 295±10 mL/min/m2, SvO2 76±2%. These are not synchronized values at the reported DO2i nadirs.
2. The two described episodes (DO2i 260 with impaired venous return; DO2i ~275 with hemodilution/Hb 7.9) are during CPB. No inference of postoperative low cardiac output or tissue hypoxia is justified.
3. The source narrative's <280 for 8.5 minutes versus <300 for less than 5 minutes is internally inconsistent if both refer to the same interval. Do not construct a timeline or oxygen debt from those durations. CPB starting Hb 8.2 vs Table 3 CPB Hb 10.4 has unresolved sampling definitions.
4. Table 3 postoperative 12-hour Hb 9.7, PaO2 99.4, pH 7.38 does not include simultaneous measured SaO2 and CO; postoperative CaO2 and DO2 cannot be established for this patient.
5. CPB DO2i target 280–300 mL/min/m2 in the 2024 EACTS/EACTAIC/EBCP guideline is context-specific to normothermic CPB; it is not a universal postoperative ICU transfusion or inotrope trigger.
6. The 2004 retracted study must remain excluded from positive evidence. Okamoto 2026 retrospective CVICU SvO2 study does not establish transfusion benefit or a 69% threshold.

## Verified during 2026-10-27 release preparation

- **Publisher PDF visual source check completed**: original Cureus 7-page publisher PDF, page 4 Table 2 and page 5 Tables 3–4 were directly inspected at full-page image resolution. CPB SaO2 and DO2i aggregates, CPB/12-hour Hb, and the separate Table 4 heparin-dose inconsistency were verified. The 8.5-minute vs <5-minute and Hb 8.2 vs 10.4 differences remain **unresolved source-internal contradictions**, not errors to silently correct.
- **2024 EACTS/EACTAIC PBM Table 11 original PDF visually inspected** (printed page 32 / PDF one-index page 32): restrictive <=75 g/L vs <=90 g/L only if the patient's clinical condition permits (Class I, A); HCT 18–24% with inadequate oxygenation during CPB may warrant consideration of PRBC after evaluating DO2 and cerebral oximetry (IIb, B). Footnotes a, b, c identify class, evidence level and references; no universal postoperative SvO2 transfusion threshold.
- **2024 CPB guideline Table 43 and 45 checked** in published full text: DO2i 280–300 only for normothermic CPB (IIa, B); Table 45 d footnote adds DO2 >273 mL/min/m2 with satisfactory cerebral oximetry in the CPB Hct decision context.
- **Pocket Medicine 9E PDF text verified** for page 32 Fick cardiac-output paragraph and page 374 formula; the original book uses oxygen binding factor 1.36 versus the article's common 1.34 approximation. PDF p33 visual preview available. Full original p32/p374 *page-image* verification remains unavailable: the library image service did not return those pixels and a raw PDF materialization attempt failed. Do not claim pixel-complete book review.
- **SVG 375/390px external raster smoke check completed** with CairoSVG on a byte-identical local copy of the latest committed SVG: initial 375/390px captures exposed tofu for Unicode subscript ₂; the local SVG and committed source were corrected to ASCII DO2i/SaO2. After fix, both sizes displayed all text without observed clipping in inspected captures. The local copy without final newline matched Git blob SHA `aaf1d5ddaf073b8b69d74f84ca5129e82989e2f4` byte-for-byte. This is **static asset validation**, not a full-site Chromium render.

## Remaining before production release

- Independent medical quality review / acceptance distinct from authoring and AI self-check; source-internal inconsistencies retained.
- Full site build with **new CTICU lesson actually registered** in `site/pages.json` and its SVG copied into flat distribution; specifically preserve current main's official national-exam interlinks. A HOLD-only branch CI pass is *not* evidence the new lesson builds.
- 375/390px **actual browser rendering** in reader layout: compare heading/figure, enlarged text, captions, horizontal overflow and clickable source link. Confirm the original source visual-access requirements or clearly scope them as reference-text checks.
- Merge and production deployment only after release gates, followed by HTTPS readback. PR #56 obsolete and PR #72 published content must not regress. No user intervention counted as zero if not measured.

## 2026-10-27 subsequent gate audit

- V2 SVG source inspected directly: viewBox 440×840; two separate CPB episodes; explicit average-versus-event caveat; no invented duration or postoperative CO. Static SVG markup alone does **not** establish 375/390px rendered legibility or absence of clipping.
- Figure text at native width includes 12–14px caveats; at 375px responsive width these scale to approximately 10.2–11.9px. This is a potential mobile legibility failure and warrants a redesign or verified larger-format presentation before release.
- Distinguish direct evidence checked in this audit (GitHub V2 text/SVG) from previous-turn reported PDF visual inspection. No false PASS for unobserved browser tests.
