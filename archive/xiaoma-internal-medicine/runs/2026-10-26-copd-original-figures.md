# COPD｜小麻四張原圖與對讀修補稿（私人）

狀態：**四張原圖已擷取及目視；公開補圖 HOLD。** 使用者原話：「你如果在小麻發現原圖要使用小麻的圖表」。本次把原圖優先寫入既有出版／EPQC／深度規範；不增加新平台、圖庫登錄系統或排程。

公開稿內容版本仍為 5d93f623cf1641818bce7ccd660391d0ecaf7176，驗證紀錄提交 35e9652a60af8ac723f3e11d5c49794f1942cd08。它曾通過當時結構門檻，**不代表已呈現小麻原圖，也不能說符合本次原圖優先的新要求**。本次不重複出刊、不覆蓋歷史原稿，不改公開教材或把私人摘圖列入 site/pages.json。

## 來源、擷取與公開界線

來源為使用者提供的 Pocket Medicine 9E flattened PDF，464 個 reader pages，SHA-256 `ad283f7db19b6575775341972360a5ca1e5b40f51383ce02d9c11c8d21a0b3c5`。只擷取當前 COPD 推理對題的四張圖／表，沒有發布原書 PDF 或完整章節。原圖只作畫面邊界裁切，不使用 AI 重生成、不替換文字或暗改符號；標題、完整欄位／分支及可見註腳保留。

擷取以 Poppler pdftoppm 的原 PDF render 為準：`-scale-to 2400`，crop `(x, y, W, H)` 分別為 p80 `(210,210,1440,840)`、p85 `(205,535,1440,565)`、p86 `(205,210,1440,305)`、p87 `(205,210,1440,1805)`。四張新 PNG 只放私人 archive，不在公開白名單。

本次使用者要求是選用原圖的編輯決策；沒有查得可證明出版社對本公開站重製這四圖的獨立授權，也沒有作合理使用等法律認定。因此不把取得書檔、使用者指示或既有另兩張圖片的上站事實當成權利已確認；公開補圖先 HOLD，不以重繪／GOLD 連結填平此缺口。以下私人稿可直接閱讀原圖，並準備好日後合法公開時的安置與安全註記。

## 1. PFT 原流程：先辨認量測問題，再沿 COPD 分支走

![Pocket Medicine 9E PDF p80 原始 PFT 流程與 race-neutral 註腳](../source-figures/copd-20261026/pocket-medicine-9e-fig2-1-pft.png)

**原圖：Approach to abnormal PFTs（Figure 2-1，圖位於 reader PDF p80）。** 圖下 race-neutral reference equations 註腳一併保留；相鄰 p79 的 PFT 說明仍應對讀。開啟圖片可看 1440 px 原尺寸，這不是 AI 重排的圖。

安置：主文 02 的 LLN／固定 ratio 討論後。帶讀時先分 FEV₁/FVC、TLC、DLCO 三個問題，再看左側阻塞分支；有 bronchodilator response 不單獨證明氣喘，minimal response 也不單獨證明 COPD。右側 TLC <80% predicted 是原圖的固定百分比簡化，不能取代適用參考式的正常下限。來源補查 [ERS Spirometry Resources Centre 的 Interpretation](https://channel.ersnet.org/media-113710-interpretation)：實讀 Assessing normality、Classification of ventilatory impairment 及 Table 1 的官方 HTML，確認低 FVC 需 TLC 釐清、低值以 LLN 定義；未讀到 ERS/ATS 2022 正式文章全文（403），不冒稱完整核讀。

PNG SHA-256：`ba2c8227a38703adcf3e018bb02ed32242bbb0e3f0ff3736d34d44b0307e9795`。

## 2. 肺氣腫／慢性支氣管炎：保留原表，拆開它的定義軸

![Pocket Medicine 9E PDF p85 Emphysema vs Chronic Bronchitis 原表](../source-figures/copd-20261026/pocket-medicine-9e-copd-definitions.png)

**原表：Emphysema vs. Chronic Bronchitis，reader PDF p85。** 保留 Definition、Pathophysiology、Clinical manifestations、Physical exam 四列及兩欄，沒有只摘定義而藏掉後面的簡化。

安置：主文 01 的定義對照前。先讀 Definition，肺氣腫是結構／病理描述，慢性支氣管炎是症狀時間描述；兩者不是互斥的 COPD 階段。最後列的 pink puffer／blue bloater 不用作診斷二分或氧療／呼吸器指示。原表的 V/Q／shunt 文字不能擴張成「每個慢性支氣管炎病人都有 true shunt」；必要解混應留在原圖旁，不藉自製表把原表藏掉。

PNG SHA-256：`28b77d730a1d013deb71c0a9c6258a36fa233779f3d6a961a995f53724dab95e`。

## 3. 原書分組表：原像素保留，旁註版本差異

![Pocket Medicine 9E PDF p86 COPD Staging and Recommended Therapies by GOLD Criteria 原表及註腳](../source-figures/copd-20261026/pocket-medicine-9e-copd-gold2024.png)

**原表：COPD Staging and Recommended Therapies by GOLD Criteria，reader PDF p86。** 保留標題、兩種症狀欄、事件次數列及戒菸／疫苗／肺復健／氧療註腳。前一頁 p85 的 Chronic treatment 明示 adapted from GOLD 2024 Report。

安置：主文 04 的初始／follow-up 區別後。圖前就要標示「原書採 GOLD 2024，這不是 2026 現行分流表」。原表所印 <2／≥2 是壓縮表示，不當完整歷史指南；GOLD 2026 原 Figure 2.13 的 E 為前一年至少一次中度或重度惡化。不能暗改舊圖的數字來偽裝原圖更新，也不能只放 GOLD 圖卻聲稱用了小麻原表。現行判斷仍依主文及其已實查 [GOLD 2026 官方 Pocket Guide](https://goldcopd.org/wp-content/uploads/2026/01/GOLD-Pocket-Guide-2026-v1.1-20Nov2025_WMV2.pdf#page=22)。

PNG SHA-256：`8cfede998cbfb56f8449b798e23f9f4759c10e995d3c1767ba970a314325e05f`。

## 4. 急性惡化原表：藥物與器官支持不是同一條加量階梯

![Pocket Medicine 9E PDF p87 COPD Exacerbation Treatment 原表，保留全部三欄及照護列](../source-figures/copd-20261026/pocket-medicine-9e-copd-exacerbation.png)

**原表：COPD Exacerbation Treatment，reader PDF p87。** 保留 Agent／Dose／Comments 與 Oxygenation、NIV、Endotracheal intubation、Other、Post-exacerb care。這張原表不能被一張只畫呼氣曲線的自編圖取代；曲線只能補它未展開的力學。

安置：主文 05–06 的支持與急性治療交界，圖前即列限制：原表較大劑量 IV methylprednisolone 不是本篇的一般建議；GOLD 2026 的一般 short course、口服條件與病人監測仍按主文限定。NIV 列的特定研究與高／低強度潮氣量，不轉成所有 COPD 病人的固定設定。

**來源疑義，不暗改原圖：**截圖 Corticosteroids comments 印有「Consider limiting use if eos ≥2%」並引 Lancet Respir Med 2024;12:67。對回 [STARR2 目前 PubMed 摘要](https://pubmed.ncbi.nlm.nih.gov/37924830/)，其 BET 組在 eos ≥2% 給 prednisolone、<2% 給 placebo；這與按原表字面把 ≥2% 當限制用藥條件不能直接相容。本次只核讀摘要的方法與設計，不冒稱取得全文或已完成其更正全文核對；PubMed 列有 [correction](https://pubmed.ncbi.nlm.nih.gov/38030376/)，本次完整讀取受限。此符號／字句必須標為疑義，不作停用 steroid 的醫囑，不用自改一個不等號來假裝已確定出版社筆誤。現行公開主文並未採用這句作急性 steroid 門檻。

PNG SHA-256：`62b7fdd002a0bf3e26c125e9187d4c5bfab6fc1a19d484660038e679a5a60806`。

## 本次精確完成與未完成

完成：四圖直接原 PDF 擷取、逐圖目視標題／分支／註腳；原圖優先規範寫回既有四個文件；私人原圖對讀稿與來源疑義保留。沒有更動歷史小麻原稿、公開圖資白名單或 figure gate 執行器，沒有把既有 represented 改作新的像素／權利證明。

未完成：四圖的公開使用依據、p87 引文／更正全文的最終判讀、公開頁補圖、該新版本的手機與 HTTPS 驗收。這些不能被先前 61 tests、CI 成功或 5d93f6 內容版本已部署取代。原圖擷取屬讀取／保真工作，不是新增醫學推薦，也未經獨立醫師審查。

下一步：取得可核實的公開使用依據後，把四張原圖放在上述相鄰正文位置，保留原創機轉圖作補充；逐圖核查原尺寸連結與窄版，不以圖片數量代替可讀性。p87 的未解字句維持原像素加明確警示，未釐清前不形成新的臨床規則。其他 A/B 覆蓋仍依現行雙考期安排，不因這個權利 HOLD 宣稱整個教材任務停擺。

本機驗證：`bash tools/build_site.sh` 通過，白名單與私人資料邊界通過；`python -m unittest discover -s tests` 重跑 61 項通過。初次測試因新環境缺 mistune 失敗，沿原 build 安裝固定依賴後重跑，沒有改測試或降低門檻。四份 PNG 與私人對讀稿未進入 dist；本次公開教材 HTML、目錄與搜尋內容未改動。這不是四圖公開發布或獨立醫學審查的驗證。

## 續修：原圖嵌入完整主文與橋接（2026-10-26）

使用者接續要求：「好，鑲嵌進文章，並補上橋接與說明」。以 main `cb74539339abf0927eacccbb796ea0163a02a5e4` 的原主文 blob `3c2b6eed24181df73a8818435f7cb9b645266fae` 為底；在獨立 `editorial/copd-originals-bridges-20261026` 分支保存未發布修訂，不覆蓋正式頁面或原始作者文章。

- [完整整合 Markdown](../drafts/2026-10-26-copd-originals-integrated.md)：保留七節主線、真實病例測值、兩張原創 SVG、兩張概念表、兩道自編遷移題與三個正式題入口；四張小麻原圖各有實際 img、caption、原頁定位及前後解讀，不是附錄或單純圖庫。
- [可直接閱讀的單檔 HTML](../drafts/2026-10-26-copd-originals-integrated.html)：沿用既有 reader，四張原圖內嵌而不依賴登入／外部圖片服務；可點圖開啟原尺寸、水平／垂直捲動並回到原段落。這是私人下載稿，不是 Cloudflare 正式頁。
- [實際本機檢查紀錄](../drafts/2026-10-26-copd-originals-integrated-qa.json)：區分 viewport／互動、原圖 byte 保真與公開部署狀態。

本輪橋接為 B（將原表連回主文已有知識）與 D（限制圖中簡化／舊版推論），不認領為新的科學發現：

1. **01 原表 Definition → 功能診斷**：由結構性肺氣腫、時間性的咳痰定義，引出 COPD 的功能條件，說明兩欄可重疊；不以 pink puffer／blue bloater 或 shunt fraction 字樣直接分配診斷／支持。
2. **02 原流程起點 → 病因資訊**：先看 FEV₁/FVC、TLC、DLCO 各測什麼，再說 bronchodilator response／低 DLCO 不能取代病史與阻塞證據；原圖 TLC <80% 與適用參考式 LLN 的差別留在圖旁。
3. **04 原表橫縱軸 → 現行治療決策**：辨認日常症狀與前一年事件，和 FEV₁ 分級分開；補上 mMRC 的活動限制與 CAAT 的生活影響意義，不讓量表只有縮寫。原書採 GOLD 2024 的壓縮表先加警示，再對回 2026 E 與 follow-up，回到開場病人已三合一仍喘的剩餘機械問題。
4. **06 原表 Agent／Dose／Comments → 多個支持終點**：藥物、氧合、通氣與氣道安全不是固定逐列加量；有氣道／循環危險時不等待試完所有藥。高 IV steroid、eos ≥2% 字句與 NIV 研究設定均限定，不盲抄成通則。

醫學新增範圍：本輪再次目視四個原 PNG，保留原像素、欄位與註腳；沒有改動病例測值或正式答案。ERS 官方 Interpretation 的相應 HTML 是 LLN／低 FVC→TLC 的對讀來源，不冒充已取得 ERS/ATS 2022 論文全文。STARR2 的分派描述沿用前段已核讀的 PubMed 摘要；本輪連線未取得完整摘要頁與更正全文，未冒稱重新通過全文核對。eos 字句仍是明示的來源疑義，不用於停用急性 steroid，也不自行修改原圖不等號。

AI 同脈絡對抗式複讀：A3（同一排空命題，原圖使閱讀負荷增加，仍分次讀）、B4（四張圖各拆不同軸）、C4（圖前問題→分支意義→病例／處置，而非圖名後貼摘要）、D4（版本、測量與來源限制就地限定）、E3（七節與病例主線保留，未改成圖卡集合）、F4（原遷移題連回原表並補四個遮圖回想問題）、G3（查核留此紀錄，正文只保留會改判的限制）。平均 3.57，屬內部篩選，不是原作者認可、隔離盲審、獨立醫師審查或與 ACS／HCM 非劣效實證。

工程與閱讀：原網站 build 與 61 tests 通過，證明原公開輸出邊界未破壞，不等同驗收本私人稿的醫學內容。私人 HTML 另在本機 Chromium 實測 320／390／768／1440 px × 預設／24px-dark 共八條件，正文及八個 figure 無水平溢出，單一 H1、七節與錨點完整；四個原圖實際開啟／關閉放大、可捲到右／下邊界與返回焦點，支援鍵盤捲動和 Escape；兩個答案開合實測。四份內嵌 PNG 解碼後 SHA-256 與原摘圖完全一致。首次測試在 lazy image 尚未進入視野前檢查 naturalWidth，已修正測試為實際捲入視野並完成 decode，未把測試時機誤判為圖檔遺失。

已目視四張窄版圖與放大表格，字型環境補妥後再測；不是實體 iPhone／Safari 測試。閱讀預覽的 CSS／小型原圖放大器只存在私人 HTML，沒有修改共享 runtime、來源 gate、公開白名單或部署設定。私人 HTML／來源圖片不進 dist。

目前狀態：**完整私人文章已嵌圖與補橋接；公開修訂仍 HOLD**。前段「把圖放進主文」這一步已在本私人版本完成；原圖的公開使用依據與 p87 引文／更正全文仍未完成，不以本機工程通過宣稱可以正式部署。原公開版本保持不變，也沒有將本次修訂當成另一篇每日出刊或讀者精熟證據。

## 續修 V2｜敘事重構與病例圖（2026-10-26）

使用者最新反饋：「很不老練、有點冗、文字讀起來很想睡覺」。同一 PR 分支改寫原 Markdown；**未另外創建每日新文章**，不覆蓋作者認可原稿與公開頁。

- 主線改為「排空限制 → 過度充氣／可動用容量 → 症狀與惡化分軸 → 急性換氣失敗」；仍維持 01–07 七節，前四節聚焦門診與力學，後兩節接急性器官支持，末節回扣病例和反事實題。
- 明確用同一 Marchand 2019 Table 1 的 After PR vs 1 month post-EBV 結果：TLC 6.75→5.84 L、RV 5.19→3.36 L、FEV1 0.85→1.67 L、FVC 1.31→2.40 L、六分鐘步行 340→399 m；新增 FEV1/FVC 表列 0.65→0.70 的精度警示及三年五次門診抗生素治療惡化，禁止把作者用語 cured 推成結構治癒。
- 增加原病例 CT Figure 1 四格圖片（Marchand et al. 2019，doi:10.3390/medicina55030065，CC BY 4.0 授權，連結外部原檔，不重繪），與原書四張小麻圖片不同，版權可逐來源辨識。
- 保留四張 Pocket Medicine 原圖與兩張原創機轉 SVG；移除兩張重述性三欄概念表，改以原圖前後的論證交代臨床意義。
- 加入 GOLD 2026 初始 ABE（前一年至少一次中度或重度惡化入 E）與 follow-up 分開、Rome proposal 急性惡化當下臨床生理嚴重度分層，避免把住院場所直接當成嚴重度定義。繼續將原書 2024 表與現行 2026 分組清楚區隔。
- STARR2 所引 eos >=2% 的來源疑義維持 **HOLD**；原書圖中的文字不能當成停藥指令。NIV、控制性氧療、急性 steroids 與抗生素的適用條件保留。
- 靜態結構檢查：Markdown 約 19,600→16,000 字元（包含六個沿用原圖／SVG 大段 markup；非精確中文字數），四張 Pocket 圖皆存在、兩張原創 SVG 皆存在、原病例 CT 另加一張、七節齊全、兩題附解析。圖的原位 image src／caption 未暗改。

**尚未完成：** (1) 原 Pocket 四圖的公開使用依據；(2) STARR2 correction 全文與原書 p87 的疑義確認；(3) 本輪 V2 的醫學獨立審查／實體手機閱讀驗收；(4) 重新生成單檔內嵌圖 HTML。本分支現有的 `2026-10-26-copd-originals-integrated.html` 仍是 V1 靜態快照，**不等於 V2 改稿已同步**。不可將這份 V2 Markdown 當成正式網站部署完成或可發佈聲明。


## 續修 V2.1｜慢性呼吸力學 → 急性呼吸床邊決策（2026-10-26）

需求：補齊此前 86/100 文章缺少的急性床邊推理；同一 PR #49 延續、不觸及正式部署。

### 編輯實際變更

- 05 重寫：R×C 排空時間常數 → expiratory flow limitation／動態過度充氣 → intrinsic PEEP／吸氣觸發負擔 → VT、VD、V̇E、V̇A 定義 → 酸鹼血氣 → NIV 的機制與評估。
- 05.2 教學公式：V̇E = VT × f，V̇A ≈（VT−VD）×f；12×500 mL 與 24×250 mL 的 V̇E 同為 6 L/min，設 VD 150 mL，V̇A 為 4.2 與 2.4 L/min。數字僅教學示意，非病例實測。為手機可讀性取消初始 6 欄表，改用上下兩個完整算式文字區塊。
- 06 重寫：NIV 開始後的臨床／血氣反應（BTS 2 小時內追血氣）、NIV 失敗與氣道保護、插管後仍需排空時間、呼吸器 flow-time／呼氣暫停的解讀、外加與內在 PEEP 的界線，及 pure IET vs true expiratory flow limitation（EFL）的不同反應。
- 07 自編遷移題由兩題增為三題：肺減容、真實 73 歲 NIV 病例、87 歲實測 auto-PEEP 病例。反事實假設與原文實際事件明確分開。
- 保留 01–04 舊版結構／同一 Marchand 案例、四張 Pocket Medicine 9E 私人來源圖、既有兩張原創 SVG 和原病例 CT。沒有重繪 Pocket 來源圖、更新圖像公開白名單或更動 site/pages.json。

### 使用的真實病例（不可跨案例串接數值）

1. **Uğurlu AÖ, Ergan B. Pulmonology. 2023;29:144–150，doi:10.1016/j.pulmoe.2022.07.010**，[完整可搜尋文字](https://www.sciencedirect.com/science/article/pii/S2531043722001787)。73F、RR30、HR120、room air SpO₂86、PaO₂54、pH7.29、PaCO₂69；day2 pH7.35、PaCO₂61.6，IPAP/EPAP 20/6。第 2 天的氣體交換改善不可冒稱「NIV 1 小時就改善」；報告 Sat 97.7% 是觀察結果，不是建議的 AECOPD 給氧目標。
2. **Management Strategies for Hypercapnic Respiratory Failure in COPD: A Case-Based Discussion (2025), Case 1**，[原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12183487/)。63M 合併肺炎與濃厚分泌物，pH7.15、PaCO₂141，bilevel NIV 約 6 小時後因臨床問題持續而插管。其部分 HCO₃、Table 1 與敘述有不一致，不採用 HCO₃／細節設定／未核定的病程數值來推理。這是**不同病人**，不是成功 NIV 病例的後續。
3. **Padrao et al., ATS Scholar 2026;7:86–88，doi:10.34197/ats-scholar.2025-0073OT**，[完整文章](https://academic.oup.com/atsscholar/article/7/1/86/8439232)。87F COPD GOLD 3B，插管後 set PEEP 5、auto-PEEP 14、total PEEP 19 cmH₂O；文章解釋 IET vs EFL、波形與相應 PEEP 反應。**不推論本例有實測低血壓**。ATS 原圖有 CC BY-NC-ND 4.0 註記，正文僅連結其圖文，不複製原圖。

### 新指南和實際決策支持

- [ATS 2026 acute noninvasive respiratory support guideline](https://doi.org/10.1093/ajrccm/aamag302)：急性高碳酸呼吸衰竭，面罩 NIV 強推薦；HFNC 只在酸中毒較輕且可迅速升級時為有條件替代。
- [ERS/ATS 2017 NIV recommendation](https://publications.ersnet.org/content/erj/50/2/1602426)：standard medical management 後持續酸中毒／高 CO₂／呼吸窘迫，bilevel NIV 重要；沒有單一「過低 pH 必須一律不試 NIV」的絕對數字規則。
- [BTS acute NIV quality standards](https://doi.org/10.1136/bmjresp-2018-000283)：開始 NIV 2 小時內驗血氣；不改善時由具升級決策能力的醫療團隊迅速重評。
- [Hess, Respir Care 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10208989/)：呼吸器 flow-time 曲線、end-expiratory hold 條件、air-trapping、auto-PEEP 與延長呼氣時間的機轉。

### 數據核查與不能越界的地方

Henderson–Hasselbalch 近似 HCO₃ ≈ 0.03 × PaCO₂ × 10^(pH−6.1)：
- 73F 第一次 pH7.29／PaCO₂69 算得約 **32.1 mmol/L**，報告 HCO₃28；
- 73F day2 pH7.35／PaCO₂61.6 算得約 **32.9 mmol/L**，報告 HCO₃29.6；
- 63M pH7.15／PaCO₂141 算得約 **47.5 mmol/L**，原文敘述 HCO₃36.1（表另見 35.5）。

因此資料限制直接寫進正文：**不能把這些 HCO₃ 當作可信的慢性代償標準或推導混合性酸鹼診斷**；需要對原報告做來源更正／勘誤查核。病例血氣的 pH、PaCO₂ 用於各原文所描述的 clinical decision，不自行編造 1-h ABG 或 PSV response。

### 驗收與仍阻塞正式發布

完成靜態內容完整性核查：七節、四張 Pocket 原圖、兩張原創 SVG、原 CT Figure 1、三道具有解答的轉移題。內文對真正量測值 vs 教學假設、跨病例界線及來源不一致均明確標示。

仍未完成：公開使用 Pocket 原圖的獨立法律依據；Pocket p87 的 STARR2 引文與更正全文；V2.1 版本整份醫學獨立審查；本次 V2.1 手機實機／Safari 版面測試；新版 HTML 單檔重建。原單檔 `2026-10-26-copd-originals-integrated.html` 和其 QA JSON **仍是 V1，不可錯認為最新 V2.1**。GitHub build 成功也只能證明目前 workflow 涵蓋項目，不能驗證這個未公開的草稿之真實手機閱讀或醫學內容。正式稿及部署維持 HOLD。
