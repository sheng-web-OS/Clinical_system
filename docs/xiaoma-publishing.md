# 小麻內科國考｜延續編輯與發布

本輪需求：讓「小麻內科國考」計畫與後續教材累積到既有醫學教育網站。沿用私人 `sheng-web-OS/Clinical_system` 與既有 Cloudflare Pages，自 main 發布，不建立另一個網站。

## 正式位置

- 公開入口來源：`content/xiaoma-internal-medicine/index.md`。
- 每日原創教材：`content/xiaoma-internal-medicine/lessons/YYYY-MM-DD-topic.md`。
- 出版目錄：`site/pages.json`，**僅對已獲出版放行的教材**新增一項；完成每日草稿、通過個別 AI 編輯審核均不等同公開。編譯後入口教材卡片、導覽與全文搜尋自動引用相同清單，無需逐日修改編譯器或發行檔檢查器。
- 私人原始計畫：`archive/xiaoma-internal-medicine/plan-20261021.md`，與原交付檔案 bytes 相同；包含個人時程與執行紀錄，不可列入公開目錄。後續個人學習回覆同樣只保留在私人來源或對話。

**涵蓋與來源擴展：** 舊文補充與新教材均遵循 [Pocket Medicine × IBCC 按需證據補強](xiaoma-evidence-expansion.md)。有重要急重症後果的主題，**必須獨立完成重症內容涵蓋檢查**，不論原稿是否已易於理解。IBCC 優先作為對題的 bedside physiology／重症管理來源，不替代現行指引與必要原始證據；教學可理解性另行驗收。歷史原稿另存，不默默改寫。

**正式寫作決策（2026-10-21）：** 具急重症後果的題目，重症臨床觀點須**嵌入主文的連續因果敘事**；不能以獨立 ICU 補充章或延伸閱讀連結取代。原稿維持原樣，整合後的新文章另開版本並查核。臨床上沒有實質重症關聯時，無須硬加重症段落。詳細契約見 [內容與 IBCC 整合規範](xiaoma-evidence-expansion.md)。

## 發布節奏：先累積，形成完整群組後再出版（2026-10-21 決定）

使用者正式選定**群組優先，獨立精品例外**。每日研讀／寫作可照計畫連續產出，先保存在 Git 來源與審稿分支，**不得把每日完成＝每日公開**。未通過出版時機判斷的稿件不進 `site/pages.json`；這不影響已公開既有頁面。

- **預設**：圍繞一個清楚的臨床問題，整合已回收原作、先備概念、連續因果、證據及處置決策，形成可獨立理解的教材群。跨篇必要前提、正反事例／反事實、關鍵安全與新證據完成檢查後，由 AI 編輯裁決 `group_ready`，再將該群內容及入口按同一出版批次加入 manifest；不以固定篇數為門檻，也不等完成整個專科。
- **例外**：若單篇已完成一個高價值、邊界明確的臨床命題，核心推導與安全前提均不依賴未公開其他篇章，且獨立通過 EPQC、醫學查核與來源核對，AI 可記錄 `standalone_release` 理由而先行出版；未完成其他稿不得因此自動跟著發布。
- **原創歷史典藏**：經查證的 Facebook 發布原稿可獨立進行保真、權利與醫學安全審查後，以「原創典藏」身份發布，與 AI 整合教材群組的出版時機分開；不得改寫成原稿或把未查明的舊版冒稱作者已發表版本。
- **發布標籤**：歷史原創／AI 整合教材是作品身分；`ai_review_passed`／`group_ready`／`standalone_release`／`published` 是工作階段。任何 AI 自評不等於臨床同儕審查或真人閱讀測試，不得互相冒稱。

執行的完整品質門檻與群組完成條件見 [內容先行與跨篇整合規格](content-first-knowledge-integration.md)。只有確認上述發布路徑之一成立後，才套用下述「加入下一篇」的技術發行程序。

## 加入下一篇

寫作後按 EPQC 的七軸逐段標出中介缺漏與主線偏移，通過醫學硬性門檻及上述群組／單篇發布時機判斷後才可出版；內容高密度或互動豐富不視為自然達標，人工閱讀結果也不得由 Agent 自評冒認。重大退稿問題先保留私稿，不在出版目錄中列出。

先讀本對話最新回覆、私人計畫、本儲存庫最新架構／教學品質契約、`docs/editorial-prose-quality-contract.md` 及 `docs/xiaoma-depth-standard.md`，再產生一篇教材。2026-10-21 使用者要求 ACS 及過往小麻閱讀文章等級的完整推導；原始計畫的第一天簡短範例已被本次正文取代，不能當成深度上限。依目前進度選主題，查完整對題來源與正式考題，標明年度、梯次、科目、題號、更正狀態、自編題及審查界限。不得以教科書原始 PDF 或個人輪訓資料當作公開資產。

在 `site/pages.json` 追加下列結構（名稱、日期與來源依本次實際內容填寫）：

```json
{
  "source": "content/xiaoma-internal-medicine/lessons/YYYY-MM-DD-topic.md",
  "output": "xiaoma-YYYYMMDD-topic.html",
  "title": "本次實際教材標題",
  "subtitle": "臨床問題與閱讀目的",
  "collection": "xiaoma-internal-medicine",
  "layout": "reader",
  "section": "本篇實際專科或問題群",
  "references": "本篇實際來源頁.html",
  "date": "YYYY-MM-DD",
  "navigation": false,
  "review": "author_source_check"
}
```

`review` 必須反映實際完成的審查，欄位本身不是審查。保存未查清的重大醫學衝突為私人草稿，不把它列入出版目錄。任何日期必須為實際日期，不可使用上例佔位符。

教材可連回 `../index.md`；編譯器會改寫為公開入口。答案使用原生 `<details>` 與 `<summary>` 放在原題後面；必要的機轉推導維持連續可讀。來源、版本、查核集中在獨立來源頁，一般課表在 `content/xiaoma-internal-medicine/plan.md`；不要混回閱讀主線。新來源頁同樣須加入 `site/pages.json`。卡片依 manifest 生成，公開後才出現在教材目錄。

## 檢查、提交與驗證

1. 比較實際 diff；保全其他人的變動，不覆蓋舊教材、私人計畫或來源。
2. 執行 `bash tools/build_site.sh`；它保留原 Tamponade 內容檢查，並驗證目錄、本地連結、所有輸出頁的 DOM 錨點、公開檔案白名單及私人資訊邊界。
3. 需要驗證出版目錄邊界時執行 `python -m unittest discover -s tests`。
4. 在 GitHub 儲存庫建立基於最新 main 的提交，更新分支時使用 expected head 防止競爭覆蓋，不強制推送。缺少本地工程工具時不能以改掉檢查器代替通過；保留草稿並說明阻擋。
5. main 提交會觸發既有 Cloudflare Pages。讀回與該 commit 相同的 deployment 狀態，然後以 HTTPS 核對入口、該篇文章及搜尋索引。GitHub CI 成功不等於已上線。
6. 成功後回覆公開教材連結；若只保存 Git 或草稿，精確回報，不宣稱發布完成。排程提示詞只是工作指令；尚未觀察到的未來執行不能稱為已實測成功。

## 學習狀態

網站的「已發布」是內容狀態，不代表使用者已讀或掌握。未來題目與錯誤回覆不得直接寫進公開教材。若有可泛化的教學缺口，可去除個人資訊後修訂教材；私人完成、答題與延後回想狀態另行保存。
