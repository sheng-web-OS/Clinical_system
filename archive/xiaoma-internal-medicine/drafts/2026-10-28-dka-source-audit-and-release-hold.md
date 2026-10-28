# DKA/euDKA 先行教材｜來源與審稿交接（私人；不得入公開正文）

- 對應 [Curriculum Gap #198](https://github.com/sheng-web-OS/Clinical_system/issues/198)
- 首稿：`archive/xiaoma-internal-medicine/drafts/2026-10-28-dka-euglycemic-case-first.md`
- 目前狀態：**FIRST_DRAFT / MEDICAL_REVIEW_HOLD / FIGURE_REVIEW_PENDING / NOT_PUBLISHED**。不得把稿件存到 `site/pages.json`，不得關閉醫學獨立審查 gate。
- 主要價值判斷：A級高危急症。114-1 醫學（三）Q56 只有跨系統題解；現有酸鹼與高碳酸/NIV文章未建立完整 DKA/euDKA 生理、診斷、insulin/K/dextrose 與緩解終點的全篇論證。

## 具體已核的原始來源（不把文字擷取冒充圖像審查）

1. Cai J, Fu T, Tan C. `Case Report: Early-onset euglycemic diabetic ketoacidosis following henagliflozin initiation in a treatment-naive patient`. *Front Endocrinol* (Lausanne). Published 2026-07-07;17:1882272, DOI `10.3389/fendo.2026.1882272`. 官網全文 `https://www.frontiersin.org/journals/endocrinology/articles/10.3389/fendo.2026.1882272/full`。實際讀回 publisher 正文 Case presentation、Treatment and clinical course、Table 1 數值與表題、Figure 1 的說明文字、Table 2 的比較及 limitations 相關敘述。**並未看原圖像像素；Figure 1 圖像本體仍待視覺/權利核查，不能宣稱已看圖。**
   - 40F newly diagnosed DM, initial fasting glucose 17.9 mmol/L, HbA1c 12.9%, started metformin+henagliflozin+chiglitazar. GI symptoms first 24h, minimal intake to day4, somnolence with BP110/70, HR108, RR22.
   - Day4: glucose 8.5 mmol/L (153), BHB 5.6, pH 7.043, HCO3 6.5, pCO2 24.4, AG28.4, lactate2.01, K4.66.
   - Day+24h: glucose6.7, BHB4.8, pH7.223, HCO3 12.1, AG17.5, K3.82.
   - Day+72h: glucose5.9, BHB0.3, pH7.356, HCO3 16.8, AG13.6, K3.95. Discharge day8; no SGLT2 restart.
   - **原始資料可能不一致須人工確認**：Table 1 把 creatinine 62.3、67.5 等標成 `mmol/l`，很可能單位標示有誤，本文已**刻意不複製這一列**。另外同文 Table 2 將主病例嚴重度欄列 `Moderate (No ICU)`，與初始 HCO3 6.5 (<10) 的2024生化 severe 門檻不完全一致。不要不加查核自行採用該分級；處置場所仍需依全人評估。
   - **因果界線**：作者將嘔吐歸因於 metformin，但病例同時開始三藥、有嚴重基礎 hyperglycemia、禁食與容量不足；不能用單例證明 metformin 是唯一因果，也不能證明特定 SGLT2 藥的事件發生率或一般最佳處方。
   - **酸鹼獨立警訊**：以初始 HCO3 6.5，Winter ≈ 1.5×6.5+8=17.75±2；同份ABG記錄 pCO2 24.4，高於預期。正文正面標示「不是代償必然足夠」，但不能把它當成已確診混合性呼吸酸中毒。需由獨立醫學 reviewer 核對原始血氣、使用 Winter 公式的適用限制、真正臨床意義和後續的通氣處置。此項在 reviewer 前為 **MEDICAL_CHECK_REQUIRED**。

2. Umpierrez GE, et al. `Hyperglycemic Crises in Adults With Diabetes: A Consensus Report`. *Diabetes Care*. 2024;47(8):1257–1275. DOI `10.2337/dci24-0032`; `https://pmc.ncbi.nlm.nih.gov/articles/PMC11272983/`、`https://diabetesjournals.org/care/article/47/8/1257/`、`https://link.springer.com/article/10.1007/s00125-024-06183-8`。
   - 官網可檢全文診斷 D/K/A：D 已知 DM 或 glucose≥200；K BHB≥3 或 urine ketone≥2+；A pH<7.3或HCO3<18；euDKA glucose<200。真題舊門檻不同，不能混用。
   - treatment：一般 IV insulin≈0.1U/kg/h（某些輕度無併發症可每1–2h SC短效類比）；glucose<250加5–10% dextrose以繼續 insulin；K<3.5先替代並暫緩 insulin；bicarb非例行，嚴重pH<7.0可考慮；monitor BG1–2h、其他labs及BHB每約4h（依院內情境）。
   - Resolution：**BHB<0.6** 且 **pH≥7.3 或 HCO3≥18**，最好glucose<200；AG不作唯一緩解標準，高Cl代謝酸中毒可干擾。從IV到SC basal至少1–2h重疊。
   - **原始共識 Figure 1,2/Table 2,3 的可視畫面／註腳仍待獨立 reviewer 逐圖比對**。這次只核正式文字/HTML的表格記載，沒有拿 Table/Figure 截圖說已人眼驗畢。

3. American Diabetes Association. `Diabetes Care in the Hospital: Standards of Care in Diabetes—2026`. *Diabetes Care*. 2026;49(Suppl 1). DOI `10.2337/dc26-s016`; `https://diabetesjournals.org/care/article/49/Supplement_1/S339/163925/16-Diabetes-Care-in-the-Hospital-Standards-of-Care`。搜尋與官方摘要驗證2026 DKA criteria 表16.1及 SGLT2相關euDKA，**publisher全文抓取受到403，不能宣稱已完整讀 Table 16.1 畫面/附註**。後續盡量取得合法全文及原表，無法取得就維持來源限制或先以已開放的2024共識為門檻證據。

4. 現存官方真題 `114 年第一次 醫學（三） Q56` canonical `content/xiaoma-internal-medicine/lessons/2026-10-22-baseline-twenty.md` 第15題：main 已載 B 是錯誤的「1U/kg regular insulin single bolus」及逐選項解釋；對應來源 `archive/xiaoma-internal-medicine` 與 `content/xiaoma-internal-medicine/baseline-sources.md`。**本次未再次逐頁目視考選部原卷更正表**，故 PR 不能聲稱已完成官方答案獨立核驗。

## 編輯完整性與閘門

- **Article-first**：「為什麼 glucose<200 仍能產酮到危急？insulin要抑的是什麼？怎樣避免補糖與鉀的治療矛盾？何時才真正解除危機？」為唯一中心。不把 DKA 題型表列強行塞入既有 acid-base，正式文只在末段對應一題。
- 必須由不同 writer 的 reviewer 開啟原始病例圖 1、Table1/2、共識原圖/表；檢查生理機轉是否過度確定性、Winter公式與臨床 implication、每個治療分支與2024/2026 guideline 原文，避免直接由病例藥量變成台灣院內醫囑。
- 待補：獨立審稿封包/EPQC逐段七軸、醫學安全獨立QA、口語/段落重複與內部metadata混正文清理、原始Figure/Table/caption/footnote核對、是否需要原創定性機轉/時間線圖（圖不應依權利不明的原像素重製）、手機與桌機reader、目錄雙向連結及真題身份唯一檢查、CI/build/Cloudflare同SHA實際核驗。
- **發布界線**：目前只新增 `archive/.../drafts` 私人草稿，不在 `site/pages.json` 登錄、不當新發布、不可合併，直至完整門檻過關。源文章原版指紋不動；嚴禁在公開正文提「審稿通過與否」或此私人補件。

## 下一個最低成本但有價值的工作

1. 獨立reviewer先核本篇最敏感的四項：初始ABG / Winter、guideline 2024 DKA resolution、K<3.5 暫緩insulin、2026 official Table16.1/原Figure。
2. 修正文中 0–1 項可驗證 P1（例如原始 source 數值誤寫）後用完整 EPQC 逐段檢查病例時間線；確認不需要再增加不服務主題的表格。
3. 上述全過再升為新的正式 `content/.../lessons` 文章及來源頁；#112 Work owner 才會在同一國考/atlas邏輯加適當導航，不能另寫平行 mapping 程式。


## 2026-10-29｜病例證據重新核讀與正文修訂（本輪編輯者複核；非獨立醫師審查）

- 正文 blob SHA：`39697f89731bdfcb7ffbb7fc195e8d319f16ca6b`，commit `ac8f5e435962be7f6edcd89c83af20202a244a52`。從原稿的單一路徑敘述，增補「初始病況 → 競爭病因（飢餓、乳酸、腎/毒物、DKA）→ 實際檢驗的鑑別作用 → 治療與連續重評」。保留真實 case 與 guideline 不同證據角色，不使用合成量測或取代已發行考題。
- 本次重新讀取原始 publisher HTML Case presentation、Treatment、Table 1、Table 2 和參考說明。**已直接顯示並目視 Cai 2026 Figure 1 原圖影像**（官方檔案 `https://www.frontiersin.org/files/Articles/1882272/xml-images/fendo-17-1882272-g001.webp`）：內容是糖尿病診斷、首次症狀、入院、住院治療與追蹤的時間線；不是檢驗值圖表。讀者稿只連結官方圖，不重製。Figure 1 caption「Timeline of the disease course」，Table 1 caption「Patient characteristics across different treatment phases」。**此範圍是本輪作者源查，不等於所有原圖/註腳、版權與醫師 QA 完成。**
- **新增原文→解釋界線**：原病例 CT 胸/腹/腦未見急性異常，妊娠檢驗陰性、無酒精/毒物暴露病史，僅可描述該病患實際排除步驟；不推廣所有 DKA 患者須做多部位 CT。原病例治療記載 0.9% saline、10% dextrose、0.1 U/kg/h insulin、確認尿量後鉀補充及頻繁測試；這是當例處置紀錄，不是台灣院內可照抄 order。
- 2024 Umpierrez 共識 HTML Fig 2 caption、Table 2 重症度欄與附註、Fig 4 caption 及正文鉀、補 bicarbonate 與 resolution 再讀。Table 2 不能機械以單欄定級：本例 pH 7.043 落 moderate pH 範圍，但 bicarbonate 6.5 落 severe 警訊且嗜睡；收治需求依全人評估。原病例 Table 2 的 Moderate (No ICU) 與極低 bicarbonate 並存，已於正文揭露，不替原始作者作事後更正。
- Winter 公式 1.5×6.5+8=17.75±2，實測 PaCO₂ 24.4。以 Henderson–Hasselbalch 粗算 pH≈7.05，與報告 7.043 相容；公式異常不當作已證實混合呼吸衰竭。仍須醫學獨立 QA，檢查是否應更明確定位呼吸性酸化成分。
- **2024 guideline pH<7.0** 為可考慮 bicarbonate 的嚴重 DKA 情境；原病例使用 pH>6.9 的表述，不能冒稱與新版字面一致。正文未宣稱此例需要 bicarbonate。
- DKA resolution 使用血酮<0.6 且**venous pH**≥7.3 或 bicarbonate≥18。病例 72h 是**arterial pH** 7.356 和 bicarbonate 16.8，β-OHB 0.3；應寫「個案作者記載已緩解，生化數據支持大幅改善」而非補造 venous pH 證成逐字吻合。Basal–IV overlap 在原文未載精確時間，不可反推有確切 1–2h 重疊。
- 原始 Table 1 的 creatinine 單位疑點仍存在，該列未用於正文推論；2026 ADA publisher Table 16.1 有可搜尋之官方頁面文字摘錄，但非完整原圖視覺核實。2024 共識 Figure 2/4 原圖連結在本次 browser 受存取挑戰阻擋；**不標示獨立視覺查核通過**。
- 本輪只做一個作者脈絡下的事實與論證複讀。尚缺異作者/醫學獨立審查、EPQC 全段落與 continuity gate、正式考選部原題與更正表目視、重要 Figure/Table 權利確認、讀者手機 preview/CI/正式站驗證。因此 `MEDICAL_REVIEW_HOLD`、`FIGURE_REVIEW_PENDING`、`NOT_PUBLISHED` 不變。沒有修改 `site/pages.json`。
