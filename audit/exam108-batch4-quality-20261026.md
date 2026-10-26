# 108（一）醫學（三）第四批｜實際 QA 2026-10-26（私人稽核，不是公開教材）

範圍：Q61/Q63/Q75/Q78；對應本分支 3 篇新教材與 exam108-acute-sources.md。執行者：AI 來源反查與醫學編輯，**不等同獨立真人專科同儕審查**。

## 0. 結論與門檻

- 原卷題幹／選項：PASS，考選部 17 頁官方 PDF 的 Q61、Q63、Q75、Q78 已逐項比對；共用題幹 Q61–63 含 Q62。更正答案 PDF 只有 Q33 一律給分。第四批答案 C/A/C/C。
- Pocket 9E 原書資料：PARTIAL PASS，PDF p137–138 已目視 (p137 Patterns of LFTs 表，p138 Figure 3-3 標題定位)；p175–176 已目視 AKI 定義／Etiologies and Diagnosis 原表的上、下半幅與 Managing complications；p177 Rhabdomyolysis 已全文文字對讀，但取得的 PDF page-image rendering 不成功。
- 外部臨床事實：來源及核心推理已核。AAST 2022 原文：輸液依 UOP 1–3 mL/kg/hr、不超過約 300 mL/hr；不建議為預防 AKI 例行 bicarbonate／利尿劑；RRT 不作預防。2025 AHA ALS 原文：advanced airway 後持續壓胸搭配每 6 秒 1 次通氣係 2b C-LD 的建議；使用波形 EtCO2 輔助確認 ET tube。2025 WSES 版實際 2026-01-28 online publish，名稱與日期不混淆。ACSM 2023 本輪僅取回摘要，不能當作已逐頁核讀全指引。
- 原書圖像重製授權／正式視覺發布：HOLD（尚未能證成公開重製權）。即使本次私人版像素可用，不能以「已看原圖」推導「可放在公網」。仍缺 p177 原頁影像、手機尺寸與原圖授權。
- 本批未列在正式 site/pages.json、未通過全站 build/test，未合併 main，未驗證 Cloudflare：NOT PUBLISHED。

## 1. 臨床安全與推理的逐題驗收

**Q61 中暑**
- PASS：核心高熱 + 嚴重 CNS dysfunction（癲癇、昏迷），熱衰竭、熱暈厥、熱痙攣不足解釋；立即快速降溫，不用 acetaminophen 處理散熱失衡。此處 Q62 也在同一組官方題，本文只是借用解釋，不將 Q62 偷加為本批已完稿題。
- HOLD：ACSM 2023 目前摘要級取得；任何精確體溫取樣或降溫程序處方不得僅以摘要宣稱確證，須在後續對讀可訪問全文時細化。

**Q63 橫紋肌溶解／AKI**
- PASS：原題 Cr 2.2→2.8、CK 42,700、tea-colored urine、dipstick heme(4+) with zero RBC、K 5.0 正確；nonoliguric AKI、myoglobin-related injury、補液尿量反應與容量過多風險的推理符合原文與 AAST。
- PASS：尿液酸化為錯，固定 2500 mL/day 未依反應調整也錯，無一般治療無法控制的嚴重併發症不應直接以 CK/Cr 當透析觸發。
- PASS：Pocket p177 bicarbonate 說法與 AAST 2022 preventive bicarbonate 不建議之版本界線已明寫；避免外推有獨立適應症的 bicarbonate。
- PASS：2024 熱傷害 AKI 真實病例（CK 722,559，Cr 667 μmol/L）已加入且與匿名考題清楚分離；單例的 CytoSorb 不當標準治療。
- LIMIT：體重未知，不能把歷史尿量 200–300 mL/hr 改寫成所有病人的固定必要目標。無單一 CK threshold 等於 RRT indicated。

**Q75 CPR**
- PASS：根據原題 2015 AHA 的四選一，插管後仍 30:2 是 C；2025 ALS 指南持續按壓，advanced airway 後可約 10 breaths/min；2025 BLS 若沒有 advanced airway 則 30:2。
- D 限制：歷史 6–7 mL/kg 措辭不是現行每人必須遵循的 tidal volume prescription；重點足夠胸廓起伏而避免過度通氣。A 若脫離 CPR/呼吸停止情境會有歧義，不能直接推成所有 BVM 情境每分鐘 10–12。
- LIMIT：advanced airway placement 有機會中斷 CPR，2025 ALS 強調不可因追求插管而無必要地拖延 CPR/除顫。

**Q78 闌尾炎敏感度**
- PASS：歷史答案 C RLQ pain；psoas sign 低敏感不代表陽性毫無價值；遷移痛具鑑別價值，但非最高敏感；敏感度、特異度、LR、pretest odds 已清楚區分。
- PASS：2004 Andersson meta-analysis 表示單項變項有限，合併體徵與發炎指標更好；2025 WSES edition (online 2026) 支持以風險分層及影像增加診斷正確性。
- LIMIT：原題選項 RLQ pain 與 examination RLQ tenderness 不可宣稱完全是同一研究變項；不可用單個敏感度數字無條件套用孕婦或老人。

## 2. 原圖回收盤點與決策資訊

| Pocket PDF | 已實際看過 | 重要資訊 | 原書可公網重製 |
| --- | --- | --- | --- |
| p137 Abnormal Liver Tests / Patterns of LFTs table | 是，完整可取得視覺 | 非肝臟肌肉傷害亦可使 AST 增高；LFT pattern 不是病因唯一標記 | 未取得許可 |
| p138 severe aminotransferase 段、Figure 3-3 標題定位 | 是，完整可取得視覺 | rhabdomyolysis 和 heat stroke 屬 AST/ALT 異常鑑別 | 未取得許可 |
| p175–176 AKI Definition / Etiologies and Diagnosis of Acute Kidney Injury table | 是，已目視上下半頁 | pigment（Hb, myoglobin）位於 intrarenal tubular injury 一欄、尿沉渣、FENa 限制及透析併發症的決策分支 | 未取得許可 |
| p177 Rhabdomyolysis 正文 | 文字已完整核讀；像素失敗 | myoglobin 的氧化與阻塞、生理上的尿量調整、bicarbonate 原文定位與電解質風險 | 未取得許可 |

原表已有的內容屬 A；Q61/63 將 p137 LFT 與 p175–177 腎損傷跨段連接屬 B；2022 AAST 對 bicarbonate 常規使用的必要更新屬 D。原表的可用像素並未寫進 Git，也未寫進公開清單。

## 3. 工程／發布規則

本 PR #50 保持 Draft；先補完 Pocket p177 圖像或留下「無相關原圖」的實際合理證據，並經原出版社授權或其他可靠合法權利依據後，才可登錄正式已發布三篇的 figure gate 記錄。然後加入既有 year-first site/pages.json，分別 exam metadata [61,63], [75], [78]；跑 build_site.sh、全測試、CI 及正式 Cloudflare readback。**不准只將 gate status 設為 represented，就用 metadata 欄位取代原圖的公開可讀性。**

第四批：**內容已擴寫並完成本次 AI 一級事實／來源 QA；原圖權利、完整像素及公網驗收未完成，總發布結果仍 HOLD**。
