# Sepsis IBCC 深度重寫：來源與差距驗收紀錄

日期：2026-10-27。僅限 PR #164 的私人審查；此報告不是公開教材，不是獨立審稿通過聲明。
正式待審正文：`content/clinical-os/2026-10-27-sepsis-from-infection-to-resuscitation.md`；最新 blob 必須依 PR head 重新讀取，不可沿用此前版本。

## Input / before
- 起點為 branch `study/ibcc-sepsis-foundations-20261027` 的原 Sepsis 中文草稿，約 8,385 UTF-8 字元，含定義、機轉、治療與單獨連回 Tamponade 病例。
- 舊稿缺口：缺少從 PAMP/DAMP/內皮到血管失張與器官功能障礙的中介；venous return/stressed volume 尚未論證；fluid responsiveness/tolerance 沒有完整改判；IBCC PHR 的監測介入回饋尚未形成主幹；未充分敘述 cardiomyopathy/ARDS/AKI/de-resuscitation 的時間演變。
- 原稿是 Git history 的前版，不改作者歷史作品，也未變更已發布 `content/tamponade.md` 或 PR #163/#165。

## New draft
- 新版約 20,450 字元，十九段主要論證節，兩張原創文字 Mermaid 機轉圖。
- 使用明示「教學虛構」的 67M obstructive pyelonephritis 長時序；不冒充 Case Report、PGY 個人病人或 IBCC 實測。
- 重要新橋樑：source×host×perfusion×feedback；PAMP/DAMP→glycocalyx/vasoplegia/capillary leak→microcirculation；stressed/unstressed volume；CO/SVR/DO2 vs MAP/SpO2；source control as distinct action；fluid responsiveness ≠ fluid requirement/tolerance；NE raises pressure but CO may worsen；CRT/DBP/perfusion across PHR challenges；cardiomyopathy and load-dependent EF；ARDS/AKI and de-resuscitation.
- 對照反例：同 MAP 不同 CRT；PLR positive 但 fluid intolerance；NE 達標但少尿；shock control 後 fluid overload；PCT/lactate 不能單獨指定 Sepsis。

## Sources read and observed (source scope)
1. IBCC Farkas `https://emcrit.org/ibcc/sepsis/`，2025-11-11；本輪實際閱讀 Definitions，Presentation，Source & mimics，Initial package，PHR（CRT／DBP／lactate／vasopressor & fluid challenge），Septic cardiomyopathy、相關腦病變章段落。其 challenge、lactate 的較強主張保留為 expert interpretation，不當作 SSC guideline。
2. SCCM 官方 2026 recommendations `https://www.sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026`：直接核對 antibiotic 時限、source control ideally six hours、30mL/kg conditional low、NE comparison certainty、MAP 65/age>=65 60-65、serial lactate/CRT、inotropes、steroids、ARDS/bicarbonate/deresuscitation。
3. ANDROMEDA-SHOCK-2 原文 `https://jamanetwork.com/journals/jama/fullarticle/2840823`：n=1467、win ratio 1.16 (CI 1.02–1.33)、28 日死亡率 26.5% vs 26.6%（未見單獨死亡率獲益），區分 bundled intervention 與 isolated CRT。
4. Sepsis-3 original consensus `https://doi.org/10.1001/jama.2016.0287`；經編輯與來源頁互核定義，全文及附錄未獨立逐頁驗證。
5. van der Poll 2017 `https://www.nature.com/articles/nri.2017.36`，使用 host response 原理；原文非本輪全文逐段重核。
6. CLASSIC `https://www.nejm.org/doi/full/10.1056/NEJMoa2202707` 與 CLOVERS `https://doi.org/10.1056/NEJMoa2212663` 原研究摘要／結果，以臨床外推的限制為主，不使用未查核分組數據。

## Adversarial edit checkpoints
- 首輪後發現 first-use abbreviation gaps：CRT、NE、ARDS、MIC、AKI/RRT；已修正能定位者，應由不同脈絡再逐段檢查。
- 新版明示『Sepsis-3 操作性定義不應延遲治療』、感染與 shock mechanism 不互斥、IBCC 高裁量 challenge 不適合直接當個人醫囑。
- 指標被刻意拆開：BP/MAP 不是 CO，SpO2 不是 DO2，lactate 不是感染診斷，fluid responsiveness 不代表需要補液，CRT 目標研究未直接證實降低單獨死亡率。
- 未核原始圖像像素，未重製 IBCC 圖表；Mermaid 為自創定性關係，正式發布前須做手機圖像與文字後備驗證。
- **缺席事項**：尚無與寫作者分離的全文醫學／EPQC 逐段審查、真人專科審查、讀者學習效果測量、正式手機實測；不應將本次自身檢查偽稱 independent editorial approval。

## Status / release boundary
`DRAFT / HOLD`。未動 site/pages.json、正式 production、舊稿源或其他 PR。GitHub Actions 通過時僅代表工程完成，獨立語義 gate、權利與醫學驗收不因此視為通過。下一步優先做獨立段落審查，再以最小 diff 修正；不要擴張維護系統。
