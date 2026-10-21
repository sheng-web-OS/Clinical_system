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
GitHub Pages 部署（需帳戶支援且 Pages Source 設為 GitHub Actions）
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
