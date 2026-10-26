# HBV 圖文修訂：以關係取代卡片摘要

日期：2026-10-27（Asia/Taipei）。輸入：正式 main `ee66409ddff610d49ddce46444caad0f5f15a8a6`，使用者指出〈HBV phase，不是在替慢性肝炎分期〉的原創圖無法呈現原脈絡。

## 失敗與限定修復

原圖以 `original-list` 將 phase／stage／prognosis 三段摘要排成卡片，沒有畫出四種 phase 的分類軸、HBeAg-negative 的分岔或相同 phase 下的結構差異。舊門檻證明 figure 存在、出處可追查及手機不溢出，沒有證明語義與教學關係完整；不得將這些檢查冒稱圖像品質通過。

本輪修訂兩篇 HBV、四張圖；其餘文章未作全面視覺驗收，不宣稱全站原創圖已修好。不增加模型 API、常駐 agent、圖表 registry 或新的自評分數。

| 圖 | 讀者現在可直接看到的關係 | 限制 |
|---|---|---|
| Phase 四格 | HBeAg 表現型 × 肝炎活動；高 DNA 可與正常 ALT 並存 | 典型組合不是單次 ALT 分類器；不表示嚴重度或時序 |
| 陰轉後路徑 | HBeAg seroconversion 後可持續低活動，亦可有持續／再現肝炎 | 箭頭不表示機率、必經歷程；低活動仍可能再活化 |
| 相同 phase、不同 stage | 固定當前 markers，只有 cirrhosis 條件改變，治療／監測前提隨之改變 | 非真實病例；未見顯著 fibrosis 不等於一律不治療 |
| DNA／ALT 機轉 | 病毒複製與細胞受傷對應不同量測，經宿主互動中介 | 不畫 DNA → ALT 固定比例，不直接量測免疫狀態 |

## 來源與醫學邊界

- 本輪實際目視使用者 Pocket Medicine 9E PDF 第 140–141 頁，包含完整 phase table、ALT 註腳與 variable fibrosis；未把摘要重建成原表，也未公開原書像素。
- 重新讀回 IDSA 官方 AASLD/IDSA 2025 完整文件的 Core Concepts、immune-tolerant／indeterminate 條件與 HCC surveillance 文字。EASL 出版社全文本輪回傳 403；相關治療條件沿用上一輪接受稿的來源審查，未新增門檻或冒稱本輪重新取得原始 Figure 1。
- 新圖屬 B（已解釋概念的可見連結），圖說限定屬 D；未將 phase ≠ stage 等作者原有洞見當成新發現。圖像來源頁與 figure-gate 逐圖用途同步更新。
- 保留所有歷史原稿；只改 AI 整合稿、圖解 CSS、來源頁及本次稽核。無真人專科同儕審查或學習成效實驗宣稱。

## 驗證

初輪 68 項 unittest 通過，公開來源／目錄／輸出檢查通過。Chrome 已目視桌面四格、390px iframe 四格及 360px iframe 的陰轉／stage 分岔；iframe 扣除捲軸後內容寬分別為 375／345px，已檢查頁面與圖形無水平溢出。同輪已目視 390px 訊號機轉圖與 360px 四格；四圖與頁面均無水平溢出。修正窄螢幕 HBeAg 欄名斷行、刪除無資訊色帶、縮短圖說。深色主題按鈕在 iframe 預覽未產生可確認狀態變更，未將其記為通過。

整合並保全同期 main `13478139a28f720da8f5f0d3d3ec8cac80e70263` 的新稿與心律不整修訂；figure-gate 僅更新兩篇 HBV 的既有記錄，未覆寫其他審查。基於該版重新執行正式 build 成功。正式部署結果另以 GitHub／Cloudflare 狀態及 HTTPS 核實，不在接受前預先標記上線。
