# 肝臟檢驗｜原稿接收與原表逐項對讀（2026-10-26）

**編輯身分**：2026-07-18〈肝臟檢驗，先告訴你病人在哪裡〉的使用者直接提供全文快照。完整原文見 [2026-07-18-liver-tests-user-supplied.md](2026-07-18-liver-tests-user-supplied.md)。**未確認 Facebook 公開發表版本；不可標為作者已發表 canonical 正稿。** 本檔是審查札記，不能覆蓋原文。

**原書證據層級**：使用者在 2026-10-26 對話中另附一張《Pocket Medicine》第九版肝臟檢驗表的**局部截圖**，肉眼確認截圖內容（標題 `Tests of hepatic function`、`Patterns of LFTs` 及 `R-value`）。尚未取得可逐頁查核的完整 9E PDF 頁碼及相鄰腳註；PNG 僅保存在對話附件，**本 Git 分支未封存其原像素**。不可把以下文字對讀稱為已核對完整 Pocket Medicine 原始頁、亦不可公開轉載此截圖。

## 一、原稿核心及增量分類

- **A｜作者已完成**：將 biochemistry pattern、serial injury signal、synthetic function 三層解混；不把 ALT 高值當作功能衰竭，不把 ALT 下降當作病情改善；重點是「檢驗提供問題位置，不直接提供病名」。
- **B｜跨篇連接**：與 HBV phase（病毒複製不等於肝細胞炎症）、cholestasis（疾病機轉與生化表型不一對一）、infiltrative ALP pattern（膽道流動與肝內浸潤分辨）銜接。其他篇尚未正式回收者不建立假連結。
- **C｜讀者必要前提**：原稿以語句描述 normalized ALT/ALP，但未寫具體公式與 >5 / 2–5 / <2 判準。正式整合教學稿需就地先說明 ULN 再引入公式：
  `R = (ALT ÷ ALT_ULN) ÷ (ALP ÷ ALP_ULN)`。這是依檢驗型態分群，**不是肝功能衰竭風險分數**；bilirubin 不納入 R。
- **D｜安全與邊界**：下面的逐項限縮必須在新整合版就地落實，不能修改此份作者來源快照。

## 二、已直接讀到的原表訊息

| 局部截圖項目 | 可確認訊息 | 不能直接推出的事 |
|---|---|---|
| `Albumin` | 肝臟蛋白合成指標；半衰期約 15–18 天，急性 hepatocyte injury 可以正常 | 正常 albumin 不能排除急性嚴重肝損傷；偏低不能單獨證明肝硬化 |
| `PT` | 多種凝血因子由肝合成；部分因子周轉短，功能惡化後 PT 可較快延長 | PT/INR 並非肝合成功能的專一測試，也不能單獨預測肝硬化出血風險 |
| `Hepatocellular` | AST/ALT 相對較高，病毒性肝炎、MASLD 等常見 ALT > AST，alcohol-associated hepatitis 可出現 AST:ALT ≥ 2 | 比值不能單獨診斷酒精性肝炎；AST 也可能來自骨骼肌 |
| `Ischemic hepatitis` | AST/ALT 可顯著升高 | 不能由酵素高值或下降速度單獨診斷缺血，也不能脫離循環狀態推斷改善 |
| `Cholestatic` | ALP 上升，direct bilirubin 可上升 | 未能單憑 ALP 區分肝內／肝外阻塞，或排除非肝源性 ALP |
| `Infiltrative` | AST、ALT 可接近正常，ALP 卻明顯升高，bilirubin 不一定高 | 不能用「ALT 正常」排除肝內病灶；infiltrative 仍是鑑別線索而非診斷 |
| `Nonhepatic` | Skeletal muscle injury：AST 可明顯大於 ALT；bone disease：ALP↑ 但 GGT 可正常；hemolysis：indirect bilirubin↑ | 不應把任何單一上升指標直接歸肝源性 |
| `Wilson disease` | 截圖提及 fulminant 時 ALP:total bilirubin <4 | 只適用在特定急性肝衰竭鑑別脈絡的輔助線索；需核實單位和原文定義，不能單獨確診 Wilson disease |
| `R-value` | ALT 及 ALP 各除以各自 ULN；>5、2–5、<2 的生化表型分群 | 同一疾病可隨病程改變 R，不能用 R 替代 etiology/work-up |

**影像界限**：此為聊天附件的局部圖片對讀，不表示完整表旁註、前後文或讀者 PDF 頁碼已全部回收。圖片若要永久歸檔，須在私有庫另行封存原像素與出處；公開頁面以獨立原創圖解並合理引註優先，不照搬原表。

## 三、正式整合稿必須補足的決策箭頭

1. **先確認資料身分**：ALP 為多源性（骨、肝等）；孤立升高時可用 GGT 或 isoenzyme 確認來源。GGT 上升本身也沒有病因專一性。AST 異常需要考慮肌肉來源；isolated bilirubin elevation 先 fractionate。
2. **再分類而非診斷**：R 的 ULN 必須來自各自實驗室；不能把 AST/ALT >2 或 high ALP 當確診。Cholestatic pattern 的下一步通常先由超音波尋找膽道擴張，並結合病史、藥物、血清學；超音波陰性不排除 microscopic/intrahepatic disease，後續 MRCP 或 biopsy 由風險和假說驅動。
3. **平行追蹤傷害與功能**：酵素下降需要和 bilirubin、INR/PT、意識狀態、循環與用藥一起讀。Albumin 時間延遲且受腎病、營養、發炎、稀釋影響；INR 也受 warfarin、vitamin K 缺乏、DIC 等影響。不能把 PT 當「不需評估其他因素」的專一肝功能試驗。
4. **不能錯過的急症分流**：急性肝損傷且 INR 顯著惡化、出現 encephalopathy（尤其無已知肝硬化）時，不再只是一般 liver tests 的分類問題；需立即評估 acute liver failure、病因及肝臟移植中心轉介。常用定義為急性病程（<26 週）、INR ≥1.5、任何程度 hepatic encephalopathy 且無既有肝硬化，特定疾病仍有例外；**即使尚未達完整 ALF 定義，也可能需要提早升級**。不同於 acute decompensation/ACLF。
5. **臨床反例**：同樣 ALT 800，一人由 5000 回落、INR 和意識改善，另一人 ALT 下降但 INR 延長且意識惡化；只有後者需要高度警覺 liver failure 的進展，不能以共同下降曲線推論相同方向。兩例皆為「推理示例」，**不是病人實測或文獻病例**。

## 四、來源與後續驗收

- Pocket Medicine, 9E，使用者於 2026-10-26 附 `Tests of hepatic function / Patterns of LFTs` **局部截圖**；完整 PDF 頁碼與圖表註腳 **pending**。
- ACG 2017, *Evaluation of Abnormal Liver Chemistries*: https://gi.org/guideline/evaluation-of-abnormal-liver-chemistries/ 。R ratio、isolated ALP 來源確認、bilirubin 分型與診斷分流。
- AASLD 2025, *How to approach elevated liver enzymes?*: https://www.aasld.org/liver-fellow-network/core-series/back-basics/how-approach-elevated-liver-enzymes 。不同指標生理意義、ALT 升高程度與風險不成比例、PT/albumin 的外肝干擾。
- AASLD 2026, *Practice Guideline on adult liver failure*（2026 年版）：https://doi.org/10.1097/hep.0000000000001644 。急性肝衰竭早期辨認、緊急肝移植中心轉介，不宜等到所有定義完全成立才轉介。
- AASLD 2025, *Defining and Managing Acute Liver Failure*: https://www.aasld.org/liver-fellow-network/core-series/back-basics/defining-and-managing-acute-liver-failure 。

**發布判斷：HOLD。** 原文完成私人回收；尚未核對歷史刊本身分、完整 9E 原頁和圖表權利，也未為新整合稿建立正式 figure-gate evidence、AI medical QA 與網站 build/CI。此分支不修改 `content/xiaoma-reading/originals` 或 `site/pages.json`，不可宣稱公開網站已收錄。

**視覺化構想（僅記意義，不複製原表）**：用兩幅彼此獨立的原創教學圖：① pattern 位置（以 R ratio 比較 normalized ALT vs ALP，另置 bilirubin 分型、非肝源排除）；② 同一病人隨時間變動的 AST/ALT 與 INR／bilirubin 並列圖，展示「injury 下降但 synthetic failure 進展」的不一致。正式繪圖時標示假設／模擬，不杜撰真實案例。
