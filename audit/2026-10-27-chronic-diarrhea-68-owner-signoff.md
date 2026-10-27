# #68｜單篇醫學驗收與發布閘門（待作者審閱）

此文件是新獨立候選的唯一驗收入口，承接 [PR #98](https://github.com/sheng-web-OS/Clinical_system/pull/98) 的 AI source/figure audit；**與 #66 Cholestasis 已發布版本及其餘兩篇不共享發布權限**。

- **文章**：`content/xiaoma-reading/integrated/2026-10-27-chronic-diarrhea-signal-etiology.md`，來源原稿 PR #98 blob `bae387fcbe7d37379d318e5631d6e5df32585fa2`；本分支文章 blob `c09e3c1b778a8a08a0761afe4438b554a493e27e`（後續變更需重核）。
- **來源**：`content/xiaoma-reading/chronic-diarrhea-sources-20261027.md`，只含本篇醫學來源；不重製 Pocket 原書 pixels。
- **P0 安全判斷 [PENDING OWNER]**：正常 colonoscopy 外觀或正常 calprotectin 不能排除 microscopic colitis；有適應症時需左右結腸 biopsies；alarm features 不等待 gap。
- **P1 臨床推論 [PENDING OWNER]**：290−2(Na+K) 是估計值，不是實測 osmolality。10/60/130 為合成示例；50–100/125 灰區，不能由 cutoff 命名疾病。
- **關鍵圖像 [PENDING OWNER]**：`fig-diarrhea-evidence-sequence`、`fig-diarrhea-gap-interpretation`；須判斷「是否傳達必要的反事實與限制」，不只是排版可見。
- **Agent 工程責任**：同 HEAD Figure Gate、靜態建置、回歸測試、360/390/1280 實際渲染、來源與內部連結；AI-source check 不冒稱獨立醫師 peer review。
- **發布停止條件**：P0/P1/圖像語意或全文未接受，均維持 Draft/HOLD。取得文章明確驗收後**另取得** owner 對本篇合併／正式部署的授權；不能因 CI success 自動發布。

## 單篇作者簽核（預留，未有決定）

- P0：PENDING；請標明 ACCEPT／REQUEST CHANGES 與具體段落。
- P1：PENDING；請標明 ACCEPT／REQUEST CHANGES 與具體段落。
- Figures：PENDING；逐 ID ACCEPT／REQUEST CHANGES。
- Whole manuscript：PENDING。
- Merge / production deploy：NOT AUTHORIZED。
