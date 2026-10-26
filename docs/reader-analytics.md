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

2026-10-26 已透過 Cloudflare API 建立 Web Analytics 站點，並設定 Pages 專案的 `build_config.web_analytics_tag` 與 `web_analytics_token`。Cloudflare Pages 將於**下一次成功部署**將 JS beacon 加入有效 HTML 頁面（參見官方文件：https://developers.cloudflare.com/pages/how-to/web-analytics/）。

- [x] Cloudflare Web Analytics 站點已建立
- [x] Cloudflare Pages 專案已配置原生 analytics tag/token
- [ ] 新部署成功且包含追蹤程式（需查 deployment 或頁面 beacon）
- [ ] 讀者端 beacon 回傳成功與 Dashboard／GraphQL 出現有效 pageviews
- [ ] 至少一週有可比的資料並產生完整週報

## 後續擴充邊界

追蹤閱讀完成率、跨文章點擊、測驗答題表現屬於事件層，需要額外埋點及相應資料處理。V1 不加入額外資料庫或追蹤識別；不收集姓名、學號、IP、病人／臨床個資，不以任何資料推斷個別讀者。
