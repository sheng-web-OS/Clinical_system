# Clinical System — Agentic Medical Knowledge & Editorial System

**GitHub 儲存庫目前為 PUBLIC（2026-10-30 實查）；醫學教材網站另由 Cloudflare Pages 公開。**

**安全邊界：**`site/pages.json` 只限制網站建置輸出，**不限制公開 GitHub 的 `archive/`、草稿分支、PR、Issues、Actions artifacts 與 Git 歷史**。不得在此存放病人資訊、私人閱讀／考試紀錄、未取得公開重製依據的原始圖表、秘密或受限 Drive 來源；這些必須留在真正受存取控制的位置。現有歷史內容的權利／隱私審查仍待獨立處理，不能因本文勘誤視為已完成。

此儲存庫是 Master Prompt v5.1 的版本化知識來源；Cardiac Tamponade 是第一個端到端教材驗證案例，不是系統的終點。

系統設計遵循 [Master Prompt v5.1 — Capability-Native Architecture Principle](docs/master-prompt-v5.1-architecture.md)；實際運作與實驗收斂請讀 [統一運作契約](docs/clinical-os-integration-20261021.md)、[實驗登記與驗收](experiments/README.md)。供 Codex／工具 Agent 使用的最小執行入口是 [AGENTS.md](AGENTS.md)，它不是另一套完整 Master Prompt。

## 來源與審查

- [Clinical OS 跨篇知識脈絡](content/clinical-os/index.md)：將實際已典藏原文、已出版教材與待驗證的跨篇因果路線分開呈現，串起 HCM、LVEDP、HF、利尿劑與重症等問題。
- [Tamponade 完整教材](content/tamponade.md)：既有八個教學單元、2025 ESC 原始圖表對讀、反事實推理。
- [正文品質契約（EPQC）](docs/editorial-prose-quality-contract.md)：以原創 HCM／ACS 的認知推進作標竿，規範概念解混、機轉推導、審稿退稿與實際對標驗證。
- [小麻閱讀原稿](content/xiaoma-reading/index.md)：保存實際已入庫、附原文身分的文章；以該頁及其逐篇來源紀錄為最新清單，勿從舊 checkpoint 的篇數推測現在進度。
- [小麻內科國考](content/xiaoma-internal-medicine/index.md)：82 日核心路線、Pocket 122 個章節項目與持續累積的每日教材。
- [2025 ESC 圖表核對](audit/esc2025-figure-check.md)：Figure 12、Table 17、Recommendation Tables 12／21。
- [可追溯審查](audit/audit-log.md)：版本、證據、已知歧義與驗收限制。
- [歷史原稿](archive/tamponade_r2_baseline.md)：原材料封存，不再當作正式編輯來源。

2026-10-21 主分支已收錄 HCM，以及由當日 21 篇對話接收中轉存的 HF、LVEDP、利尿劑、DCM、胰臟炎、癲癇重積六篇，另十五篇仍待逐篇轉存。此數量是**原文 Git 存檔狀態**，並非作者最終發表版本、全篇 Figure／Table 或臨床醫學審查已核實。後續請以[實際原稿目錄](content/xiaoma-reading/index.md)和[接收紀錄](archive/xiaoma-reading/intake/2026-10-21-chat-manuscripts.md)判斷，不從過時的工作清單自動生成進度。跨篇知識脈絡頁僅是編輯導航，不冒充因果依賴已驗證。

小麻內科國考的歷史時程檔曾留存在 `archive/xiaoma-internal-medicine/`；**該路徑在 PUBLIC repository 不是私人儲存空間**，既有內容須另行審查，未來個人時程不可繼續放入公開 Git。網站入口僅應發布教材與去除個人行程的學習路線。後續新增方式見 [小麻教材發布](docs/xiaoma-publishing.md)；出版目錄為 `site/pages.json`。

## 目標工作循環

```text
ChatGPT 對話 / Work / Codex：研究、修訂教材、審查
                 ↓
GitHub PUBLIC / main：僅放可公開的 Markdown 與版本歷史
                 ↓
Cloudflare Pages：驗證 → 編譯 → 免費公開網站
                 ↕
GitHub Actions：相同驗證器，獨立 CI 與預覽成品
```

Cloudflare 先執行 `bash tools/build_site.sh`。若來源檔案檢查、網站編譯或發行白名單檢查失敗，就阻擋當次部署；避免 CI 通過但 Cloudflare 使用不相同的建置邏輯。

**2026-10-21 歷史交接狀態（不可當作當前安全設定）**：Cloudflare Pages 正式部署已成功，公開 HTTPS、首頁、ESC 審查頁、審查紀錄、章節導航與全文搜尋已實際驗證。正式網站：[sheng-clinical-system.pages.dev](https://sheng-clinical-system.pages.dev/)。當時紀錄 GitHub repository 為 private，**但 2026-10-30 實查已為 PUBLIC**；main 自動部署與預覽分支設定需以平台即時狀態核對，不由此歷史紀錄推定。完整證據與限制見 [發行審查紀錄](audit/audit-log.md)。

## 一次性部署設定

詳見 [Cloudflare Pages 部署指南](docs/cloudflare-pages.md)。

| Cloudflare 欄位 | 設定 |
|---|---|
| 產品 | Cloudflare Pages（靜態網站） |
| Project name | `sheng-clinical-system` |
| GitHub repository | `sheng-web-OS/Clinical_system`（目前 PUBLIC） |
| Production branch | `main` |
| Framework preset | None |
| Root directory | 專案根目錄（留空） |
| Build command | `bash tools/build_site.sh` |
| Build output directory | `dist` |
| Python version | `.python-version` 與 `PYTHON_VERSION` 指定 3.12 |
| Preview branches | None |

不需要 GitHub Pro、Cloudflare API Token 或 GitHub Secrets。

## 可重現測試

```bash
bash tools/build_site.sh
python -m http.server --directory dist 8000
```

網站建置只選取 `dist/` 白名單中的教材 HTML、審查頁、CSS、JavaScript 與搜尋索引；`archive/`、Markdown 來源、編輯狀態 JSON 與 Git 歷史不會因此上傳至 Cloudflare Pages，**但在目前 PUBLIC GitHub repository 仍可被公開取得**。

本教材供醫學教育；未經真人專科同儕審查。修改核心機轉時按需重建依賴、驗證影響，不強制永久維護全域 Claim Graph。

