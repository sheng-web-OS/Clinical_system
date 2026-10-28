# Lab Medicine 01｜早晨一張 Lab sheet：真實病例、實驗室原理與證據界線

本頁對應[〈早晨一張 Lab sheet：從真實病例與原始研究，判斷數字究竟能告訴我們什麼〉](lessons/2026-10-28-lab-morning-sheet.md)。**目前正文主幹是 2024 AML 真實病例、一篇有嚴格納排條件的 66 人急診研究，以及一篇 2,440 人同日重抽急診回溯研究**；後續 AKI 與 ADHF 為**不同文獻、不同人群**的說明，絕不能把它們拼成同一患者或把病例推論當成醫囑。舊稿的 70M 心衰竭完整四時點合成時間線已非主故事。原來源頁的 UKKA／KDIGO 原始圖表核對紀錄仍保留，但不代表新稿已通過獨立醫學或教學審查。

## 0. 三份直接支持新版正文的真實來源（原始資料／分母／反事實）

**A. 2024 AML 案例：介入與重驗混在一起，不能聲稱無治療的 K 7.8→3.6。** [Manual flagging failed to identify pseudohyperkalemia in acute myeloid leukemia: case report, *International Journal of Emergency Medicine*](https://pmc.ncbi.nlm.nih.gov/articles/PMC11462689/)；[原出版社](https://link.springer.com/article/10.1186/s12245-024-00734-x)。原文 Table 1 明確列 2024-04-03 四個 samples：A 12:00 K3.0、B 20:03 K6.7、C 20:48 K7.8、D 23:37 K3.6 mEq/L。B/C 用 pneumatic tube、D 走路送檢；原患者 WBC 206.8 ×10³/µL（90% blasts）、Hb 7.9 g/dL、platelet 38 ×10³/µL、creatinine 1.2 mg/dL。**原作者明示 D 於降鉀治療開始約 30 分鐘後取得**，因此不能把後續 3.6 當「無介入的乾淨重驗」；不同採檢/運輸方式亦不能單獨分出每一因素的因果效應。這篇 case report 支持對該患者檢體失真的調查，不構成普遍 ECG/AKI/治療決策規則。

**B. 低風險急診 66 人研究：只有符合納排條件才有外推可能。** [Accuracy of Hemolyzed Potassium Levels in the Emergency Department, *Western Journal of Emergency Medicine*](https://pmc.ncbi.nlm.nih.gov/articles/PMC7673871/)；[PubMed](https://pubmed.ncbi.nlm.nih.gov/33207176/)。原始 399 encounter 先篩出符合年齡、腎功能與重抽條件者，排除高風險或樣本重抽超時後只留下 66。初次有溶血 K 中位數 5.8 mmol/L、重抽中位 3.9、重抽未持續高鉀 0/66；**95% CI 0–6%** 並不等於全病人群的 0% 真風險。原文排除 ≥65 歲、eGFR<60、調鉀藥物、血液惡性疾病、重抽前降鉀治療及其他條件。此研究不足以支持病房 AKI／ACEi／老年患者延後危急處理，且未直接測量不重抽之決策的因果安全性。

**C. 同日重抽 2,440 人研究：不可用分母錯置宣稱急診高鉀有 35% 一定是假的。** [Hyperkalemia or Not? A Diagnostic Pitfall in the Emergency Department, *West J Emerg Med* 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11908522/)；[PubMed](https://pubmed.ncbi.nlm.nih.gov/39918159/)。在有**首次 whole blood/plasma K≥5.0、當日又完成重抽**的急診病人中，1,576（65%）再次高鉀，864（35%）重抽正常；後者之中 597（69%）第一次檢體有溶血。**這不是所有抽血者、所有初次高鉀者或所有住院者的母體發生率**；研究用「當日重抽結果」操作性定義 factitious，不能自動排除選擇偏差、治療時序與其他樣本差異。2019/2020 小樣本與 2025 大樣本研究的分母及適用對象不同，不能拿兩個百分比直比或合併成單一「重抽安全規則」。

## 0A. 補充案例（非目前文章主故事）

- [Salvagno et al., *A paradigmatic case of haemolysis and pseudohyperkalemia in blood gas analysis*](https://pmc.ncbi.nlm.nih.gov/articles/PMC6366946/)：51M venous blood-gas syringe K5.2；不同試管 lithium-heparin plasma K4.6；原 syringe 餘血的 hemolysis index50，而另一管 index5；運送約15分鐘直接接觸冰塊。這是前分析干擾個案，**不是 AML 病人或原 HF 合成個案**。
- [Šálek 2018, *Pseudohyperkalemia - Potassium released from cells due to clotting and centrifugation*](https://pmc.ncbi.nlm.nih.gov/articles/PMC5806620/)：62F essential thrombocythemia，platelets1305 ×10⁹/L、WBC39.8 ×10⁹/L，serum K6.3、plasma4.6、whole blood3.4 mmol/L；CBC 解釋部分檢體差異，不可將不同患者的數值拼接。

**證據界線**：真實病例只支持病例內觀察，單一研究的比例只適用其納排條件；HK 急救閾值、確認採檢與醫囑須回 UKKA 等當代指引、病人當下狀態及當地院內 SOP。以下原始來源與圖表的限定審查，不代表這個新版已獲獨立審稿 PASS。

## 1. 為何一張 BMP 可能不完全可信？

[Takieddine LT, El-Khoury JM. Laboratory Anomalies in the Basic Metabolic Panel: Core Curriculum 2025. *American Journal of Kidney Diseases*. 2025;85(1):104–114. DOI: 10.1053/j.ajkd.2024.06.019.](https://www.sciencedirect.com/science/article/pii/S0272638624009211)

[PubMed 索引](https://pubmed.ncbi.nlm.nih.gov/39396361/)與 [AJKD 期刊來源頁](https://www.ajkd.org/article/S0272-6386(24)00921-1/fulltext)。

**臨床關聯**：preanalytical（採檢／運輸／儲存）、analytical（測定方法）與 postanalytical（報告詮釋）可造成與實際病況不符的異常；hemolysis 影響 K 的例子是本篇判讀鏈起點。無明顯 ECG 變化、標註溶血、與既往差距大，會提高重驗的重要性，但**無法單獨排除真正高鉀**。

**本文並未聲稱**原研究提供了本篇 70 歲合成病例、K 6.3→4.9 數值或一套固定高鉀急救規則；這些只是教學情境。公開網站不重製該論文受版權保護的原圖。

**原始圖表核對邊界**：AJKD 原文（85 卷 1 期，104–114 頁）可查得電解質異常與採樣、測量干擾的論述，並有 Figure 1 檢驗流程相關說明；本次僅核實書目、可讀的期刊正文與已顯示的內容，未逐張取得 Figure/Table 全部原畫面和圖說。因此不把本文的病例圖說成 AJKD Figure 1 的翻拍，亦不把該來源列作「原始圖表已完整目視驗收」。若欲深入查溶血 index、不同樣本型態與假性異常的定量限制，應回看期刊全文及各院實驗室條件。

## 2. AKI 是時間定義，不是 Cr 的單次絕對值

[KDIGO 2012 AKI work group 綜述：Diagnosis, evaluation, and management of acute kidney injury: a KDIGO summary (Part 1).](https://pmc.ncbi.nlm.nih.gov/articles/PMC4057151/)

[ADLM/AACC Guidance Document on Laboratory Investigation of Acute Kidney Injury, JALM 2021](https://academic.oup.com/jalm/article/6/5/1316/6272705)。

血清 creatinine 若 48 小時內增加 ≥0.3 mg/dL、7 日內增加至 ≥1.5 倍基線，或尿量低於 0.5 mL/kg/h 達至少 6 小時，即符合 KDIGO AKI 定義。主文以兩次獨立重抽的 Cr 1.68、1.69 及昨天 1.16 判斷 AKI；尿量 240 mL/8h 在 75 kg 情境中只有 8 小時平均約 0.4 mL/kg/h；**不能僅由 8 小時總量證實連續 6 小時的門檻**，仍須核對分時紀錄與漏記，才能判斷尿量診斷條件。AKI 定義不會回答病因；為確認腎前、鬱血、內因性傷害或阻塞，需要另外的病人與尿液證據。

[KDIGO 2024 CKD guideline](https://kdigo.org/guidelines/ckd-evaluation-and-management/)與[非穩態 eGFR 限制的臨床導讀](https://academic.oup.com/ajhp/article/82/12/660/8107680)。CKD 的穩態估算架構不可直接視為 AKI 當下瞬間真實 GFR。

**已目視的 KDIGO 2012 原表／原圖**：Chapter 2.1，印刷 p.19 **Table 2 (Staging of AKI)**，明列 Cr ≥0.3 mg/dL 的 stage 1 分期條件與 <0.5 mL/kg/h 持續 6–12 小時的尿量門檻；Chapter 2.3，印刷 p.25 **Figure 4 (Stage-based management of AKI)**，將 volume status/perfusion、nephrotoxic exposure、Cr/urine monitoring 與必要時的 RRT 評估列為隨風險階段處理的項目。Figure 4 圖說還指出陰影強度代表措施隨嚴重度增加而提高優先度，**不是已知病因、絕對給液量或透析 cutoff**。[KDIGO AKI 原始完整 PDF](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf)。

## 2A. 心衰竭合併 AKI：為何 Cr 上升不等於缺水？

[2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure：住院 ADHF 的初始 assessment 需要同時評估 congestion 與 perfusion](https://www.jacc.org/doi/10.1016/j.jacc.2021.12.012)。

[Michigan Medicine Inpatient Diuretic Guideline for Patients with Acute Decompensated Heart Failure：Q18，creatinine rise during effective decongestion](https://www.ncbi.nlm.nih.gov/books/NBK589894/)。

原文章由「既有鬱血、靜脈利尿、Cr 升高」推進至心衰竭的血流動力不確定性時，有必要先區分**殘餘鬱血、有效灌流、腎臟實質損傷與阻塞**，而不是單看 I/O 負 1.4 L 便補液或一律停藥。AHA/ACC/HFSA 指引支持同時看 congestion/perfusion；Michigan Medicine 住院利尿實務規範提醒 modest Cr increase 在仍有鬱血時不一定是必須停止利尿的獨立理由。但兩項參考**不能證明本文合成病例的 Cr 上升為 benign、也不能直接決定實際病人的利尿劑量**。新的逐段病例寫法把床邊灌流／鬱血資訊放在醫囑抉擇之前，而非直接由 Cr 得出單一治療。

## 3. 高鉀救治需要 ECG、病人風險和分層流程

[UK Kidney Association，Treatment of Acute Hyperkalaemia in Adults（官方頁，載有 2026 年 7 月更新版下載入口）](https://www.ukkidney.org/health-professionals/guidelines/treatment-acute-hyperkalaemia-adults-0)。

[醫院臨床操作頁：GGC Medicines，Management of Hyperkalaemia](https://handbook.ggcmedicines.org.uk/guidelines/electrolyte-disturbances/management-of-hyperkalaemia-plasma-k-5-5mmol-l/)。

臨床依據是血鉀數值、檢體品質、ECG、循環狀態、renal function、治療後回測與 glucose monitoring 共同決定。主文沒有提供可脫離當地 protocol 使用的 calcium/insulin 劑量。IV calcium 是穩定心肌膜而非實際排除鉀；insulin 促進 K 從細胞外轉入細胞內，必須防低血糖；持續高鉀需另外解決鉀移除、原因與復發。

**已逐頁目視的原文範圍**：UKKA *July 2026* 官方完整 PDF 的印刷 **p.14–15（PDF 第 14、15 張，從零起算索引 13、14）**。原文 Guideline 15.3 建議疑似假性高鉀時以不同容器的配對 lithium-heparin 與 clotted serum 採樣核實；Guideline 16.2a 指出 ECG 改變時 IV calcium 建議強度為 **2C**（2026 已降級，不可拿它當高等級確定療效證據）；16.3.1 與 16.3.2 區分嚴重和中度高鉀使用 insulin-glucose 的建議強度。17.1–17.2 要求注意血鉀反彈與 insulin 後低血糖。這些是**原文建議與適用限制**，主文合成案例並未使用其固定處方劑量。[開啟 UKKA 2026 原始 PDF](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf)。

**與本文最相關的 UKKA 原始圖／表已補做目視核對**：[Figure 4，印刷 p.75／PDF 索引 74](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=75)，描繪心肌保護、細胞轉位、移除鉀、血鉀與血糖監測、避免復發五個處置面向；此圖不代表每位中度高鉀患者都要給 IV calcium。[Table 22，印刷 p.98／PDF 索引 97](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=98) 是原指引的 insulin-glucose protocol，包含治療前血糖、後續補糖條件及血糖與 K 監測，且原表下方特別指出腎衰竭病人的輸液體積負擔。主文不提供固定劑量，避免把此原圖誤當台灣各院通用 order set。原圖只提供合法原站連結，不重製像素。

已查看以上指引的相關條文與頁面，但**未完整審閱 180 頁全部 Appendix、每一張 algorithm 或特定醫院 formulary**；不可宣稱全套圖表完整驗收。對任何實際用藥仍須回原頁與當地流程。

## 3A. 低鎂與心律：為何新心電證據會改變處置？

[NHS Specialist Pharmacy Service, *Treating acute hypomagnesaemia in adults* (2024, 現行臨床用藥安全指引)](https://sps.nhs.uk/articles/treating-acute-hypomagnesaemia-in-adults/)

[ESC ACVC/EHRA/HFA 2025 consensus, *Ventricular arrhythmias in acute heart failure*, Table 4 / reversible causes](https://onlinelibrary.wiley.com/doi/full/10.1002/ejhf.3645)

主文額外設計 **08:40 telemetry 單發 PVCs 變多、Mg 1.5 mg/dL、09:00 循環仍穩定** 的合成觀察，目的是讓另一個原本只是紅字的檢驗值真正改變監測／可逆因素評估。Loop diuretic 為低鎂可能的藥因；低鎂可增加心律風險，但**不等於此病人的 PVCs 已被診斷由低鎂造成**。NHS SPS 提醒因 AKI、嚴重 CKD 或透析而補鎂者應先尋求適當專業評估，補充路徑及給藥量不能從單一 Mg 數字照抄；嚴重心律異常時必須先處理臨床急症。ESC 共識支持在急性心衰竭心律不整中找出並修正可逆因素，但沒有證實合成病例 PVC 的單一病因。這不是對 Mg 1.5 和 PVC 之間因果的實證研究，也不是台灣院內補鎂 order set。

## 4. Hb、輸血與族群差異

[Carson JL et al. Red Blood Cell Transfusion: 2023 AABB International Guidelines. *JAMA*. 2023.](https://pubmed.ncbi.nlm.nih.gov/37824153/)

[AABB 2025 AMI transfusion 建議說明](https://www.aabb.org/news-resources/news/article/2025/08/20/expert-panel-recommends-liberal-transfusion-strategy-for-hospitalized-patients-with-ami)。

一般 hemodynamically stable inpatient 與 cardiac surgery、既存 cardiovascular disease、active bleeding、acute MI 等族群的血品策略不可互換；本篇 Hb 10.2 不能孤立地觸發一般成人紅血球輸血，但**這不是說 Hb 10.2 的所有臨床狀態均不需介入**。

## 5. 檢驗是臨床問題的工具，不是每天必填的欄位

[Society of Hospital Medicine: Choosing wisely in adult hospital medicine, 2013](https://pubmed.ncbi.nlm.nih.gov/23956231/)；[Choosing Wisely Canada: Using Labs Wisely](https://choosingwiselycanada.org/hospitals/labs-test/)。

以上建議限於**clinical and laboratory stability** 時避免無目的重複抽 CBC/chemistry，不應用來減少持續 AKI、電解質異常、治療風險或不穩定病人的必要監測。是否重測由預期對處置的資訊增量決定。

## 6. 圖表的身分

[主文圖 1](lessons/2026-10-28-lab-morning-sheet.md#lab-three-clocks) 是本站原創的**合成病例「同一張 Lab、兩種灌流證據」反事實比較圖**。它固定 06:00 溶血 K 6.3 → 07:15 無溶血 K 4.9、10/27 Cr 1.16 → 10/28 重抽 Cr 1.69、I/O 負 1.4 L，以及 240 mL／8 h（平均約 0.4 mL/kg/h、採檢以外的尿量收集可靠性**待確認**），比較 A：09:00 BP 112/70、四肢溫暖、JVP 高，與 B：同樣 Lab 但 BP 90/55、四肢冰冷且仍鬱血的**反事實**。病人危險分流、採檢可信度、AKI 原因仍須**並行**評估，但新增的灌流資料會改變「沿用去鬱血評估」與「立即升級休克評估」的急迫性。

這不是 KDIGO 2012 AKI staging Table／Figure 4、UKKA hyperkalaemia Figure 4／Table 22、AJKD Figure 的重製，也不是驗證過的「warm 就一定利尿、cold 就一定補液」處方圖。A 組是本篇**合成**病例明確宣告的新床邊觀察，B 組是刻意只改部分床邊資訊的反事實；相同 Cr 與 I/O 無法證實同一種 AKI 病因。若要查實際 cutoff 或心律／灌流分支，應返回原始指引與圖說、結合病人狀態與當地流程。

