# Clinical System — Agentic Medical Knowledge & Editorial System

**GitHub 保持私人；醫學教材網站可免費公開閱讀。**

此儲存庫是 Master Prompt v5.1 的版本化知識來源；Cardiac Tamponade 是第一個端到端教材驗證案例，不是系統的終點。

## 來源與審查

- [Tamponade 完整教材](content/tamponade.md)：既有八個教學單元、2025 ESC 原始圖表對讀、反事實推理。
- [2025 ESC 圖表核對](audit/esc2025-figure-check.md)：Figure 12、Table 17、Recommendation Tables 12／21。
- [可追溯審查](audit/audit-log.md)：版本、證據、已知歧義與驗收限制。
- [歷史原稿](archive/tamponade_r2_baseline.md)：原材料封存，不再當作正式編輯來源。

## 目標工作循環

```text
ChatGPT 對話 / Work / Codex：研究、修訂教材、審查
                 ↓
GitHub private / main：Markdown 與版本歷史
                 ↓
Cloudflare Pages：驗證 → 編譯 → 免費公開網站
                 ↕
GitHub Actions：相同驗證器，獨立 CI 與預覽成品
```

Cloudflare 先執行 `bash tools/build_site.sh`。若來源檔案檢查、網站編譯或發行白名單檢查失敗，就阻擋當次部署；避免 CI 通過但 Cloudflare 使用不相同的建置邏輯。

**目前交接狀態**：已準備好從 GitHub 自動建站，但 Cloudflare 帳號尚須由使用者完成授權並啟用 Pages 專案。只有成功部署並驗證 HTTPS 後才會有可確認的正式網站網址。

## 一次性部署設定

詳見 [Cloudflare Pages 部署指南](docs/cloudflare-pages.md)。

| Cloudflare 欄位 | 設定 |
|---|---|
| 產品 | Workers & Pages → Pages → Connect to Git |
| GitHub repository | `sheng-web-OS/Clinical_system`（private） |
| Production branch | `main` |
| Framework preset | None |
| Root directory | 專案根目錄（留空） |
| Build command | `bash tools/build_site.sh` |
| Build output directory | `dist` |
| Python version | `.python-version` 指定 3.12 |

不需要 GitHub Pro、Cloudflare API Token 或 GitHub Secrets。

## 可重現測試

```bash
bash tools/build_site.sh
python -m http.server --directory dist 8000
```

網站只會發布 `dist/` 白名單中的教材 HTML、審查頁、CSS、JavaScript 與搜尋索引；私人 `archive/`、Markdown 來源、編輯狀態 JSON 與 Git 歷史不會被上傳。

本教材供醫學教育；未經真人專科同儕審查。修改核心機轉時按需重建依賴、驗證影響，不強制永久維護全域 Claim Graph。
