# Tamponade r3 發行與可追溯審查

日期：2026-10-21。範圍：原有 8 單元 + ESC 2025 圖表核對及病例反事實推導（新增第 9、10 章）。

**目前發布狀態：Cloudflare deployment succeeded / public HTTPS verified。** 正式網站：[sheng-clinical-system.pages.dev](https://sheng-clinical-system.pages.dev/)。下列 GitHub Pages 阻擋紀錄是歷史事件；最新驗收見文末「Cloudflare 正式部署與公開驗證」。

## 基線與版本

- Baseline：\`archive/tamponade_r2_baseline.md\`，原先 399 行主教材。
- Legacy evidence：\`archive/editorial_state_r2_audited.json\`，先前 26 條主張與三項 P2、原文件證據等的封存紀錄（原樣保存）。
- Current source：\`content/tamponade.md\`，Markdown 為唯一網站內容來源。出版前跑 \`tools/validate.py\`；由 Actions 生成 HTML，並非人工維護第二份教材。
- 未更動原有 Clinical OS、v4.12 原檔或已發布教材；此 GitHub 儲存庫原先只有 README。

## 本次新審查結果（非「獨立真人專家審查」）

| ID | 問題／風險 | 依據 | 修正 | 結果 |
|---|---|---|---|---|
| R3-001 | 原教材指向不存在的 \`assets/echo_figure20.jpg\`，會顯示破圖 | 原文 U04 | 改指向 PMC Figure 20 真正來源，清楚聲明非原病例影像；不自行重製版權圖 | 已在來源修正；頁面建置待 CI 驗證 |
| R3-002 | Figure 12 的「≥6」與「>6」易被誤當確定單一規則 | ESC Figure 12 圖像、圖註與 §6.3.2.1 | 保留原文不一致，將評分定位為輔助，凸顯 §11.8.3 不穩定者緊急引流 | 來源核對完成 |
| R3-003 | 病例可能被回溯補造實際穿刺量、RV collapse、引流時間 | Azim 2010 原文與 r2 基線 | 延續原有缺失資料警示；禁止將 ESC 常規倒填個案 | 已核對教材文字 |
| R3-004 | 3–6 天可能被誤泛化至所有心包填塞 | ESC Recommendation Table 21 | 僅限疑似／確定腫瘤性心包積液，標註 I/B | 已核對 |
| R3-005 | 圖文版權／不能保證鏡像可用 | ESC 出版使用條款、原有外部圖 | 只連結原文而不在站點直接重製；外部資源不計為已本地保存 | 已納入發布範圍 |
| R3-006 | 網站能構建 ≠ GitHub Pages 已真正公開／載入 | GitHub Actions/Pages | 將 CI、發布環境、實際站點存取分別驗收 | 首次 Actions 的 build、校驗與 artifact 上傳成功；deploy 遭 GitHub Pages API 404（未啟用 Pages 或未配置可用）。需啟用 Pages 並再次遠端驗收 |

## 重要主張的 Traceability（最小可重建證據）

| 教材位置 | 主張概要 | 直接來源 | 主張性質 |
|---|---|---|---|
| U02 | 45 歲女性及血流動力學資料、診斷轉折 | Azim 2010 原病例 [1] | 病例事實 |
| U03 | CVP 不等於跨壁充盈壓；快速惡化生理 | ESC 2025 §11.8、Klein 2024 [2,7] | 機轉推理 |
| U04 | Echo 證據須與臨床灌流整合 | ESC 2025 Table 17 [2]、Mercé 1999 [6] | 證據綜合 |
| U05 | 不穩定 CTP 不應延誤引流 | ESC 2025 §11.8.3、Rec Table 12 [2] | 指南推薦 |
| U05 | sepsis 30mL/kg 是有條件且應個別評估 | SSC 2026 official recommendation [3] | 另一適用族群指南 |
| U06 | 惡性積液 3–6 天延長引流 | ESC 2025 Rec Table 21 [2] | 指南推薦 |
| §9 | Figure 12 score ≥6 vs >6 | ESC 2025 Fig 12／圖註／§6.3.2.1 | 原始文件歧異 |
| §10 | 反事實條件下不能沿用舊機轉 | U01–U06，ESC 2025 [2] | 教學推理，不代表原病例觀察 |

## 驗收與限制

**醫學資料審查**：指定來源中的 ESC 主要推薦、Figure 12 原圖與 Table 17 原表已對照；r2 報告先前 AI 獨立脈絡審查曾關閉三項 P2，但本輪沒有重現該獨立受試實驗。尚未有專科醫師的外部醫學審查或學習成效驗證。

**網站結構**：以 CI 檢查內容、連結路徑、Figure 12 核對檔與內容存在；真正網站上線須由 Cloudflare Pages 服務回報部署成功，並以 HTTPS 存取確認。開發端工具的文字輸出，不足以證明公開站已可閱讀。

**未解問題**：原始 ESC Figure 12 兩種門檻符號的內部差異屬 upstream ambiguity；採明示處理，不臆測修正版。若後續發現 ESC erratum，應重新核對原圖與受影響教學章節。


## 技術驗證補遺（2026-10-21）

GitHub Actions run [#1](https://github.com/sheng-web-OS/Clinical_system/actions/runs/39522812463) 的 build 工作已成功，並產生 `github-pages` 發行檔；然而 deploy 顯示 **404 Not Found / Ensure GitHub Pages has been enabled**。發行狀態因此為 **build passed / deployment blocked**，不是 published。網站採靜態 Markdown 編譯，並已新增產出 HTML 的路徑驗證，以防原先 Markdown 相對連結在 HTML 根目錄失效。Figure 12 與 Table 17 已重新檢視原 PDF 頁面圖像；Table 12／21 僅能宣稱文本核對。


## 發行驗收：第二輪建置

2026-10-21 GitHub Actions [run #2](https://github.com/sheng-web-OS/Clinical_system/actions/runs/39523560239)（commit \`62e5a1e1ebafb2879a0ce8bb1d1c59d8832c8b08\`）：build、結構稽核、Markdown 編譯及 artifact 上傳全部成功。發行檔內具有首頁、兩份審查頁、CSS、JS、搜尋索引與無 Jekyll 設定。檢查產物確認 8 個原有 U01–U08 定位點、6 張原生因果節點、12 個章節導航，未見原始 Markdown 相對連結殘留，JS 語法檢查通過，HTML 沒有重複 ID。

**部署狀態：阻擋。** 同一次 workflow 的 deploy 仍回傳 GitHub API HTTP 404，訊息明確要求先啟用 [Pages 設定](https://github.com/sheng-web-OS/Clinical_system/settings/pages)。因此不得把目前狀態標示為 published 或 live。驗證成品可作本地單檔／多檔網站預覽，尚未完成公開 HTTPS 網址存取或實際圖形瀏覽器截圖檢查（執行環境的瀏覽器頁面載入被安全限制攔阻）。

**最低人為介入**：由儲存庫管理員在 Pages 設定選擇 GitHub Actions 為發布來源。依 GitHub 官方說明，GitHub Free 帳戶下私人 repo 不支援 Pages；私人 repo 需要 GitHub Pro／Team 等適用方案。是否公開 repo 屬資訊揭露決策，不得由 Agent 自動變更。


## 出版平台變更：GitHub 私人原始碼 → Cloudflare Pages 公開閱讀

日期：2026-10-21。方案選定 Cloudflare Pages Free 與 GitHub private repository。原 GitHub Pages API 404 部署流程被移除；GitHub Actions 只做品質檢查及可下載 HTML 產物，不再使用 GitHub Pages API。Cloudflare Pages 連接 main 分支，自行執行相同的驗證與建站腳本，任何檢查失敗皆阻擋本次 Cloudflare 建置。

發布狀態必須分辨：source committed、CI passed、Cloudflare deployment succeeded、public HTTPS verified。GitHub Actions 成功不等於 Cloudflare 已連接或正式站已上線。需擁有者在 Cloudflare 與 GitHub 授權安裝 Pages GitHub App，並確認實際 pages.dev 網址可讀。

安全邊界：僅 dist/ 編譯好的教材 HTML、CSS、JS、索引公開；archive/、原始 Markdown、編輯狀態 JSON 與 Git 歷史仍在私人儲存庫，不當作網站原始檔發布。請注意公開審查頁本身的內容仍可被任何人閱讀，來源的私有 Git 歷史無法由一般訪客查閱。

## Cloudflare 正式部署與公開驗證（2026-10-21）

使用者已授權 Cloudflare Workers and Pages GitHub App，範圍僅限私人 repository `sheng-web-OS/Clinical_system`。建立前以控制台與 API 確認帳號內無既有 Pages 專案；網頁建立流程曾回傳未具體說明的錯誤，重新確認清單為空後，改用已連接的 Cloudflare API 建立，未重複建立專案。

| 驗收層 | 實際證據 | 結果 |
|---|---|---|
| 原始碼 | commit `5ddacac531cf68162cb09aa971023a5a34ce89cf`；repository visibility = private | 已確認 |
| GitHub CI | [run 39526159420](https://github.com/sheng-web-OS/Clinical_system/actions/runs/39526159420)，completed / success | 通過 |
| Cloudflare | project `sheng-clinical-system`；production deployment `a9afe82b-c08c-40fe-af45-d7206974829a`，clone、build、deploy 均 success | 通過 |
| 完成時間 | 2026-10-21 11:56:16（Asia/Taipei，平台原始時間 03:56:16 UTC） | 平台回報 |
| 正式 HTTPS | [正式網站](https://sheng-clinical-system.pages.dev/) 與 [不可變部署網址](https://a9afe82b.sheng-clinical-system.pages.dev/) | 正式站實際存取已通過 |
| 公開頁面 | 首頁、ESC 審查、審查紀錄均回傳 HTTP 200；.html 路徑正常導向乾淨網址 | 通過 |
| 站內引用 | 三頁全部 42 個站內連結／資產引用、19 個不重複章節定位；CSS、JS、搜尋索引內容類型正常 | 通過 |
| 互動 | 章節點擊跳轉；以 tamponade、ESC 搜尋得到三頁結果，並實際開啟審查頁 | 通過 |
| 私人來源邊界 | 原始 Markdown、archive、.git/config 的探測回應與首頁 HTML 完全相同（Pages fallback），未返回原始檔 | 未洩出來源 |

專案設定：production branch `main`；build command `bash tools/build_site.sh`；output `dist`；根目錄留空；`PYTHON_VERSION=3.12`，首次日誌實際安裝 3.12.12；正式分支自動部署開啟；`preview_deployment_setting=none`；PR 自動留言關閉。網站為純靜態內容，該部署 `uses_functions=false`。

外部連結：ESC 官方指南頁與 Myocarditis Foundation 原指南 PDF 回傳 HTTP 200；DOI 可解析到出版社，但自動化請求最終回傳 HTTP 403，因此記為出版社存取受限，沒有宣稱完整期刊頁可讀。連結存取檢查不等同重新醫學審查；原先指南符號歧異及真人同儕審查限制仍保留。

後續變更已納入版本追蹤：手機初驗發現表格固定最小寬度造成整頁橫向溢出，故修正表格自身的捲動範圍；另依使用者原文新增私人架構原則文件。未修改醫學內容、品質驗證器或公開發行白名單。以上成功部署證據對應所列 commit；紀錄與版面更新會由 main 再觸發自動部署，須以新提交對應的 Cloudflare 狀態及公開頁面另行驗證。

## 小麻內科國考納入既有網站（2026-10-21）

新增學習入口、82 日核心路線、122 個參考書章節定位與第一天「低血氧」教材。個人輪訓／出遊／學習紀錄及完整原始計畫留在私人來源；公開產物只含去除個人行程的路線、原創教學與來源連結，不附教科書 PDF。

第一天教材承接已完成的作者來源查核：Pocket Medicine 第九版 PDF 79、105–106；115 年第二次醫學（三）第 3、9 題，及同次官方標準與更正答案。教學 ABG 數值明標自編並驗算；官方答案後置為原生可展開區塊。未新增醫學結論，沒有獨立真人專科審查或學習成效資料。

出版目錄改由明列清單驅動，未改為掃描或發布整個儲存庫。保留原 Tamponade 的來源與 8 個單元驗證；擴充至所有公開頁的連結／錨點檢查，並加入私人 archive、路徑越界、符號連結、重複目的頁、日期與實際審查類型的 9 個邊界測試。原文與私人原檔保全、來源驗證、完整建置、發行白名單及 9 個測試均在本地通過。

新教材透過同一出版清單加入入口及全文搜尋；相關工程檢查不等同醫學正確性或未來排程執行成功。每次發布仍需核對對應 Git commit 的 Cloudflare 狀態與實際 HTTPS。



## 2026-10-21｜小麻歷史原稿回收

在既有網站加入小麻閱讀入口及 HCM 完整原稿。原稿取回後逐位元組保存，出版目錄記錄 SHA-256，建置時會阻擋未說明的原文變動。閱讀頁使用精簡頁首、可展開目錄及獨立來源註記；個人檢索識別、對話時間定位與原始來源檔案留在私人 archive。

搜尋涵蓋 223 筆可讀文件／壓縮檔、歷史對話、已連結筆記、Drive 與相關 GitHub 工作庫。結果為一篇完整回收，十筆文章／主題線索待取得全文或確認完稿；不把摘要、模板或比較紀錄發布成原文。詳見[原稿回收核對](xiaoma-reading-recovery.md)。

本次是來源回收與網站整合，並完成明列範圍的 HCM 原稿校讀；未宣稱已重新審查所有醫學主張、完成所有歷史稿件遷移或通過學習效率試驗。
