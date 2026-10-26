# HBV Phase vs Fibrosis Stage｜Editorial Intake & Figure Audit

日期：2026-10-26｜分支：`editorial/hbv-phase-state-vs-stage-20261026`

## 狀態

- GitHub main（檢查時 497 tree items）無獨立 HBV phase 原稿／整合教材；本分支補入未發布候選。
- 作者文字：`archive/xiaoma-reading/intake/2026-10-26-hbv-phase-user-supplied.md`。由本次使用者對話提供之完整文字轉存；**非已核 Facebook 作者 canonical**，不得將其自動認定為 `content/xiaoma-reading/originals/` 的已發表版。
- AI 來源對讀整合版：`content/xiaoma-reading/integrated/2026-10-26-hbv-phase-state-vs-stage.md`。非作者原文，未宣稱獨立醫師 peer-review。
- 來源：`content/xiaoma-reading/hbv-phase-sources.md`。**未加入 site/pages.json**；無公開 URL／Cloudflare 部署／CI 完成宣稱。

## PM9 原表視覺核讀

- 來源：使用者 Library 之 `內科_Pocket Medicine The Massachusetts General Hospital Handbook of Internal Medicine, 9th Edition_625A_Flatten(1).pdf`，第 140–141 實際 PDF 頁；此次實際取回第 141 頁的頁面圖像，非僅文字搜尋。
- 本次對話也提供相同書頁的直接截圖。頁 141 表標題為 `Phases of Chronic HBV Infection`，欄位 ALT／sAg／DNA／eAg／Liver histology (inflam/fibrosis)／Rate of cirrhosis；腳註 ALT <35 U/L 男、<25 U/L 女，表格 adapted from *Hepatology*. 2018;67:1560。
- **讀回要點**：HBeAg-positive infection 為 normal ALT + very high DNA + minimal histology；HBeAg-negative low-replication 組明列 `min necroinflam; variable fibrosis`。同一 phase 不證明既有纖維化程度；rate of cirrhosis 是歷史族群估計。
- 圖表身份：原書三方著作，2026-10-26 私下視覺查核，**未公網重製**。對話/Library 內文件非 GitHub repository 資產；若未來發布，公開的是另製具有解釋意義的圖 1／圖 2，並提供頁次與著作書目，不可標成原書截圖已附。
- 新增兩個 `<figure>`：`fig-hbv-three-questions`（phase/stage/prognosis 三個不同問題）；`fig-hbv-decision`（從 stage 到必要治療／個別化決策）；使用網站既有卡片語彙，不添加新 JS 系統。未測手機 rendering，發布前要目視。

## 知識增量與校正

| 類型 | 項目 | 決策意義 |
|---|---|---|
| A 作者已完成 | Phase ≠ stage、DNA ≠ ALT ≠ histology、HBeAg-negative 分岔、灰區與 HBsAg loss 後風險 | 保留作者命題，不當作 AI 新發現 |
| B 跨文件橋 | 將原表的 `variable fibrosis` 接回病人需要獨立 staging 的理由 | 避免同格 phase 誤認個人風險相同 |
| C 新增證據性補強 | EASL 2025 simplified algorithm 不須硬套四格；AASLD/IDSA 2025 indeterminate 的 shared decision | 從概念分類連至 2026 年實際臨床處置 |
| D 必要校正 | 書上 HBV DNA `≥10^6` 不等於新 AASLD 狹義 immune-tolerant `≥10^7`；單次 ALT、cirrhosis rates／fibrosis、HBsAg loss 後 HCC surveillance 分別有適用界線 | 防止把舊表變成新處方流程 |
| X 未納入 | 單一 phase 直接決定治療、使用自編病人值冒充病例、宣稱原圖已獲版權授權 | 避免誤導 |

## 臨床／出版品質閘門

1. **內容來源**：小麻原表第 141 頁已視覺核查；EASL／AASLD 新文獻以官方全文／權威原始出版頁文字及具體條款查核；EASL 原 Figure 1 本輪未以原 PDF 截圖逐欄驗證，公開教材只概括而不重製其演算法。
2. **重大安全線**：已避免 `normal ALT => no treatment`、`HBeAg-negative => cured`、`cirrhosis needs DNA≥2,000`、`HBsAg loss => stop HCC surveillance` 等危險推論。建議行為與其證據等級就地說明。
3. **作者保真**：歷史使用者提供的原稿另存私人 intake；Facebook 發布版逐字身分尚未對讀，不能掛上 `historical_original` 已證實標籤。
4. **審稿**：已做同輪來源審閱與反事實編輯；**尚未完成獨立醫師／盲審／實際手機版面／讀者成效實驗**，不以 AI 自評取代。
5. **公開**：因尚未核對網站建置與 Figure Gate 註冊、未加入 `site/pages.json`，本 PR 一律 Draft，`HOLD_PUBLICATION`。往後需補 `audit/figure-gate.json` 對應記錄、正式來源頁與文章 allowlist、編譯測試、站點實際打開後才能宣稱正式發布。
6. **權利**：原圖合理引用及市場替代風險未個別認證；公開不重製原書像素。原創教學圖不臨摹原表整體布局或視覺元素。

## 未完成事項

- 檢查來源參考的最終 permalink 與錨點／網站排版；
- 按 figure-gate 契約建立可測記錄與在手機實際驗證 `original-list` 樣式；
- 將整合版依 EPQC 交予獨立讀稿審核，並對醫療指引的時效作發布前再查；
- 若作者原 Facebook 公開全文可取得，才更新作者 canonical 的 provenance，不替換 AI 新稿。
