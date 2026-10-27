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


## 2026-10-27 自評與五題真題回歸（不等於獨立審查）

### EPQC 七軸（同稿單輪模型自評）
| 項目 | 0–4 | 具體可見增量與缺陷 |
| --- | ---: | --- |
| A 命題與取捨 | 3 | 全篇圍繞感染→器官障礙→循環瓶頸→介入回饋，但 20+ 段落偏廣 |
| B 概念解混 | 4 | Infection／SIRS／Sepsis／shock、fluid responsiveness／tolerance／requirement、MAP vs CO、lactate vs infection 已拆開 |
| C 中介推導 | 3 | Glycocalyx/vascular tone→venous return/CO→organs，仍有部分免疫與病程的解釋跳幅 |
| D 證據決策 | 3 | SSC 2026 vs IBCC expert practice，ANDROMEDA-SHOCK-2 separate composite vs mortality；需獨立逐項醫學 QA |
| E 敘事連續性 | 2 | 虛構病例雖串起時序，19+ 節及多條公式仍使初學者切換負擔偏高 |
| F 臨床遷移 | 3 | 反事實含 PLR responsive 但 intolerant、MAP 達標 CRT 不佳、adrenal crisis mimic |
| G 語言與認知成本 | 2 | 多縮寫、英文與高密度段落，初學者的基礎導讀尚不足 |

合計 **20/28，約 71/100**，是嚴格但主觀的模型自評，不具對外醫學或教學驗證效度。內部 EPQC 逐軸至少 3、平均至少 3.3；E/G <3，故 **HOLD**。既有使用者要求公開品質至少 90 分，此版未達發布條件。

### 可以被真正測量的退稿理由
1. **E｜敘事分岔**：從微循環轉到靜脈容量模型、再到抗生素藥動學時，讀者可能忘記最初病例目前在等待哪項檢查。下版應減少章節切換並使用同一時間序列重構，但不可為修稿而省略重症必需內容。
2. **G｜認知成本**：使用 PHR、DAMP、stressed volume、DO2、AKIN 等術語時，先備知識雖多已補，但濃度太高。要對照初學者能否無教學者講出因果，不能只看寫作者是否理解。
3. **D｜來源與實例**：主案例為明示的教學虛構，尚未讓讀者完整看到有原始時間序列、POCUS/液體/升壓反應的真實 Sepsis case report；不能把合成患者冒充真實臨床研究。
4. **臨床安全**：PHR vasopressor/inotrope challenges 需要患者選擇與監測前提，寫有安全邊界但未完成獨立專家核查。帶有即時改藥效果的敘述不宜直接發布。

### 本輪新增國考真題
新檔：\`content/xiaoma-internal-medicine/exams/sepsis-core-112-114-med3.md\`。主文在 §4、§6、§8、§15 及專門考題小節建立向外連結；考題詳解亦連回 Sepsis 正文，**只是未發布的 Markdown 雙向連結，不等於已測過公開網站的雙向連結**。

| 考選部真題 | 官方原始答案 | 更正狀態 | 教學焦點 | 來源 |
| --- | --- | --- | --- | --- |
| 112-1 醫學（三）33 | A | 該題未更正 | IL-5 vs TNF/IL-1/IL-6 | official 112020 Q/S/M |
| 112-1 醫學（三）64 | D | 該題未更正 | 海水、肝硬化、Vibrio vulnificus、source control | official 112020 Q/S/M |
| 113-1 醫學（三）48 | B | 本科該題未更正 | bicarbonate 不可當首要目標 | official 113020 Q/S |
| 114-1 醫學（三）51 | B | 該題未更正 | SVR: distributive vs cardiogenic | official 114020 Q/S/M |
| 114-1 醫學（三）57 | C | 該題未更正 | Sheehan/adrenal crisis，採檢不延誤 hydrocortisone | official 114020 Q/S/M |

正式官方頁：
- 112-1 https://wwwq.moex.gov.tw/exam/wFrmExamQandASearch.aspx?e=112020&y=2023
- 113-1 https://wwwq.moex.gov.tw/exam/wFrmExamQandASearch.aspx?e=113020&y=2024
- 114-1 https://wwwq.moex.gov.tw/exam/wFrmExamQandASearch.aspx?e=114020&y=2025

已用官方「醫學（三）」答案圖頁核對：112 標準 A33/D64，112 更正只有 47 與本次無關；113 標準 B48；114 標準 B51/C57，更正只有 23、42，與選用題無關。官方題目本文在 Repository 的五年 \`structured/\` 擷取可回查；114 Q51/Q57、113 Q48 另由官方 PDF 文字確認題意。因官方 PDF 題目頁的網頁 screenshot 服務部分回報 cache miss，**不可宣稱所有題目原像素目視核對完成**；本輪五題皆是無原附圖的文字題。題面以「重述」呈現，官題、官方答案與 2026 指南需分開。

### 結論
- **能確認**：PR 上已保存深度新版與真題詳解，並且有相互 Markdown 連結，官題答案與更正情形已依上述查核。
- **不能確認**：獨立審稿已完成、正式站題頁可點開、手機版已通過、真實讀者能更快理解。
- **仍然 HOLD**：E/G 未過內部 EPQC，並無獨立醫學審查；不把自評寫成審稿完成或為了擺放國考題直接改 site/pages.json。
