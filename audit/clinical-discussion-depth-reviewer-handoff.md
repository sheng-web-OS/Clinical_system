# Blind Clinical Discussion Depth Review｜Reviewer-only handoff（未執行）

> **COORDINATOR / EVALUATOR ONLY — DO NOT PROVIDE THIS DOCUMENT TO THE REVIEWER.** This file discloses the expected failing case and names author-side revision artifacts. Using it as the actual reviewer prompt contaminates the blind test. Send only the [neutral reviewer packet](clinical-discussion-neutral-reviewer-packet.md), the frozen transcript, and permissible primary evidence. The new [unhinted calibration preregistration](clinical-discussion-depth-unhinted-calibration.md) includes matched valid-claim preservation controls, clean-case requirement and A/B/C comparison of native review versus a minimal reviewer-perspective switch versus full SOP. **No independent run has been performed.**

**Purpose**：驗證 Clinical Discussion Depth SOP 能否在不洩漏作者預設答案的前提，將 2026-09 九頁神外 BA aneurysm Discussion 判為不夠深入，並挑戰後續的單題 EVD 深修稿。這是供**另外一個真正分離的審稿脈絡**使用的工作說明；**建立此檔本身不是審查完成**。

## Review conditions / contamination firewall

- Phase A 只能取得**固定來源檔**：`audit/fixtures/ba-aneurysm-discussion-202609-frozen.md`（Git blob **`afe6acddeb9d8ca5d677724635b7431100d07a68`**）以及讀者任務：2026-09 神外 CBD 的 **Discussion only**，前一位已報告病歷；不需要重新做 case presentation。原稿包含 9 頁 Speaker notes 原文的完整文字，但不包括可直接核實的病人原始病歷或完整投影片影像。
- 可按需查 **原始醫學研究／指南**，不能先閱讀作者預設失敗答案、原稿批評、修訂稿或過去 ChatGPT 評分。明確禁止先讀：`audit/clinical-discussion-depth-red-20261028.md`、`experiments/clinical-discussion-depth/evd-timing-deep-rewrite-20261028.md`、`experiments/clinical-discussion-depth/evd-oral-discussion-candidate-20261028.md`、Issue #203 詳細 failure analysis、PR #205 body 的預設缺陷。
- 審稿者即使在另一段 ChatGPT 對話，也需**明確聲明先前是否已看過相關答案**。已看過不等於獨立盲審；記 `CONTAMINATED_REVIEW`，只作補充質性意見。
- 需先封存 Phase A 結論和來源、日期、審稿者脈絡識別與原稿指紋。**先提交結論再揭露作者答案**，不得事後改 Phase A 票據。

## Phase A: Source-only independent RED detection

請審稿者**先不看九頁標題所暗示的作者主線**，自原稿正文辨識對神經外科臨床決策最具價值的 1–2 個矛盾（並說出為何其他題目次之），再逐一回答：
1. 這份稿最強的解釋與最強的「尚未證明的主張」各是什麼？可指到原稿段落，不能泛泛說深度不夠。
2. 哪些機轉/候選治療其實在競爭？缺什麼病人特徵／原始證據才能選邊？若本案缺病歷，不虛構。
3. 若只允許三個專科追問，應挑哪三個最可能改變主論點的 **why / how-do-you-know / what-if**？需說明為何是重要而非枝微末節。
4. 分別裁決 Gate Q（選題）、D（論證）、E（來源適用）、R（獨立審查）：`PASS / REVISE / HOLD / NOT_VERIFIED`，每個判定附可重查理由，**不得以九頁漂亮、引用多、AI 自評當加分抵銷**。
5. 要求審稿者明確指出「哪些正確要素已經在舊稿存在」，避免靠誇大缺陷讓 RED 看似成功。

不提供預期分數、舊稿應 fail 的頁碼或問題答案。後續由 owner 於 Phase A 凍結後與作者側 RED fixture 比對。

## Phase B: Source-isolated new challenge

在 Phase A 結果封存後，再給審稿者 **未曾看過的** `experiments/clinical-discussion-depth/evd-oral-discussion-candidate-20261028.md` 及此稿所列原始證據，讓 reviewer 寫三題作者未曾看到的專家級質疑：
- Why：挑一項最可能不成立的病理生理中介，要求替代解釋。
- How-do-you-know：要求**被研究真正測到的 outcome、比較組的可交換性、適用於 BA 的程度**，不能把 OR/P 當答案。
- What-if：從**病例型態、醫療資源、臨床變化或裝置需求**改一個關鍵條件，要求説明新的取捨及不確定性。
作者在不知道題目時獨立回答；reviewer 才判定回答是否可辯護。只有 reviewer 自己寫題目但作者預先看了它們、或作者自己代答，都不是真正非預告測試。

## Phase C: Interpretation / scope

- 先核對原文與 candidate 是否同一任務、資料可得性與口述負擔是否可比較。**完整研究稿 8k+ 字對原九頁口頭報告，不能直接主張前者一定更好**。
- 保存每題 verdict、決定性引用、仍缺證據、修訂 round 與無法判的原因。
- **任何使用者未提供的原始病例資訊均留空**；不能用合成 case report 代替本案。
- 若 Phase A 獨立審查不足，Gate R=NOT_VERIFIED；若 Phase B 未完成，不能把新稿標為通過。
- 這個 packet 本身包含 PR 路徑、對應階段與中立任務，不是對作者失敗結果的提示單；審稿者實際看到的內容與順序仍須可稽核。
