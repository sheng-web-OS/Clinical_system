# ACS 網站整併｜來源回收與出版邊界（2026-10-27）

## 本次實際完成

- 對象：[ACS｜理解與臨床判斷](https://acs-deep-learning.dreamycarp4.chatgpt.site/)，其首頁目前聲明四章、27 核心＋6 延伸及原講者宋偉廷醫師 150 頁課程對照。本儲存庫原先 `site/pages.json` 無獨立 ACS 入口。
- 取得公開可讀的 `/data/units.json`，由第三方擷取器轉成 HTML 文字，再以單元 JSON 邊界逐個解析（**不是對原始檔 byte-preserving 的下載**）。已驗 31 個完整 JSON 物件，序號 02–32：建立診斷 5 節、ECG 10 節、治療 11 節、MI 後 5 節。
- 單元 01 `pathology/diagnosis` 的物件開頭在第一次 HTML 清洗時被截除；單元 33 `postmi-inflammation` 尾端在 HTML 清洗時被截除。雖有部分正文片段，**兩者不當作完整回收；不可補造缺漏來源欄位**。
- 保存四份私有、可逐節閱讀的研究稿在 `archive/acs/site-recovery/`，保留 question / answer / 原始教學段落 / 文獻 URL / PPT 頁碼 / figure caption / cautions / selfCheck / 推理界線。這些是第三方格式轉換後的**研究擷取稿**，不是作者認可定稿或原站程式碼。
- 新增 Clinical System 的 ACS 因果導航頁 `content/clinical-os/acs.md`，連回原站全 33 單元，以及本站 HF／LVEDP／DCM 與國考練習，不冒充為完整原站本地鏡像；並在唯一知識地圖 `#chest` 加入路徑。

## 圖、互動與來源的不可混同

- **原站 figure metadata 有回收**（原投影片頁次與圖說），**原始醫學影像、ECG、原始講者 PPT、原網 JS widgets/case/engine、150 頁原投影片未複製**。不可在新站宣稱原圖已發布或已有原網同等互動。
- 原圖究竟由原講者原創、學術論文、原投影片引用或第三方教材提供，目前沒有逐項權利核查；不得透過把每個 figure caption 變成空連結冒充圖已存在。
- 原站來源 URL 與 `cautions` 狀態屬**原站原有註記**；本次未逐一核對所有 guideline 全文、原始試驗、Figure、表格、圖說、腳註，亦沒有獨立醫師審查。原資料中的數字、劑量、適用情境留待醫學審核，不因成功解析 JSON 而獲批准。
- 這次新增的公開候選 **僅** `content/clinical-os/acs.md` 是由本站自編的跨篇閱讀入口；不以 `kind=ai_integrated` 的教學文章名義放行那 31 份未核對的舊稿。所有擷取草稿只存在 `archive/`，不得進入 Cloudflare `dist`。

## 完成 ACS 本地整合的必要條件

1. 用不經 HTML sanitizer 的來源出口取得**33/33 完整單元**與所有 site asset manifest，確認原站修訂時間與版本、原文段落、內部連結、表格及公式在轉換中無遺失。
2. 逐個追查對臨床決策有影響的原始 ECG、導管影像、血流／導程示意、2025 AHA/ACC 與 2023 ESC ACS 指引圖表；核查其權利、放大閱讀、圖說及最低可讀寬度。外部連結可作原課導航，但不能取代讀者需要的決定性圖。
3. 重建四章共用的診斷與治療脈絡；清楚標記被保留的原站推導、本站真正的新增橋樑、需更正的臨床誤讀；經 EPQC 七軸、P0/P1、危急處置和 antithrombotic 風險檢查，才能把 31＋2 私稿逐篇列入公開教材。
4. 跑既有 `bash tools/build_site.sh`、unittest、網站實際桌面／360px／390px 及鍵盤／圖像放大 QA；GitHub CI 通過與 Cloudflare production 部署、HTTP 可讀各自獨立記錄。
5. 完成前，此 PR 應保持 **Draft / CONTENT HOLD**。此用戶指令是繼續整併，**不是直接核准原課第三方圖的重製，也不是本次將 31 份未審稿發布到正式站。**

## 避免與並行工作衝突

僅增設獨立 `content/clinical-os/acs.md` 與私有 `archive/acs/` 快照，對 `content/clinical-os/index.md` 的胸痛入口新增短銜接，不改既有 HCM、HF、LVEDP、DCM、心律與國考文章，也不建立第二份知識地圖或第二個國考年度資料庫。只有一條新的 `site/pages.json` reader 入口，避免將 31 份原資料冒充現行已審核教材。
