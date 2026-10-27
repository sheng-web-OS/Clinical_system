# CTICU 氧輸送：原始來源與圖像查核

本文對應〈血氧看起來不差，DO₂i 為什麼仍下降？〉。此頁提供原始資料的直接入口，並指出原論文資料與本篇教學圖可以、不能支持的推論。

## Civelek 2025：CPB 個案與兩張原始表格

[Civelek 等人 2025，Cureus 原始出版 PDF（7 頁）](https://www.cureus.com/articles/446799-advanced-metabolic-guided-perfusion-concepts-in-an-obese-patient-undergoing-cardiac-surgery-a-case-report.pdf)，DOI 10.7759/cureus.99447。2026-10-27 已直接以頁面影像檢查原 PDF 的第 4 頁 **Table 2** 與第 5 頁 **Table 3／4**，並對照案例敘述。

- **Table 2（第 4 頁）**：CPB 期間整體摘要 SaO₂ 98 ± 0.5%、PaO₂ 230 ± 25 mmHg、pump flow 5.4 ± 0.25 L/min、DO₂i 295 ± 10 mL/min/m²、SvO₂ 76 ± 2%；DO₂i <280 的時間列為 8.5 分鐘。這些摘要值**不是**任何一次 DO₂i 下降事件的同步 SaO₂。
- **Table 3（第 5 頁）**：Hb 為術前 13.4、CPB 欄 10.4、術後 30 分鐘 11.2、術後 12 小時 9.7 g/dL。術後 12 小時 PaO₂ 99.4 mmHg、pH 7.38，**沒有同步 CO 與實測 SaO₂**，無法計算當時的實際 DO₂。
- **來源本身的內部矛盾**：文字稱 DO₂i <280 持續 8.5 分鐘，另一段卻稱 DO₂i <300 不足五分鐘；若時間範圍及指標定義相同，兩句不能同時成立。文字提到 CPB 起始 Hb 8.2 g/dL，但 Table 3 的 CPB Hb 是 10.4；缺少採樣時點解釋。文字起始 heparin 300 IU/kg 與 Table 4 heparin 400 U/kg 亦不一致。這些屬原始報告的記載問題，不能靠本站示意圖補造資料。
- **溫度邊界**：個案 CPB 在 30°C，作者同時描述 37°C 標準化與溫度校正的 DO₂i；事件敘述未逐一標清所用序列。不能直接把其數值視為 normothermic CPB 門檻的完整驗證。

本站圖 1 是依作者文字重組的「流量不足／攜氧容量下降」**原創教學示意圖**，不是 Table 2、Table 3 的轉描或時間曲線；不能證明事件同期 SaO₂、Hb、pump flow 或術後 cardiac output，更不能由單一病例的正常 lactate 推論整體策略具因果療效。

## Pocket Medicine 第九版：PA catheter 與 Fick

*Pocket Medicine*, Ninth Edition，私人閱讀版 PDF 第 **31–33、373–374 頁**。2026-10-27 已核對原書文字：第 32 頁「Cardiac output」段落列出 Fick 方法、動靜脈氧含量差與量測 VO₂ 的限制；第 374 頁「Fick cardiac output」再次列出 Hb × 10 × **1.36** ×（SaO₂ − SMVO₂），並強調估計 VO₂ 可能不準確。

本站使用 **1.34 mL O₂/g Hb** 為常見 CaO₂ 近似係數；原書動靜脈差公式用 **1.36**，兩者是不同參考近似值，不宜誤稱逐字一致。這些頁面可作生理公式與採樣限制的原書定位；本站未重新發布原書插圖，也不以任何單一公式取代床邊循環評估。

## 2024 EACTS/EACTAIC／EBCP：兩種場景、兩份指引

[2024 patient blood management guideline 原文 PDF](https://matcvs.org.my/documents/guidelines/2024%20EACTS%20Guideline%20on%20Patient%20Blood%20Management.pdf)，第 **32 個 PDF 頁面／印刷頁 32，Recommendation Table 11** 已於 2026-10-27 直接檢視表格與註腳：

- 若病人的臨床狀況允許，建議採限制性 RBC 輸血觸發值（≤75 g/L，即 Hb 7.5 g/dL），相較寬鬆策略（≤90 g/L）；表列 **Class I，Level A**。這不是所有病人的無條件輸血指令。
- **在 CPB 期間**，Hct 18–24% 且其他方法不足以維持組織氧合時，可依 DO₂ 與 cerebral oximetry 考慮 RBC，表列 **Class IIb，Level B**。此建議特別限定 CPB，不等同於術後 ICU 的固定門檻。
- 表 11 註腳 a／b／c 分別為建議等級、證據等級及文獻來源；沒有另列適用每位病人的通用 SvO₂ 數字。

另見 [2024 EACTS/EACTAIC/EBCP CPB guideline](https://pmc.ncbi.nlm.nih.gov/articles/PMC11947607/)：Recommendation Table 43 對 **normothermic CPB** 的 DO₂i 280–300 mL/min/m² 為 **Class IIa、Level B**；Recommendation Table 45 說明 Hct 18–24% 的氧合判斷，附註 d 的情境為 DO₂ >273 mL/min/m² 且 cerebral oximetry 滿意。不能將 CPB 的幫浦流量門檻直接套用到離開 CPB 後的 ICU 自體 cardiac output。

[TRICS III](https://pubmed.ncbi.nlm.nih.gov/29130845/) 與 [2023 AABB RBC guideline](https://doi.org/10.1001/jama.2023.12914) 是其他場景的輸血證據；[Okamoto 等人 2026 年 CVICU 回溯性研究](https://link.springer.com/article/10.1186/s13054-026-06149-9) 不能證明輸血的因果效益，也不支持「SvO₂ 69% 就該輸血」之類的固定觸發值。

## 使用本頁的界線

來源表格的部分數字與註腳已直接核對，**不代表**所有文獻都完成獨立醫師審查。本站圖像沒有複製 Pocket Medicine 圖像，也沒有將 CPB 的 redo-valve 個案寫成 CABG 或術後 ICU 個案。治療仍需依病人的出血、循環狀態、器官灌流與團隊處置判斷。
