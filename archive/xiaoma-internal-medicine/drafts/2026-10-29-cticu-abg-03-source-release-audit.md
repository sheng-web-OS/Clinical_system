# CTICU ABG 03｜Source / clinical / release audit — PRIVATE HOLD

2026-10-29。正文：archive/xiaoma-internal-medicine/drafts/2026-10-29-cticu-abg-03-cpb-acidbase.md。新稿未列入 site/pages.json，**不是已發表教材**。

## Editorial purpose

- 系列承接：#72 CABG lactate/ScvO2 與 #115 CPB oxygen delivery 已合併；第三篇聚焦 CPB 後 non-lactate metabolic forces，避免重寫既有 Winter、AG、lactate 篇。
- 核心疑問：HCO3 / BE 下降時，為何不能宣稱就是 lactic acidosis；SID 降低但 pH 可能相對穩定，隔日反而因 PaCO2 改變酸血症。
- 真實觀察：2013 Chuah CABG cohort n=55 on pump、n=26 off pump 的術前、CABG+protamine 後、隔日 06:00 組別平均。**不是單一真實個案、不能以群體均值組成個體 AG/代償或宣稱具體術後處置理由**。
- 無夾帶私人病患或輪訓資訊；文中模擬接班決策為明示條件式教學，不是 clinical case chart。

## Verified primary evidence and actual access

1. **Chuah CS et al. 2013 J Cardiothorac Surg 8:184** DOI 10.1186/1749-8090-8-184; https://link.springer.com/article/10.1186/1749-8090-8-184 and PDF https://link.springer.com/content/pdf/10.1186/1749-8090-8-184.pdf. **Full-text and PDF visually inspected**. PDF zero-index p1 Methods; p2 Table 2–3, p3 Figure 1, p4 Figure 2, p5 Figure 3 + Table 4 + discussion. Online Table 3 https://link.springer.com/article/10.1186/1749-8090-8-184/tables/3 independently confirms figures. On pump n55: Na 139.5→135.8→137.2; Cl 105.3→111.0→106.8; HCO3 24.9→22.6→23.9; BE +0.38→-1.96→-0.75; simplified SID 38.2→29.7→35.1; [H+] 38.1→39.8→41.9 nmol/L; PaCO2 5.23→4.93→5.60 kPa. Study on-off group post-CABG SID mean difference 4.0 (CI 2.8–5.3). **Research does NOT assay lactate or albumin; Hb used indirectly for dilution, not direct albumin evidence**. Non-randomized on/off-pump assignment; fluid decisions clinical; 3 sample windows not continuous intra-CPB time series.
2. **Hayhoe M et al. 1999 Intensive Care Med 25:680–685** PMID 10470571 https://pubmed.ncbi.nlm.nih.gov/10470571/. **Abstract-only (PubMed), original Table/Figure not obtained**. n10 with polygeline/chloride-rich prime: standard HCO3 median 25→22.3 (cooling); chloride median 104.9→111.0; lactate median 3.20→1.83; SIG +3.8 at cooling & rewarming, albumin-dilution discussed. Cohort medians not same individual.
3. **Guarnieri et al. 2026 J Cardiothorac Vasc Anesth 40:204-213** PMID 41130846 https://pubmed.ncbi.nlm.nih.gov/41130846/. **Abstract-only**; publisher PDF is restricted. n50 elective cardiac surgery with CPB; ICU mean pH 7.33±0.05, BE -3.87±3.3, lactate 2.52; SIG median 6→9.8; no individual paired ABG or patient diagnosis. Does not establish SIG-guided benefit.
4. **2024 EACTS/EACTAIC/EBCP CPB guideline, published February 2025** https://pmc.ncbi.nlm.nih.gov/articles/PMC11826095/ and https://www.eacts.org/clinical-practice-guideline/2024-eacts-eactaic-ebcp-guidelines-on-cardiopulmonary-bypass-in-adult-cardiac-surgery/. **Full text / section on prime and acid-base read**, not a Table/figure reproduction. Unbalanced chloride-rich prime associated with acidosis; two small RCTs Plasmalyte vs Ringer's lactate, insufficient patient-centered outcome evidence.
5. **2009 bicarbonate-balanced vs Plasma-Lyte 148 randomised trial**, PMID 19115651 https://pubmed.ncbi.nlm.nih.gov/19115651/ **abstract only**. n20; early SIG change suggests possible exogenous acetate/gluconate, authors explicitly do not establish harm.
6. **2026 colloid priming RCT physicochemical analysis** PMID 42791111 https://pubmed.ncbi.nlm.nih.gov/42791111/ **abstract only**; 170 observations, adjunct crystalloid use associated with physicochemical shifts, cannot infer cause from extra crystalloid adjustment without design limitations.

## Numerical and methodology guardrails / discovered issue

- The original 2013 **Table 3 shows Hb unit as g/L but displays 13.8 / 10.1 etc**, values physiologically corresponding more plausibly to g/dL. Do **not** copy them into a public clinical calculation without checking a journal erratum/original author confirmation. Present draft omits Hb numerical row entirely. This mismatch is a source-quality flag, not licence to silently correct the original.
- Study 2013 SID = simplified formula as published; never assert it includes directly measured albumin, Ca, Mg, lactate or unmeasured anions. The authors explicitly lacked lactate measurement, so their albumin cancellation is a **mechanistic hypothesis**, not established individual mechanism.
- AG is Na − (Cl + HCO3), but **not calculated using mean timepoint values as if one patient**. No clinical albumin correction estimate is fabricated. No pH fabricated from group means.
- Time labels post-CABG are **after protamine reversal**, NOT while on pump. Avoid mixing CPB-on periods with post-operative arrival.
- Refrain from saying chloride-related acidification is benign or excludes hypoperfusion. The cohort never tests a lactate/shock exclusion rule.
- Separate clinical logic mechanism generation from EBM evidence ranking. No claim that normal AG or lactate has validated negative likelihood ratio for surgical tamponade/bleeding.
- No original figure copy; any public schematic must be original and non-misleading. In a figure derived from group data, label means and sampling times rather than pretending individual serial observations.

## Editorial rejection tests before any publication

- [ ] **Full source expansion**: original 1999, 2026 Guarnieri, 2009 trial tables/figures if used for new strong claims; when inaccessible stay abstract-only and restrict claims.
- [ ] **Independent medical adversarial review**: source-specific denominators, physicochemical explanatory neutrality, sample granularity, rate of albumin effect, false inference from normal lactate/AG, and hypotension management.
- [ ] **Independent EPQC paragraph packet** on exact Git blob and coverage; reviewer must be distinct from authoring context, not this audit.
- [ ] **Visual**: meaningful original chart for cohort Na/Cl/SID/H+/PaCO2 (separate axes/units) and competing mechanisms; verify source numbers; show screenshots at 360, 375, 390, 1280px. No copyright original reprint.
- [ ] **Technical**: if moved to public content, update source/figure gate and site registry only after gate; run validation, build, exact-head CI, production readback after explicit authorization.
- [ ] **Curriculum exam mapping**: search verified official 111–115 year Taiwan second-stage ABG/acid-base questions, link only true relevant items, don't force surgical CPB-specific material into exam rationale.

**Current status: PRIVATE DRAFT / EDITORIAL HOLD.** No independent approval, tests, mobile QA, merge or production publish is claimed.
