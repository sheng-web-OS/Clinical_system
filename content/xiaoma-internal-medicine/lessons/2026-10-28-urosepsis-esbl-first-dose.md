# 為何這樣選抗生素？從真實 ESBL 尿源性感染理解證據與決策

**閱讀定位｜醫學生深讀，不是藥囑指南。** 這篇文章的主要問題不再是「看到數字，當班 PGY 應該直接開什麼藥」，而是「我們從真實病人的病程、微生物學與臨床試驗，究竟可以知道什麼？」臨床藥囑需要上級醫師、藥師、當地 antibiogram/formulary/ASP 與當下病況共同驗證。本文不提供可直接複製的劑量、間隔或輸注處方；如遇真實危急病人，應立即依當院流程求援與處置，不因閱讀教材而延誤照護。

## 第一問｜真實病人發生了什麼？先看病程，而不是先選藥

一篇已發表的[尿源性敗血性休克病例報告（81 歲女性）](https://pmc.ncbi.nlm.nih.gov/articles/PMC8633641/)將「實驗室數據、循環惡化、解剖感染源」放在同一位真實患者的時序中。患者因發燒、食慾不振和無法活動就醫；初診 **BP 68/36 mmHg、HR 84/min（不規則）、RR 24/min**。原作者記錄 **WBC 27.1 ×10³/μL（neutrophils 93.8%）、Cr 2.7 mg/dL、lactate 3.3 mmol/L、CRP 26.7 mg/dL**；CT 發現左側 ureteropelvic junction（UPJ）阻塞及膿瘍。這些是**原文實測**，不是依「典型敗血症」自行配出的 labs；原文沒有提供這些值對應的完整個人基線，因此不能單憑 Cr 2.7 重新推算精確的 AKI 分期。

**處置的先後順序也是可核對的病例觀察。** 醫療團隊先使用輸液、norepinephrine 與 carbapenem，但持續嚴重低血壓，使原計畫的經皮腎造瘻（percutaneous nephrostomy）暫時無法進行；作者接著記載使用 polymyxin B hemoperfusion（PMX-DHP）及 hydrocortisone。約八小時後血壓改善，才完成腎造瘻引流阻塞的集尿系統。**第 4 天回報的血液與尿液培養均有 ESBL-producing *Escherichia coli***，團隊繼續原本的 carbapenem；作者描述約兩週後病情恢復，最終第 65 天接受左側腎輸尿管切除，病理顯示 urothelial carcinoma。以上來自[原始 Case report／CT Figure 1 圖說](https://academic.oup.com/omcr/article/2021/11-12/omab109/6439717)，但**「PMX-DHP、hydrocortisone 後血壓改善」只是先後發生的個案觀察**；同時存在輸液、升壓、抗菌治療與疾病演變，不能將改善歸因於兩種輔助療法或推廣為標準處置。

這裡先不要把病例整理成「遇到 ESBL 就開 carbapenem」的速查表。病程至少有三條不同但互相牽連的線：

- **感染線**：出現危急感染表現時，當次微生物鑑定及 AST 還沒有回來；初始治療依當下感染機率、嚴重度和既有抗藥資訊選擇，隨後再用實際培養重新評估。
- **解剖線**：被阻塞的集尿系統無法只靠抗菌藥恢復引流。這篇真實報告涉及腫瘤性阻塞及之後的 nephrostomy；它讓「抗菌治療」與「source control」的不同功能具體可見。
- **循環線**：作者也報告使用 polymyxin B hemoperfusion 與 hydrocortisone 等個別輔助治療。**這只是單一病例曾採取的措施，不能視為這些措施已被證明有效、也不能由此建議一般病人常規採用。** 其適應與療效要另查對照研究、現行 sepsis 指引及適用情境。

**這篇 case report 沒有證明：**任何同樣有 ESBL 尿培史的病人都會出現相同病原；腎造瘻與抗生素的個別療效百分比；本次病例的處置對其他患者必然最佳。病例報告是觀察材料，不是有對照組的因果試驗。原文未提供給教材的數據應標示 **NOT_REPORTED**，不能自行替病人補 Cr、lactate、MIC、劑量與完整病情細節。

### 第二份真實病例｜當培養結果讓初始抗生素的「有效性」被重新評估

[Evins 等人 2021 年發表的 28 歲女性病例](https://www.mdpi.com/2079-6382/10/5/533)有發燒、腰痛及 pyelonephritis，初期血壓 **83/44 mmHg**、心跳 **117/min**，需要住院及加護照護。原始病例記載初始使用 **ceftriaxone**，第 3 天尿培養與藥敏發現 ESBL-producing *E. coli*，此後調整為 **meropenem**；作者記載隔天退燒，後續以靜脈方案完成療程。

這篇特別值得讀，因為[原文 Table 1](https://www.mdpi.com/2079-6382/10/5/533)具有當次菌株而非 AI 猜測的 MIC/AST。以原文記錄的數值與判讀為例：

| 病例中的藥物 | 當次 urine isolate MIC（依原表） | 當次 AST |
| --- | ---: | --- |
| Ceftriaxone | >64 | R |
| Meropenem | <0.25 | S |
| Piperacillin–tazobactam | 64 | I |
| TMP-SMX | >320 | R |

當次藥敏支持「最初 ceftriaxone 與這株分離菌不匹配」，卻**不能**由後續好轉精確推算 meropenem 的獨立療效，因為患者同時經歷復甦與其他照護。更重要的是，**這位病人沒有已知『兩個月前 ESBL 尿培養』的背景**，不能把她冒充下方的合成 68 歲男性，也不能用她的 AST 預測另一位病人的菌株。這正好讓讀者看清楚：真實「後來知道當次 AST」與指引要求「在還不知道 AST 時如何評估風險」，其實是兩個證據問題。

## 第二問｜個別病例提供線索，什麼證據才支持普遍性的抗生素選擇？

先將「病例觀察」和「如何治療的一般建議」分開。2025 [IDSA cUTI guideline](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections)整理臨床研究，建議選擇經驗性治療時依序考量**疾病嚴重性、既往抗藥菌或抗菌藥暴露、病人限制、適用的當地 antibiogram**；特別提到近期尿培有 ESBL 時，不能機械把 ceftriaxone 當作可靠的經驗性選擇。這是有條件的治療建議，不等於歷史菌株必然就是當次致病菌。

2026 [IDSA AMR guidance](https://www.idsociety.org/practice-guideline/amr-guidance/)則處理已知 ESBL-E 的病原學與治療選項：當次藥敏證實 susceptible，TMP-SMX 或 fluoroquinolones 可以具有治療 cUTI 的角色；當抗藥、禁忌、不耐受或感染狀態限制其使用時，carbapenem 等選項的地位才需要按條件比較。**尚無 AST 的 empiric 決策，與已知 AST 的 definitive 決策，不是同一個問題。**

ESBL 是能水解部分延伸型 β-lactam 的酵素機轉；菌株往往還可帶有其他抗藥機轉。藥物是否適合，至少還取決於感染部位、藥物可達到的暴露、當次 MIC/AST、器官功能與疾病嚴重性。不要用「ESBL 陽性」取代整份微生物報告。

為什麼要研究**療效的比較證據**，而不是相信病例中某個藥物使用後患者改善？因為單一病例的改善，同時受到抗生素、解除阻塞、循環支持、疾病自然病程及其他介入影響，無法分辨每一項的因果貢獻。像 MERINO 隨機試驗所研究的 ESBL相關菌血症抗菌藥比較，才直接涉及治療效果的對照；但其菌血症母群與適用限制，也不能不加區分地外推到所有非菌血症、低風險 UTI。以下保留原稿較深入的 ESBL 作用機轉、研究差異與指引適用條件，作為本節的延伸。

| 層次 | 真正回答什麼 | 這篇教材禁止的跳躍 |
| --- | --- | --- |
| Case report | 特定病人實際檢查、培養、介入與演化 | 單一個案中藥後改善 ≠ 該藥優於替代方案 |
| Microbiology / AST | 這個菌株呈現哪些抗藥與感受性資訊 | 舊 ESBL ≠ 本次同一菌、同一 AST |
| Trial / guideline | 在特定族群與條件下，哪些選項有比較證據 | 菌血症研究 ≠ 所有輕症膀胱炎；海外指引 ≠ 本院醫囑 |
| Local clinical review | 在此院此病人的風險、劑量、過敏、腎動態、庫存與限制 | AI 設計的完整醫囑 ≠ 經醫師/藥師核准的處方 |

## 第三問｜即使病例與指南都讀對了，還不能推論什麼？

**不能**用病例報告選出「最佳第一劑」、用舊培養替代新藥敏、用單次腎功能數值給出完整輸注處方，或把任何病人對某藥的好轉全歸因於那支抗生素。相同的 ESBL 名稱，在「沒有 sepsis 的 cUTI」「有菌血症的全身性感染」「合併感染性阻塞、循環不穩」等背景下，錯誤涵蓋的代價與治療選項不同。讀者現階段的合格成果，是**辨認證據來自哪裡、支持到哪裡、還要向上級或藥師核實什麼**；不是能否獨立開出一張藥單。

---

## 從酵素到真實藥敏：ESBL 不是一張可直接開立的處方

β-lactam 抗生素要與細菌的 penicillin-binding proteins（PBP）結合，抑制細胞壁交聯；某些革蘭陰性菌的 β-lactamase 則可在藥物抵達靶點之前水解 β-lactam ring。**ESBL 是一類抗藥機轉，不是病人的疾病嚴重度分數，也不是完整的感受性報告。** 典型 ESBL 可水解 cefotaxime／ceftriaxone 等延伸型 cephalosporins 與 aztreonam，但 ESBL 酵素本身通常不水解 carbapenem。臨床分離株仍可能因其他 β-lactamase、porin 或其他機轉而對 carbapenem 不敏感。[IDSA 2026 AMR Section 1](https://www.idsociety.org/practice-guideline/amr-guidance/)。

這也解釋為何第二位真實患者的分離株可以**同時**是 ceftriaxone-R、meropenem-S、TMP-SMX-R：ESBL 酵素不能直接破壞 TMP-SMX 或 fluoroquinolone，卻不排除菌株攜帶其他抗藥基因。由菌名和「ESBL positive」推估其他藥的 S/R，是把微生物機轉誤當成完整 AST。**MIC 是在特定試驗方法及 breakpoint 下對「這一株分離菌」的測量，不是另一個病人未來的預測數字**。就算菌株相同，感染部位、藥物暴露、病況及 source control 仍會影響實際療效。

### 為什麼不能拿一位病人的改善當作治療優劣證明？

28 歲女性原作者於住院第 3 天根據 urine isolate AST 將 ceftriaxone 改為 meropenem，後續退燒；第 5 天出院後改為居家 IV ertapenem，總計 10 天 carbapenem 治療，後續追蹤無復發。這是**同一個病例**確實被報告的時間序列，不是適用所有 cUTI 的標準 10 天療程，也無法分離先前補液、自然病程和換藥各自的因果貢獻。[Evins 2021 原始病例與 Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC8147929/)。

要比較抗菌藥效益，應轉向真正有對照組的試驗。例如 [MERINO 隨機試驗（JAMA 2018）](https://pmc.ncbi.nlm.nih.gov/articles/PMC6143100/)研究的是 **ceftriaxone-resistant *E. coli*／*Klebsiella pneumoniae* 菌血症的 definitive therapy**，而不是一般門診膀胱炎，也不是每個 septic 病人的未知菌種首劑。主要分析中，30 天死亡率為 piperacillin–tazobactam **23/187（12.3%）**、meropenem **7/191（3.7%）**，風險差 **8.6 個百分點**，未達預設的非劣性判定。這是試驗的結果，不代表所有 ESBL cUTI 都需要 carbapenem；而且研究以 ceftriaxone resistance 選入，不能聲稱每株都已由基因檢測確認 ESBL。

原試驗後續以 reference broth microdilution 重驗部分分離株，差距縮小；**事後次群分析並未推翻主要試驗的限制，亦不能單憑不顯著就宣稱兩藥等效**。IDSA 2026 AMR 因而區分：已知 susceptible 的 ESBL-E cUTI、侵襲性或合併菌血症感染，和危重但尚未知 AST 的 empiric 情境，並不適用同一條處方捷徑。[IDSA 2026 §1.2–1.4](https://www.idsociety.org/practice-guideline/amr-guidance/)。

### 選藥前至少要分清三個不同的資訊狀態

| 時間／證據狀態 | 實際已知 | 不應偷渡的結論 |
|---|---|---|
| **Empiric／尚無當次 AST** | 感染症候群、重症程度、近期舊培養、藥物暴露與在地抗藥風險 | 舊 ESBL 培養 ≠ 本次同一菌、同一 MIC；不能將個案中的後來藥敏倒灌回初次就醫 |
| **Definitive／當次菌株已鑑定** | 分離株的 MIC／S-I-R、感染部位和病人病程 | 一個 S ≠ 對所有部位、器官功能及治療時點都能使用，也不直接等於適合改口服 |
| **追蹤／治療後的病程** | 有無退燒、循環改善、感染源是否已引流及其他器官變化 | 退燒 ≠ 某藥單獨造成改善；未解除感染性阻塞時，不可只從新 AST 假定已完成 source control |

依 [IDSA 2025 cUTI](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections)，經驗性治療的四個考量是嚴重度、既往抗藥菌或抗菌藥暴露、個人禁忌與交互作用，以及有 sepsis 時適用的**當院、近期、相近人群** antibiogram。這些是有條件的建議，**不是允許把美國指南或本站教材當成臺灣院內可直接複製的第一劑醫囑**。

### 回到原始指引圖表：這不是四張醫囑表

想追查「哪個證據出現後才足以改變討論」，請由出版者的原圖閱讀而不是只抄結論：[IDSA 2025 cUTI **Figure 1.1**：經驗性選藥四步流程](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-1-figure-1.1.pdf)；[**Table 1.1**：尚未套用個人條件前的候選藥物類別](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-1-table-1.1.pdf)。兩者分工不同：表格列出**可能的選項**，流程則要求先核對嚴重程度、舊菌株及患者限制；缺少本院 antibiogram 就不能把模型中 90%／80% 的參考值寫成院內真實敏感率。

另外，[**Figure 1.2**：臨床改善與未改善時，是否可討論 IV-to-oral](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-2-figure-1.2.pdf)，以及 [**Figure 1.3**：療程與臨床反應的條件分支](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-3-figure-1.3..pdf)，處理的是**之後已有新資訊的另一個時點**。它們不能回頭證明初始 ceftriaxone 在 28F 病例有效，更不代表感染性阻塞尚未解除、休克未穩定者都可以直接改口服或套固定短療程。以上只提供原圖入口與適用界線，不翻印原圖，也不宣稱已完成本輪圖表註腳的獨立核驗。

### 反事實練習｜辨認證據缺口，不模擬簽核醫囑

**以下病例為人工合成，並非發表病例；只測試辨認資訊不足的能力。** 想像一名 68 歲男性有 CKD、既往 ESBL 尿培養、發燒與疑似阻塞，BP 92/56（粗估 **MAP 約 68 mmHg**），兩週前 Cr 1.3、現在 2.0 mg/dL。這兩筆 Cr **尚不足以單憑兩筆數值確認 KDIGO AKI** 的時間窗；既往尿培亦不等於本次 AST。真正臨床上若病人不穩，不能因等待教育題目的完整定義而延遲求援、急症評估及源控制。此練習不提出 meropenem 或其他藥的可執行處方，也不要求讀者判斷劑量；需要額外資訊的是既往 AST、當次培養、過敏反應、腎功能動態、解剖影像與當院處方規範。

請回答：① 哪些資訊是「已實測／已觀察」，哪些只是「疑似」？② 如有新培養、血流動力及引流資料，哪些原先推論可能被推翻？③ 為何「先前培養 ESBL」及「病例後來使用 meropenem 改善」都不足以單獨證成另一個病人的第一劑？


## 真正的二階國考對題｜111 年第二次・醫學（三）第 60 題

**考點不是「有 ESBL 就開哪一支」；而是用機轉劃出抗菌藥**不能**與**仍可能**有效的邊界。**

> 考選部 111 年第二次醫師第二階段考試，醫學（三）第 60 題（代號 1302）：ESBL 能水解哪些 β-lactam 抗生素，導致它們失效？選項是 ① cefotaxime、② aztreonam、③ ertapenem；A 僅①②、B 僅①③、C 僅②③、D ①②③。**官方標準答案 A**，核對原始更正清冊後，本題**沒有更正**。

**逐選項解析：** ① **Cefotaxime 正確**——它是第三代 cephalosporin，屬典型 ESBL 可水解的延伸型 β-lactam，和本例為何不直接以 ceftriaxone 當可靠經驗性第一劑相連。② **Aztreonam 正確**——雖屬 monobactam，但「單環」不代表可逃過 ESBL 水解；不能把對某些其他 β-lactamases 的穩定性外推至 ESBL。③ **Ertapenem 錯誤**——它是 carbapenem，**典型 ESBL 酵素本身**通常不能有效水解 carbapenem；不過若同時具其他抗藥機轉，真實分離株仍可能對 ertapenem 不敏感，所以「③ 錯」不是臨床上保證 ertapenem-S。

**選項辨識：** A（①②）正確；B（①③）錯在把 carbapenem 納入典型 ESBL 水解譜、卻漏掉 aztreonam；C（②③）錯在漏掉 cefotaxime、且多選 ertapenem；D（①②③）錯在把 ESBL 與 carbapenemase 混為一談。

這題再向臨床推一步：**正確知道「ESBL 不直接水解 ertapenem」，仍不足以在本案例選 ertapenem 當第一劑。** 本例不穩定、疑似菌血症、未知 Pseudomonas 風險與 albumin/藥動狀態，和酵素能不能水解是**不同層級的問題**；這就是國考辨識題到 PGY 用藥決策之間的中介。

考選部原始來源：[111-2 醫學（三）正式試題 PDF（第 60 題，紙本第 13 頁／PDF index 12–13）](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=111080&q=1&s=11&t=Q)｜[標準答案](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=111080&q=1&s=11&t=S)｜[答案更正清冊](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=111080&q=1&s=11&t=M)。已實際目視原 PDF 的題幹與答案行，不依賴有亂碼的機器匯入題庫。

## 學習回收｜三問是推理，不是處方核對表

1. **病人與病原**：81 歲阻塞病例和 28 歲無已知抗藥風險的病例，哪個觀察資料能證明本次有 ESBL？兩者能否互換 AST？
2. **臨床證據**：在 MERINO 中，分母、主要終點、非劣性假說與適用病人是什麼？為何不能由單一病例的退燒推出 meropenem 獨立療效？
3. **過度推論**：何時需要處理感染性阻塞？為何 ESBL ≠ 全部抗生素 R、S ≠ 適合所有感染部位、指南 ≠ 臺灣醫院處方核准？

本文引用的原始病例、指南、臨床試驗與官方考題整理於 [證據來源與適用界線](../urosepsis-esbl-first-dose-sources.md)。完整原始值班情境留在私人教學研究資產，不作本篇閱讀主幹。**本篇不提供可直接開立的第一劑、劑量、間隔或輸注建議；臨床決策需由實際照護團隊按患者狀態、原始資料及院內規範處理。**
