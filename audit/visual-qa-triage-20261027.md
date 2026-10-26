# Clinical OS｜全站圖像品質監督：2026-10-27

**範圍**：對 `site/pages.json` 66 個公開頁的來源 Markdown 進行靜態結構掃描。57 個 `figure`（23 篇文章）：32 個純 HTML/CSS 結構、19 個 SVG、6 個圖片引用。對應版本及每張圖 id／指紋見 [visual-legacy-baseline.json](visual-legacy-baseline.json)。

**這是第一階段靜態掃描，不是 57 張視覺內容已看過的審核。** 純文字 CSS 畫面不必然不好、SVG 不必然正確；在實際桌面/手機呈現、醫學語意及原始證據逐張核對之前，一律 `legacy_unreviewed`。資料夾中保留的原書圖片、圖片合法公開引用、已核原始醫學證據，與最終插在網站上的圖片是不同狀態。

## P0｜作者已指出教學圖失敗；停止以既有圖作成功案例

| 文章 | 優先審查圖 | 已知失敗類型／實際需要證明的教學增量 |
|---|---|---|
| 肝臟檢驗 | `liver-independent-axes` | 三文字卡，沒有呈現 R-value normalized ALT/ALP 的比較，亦沒有傷害訊號與功能訊號分離的時間曲線；重做草稿見 PR #73 |
| HBV phase | `fig-hbv-three-questions`、`fig-hbv-seroconversion`、`fig-hbv-decision` | phase ≠ stage、virus replication ≠ inflammatory activity、治療分支非線性；逐圖檢查是否真正可見，而非重說文章 |
| HBV signals | `hbv-observation-inference-action` | 觀察值 → 潛在狀態 → 行動的不確定性不能用三段文字卡代替 |
| WPW | `wpw-pathway-figure` | SVG 確有傳導路徑，但要以心房、AV node、AP、心室同一解剖參照重建各種節律差異、方向及 ECG 結果 |
| Pre-excited AF | `af-ecg-evidence`、`af-two-exits` | 必須讓讀者看出經 AV node 篩選 vs accessory pathway 下傳，並真正在病例 ECG 上驗證，不能只放箭頭 |
| WCT／ACLS | `wct-decision-figure` | ECG 不確定性、血行動力學與藥物禁忌的決策分界；不得把處置順序當作診斷路徑 |

上列是使用者明確反饋以及逐圖原始碼認知任務的對照。**P0 不是已完成重畫／驗收**。

## P1｜純文字／卡片結構優先批次複核

網站其他 HTML/CSS 結構圖，特別是以下與「卡片替代圖像」失敗模式高度相似的頁面：
- `2026-10-21-hypoxemia.md`：6 圖，偏分類與支持措施列表；逐張確認氣體流向、氧合／換氣分流是否真的可見。
- `2026-10-22-exam108-renal-foundations.md`、`2026-10-23-hf-lvedp-figures.md`、`2026-10-24-asthma-variable-airflow.md`、`2026-10-25-pneumonia-severity.md`：各自檢查是否真有測量的維度、相互制約與病例時間方向。
- `2026-10-26-exam108-heat-rhabdo.md`、`2026-10-26-exam108-cpr-airway.md`、`2026-10-26-exam108-appendicitis.md`、`2026-10-26-constipation.md`：文字分支是否比正文產生更高的辨識力，否則刪圖保留文字。
- `2026-10-26-vte-visual.md`：檢查共同血栓風險、DVT/PE 競爭假說與不同停止規則；複雜分支可保留，但必須看得出關係而非只看得見句子。
- `2026-10-27-cticu-abg-cabg-lactate.md` 的 `cticu-measurement-layers`：應呈現不同測量如何在循環/供氧推理上連接，而不是四段結果列表。

## P2｜SVG 與有實際數值的原創圖

`diuretics-visual`、`acid-base`、`hypoxemia-mechanisms`、`hypercapnia-physiology`、`copd-emptying`、`cticu-abg-cabg-lactate` 等 SVG：逐一審查座標定義、量化比例、圖例、病人實測與模擬數值的區別、手機替代視圖，以及原始病例可否支持繪出的因果關係。SVG 的存在不是品質通過。

## P3｜來源圖與影像清晰度／權利

DCM 文獻圖 3、Pocket Medicine 第九版 hypoxemia 與 hypercapnia 原圖 2、COPD 個案 CT 1。檢查原圖的 citation、授權與必要性、放大後的清晰度、caption、截圖範圍及關鍵符號是否完整。不用原圖為自己設計的錯誤流程圖背書。

## 一張圖的發布 QA

1. **唯一任務**：讀者的錯誤心智模型與預期矯正的推論是否可獨立驗證？
2. **形態對題**：機轉要真有可見的空間或生理中介；數據要有坐標／單位／比例；時間要有共同方向；決策要有條件與禁忌；若只改文字排版，刪圖。
3. **來源與界線**：原圖／獨立重繪／教學模型／真實病例的身份不能混淆，檢查來源、取樣、混雜及極端反例。
4. **實際畫面**：在至少 360px 手機與桌面實際渲染後截圖檢查，不可只自稱 responsive。
5. **獨立驗收**：完整圖加上前後正文做醫學與認知審核；獨立複查；產生有版本指紋的 QA 記錄。視覺 QA pending 不能寫成 passed。

**系統治理**：現有 57 圖全部是 `legacy_unreviewed`，可在原網址維持原有可讀性，但不准因 figure-gate 結構通過而自稱教學圖驗收完成。任何新增或修改的 figure 皆須版本匹配的審查與桌面／手機截圖，否則 build HOLD。此規範不需要使用者逐張替 AI 找錯，但不虛構「機器能自動判定醫學圖品質」的能力。
