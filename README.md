# Clinical System — Medical Knowledge & Editorial Site

**Cardiac Tamponade Mimicking Sepsis** 是首個端到端教材實例；不是整套 Clinical OS 的終點，也不是把既有網站堆疊到一起。

正式知識來源只有 \`content/*.md\`。GitHub 保存版本差異、來源審查及發布歷史；GitHub Actions 由 Markdown **自動生成 HTML 站點**，無須人工維護平行 HTML 教材。

## 閱讀與維護

- [Tamponade 深化教材](content/tamponade.md)：原有八單元 + 2025 ESC 原始圖表對讀 + 反事實推導。
- [ESC 2025 圖表核對](audit/esc2025-figure-check.md)：Figure 12、Recommendation Tables 12／21、Table 17 來源定位及疑義。
- [可追溯審查](audit/audit-log.md)：資料忠實性、風險與未完成事項。
- [既有版封存](archive/tamponade_r2_baseline.md)：原材料；不作新的正式內容來源。
- [歷史編輯狀態檔](archive/editorial_state_r2_audited.json)：只作歷史可驗證快照，非持續全域 Claim Graph。

## 自動網站流程

\`\`\`
修改 content/*.md 或 audit/*.md
     ↓
GitHub push main
     ↓
Actions → Python validators
     ↓
Markdown 轉靜態 HTML、建立搜尋索引
     ↓
GitHub Pages 部署（需帳戶支援且 Pages Source 設為 GitHub Actions；目前首次部署 API 404，請開啟 [Settings → Pages](https://github.com/sheng-web-OS/Clinical_system/settings/pages) 啟用）
\`\`\`

預期 GitHub Pages 路徑：\`https://sheng-web-OS.github.io/Clinical_system/\`。**這只是預期 URL；必須實際部署與 HTTPS 確認，才可宣稱網站可訪問。** 注意此儲存庫目前為 private；是否允許 private repository 啟用 Pages，取決於 GitHub 帳號方案與 Pages 設定，且 Pages 網址本身可能公開。

手動重現建置：

\`\`\`bash
python -m pip install -r requirements.txt
python tools/validate.py
python site/build.py
python -m http.server --directory dist 8000
\`\`\`

教材編輯時請維持病例事實、指南條件、機轉推理與個別行動建議的清楚區分。改變核心機轉時，才按需檢索相關章節、臨時重建依賴並再審查，不強制持續維護全域主張圖譜。

本網站供專業醫學學習，並非個別病患診療建議；未宣稱已經真人專科審查。


**2026-10-21 發布阻擋**：初次 GitHub Actions [#1](https://github.com/sheng-web-OS/Clinical_system/actions/runs/39522812463) 成功產生站點 HTML，但 Pages 部署回傳 404。需由儲存庫擁有者在 [Settings / Pages](https://github.com/sheng-web-OS/Clinical_system/settings/pages) 開啟 Pages 並將 source 選為 GitHub Actions。此私人儲存庫在目前方案是否允許 Pages 需依介面實際顯示確認；不要為了部署擅自改為 public。


## 發行事實（2026-10-21）

[第 2 次 Actions](https://github.com/sheng-web-OS/Clinical_system/actions/runs/39523560239) 已通過網站編譯與建站後的站內相對連結檢查；但 Pages 仍未啟用，deploy 因 404 失敗。請到 [GitHub Pages Settings](https://github.com/sheng-web-OS/Clinical_system/settings/pages) 啟用後，手動 Run workflow 或推送下一次教材更新。預覽可使用當次 Actions 的 github-pages artifact，或會話交付的單檔 HTML／完整網站 ZIP。切勿把可下載 artifact 誤當已發布網址。
