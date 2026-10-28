# CTICU ABG 04 | PRIVATE source and publication audit — HOLD

Date: 2026-10-29. New private article: archive/xiaoma-internal-medicine/drafts/2026-10-29-cticu-abg-04-alphastat-phstat.md. Does not alter public site, original authors, article registries, or figures.

## Distinct question / reader gain
ABG 03 covers fluid-related metabolic acid-base forces. ABG 04 covers low-temperature measurement frame vs actual CO2 management strategy, and tests two questions separately: (1) same specimen reported at 37C vs temperature correction; (2) target-dependent oxygenator CO2 manipulation affecting cerebral perfusion. Do not conflate display adjustment with actual therapeutic intervention.

## Checked and bounded sources

1. 2024 EACTS/EACTAIC/EBCP adult CPB guideline, 2025 print; §10.3 and Recommendation Table 52. Original licensed PDF https://iperfusion.org/wp-content/uploads/2025/02/EBCP-Guidelines-on-cardiopulmonary-bypass-in-adult-cardiac-surgery.pdf: PDF zero-index p57 screenshot visually reviewed. Adult high-moderate hypothermia alpha-stat IIa B. 2019 guideline §7.5 explicitly excluded DHCA from mild-moderate routine alpha-stat discussion. Do not overgeneralize to deep HCA, pediatric population, or every adult surgical situation.
2. Patel RL et al. 1996, PMID 8642829, DOI 10.1016/S0022-5223(96)70230-1. PubMed + ScienceDirect abstract accessible; PDF 403. RCT n70 adult CABG alpha 7/35 (20%) vs pH 17/35 (48.6%) neuropsych impairment defined as deterioration in three or more tests at six weeks, p=0.02. Do not claim all clinical neurological endpoints, stroke, mortality or modern generalizable risk.
3. Murkin JM et al. 1995, PMID 7637352, DOI 10.1016/S0022-5223(95)70230-X. PubMed/ScienceDirect abstract available; 2x2 randomized pulsatile vs nonpulsatile and alpha vs pH, n316 CABG. Whole-study stroke 2.5% without between-group difference. Cognitive outcome at two months, CPB >90min alpha 27% vs pH 44%, p=0.047. Stratified analysis, not pooled 316-patient event percentages.
4. OpenAnesthesia pH Stat vs Alpha Stat, last updated 2026-08-31, https://www.openanesthesia.org/keywords/ph-stat-vs-alpha-stat/ full editorial explanatory page read. Physiology: decreased temperature increases gas solubility; temperature-corrected pH rises and PCO2 falls; alpha 37C, pH actual-temp; CO2 influences cerebral blood flow. Educational overview not treatment guideline; do not copy images. Some claims on strategy preferences are broader than actual adult guideline.
5. Chatzopoulou et al. 2025 systematic review, PMID 40755621, PubMed abstract only; seven studies mixed adults/pediatrics; avoid unstratified conclusion about adult DHCA.
6. Hydrogen ion (pH) and gas behavior during deep hypothermic CPB, PMID 42332422, 2026 review abstract only; no patient measurements quoted.
7. Temperature correction examples: article intentionally uses no fabricated matched raw/corrected numerical ABG pairs, as exact values depend on temperature, composition and correction method. 28C is illustrative only.

## Medical / narrative hard stops and QA

- [x] One main narrative: instrument → actual-temp physics → intervention → cerebral perfusion → RCTs → subgroup/generalizability → ICU handoff.
- [x] Distinguishes 37C reported pH vs actual-temp corrected pH vs actively changing CO2 clearance. No patient case-report data created.
- [x] RCT outcomes have separate timing and denominator; population boundaries explicit.
- [ ] Independent clinical review of pH-stat mechanism, histidine/alpha rationale, actual-temp targets and cerebral risk against primary trials or specialty references. If original tables inaccessible, maintain abstract-only provenance.
- [ ] Independent EPQC paragraph-semantic packet on exact content blob; reviewer must genuinely be separate, not current authoring pass.
- [ ] Original causal figure if clearly better than prose, verify temperature/specimen/intervention logic and 360/390/1280 rendering; no copied publisher figures.
- [ ] Official Taiwan second-stage exams verification.
- [ ] Public registry, source and figure gate, local validation, build, exact-head CI and production SHA readback are all future release scope.
- [ ] External clinician peer review not performed.

Current state: PRIVATE EDITORIAL DRAFT / HOLD. No merge/deploy or review pass claimed.

## 2026-10-29 cross-source adversarial audit (author-side, not independent review)

**P1 secondary-evidence classification failure found and corrected in reader text:**
- Chatzopoulou 2025 https://pmc.ncbi.nlm.nih.gov/articles/PMC12318452/ incorrectly classifies Abdul Aziz & Meduoye 2010 as a prospective n160 RCT. Actual https://pubmed.ncbi.nlm.nih.gov/19914925/ is a BEST EVIDENCE REVIEW of 206 located and 16 selected articles, not a clinical trial.
- Same review labels Voicu 2014 as an n88 prospective RCT in post-arrest hypothermia. Actual https://pubmed.ncbi.nlm.nih.gov/24717455/ is an observational crossover study of therapeutic hypothermia after out-of-hospital cardiac arrest, NOT surgical DHCA. Both study-design and target-population mismatches materially bias clinical synthesis.
- Consequently, removed 2025 review as evidence supporting clinical strategy; reader's source list instead explicitly labels 2010 BEST EVIDENCE review as historical commentary, NOT new RCT data. Preserve direct adult RCT Patel 1996 https://pubmed.ncbi.nlm.nih.gov/8642829/ and Murkin 1995 https://pubmed.ncbi.nlm.nih.gov/7637352/ plus guideline https://pmc.ncbi.nlm.nih.gov/articles/PMC11826095/ . Patel/Murkin underlying tables remain inaccessible; abstract-grounded numeric claims only.
- Original conceptual SVG saved under archive/xiaoma-internal-medicine/drafts/figures/2026-10-29-cpb-alpha-phstat-logic.svg: mobile-first 390x1040, distinguishes specimen measurement/display from actual CO2 addition and target choice; text-bound static estimation found no overflow. Not an actual browser/mobile screenshot check.
- Verify in future independent pass: rewarming or post-CPB ABG must not be excused by a previous intraoperative pH-stat strategy; adult high-moderate hypothermia guidance is not direct evidence for all DHCA/pediatric cases.
- Current release gate: HOLD, no independent reviewer approval, no actual phone/browser screenshot, no production deployment.
