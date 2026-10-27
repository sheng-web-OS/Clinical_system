# U01｜第一劑醫囑演練：選藥與真正完成下單之間，差了什麼？

2026-10-28｜v0.2｜**EDUCATIONAL / NOT ORDER-READY**。本個案為合成病例；病人體重、實際過敏反應、當院 susceptibility / formulary、動態 CrCl 與藥品輸注規範未核。任何 mg、interval、infusion rate 均需即時由上級/藥師確認，**本稿不是可貼到 EMR 的處方**。

## A. 第一步：先確認這個病人有沒有必要立刻給 IV 抗菌藥

68 歲男性，發燒、低血壓、意識變慢、AKI、lactate 3.8，右 hydronephrosis、CVA tenderness，兩個月前尿培 ESBL *E. coli*。要當作 **probable severe systemic UTI / possible bacteremia and infected obstruction** 危急處理；同步上級求援、血/尿培（理想在給藥前而不延誤）、復甦、urgent urology。並非只因 pyuria 或舊 ESBL 就給藥。不要根據單一 BP、lactate 宣稱已滿足 septic shock 定義。

## B. 第二步：用四層證據選候選 first agent

| 層次 | 本例證據 | 如何改變初始處置 |
| --- | --- | --- |
| 危重程度 | 血壓/意識/尿量與 AKI 警訊 | 優先可靠 active empiric IV 而非等待 AST |
| Resistance prior | 2 個月前 ESBL E. coli | 常規 ceftriaxone 不宜被當作可靠預設 |
| 病人禁忌與藥動 | penicillin allergy 不明、AKI on CKD | 立即查真實反應、體重、腎功能動態與藥品給藥策略 |
| 在地資料 | 當院 antibiogram 與 restricted agent 未核 | 不可將全臺監測率代替病房族群的本院資料 |

**此例初始優先討論 meropenem IV**，並依 ID/藥師、已知舊 AST 和院內規則確認是否可實施。此例未確認對本次病原必有活性，且本次 AST 尚未回來。

### 競爭藥物辨識

- **Ceftriaxone**：一般 cUTI 常用，但此例近期 ESBL 將 inactive risk 抬高；不可因「尿路感染」四字直接用。
- **Piperacillin–tazobactam**：2026 IDSA AMR §1.4 容許其作**非危重、無 concomitant bacteremia 的 ESBL-E cUTI** alternative，**不建議**用在 ESBL-E cUTI 危重或伴菌血症者。初始尚未知菌血症但高度疑慮，這是偏向 carbapenem 的重要理由；也不代表對所有一般 cUTI 禁用。
- **Ertapenem**：非危重、適合情境可用，但缺乏 Pseudomonas 覆蓋；2026 AMR 對危重／hypoalbuminemia 的侵襲性 ESBL 情境偏向 meropenem/imipenem，勿等價替換。
- **Cefepime 單方**：不要把它與 cefepime–enmetazobactam 視為同藥；2026 AMR 建議避免 cefepime 單方治療 ESBL cUTI，即使 susceptibility 測為 S。
- **TMP-SMX / ciprofloxacin / levofloxacin**：若已知本次 susceptible，可作 definitive cUTI 甚至適條件的 PO；不能拿預想藥敏替代此例第一劑的必要覆蓋。
- **Aminoglycoside**：可以是部分 ESBL cUTI alternative，但本例 AKI/CKD 使腎毒性、給藥暴露和監測代價格外重要，不應無條件加一支。

原始依據：[IDSA cUTI 2025 §Selection，Fig 1.1](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections)、[IDSA AMR 2026 §ESBL Q1.2–1.6](https://www.idsociety.org/practice-guideline/amr-guidance/)。

## C. 第三步：與上級／藥師共同完成的安全處方欄位

| 欄位 | 模擬填寫與待確認狀態 |
| --- | --- |
| Patient & indication | 68M; suspected invasive cUTI ± bacteremia ± infected obstruction |
| Cultures | 兩套血培及尿培，實際採檢 timestamp: PENDING |
| Prior organism / AST | 2 months ago ESBL E. coli；**原完整 AST PENDING** |
| Candidate generic / route | meropenem / IV **under immediate local verification** |
| Actual first-dose time | 調劑/執行時間 PENDING，需記錄給入時間 |
| **Actual dose / infusion / interval** | **NOT_VERIFIED – 不得直接複製到 EMR** |
| **First loading vs maintenance** | 分開評估，依實際藥品、renal trend、本院 infusion SOP |
| Current renal info | Cr 2.0 vs 1.3 mg/dL 兩週前；尿量、CrCl method、RRT status PENDING |
| Actual weight | PENDING；不可用未知 eGFR 補成虛構 CrCl |
| β-lactam allergy | 反應型態/時間/是否耐受 carbapenems PENDING |
| Interactions and toxicity | 藥物清單、神經毒性與 K/Cr 風險 PENDING |
| Prescriber, pharmacist, restricted approval | 姓名/時間/核准狀態 PENDING |
| Resuscitation & source control | BP/MAP、尿量、urology call、影像/引流時程 PENDING |
| Review trigger | 病人惡化當下重評；新培養/AST 回報；定時抗生素 time-out |

**關鍵 PK/PD**：β-lactam 重視 fT>MIC。2026 SSC 建議 sepsis/shock 於 initial loading 後採 prolonged-infusion maintenance；但並不提供本個案體重/AKI/院內流程所需的可複製數值。首劑不足暴露與後續腎功能惡化下累積毒性可以同時需要防範，必須動態複核。([SSC 2026：Beta-lactam antibiotics](https://sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026))

## D. T48：有 S 仍不一定能馬上 PO

合成 blood/urine 均 ESBL E. coli；ceftriaxone-R, meropenem-S, TMP-SMX-S。

- **仍需升壓劑、未解除阻塞**：不因 TMP-SMX-S 立刻改 PO，先完成源控制、灌流支持與有效 IV 治療。
- **已引流且穩定、能可靠吸收**：核對 source、AST、血中與組織濃度、K/renal/interaction，以及院內用藥後，可考慮 TMP-SMX 等具活性的 oral agent。**菌血症並非永久禁止轉口服；不穩定及未 source control 才是此時的主要阻擋。**
- **療程**：從第一個 effective treatment day 算；一般有反應 cUTI 可參考 FQ 5–7 天或非 FQ 7 天，但本例 CKD/阻塞/男性攝護腺炎風險與重症使外推有條件，不能自動設定 7 天或 14 天。([IDSA cUTI 2025：IV-to-oral, Duration & exclusions](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections))

## E. 本地化 release gate

尚無 Sanford Guide 付費全文、當次院所 antibiogram／formulary／限制用藥、仿單／本院腎劑量輸注對照以及獨立處方醫學 QA。此頁即使作為教學文稿公開，也永遠不得標註為「本院首劑標準醫囑」；order-ready 必須另行本地驗證。