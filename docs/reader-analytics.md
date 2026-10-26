# Clinical OS — 發布後閱覽分析（v1）

啟用日期：2026-10-26（Asia/Taipei）
正式站：https://sheng-clinical-system.pages.dev/
Cloudflare Pages project：`sheng-clinical-system`
Cloudflare Web Analytics site tag：`fec8c44afd484f3fa4670885ba10dce5`

## 定位與原則

發布前醫學品質審查與發布後讀者行為分析是獨立兩道關卡。流量、停留或來源均不得替代醫學審查，也不得以較少觸及作為刪除醫學重要內容的理由。

### V1 — Cloudflare 原生流量

- Page views：網頁被閱讀的次數，並非唯一讀者數。
- Visits：造訪次數，並非獨立人數、完成閱讀或學習效果。
- 各文章 URL/路徑：分析入口、文章人氣與閱讀需求。
- Referrers：可觀察的外部來源；不代表精準到人的渠道歸因。
- Device：手機、桌機比例，供行動端排版驗收排序。
- Web Vitals（若可取得）：LCP、CLS、INP 等效能訊號。

不把總流量、Requests、Bots 當作真實讀者人數，也不將日誌或假造樣本替代訪客資料。

## 分析節奏

- 每週一產生上週一至上週日（Asia/Taipei）的報告，註記資料可用期間、采樣、缺漏及統計延遲。
- 報告最小集合：page views、visits、前五名文章路徑、週對週比較、來源與裝置占比；能取得才呈現，否則標註未提供。
- 明確分開三類：①可觀察事實；②合理假說；③是否值得安排醫學／排版審查。
- 只把低成本、可驗證且能提升讀者體驗的變動列入建議；不自動修改醫學教材或發布內容。
- 未通過收數驗證前不宣稱已在追蹤實際訪客；啟用前的歷史訪客也無法補回。

## 實作狀態與驗收

2026-10-26 已透過 Cloudflare API 建立 Web Analytics 站點，並設定 Pages 專案的 `build_config.web_analytics_tag` 與 `web_analytics_token`。由於對正式首頁與 DCM 文章實際瀏覽器檢查發現僅靠 Pages 專案原生設定未注入 beacon，本版改由 `site/build.py` 統一對首頁及正式文章 HTML 添加一次 Cloudflare Web Analytics JS。為避免誤記二次瀏覽量，不在舊版轉址頁安裝；由 `tools/check_output.py` 驗證每個正式 HTML 頁恰好一個 beacon。Web Analytics 站點本身的 auto_install=false，採手動注入；已將 Pages 專案的 `build_config.web_analytics_tag` 與 `web_analytics_token` 清空，確保避免平台與原始碼重複注入。參見官方文件：https://developers.cloudflare.com/web-analytics/get-started/。

- [x] Cloudflare Web Analytics 站點已建立
- [x] Cloudflare Pages 曾設定原生 analytics tag/token；經實際 DOM 驗證未生效後已清除，避免重複追蹤
- [x] 手動 beacon 修正版本（main `1f42eeab`）於 2026-10-26 13:55:25 UTC 正式部署成功；Cloudflare Browser Rendering API 確認首頁與 DCM 完整文章各有且僅有一個 beacon，且 token 符合 Web Analytics 站點設定
- [x] Cloudflare GraphQL Analytics API `viewer.accounts.rumPageloadEventsAdaptiveGroups` 已能讀到正式站的 pageview/visits/路徑/裝置資料；2026-10-26 14:00 UTC 起的查詢出現有效資料（初期混有人工及工具驗收流量，僅作鏈路驗證，非自然訪客成效）
- [ ] 個別 beacon HTTP POST 的 2xx 網路結果尚未直接逐次核對（GraphQL 已驗證平台實際有事件資料）
- [x] 已安排 2026-11-02 起每週一台灣時間上午定期分析（首次報告屬啟用後不滿一週資料）
- [ ] 至少一個完整可比較的自然週已累積且完成正式週對週比較

### 資料查詢與上線基準

- 首次確認部署完成：2026-10-26T13:55:25Z（台灣時間 21:55:25）；不要把部署前 Cloudflare 統計、測試瀏覽或 13:55 五分鐘跨界桶直接當作「新追蹤」的自然讀者數。
- 2026-10-26 14:00 UTC 之後有回傳的新資料，可作為 post-release analytics ingestion 的證據；但目前不足以證實「使用者完讀」或「學習有效」。
- GraphQL 資料集：`viewer.accounts.rumPageloadEventsAdaptiveGroups`；以 `siteTag` 指定當前站點，`count` 是 pageview 事件，`sum.visits` 是造訪，`dimensions.requestPath / deviceType / refererHost / datetimeFiveMinutes` 用於摘要。
- GraphQL 可能有采樣、時間桶與來源歸因限制，數據品質須在每份週報分開註記；路徑需先排除 `/xiaoma-plan.html` 等 alias，避免歸因重複。
- 初期人工與工具驗證流量無可靠個人標記可完全排除，因此**不得把最初的數字解釋為真實新讀者或其數量**。

## 後續擴充邊界

追蹤閱讀完成率、跨文章點擊、測驗答題表現屬於事件層，需要額外埋點及相應資料處理。V1 不加入額外資料庫或追蹤識別；不收集姓名、學號、IP、病人／臨床個資，不以任何資料推斷個別讀者。

## v1 數據契約與週報 QA（2026-10-26 補充）

本網站採用最小化的 **Cloudflare GraphQL → 排程週報**，不需要新增瀏覽追蹤資料庫。從 `viewer.accounts.rumPageloadEventsAdaptiveGroups` 讀取資料，至少以 `siteTag=fec8c44afd484f3fa4670885ba10dce5` 及 `requestHost=sheng-clinical-system.pages.dev` 限定正式環境；預覽部署與轉址 alias 不列入正式站統計。

1. 指標契約：`count` 為瀏覽事件數，`sum.visits` 為 Cloudflare 的 visits 指標；兩者均**不可**寫成獨立人數、學習完成率或理解率。維持原始期間與時區，首週（2026-10-26 至 11-01）為部分週，不做不對稱的週對週增幅。
2. 路徑比對：GraphQL `requestPath` 常省略 `.html`，先以 / 開頭正規化並對照 `site/pages.json` 的 `output`（去掉 .html），再將首頁／導覽／年度詳解索引與單篇文章分開。只用實際的 catalog 對照，不憑猜測組題號。
3. 來源：`refererHost=sheng-clinical-system.pages.dev` 為**站內導航**，非外部導流；`l.threads.com` 為 Threads 外部 referrer；空來源標註為「來源不明／可能直接開啟」，不宣稱都是 Direct。
4. 裝置與機器：按 `deviceType` 觀察手機／桌機／平板比例。即使 `bot=0`，也無法排除作者自己打開網站、第三方自動化驗收或其他 JavaScript 瀏覽器；前期不得解讀為自然讀者數。
5. 缺口揭露：Cloudflare 事件資料可能有抽樣、延遲、缺漏與低樣本風險，週報須標註。有資料不足時寧可回報「暫不可判讀」，也不編造原因或轉換率。不得為追蹤而收集姓名、IP、學號或病人個資。

### 上線初始驗證快照（非正式成效報告）

2026-10-26 正式上線後的 GraphQL 即時快照：**51 pageview events、22 visits**；當中 `/xiaoma-internal-medicine` 目錄入口有 29 次瀏覽（不是 29 名讀者），`/xiaoma-exams` 年度詳解索引有 7 次。依裝置分：mobile 25、desktop 24、tablet 2（分母為 51 個事件）。依 referer 分：本站內跳轉 29、`l.threads.com` 14、來源不明 8（均為事件數）。資料包含可能的驗收與作者自測，**只能驗證收數鏈路、閱讀入口與手機需求的觀察方向**，不能解讀為自然讀者量或文章的教學成效。初期數值隨資料累積而變動。

這組資料顯示：**文章與導覽不能混排**。若只列「前五熱門頁」，會被題庫／目錄入口掩蓋。週報須先報站點入口頁，再獨立列正式教材文章；樣本不足時不給品質高低排名。
