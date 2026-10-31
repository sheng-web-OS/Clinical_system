# 2026-10-31｜Evidence-to-decision：高密度研發的文獻檢索、繼續／轉向／停止契約

**定位：** 接續 [Growth V2](../docs/growth-measurement-v2.md)、[#137](https://github.com/sheng-web-OS/Clinical_system/issues/137)、[#254](https://github.com/sheng-web-OS/Clinical_system/issues/254) 與已存在的 [#244 GDC](https://github.com/sheng-web-OS/Clinical_system/issues/244)。這是 **research + read-only shadow proof**，不是建立第二套 dispatcher、發佈授權、自動排程、或聲稱已量得新能力。公開 GitHub 僅放非敏感評估資料，私人 ALE/Anki 內容不進此庫。

## 1. 目前可直接沿用的文獻方法

| 核心問題 | 原始研究及限度 | 轉換成 Clinical OS 的決策 |
|---|---|---|
| 系統動態改版，怎樣頻繁量測？ | She & Lin, *Efficient Benchmarking in Production: A Study of an Evolving LLM Agent* (2026-09-18), https://arxiv.org/abs/2609.21267；其生產環境比較隨機子集、歷史快取、固定分層及 IRT 適應測試；IRT 保真度佳，實際採簡單固定難度分層。 | **先採固定分層小測集**（新題/故障/交接/教材各類），持續把原始題目與難度錨點固定；樣本量與錨點不足時不建 IRT 模型。 |
| 應測最終產物還是過程？ | Li et al., *AgencyBench*, ACL 2026 https://aclanthology.org/2026.acl-long.337/；Pan et al., *Measuring Agents in Production*, ICML 2026 https://proceedings.mlr.press/v306/pan26a.html | 記錄 `artifact → engineering → independent acceptance → downstream value` 的證據轉換，不以 CI、PR 或長軌跡長度等同成功。 |
| benchmark 本身可能錯嗎？ | Suh et al., *AgentSuite*, ICML 2026 https://proceedings.mlr.press/v306/suh26a.html；Wang et al., *Search-Time Contamination*, EMNLP 2026 https://aclanthology.org/2026.findings-emnlp.760/ | 獨立稽核 task/environment/gold/evaluator；未見題放在授權隔離源，檢索與答案曝光軌跡需分開。公開 PR 不能當真實未見題私有保管。 |
| 記憶或技能越多就越好？ | Hu, CMU 2026 thesis https://publications.ri.cmu.edu/the-limits-of-prompt-based-self-improvement-in-language-model-agents-meta-optimization-and-failure-attribution；Hajimiri et al., EMNLP 2026 https://aclanthology.org/2026.emnlp-main.1657/ | 必須對照**相同模型、工具、token/時間總預算**的 native/evidence-only baseline；不因更多 memory/skills/token 或合成回歸數量而自稱進步。 |
| 不確定時，該繼續查或求助？ | Dong et al., *Value of Information: A Framework for Human–Agent Communication*, ACL 2026 https://aclanthology.org/2026.acl-long.1987/ | 比較追加證據能否實際改變行動、owner 打斷成本、風險與時間；在不需人核准的可逆低風險問題，優先自行查明與執行。 |
| 陌生／環境漂移是否能主動學？ | Wang et al., *AdaExploreBench* arXiv:2610.25950（2026-10-19；**preprint, not treated as independent field consensus**） https://arxiv.org/abs/2610.25950 | 把「發現證據不足→尋找區辨資料→環境變動後重新探索」設為未來對照的能力假說；尚不能聲稱 Clinical OS 已有該能力。 |

**可行性注意：**上述文獻來自不同環境、樣本與模型。它們支持研究方法，不等同本專案存在同樣效果；採用後需以本系統的未見真任務與合規成本證明增益。

## 2. 文獻檢索優先於無邊界猜測

每當關鍵證據不足、原有假設被反例推翻，依序：

1. **界定可證偽的決策問題：**具體任務、失敗環節、對照選項、哪個觀察結果會改變下一步。
2. **先找近期綜述，再找原始方法論和相反證據：**ACL/EMNLP/ICML/NeurIPS/ACM/相應專科指南及其引用網；檢索 benchmark、methods、metrics、sample、cost 和負面結果；查最新日期、實際發表版本與來源權限，避免只看摘要與排行榜。
3. **資料萃取：**input/exposure、任務難度、模型與工具、對照、分母、效果、成本、侷限、污染、能否遷移、反例；引用原文。沒有找到不等於證明世界上無人研究。
4. **遇到未覆蓋領域：**以相鄰研究方法提出最小可證偽假說，例如「更少獨立 QA 退修」「未見任務首次驗收率上升」「學習概念延遲測增益」；先寫明預測、可接受反例、預算與停止條件，再用低風險 shadow/小實驗證偽。不可杜撰外部文獻。
5. **把研究轉成下一個真實行動：**若再找一篇文獻不會改變 go/no-go 決策，就停止搜尋；轉為小實驗或回到既有交付。探索不自動授權醫學合併、權限擴張、付費 API 或個資輸出。

## 3. 五種研究決策（每次清楚表態）

| 決策 | 觸發條件 | 下一個可觀測結果 |
|---|---|---|
| **CONTINUE / SHIP** | 授權齊全、相對簡化基線有直接可驗收的收益，重要護欄不倒退 | 推進最近的尚未通過 gate，產生可核對實物，不延伸研究規格 |
| **PIVOT** | 已有真實失敗定位在特定環節，現方法無效，但更簡單替代方法有可測試預測 | 限定修改一個主要因子；保留原始 V1 與獨立測試 |
| **PARK** | 缺真正獨立出題／審查／來源／權限／預算，或與更高價值交付競爭資源 | 明列缺失證據和解除條件；停止無關合成追加測試 |
| **STOP / REMOVE** | 在事前可比較條件下，反覆未見題顯示對簡化方法無實用淨益、成本更高；或維護負擔持續抵銷效益 | 回退可逆增量，留下必要的錯誤回歸與結論，不刪歷史證據 |
| **EXPLORE (bounded)** | 現成研究不能處理具高價值的真實問題，且可合法低成本證偽 | 一個主要假說、一個負對照、最小可用成果、一次評估點；失敗後 PARK/PIVOT，不無限延長 |

**區分停止資助特定方向與宣告該想法在科學上無效：**低樣本、欠缺對照時只能 PARK / 尚無充分價值，不可宣稱研究已證偽。若高風險醫學 P0/P1、個資或未授權動作存在，任何預期效益不能覆蓋硬閘。

在無充分歷史分布下，不使用虛構的加權總分或自訂小數「進步程度」。初始低風險探索可設定**預算上限與單一可否證假說**；費用／模型推論要遵守 owner 既有門檻：**只有有獨立對照顯著提升自主交付才例外付費**。

## 4. 一次真實讀回：非隨機 Shadow baseline

已讀取 GitHub PR #238, #257, #260, #243 的更動檔案列表；其中 #238 PR 本文記錄特定 HEAD `8779f0abb1314eddb23cae6895479d0df4d3fac3`；GitHub workflow readback 回傳 `40866217133 completed/success`。對其他 PR 未另核獨立工程成功／醫學／讀者結果，**不把作者自述當獨立證明**。

- 實際程式／教材產物：**4 個 PR 有可查檔案**。
- 本次核實的工程成功里程碑：**1 個**；另 **3 個 NOT_VERIFIED**，不是 3 個失敗。
- 本次核實的獨立驗收：**0 個**；**4 個 NOT_VERIFIED**，不是四次驗收失敗。
- 無提示自主成功率、學習遷移、人工分鐘：**NOT_COMPUTABLE / NOT_MEASURED**。
- 這四個任務均為 owner-directed／不納入原 #137 凍結 cohort；樣本選取非隨機，**不能外推為全 repo 的成功率、階段轉換率或今日成長率**。

可重跑：
```bash
python3 -m unittest discover -s tests -p 'test_growth_snapshot.py' -v
python3 tools/growth_snapshot.py experiments/growth-measurement/selected_pr_shadow_20261031.json
```

本地以相同邏輯及四個資料案例執行，**10 個測試 PASS**；包括拒絕原 #137 cohort、虛構的 reviewer 狀態、跳過工程 gate、沒有 downstream 結果卻升級、把未知 owner 分鐘寫 0、重複 task ID。**GitHub exact-head CI 尚待獨立讀回**；程式目前只消費人工核實 JSON，不從 GitHub 即時抓全體 cohort，這是下一個技術可用性缺口。

## 5. 現階段研發優先序：給可執行的決策，不再開研究平台

| 現有工作線 | 現在的判斷 | 最值得完成的下一件事 | 最低放棄／轉向條件 |
|---|---|---|---|
| **PiCCO #243／每日新稿** | **CONTINUE／交付優先** | 實際獨立醫學/來源/EPQC 完成，再接已授權的正式站 gate；本研究不代替 reviewer | 若 P0/P1 或不可解權利阻塞，PARK 並精確列出解除條件 |
| **#241／#238 跨輪交付** | **PARK until original 72h gate, then CONTINUE** | 使用原正常排程與獨立 QA 證明 no-nudge 跨兩輪接續及實質成功 | 若只剩留言/喚醒而無交付，改修 dispatcher 的最小根因，別繼續補規格 |
| **ALE #258／#260** | **CONTINUE narrowly** | 在私有合規環境做未見題概念修補／語義抽象與簡化方法對照，先看真正學習／誤合併 | 若只增加 Concept Family tags、合成測試而無未見題收益，PIVOT/PARK |
| **XDT-01 #257** | **PARK live experiment** | 先完成私有考官權限、隔離與合法成本前提；保留已完成離線工程，不重做 | 無獨立 evaluator 或無實用正增益的驗證可能時停止新實驗維護 |
| **新持久 Claim Graph／長 prompt／新 dashboard** | **PARK / NO NEW BUILD** | 只有在等預算對照下證明既有 Lite 不能處理的跨層依賴時才啟動 | 未見題無實用增益，停止新增結構，保留必要回歸案例 |
| **高解析度評估 #265** | **CONTINUE very narrowly** | 用目前工具先建立正確的可核對證據覆蓋；之後優先接原週報，不增加排程 | 若成本大於可支持的決策數，縮回簡單的 stage/gate 記錄 |

**對未知研究空白的優先假說（目前尚非成果）：**「使用 *Evidence uncertainty + next-action value + hard-risk gates* 取代固定工作槽輪流選題，是否能在同樣工作槽/成本/安全下，提高真實 task completion、減少 owner 催促？」先與已存在的 #244 最小 shadow GDC 協調；先不建立新 dispatcher。須在 #137 72h 正式結束、相應授權、驗收和對照可得後，才能宣稱測到相對增益。
