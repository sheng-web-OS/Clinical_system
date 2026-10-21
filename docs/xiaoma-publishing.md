# 小麻內科國考｜延續編輯與發布

本輪需求：讓「小麻內科國考」計畫與後續教材累積到既有醫學教育網站。沿用私人 `sheng-web-OS/Clinical_system` 與既有 Cloudflare Pages，自 main 發布，不建立另一個網站。

## 正式位置

- 公開入口來源：`content/xiaoma-internal-medicine/index.md`。
- 每日原創教材：`content/xiaoma-internal-medicine/lessons/YYYY-MM-DD-topic.md`。
- 出版目錄：`site/pages.json`，每份新教材新增一項。編譯後入口教材卡片、導覽與全文搜尋自動引用相同清單，無需逐日修改編譯器或發行檔檢查器。
- 私人原始計畫：`archive/xiaoma-internal-medicine/plan-20261021.md`，與原交付檔案 bytes 相同；包含個人時程與執行紀錄，不可列入公開目錄。後續個人學習回覆同樣只保留在私人來源或對話。

## 加入下一篇

先讀本對話最新回覆、私人計畫與本儲存庫最新架構／教學品質契約，再產生一篇教材。依目前進度選主題，查完整對題來源與正式考題，標明年度、梯次、科目、題號、更正狀態、自編題及審查界限。不得以教科書原始 PDF 或個人輪訓資料當作公開資產。

在 `site/pages.json` 追加下列結構（名稱、日期與來源依本次實際內容填寫）：

```json
{
  "source": "content/xiaoma-internal-medicine/lessons/YYYY-MM-DD-topic.md",
  "output": "xiaoma-YYYYMMDD-topic.html",
  "title": "本次實際教材標題",
  "subtitle": "臨床問題與閱讀目的",
  "collection": "xiaoma-internal-medicine",
  "date": "YYYY-MM-DD",
  "navigation": false,
  "review": "author_source_check"
}
```

`review` 必須反映實際完成的審查，欄位本身不是審查。保存未查清的重大醫學衝突為私人草稿，不把它列入出版目錄。任何日期必須為實際日期，不可使用上例佔位符。

教材可連回 `../index.md`；編譯器會改寫為公開入口。答案使用原生 `<details>` 與 `<summary>` 放在原題後面，內容仍可由瀏覽器原生開啟，無需 JavaScript。

## 檢查、提交與驗證

1. 比較實際 diff；保全其他人的變動，不覆蓋舊教材、私人計畫或來源。
2. 執行 `bash tools/build_site.sh`；它保留原 Tamponade 內容檢查，並驗證目錄、本地連結、所有輸出頁的 DOM 錨點、公開檔案白名單及私人資訊邊界。
3. 需要驗證出版目錄邊界時執行 `python -m unittest discover -s tests`。
4. 在 GitHub 儲存庫建立基於最新 main 的提交，更新分支時使用 expected head 防止競爭覆蓋，不強制推送。缺少本地工程工具時不能以改掉檢查器代替通過；保留草稿並說明阻擋。
5. main 提交會觸發既有 Cloudflare Pages。讀回與該 commit 相同的 deployment 狀態，然後以 HTTPS 核對入口、該篇文章及搜尋索引。GitHub CI 成功不等於已上線。
6. 成功後回覆公開教材連結；若只保存 Git 或草稿，精確回報，不宣稱發布完成。排程提示詞只是工作指令；尚未觀察到的未來執行不能稱為已實測成功。

## 學習狀態

網站的「已發布」是內容狀態，不代表使用者已讀或掌握。未來題目與錯誤回覆不得直接寫進公開教材。若有可泛化的教學缺口，可去除個人資訊後修訂教材；私人完成、答題與延後回想狀態另行保存。
