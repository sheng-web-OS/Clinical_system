# 心血管群組｜因果連結第一輪實測稽核（2026-10-21）

狀態：**internal audit / PARTIAL / HOLD FOR BUNDLE PUBLICATION**。本文是 AI 的首次可重現醫學與敘事驗證，**不是原創全文四篇已核對、真人臨床同儕審查或網站教材**。

## 一、問題及本次驗證範圍

中心問題：**心肌結構與功能上的異常，何以造成不同的 filling pressure、pulmonary congestion、forward perfusion，並在不同 haemodynamic phenotype 下導向相反的治療？**

候選文章群：HCM（2026-07-14）、〈從四象限走進 LVEDP〉（2026-07-12）、〈Heart Failure：從四象限到診斷與急性失衡〉（2026-07-12）、〈利尿效果不夠，為什麼下一步不一定是加量？〉（2026-07-20），以及 DCM／〈心肌病變〉（2026-07-10）比較篇。

**原文可得性（重要）**
- **HCM 已核對完整正文**：`content/xiaoma-reading/originals/2026-07-14-hcm.md`，亦備存 `archive/xiaoma-reading/originals/HCM_從EF回到定義.md`；是否與 Facebook 已發表版本完全一致仍需查核。本文中引述的 HCM 內容僅代表已封存來源快照，不冒稱已獲 Facebook 終稿證實。
- **LVEDP／HF／Diuretics／DCM 原稿未完整取回**：在現有 GitHub 只有 `archive/xiaoma-reading/intake/2026-10-21-chat-manuscripts.md` 的 user-pasted 全文接收紀錄和 `archive/xiaoma-reading/recovery-records-20261021.json` 的歷史線索。兩者均不含可供逐段核對的文章原文。因此本輪可完成臨床**機轉和證據**查核，不能將它冒稱為**各原作之間**已完成逐段連結查核。
- 本次已搜尋可存取 ChatGPT Library／conversation／GitHub 檔案，除 HCM 外未獲上述原文；不從標題或摘要重建「原稿」。Facebook 發布版是舊文章真正 author-canonical 基準，但其全文目前也未取得。

本輪採用 `E = clinical evidence checked`、`H = supported in complete HCM manuscript`、`X = missing manuscript-to-manuscript verification`、`R = automatic inference rejected`、`P = plausible conditional bridge`。**一條關係只有 E+兩端原稿核對+反事實通過，才可能升為 group-verified；目前沒有任何一條達到整組發布的最高驗收。**

## 二、臨床因果骨架（非單線自然史）

疾病／病因 etiology 與心肌形態 morphology 不是 HF 嚴重度；幾條不同維度在同一患者並存：

1. **etiology／myocardial substrate**：HCM、DCM、phenocopies、hypertension、valvular disease；不能由 LVH、低 EF 或症狀單獨推出病因。
2. **mechanical expression**：dynamic LVOTO、mitral regurgitation、valvular lesions（不等於 myocardial diastolic dysfunction）。
3. **ventricular pressure–volume physiology**：舒張期 relaxation、passive stiffness／compliance、volume loading、heart rate／diastolic filling time、chamber geometry；此處才可理解 LVEDP 的變動。單一「壁厚」不是 LVEDP 數值。
4. **measurement and downstream circulation**：LVEDP 是 LV 舒張末瞬時壓；mean LAP／PCWP 更接近左房及肺靜脈循環平均壓力，各自不完全等價，MR/LA compliance/large V waves 等可造成顯著差異。
5. **clinical state**：congestion（肺／體循環充血）與 perfusion（器官灌流適足）是兩個臨床判斷軸；wet/dry、warm/cold 是 bedside 起點而非病因或完整定量診斷；HF 可以 EF preserved 或 reduced。
6. **intervention and feedback**：支持呼吸與灌流、確定病因／誘因、解除顯著的 LVOTO 或改善 congestion；利尿藥物作用以 natriuresis 和臨床 decongestion 衡量，不以「給藥毫克數」或「尿量一項」等同循環目標已達成。

這不是要將 HCM → LVEDP → HF → diuretics 寫成所有病人必經的一條病程，而是把四篇文章內各自解決的不同問題納入一個**能夠分岔的共同推理模型**。

## 三、實際逐邊查核（第一次，主張不是已完成原作驗證）

| Edge | 待驗證推論 | 第一輪結果 | 重要的必備中介／例外 | 原稿端點 |
|---|---|---|---|---|
| CV01 | HCM 可以在沒有 LVOTO 時仍出現 filling dysfunction | **H+E / conditional** | LVOTO 是 dynamic mechanical expression，不是 HCM 定義；病人個別填充、節律及疾病表型有異質性 | HCM 已讀、LVEDP 待讀 |
| CV02 | HCM 壁厚 → LVEDP 必然上升 | **R** | 壁厚不等於僵硬程度或 pressure–volume operating point；須結合 relaxation、stiffness、load、HR 和其他因素 | HCM 已讀、LVEDP 待讀 |
| CV03 | LV stiffness、relaxation、volume → filling pressure | **E+P / conditional** | 在相同容積條件下 stiffness 上升可提高 diastolic pressure；但同樣 LVEDP 可來自不同負荷和物性，不能逆推唯一病因 | LVEDP 缺原文 |
| CV04 | LVEDP = mean LAP = PCWP | **R** | 心室舒張末瞬時值不等於左房／肺毛細血管楔壓平均值；MR、LA compliance、V waves 可使差異很大 | HCM 有簡化用語；LVEDP 缺原文 |
| CV05 | 升高左側充盈壓可以促成肺充血與呼吸困難 | **H+E / conditional** | 需考慮 left atrial / pulmonary venous pressure、時間、肺血管通透性與其他 dyspnea 病因；並非單憑 LVEDP 一個數字判定肺水腫 | HCM 已讀、HF 待讀 |
| CV06 | preserved EF 排除低 forward stroke volume／HF | **R** | EF = (EDV−ESV)/EDV，fractional ejection ≠ SV ≠ cardiac output ≠ intrinsic contractility；EF 受 loading／geometry 影響 | HCM 已讀、HF 待讀 |
| CV07 | 有 LVOTO → dyspnea 一定來自 LVOTO | **R** | 必須測 resting/provoked gradient，評估症狀歸因及其他 filling、MR、rhythm、ischemia pathways | HCM 已讀 |
| CV08 | HCM 有 outflow obstruction 可由 gradient ≥30 mmHg 描述；≥50 mmHg 對治療評估重要 | **H+E / verified thresholds** | ≥30 為 obstruction 存在門檻；≥50 是在症狀歸因、標準治療未改善等條件下思考進階療法的閾值，非「數字一到直接介入」 | HCM 已讀 |
| CV09 | elevated left-sided filling pressure → 全身總水量過多 | **R** | 肺水腫可能以 redistribution／afterload 變動為主，並不保證 whole-body fluid overload；左側與右側充盈壓可不一致 | HF 待讀 |
| CV10 | wet/dry 與 warm/cold 是兩條不同床邊分類軸 | **E / verified clinical framework** | assessment of congestion and hypoperfusion required；四象限不直接告訴病因、血行動力學量測值或藥物處方 | HF、LVEDP 待讀 |
| CV11 | wet → 一律積極利尿；即使 hypotensive obstructive HCM 亦然 | **R** | obstructive HCM 下過度降低 preload 可加重 dynamic LVOTO；低血壓且 underfilled／LVOTO 時治療原理與明確 fluid overload 的情況相反 | HF、diuretics 待讀 |
| CV12 | HF 住院並有重要 fluid overload → IV loop diuretic 支持去充血 | **E / conditional** | 以是否有需要去除的 fluid overload、血壓／灌流、腎功能、藥物暴露與合併疾病判定；需 monitor response and harm | HF、diuretics 待讀 |
| CV13 | 利尿無效 → 只是劑量不足 → 直接加倍 | **R** | 判定真正的 persistent congestion、是否收到有效 IV 曝露、早期尿鈉／尿量、renal function、sequential nephron sodium reabsorption；調整方案可能包括 loop dosing 或合併其他部位利尿劑 | Diuretics 待讀 |
| CV14 | 2 h urine Na 與 6 h urine output 可協助早期 diuretic-response 分層 | **E / conditional** | 2026 ESC HF guideline：2 h urinary Na ≥70 mEq/L 或前 6 h 尿量 ≥100 mL/h 作滿意反應的操作定義之一；urine Na 指導治療為 IIb B1，可改善 natriuresis/diuresis，**尚未證明死亡率或 HF 再住院改善**；不可直接當個別病人固定終點 | Diuretics 待讀 |
| CV15 | acute pulmonary oedema 必然需要高劑量 loop | **R** | 2026 ESC 強調部分 acute pulmonary oedema 主要是 redistribution；優先按 BP、呼吸與實際體液負荷適度 vasodilator/support，並處理病因，非統一大劑量利尿 | HF、diuretics 待讀 |
| CV16 | 一旦同時 congestion + hypoperfusion，單純持續增加利尿即可 | **R** | 要迅速辨認 cardiogenic shock 或惡化的器官灌流、相關機轉和 hemodynamic support；可與去充血同時處理，但不可當作同一藥物加量問題 | HF、diuretics 待讀 |
| CV17 | DCM、HCM、restrictive physiology 為同一量表之互斥程度 | **R** | morphology、etiology、filling、systolic function 不同分類軸，advanced HCM 可呈現收縮功能受損；DCM 不只是「HCM 更嚴重的後期」 | HCM 已讀、DCM 待讀 |

### 重大問題：HCM 原稿中的兩個語義捷徑

**原稿句型 A：**「LVEDP 上升後，壓力會傳向左心房與肺靜脈」。作為病人生理的主線方向可理解，但教學整合版本必須在 LVEDP 與 mean LAP／PCWP 之間補入時間、壓力表型、MR／LA compliance 的關係，避免誤以為 three pressures 數值相等。此處是**AI 新教材必要精修**，不改原文檔案。

**原稿章節標題 B：**「EF 只回答 contraction，不能代表整個 pump」。正文已正確強調 fractional emptying vs actual output，但精準表述應為 EF 是 load- and geometry-dependent **systolic emptying metric**，不是 intrinsic myocardial contractility 或 adequate perfusion 的直接量測。整合版本應由 EDV、ESV、SV、HR/CO 逐步推導，不把 systolic EF 正常當成 diastolic pressure normal。

以上是來源事實與醫學概念的**初步獨立稽核**，非宣稱已證實原稿存在重大醫療錯誤。

## 四、反事實測試（用來驗證分岔而非背誦詞彙）

以下全是自編教學情境，**不是作者個案或原始病歷**；著重問「更動一個前提，決策為何反向」。

| 測試 | 核心條件 | 預期推理（不是病人個別處方） | 能抓到的錯誤 |
|---|---|---|---|
| T1 / Nonobstructive filling failure | HCM、rest/provoked LVOTO 不明顯、EF 70%、呼吸困難、需再評估左側 filling pressure | 高 EF 不排除 HF／低 SV；重心轉向 diastolic physiology、肺充血、MR、節律、其他 dyspnea 病因 | EF normal → no HF；no LVOTO → no important disease |
| T2 / Dynamic obstruction underfilling | HCM、明顯 provoked LVOTO、低血壓、狹小腔室／underfilling 證據、無可支持的大量 volume overload | 不直接套一般 wet-HF 高劑量去充血；查 preload／afterload／rate／contractility，依 HCM 指南處理 hypotension／LVOTO 並動態評估 | hypotension + dyspnea → automatic diuretic / vasodilator |
| T3 / Wet warm and poor response | 有持續 fluid overload、足夠灌流、使用 IV loop 後 2 h uNa 低且尿量不足 | 先確認導致利尿反應差的環節；可考慮調整有效 IV loop 曝露或 sequential nephron blockade，密切看 Na/K/creatinine 與去充血 | urine output low → 腎衰竭或無條件加同一劑 |
| T4 / Hypertensive redistribution | 急性肺水腫、高 SBP、體重未顯著增加／全身過多體液證據不足、無 dynamic obstruction | 可能以 afterload／redistribution 為主，呼吸支持、針對誘因和適當 vasodilator 才是重要思考；不預設需要大量 loop | pulmonary oedema → 必然全身體液過多 |
| T5 / Wet cold with organ compromise | 肺充血加上 cool extremities、低灌流、lactate 上升或尿量急減 | 應升級 shock／organ perfusion 評估，不能僅用一般 decongestion 劑量階梯處理；辨認 triggering condition | wet → 治療順序只剩加強 diuresis |

T1–T5 的機轉一致性已依現有指南作首次 AI review；**尚未執行獨立臨床審稿，也未由讀者盲測理解時間／正確率**。原始文章對這些情境的覆蓋情況目前仍是 unknown。

## 五、來源、核對範圍與更新時間

已實際讀取或以搜尋結果查閱的核心來源（不代表每份完整 guideline 所有章節都已審閱）：

1. 2024 AHA/ACC Multisociety HCM Guideline，LVOTO 的 ≥30/≥50 門檻、provocation、obstructive HCM hypotension 與 cautious diuretics：
   https://www.jacc.org/doi/10.1016/j.jacc.2024.02.014
2. 2025 ASE Recommendations for Evaluation of LV Diastolic Function / HFpEF（更新 2016 版本；diastolic measurements 與估計 LA pressure）：
   https://www.asecho.org/guideline/left-ventricular-diastolic-function-by-echo/
3. Left Atrial Hemodynamics and Clinical Utility in Heart Failure（2024 review，LVEDP vs mean LAP / PCWP，large V wave、MR）：
   https://pmc.ncbi.nlm.nih.gov/articles/PMC11440442/
4. 2026 ESC Guidelines for Management of Heart Failure（ESC 官方 2026-08-28 更新；decompensated HF、acute pulmonary oedema、diuretic response，urinary Na 及 Recommendation Table 9）：
   https://academic.oup.com/eurheartj/article/47/38/5346/8766302
   官方入口：https://www.escardio.org/guidelines/clinical-practice-guidelines/all-esc-practice-guidelines/heart-failure/
5. 2022 AHA/ACC/HFSA HF Guideline，hospitalized HF assessment of congestion/perfusion、IV loop and escalation：
   https://www.jacc.org/doi/10.1016/j.jacc.2021.12.012
6. 2025 European Journal of Heart Failure Expert Consensus urinary Na／diuretics：
   https://esc365.escardio.org/journal/96070

**待補查：**整組將來正式出版前須再對讀各 guideline 全文之適用人群／禁忌與重要原始 RCT，以及台灣現行臨床可得性；本次無權據搜尋結果稱已完成實務處方的全面安全驗證。

## 六、交付結論與下一個具體阻點

- **病理生理共用模型已建立並實際查到 17 條主要候選關係**，其中 10 條屬於「不可無條件跨越的推論」；已設計 5 個反事實測試。
- **最重要的兩個跨篇補強優先序**：第一是 LVEDP／LA／PCWP 與 congestion 的壓力—症狀橋；第二是明確 fluid overload、redistribution、obstructive HCM、hypoperfusion 如何導出不同 decongestion／support 決策。
- **整組內容發布門檻：HOLD。** 完整原稿可核對率：1/5（包括 DCM 比較篇）；若只算四篇核心主文為 1/4。這僅是 source availability，不是通過率或全站已完成篇數。
- **下一步**：從 2026-10-21 直貼原文對話及可訪的 Facebook 已發表貼文逐字回收 LVEDP／HF／Diuretics／DCM，保留原文字元與發布證據，逐篇核對本表 CV01–CV17。**在取回之前，可以完成 AI 獨立「因果橋」草稿，但不得把草稿冒充這四篇原作或聲稱整組原作驗證完成。**
- 本檔保存在私人 repo 的 `audit/`，不進 `site/pages.json`；僅此篇審核用途的臨時因果矩陣，不是要求日後常態維護全域 Claim Graph。

**核心判定：目前驗證出的不是「HCM 自然地進展到 HF 然後需要加強利尿」，而是病因／形態、功能、壓力、肺循環、灌流與藥效之間的一組有條件連結。真正的教材必須讓讀者看見哪個條件令治療方向反轉。**
