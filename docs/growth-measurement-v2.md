# Clinical OS｜高解析度成長測量 V2（僅供內部評估）

更新：2026-10-31（Asia/Taipei）｜狀態：**提案／待資料驗證**，不是已量測的能力增益。

## 0. 為何修訂

[Issue #137](https://github.com/sheng-web-OS/Clinical_system/issues/137) 的固定 1–5 成熟度錨點只適合低頻、長期、跨任務驗證；在一天多次工程與教學修改下，離散階段會產生「能力正在形成但評分不動」的解析度不足。相反，產生更多 PR、CI success、提示詞或報告也不能自動增加能力評分。

**核心改動：保留成熟度階段，新增可核實的逐事件成長訊號與跨時間窗的結果比較。** **最高優先結果是 Agent 自身從新證據形成可追溯的知識／決策修正，並在獨立、未見任務中證明真正改善及跨輪保留。** 讀者或 owner 的學習收益、實際交付與較少人工介入是彼此獨立的結果與護欄；不是事件數變多。所有分母、證據等級、未測量欄位必須可追溯。**沒有充分事件資料，禁止生成人工精細的 1.2/5、83.6 分或能力增益百分比。**

既有來源仍為 #137（成長基準）、#133（唯一失敗事件源）、#254（跨工作槽交付路線）、原始 PR/CI/QA/正式站驗收、`experiments/README.md`（證據等級）及私人 ALE/Anki 合規聚合；**不新增服務、資料庫、排程、公開網站儀表板或第二事件台帳**。

## 1. 三種尺度分工

| 尺度 | 更新方式 | 真正回答什麼 | 不可推論 |
|---|---|---|---|
| **事件／每輪** | 僅記錄現有任務的可觀察狀態變化，包含原始來源連結與 commit SHA | 這一次是否從發現 → 選擇 → 真正修復 → 驗證 → 被接受？由誰觸發？ | 事件多就更成熟 |
| **24h 與 rolling 7d** | 逐日增量；同口徑與同條件比較，附 n/N、欠測及觀察時間 | 微小能力是否正在增加？阻塞在哪關？返工有無下降？ | 單日 1/1 就是穩定 100% |
| **28d 與跨新領域** | 使用 #137 既有 1–5 錨點，僅新證據足以跨越門檻才更改 | 無提示能力是否穩定、可遷移、對讀者／owner 有效？ | 4 週未升級即零成長 |

每個數值同時顯示 `window, numerator, denominator, coverage, evidence_level, SHA/source, uncertainty`；缺分母時只報件數，不報百分比。

## 2. 九個能力群與高解析度指標

這些是**診斷維度，不是九個互相相加的 KPI**。只為實際決策記錄能由既有事件核查的項目。

| 群 | 須分別量測的微能力 | 最低可核驗來源 |
|---|---|---|
| **知識取得** | 未提示自行發現關鍵資料缺口；核原始 Figure/Table；辨別來源版本／相衝突證據；成功檢索必要資料 | PR source audit + 來源頁及 evidence trace |
| **知識整合** | Concept Family 的有效新連結；誤合併／漏合併；上位抽象在未見案例遷移；維持概念來源邊界 | ALE 私人評估的最小聚合、獨立評閱／未見題 |
| **推理與決策** | 正確界定問題；辨識競爭機轉與必要反事實；在既定風險與依賴中選可完成的高價值下一步 | 預定任務條件／對照、客觀決策行動 |
| **自主規劃** | 無提示選題；跨輪保有任務狀態；被阻塞後重排；區分可逆自主與必須授權的改動 | 排程觸發、原 task ID、PR checkpoint、使用者 prompting 紀錄 |
| **自主執行** | 真的改出產物；局部回歸通過；獨立接受；正式交付／production 讀回；跨不同任務重現 | 產物 SHA、CI、獨立 QA、原任務驗收 |
| **自我修正** | 自己先發現缺陷；根因確認；實施修補；新回歸確實攔截舊缺陷；同根因在後續新題不再發 | #133 failure_id + 具體修復與回歸證據 |
| **教材品質** | 首稿醫學／來源正確；因果鏈連續；圖表確有認知增益；手機可讀；獨立 EPQC 評審 | 版本凍結首稿、來源核對、獨立 QA |
| **學習成效** | 原先不會的概念答對；新的同概念變形題答對；延遲回憶；跨題族臨床判斷轉移；嚴重誤解是否消失 | 私人 ALE/Anki／獨立讀者的未見題與延遲測 |
| **系統效率** | owner 必需介入次數與實際分鐘；有效交付耗時；返工次數；可觀測工具費與 token；被不必要的 HOLD 阻塞之輪次 | 任務與使用者介入原始紀錄、可得成本憑據 |

**注意：**私人 Anki 卡面、作答紀錄、學習者識別及任何臨床私有資料不得寫入公開 GitHub；僅在適用授權下使用最小化且無法回推出個人的聚合。保留先前跳過的 Anki 卡片，不以刪卡製造學習改善。

## 3. 成長結果的優先序：Agent 學會 → 使用者受益 → 自主交付（效率為護欄）

依 [#254 owner strategic correction](https://github.com/sheng-web-OS/Clinical_system/issues/254#issuecomment-6541025279)，後列原 P1/P2/P3 指標保留、各自獨立，但**不可把「使用者學會」直接當作「Agent 學會」**。評估上位結構為三條曲線 A. agent evidence-backed learning（首要）／B. 使用者或產品被獨立驗證的實際增益／C. 自主交付與可靠性；人工時間、成本為 C 的條件式護欄。

### A｜可反證的 Agent 自身學習（首要，不能由提交或 CI 代替）

最小可檢驗事件：`source identity → frozen before-claim/prediction → new independent observation → competing explanations & counterexample → versioned concept/policy/skill revision → independent agent-unseen fresh challenge → baseline/after comparison → negative control & regression → next-run retained/recovered state`。必須區分：
- 新增有效知識（new justified knowledge）：以前沒有支持、現在經新證據與反例檢驗而成立。
- 糾正錯誤（error correction）：先前結論有可重現的錯誤，修改後未見反例改善。
- 重新檢索或分類（retrieval/relabeling only）：資訊量增加但尚未證明決策品質改善，**不得領取已驗證學習增益**。
- 若 skill、memory 或 Concept Family 只是外部可逆狀態而非模型權重改變，須如實寫 versioned external state learning；不可宣稱模型權重已自我訓練。
- **保留與遷移**：不同排程輪次可復原修正，並在未曝光的另一題族使用；來源/題目/答案不得提前洩漏。題族重合、同模型自評或樣本不足 → `INCONCLUSIVE`。

有可信分母時分別報 `independently_validated_learning_events / eligible_learning_hypotheses`、`corrected_misgeneralizations / independently_challenged_cases`、`retained_after_restart / eligible_retention_probes`，附原始樣本、對照組及成本；**樣本不存在就 NOT_MEASURED，不湊比例**。

### B｜下游實際效益（包含原本的 P1 讀者／owner 學習）

### P1｜未見題／延遲題的實際學習增益（Outcome）

分別報：
- `unseen_transfer_correct / unseen_transfer_attempted`：未見題族的正確率與 n/N；需要獨立出題、固定難度／評分標準；不得把複習過的同題改名當新題。
- `misconception_repaired_and_retested / baseline_misconceptions`：原先客觀錯誤 → 教學介入 → 不洩題的新變形題再次測試成功的概念數；未復測不算修復。
- `retained_correct_7d / eligible_delayed_retests`：7 日延遲測仍保留的比例；無足夠間隔則 NA。
- `clinical_transfer_critical_errors`：未見情境重大錯誤絕對件數；高安全性問題優先。

**必須切開**：owner 的私人學習成效 vs 網站讀者的受控教學試驗 vs Agent 自身的能力評估。三者不得混為同一學習曲線。初期沒有真人實驗、未見題或後測時標記 `NOT_MEASURED`。

### C｜原 P2：真正被接受的自主交付（Enabler / outcome）

`unprompted_independently_accepted_tasks / preregistered_eligible_tasks`：分子須有當輪之前已定義的完成條件、無額外 owner 催促、真實交付，以及不同執行角色或客觀 gate 接受；分母**同時包含尚未完成、明確失敗以及合法 BLOCKED 的已承諾 eligible 任務**，需另列阻塞率，避免只挑容易成功者。明確不合法、不在授權範圍的任務不列 eligible，需記排除理由。

對每個任務另列階段：`identified → selected → action_executed → engineering_verified → independently_accepted → downstream_value_verified`。任務可以合法終於 code merge、醫學文章發布或教學測試，依事前 acceptance 定義，不強求所有任務都 deploy。**CI 過了只是其中一關**，Draft、comment、實驗設計不算最終交付。

分欄記 `owner-initiated`（使用者要求開始）、`owner-nudged`（中途催促／修正）、`scheduled-unprompted`、`agent-proposed` 與 `mandatory-approval`；合法醫學審批不視為 Agent 缺陷，卻仍如實記 owner 負擔。

### C 的護欄｜原 P3：品質約束下的 owner 注意力成本

`owner_measured_minutes / independently_accepted_task_count`；另列 `owner_interruptions` 件數與分布，以及 `verified_net_teaching_units`（沿用 #137 嚴格品質定義）。

實際分鐘未測到時不得報 0；作者未催促不等於完全沒有介入。若沒有可接受產出，分母為 0 應回報 `NOT_COMPUTABLE`，不能當無限好或無限差。

## 4. 只診斷、不拿來灌分的早期訊號

| 指標 | 定義 | 典型誤用 |
|---|---|---|
| **Stage conversion** | 同 cohort `到達下一個有證據 gate 的任務數 / 到達上一 gate 的任務數`，顯示每關 n/N | 把不同階段、不同任務混同分母 |
| **No-nudge continuation** | 非人工提醒下，跨至少兩次合法排程接續至實質改動且驗證的任務 / 有此機會的任務 | 只寫留言、醒來即計成功 |
| **Autonomous repair yield** | 首次由 Agent 偵測且修復並獨立驗證的**唯一事件** / 有證據具備修復授權且可處理的已確認事件 | 只查到錯或開 PR 即算修復 |
| **Escaped/recurrent defects** | 按 #133 唯一 failure_id 量測重大逃逸與同根因在新任務再發；有覆蓋分母才報率 | 重複 issue 當多起、沒有分母報 0% |
| **First-pass quality** | 凍結的首次完整產物通過來源／醫學／教學／視覺等獨立關卡的數量 / 有可比首稿的任務 | 以 V2 修訂後 PASS 倒填首稿 |
| **Novel semantic transfer** | 未見題族中經獨立確認有用的概念抽象／選擇與反例表現；誤合併和漏合併一併報 | graph 邊數增加即宣稱理解變好 |
| **Time to accepted outcome** | 任務承諾至可接受完成的耗時分布（median / p75，如 n 足夠），分開待外部核准時間 | 將所有 HOLD 當 Agent 無能 |
| **Waste / rework** | 被取代的重工、失敗重試／工具成本；分母為合格交付或任務數 | Actions cancelled 一律當失敗 |

## 5. 事件證據最小契約（不是新增資料庫）

沿用既有 PR/Issue/CI/QA/排程紀錄；報告層從其抽取必要欄位：

```text
task_id, cohort_id, domain, acceptance_ref
observation_at_utc, window_start_utc, window_end_utc
trigger_type, owner_nudge_count, owner_minutes_status
phase_before, phase_after, evidence_level
source_issue_or_pr, observed_sha, verification_link
independent_reviewer_status, eligibility, exclusion_reason
clinical_safety_status, publication_status, learning_test_id_private
metric_numerator, metric_denominator, sample_coverage, missingness
```

- 既有來源**只記一次**，報告衍生多個指標，不新建可競爭的寫入位置。
- `evidence_level` 遵循 experiments/README.md：Design / Artifact / Pilot / Validated / HOLD，不能跨越證據門檻。
- 無法核對來源：`NOT_VERIFIED`；尚無實際測量：`NOT_MEASURED`；無有效分母：`NOT_COMPUTABLE`；無 task 機會：`NO_ELIGIBLE_EVENTS`；全部與數值 0 區分。
- `created_at`、事件第一次被見到的時間、研究時窗截止與觀察回報時間是不同欄位；禁止事後補入資料卻宣稱當時即知道。
- 小樣本顯示 raw n/N，不用變動劇烈的百分比掩蓋缺口。適當時加置信區間、題目難度與配對比較，但不能憑精細儀表創造精確度。

## 6. 建議顯示層（私人報告，不修改公開 reader 頁）

**日報只列四行**：今日可獨立接受的結果、上一次到這一次跨過哪些 gate、首次發現／修復哪些真問題、哪個學習缺口被未見題證實改善；再列真正 blocker / nudge。

**7 日對比**：小型 funnel + P1/P2/P3 當期與前期 n/N，依九大能力群顯示「新增證據／仍無證據／重複失敗」，不畫沒有數字來源的折線。

**28 日**：回到 #137 的 1–5 六維成熟度評審，附「距下一級尚缺哪個可驗證條件」，不得因 micro-metric 上升自動升級。

例（**純示意，非觀測結果**）：
`1/5 unchanged | identified 6 → executed 4 → independent accepted 1 | no-nudge accepted 1/5 | owner minutes NOT_MEASURED | unseen transfer NOT_MEASURED`
表示有新的短期證據，但尚未證明跨題穩定自主，更沒有證明教學成效。

## 6.1 自動研發決策回路（現有工程工作槽，不新建平台）

- 既有排程「Clinical OS｜GitHub 工程工作槽」是主動實作端；#244 GDC/ADPC 是研究選題與停損唯一源，#254 為後 72h 跨槽索引，本 PR 只提供診斷工具與證據契約。不能修改原 #137 72h 成績。
- 每個**自然排程機會**先從已授權且未完成的 P0/P1、PiCCO #243 窄授權門檻、#241/交付依賴與作者衝突中辨識可完成的下一步；每輪最多一個主要實質交付。只有當新的不確定性會改變下一步時，採「近期領域研究 → 原研究方法/反例 → 可遷移性 → 低成本可否證試驗」；不存在文獻不是無人研究的證明。
- 候選處置為 `CONTINUE/PIVOT/CHEAP_PROBE/PARK/STOP_L0/REQUEST_AUTHORIZATION`。停選只對原工程槽自己、可逆且無 owner 承諾的 L0 工作有效，沿用 #244 已授權的精確 receipt、rollback、7 日內重審；絕不停止正式 QA、醫學發布 gate、原 Writer 或原 72h 守護。
- 每次有新 outcome 才更新既有 Issue/PR，附 source/SHA、frozen before 版本、追加觀察、獨立驗證、否定案例、下一 gate；沒有新證據 `NO_CHANGE`。**不需要定期生成長篇研究報告或持續搜尋**。
- 在 2026-11-01 14:20:15 Asia/Taipei 原試驗時窗結束前，只允許原授權的隔離、非敏感 Shadow 與本 PR 工程，不碰原 cohort/保護路徑；之後也需先核對 #137 真實結案與原 tasks 的條件。
- 本決策更新由 owner-directed 啟用，不能計入以前或未來對照中未提示自主修正的成功分子；要在**後續真正未提示、事前凍結的新任務**中驗證增益。

## 7. 導入與接受條件

1. **凍結邊界**：#137 原始 72h 試驗的 cohort、排程、成功定義、統計方法、原始 evidence 與封存時間（2026-11-01T06:20:15Z）全部不變；本文件不追溯改判，不修改 #137/#159/#224/#225/#234/#235 的任何原始評測。
2. **先用既有資料做 read-only shadow baseline**：從已存在的兩條不同工作線抽取真實 task/gate 事件，註記缺分母、漏記 nudge、未知 owner minutes；驗證可重複抽取、不複算 PR。不得直接宣稱所有歷史資料都是完整 cohort。
3. **最小前瞻驗證**：下次既有週報使用同一口徑展示 24h/7d 比較，至少能指出「哪一個 gate 改善、哪個問題仍未改善」，且所有數字可點回原始證據；資料不完整則顯示 NA。**不新增自動化排程**。
4. **學習先行**：私人 ALE 僅在合法資料存取下以未見題、概念修補後重測與延遲測建立學習成效；公開 GitHub 不接觸原始卡面／學習日誌，也不因修補工程能力就宣稱國考成績進步。
5. **持續淘汰無效訊號**：若指標無法導致不同決策，或增益不能重現，停止追蹤；只保留能改善下一輪選題、交付、品質或學習的資料。

**Definition of done：** 不只是產生一份 V2 規格，而是至少一份有來源、時間窗、分母與不確定度的實際對照讀數，並能回答「這一次新增了什麼有用能力？下一次應該選哪個任務？對使用者學習是否真的有益？」。目前此驗收 **尚未完成**。
