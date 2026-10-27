# PGY 心血管講義｜Clinical OS 編輯校準（開發回歸集）

日期：2026-10-23｜**Artifact / exploratory pilot / NOT VALIDATED / publication HOLD**

## 目的與邊界

這是對第三方《PGY職前加油站：胸痛與心血管值班急症講義》（黃品叡醫師，20 頁）做的**教學設計觀察及局部醫學查核**。來源 PDF 由使用者提供，**不提交原始 PDF、不複製第三方圖像、不放進公開站點**。已核對 PDF 頁面文字及相關流程圖／表格（尤其 pp.13–17）；部分正式指南核對到文字與 Recommendation Table，不代表講義 20 頁都已完成醫學 QA，也不代表已核對 Pocket Medicine 的相同主題。

**收斂而不是增生規則**：編輯品質採既有 [EPQC](../../docs/editorial-prose-quality-contract.md)；證據／原稿版本與 A/B/C/D/X 採 [統一契約](../../docs/clinical-os-integration-20261021.md)；臨床書圖採 [來源擴充規範](../../docs/xiaoma-evidence-expansion.md)；效益宣稱依 [實驗登記](../README.md)。本文件只保存不能可靠憑空重現的來源定位、差錯實例與對照測試。**不要把護理站電話 SOP 變成所有文章的模板，也不要因為案例庫增加而宣稱模型接受了訓練或能力已被驗證。**

## 可轉移的編輯判斷

第三方講義的優點在於把「當下要決定什麼」明確放在知識之前：值班觸發 → 致命／穩定性分流 → 真正會改變行動的資訊 → 安全界線 → 下一次評估。小麻閱讀的任務更進一步：先保留作者已存在的概念推導，再補足必要的生理機轉與臨床反例，不把長文寫成口訣集。

在真正改稿前，優先判斷：
- **A 已寫清楚／K keep**：保留，不能為了顯得有新意而重構。
- **B 有橋但跨篇未連接**：補導航或局部銜接。
- **C 真正缺少中介**：補因果橋、分支圖或最短必要文字。
- **D 條件或例外失真**：局部替換，保持原稿正確的臨床主張。
- **X 無法核實**：列待證，不能升格為「已修正」。
在檢出每一個問題後，先提出「原文也可能只是合理簡化」的最強反方；以原始 Figure／Table、相關指南及反事實測試決定最小充分修訂。輸出以 `keep / annotate / minimal_patch / restructure / defer` 分流，並量測沒有必要的修改。

## 本次可回歸案例（非盲測）

| ID／來源頁 | 原文主張的問題 | 分類 | 最小充分修訂 | 狀態 |
|---|---|---|---|---|
| CV-01 p.14 | AF 提及轉律前 24h 條件，卻未充分分開轉律後 OAC 與長期預防 | C/D | 在既有段落後補 **pre / post ≥4 weeks / long-term stroke risk** 三層；例外須確定 AF <24h 且無血栓危險因子 | 已查指引，待獨立醫學 QA |
| CV-02 p.14 | 「瓣膜性 AF」作為 DOAC 例外過於寬泛 | D | 把例外精準限於機械瓣與中重度 MS；保留其他瓣膜病符合條件時可用 DOAC 的原則 | 已查指引，待 QA |
| CV-03 p.17 | pericarditis + troponin 上升 → 一律「照心肌炎處理」 | C/D | 補 IMPS 的診斷和風險分層；NSAID+PPI 對伴心包炎症狀者、colchicine 對 myopericarditis 有條件可考慮，不能以 troponin 決定全部處置 | 已查指引，待 QA |
| CV-04 pp.15–16 | 高風險 syncope 標題直接聯結住院／監測 | D | 改為「需快速評估／可能需監測或住院」；補 ED observation／fast-track vs admission 的條件 | 已查指引，待 QA |
| CV-05 pp.13–14 | pre-excited AF 的 AV nodal blockers 警示 | A/K | **原文保留**；禁止 AI 不必要改寫 | 負對照 |
| CV-06 p.16 | 「任何暈厥都要血糖」屬 SOP 安全檢查 vs 指南必要檢查的層級差 | B/D-light | 不列重大醫學錯誤；僅釐清它不是 ESC universal guideline mandate | 負對照／措辭候選 |

**重要細節**：CV-01 不能把「AF 確定 <24h」單獨寫成可省略後續抗凝；還要**沒有 thromboembolic risk factors**。CV-03 不應反過來把 NSAID 寫成適用所有心肌炎，需顧及心衰／腎功能／出血風險。CV-04 也不等於「所有高風險暈厥可回家」；觀察環境必須能監測與搶救。

## 醫學證據定位（2026-10-23 再核）

- 2024 ESC AF guideline：cardioversion pre-OAC / TOE、postcardioversion OAC ≥4 週／少數例外、長期預防三者分立；DOAC 例外：mechanical valve 或 moderate-to-severe MS。`https://academic.oup.com/eurheartj/article/45/36/3314/7738779`
- 2025 ESC myocarditis/pericarditis Recommendation Table 9：伴心包炎症狀之 myocarditis 可考慮 NSAID + PPI（IIa/C）；myopericarditis 可考慮 colchicine 預防復發（IIa/B）。`https://www.escardio.org/static-file/Escardio/Guidelines/Products/Slide%20sets/2025/2025%20official%20slides_MyoPeri.pdf`
- 2018 ESC Syncope guideline Table 7：high risk disposition 要區分 ED observation／syncope unit fast track 與 inpatient admission。`https://academic.oup.com/eurheartj/article/39/21/1883/4939241`
- 2023 ACC/AHA AF：pre-excited AF 應避免 AV nodal blockade；此項保留原文。`https://pmc.ncbi.nlm.nih.gov/articles/PMC11104284/`
- 2025 AHA Tachyarrhythmia Algorithm：辨認「tachyarrhythmia *causing* instability」與代償性 sinus tachycardia，適合作為**另一個已曝光的**回歸案例。`https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/algorithms/`
- 2026 Fifth Universal Definition of MI：acute myocardial injury ≠ MI，且**2026 新分類為 primary／secondary／procedure-related**；不能沿用舊「Type 1/2」字眼而不註明版本。`https://www.jacc.org/doi/10.1016/j.jacc.2026.07.025`
- 2026 ESC HF guideline 已發布：需在每篇 HF 的指定論點逐項做新舊差異，不能只因新版存在就宣稱舊教材全錯。`https://www.escardio.org/guidelines/clinical-practice-guidelines/all-esc-practice-guidelines/heart-failure`

## 修稿規則（最小，不重複 EPQC）

1. 先比對原文句、圖、腳註、前後章已存在的說明；先對原稿做最強反方辯護。
2. 限定論點層級：觀察／病因／風險／診斷／適應症／行動後追蹤；特別找**風險→住院、marker→處方、轉律前→轉律後**等被壓成一層的跳躍。
3. 每個重要新增概念都需要「原稿缺哪個不可省略的中介」「資料如何影響分支」「條件改變是否改判」；清晰但無新意時可判 A，不能搶占原作者貢獻。
4. 只改必要句段或補一張真正能解決混淆的圖。醫學 P0/P1、來源與權利未解即 HOLD；發布必須走既有出版閘門。

## 實驗地位與污染風險

**本對話已展示上述全部候選問題、來源、補丁與 gold labels。先前名為 `Blind_Prompts` 及 `Heldout_Eval_Cases` 的檔案全數重新標記為 development/regression data；即使對受試模型隱藏答案，也不能再把它們稱為「對該模型從未曝光之 holdout」。** 本次沒有 Native／Evidence-only／Lite 三臂隔離執行，也沒有獨立 reviewer、計時或臨床學習結果。故結論僅能是 Artifact + exploratory pilot，不能宣稱自主編輯能力提升。

想測**真正增量**，應從新的未公開教材與陌生主題建立獨立封存題，採同模型、同來源圖表、同工具／effort／預算，分離三臂上下文，盲審「重要錯誤與漏修、無謂修改、證據準確性、最小修訂、人工總分鐘數」，並記錄 P0/P1 與成本。若 Lite 只提高修改量、不增加安全的真實增量，回退到 Native + evidence gate。

**交付邊界**：僅建立本實驗素材，不修改作者 originals、公開內容、`site/pages.json`、模型權重、CI 或 Cloudflare。合併 PR、工程測試、醫學 QA、對照驗證與網站發布須分別報告。
