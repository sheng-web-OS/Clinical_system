# #67｜單篇醫學驗收與發布閘門（待作者審閱）

此文件是新獨立候選的唯一驗收入口，承接 [PR #98](https://github.com/sheng-web-OS/Clinical_system/pull/98) 的 AI source/figure audit；**與 #66 Cholestasis 已發布版本及其餘兩篇不共享發布權限**。

- **文章**：`content/xiaoma-reading/integrated/2026-10-27-infiltrative-alp-hypothesis.md`，來源原稿 PR #98 blob `ea96803cc35b93cd8ab13b8cff52ae34f5970a00`；目前候選文章 blob `1a806cd9a214816e1f3a0f0dd3ba510be494607b`（前版 `1d72b7a089b446aa1c47c5bbdcf9fb8ed3e8b226`；此回合清理了讀者不需看到的內部編輯狀態）（後續變更需重核）。
- **來源**：`content/xiaoma-reading/infiltrative-alp-sources-20261027.md`，只含本篇醫學來源；不重製 Pocket 原書 pixels。
- **P0 安全判斷 [OWNER ACCEPT — CORE ONLY, 2026-10-27]**：單一 SPEP 陰性不能排除 AL amyloidosis；SIFE、UIFE、sFLC 只適用於合理懷疑的情境，檢驗陽性仍非組織 typing。
- **P1 臨床推論 [PENDING OWNER]**：2020 AL hepatic case 95% 僅指受檢切片，不是全肝；同病例 ALP 85 IU/L，不能推算 ALP 敏感度。
- **關鍵圖像 [PENDING OWNER]**：`fig-infiltrative-alp-update`、`fig-alp-claim-boundary`、`fig-alp-amyloid-real-case`；須判斷「是否傳達必要的反事實與限制」，不只是排版可見。
- **Agent 工程責任**：同 HEAD Figure Gate、靜態建置、回歸測試、360/390/1280 實際渲染、來源與內部連結；AI-source check 不冒稱獨立醫師 peer review。
- **發布停止條件**：P0/P1/圖像語意或全文未接受，均維持 Draft/HOLD。取得文章明確驗收後**另取得** owner 對本篇合併／正式部署的授權；不能因 CI success 自動發布。

## 單篇作者簽核（預留，未有決定）

- P0：ACCEPT — ONLY the core safety decision that negative SPEP alone does not rule out AL, with clinically appropriate SIFE/UIFE/sFLC and tissue typing distinction. The acceptance reply was scoped explicitly to P0, not whole article. Evidence: [PR #119 owner-scope comment](https://github.com/sheng-web-OS/Clinical_system/pull/119#issuecomment-6432460860).
- P1：PENDING；請標明 ACCEPT／REQUEST CHANGES 與具體段落。
- Figures：PENDING；逐 ID ACCEPT／REQUEST CHANGES。
- Whole manuscript：PENDING。
- Merge / production deploy：NOT AUTHORIZED。


## 2026-10-27｜發布候選前的讀者界面清理

- **Agent 原始來源逐段複核（非 owner approval）**：ASH 2026 Diagnosis of AL amyloidosis 指引 good-practice 明定 electrophoresis 單獨不可作為 AL 篩查／排除工具，疑似 AL 需 serum/urine immunofixation + sFLC；陽性單株蛋白非沉積物確診，診斷需 tissue amyloid + subtyping。Doe-Williams et al., Case Rep Gastroenterol 2020 PMID 32518538 的 50 歲個案原文顯示 SPEP 為 acute inflammatory pattern、serum IFE 陰性、urine IFE 微弱 lambda 陽性；肝切片 **95% of specimen**、ALP **85 IU/L**、ALT 14、AST 24、bilirubin 0.57。用於破除 ALP 與切片受累程度線性關聯，不能外推敏感度。
- **來源**：[ASH 2026 正式全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC13425172/)、[Karger 2020 原始病例](https://karger.com/crg/article/14/2/271/86741/Massive-Hepatomegaly-Secondary-to-Amyloidosis-with)、[PubMed](https://pubmed.ncbi.nlm.nih.gov/32518538/)。
- 最新正式文章 blob：`1a806cd9a214816e1f3a0f0dd3ba510be494607b`；PR HEAD 此後若移動，需重新取檔案 blob。內部審查狀態為 **P0 CORE ACCEPTED；P1／figure／whole manuscript PENDING，merge/deploy NOT AUTHORIZED**。


## Figure 1 semantic revision — author review still PENDING

- New figure ID unchanged: `fig-infiltrative-alp-update`. Earlier 4-column text matrix replaced with three independently-labeled decision branches at the **same ALP/GGT signal**: (A) drug/pruritus/immune evidence → PBC/DILI differential; (B) known tumor + new lesion → increased infiltrative suspicion, imaging +/- tissue; (C) hepatomegaly + otherwise unexplained proteinuria → testable amyloid suspicion with **SPEP alone insufficient**, SIFE/UIFE/sFLC and validated tissue subtype where appropriate. Every branch names the alternative and next diagnostic action.
- Article blob **`1a806cd9a214816e1f3a0f0dd3ba510be494607b`**, PR current HEAD at audit time `9b94820aa2bc6c96bfb7913adfb1b202a612baf5`; separate scoped responsive CSS and Figure Gate teaching role were updated. Branches are **hypothetical** and do not equate a single lab result with a microscopic diagnosis.
- This is an Agent revision for *semantic clarity* and must be **reviewed by the owner**, not a claim of figure ACCEPT or whole-article release permission. Re-run same-head CI and 360/390/1280px figure screenshots. Publication **HOLD**.


## 2026-10-27 作者最新回覆：#67-P0 限定接受（全文仍 HOLD）

- 作者對前一則明確僅詢問 **#67-P0** 的問題回覆「我覺得可以了，推進文章發佈」。因此 **ACCEPT #67-P0 核心判斷**：SPEP 單獨陰性不能排除 AL；只有在合理懷疑時才結合 SIFE、UIFE、sFLC，單株蛋白檢驗不取代組織沉積證據及 validated typing。這是作者自審，非獨立同儕審查。
- 上述允許 Agent 完成技術整合與發布前驗證，**不等於** #67-P1、三張新版圖像語意、全文或合併部署一併接受。P1 / Figures / Whole article / Merge-deploy 均維持 PENDING。
- GitHub 原始證據：[PR #119 作者回覆範圍紀錄](https://github.com/sheng-web-OS/Clinical_system/pull/119#issuecomment-6432460860)。原始回答所針對的文章 blob `1a806cd9a214816e1f3a0f0dd3ba510be494607b`，此分支 copy 仍是同一篇實際正文；後續修改 P0 需要再審。
