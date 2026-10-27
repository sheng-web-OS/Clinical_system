# Lab Medicine morning panel｜第一輪來源、數值與編輯稽核

**對應課程規劃**：Issue #180  
**候選正文**：content/xiaoma-internal-medicine/lessons/2026-10-27-lab-medicine-morning-panel.md  
**形式與風險**：私有分支 manuscript draft；不在 site/pages.json，未合併，未部署。  
**狀態**：HOLD — 本輪為作者同一執行脈絡的初步校閱，**不是獨立 AI 審稿、人工腎臟／血液／檢驗醫學同儕審查或真實讀者測試**。

## 主命題與區別

- 從一張早晨檢驗單重建多系統病人狀態：床邊危險訊號、檢體品質、相互作用的生理改變與下一次抽血的目的。
- 相對既有 acid-base、diuretics、sepsis 教材，增量在「跨面板 + 三時間軸 + 檢驗不可信時的平行安全分流」；避免重寫酸鹼深度原文。
- 初始病例為**自編模擬**，不宣稱文獻病例；AHRQ PSNet *Hemolysis Holdup* 是獨立的真實警示例，不可把其病程或數據搬進模擬病例。

## 已核對的數值與單位（教學自編）

- 尿量 170 mL ÷ 70 kg ÷ 8 h = 0.30357 mL/kg/h → 0.30，符合尿量低於 0.5 持續八小時。
- Creatinine 1.0→1.7 mg/dL：二十四小時內上升 0.7；同時相對基線 1.7×，若無更嚴重的其他條件，對應 KDIGO 2012 stage 1 功能性 AKI。
- ANC 17.5 × 0.88 = 15.40 × 10³/µL；反例 3.0 × 0.8 = 2.4、3.0 × 0.1 = 0.3。
- 同時點生化 AG = 134 − (102 + 18) = 14 mmol/L。假設 albumin 2.8，經驗校正 = 14 + 2.5 × (4 − 2.8) = 17；均不能單獨證實病因。
- Winter 預期 PaCO₂ = 1.5 × 18 + 8 = 35 ± 2，ABG PaCO₂ 35；pH Henderson–Hasselbalch 近似 6.1 + log₁₀(18 ÷ (0.03 × 35)) = 7.334，對應教學 pH 7.33。
- Glucose 210、Na 133：ESE 2014 指引 2.4 係數估算 = 135.64；Katz 1.6 係數 = 134.76。**第一版引用 ESE 卻以 1.6 作唯一計算，已在後續 commit 修正**。原指引於 2014 年發布勘誤，正文已說明單位與不同係數的局限。
- 所有數值沒有拿跨時點任意拼接 AG；修訂後 ABG 與 07:00 生化同步採檢；快速病情變化時仍須檢查實際採檢時間與配對來源。

## 網頁原始證據與查核層級

| 實際查核位置 | 查核層級 | 本文可支持的主張／限制 |
| --- | --- | --- |
| NICE NG148 官方 HTML Recommendations 1.1–1.5，https://www.nice.org.uk/guidance/ng148/chapter/Recommendations | 官方線上條款文字 | AKI 門檻、尿檢與阻塞評估、合併症與透析分流；不能以單一 SCr 門檻決定透析 |
| KDIGO 官方 AKI/AKD 主題頁 https://kdigo.org/guidelines/acute-kidney-injury/ | 官網狀態文字 | 2026 版仍是 draft after public review；不可提前升格成正式推薦 |
| KDIGO 2024 CKD 官網 https://kdigo.org/guidelines/cKD-Evaluation-and-Management/ | 官網頁 + executive summary | GFR/albuminuria 和 chronicity 的共同評估；2027 focused chapter 仍為 public review |
| AHRQ PSNet, Hemolysis Holdup https://psnet.ahrq.gov/web-mm/hemolysis-holdup | 專家病例文字 | 溶血可使 K 結果不可靠；並不必然造成假性「較高」結果 |
| *Laboratory Artifacts in Clinical Medicine*, Mayo Clinic Proceedings 2026, DOI 10.1016/j.mayocp.2026.04.009 | PubMed 摘要 + journal 網頁 summary；**未取得完整論文** | pseudohyperkalemia、EDTA platelet clumping 等假性異常的概要 |
| UKKA Treatment of Acute Hyperkalaemia official page https://www.ukkidney.org/health-professionals/guidelines/treatment-acute-hyperkalaemia-adults-0 | 官網版本／更新頁；**未目視核對 July 2026 PDF 算法** | 只能支援臨床風險與本院指引必要性；具體給藥流程與劑量 HOLD |
| European Hyponatraemia Guideline https://academic.oup.com/ejendo/article/170/3/G1/6668028 and correction https://academic.oup.com/ejendo/article/171/1/X1/6661472 | 官方期刊 HTML 及勘誤 | 2.4 per 100 mg/dL；明確避免原版公式排印／單位錯誤 |
| MedlinePlus CBC and Differential (official) | 官方臨床教育網頁 | CBC 與 DC 的量測對象，ANC 作臨床運算而非來源直接給定數字 |
| Choosing Wisely Canada, Using Labs Wisely, https://choosingwiselycanada.org/hospitals/labs-test/ | 現行專業建議頁 | 限定於穩定患者避免無臨床問題的 daily CBC/chemistries |

## 初步自我審稿／安全硬閘（不能代替獨立審稿）

- **通過：** 自編病例身分、單位、時間軸、數學、自編反事實、真／假 K 並行檢查、AKI≠病因、輸液後 Hb 下降≠已排除失血、DC 百分比≠ANC、慢性 eGFR 不能套用急性情境、逐項抽血需有目的。
- **修正：** 源於第一次檔案寫入的酸鹼教材相對路徑錯誤已修復並核實目的檔存在；Na-correction 來源係數不一致已修復。
- **尚未通過：** 分離寫作與審稿的獨立語義 review、逐段 packet / editorial-semantic-reviews.json、UKKA July 2026 原始 PDF 的完整療法圖核對、外部病例資料可合法展示／對照、手機 360/375/390 視覺 QA、完整 CI。因**尚未列為公開頁面**，以上應在決定發布前按最小必要步驟完成，不應偽稱通過。
- **風險邊界：** 應由當院 critical value 通報與臨床 protocol 決定急性電解質處置；本文沒有提供具體 insulin/calcium/IV K 劑量，不能被拿來取代醫囑或在低血壓情境下自動決定再輸多少液。

## 下一個最有價值的工作

1. 對正文做真正分離的審稿，獨立查主要 P0/P1：模擬病例 AKI stage、K/ECG、低鈉校正、AG、輸血／出血邊界；逐段評估核心中介與冗餘。
2. 使用已發布、可查病程的檢體假異常 case report 開展 **第二篇：當檢驗值「看起來不可能」時，如何安全驗證而不是失去病人？**，涵蓋溶血、EDTA platelet clumping、採血輸液污染、pseudohyponatremia、時間差；不可把文獻案例混編。
3. 依 Issue #180 評估「完整 lab panel」有無比既有分科文章新增能力；A 級舊進度（2027 二月筆試前）不被此系列的發刊數排擠。

**發布條件**：來源、數值與版本核對 → 獨立 review 完成 → semantic packet 和 receipt → CI → mobile QA → 明確出版許可 / 既有授權 → Cloudflare production readback。任何一步不能用上一步的成功冒稱。
