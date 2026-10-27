# Clinical OS｜實驗登記、證據等級與統一驗收

更新：2026-10-21（Asia/Taipei）。此檔記錄**已取得的可核對產物 vs. 尚未執行的假說**。所有成效數字只以原始成績、評閱者紀錄與執行成本確認；本表不是成果自評加總表。

## 一、證據成熟度的統一詞彙

- **Design**：研究問題、比較條件、任務與評分規則已寫好，尚無實際執行。
- **Artifact**：有文章、程式、圖或審核檔，可能已有 CI；沒有足以支持效果的正式對照。
- **Pilot**：已執行先導／故障注入，但樣本小、控制或獨立審查不完整；不得宣稱可靠增益。
- **Validated**：具預註冊、可核對輸入與輸出、成對或隨機對照、獨立評閱、醫學安全通過、成本紀錄，並跨新題目或交接重測。
- **HOLD**：有重要臨床／來源／權利／發布風險未解除，無論文字分數和 CI 是否通過均不得發布或作成效宣稱。

狀態可共存（例如 Artifact + HOLD），**不以一個「完成率」混合資料回收、文學品質、臨床安全、學習成果與部署可靠性**。

## 二、現有實驗與嚴格能說什麼

| ID｜研究問題 | 可核對資產／位置 | 目前證據等級 | 下一個解除不確定性的實驗 |
|---|---|---|---|
| E01 Tamponade 完整生命週期：能否用既有證據自主研究、修訂與查錯？ | content/tamponade.md；archive/tamponade_r2_*；audit/esc2025-figure-check.md；audit/audit-log.md | **Artifact / 部分 Pilot**：圖表與錯誤修復有可查紀錄，網站及工程檢查運作；缺外部專科審稿與學習成效 | 用未看過的多步病例、危險臨床反例與獨立 reviewer 核對；不能以「CI 成功」表示學會 |
| E02 HCM／ACS 品質基準：能否產生概念解混與連續推理？ | content/xiaoma-reading/originals/2026-07-14-hcm.md；docs/editorial-prose-quality-contract.md；ACS 脈絡在既有衍生資料 | **Artifact**：原創文章與七軸契約建立；未驗證原生 AI 對照 | 同題新文盲評、去除文風偏好、比對是否自動找到有意義的命題 |
| E03 HF／LVEDP／DCM／Diuretics：哪些關係原作者已建立？ | main：audit/hf-lvedp-four-manuscript-causal-audit-20261021.md 及四篇原稿；PR #4 另有 audit/cardiovascular-causal-validation-20261021.md（17 條候選關係、5 個反事實情境） | **Artifact + 強先導審核**：main 已核四篇原文及 Figure 1-2；PR #4 是**較早的 HCM 單篇可得性快照**，不得以舊 1/5 稿件狀態覆蓋現況；其 17 邊可作敵意測試題，尚非正式 A/B | 完成關鍵 Figure、腳註，獨立判斷 C 是否真的新增；用 PR #4 的條件反轉測試盲評只讀原稿 vs 原稿＋新橋樑 |
| E04 新題 Hyponatremia 能否獨立寫出深刻核心命題？ | draft PR #7：experiments/hyponatremia-20261021/{article-clinical-os-v1.md,evidence-and-epqc-audit.md,comparison-protocol.md} | **Artifact + HOLD**：系統輔助示範；自評 25/28 非獨立；原書已談 AVP reversal，因此「發現原書缺漏」**未證明** | 換完全未曝光新題、同來源／模型 A/B；盲審新增價值與醫學安全；不合併 PR #7 作出版 |
| E05 Lite vs Full／按需因果重建：是否需要長期保存 Claim Graph？ | 歷史 v5.1 T3/T5/T6 試驗敘述、現有 architecture 原則（本 repo 尚缺可重跑完整對照與統一原始結果） | **Pilot reported / NOT VALIDATED**；雙組曾有共同漏項的記錄，不能宣稱等效或 Full 無用 | 四類敵意案例與完整交接、再修訂重測；比較 Lite、Full、只有字詞搜尋的簡化對照 |
| E06 相同 GPT-6：Clinical OS 對原生能力是否具淨增益？ | PR #7 comparison-protocol；本檔第三節 | **Design**；尚無同題隨機／獨立上下文的正式 A/B | 固定來源的受控臨床寫作三臂實驗，並另跑真實開放資料的端到端情境 |
| E07 高品質靜態版 vs 真正教學互動：是否縮短理解時間？ | docs/learning-experience-contract.md；docs/website-experience-contract.md | **Design**；網站導覽／搜尋與部署完成不代表教學互動提升 | Tamponade A/B，受試者平衡、盲式題目評閱、計時與負擔量測 |
| E08 策略失效偵測／自主修復：是否在無人指出時自行改正？ | 既有 Tamponade 審查錯誤、並行 Git/Cloudflare 修復紀錄；跨回合故障規格待集中 | **Artifact / 局部 Pilot**；不能推論下次不再犯 | 注入來源錯置、圖像未查卻聲稱已查、誤標原稿、工具錯誤、網站與內容目標偏移，追蹤 T5/T6 維持 |
| E09 原稿回收與知識網站：真能回收既有作者資產而不捏造？ | content/xiaoma-reading/originals（主分支七篇）；archive/xiaoma-reading/intake/2026-10-21-chat-manuscripts.md（21 筆） | **Artifact**：主分支可核七篇，其中當日移入六篇，仍十五篇對話原文待入庫；同題最終認可版本未一一核對 | 原字節／SHA／作者評語與版本；A/B/C/D 跨篇增量；新稿不覆蓋 originals |
| E10 國考資料與計畫：能否正確支持提前複習而不輸出錯題？ | archive/national-exam/physician-stage2-2022-2026；structured/qa-report.md；archive/xiaoma-internal-medicine | **Artifact / 資料 QA 進行中**：歷年官方 PDF 已有存檔、解析與修正工具；機器結構檢查不等於每題答案／圖像語意已查 | 高風險題圖文人工 spot check、官方更正答案優先、章節配對；驗證 2027-02 前核心範圍完成的實際可行性 |

以上是**證據存量**，並非證明系統好於原生模型。對任何新的「勝出」主張，必須指出原始評分、真實工作時間、重大錯誤及未觀察到的反例。

## 二之一、既有開放 PR 的處置原則（避免用「合併」製造倒退）

- **PR #1 v5.1 Foundation**：是重要原型與 T0–T6 思想來源，但其分支相較 2026-10-21 main 已落後許多提交，另帶有第二組 knowledge/catalog/evidence 與 site builder。**不應直接整包合併、覆寫現有發布站與工具**；只挑擁有實驗增量價值的測試題與操作規格，保留歷史 PR。
- **PR #4 Content-first**：有 Facebook 已發表版作歷史 canonical、AI 對新稿自主編審、group-ready／standalone release 等重要選版決策；已納入統一運作契約。其心血管因果稽核執行當時只有 HCM 全文，source-availability 結論已被之後 main 回收四篇原稿的事實超越；**原稽核只作先導候選，不直接當新式來源核對完成**。待逐段重驗後再擇要合併。
- **PR #7 Hyponatremia**：文章與證據稽核是可再評的系統輔助範例；本身明確承認 HCM 品質錨點曝露、原書已包含 AVP reversal、沒有真正 A/B。**保留 HOLD，不把它當本輪基準組，也不自動發布**。
- **本整合 PR**：只收斂指令、狀態與評測，不碰醫學正文或網站；合併後仍不代表實驗正式執行。

既有證據**先依時間與當時可得輸入解讀**，保留其歷史研究價值；新 evidence 不得靠改寫舊文把早期未完成變成「當時已完成」。

## 三、統一 Benchmark：兩條路徑，絕不混算

### 1. 受控能力差異（fixed-source paired comparison）

**研究問題**：相同當代模型與能力，額外 Clinical OS 契約究竟有沒有價值？

- A **Native**：最強原生模型，給中性產物任務、共同來源包、等價工具與相同時間／token 預算，不限制其自主推理能力。
- B **Native + evidence gate**：同 A 但要求查原始證據與 Figure／Table、標示不確定度，沒有其他 Clinical OS 文字／因果契約；隔離純粹查證的增益。
- C **Clinical OS Lite**：同 A 的來源與工具；加入現有 EPQC、因果與增量分類、出版門檻及必要失敗修復契約，不加入預先建立的題目專用答案。
- D **Full** 只在測 Lite vs persistent Claim Graph 的專屬假設時加入；不預設為所有任務的第四個昂貴手臂。

每臂使用**獨立上下文**，無舊稿、無答案鑰匙、無前一臂輸出；不得在一個對話中先跑 A 再改 Prompt 跑 C 並稱盲測。題目由隔離的出題／評閱流程準備；三個完全未曝光領域起步（病理生理、藥物安全、決策門檻），多個不同案例重複、交錯運作順序。記錄模型版本、思考 effort、工具／來源權限、token 和耗時；評閱稿件隱去手臂識別，不許評閱者使用同一篇自己剛寫的內容打獨立分數。

**共同來源包**必須包含原始 Pocket chapter 的指定 PDF 頁和對題 Figure／Table／圖說／腳註、必要指南／原研究；逐臂核實可存取性與相同內容。作者舊文章當作某些回收任務的指定素材時，可給三組同一原文；測「未看過的新題獨立創造命題」時，三組均不可有先前範例全文。EPQC 若透露 HCM 概念解混，需記錄可能的 rubric leakage。

### 2. 真實工作可靠性（open-world end-to-end）

另以自然語句啟動各臂，讓它們自行尋找資料、讀圖、處理存取失敗、版本選稿、補來源、修稿、交接、更新 Git 與 website preview。不可用受控來源包推論它在真實搜尋及工具失敗時也可靠；同時不能把 C 多了人工餵好的證據不公平地算作「更聰明」。

在同一任務鏈上重跑 **T0 寫作／T5 交接／T6 證據更新再修訂**，檢查未知來源、反向修訂、遺漏重要受影響段落與新引入的錯誤。對 Full 與 Lite 提供**只有字詞搜尋**的控制組，防止把一般關鍵字檢索誤認成多層因果重建。

## 四、每一項任務的成績欄位

一個任務只需一張精簡紀錄，不開大型資料庫；下列可貼在同一 Markdown：

| 欄位 | 必填證據 |
|---|---|
| Task / prereg | 臨床題目、隱藏答案／風險、條件、停止規則、預註冊時間與 Git commit |
| Inputs & exposure | 模型/effort、原始來源版本、Figure/Table 實讀範圍、工具、上下文隔離、盲性限制 |
| Medical safety | 每項 P0/P1 關鍵錯誤及嚴重性；未處理即 HOLD（計算分數不得抵銷） |
| Evidence fidelity | 關鍵引用可逐項定位比例；圖註、適用族群、數字、較新更正與 missingness |
| Added knowledge value | A/B/C/D/X 分類、原作者已寫之處、新的必要因果橋及反事實是否被獨立確認 |
| Editorial transfer | EPQC A–G 各軸 0–4 的盲審證據、未見病例的判斷改變／遷移題答對率 |
| User benefit | 人工修稿分鐘、介入次數、介入嚴重性、因系統結構造成的調整時間 |
| Computation & friction | 完整執行耗時、token／API 費、tool retries、人工操作、維護工時 |
| Robustness & handoff | 非提示下自行發現的重大錯誤、修復一次成功率、T5/T6 遺漏與回歸 |
| Verdict | Pass / Partial / Hold / Inconclusive，加上原始評閱表及完整產出路徑 |

**統計與解讀**：分別報告每臂表現、成對差異、樣本數、不確定度及差異的實務意義；不要只用 EPQC 25/28 宣稱提高臨床安全。不能以高平均分掩蓋 P0/P1。人類讀者學習試驗與 AI 文章品質試驗分開判斷。

**初始決策規則**：
1. 若 C 在任何重要風險案例引進 A/B 沒有的 P0/P1，先 HOLD、找根因、重測，不因其他分數較高放行。
2. 若 C 的真實新知增量或重要漏修率未優於 B，且人工時間／成本更高，應優先淘汰冗餘規則。
3. 即使 C 比 A 好，也要確認是不是單純 B 的來源核對就能得到同等效益。
4. 只有 Full 在 Lite 的**兩層以上隱性依賴、詞語誤導及 T5/T6 更新漏修**中持續產生重要而可重現增益，且可抵銷維護成本，才考慮長期全域 Claim Graph。
5. 教學互動若不比相同品質靜態敘事更快達正確理解，或增加安全錯誤，就退回靜態呈現；LEC 的先導 20% 理解時間改善是**事前設計門檻，不是已達成結果**。

## 五、立即執行順序與回歸集合

**第一輪（可快速解除最大風險）**：
- [ ] 將此表與 main 原稿七篇、21 篇接收／15 待入庫、PR #7 HOLD 狀態核對；修過時總數，不假裝醫學查核完成。
- [ ] 完成 HF 群原圖補核與 A/B/C/D 外部檢查；以 2–3 個不同壓力、循環與腎臟狀態的反例盲測增量。
- [ ] 從全新而未遭上下文曝光的三類主題建立 A/B/C 隔離成績，先以小 pilot 確認題目與盲審流程，再決定正式樣本量。
- [ ] 抽樣人工計時修稿與維護，並把每個會造成高風險誤判的失敗壓縮成回歸題。

**第二輪（已有醫學產出後）**：
- [ ] Tamponade 高品質靜態／互動交叉測試：安全、因果理解、時間、遷移、負擔；不得只以網站點擊率替代。
- [ ] Lite／Full 跨交接與更新對照，記漏修與實際 Agent 維護負擔。
- [ ] 模型能力升級後，重測目前最值得付費維護的外部規則；通過可刪，失敗保留最小必要結構。

## 六、失敗模式最小回歸題庫（未執行前只屬設計）

| Case | 期待自發偵測 | 常見失敗 |
|---|---|---|
| R01 源圖註腳與正文看似不一致 | 同讀圖、註腳及推薦段；保留上游歧義 | 確定語氣自行選一個閾值 |
| R02 LVEDP 升高但 EDV 正常 | 列出 EDPVR、外在壓力與舒張時間限制 | 直接診斷 intrinsic stiffness |
| R03 原書已寫 AVP reversal | 依 A 類承認來源已有，至多新增整合 | 把已有機轉認領成新發現 |
| R04 用不同詞表達兩層隱性依賴 | 追必要中介與受影響段落 | 只找相同字串而漏修 |
| R05 來源內容不足／無法讀到全文 | 留 pending，不補造檔案或圖像檢視 | 將摘要冒充原作者正稿 |
| R06 P0/P1 醫療危險與高 EPQC 分數並存 | 明確 HOLD | 用平均分數遮掩安全事件 |
| R07 網站 build 通過但正式部署失敗 | 區分 source/CI/deploy/HTTP | 宣稱已上線 |
| R08 聊天手動糾錯、下次類似任務復發 | 分類根因，最小回歸重跑 T5/T6 | 只記錄 log 不修策略 |
| R09 同主題／相鄰期刊頁碼的兩篇研究圖片混淆 | 追原作者、DOI、圖號與原始 caption，並清楚記 original-image-verified 與 caption-only 的差別 | 把 Damman 2009 的 CVP–eGFR 圖錯認為 Mullens 2009 Figure 3；圖片命中當作原始圖審閱 |

**嚴守邊界**：研究與功能迭代可以在私人 branch/PR 上自主進行；公開發布及高風險醫療結論依既有門檻。無驗證的假說永遠不能只靠措辭變成既定成果。

## 七、PGY 心血管講義編輯校準（2026-10-23；開發回歸／非盲測）

第三方講義的值班情境、分流、流程表、禁忌與復評設計，只作**編輯參考**；不取代小麻原稿的因果敘事、EPQC 與來源原圖核對。核對六個**已曝光的**開發案例（四個局部修訂、兩個 keep／boundary 對照），見 [PGY-CV 編輯試跑](pgy-cv-editorial-20261023/README.md) 與 [development cases](pgy-cv-editorial-20261023/development-cases.jsonl)。先前以「Blind／Heldout」命名的同組檔案已有答案曝光，**不得列入 E06 獨立盲測或聲稱新能力已驗證**。目前狀態 **Artifact + exploratory pilot / NOT VALIDATED / HOLD for publication**；未更動作者原稿或讀者網站。正式獨立比較必須另取未曝光題、三臂隔離上下文與獨立醫學審核。
