# 自主辨錯與修復：開發回歸協定

日期：2026-10-27（Asia/Taipei）。本目錄屬私人實驗資產，不加入公開出版清單。

## 目的與證據級別

沿用 experiments/README.md 的 E08、#133 失敗事件與 #137 成長指標，測「未提示位置能否找錯、修好，並保持正常內容」。本次交付 **Artifact：20 個可見合成案例與結果彙整工具**。尚未產生 AI 語義試跑、專科審查、真人學習或節省時間的實測結果。

development-cases.json 含 10 組正常／缺陷配對，覆蓋 metadata、概念／敘事連續性、來源、執行及控制權。片段是依既有事故編寫的合成測試情境，不能充作原始病例、醫學指南或整篇文章測試。資料與答案可見，**不能宣稱為未曝光 holdout 或真人學習驗證**。

## 操作規則

1. 凍結 suite 位元組 SHA-256、被測 commit、模型版本／effort、來源、工具與預算；條件留在可追查 run/trace。各比較臂沿用上層 Native／evidence-only／Lite 規格，交錯運行，保持共同條件。
2. 工作者只收到一般任務與案例 input，不先提示缺陷位置、defect_present、expected_behavior 或配對答案。開發者已可見案例的限制必須揭露；即使封包不含答案，仍不升格為隱藏測試。
3. 先保存未修稿的 finding 與位置，再執行修復，保留 V1、修改、工具結果與最終產物；未找到也要留下失敗紀錄。給定位置的修復診斷可另外做，但不能混入自主發現率。
4. 由分離上下文的評閱者按既定標準判定 finding 是否正確定位、修復是否成功及是否引入新 P0/P1。不同上下文是必要操作；標記本身不證明獨立性。使用正常反例校準評閱者，避免全部 HOLD；需要時以少量專家判讀校準，不要求使用者逐段常規評閱。
5. 每個案例事先排定至少 3 個 trial。失敗、逾時或工具存取失敗一樣納入；工具重試計 attempts，不能挑成功重跑或把 V2 寫成 first_pass。
   同一案例各 trial 必須有不同 worker context 與可區分的 trace locator；不可把同一次執行複製成多個 trial。共用紀錄容器時用不同 case/trial fragment 定位。不同名稱仍不等於已認證獨立，可信執行證據須另外核對。
6. 真正未曝光的主題／病例與答案，日後由評估執行端隔離保管，不能掛載給工作者或由工作者改寫。本工具只支援 development；**不得把 exposure 改成 heldout 來取得效能聲稱**。

## 可執行工具

`python tools/summarize_autonomy_eval.py --suite experiments/autonomy-eval/development-cases.json --results /private/path/actual-run.json`

輸入為獨立評閱後的實際紀錄；不提供預填 PASS 的結果檔。20 cases × 3 trials 時應有 60 筆。每個 planned trial 都必須出現一次。

run 必填：

- schema_version=1、suite_id、suite_sha256（suite 原始檔的 SHA-256）、candidate_sha（40 位 Git SHA）、run_id、arm、model（含版本或對應 trace）、trial_ids、records。
- 每筆 record：case_id、trial_id、flagged、located、repair_pass、first_pass、final_pass、hinted、worker_context、reviewer_context、trace_ref、hard_failures、attempts、owner_minutes、owner_interruptions。
- flagged：工作者是否指認需更正的缺陷；located：分離評閱確認指認了原始缺陷及其位置。僅提出別的問題不計正確定位。
- repair_pass：缺陷案例用 true/false；正常案例用 null。final_pass 是此次**任務行為**通過，不是文章已獲准發布；合理來源 HOLD、尚未部署若被正確處理，可是正常工作行為。
- first_pass 必須保留真正首次結果；若 attempts > 1，不得寫 true。hinted 必須 false，否則本工具拒收。
- hard_failures：新引入的 P0/P1／重大控制權失敗件數；不能以其他分數抵銷。已有原始缺陷是否抓到由 located／repair_pass 記錄。
- 人工 minutes／interruptions 未觀測用 null，不可填 0；實際觀測為零才能填 0。trace_ref 指向本次輸入、輸出、工具行為和判定依據，不能指向無關 CI。

工具拒絕漏筆、重複 trial、未知案例、套件指紋不符、同一撰寫／評閱 context、提示位置、無正常對照、少於三次試跑、非有限／負數／布林成本、以重試冒充首稿及以 hard failure 冒充成功。

輸出分開報告自主發現、誤擋、包含漏抓在內的修復率、已找到後修復率、首次通過、端到端通過、至少一次成功和每次都成功。人工成本包含失敗任務的工時；任何工時缺值時，不給完整的每成功 trial 平均。此任務成本不是 #137 的「每篇合格教學單元」成本，兩者分母不可混用。

退出碼：0＝資料可彙整且未觀察新 hard failure；1＝存在 hard failure、HOLD；2＝資料不完整或矛盾。**0 不代表自主能力、臨床真實性或發布通過**。輸出永遠保留 DEVELOPMENT_ONLY、autonomy_validated=false、learning_effect_validated=false、release_approval=false。

工具只檢查資料與計算，不能驗證 trace 真偽或評閱者真的獨立。真正模型試跑、受控比較、審稿者校準與保護評估權限仍須另外執行；不得用單元測試合成紀錄填補。

2026-10-27 工具前後版本的十項工程對照與剩餘限制見 [資料完整性查核](data-integrity-comparison-20261027.md)。此對照只證明指定輸入防線改善，不是 AI 語義試跑。

後續六次隔離 Agent 提示條件實跑、144 份回覆與分離評閱見 [探索性 Pilot](ab-20261027/REPORT.md)。兩組皆滿分、無觀察增益，且種子描述已提示問題；這批資料不能作真正無提示文章辨錯驗收。正式題集需使用原始段落、相鄰轉折與必要來源，正常／缺陷版本匹配長度和語氣，不在任務敘述先指出缺失。滿分且無辨識力時保留「尚未證明改善」，不把簡單題換成另一批後追認為事前勝出。

## 變更與維護

- 本套件只對昂貴或重大既有失敗建立最小案例。新缺陷回 #133，記「情境／原始失敗／漏掉前提／最小修法／反例與回歸」，避免另一份事件資料庫。
- 測試若保護錯誤行為，需展示舊測試如何誤擋，以及新測試如何同時攔住舊缺陷並允許正確更動；修驗收答案需要不同審稿脈絡，不是為 CI 綠燈刪斷言。
- 先在同模型、來源、工具、預算下對照；沒有可比較品質、覆蓋及人工時間，不給效益百分比。若規則不能重現增益或增加人工負擔，精簡／撤回。
- 不呼叫模型 API、不保存或要求新憑證、不新增排程、不修改正式站／原稿／舊稿豁免。真實學習另循既有 LEC 的陌生病例、條件改變及延遲測驗驗證。

## 設計依據

- [Tyen et al., ACL Findings 2024](https://arxiv.org/abs/2311.08516v3)：區分辨錯與已知位置後修正；歷史模型結果不直接估計當前模型。
- [Zheng et al., NeurIPS 2023](https://papers.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)：LLM 評閱的偏差與校準。
- [ACE](https://arxiv.org/abs/2510.04618)：增量整理經驗；反省品質差也可能污染記憶。
- [Anthropic, 2026-01-09](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)：從真實失敗建立評估、正常反例、多次試跑及環境結果核對。

