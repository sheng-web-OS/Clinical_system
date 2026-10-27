# 評估資料完整性：前後版本對照（2026-10-27）

## 結論與範圍

**修正版對本組資料完整性反例較好；尚未驗證 AI 醫學／教學品質提升。**

比較基線為 PR #155 commit `0fff0879b0dd98c5a2bd31406053d21e434eb0f5` 的 `tools/summarize_autonomy_eval.py`。保留基線，不回寫舊版結果。兩版使用相同的兩案例 × 三 trial 合成資料及十種資料變形，逐項比對事先固定的合法／非法預期。這是程式輸入與計算的工程檢查，AI 模型試跑數為 **0**。

| 檢查 | 基線 | 修正版 |
|---|---|---|
| 同案例以一個 worker context 冒充三次獨立試跑 | 錯誤放行 | 拒收 |
| 同案例以一個 trace reference 冒充三次獨立試跑 | 錯誤放行 | 拒收 |
| 作者與 reviewer 識別只差前後空白 | 錯誤放行 | 拒收 |
| 布林值 true 冒充 schema version 1 | 錯誤放行 | 拒收 |
| suite_id 空白／空字串 | 錯誤放行 | 拒收 |
| planned trial ID 含前後空白 | 錯誤放行 | 拒收 |
| 漏掉原定失敗 trial | 正確拒收 | 正確拒收 |
| 已提示缺陷位置 | 正確拒收 | 正確拒收 |
| 未量測人工時間 | 正確保留未知 | 正確保留未知 |
| 同一紀錄容器以不同 case/trial fragment 定位不同執行 | 合法輸入通過 | 合法輸入通過 |

本組檢查正確處理 **4/10 → 10/10**；非法紀錄誤放行 **6 → 0**。這些分母僅是列出的十個測試輸入，不是醫學缺陷率、模型成功率、統計獨立樣本、罕見風險界限或人工作業節省。

## 最小修正

- 每案例的跨 trial worker context 及 trace locator 不可重複；同一容器可以用不同片段定位，不因共用 log 檔一概拒收。
- 正規化作者／評閱識別的前後空白再檢查分離。
- 嚴格要求整數 schema、非空 suite identity、無前後空白的 case/trial identity。
- 加入對應回歸，保留既有 missingness、分母、硬性失敗與不宣稱自主驗證的邊界。

**剩餘邊界**：不同名稱仍可指向同一真實執行；檔案／trace 內容與 reviewer 身分仍未由可信執行器驗證。因此輸出繼續保留 DECLARED_NOT_AUTHENTICATED、DEVELOPMENT_ONLY 與所有 validation/release flags=false。不能把這次修正稱作已完成獨立性認證。

## 可回查證據與重現

原始逐項結果及兩版程式 SHA-256 見 [data-integrity-comparison-20261027.json](data-integrity-comparison-20261027.json)。固定輸入由 tests/test_autonomy_eval_summary.py 的 `inputs()` 產生；每項變形由相應測試方法描述。原有十五項檢查保留，修正版共二十項測試通過。

重現時將上述 immutable commit 的程式另存至隔離路徑；載入目前 regression module 後，只替換它的 `module` 和 `SCRIPT` 為基線路徑，對兩版執行同一 unittest suite。基線在新增反例下應失敗；修正版應通過。不要編輯原基線，也不要把 unittest 合成紀錄填成 AI trial。合法的 shared-container control 與 unknown-cost control 都須保留。

本次只修同一 canonical PR #155，未修改醫學正文、舊稿 baseline、發布清單、權限、憑證或排程。下一層仍是隔離模型的真實同條件比較及獨立語義判定；在那之前維持「AI 品質／節時效益未驗證」。

