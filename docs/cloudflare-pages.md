# Cloudflare Pages 一次性設定｜私人 GitHub → 免費公開網站

依 Cloudflare [Git integration 官方說明](https://developers.cloudflare.com/pages/get-started/git-integration/)，Cloudflare Pages 可連接私人 GitHub 儲存庫。原始碼不需轉公開；**發布的 HTML 網站會公開**。

## 使用者需完成的唯一外部授權

1. 登入 [Cloudflare Dashboard](https://dash.cloudflare.com/)，使用 Free plan。
2. 選 **Workers & Pages → Create application → Pages → Connect to Git**（UI 文案可能隨版本調整）。
3. 選 GitHub、Install & Authorize。授權建議選 **Only select repositories**，只授權 `sheng-web-OS/Clinical_system`，不授權全部私人儲存庫。
4. 選擇 repository `sheng-web-OS/Clinical_system`，Production branch `main`。
5. Framework preset **None**；Root directory 留空；Build command **`bash tools/build_site.sh`**；Build output directory **`dist`**。
6. Python 預設由根目錄 `.python-version` 指定 3.12。如 Cloudflare 未偵測，可新增環境變數 `PYTHON_VERSION=3.12`。不需要 Cloudflare API Token。
7. 部署，取得平台實際回傳的 `*.pages.dev` 網址。再測首頁、ESC 審查、審查紀錄、章節導航、搜尋和手機排版。URL 未經確認前不要自行推定或宣稱已上線。

**建議安全設定**：在 Pages → Settings → Builds → Branch control，將 Preview branches 設成 None，避免未審核的分支內容被發布到公開預覽網址；正式分支只用 `main`。

## 驗證阻擋條件

Cloudflare build command 會按順序執行：

1. 安裝固定 Python 依賴；
2. 驗證病例／指南來源欄位與本地引用 `tools/validate.py`；
3. 編譯靜態網站 `site/build.py`；
4. 確認 dist 發行檔白名單、標題、錨點與資產連結 `tools/check_output.py`。

如果任一步驟失敗，腳本以非零狀態離開，Cloudflare 會標記此次建置失敗。GitHub Actions 也執行完全相同的腳本，但**GitHub 的 CI 結果不等同 Cloudflare 已發布成功**。

## 資訊邊界

可發布：`index.html`、`esc-audit.html`、`audit-log.html`、`styles.css`、`app.js`、`site-index.json`、`site-index.js` 及 `.nojekyll`。

不應發布：`archive/`、`content/` 原始 Markdown、`tools/`、`.github/`、編輯狀態 JSON、Git 歷史與任何憑證。**公開審查頁本身依然公開**，請在任何教材進版前確認無病人可辨識資訊、私人訊息或未取得散布權限之圖表。

發行狀態以四層分開記錄：Git commit、CI build、Cloudflare deploy、實際 HTTPS 驗證。第三與第四層需等外部授權和部署完成，現階段不得宣稱成功。

官方文件：[Private GitHub 連接](https://developers.cloudflare.com/pages/configuration/git-integration/) · [Python build image](https://developers.cloudflare.com/pages/configuration/build-image/) · [Cloudflare Free build limits](https://developers.cloudflare.com/pages/platform/limits/)。
