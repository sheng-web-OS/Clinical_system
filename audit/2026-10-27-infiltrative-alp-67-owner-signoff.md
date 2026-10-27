# #67｜單篇醫學驗收與發布閘門（待作者審閱）

此文件是新獨立候選的唯一驗收入口，承接 [PR #98](https://github.com/sheng-web-OS/Clinical_system/pull/98) 的 AI source/figure audit；**與 #66 Cholestasis 已發布版本及其餘兩篇不共享發布權限**。

- **文章**：`content/xiaoma-reading/integrated/2026-10-27-infiltrative-alp-hypothesis.md`，來源原稿 PR #98 blob `ea96803cc35b93cd8ab13b8cff52ae34f5970a00`；目前候選文章 blob `0e0c6e81339ea369e07a26509fa6be68da219812`（前版 `1d72b7a089b446aa1c47c5bbdcf9fb8ed3e8b226`；此回合清理了讀者不需看到的內部編輯狀態）（後續變更需重核）。
- **來源**：`content/xiaoma-reading/infiltrative-alp-sources-20261027.md`，只含本篇醫學來源；不重製 Pocket 原書 pixels。
- **P0 安全判斷 [PENDING OWNER]**：單一 SPEP 陰性不能排除 AL amyloidosis；SIFE、UIFE、sFLC 只適用於合理懷疑的情境，檢驗陽性仍非組織 typing。
- **P1 臨床推論 [PENDING OWNER]**：2020 AL hepatic case 95% 僅指受檢切片，不是全肝；同病例 ALP 85 IU/L，不能推算 ALP 敏感度。
- **關鍵圖像 [PENDING OWNER]**：`fig-infiltrative-alp-update`、`fig-alp-claim-boundary`、`fig-alp-amyloid-real-case`；須判斷「是否傳達必要的反事實與限制」，不只是排版可見。
- **Agent 工程責任**：同 HEAD Figure Gate、靜態建置、回歸測試、360/390/1280 實際渲染、來源與內部連結；AI-source check 不冒稱獨立醫師 peer review。
- **發布停止條件**：P0/P1/圖像語意或全文未接受，均維持 Draft/HOLD。取得文章明確驗收後**另取得** owner 對本篇合併／正式部署的授權；不能因 CI success 自動發布。

## 單篇作者簽核（預留，未有決定）

- P0：PENDING；請標明 ACCEPT／REQUEST CHANGES 與具體段落。
- P1：PENDING；請標明 ACCEPT／REQUEST CHANGES 與具體段落。
- Figures：PENDING；逐 ID ACCEPT／REQUEST CHANGES。
- Whole manuscript：PENDING。
- Merge / production deploy：NOT AUTHORIZED。


## 2026-10-27｜發布候選前的讀者界面清理

- **Agent 原始來源逐段複核（非 owner approval）**：ASH 2026 Diagnosis of AL amyloidosis 指引 good-practice 明定 electrophoresis 單獨不可作為 AL 篩查／排除工具，疑似 AL 需 serum/urine immunofixation + sFLC；陽性單株蛋白非沉積物確診，診斷需 tissue amyloid + subtyping。Doe-Williams et al., Case Rep Gastroenterol 2020 PMID 32518538 的 50 歲個案原文顯示 SPEP 為 acute inflammatory pattern、serum IFE 陰性、urine IFE 微弱 lambda 陽性；肝切片 **95% of specimen**、ALP **85 IU/L**、ALT 14、AST 24、bilirubin 0.57。用於破除 ALP 與切片受累程度線性關聯，不能外推敏感度。
- **來源**：[ASH 2026 正式全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC13425172/)、[Karger 2020 原始病例](https://karger.com/crg/article/14/2/271/86741/Massive-Hepatomegaly-Secondary-to-Amyloidosis-with)、[PubMed](https://pubmed.ncbi.nlm.nih.gov/32518538/)。
- 最新正式文章 blob：`0e0c6e81339ea369e07a26509fa6be68da219812`；PR HEAD 此後若移動，需重新取檔案 blob。內部審查狀態仍為 **P0/P1/figure/whole manuscript PENDING，merge/deploy NOT AUTHORIZED**。
