# Clinical OS｜ABG × Surgical ICU 深度系列：首次成稿品質試驗

日期：2026-10-26（Asia/Taipei）｜狀態：PRIVATE EDITORIAL PLAN / HOLD，不是已完成正文、醫學審查或正式出版。
執行原則：沿用 Master Prompt v5.1、EPQC、LEC、Figure Gate 與 site/pages.json；不開第二套教材／題庫系統，不修改歷史原稿。本計畫僅在私人實驗分支，不放入公開出版白名單。外科 ICU 情境用於教學案例，不公開私人輪訓、病人資料或任何個人紀錄。

## 0. 主命題與範圍

> ABG 是氧合、有效換氣、酸鹼與代謝／灌流線索的共同觀察，不是獨立的病因診斷，更不是單一治療指令。

臨床順序：先確認氣道／呼吸／循環有無立即危險 → 確認血氣檢體與採集條件（動脈／靜脈、FiO₂、呼吸器設定、採樣時間）→ 解構 pH / PaCO₂ / calculated HCO₃⁻ / PaO₂ → 配對同時點 electrolytes、albumin、lactate、Hb、尿量、血壓、灌流及器官支持 → 建立競爭假說與預期代償 → 介入後重新檢查「哪個指標為什麼改變」。

不得由 ABG 單獨推定組織灌流、休克類型、絕對氧輸送、乳酸升高機制、呼吸器設定或腎替代治療適應症。不能把 PaO₂/SaO₂ 代表整體氧輸送，也不能把「pH 已正常」視為生理安全。

## 1. 先確認已有作品，避免重製

以下為 2026-10-26 main 已發布資產（需於開稿當日重核最新狀態）：

- content/xiaoma-internal-medicine/lessons/2026-10-21-hypoxemia.md — 氧合、肺泡換氣、A–a 與攜氧；
- content/xiaoma-internal-medicine/lessons/2026-10-23-acid-base.md — pH 與 process、Winter、AG／albumin、delta、代償中斷；
- content/xiaoma-internal-medicine/lessons/2026-10-25-hypercapnia-physiology.md — V̇E/V̇A/VD 與呼吸泵；
- content/xiaoma-internal-medicine/lessons/2026-10-22-hypercapnic-failure.md — NIV 與插管條件；
- content/xiaoma-internal-medicine/lessons/2026-10-25-hypoxemia-mechanisms.md — A–a、V/Q、shunt；
- content/xiaoma-internal-medicine/lessons/2026-10-26-copd-emptying.md — auto-PEEP、困氣與呼吸器。

原則：已有 A（充分說明）則連結；B（跨篇關係）加最短必要橋；C（真正欠缺）才寫新主線；D（必要限制／更新）進行原篇修訂。不可將已寫之原作者／舊教材概念重新命名當新發現。已有「pH 正常仍可能混合障礙」完整主文，不另建同義章。

## 2. 預定八篇：以床邊決策而非課本分類切分

| 順序 | 擬題與單一核心張力 | 必須建立的中介與決策 | 既有連結 |
| --- | --- | --- | --- |
| 01 / **首次成稿試驗** | **術後 pH 下降，為什麼不一定代表組織缺氧？** | 血氣顯示 acidemia→釐清呼吸／代謝→Na/Cl/HCO₃⁻與校正 AG、lactate、albumin→高氯性酸化 vs 乳酸相關酸化、可共存→液體來源、容量／氣道問題與灌流觀察各自如何處理。Stewart/SID 先建直覺再作進階，不以公式堆砌。 | 既有酸鹼篇、HF／灌流 |
| 02 | **術後乳酸升高，為什麼不能直接下補液指令？** | 乳酸生成／清除、氧輸送／氧耗、兒茶酚胺與術後背景、Hb與循環；區分「需立即找可逆性低灌流」與「固定只靠乳酸追液」。追蹤灌流與液體反應、出血／感染／低心輸出之條件。 | 氧輸送、HF四象限 |
| 03 | **嚴重代謝性酸中毒，為什麼插管前後可能更危險？** | Winter 預期通氣 vs 病人實際呼吸負荷、接近極限的 VE、插管短暫 apnea 與 post-intubation minute ventilation 不足；安全與適應症優先，切勿把單一 RR 當通氣保證。 | 既有酸鹼、V̇A、NIV |
| 04 | **插管後 PaCO₂ 上升，為什麼不一定只要提高 RR？** | 實際呼吸器 VT、RR、dead space、呼出時間、auto-PEEP、氣流波形、Pplat／氣道壓、機械通氣安全；辨認真通氣問題與 CO₂ 產生改變。 | COPD、hypercapnia |
| 05 | **給了很多氧，術後 PaO₂ 為什麼仍不好？** | FiO₂ 取得方式、A–a / P:F 的不同目的、atelectasis、pulmonary edema、aspiration、ARDS 等分叉；影像、肺超音波、循環與通氣設定聯合判讀。 | 低血氧與 shunt |
| 06 | **NG drainage／利尿之後 HCO₃⁻ 上升，為什麼不是所有 alkalosis 都一樣？** | 胃酸流失／腎臟 HCO₃⁻ 維持、chloride/K/ECF、尿氯判別前提與利尿劑干擾；依容量與氯狀態辨別可修正原因。 | 利尿、酸鹼 |
| 07 | **pH 很低且 AKI，為什麼 bicarbonate 不等於救回病人？** | 酸血症的生理後果、CO₂ 負荷、鈉／容量、Ca 與呼吸支持、AKI、RRT 狀況；逐項讀 BICARICU-2 的死亡率與 KRT，不能從次要指標外推存活利益。 | AKI、酸鹼 |
| 08 | **這張血氣真的可靠嗎？ABG、VBG 與連續抽血的判讀界線** | ABG vs VBG 何者可替代、PaO₂ 不可由 VBG 代替、採血／line flush／air bubble／延遲、FiO₂ 與體溫／時間差、analyzer calculated HCO₃⁻、同時點配對電解質；以有衝突的血氣讀數反推檢體。 | 全系列底層 QA |

閱讀路線：01 + 03 + 05 為 Surgical ICU 最高優先三個臨床情境；02/04/06/07/08 按需要深化。第 08 篇的採檢核查規則必須前置到每一篇，不得等待讀完第 08 篇才知道採檢條件。編輯不以固定日期或固定篇幅強推發布。

## 3. 第一篇實際案例與可核來源

**真實 case report 候選（已核讀出版社公開 HTML 正文；Table 1 數值尚須視覺核對後才可抄入正文）**：
Tabuchi M et al. *Hyperchloremic metabolic acidosis due to saline absorption during laser enucleation of the prostate: a case report.* JA Clinical Reports 8:20 (2022). DOI: 10.1186/s40981-022-00499-3
https://link.springer.com/article/10.1186/s40981-022-00499-3

原文：七十多歲男性手術中約 90 分鐘出現氣道壓上升、ETCO₂ 波形不良、腹脹；更換氣道時發現口咽／頸部水腫。術中經破裂膀胱吸收大量沖洗生理食鹽水，估算未回收正差約 +6400 mL；術後 ABG 顯示明顯高氯性代謝性酸血症，研究者的 simplified Stewart 分析指出 chloride 為主要酸化因素，而低白蛋白有反方向效應、lactate 效應有限。因氣道風險持續插管至術後第一天。不能把單一個案概括為所有術後酸中毒；也不能用表格未核值硬填 ABG 數字。

**一般 SICU 背景 cohort（不能捏成一個病人）**：
Park CM et al. *Factors related to post-operative metabolic acidosis following major abdominal surgery.* PubMed PMID 22985420。172 名術後 SICU 族群，觀察到術後代謝性酸化與大量 saline／高氯及 lactate 的關聯；屬回溯資料，不能直接得出單病人因果或所有補液策略定論。
https://pubmed.ncbi.nlm.nih.gov/22985420/

**底層規範**：
- AARC Blood Gas Analysis and Hemoximetry 2013（非聲稱 2026 新版）：https://doi.org/10.4187/respcare.02786
- ANZSRS ABG Sampling Position Statement 2024：https://doi.org/10.1111/imj.16439
- AAFP Acid–Base Interpretation: A Practical Approach 2025（已更正版）：https://www.aafp.org/afp/2025/0200/acid-base-interpretation
- SCCM Surviving Sepsis Campaign 2026（只在相符的 sepsis context 使用，不外推所有術後病人）：https://www.sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026
- BICARICU-2 JAMA 2025：https://doi.org/10.1001/jama.2025.20231 （90日死亡率無顯著差異；KRT 使用較少，注意研究設計與次要終點）。
- 小麻第 9 版第 158–162 頁已在既有酸鹼來源頁記錄核讀範圍；第一篇正式寫作仍須取回並目視相關原書 Figure 4-1、代償表與相鄰註腳。醫學來源與圖像重製權分開查。

第一篇敘事骨架：
A. 從真實病例的通氣困難／水腫與術後酸血症進入，先回答氣道／循環是否需要立即支持。
B. 釐清這份 ABG 哪些是實測、哪些是計算，以及尚缺哪些 electrolytes/albumin/lactate。
C. 從 chloride 擴張／strong ion difference 的方向性，拆開 HCO₃⁻ 變低與「一定多產酸」的不同意義；用不同來源的 lactate acidemia 對照，指出兩者可共存。
D. 以原文 Table 1 的時間線與真正臨床調整，辨識哪些關係有直接紀錄、哪些仍是作者推論；不能將單一 case 認定其他治療最佳。
E. 回到外科 ICU：術後看到低 pH，要同時確認容量、血流、血紅素、氧合、氣道、體液輸入輸出、藥物／輸液與潛在出血或感染。最後用新情境變更 chloride / lactate / albumin 一項以觀察如何改判。

圖像最低設計：① H-H / chloride–SID 與 lactate 不同路徑的原創因果圖；② 來自病例 Table 1 的實際可核時間線／圖表（依 CC BY 4.0 及個別 credit 查核標示），並分開「實測／衍生值／作者推論」。兩張圖皆需 375–390 px 真正可閱讀版，不以寬 SVG 橫滑冒充行動版驗收。

## 4. 首次成稿品質試驗：先評初稿，再談改稿

**目的**：是否能在不依賴使用者逐次發現缺口的情況下，自發寫出可以交付的臨床教材。

1. **凍結任務與來源**：第一篇選定後記錄初始 brief、可取得來源清單與模型／工具條件；原稿與既有文章只作已公開先備，不能先看使用者新一輪逐段糾錯。來源無法取回者標未核實，不能捏造。
2. **建立 first-draft snapshot**：第一份完整文章連同來源紀錄及第一版圖放入私有草稿，記 commit SHA；在它被審查前不覆寫。不能以修改後達到 90 分追認初稿也達標。
3. **分離審稿**：用 EPQC A–G 七軸、病例與醫學 source audit、Figure Gate、作者先備缺口、實際手機圖閱讀驗收。AI 同輪自評只作內部查錯，不能當獨立 reviewer。必要外部醫師審查另標。
4. **硬性失敗**：P0/P1 錯誤；虛構患者檢驗數值；用病例相關性宣稱因果通則；誤抄 Figure/Table/footnote；缺少理解主線必要的術語和中介；將處置建議脫離氣道／循環／腎臟安全前提；公開侵權或患者隱私。P0/P1 不能被總分補償。
5. **首次成稿品質分數 100**：核心命題與敘事取捨 20；前提與因果中介 20；床邊安全與反事實改判 20；病例／文獻 fidelity 15；原圖／原創圖的功能與手機可讀性 10；語言與認知成本 10；跨篇最小必要連結與 provenance 5。
6. **暫定門檻**：初稿 90/100 以上、EPQC A–G 均至少 3/4、無未解 P0/P1、重要原圖真實讀回、病例數值可追溯、核心手機版可讀；低於門檻可修稿但初稿結果仍記失敗。一次成功僅是 artifact，不是穩定能力的證明。
7. **後續重測**：在 01／03／05 三種差異夠大的 SICU 任務中，分別記「初稿達標率、人工指出的高階/基礎遺漏、介入次數及分鐘、修後有無新錯」。三篇成功僅屬小型 pilot，不能聲稱較 Native GPT 高品質，後續再做固定來源對照。

**本分支驗收**：只有計畫與既有內容盤點；尚未完成第一篇、未建立 first-draft snapshot、未實際審閱 Pocket 原圖或出版社 Table 1 像素、未跑醫學實測、未發布。未來由原系統出版流程決定是否發行，無第二個目錄或新網站。
