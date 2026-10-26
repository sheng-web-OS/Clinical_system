# 2026-10-21 對話直貼文章｜原稿接收清單

狀態（截至 2026-10-26）：**21 篇對話接收稿中，六篇已進入 Git originals 與出版目錄、三篇（Constipation、HBV ALT 訊號、Chronic diarrhea）已保存完整私人 source snapshot（未出版）、其餘十二篇仍是 conversation_only。** 這三種狀態不可混同。原稿的網站部署以實際 Cloudflare 成功狀態為準。

本清單是接收及搬遷追蹤，不是已完成醫學事實查核、已確認唯一最終版本的證明。原文保留在本次 ChatGPT 對話；僅已核對確實寫入 Git 原稿檔案者標為 `imported`；不同歷史版本仍可能待比較。不得根據標題或摘要重寫成所謂原稿。使用者送來的「臨床筆記」不自動當作「小麻閱讀已發表正稿」。

| 日期（文章自述） | 原始題名 | 系列／來源標籤 | 內容移轉 |
|---|---|---|---|
| 2026-07-28 | 同樣都是 seizure 持續，為什麼流程圖每往下一格，改變的不只是下一顆藥？ | Status epilepticus 閱讀 | imported → `content/xiaoma-reading/originals/2026-07-28-status-epilepticus.md` |
| 2026-07-26 | 糞便已經變軟，為什麼下一步不一定是再加一顆瀉藥？ | 藥物閱讀（Constipation） | **source_snapshot_archived** → `archive/xiaoma-reading/intake/2026-07-26-constipation-user-supplied.md`；待版本／醫學／出版審查 |
| 2026-07-24 | 同樣屬於 VTE，為什麼可以一起預防，診斷卻必須分開？ | 小麻閱讀（9E） | conversation_only |
| 2026-07-23 | 肝硬化明明由結構定義，為什麼臨床判斷不能只沿著結構前進？ | 小麻閱讀（9E） | conversation_only |
| 2026-07-21 | 找到腹瀉的類型，為什麼仍然沒有找到病因？ | 小麻閱讀（9E） | **source_snapshot_archived** → `archive/xiaoma-reading/intake/2026-07-21-chronic-diarrhea-user-supplied.md`；原圖／醫學審查見 `audit/chronic-diarrhea-2026-10-26-source-and-clinical-review.md`；待正式刊行版本核對與出版 |
| 2026-07-21 | 同一顆 octreotide，為什麼既能止瀉又能促動？ | 藥理學精要閱讀 | conversation_only |
| 2026-07-20 | 利尿效果不夠，為什麼下一步不一定是加量？ | 小麻閱讀（9E） | imported → `content/xiaoma-reading/originals/2026-07-20-diuretics.md` |
| 2026-07-20 | 胰臟已經壞死，為什麼還不一定是 severe acute pancreatitis？ | 小麻閱讀（9E） | imported → `content/xiaoma-reading/originals/2026-07-20-pancreatitis.md` |
| 2026-07-19 | 肝臟被占據，為什麼最突出的卻是 ALP？ | 小麻閱讀（9E）；Cholestasis 續篇 | conversation_only |
| 2026-07-19 | Cholestasis，是主要病理過程，還是其他肝病的結果？ | 小麻閱讀（9E）；肝臟檢驗續篇 | conversation_only |
| 2026-07-19 | 我們看見的是病程，還是病程留下的訊號？ | 小麻閱讀（9E）；chronic HBV 續篇 | **source_snapshot_archived** → `archive/xiaoma-reading/intake/2026-07-19-hbv-signals-user-supplied.md`；附表核讀紀錄 `2026-07-19-hbv-signals-figure-review.md`；待原書 PDF 頁次、授權／醫學審查與出版驗證 |
| 2026-07-18 | HBV phase，不是在替慢性肝炎分期 | 小麻閱讀（9E） | conversation_only |
| 2026-07-17 | 還不知道是什麼，憑什麼治療 | 小麻閱讀（9E）；WCT／ACLS | conversation_only |
| 2026-07-16 | 急性 AF，不一定要立刻結束 | 小麻閱讀（9E） | conversation_only |
| 2026-07-16 | Syncope：以機轉定義，卻從現象開始診斷 | 小麻閱讀（9E） | conversation_only |
| 2026-07-12 | 從四象限走進 LVEDP | 小麻閱讀 | imported → `content/xiaoma-reading/originals/2026-07-12-lvedp.md` |
| 2026-07-12 | Heart Failure：從四象限到診斷與急性失衡 | 小麻&IBCC 閱讀 | imported → `content/xiaoma-reading/originals/2026-07-12-heart-failure.md` |
| 2026-07-11 | Accessory pathway ＆ WPW syndrome | 小麻閱讀（9E） | conversation_only |
| 2026-07-10 | 心肌病變 | 小麻閱讀（9E）；DCM | imported → `content/xiaoma-reading/originals/2026-07-10-dcm.md` |
| 2026-07-07 | ASD 與 PFO | 台北榮總心臟科教學紀錄 | conversation_only |
| 未提供 | 臨床筆記：血管炎 | 臨床筆記／非小麻閱讀 | conversation_only |

既有 `content/xiaoma-reading/originals/2026-07-14-hcm.md` 為先前已核對收錄的 HCM 原稿，不在本次 21 篇直貼計數內。

## 編輯結構（待正文核對後建立）

- HF → LVEDP → DCM／HCM：血流動力學、壓容、結構與症候群
- WPW → WCT／ACLS → AF：導電路徑、危險的主因、急性安全性
- VTE → ASD／PFO：靜脈血栓生成、逆理性栓塞、偶然發現與因果
- HBV phase → ALT 訊號 → cholestasis → ALP／infiltrative hypothesis → cirrhosis：病毒—宿主、肝損傷與肝膽生理多軸
- Diarrhea → octreotide → constipation：分類機轉、藥物介入位置與症狀—病因邊界
- Status epilepticus／diuretics／pancreatitis：策略轉換、治療反應與時間尺度
- Vasculitis：血管尺度 → 器官表型 → 免疫機轉／形態學證據 → 風險與治療；來源類別不同，保留獨立編輯狀態

## 編輯風險

原稿不得默默改寫。涉及藥物、心律不整、急重症、GCA 緊急治療等主張，在公開教學前另建逐條醫學核對。風濕免疫筆記結尾「Rheumatologic diseases are clinical diagnoses, supported by positive autoantibodies」應單獨檢查：自體抗體陰性不排除多種臨床血管炎，陽性亦非確診證據。不要將此句直接提升為網站規範。


### 2026-10-26 增量回收（Constipation）

作者於 2026-10-26 對話再次貼出 2026-07-26 全文，已逐字存入私人 `archive/xiaoma-reading/intake/2026-07-26-constipation-user-supplied.md`（commit `3fa97afb07d50ebdc453033d3efa18fcae0facea`）。這是 **user-supplied source snapshot**，不等於確認 Facebook 已刊版本、`content/xiaoma-reading/originals` 正稿或公開網站頁面。下一步按 EPQC 查核原書圖表及現行 AGA／ACG、ASCRS 來源；特別注意 fecal impaction／mechanical obstruction、defecatory disorder testing 與腰椎骨折相關神經危險徵象。不要依舊的『六篇已入庫、十五篇待移轉』靜態數字判斷新的 source snapshot 數量。


### 2026-10-26 增量回收（HBV phase → ALT 訊號）

作者再貼出 2026-07-19 全文與一張〈Phases of Chronic HBV Infection〉表格圖片。**原稿逐字保存**於 `archive/xiaoma-reading/intake/2026-07-19-hbv-signals-user-supplied.md`（首次保存 commit `e3dc0d941456a6473af32e33548f346c478399e7`）。已逐欄閱讀提供的表格截圖、記錄附件 fingerprint 與 2018/2025 指引門檻差異，詳 `archive/xiaoma-reading/intake/2026-07-19-hbv-signals-figure-review.md`。圖片原始像素**仍僅在對話附件，未搬入 Git**，且尚未對回 Pocket Medicine 9E 原 PDF 完整頁次；不得把摘要當原頁驗收。這是 source snapshot，**並非**已公開的歷史原稿、醫學放行或合法原圖重製。系列閱讀順序維持 2026-07-18〈HBV phase，不是在替慢性肝炎分期〉→ 2026-07-19〈我們看見的是病程，還是病程留下的訊號？〉；前一篇仍另行回收，不能冒稱已保存。
