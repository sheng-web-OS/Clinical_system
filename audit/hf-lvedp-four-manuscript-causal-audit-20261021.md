# Heart Failure × LVEDP × DCM × Diuretics｜原稿因果前提稽核

日期：2026-10-21
身分：**AI 編輯稽核報告**；不是作者原稿、不是已核准公開教材。
狀態：**四份 Git 全文已讀；Pocket Medicine 第九版 Figure 1-2 已實際看原始 PDF 頁面；部分原始生理研究的文字／圖說已比對，未完成所有研究圖像與補充資料逐圖查核。**

## 0. 稽核目的與來源固定

本次不以 AI 發明新綱要，而是測試：四篇既有文字是否已經完成主要因果鏈，哪些新增資訊才具有不可替代的解釋力。

作者原稿的 Git 相對路徑及本次已讀 blob SHA：
- [Heart Failure｜2026-07-12](../content/xiaoma-reading/originals/2026-07-12-heart-failure.md) — `2ccc44d1b6e478031c23b7637cca1c4f36833043`
- [LVEDP｜2026-07-12](../content/xiaoma-reading/originals/2026-07-12-lvedp.md) — `a84c6a107a6fc5145e4da22226f18d741e319a34`
- [DCM｜2026-07-10](../content/xiaoma-reading/originals/2026-07-10-dcm.md) — `83d64dcd381f44c3cf8815fd88694c2e14b2da50`
- [Diuretics｜2026-07-20](../content/xiaoma-reading/originals/2026-07-20-diuretics.md) — `785f28e292b9e7160c7b8fb250fdaa38af15d24b`

**來源身分限制：**上述是儲存庫中標為 originals 的完整檔案；檔案存在、全文已讀，不自動等於與歷史聊天中作者最後核准版本逐字相同。儲存庫的 `archive/xiaoma-reading/recovery-status-20261021-verified.md` 仍以 conversation_only 記錄多篇文章，與 `content/xiaoma-reading/originals/` 現況不同步。此處不擅自改寫回收狀態；需按提交時間與歷史直貼版本稽核來源鏈。

指定原始教材：使用者提供之《Pocket Medicine: The Massachusetts General Hospital Handbook of Internal Medicine, 9th Edition》PDF（463 頁）；**PDF 第 34 頁** HF 定義及 prior hemodynamic treatment；**PDF 第 35 頁 Figure 1-2 原圖**（不只是擷取文字）；**PDF 第 39 頁** HFpEF 的 poor compliance/volume-pressure 敘述。請以 PDF 頁碼，勿與印刷頁碼混用。

## 1. 原圖與作者原稿的忠實程度

Figure 1-2「Approach to left-sided heart failure」圖像上的順序：
- left-sided HF → 須考慮 mitral valve disease / pulmonary venous obstruction 等不由 LVEDP 單獨解釋的情況；
- ↑ LVEDP → **↑ LVEDV** 與 **normal LVEDV**；
- ↑ LVEDV → ↑ ESV（systolic dysfunction；例 contractility 下降、afterload 增加），或 ↑ SV（high SV failure；high output、regurgitant/shunt total-flow states）；
- normal LVEDV → diastolic dysfunction 與 pericardial disease（後者通常更突出 right-sided failure）。

LVEDP 原稿已忠實保留這四路；另外補出：四象限只描述 congestion vs perfusion、left-sided HF 圖主要處理肺鬱血路徑，EF 不等於有效輸出，total SV 不必然等於 systemic forward SV，並區分 left atrial / pulmonary venous obstruction。**以上不能被報告為「作者未說清楚」。**

Heart Failure 原稿已分清 wet/dry、warm/cold、EF/SV/CO、congestion 的 accumulation vs redistribution、dry-cold 非 HF 診斷、HF syndrome vs DCM phenotype、ADHF 事件 vs Stage 病史，以及誘因如何導向壓力或流量。Diuretics 原稿已詳述 tubular exposure→threshold→ceiling→post-diuretic sodium retention/distal compensation→24 h sodium balance→真正 decongestion，並警告 creatinine 不能獨立決定停藥。DCM 原稿已述 contractility 與神經體液代償（SVR、preload、RAAS）的交互作用。

## 2. 必須區分的審查結果

| 關係主張 | 原稿現況 | 稽核分類 | 動作 |
|---|---|---|---|
| Congestion ≠ perfusion；EF ≠ CO | HF、LVEDP 明說 | A：已充分 | 保留原稿、連結，不再重寫 |
| Elevated filling pressure ≠ total body water excess；volume redistribution | HF 明說 | A | 連到 acute pulmonary edema bedside phenotype；不冒稱新發現 |
| LVEDP↑後分 LVEDV／ESV／SV 與 myocardium／pericardium | LVEDP 詳述 | A | 使用 Figure 1-2 與作者解析，不另製一份同義教學 |
| DCM（structural phenotype）≠ HF（clinical syndrome） | HF 與 DCM 均說明 | A | 建立雙向導航，不增篇幅 |
| Loop early natriuresis ≠ full-day negative balance ≠ decongestion | Diuretics 已詳述 | A | 既有利尿圖表稽核直接沿用 |
| 單點 LVEDP↑、LVEDV normal → 直接確定「compliance 下降」 | 原稿語氣偏確定；原圖是分類示意 | **D：需限定** | EDPVR 是壓力-容積的函數關係；單次 P/V 不能唯一估計 stiffness = dP/dV，也不能區別 active relaxation、被動僵硬、heart rate/atrial effect、external pressure。適合用精簡註釋，而非推翻原圖 |
| 把 LVEDP、mean PAWP/PCWP、LAP 近似作同一壓力 | LVEDP 原稿已提出 obstruction 前提，但尚未說明波形時相 | **D：需限定** | PAWP 常近似 mean LA pressure，LVEDP 是特定時點壓力；AF、LA compliance、大 V wave、valvular physiology 等可能使兩者顯著不同 |
| 把 LVEDP 當單一 preload 指標 | 原圖未完全討論；小麻 shock 章用「LVEDV ≈ LVEDP ≈ LAP ≈ PCWP」簡記 | **D：需限定** | 容量和壓力不是等量單位；transmural LV filling pressure ≈ LV intracavitary pressure − extrinsic pressure（RA pressure 僅在特定條件下是外壓 surrogate）；並區分充盈量與 Starling 機轉 |
| Renal dysfunction 只能用低 CO 或利尿引起「太乾」解釋 | DCM/HF/Diuretics 已涉及 renal perfusion/creatinine，但缺 renal **back pressure** 的連續因果橋 | **C：真跨篇缺口** | 說明右側 venous congestion、renal venous/interstitial pressure 與有效灌流壓的關係；MAP−CVP 可當粗略 hemodynamic proxy，不視為腎內實際灌流壓的精確值；辨別 correlation vs causality |
| DCM contractility 下降「這件事會讓血壓下降」 | DCM 原稿早段有該句，同時介紹後續 SVR 補償 | **D：需限定** | ↓inotropy 傾向降低 SV/CO，但 MAP 取決於 CO×SVR（兼受 HR、loading condition 影響）；血壓可以維持、甚至升高，不能把低血壓當 DCM 必然早期表現 |
| 左心 pulmonary congestion 足以判斷右心 systemic venous congestion | HF、LVEDP 分清左右，但四篇臨床用語有時統稱「congestion」 | **B/C：必要連接** | 以左右兩套壓力軸連結肺鬱血與 systemic/renal venous congestion；不要從單一 JVP/PAWP 假定兩側同向、同程度 |
| 高 LVEDP 足以證明肺水腫當下機制/嚴重度 | 原稿已有 LA/pulmonary venous intermediate，缺肺微血管淨濾過限制因素 | **P2：視內容目的按需擴充** | Hydrostatic gradient、oncotic forces、barrier、lymphatic compensation；僅在需解釋肺水腫臨床差異時增加，避免主線失焦 |

A = 作者已說清楚，不重述；B = 已有但跨文需連結；C = 證據支持的實際新增橋樑；D = 必要的限定或精確修訂；P2 = 目前非必需。

## 3. 原始生理與臨床證據及限制

**EDPVR／stiffness**
- Zile, Baicu & Gaasch, *NEJM* 2004;350:1953–1959, [DOI](https://doi.org/10.1056/NEJMoa032566)：47 HF/normal EF 病人 vs 10 controls；研究以導管與心超描述 relaxation τ 延長、stiffness 上升與 EDPVR 左上位移。原始研究支持主線；不是所有 HFpEF 患者都需具有完全相同機轉。
- Burkhoff et al., *Am J Physiol Heart Circ Physiol* 2005, [DOI](https://doi.org/10.1152/AJPHEART.00138.2005)：EDPVR 為曲線，stiffness = dP/dV，可用多種非線性模型擬合；一組 P/V 無法識別完整曲線。
- Borlaug 等研究者，*JACC Heart Failure* 2019, [DOI](https://doi.org/10.1016/j.jchf.2019.03.021)：Figure 1／2（已核對圖說，**未像素級檢視全部原圖**）討論 intracavitary vs transmural pressure、pericardial restraint 與 ventricular interaction；這是 Figure 1-2 正常 LVEDV／高 LVEDP 分支最值得補上的實質測量前提。

**Mean PAWP ≠ LVEDP**
- Hemnes et al., *Chest* 2018;154:1099–1107, [原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC6224703/)：2,270 次同步左右心導管觀察，42% 病人兩者差距 >5 mmHg；Figure 2 顯示 agreement / regression 差異（已取得結果及圖說，未完成全幅圖像核對）。觀察族群異質，不能直接外推為 HF 特定病人錯判比例。
- Hanna et al., *JACC Heart Failure* 2018, [討論](https://www.jacc.org/doi/10.1016/j.jchf.2017.11.009)：mean wedge 與單點 LVEDP 有波形／時間定義差異；V wave、LA compliance 等重要。應補入簡短的臨床量測邊界。

**Congestion、redistribution、organ perfusion**
- 2021 ESC HF Guideline [完整指南](https://academic.oup.com/eurheartj/article/42/36/3599/6358045)：急性失代償與急性肺水腫在 accumulation vs redistribution、SBP、CO 上有不同典型模式；Figure 7/8 表達管理分流，Figure 13 追蹤早期利尿反應和 complete decongestion。**本次閱讀正文、圖說及原圖資訊；第 13 圖的完整稽核應沿用** [既有 diuretics-figure-evidence-check.md](diuretics-figure-evidence-check.md) 的核實分級，不能偽稱所有圖像已重新逐像素驗證。
- Fudim, Hernandez & Felker, *JAHA* 2017;6:e006817, [原文](https://pubmed.ncbi.nlm.nih.gov/28862947/)：review volume redistribution、splanchnic venous capacitance、stressed/unstressed volume；支持 HF 原稿既有模型，非「AI 新增」。
- Mullens et al., *JACC* 2009;53:589–596, [完整研究](https://pmc.ncbi.nlm.nih.gov/articles/PMC2856960/)：145 名 advanced ADHF 病人之**觀察性**分析；WRF 組入院 CVP 18±7 vs 12±6 mmHg，臨床變化與 CVP 相關，並非僅低 CI。原研究 Figure 1/3 與 Table 2 是最值得續核對的腎臟段證據。**不應由此宣稱 CVP 升高是所有 AKI 的唯一原因或已有隨機試驗證明降低 CVP 必然保護腎臟。**
- 2022 AHA/ACC/HFSA HF Guideline [全文](https://www.jacc.org/doi/full/10.1016/j.jacc.2021.12.012)：住院 HF 評估需獨立辨認 congestion/hypoperfusion，並指出右、左充盈壓可不匹配；與本次補充優先序一致。

## 4. 真正值得形成的「增量教材」，而非重寫

建議唯一優先補充模組名稱：**「同樣是壓力，究竟是哪一種壓力？從 LVEDP 到肺鬱血、腎靜脈鬱血與利尿限制」**。

用同一條連續因果敘事處理：
1. Left atrial / pulmonary venous pressure 高 → lung hydrostatic congestion（肺側，與 LVEDP 關係有條件）。
2. LVEDP↑ → 分辨 LVEDV、intrinsic EDPVR、extrinsic restraint（心室壓力讀值並非唯一病因）。
3. Right atrial / central venous pressure 高 → renal venous back pressure → 可損及 kidney function（右側，與肺側 filling pressure 不必然一致）。
4. Early loop natriuresis → 全天 sodium balance → 真正 decongestion；同時以 congestion、tissue perfusion、creatinine 與呼吸循環狀態做動態安全判讀（接回作者已寫好的 Diuretics），不把 Cr 上升直接等同「利尿過度」。

**臨床連續論證 > 獨立補一篇「Cardiorenal Syndrome 綜述」。** 重症角度只在病人無法維持氧合／灌流的臨床分岔出現，不另開雜亂附錄。

## 5. 待查／驗證事項

- [x] 四份 Git 原稿全文與 blob SHA 已核對。
- [x] Pocket Medicine 第九版 PDF 第 35 頁 Figure 1-2 實際圖像查閱；第 34、39 頁查閱。
- [x] 2021 ESC Figure 13 已有舊稽核，避免重工。
- [x] 檢索核對 EDPVR、pericardial restraint、PAWP-LVEDP discordance、venous congestion 研究的摘要／正文／圖說層級證據。
- [ ] 原始研究的所有重要 Figure / Table / Supplementary 進一步逐像素與圖註查核，特別是 Mullens Fig 1/3、2019 pericardium Fig 1/2、Hemnes Fig 2。
- [ ] 將四份 Git 原稿與歷史聊天中作者認可版本逐字比對，釐清 `recovery-status-20261021-verified.md` 與 repository originals 的狀態不一致；不改寫原稿。
- [ ] 以 2–3 個反例（高 LVEDP 正常 EDV、肺鬱血但 CVP 不高、高 CVP 且 creatinine 上升但未必 low CO）盲測新教材是否比「只閱讀四原稿」提高正確因果推論，而不是單純增加篇幅。
- [ ] 跨篇材料經審閱後才考慮網站發布；本稽核檔本身不是公開文章。


## 6. 續查補遺｜靜脈鬱血、壓力量測與研究年代界限（2026-10-21）

性質：**本次追加原研究正文、Table 與 Figure legend 的來源核對**，不是新醫學整合稿、不是人體盲測、也不宣稱已重新取得全部原圖影像。原稿作者的既有內容仍依本文 §1–2 的 A/B/C/D 分類判讀；不將數值再換句話說冒充新發現。

### Mullens 2009（renal venous congestion）｜來源已核對，Figure 圖像仍待目視

完整作者稿：https://pmc.ncbi.nlm.nih.gov/articles/PMC2856960/
期刊：https://doi.org/10.1016/j.jacc.2008.05.068

- **研究設計**：145 名 advanced ADHF、接受 PAC 指引密集治療患者的觀察研究，LVEF 20 ± 8%；58 人（40%）發生住院期間 creatinine 上升至少 0.3 mg/dL 的 WRF。不是一般 HFpEF、未篩選 AKI 或隨機分配 CVP 目標的試驗。
- **Table 2／baseline**：WRF vs non-WRF，CVP 18 ± 7 vs 12 ± 6 mmHg（p<0.001）；CI 2.0 ± 0.8 vs 1.8 ± 0.4 L/min/m²（p=0.008）。不能把「WRF」的必要定義說成 CI 更低；原研究恰恰看見較高 CVP 與較高（非較低）CI。
- **Figure 1 正文／圖說**：以 admission CVP、CI、SBP、PCWP 分層比較 WRF 發生率；CVP 大於 24 mmHg 的受試者 75% 發生 WRF，須加上樣本大小及群組限制，不可製成普遍的 24 mmHg 臨床硬閾值。
- **Figure 2 正文／圖說**：baseline CVP 之 ROC AUC 0.734（p<0.0001），baseline CI AUC 0.552（p=0.6）；模型辨識能力不是隨機介入療效，也不是 CVP 測到 0.734 即可單獨決定治療。
- **Figure 3 正文／圖說**：PAC removal 時比較 CVP 分組（8 mmHg）與 CI 分組（2.4 L/min/m²）對 GFR 的關係，error bar 為 95% CI。隨訪 CVP 持續大於 8 mmHg 者 WRF 發生率 51% vs 18%（p=0.01）；不得推論 8 mmHg 是所有人最適用的固定目標。
- **C bridge 的真正貢獻**：補上 elevated venous back pressure 與器官充血／腎功能之間被只談 forward CO 的模型忽略的生理軸，並將「肺側充盈壓」與「系統靜脈／腎靜脈充血」分開。觀察性關聯、適用族群及干預效果三者必須獨立。
- **目視驗證狀態**：本次核對原文、Table 2 與 Figure 1/2/3 標題、圖說及相鄰結果段；尚未將 Figure 1/2/3 的原始像素圖像實際開啟逐圖驗證。不能填成 original-image-verified。

### Hemnes 2018（PAWP 與 LVEDP discordance）｜研究定義的時間外推邊界

完整作者稿：https://pmc.ncbi.nlm.nih.gov/articles/PMC6224703/
期刊：https://doi.org/10.1016/j.chest.2018.08.1033
對照正式指南：https://doi.org/10.1093/eurheartj/ehac237

- **Table 2／Results**：2,270 位同時右、左心導管患者之 PAWP 與 LVEDP 差異；整體 42% 相差超過 5 mmHg，不能用兩種壓力都是 filling pressure 就直接寫等號。Figure 2 A–D 提示一致性和相關性不是同一回事；整體 R² = 0.36。
- **研究族群與時間定義**：該文 PH 亞群使用當年 mPAP 至少 25 mmHg 的分類方式；2022 ESC/ERS 改為 resting mPAP >20 mmHg，前毛細血管 PH 還須 PVR >2 WU、PAWP 不高於 15 mmHg。原研究在其 PH 族群中的分類錯誤比例不能直接當成新定義下的誤判比例；如需此數值，應依最新定義重新分析原始資料。
- **D qualification 的真正增量**：在測量詞彙相似時，須回答資料來自哪個心腔／波形時間點、mean vs instantaneous 定義、甚麼臨床現象改變兩者差距。把分歧比例直接拿來支持所有 HF、所有 PA catheter 或特定處方會外推過度。
- **目視驗證狀態**：本次核對原文、Figure 2 圖說及 Table 2 文字數據；Figure 2 原圖尚未逐像素讀取，e-Tables 未完整核對。

### 來源身份錯誤的負例（正式納入 Agent 回歸題）

本次搜尋「CVP vs eGFR figure」所得一張第三方投影片，實際引用的是 **Damman et al., JACC 2009;53:582–588**，並非 **Mullens et al., JACC 2009;53:589–596**。兩篇同屬心腎血行動力學、刊登頁次相鄰，但研究不同。不得因圖片在主題上相符，就誤配成 Mullens Figure 3；要以 DOI、第一作者、正式期刊圖號／圖說或原文 Figure link 核驗 provenance。

此失敗案例並非證明「圖片已查核」，而是說明：**圖像搜尋命中 ≠ 原文圖像身分成立；可讀圖說 ≠ 已親眼看圖；相關機轉一致 ≠ 可互換研究及樣本。**

### 發布與下一次實驗的門檻

原稿與本段只供來源回查；HF 跨篇 C／D 精修仍需完成必要原圖視覺稽核（Mullens Figures 1–3、Hemnes Figure 2、Borlaug 2019 Figures 1–2）及來源適用性檢查後，才可能將此子論點標記為 figure-audited。增量有效性另需以只讀四篇原稿 vs. 原稿加經核對橋樑的反事實題，分開評估：是否真的補上必要解釋、還是延長閱讀而未改變決策。**暫不將此 audit 升格為公開教材。**
