# 半夜疑似泌尿道敗血症，舊培養有 ESBL：從真實病例理解第一劑

這篇改用**已發表的真實病例、原始藥敏及現行指南**追問：醫師在不同時間點知道什麼、憑什麼改變治療、還不能宣稱什麼。它不再以 AI 自行設計的夜班病人、體重、腎功能、過敏與「第一劑醫囑表」作為主要依據。**本文不是可以複製到 EMR 的醫囑或特定醫院處方建議。**

先區分：**病例觀察**有作者、原始病程和可追溯數值，但單例不能證明因果；**指南建議**適用於特定族群，需核對條件；**「若夜班遇到舊 ESBL」**是問題設定，並非把兩個不同病人的紀錄拼在一起。任何原文沒報告的過敏、體重、舊 AST、腎功能時序和院內 antibiogram，都明確保留未知，不讓 AI 補寫。

## 真實病例一｜開始使用的抗生素，為何第三天才發現可能無效？

2021 年《Antibiotics》報告一名 **28 歲女性**，沒有已知近期抗菌藥使用或醫療照護暴露，因發燒、左側腰痛和泌尿症狀就診。初次評估 HR **117/min**、BP **83/44 mmHg**；初始給予 ceftriaxone，病況不穩而進入 ICU。**住院第 3 天**尿培養與 AST 確認 ESBL、廣泛抗藥性的 *E. coli*，才將 ceftriaxone 改為 meropenem。作者報告**第 4 天**退燒且生命徵象改善，第 5 天出院後以靜脈治療銜接 ertapenem，總計約 10 天 carbapenem；追蹤未見復發。[原始病例與 susceptibility Table 1](https://www.mdpi.com/2079-6382/10/5/533)。

<box></box>

同一份**真正原始尿培養**可對照這幾個 MIC（依論文 Table 1 記錄的單位和判讀）：ceftriaxone **>64（R）**、meropenem **<0.25（S）**、TMP-SMX **>320（R）**、piperacillin/tazobactam **64（I）**。這不是「ESBL 通常如何」的 AI 推測；是當次分離株實測。拿到新 AST 後能確認當時 ceftriaxone 與病原不匹配，但**不能單憑換藥後改善，推算所有改善都由 meropenem 導致**：病程、復甦、器官支持同樣可能影響結果，且沒有對照組。

最容易被錯誤移植的兩點：**原報告並無「兩個月前尿培 ESBL」的前提**，因此不能把它說成「依舊培養選第一劑」的直接實證；作者用了 10 天療程，也不能變成所有 ESBL cUTI 的通用療程。病例應教會讀者的是**病原—藥物失配如何由後來的培養揭露**。

## 第一問｜舊培養 ESBL 究竟把「第一劑的推理」改變了哪一層？

現在才切換到題目的**反事實情境**：若另一名危重病人在初次治療前就有近期相關尿培養 ESBL *E. coli* 的紀錄，這項歷史證據會增加某些經驗性 cephalosporins 無法涵蓋本次病原的可能；但**不代表本次已證實是同一株菌，更不代表已知道本次 AST**。

[IDSA 2025 cUTI 的原 Figure 1.1](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-1-figure-1.1.pdf) 應該從四個層次讀：**感染與器官嚴重度 → 既往抗藥菌／抗菌藥暴露 → 病人限制（例如過敏、腎功能）→ 相似病人族群的當院 antibiogram**。閱讀原 [Table 1.1](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-1-table-1.1.pdf) 也要看候選類別與註腳，不能直接從表格抄成某病人的處方。

| 此刻的資訊 | 真正支持的推論 | 不能超前的結論 |
|---|---|---|
| 高度懷疑感染且循環／器官功能惡化 | 延誤有效抗菌治療的風險可能升高，需立即進入急重症團隊評估 | 一個 BP、MAP 或 lactate 不能單獨完成 septic shock 定義 |
| 近期尿培曾有 ESBL | 提高對 resistant Enterobacterales 的先驗疑慮 | 不等於當次菌種、MIC、是否菌血症已確認 |
| 當次 AST 回報 | 在菌種具有致病意義時，支持確定性方案與降階評估 | 不能把第 3 天才知道的答案搬回第 0 天 |
| 體重、過敏型態、CrCl、當院限制用藥未知 | 這些是需要真實照護團隊核實的資訊缺口 | 不得由 AI 臆造第一劑 mg、interval、輸注方式 |

**ESBL 的意義首先是機轉，並非完整處方。** β-lactam 需結合 PBP 干擾細胞壁；典型 ESBL 可水解 cefotaxime、ceftriaxone 等延伸型 cephalosporins 及 aztreonam，但不能據此斷言所有 carbapenem 必為 S，因為菌株仍可能同時存在其他抗藥機轉。TMP-SMX、fluoroquinolones 不受這個酵素直接水解，卻仍可能因其他機轉抗藥。故**舊 ESBL 降低某些經驗性方案的可信度，新 AST 才能進一步確認當次分離株**。

[IDSA 2026 AMR 的 ESBL 指引](https://www.idsociety.org/practice-guideline/amr-guidance/) 對**已確認且有 susceptibility 的 ESBL-E cUTI**，在條件吻合時將 TMP-SMX、ciprofloxacin、levofloxacin 列作 preferred options；對危重或可能菌血症、藥敏未明的病人，應另外考慮可靠的 IV ESBL-active coverage，meropenem 等 carbapenem 在適當條件下有其角色。但這些都是**有條件的群體層次建議**，不等於任何見到 ESBL 三個字就固定開同一藥。

Piperacillin/tazobactam 亦不能只憑「抗菌譜廣」或一次體外 S 和 carbapenem 畫上等號；IDSA 2026 特別區分非危重、無同時菌血症之 ESBL cUTI alternative 與不建議的危重／菌血症情況。這背後有體外 MIC 的限制、其他 β-lactamases 與血流感染比較性證據。既不應忽略風險，也不該推廣成「所有 ESBL 膀胱炎都必須 carbapenem」。

## 第二問｜另一個真實病例：抗菌藥以外，還有哪個病灶沒有被解決？

Arai 等人在 2021 年 *Oxford Medical Case Reports* 發表的是**另一名 81 歲日本女性**，既往有反覆 UTI。就醫時 BP **68/36 mmHg**、creatinine **2.7 mg/dL**、lactate **3.3 mmol/L**，左側 CVA tenderness；CT 發現左輸尿管腎盂交界處阻塞性病變。原作者啟動抗菌藥與血流動力支持，因持續嚴重低血壓而延後經皮腎造瘻；在進一步循環支持後完成**percutaneous nephrostomy（PCN）**與引流。**第 4 天**血、尿培養報告 ESBL *E. coli*。病人後續改善，日後病理確認泌尿上皮癌。[原始病例及 CT/引流 Figure 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC8633641/)。

這是一個教學上真正重要的**資訊轉折**：即使先選了合理的抗菌藥，也不能讓被阻塞的集尿系統自動排空。阻塞的解剖原因、是否有感染性腎積水／膿瘍、引流是否可行，與「這個菌對藥是否 S」是不同問題。

這篇病例曾使用 polymyxin B hemoperfusion 及 hydrocortisone。**那是該院在特定嚴重休克下採用的救援治療，不是證明 PMX-DHP 有標準存活效益的臨床試驗，亦非本教材鼓勵模仿的做法。** 原文的阻塞病因是腫瘤相關病變，不能偷換成「病人一定有阻塞性結石」。

[EAU 尿路結石指引](https://uroweb.org/guidelines/urolithiasis/chapter/guidelines) 對合併 sepsis 的**阻塞結石**強調緊急減壓、再處理結石；[SSC 2026](https://sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026) 強調辨識需 source control 的感染灶並迅速處理。兩份指南提供比個別成功病例更可靠的處理方向，但也不能變成 AI 在不了解病人影像與手術風險時直接指定支架或 PCN 的醫囑。

## 第三問｜病例不能替我們下哪些結論？

**不能把相關性當因果。** 第一例換藥後退燒，不證明改善完全由 meropenem 造成；第二例引流後改善，也不能把所有病程變化完全歸給引流或某項救援輔助治療。Case report 用來辨識真實問題與推理節點，不能取代隨機試驗和指引。

**不能把個案療程變成通則。** 第一例約 10 天 carbapenem 是作者的實際治療經過；[IDSA 2025 cUTI 原 Figure 1.2](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-2-figure-1.2.pdf) 討論臨床改善時的 IV-to-oral 邊界，[Figure 1.3](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-3-figure-1.3..pdf) 與正文則針對合適病人提供較短療程的條件性建議。重症、未引流阻塞、膿瘍、腎功能限制或疑似急性攝護腺炎，都需逐一檢查適用性。

**不能從兩筆 Cr 自動宣告 AKI stage。** [KDIGO 2012](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf) 需核對 48 小時／7 天血清 creatinine 或連續尿量資料；第二例的單次 Cr 2.7 不足以供我們虛構完整基線與腎功能時間線。也不能用單次血壓或 lactate 代替 Sepsis-3 的完整休克定義。

**不能把陽性尿培當作一定需要治療。** [IDSA 2019 ASB](https://www.idsociety.org/practice-guideline/asymptomatic-bacteriuria/) 指出：沒有可歸因感染症狀的菌尿，即使 ESBL，也不能單憑檢驗結果推動 carbapenem；懷孕與特定侵入性泌尿手術是不同情況。

## 真正的二階國考對題｜111 年第二次・醫學（三）第 60 題

[考選部原題、答案與更正清冊](../urosepsis-esbl-first-dose-sources.md)：典型 ESBL 能水解 cefotaxime（①）和 aztreonam（②），但不以直接水解 ertapenem（③）為其典型機轉；官方標準答案 **A（①②）**，該題未更正。**這只回答酵素可水解什麼，不保證臨床分離株一定 ertapenem-S**；也不能從國考答案推出敗血症首劑處方。

## 帶走一條連續的閱讀路徑

第一個病例把**當次藥敏出現前後**分清楚；第二個病例揭示**用藥與感染源控制不是二選一**。接著才用 IDSA、SSC、EAU、KDIGO 把兩例無法解決的普遍性問題放回其研究適用族群。真正要練習的是：**這句判斷來自哪篇原文、是哪個時間點取得的資料、哪一項仍然未知，以及什麼反證會推翻它**。

兩例來源、可核對的數據、未報告的欄位、證據層級與臨床限制，請閱讀[原始資料與證據界線](../urosepsis-esbl-first-dose-sources.md)。本教材不提供 EMR 可直接抄寫的 mg、間隔或輸注條件；真實急重症病人仍需當下醫療團隊依實際病情、抗藥資料及院內規範迅速處理。
