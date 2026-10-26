# Clinical OS｜ABG × Cardiothoracic ICU 深度系列：首次成稿品質試驗

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

## 2. 使用者最新臨床場域：心臟、胸腔外科術後為主

2026-10-26 確認：下一階段 SICU 以心臟、胸腔外科術後為主。因此原本「一般腹部手術 saline absorption」只保留為高氯性酸化的補充比較，不再作主病例，也不成為第一篇。新系列以 CABG、瓣膜、主動脈與 CPB、胸腔鏡／開胸／肺切除術為主要臨床脈絡。原先擬定八篇的未執行計畫仍保存在 Git 歷史中。

床邊整合順序不變：血氣 sample/setting/time 正確性→即刻氣道／循環危險→氧合與有效換氣→acid-base process→Hb、心輸出與氧輸送／氧耗、代謝、微循環→術式及支持設備條件→再測及反事實。ABG 本身不含 ScvO₂/SvO₂、CI、echo 或 PA catheter 的資訊；需從對應檢體及儀器取得，不能把不同時間點資料偽裝成一張 ABG。

### A. 心臟手術後：四篇

| 次序 | 擬題 | 必須釐清的決策張力 | 舊文定位 |
|---|---|---|---|
| **01 / first draft pilot** | **乳酸 14.8、ScvO₂ 卻 95%：CABG 術後，究竟該相信哪一個數字？** | lactate production/clearance、early/late timing、CO×CaO₂、Hb/SaO₂、ScvO₂ 解釋邊界、CPB/epinephrine 與 cardiac tamponade/bleeding/LCOS 的排查；BE≠pH，文獻未提供 pH 必須明說 | acid-base、hypoxemia、HF/LVEDP |
| 02 | **SpO₂ 100%，為何低 Hb 或低 cardiac output 的心臟術後病人仍缺氧？** | SaO₂ vs CaO₂ vs DO₂、hemodilution、失血、輸血適應症需個別判定，組織氧耗與心輸出動態，ScvO₂ 不能單獨排除局部缺血 | oxygen delivery、HF 四象限 |
| 03 | **離開 CPB 後 HCO₃⁻ 降低，為什麼不只有 lactic acidosis？** | saline/prime、chloride、albumin 與 AG，Stewart strong ion difference 的方向性；hypothermia/rewarming，將相互獨立的 acidifying/alkalinizing forces 與實際血氣接起來 | 已有酸鹼篇（避免再教一遍 Winter/AG） |
| 04 | **低溫 CPB 的同一份血氣，alpha-stat 與 pH-stat 為什麼判讀不同？** | 37°C 報告值與體溫校正、CO₂ 管理、不同體溫策略的生理及適用情境；不把兒科、深低溫停循環與一般成人 CPB 隨意互推 | 新增高專一性 CPB 橋樑 |

### B. 胸腔手術後：三篇

| 次序 | 擬題 | 內容與安全邊界 | 舊文定位 |
|---|---|---|---|
| 05 | **肺切除後提高 FiO₂，PaO₂ 為什麼仍持續下降？** | lung resection、atelectasis、分流、液體／心因性與非心因性 pulmonary edema、aspiration、ARDS；PaO₂、FiO₂、P/F、A–a 的不同資訊量與時間、影像、超音波；引用可追溯真實 lung-resection case | 已有 A–a/shunt |
| 06 | **One-lung ventilation 造成低氧，為什麼不能單靠增加 FiO₂？** | nondependent lung shunt、hypoxic pulmonary vasoconstriction、dependent lung PEEP / VT / positioning、tube malposition、術野與血流動力；術中與 ICU 術後邊界須分開 | 已有 V/Q、shunt |
| 07 | **拔管後 PaCO₂ 升高，為何不能只認為是 opioid 或 COPD？** | residual anesthetic/analgesia、hypoventilation、pain/splinting、atelectasis、dead-space、呼吸肌疲勞、氧療 masked hypoventilation；NIV / reintubation 依氣道與臨床失代償決定 | 高碳酸、NIV、COPD |

### C. 兩類術後共同：兩篇＋高階專題

| 次序 | 擬題 | 內容與邊界 |
|---|---|---|
| 08 | **插管後 pH 變好，病人真的更安全了嗎？** | ventilator VE/VA、CO₂ 清除、氣道與氧輸送、肺保護性通氣、胸腔手術殘肺壓力、心臟術後 PEEP 與靜脈回流／RV，校正 pH 可能改變 hemodynamics |
| 09 | **ABG 正常，為什麼心胸外科術後仍可能需要 ICU？** | 釐清 ABG/VBG/ScvO₂、採樣與 FiO₂、A-line 問題、時間差、乳酸與 hemodynamics、術後出血、低心輸出、tamponade 等未在一張 ABG 出現的危險 |
| Advanced / 按需 | **VA-ECMO 上半身氧合，為什麼不能只看氧合器之後的血氣？** | mixing point、differential hypoxemia、right radial ABG 与 pre/post-oxygenator sampling；僅設備實際相關時開稿，不以 ECMO 複雜知識排擠常見 ICU 決策 |

預定先跑 01（心臟）、05（胸腔）、08（呼吸器）三篇不同壓力案例的「首次成稿盲審／人工介入」小型 pilot；不能拿三個稿件當作已證實改善。

## 3. 第一篇：真實病例與來源核對（先准備，初稿另檔凍結）

**Case series：** Wardhana A, Kurniawaty J. *Hyperlactatemia Post-CABG: Case Studies in Three Patients.* MajAnestCriCare. 2025;43(3). DOI 10.55497/majanestcricar.v43i3.429。全文 PDF：https://macc.perdatin.org/index.php/my-journal/article/download/429/365/3106

2026-10-26 已實際取得 10 頁原始 PDF，並目視印刷第 278 頁的 Table 1 與第 279 頁的 Figure 1。Table 1（原始 paper PDF 第 4 頁，zero-index p3）提供三名 CABG 病人 pre/CPB/post/T0–T5：lactate、base excess、ScvO₂、venous–arterial PCO₂ gap、glucose；時間註記 T0 ICU 到院、T1 4h、T2 8–10h、T3 12–14h、T4 18–20h、T5 24–30h。**原表並未完整列出 pH、PaCO₂、PaO₂、HCO₃⁻、Hb**，不能從 BE+Lactate 冒充完整 ABG 或倒算 pH。作者對 epinephrine / type-B 的說法仍屬推論，無單例因果對照。

第三例：69 歲、術前 EF 45%、CPB 108min；術後 TTE CI 3.1 L/min/m² 但臨床不穩且需 temporary pacing 和 catecholamines（含 epinephrine）。T0 ICU lactate 3.6、BE -7.69、ScvO₂ 92.6%；T1 (4h) lactate 14.8、BE -15.7、ScvO₂ 95%；T2 (8–10h) lactate 14.8、BE -7.90、ScvO₂ 92.1%；T3 (12–14h) lactate 8、BE -3.8、ScvO₂ 82%。三名患者不合併為一個病例，不把「CI 正常」說成無低灌流，不把 ScvO₂ 95% 說成每個器官氧供安全。

**當代 guideline（正式來源）：** EACTS/EACTAIC/EBCP 2024 cardiopulmonary bypass guideline，online publication 2025-02-14：
https://pmc.ncbi.nlm.nih.gov/articles/PMC11826095/
需對讀 LCOS 及 acid–base homeostasis/alpha-stat/prime 等節，記錄情境限制。其 reference 框架說明 lactate、ScvO₂ 等需合看，normal systemic oxygen delivery 不能排除區域性缺血。

**Review / 補充：**
- Minton J, Sidebotham DA. *Hyperlactatemia and Cardiac Surgery.* J Extra Corpor Technol 2017，全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC5347225/ 。提供早/晚與 epinephrine mechanisms；舊文所謂 late-onset benign 不可直接當排除 shock 規則。
- 2026 cohort *Severity and timing of elevated lactate correlates with mortality after cardiac surgery*，PMID 42637069；峰值幅度及晚於24小時的時點和更差結果相關，屬風險關聯，不是特定個案的病因或固定治療門檻：https://pubmed.ncbi.nlm.nih.gov/42637069/
- 2026 review *Rethinking Lactate in Cardiac Surgery and Intensive Care* DOI 10.1053/j.jvca.2026.03.010；可作機轉補充、不能代替真實病例：https://pubmed.ncbi.nlm.nih.gov/41963151/

**第一篇硬性敘事要求：** 真實病例→術後立即危險分流→逐段解混 ABG vs venous lab and CO、pH vs BE vs lactate、DO₂ vs CO vs ScvO₂→生產/清除、微循環/epinephrine→手術後具體可逆原因（bleeding, LCOS, tamponade, RV dysfunction, ischemia, sepsis）及互斥與共存假說→時間序列哪些變化能和不能推論→反事實改判。不要假裝所有升高 lactate 都安全，也不要說 lactate 增高就必補液。

**第一篇必要圖像：** ①自己從 Table 1 數字重建的 T0–T5 lactate/BE/ScvO₂ 多軸概念與時間視覺，標示不同單位，資料缺失按 N/A；② DO₂ / oxygen extraction / lactate sources／clearance 的平行機轉分支；③ 心臟術後床邊同步檢驗表。初稿可先用文字 table + Mermaid 原創圖表做快照，figure Gate / 真正 mobile 圖視覺仍須單獨驗收，不因 private draft 有圖即聲稱 Figure Gate 通過。

**胸腔第二個病例候選：** *Acute respiratory failure following lung resection*, Thorax 2003：https://thorax.bmj.com/content/58/9/820 （網頁曾回 403，須於正式寫作驗證原文可得）；*Causes of acute respiratory distress syndrome complications after lung resection* 2025 case reports：https://pmc.ncbi.nlm.nih.gov/articles/PMC12696315/ （須查全文和圖，不把術後 pulmonary edema 全推為 transfusion-induced）。

## 4. 首次成稿品質試驗：先評初稿，再談改稿

**目的**：是否能在不依賴使用者逐次發現缺口的情況下，自發寫出可以交付的臨床教材。

1. **凍結任務與來源**：第一篇選定後記錄初始 brief、可取得來源清單與模型／工具條件；原稿與既有文章只作已公開先備，不能先看使用者新一輪逐段糾錯。來源無法取回者標未核實，不能捏造。
2. **建立 first-draft snapshot**：第一份完整文章連同來源紀錄及第一版圖放入私有草稿，記 commit SHA；在它被審查前不覆寫。不能以修改後達到 90 分追認初稿也達標。
3. **分離審稿**：用 EPQC A–G 七軸、病例與醫學 source audit、Figure Gate、作者先備缺口、實際手機圖閱讀驗收。AI 同輪自評只作內部查錯，不能當獨立 reviewer。必要外部醫師審查另標。
4. **硬性失敗**：P0/P1 錯誤；虛構患者檢驗數值；用病例相關性宣稱因果通則；誤抄 Figure/Table/footnote；缺少理解主線必要的術語和中介；將處置建議脫離氣道／循環／腎臟安全前提；公開侵權或患者隱私。P0/P1 不能被總分補償。
5. **首次成稿品質分數 100**：核心命題與敘事取捨 20；前提與因果中介 20；床邊安全與反事實改判 20；病例／文獻 fidelity 15；原圖／原創圖的功能與手機可讀性 10；語言與認知成本 10；跨篇最小必要連結與 provenance 5。
6. **暫定門檻**：初稿 90/100 以上、EPQC A–G 均至少 3/4、無未解 P0/P1、重要原圖真實讀回、病例數值可追溯、核心手機版可讀；低於門檻可修稿但初稿結果仍記失敗。一次成功僅是 artifact，不是穩定能力的證明。
7. **後續重測**：在 01／03／05 三種差異夠大的 SICU 任務中，分別記「初稿達標率、人工指出的高階/基礎遺漏、介入次數及分鐘、修後有無新錯」。三篇成功僅屬小型 pilot，不能聲稱較 Native GPT 高品質，後續再做固定來源對照。

**本分支驗收**：已重排 cardiothoracic 系列、取得並目視 CABG 來源 Table 1 和 Figure 1，另將 V1 初稿永久保存於同一 private branch；仍未完成獨立醫學審查、所有 Pocket 原圖重核、正式 Figure Gate、網站手機實機審視、學習效果驗證及正式發布。未來由原系統出版流程決定是否發行，無第二個目錄或新網站。


## 5. IBCC research layer — added at user's request (2026-10-26)

The primary care setting is **postoperative cardiac and thoracic surgery**. The user does **not yet know** whether their future ICU routinely uses pulmonary artery catheter, SvO₂, cardiac index or only arterial line / central line / bedside echo. Educational entrypoint must therefore be device-agnostic: symptoms + A-line blood pressure/waveform, rhythm, drain output, urine output, skin perfusion, ABG/chemistry, bedside imaging; explain PAC/ScvO₂/SvO₂/CI/PAWP only when they change a specific decision. Never represent advanced monitoring as a universal prerequisite.

### Source-role contract

**IBCC = high-value expert-written clinical physiology + bedside reasoning resource, not guideline/primary evidence.** Use IBCC to identify the causal model, common postoperative pitfalls, response-to-intervention framework, and which variable is missing. Verify precise clinical claims, threshold values and intervention choices against current specialty guidance, primary studies, and source case reports. Cite primary sources for trial effects or case facts. Preserve uncertainty and surgical-specific caveats. Do not reproduce IBCC figure assets or substantial prose on the public site without license/permissions; use links and original causally useful figures.

2026-10-26 live IBCC navigation checked; relevant pages and published page dates:

1. **Postoperative cardiac surgical patients** (Josh Farkas, 2025-01-05): https://emcrit.org/ibcc/cts/ — directly relevant to cardiac post-op approach, low-output vs hemorrhage vs obstructive causes (tamponade, excessive airway pressure), post-CPB vasoplegia, pacing, A-line/ABG, lactate, SvO₂. **Article suggests approximate hemodynamic targets (e.g. CI ~2.2)**: they are *rough targets* and cannot diagnose safety or trigger treatments in isolation.
2. **Diagnosis of metabolic acid-base disorders & AGMA (including lactic acidosis)** (2024-06-29): https://emcrit.org/ibcc/agma/ — compare lactate interpretation, ΔAG, low bicarbonate, parallel respiratory assessment and 2026 source case. **IBCC purposely uses an uncorrected AG workflow**. The existing Clinical OS `acid-base-sources.md` documents other endorsed approaches with albumin-corrected AG. Expose the conflict and when hypoalbuminemia makes AG interpretation unsafe; **do not silently treat uncorrected AG as a universal screening rule**.
3. **Shock & vasoactive medications**: https://emcrit.org/ibcc/shock/ — integrate perfusion phenotype, echocardiography, clinical signs and vasopressors with lactate and blood gas, especially where PAC data are unavailable. General shock framework needs surgery-specific differential.
4. **Right Ventricular failure** (2025-03-21): https://emcrit.org/ibcc/rv/ — explain effects of oxygenation, hypercapnia, PEEP, intrathoracic pressure, CVP/congestion on RV and systemic perfusion, particularly CABG/valve/aortic patients; RV-specific advice cannot be generalized to all cardiothoracic cases.
5. **ARDS**: https://emcrit.org/ibcc/ards/ — refractory hypoxemia, driving pressures/ventilation and RV strain as relevant to lung-resection postoperative injury; guideline ARDS criteria must be verified separately and **post-lung-resection low P/F alone is not automatically ARDS**.
6. **IBCC Table of Contents** (2026-03-07): https://emcrit.org/ibcc/toc/ — route to chapters on ECMO, right heart catheterization, nonanion-gap metabolic acidosis, metabolic alkalosis, respiratory acidosis; follow the precise chapter links when authoring actual lessons.

### Per-article source targeting

| CTICU draft | IBCC primary discussion | Independent verification |
| --- | --- | --- |
| 01 CABG lactate/ScvO₂ | cts + agma + shock | 2025 actual CABG series Table 1, CPB 2024 EACTS/EACTAIC/EBCP guideline, lactate physiology research; differentiate *measurement* vs *clinical conclusion* |
| 02 Hb/DO₂/CO | cts + shock | CaO₂/DO₂ physical units and source measurement timing; evidence-based transfusion threshold (do not adopt IBCC rough Hb suggestion) |
| 03 CPB acid–base | agma + cts | Pocket 9E p158–162; EACTS CPB acid–base and solution type; track albumin/chloride |
| 04 alpha-stat vs pH-stat | cts as postoperative context only | Actual CPB guideline/temperature correction primary source; **IBCC is not sufficient** to teach alpha-stat/pH-stat |
| 05 postoperative hypoxemia after resection | ards + rv | Reconstruct original post-resection case / radiology and ARDS diagnostic definition, isolate edema/atelectasis/aspiration |
| 06 one-lung ventilation | rv + ards as mechanisms only | Thoracic anesthesia/one-lung ventilation specialty references; do not force IBCC to serve as a one-lung-ventilation guideline |
| 07 post-extubation hypercapnia | agma (only mixed acid–base check) + rv where relevant | Existing hypercapnia/NIV/COPD articles; anesthesia/reintubation evidence |
| 08 ventilator pH vs cardiac load | rv + ards + cts | Relevant CPB/postop and lung-protective mechanical ventilation guidelines |
| 09 normal ABG, still ICU | cts + shock | Surgical complication risk, echocardiography, bleeding/tamponade assessment |

### First-draft quality integration

- For each candidate IBCC mechanism, create an **evidence check with exact claim, IBCC section URL, original patient observation or primary guideline/study, measured vs inferred, context where false**. This is a private reviewer work product, not added UI infrastructure.
- Before first V1 freeze, source coverage should be sufficient to compose the entire clinical narrative. It must NOT require the user to remind the writer to explain basics (e.g., PAC/ScvO₂, lactate vs BE, FiO₂, V/Q, PEEP). Conversely, avoid dumping the entire IBCC chapter's checklist into one article.
- **The CABG initial V1 is already immutable** (`b9f5ee1c9ab0719da4f657d7990c1a199c28cf92`). The IBCC research layer is a **post-freeze source addition**; do not retroactively mark that draft as if it had been produced with these sources. Later V2 should state which fixes derive from IBCC, original paper or independent reviewer.
- Separate clinician-independent clinical QA / artifact score / reader comprehension. IBCC consultation does not satisfy any of these gates by itself.
