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
