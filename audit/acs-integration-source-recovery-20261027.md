# ACS 網站整併｜來源回收與出版邊界（2026-10-27）

## 本次實際完成

- 對象：[ACS｜理解與臨床判斷](https://acs-deep-learning.dreamycarp4.chatgpt.site/)，其首頁目前聲明四章、27 核心＋6 延伸及原講者宋偉廷醫師 150 頁課程對照。本儲存庫原先 `site/pages.json` 無獨立 ACS 入口。
- 取得公開可讀的 `/data/units.json`，由第三方擷取器轉成 HTML 文字，再以單元 JSON 邊界逐個解析（**不是對原始檔 byte-preserving 的下載**）。已驗 31 個完整 JSON 物件，序號 02–32：建立診斷 5 節、ECG 10 節、治療 11 節、MI 後 5 節。
- 單元 01 與 33 在 HTML 清洗時分別丟失物件開頭／結尾：首次僅有 **31/33 個完整可解析的單元 JSON**。其後瀏覽器代理讀回兩節的結構化資料（保存在 `archive/acs/site-recovery/2026-10-27-boundary-units-browser-capture.json`），因此**33/33 個單元的主題與主要正文已有研究擷取**；但是核對發現「追序列 cTn」被改成「追文字列 cTn」、課程只有 150 頁卻虛構 p.151–154、以及 p.149 劑量表被扁平化。修正證據見 `archive/acs/site-recovery/2026-10-27-boundary-reconciliation.md`。目前**原始位元組保真仍只有 0/33**，不可稱來源原檔完整備份或作者確認版本。
- 保存四份私有、可逐節閱讀的研究稿在 `archive/acs/site-recovery/`（完整解析 31 個），另存首尾兩節的**帶差異旗標的瀏覽器擷取稿與來源對照**；研究稿記有 question / answer / 教學段落 / 文獻 URL / PPT 頁碼 / figure caption / cautions / selfCheck / 推理界線。這些是格式轉換後的**研究擷取稿**，不是作者認可定稿、原始 JSON 或原站程式碼。
- 新增 Clinical System 的 ACS 因果導航頁 `content/clinical-os/acs.md`，連回原站全 33 單元，以及本站 HF／LVEDP／DCM 與國考練習，不冒充為完整原站本地鏡像；並在唯一知識地圖 `#chest` 加入路徑。

## 圖、互動與來源的不可混同

- **原站 figure metadata 有回收**（原投影片頁次與圖說），**原始醫學影像、ECG、原始講者 PPT、原網 JS widgets/case/engine、150 頁原投影片未複製**。不可在新站宣稱原圖已發布或已有原網同等互動。
- 原圖究竟由原講者原創、學術論文、原投影片引用或第三方教材提供，目前沒有逐項權利核查；不得透過把每個 figure caption 變成空連結冒充圖已存在。
- 原站來源 URL 與 `cautions` 狀態屬**原站原有註記**；本次未逐一核對所有 guideline 全文、原始試驗、Figure、表格、圖說、腳註，亦沒有獨立醫師審查。原資料中的數字、劑量、適用情境留待醫學審核，不因成功解析 JSON 而獲批准。
- 這次新增的公開候選 **僅** `content/clinical-os/acs.md` 是由本站自編的跨篇閱讀入口；不以 `kind=ai_integrated` 的教學文章名義放行那 31 份未核對的舊稿。所有擷取草稿只存在 `archive/`，不得進入 Cloudflare `dist`。

## 完成 ACS 本地整合的必要條件

1. 用不經 HTML sanitizer 的來源出口取得 **33/33 原始 JSON 單元與 site asset manifest**，確認版本、原文段落、內部連結、表格及公式；不得以瀏覽器代理自行概述與 `content_complete=true` 代替全文保真。
2. 逐個追查對臨床決策有影響的原始 ECG、導管影像、血流／導程示意、2025 AHA/ACC 與 2023 ESC ACS 指引圖表；核查其權利、放大閱讀、圖說及最低可讀寬度。外部連結可作原課導航，但不能取代讀者需要的決定性圖。
3. 重建四章共用的診斷與治療脈絡；清楚標記被保留的原站推導、本站真正的新增橋樑、需更正的臨床誤讀；經 EPQC 七軸、P0/P1、危急處置和 antithrombotic 風險檢查，才能把 31＋2 私稿逐篇列入公開教材。
4. 跑既有 `bash tools/build_site.sh`、unittest、網站實際桌面／360px／390px 及鍵盤／圖像放大 QA；GitHub CI 通過與 Cloudflare production 部署、HTTP 可讀各自獨立記錄。
5. 完成前，此 PR 應保持 **Draft / CONTENT HOLD**。此用戶指令是繼續整併，**不是直接核准原課第三方圖的重製，也不是本次將 31 份未審稿發布到正式站。**

## 避免與並行工作衝突

僅增設獨立 `content/clinical-os/acs.md` 與私有 `archive/acs/` 快照，對 `content/clinical-os/index.md` 的胸痛入口新增短銜接，不改既有 HCM、HF、LVEDP、DCM、心律與國考文章，也不建立第二份知識地圖或第二個國考年度資料庫。只有一條新的 `site/pages.json` reader 入口，避免將 31 份原資料冒充現行已審核教材。


## 2026-10-27 ACS 正式國考雙向整合追加

- 直接對讀考選部原卷及**更正答案 PDF**：113（二）醫學（三）Q6 = **D**；114（二）醫學（三）Q6 = **C**、Q9 = **A**，三題均**未更正**。原卷及更正連結保存在 `content/xiaoma-internal-medicine/acs-exam-sources.md`。
- 兩份深入詳解已寫在 `content/xiaoma-internal-medicine/exams/113-2-med3-acs-q6.md` 和 `.../114-2-med3-acs-q6-q9.md`；不覆蓋原本 108（一）Q76。官方原卷沒有重製成公網 PDF，也沒有把自編反事實當官方題。
- 依既有 `site/exam_archive.py`、`site/pages.json` 設定唯一身份與 `related_exams`，由相同紀錄生成**年度題目→ACS 導讀章節**反向連結，無第二套索引；ACS 章節正文也有**ACS→真題**的直接連結。
- **新證據必須反向修訂舊文：**[2026 Fifth Universal Definition of MI](https://pmc.ncbi.nlm.nih.gov/articles/PMC13523810/) 已以 primary／secondary／procedure-related MI 取代 Type 1–5 的數字分類。113（二）Q6 依舊規 D 正確，但在 2026 臨床不能再使用「Type 5＝cTn >10×」單獨確診，亦不能將術後 cTn 升高直接當作 procedure-related coronary complication。本次先在 ACS 導讀與該題詳解**明示改判**；原站 33 個單元逐篇更正仍列醫學審查待辦。
- **治療時點的另一項重要限定：**114（二）Q6 官方 C；題目 B 所說 6 個月 DAPT「可能」成立，但 2025 ACC/AHA ACS 無高出血風險之**預設 ≥12 個月**，不能因題目未選 B 就將 6 個月一律停藥。
- ECG 必要波形尚未有新的**同時完成原圖目視、正式題號／答案核對、影像公開合法性**的官方題，因此本次不假造一題作為已收錄的 ECG 真題。網站來源圖的補救仍需另行完成。

**工作邊界：** 上述為可由 CI 測試的官方題目**出版候選**與循環閱讀，並非已對 33 節原課完成圖像、臨床、互動或公開可讀驗收；在 PR #123 Draft 狀態不自動發布。
