# Lab Medicine 01｜檢體可信度：真實病例、實驗室原理與證據界線

本頁對應[〈早晨一張 Lab sheet：從真實病例與原始研究，判斷數字究竟能告訴我們什麼〉](lessons/2026-10-28-lab-morning-sheet.md)。這篇文章的核心，是依照 2024 年 AML 個案的原始採樣記錄，理解為什麼檢體處理會改變報告中的 K；再以 66 人和 2,440 人兩份不同納排條件的急診研究，判斷這種經驗可以外推到哪裡。後段 AKI 與心衰竭的說明則取自**另外的研究與指引**，並非替 AML 患者補寫心衰竭或新的抽血與處置。以下連結提供原文、表圖位置，以及每個推論不能跨越的界線。

## 0. 三份直接支持新版正文的真實來源（原始資料／分母／反事實）

**A. 2024 AML 案例：介入與重驗混在一起，不能聲稱無治療的 K 7.8→3.6。** [Manual flagging failed to identify pseudohyperkalemia in acute myeloid leukemia: case report, *International Journal of Emergency Medicine*](https://pmc.ncbi.nlm.nih.gov/articles/PMC11462689/)；[原出版社](https://link.springer.com/article/10.1186/s12245-024-00734-x)。原文 Table 1 明確列 2024-04-03 四個 samples：A 12:00 K3.0、B 20:03 K6.7、C 20:48 K7.8、D 23:37 K3.6 mEq/L。B/C 用 pneumatic tube、D 走路送檢；原患者 WBC 206.8 ×10³/µL（90% blasts）、Hb 7.9 g/dL、platelet 38 ×10³/µL、creatinine 1.2 mg/dL。**同病例的另一項 analyte 也曾造成困擾：**居家採樣 Hb 4.5 g/dL（兩天前 7.5）觸發急診轉診，急診 Hb 7.9 g/dL；作者稱居家 Hb 4.5 為錯誤讀值，卻沒有證據可把 Hb 差異歸因於造成 K 假高的同一個確定機轉。這些是原文 Case presentation 的觀察，不是 AI 補造的 CBC 數據。 **原作者明示 D 於降鉀治療開始約 30 分鐘後取得**，因此不能把後續 3.6 當「無介入的乾淨重驗」；不同採檢/運輸方式亦不能單獨分出每一因素的因果效應。這篇 case report 支持對該患者檢體失真的調查，不構成普遍 ECG/AKI/治療決策規則。

**B. Wilson et al. 2020（正式發表於 2020-10-20）的低風險急診 66 人研究：只有符合納排條件才有外推可能。** [Accuracy of Hemolyzed Potassium Levels in the Emergency Department, *Western Journal of Emergency Medicine*](https://pmc.ncbi.nlm.nih.gov/articles/PMC7673871/)；[PubMed](https://pubmed.ncbi.nlm.nih.gov/33207176/)。原始 399 encounter 先篩出符合年齡、腎功能與重抽條件者，排除高風險或樣本重抽超時後只留下 66。初次有溶血 K 中位數 5.8 mmol/L、重抽中位 3.9、重抽未持續高鉀 0/66；**95% CI 0–6%** 並不等於全病人群的 0% 真風險。原文排除 ≥65 歲、eGFR<60、調鉀藥物、血液惡性疾病、重抽前降鉀治療及其他條件。此研究不足以支持病房 AKI／ACEi／老年患者延後危急處理，且未直接測量不重抽之決策的因果安全性。

**C. 同日重抽 2,440 人研究：不可用分母錯置宣稱急診高鉀有 35% 一定是假的。** [Hyperkalemia or Not? A Diagnostic Pitfall in the Emergency Department, *West J Emerg Med* 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11908522/)；[PubMed](https://pubmed.ncbi.nlm.nih.gov/39918159/)。在有**首次 whole blood/plasma K≥5.0、當日又完成重抽**的急診病人中，1,576（65%）再次高鉀，864（35%）重抽正常；後者之中 597（69%）第一次檢體有溶血。**這不是所有抽血者、所有初次高鉀者或所有住院者的母體發生率**；研究用「當日重抽結果」操作性定義 factitious，不能自動排除選擇偏差、治療時序與其他樣本差異。2019/2020 小樣本與 2025 大樣本研究的分母及適用對象不同，不能拿兩個百分比直比或合併成單一「重抽安全規則」。

## 0A. 補充案例（非目前文章主故事）

- [Salvagno et al., *A paradigmatic case of haemolysis and pseudohyperkalemia in blood gas analysis*](https://pmc.ncbi.nlm.nih.gov/articles/PMC6366946/)：51M venous blood-gas syringe K5.2；不同試管 lithium-heparin plasma K4.6；原 syringe 餘血的 hemolysis index50，而另一管 index5；運送約15分鐘直接接觸冰塊。這是另一名患者的前分析干擾個案，不能與 AML 病人的時序混寫。
- [Šálek 2018, *Pseudohyperkalemia - Potassium released from cells due to clotting and centrifugation*](https://pmc.ncbi.nlm.nih.gov/articles/PMC5806620/)：62F essential thrombocythemia，platelets1305 ×10⁹/L、WBC39.8 ×10⁹/L，serum K6.3、plasma4.6、whole blood3.4 mmol/L；CBC 解釋部分檢體差異，不可將不同患者的數值拼接。

**證據界線**：真實病例只支持病例內觀察，單一研究的比例只適用其納排條件；HK 急救閾值、確認採檢與醫囑須回 UKKA 等當代指引、病人當下狀態及當地院內 SOP。以下原始來源與圖表的限定審查，不代表這個新版已獲獨立審稿 PASS。

## 1. 為什麼同一張 BMP／CBC 的數字會彼此矛盾？

[Takieddine & El-Khoury, *Laboratory Anomalies in the Basic Metabolic Panel: Core Curriculum 2025*, AJKD 85:104–114](https://pubmed.ncbi.nlm.nih.gov/39396361/) 討論檢驗的前分析（採血、試管、運送、儲存）、分析（方法與儀器）和報告後詮釋的誤差來源；[期刊全文入口](https://www.ajkd.org/article/S0272-6386(24)00921-1/fulltext)。這些途徑說明 **K 的試管濃度**與**病人體內即時濃度**為何有時不同，卻不能僅因數據不合就宣告病人無危險。

[2024 AML 原始病例 Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11462689/) 真正有用的不是最後一個 K 3.6，而是四筆樣本的不同來源：A 從家中採、plasma，B/C 在急診使用 whole blood 與氣送管，D 雖仍是 whole blood、改成步行送檢，卻已處在降鉀治療之後。若要研究「單獨是氣送管造成多少 K 升高」，必須保留其他條件不變；原病例沒有達到這個反事實條件。

此病例的 **Hb 4.5 g/dL（家中檢體）與 7.9 g/dL（急診複測）** 也不一致；作者認為前者是檢驗錯誤。這不等於讀者有足夠資訊定量還原錯誤原因；它提醒我們**CBC 的採樣可信度與 chemistry 的干擾須分別查證**。而 AML 患者 WBC 206.8×10³/µL、90% blasts、platelet 38×10³/µL，不能被套用一般低風險急診重抽研究。

## 2. Cr 是濃度及時間的訊號，不是 AKI 病因的直接測量

[KDIGO 2012 AKI 官方原始完整 PDF](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf) 中 **Table 2 — Staging of AKI（印刷 p.19，[PDF p.22](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf#page=22)）** 規定肌酐與尿量分期；在 48 小時內 SCr 增加 ≥0.3 mg/dL，或 7 天內 ≥1.5 倍基線，或尿量 <0.5 mL/kg/h 持續至少 6 小時，均須按定義的時間條件判讀。**Figure 4 — Stage-based management（印刷 p.25，[PDF p.28](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf#page=28)）** 將容量與灌流、避免腎毒性暴露、Cr/尿量監測與依病情處理的優先度連起來，**不是**「每個 AKI 病人補一定量 saline」或任何單一的透析 cutoff。

例如 *假想*「75 kg 病人最近 8 小時尿量總計 240 mL」只能得到平均 0.4 mL/kg/h；**8 小時總量不足以單獨證明連續 6 小時的尿量門檻，還要核對分時及收集完整性**。此處是單純的測量限制示例，**不是** 2024 AML 病人的病歷，也不是合成患者的治療方案。

[ADLM/AACC *Guidance Document on Laboratory Investigation of AKI*, 2021](https://academic.oup.com/jalm/article/6/5/1316/6272705) 補足採檢時間、檢驗準確度及動態變化的背景；[KDIGO CKD 2024](https://kdigo.org/guidelines/ckd-evaluation-and-management/) 的穩態 eGFR 用法不可直接當作 AKI 的即時腎清除能力。

## 3. 心衰竭的 Cr 上升：需要的是病因證據，而不是從 Lab 直接開藥

[2022 AHA/ACC/HFSA Heart Failure Guideline](https://www.jacc.org/doi/10.1016/j.jacc.2021.12.012) 與 [Michigan Medicine Inpatient Diuretic Guideline，Q18](https://www.ncbi.nlm.nih.gov/books/NBK589894/) 說明住院失代償心衰竭須整合 **congestion、perfusion、治療中的腎功能變化與安全風險**。有些病人在有效去鬱血時會有暫時性的 Cr 升高，也有病人可能存在低灌流、持續腎靜脈鬱血、藥物或腎實質傷害；兩種情況不能只靠 Cr 濃度區分。

正文談的是**這些原始研究與指引所容許的機轉和決策界線**，不是把 2024 AML 患者突然寫成有心衰竭，或讓虛構 70 歲病人的 Cr/I-O 替另一人決定停止利尿或補液。

## 4. 真正高鉀的危急界線，以及其他 Lab 項目的用藥前提

[UK Kidney Association, *Treatment of Acute Hyperkalaemia in Adults*, July 2026](https://www.ukkidney.org/health-professionals/guidelines/treatment-acute-hyperkalaemia-adults-0)：**Figure 4（原印刷 p.75，[PDF p.75](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=75)）** 區分心肌保護、暫時移鉀、實際移鉀、血鉀/血糖監測及預防復發；**Table 22（原印刷 p.98，[PDF p.98](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=98)）** 說明 insulin-glucose 與後續監測細節。指引推薦強度和適用條件不可由單一病例外推。特別是，**心電圖（ECG）沒有典型變化，不能保證不存在真高鉀**；危急風險評估與檢體查核必須並行。若依適用指引由醫療團隊選擇 insulin-glucose，除了暫時將 K 轉入細胞，還須留意**低血糖、反彈性高鉀與腎功能不佳患者的補液體積風險**；因此 Table 22 的後續血糖／K 追蹤不是可刪除的附註。原圖不在本站翻印，也不能把其他國家的固定處方劑量直接套進台灣醫院。

血氣與生化 total CO₂、serum/plasma 不同採檢介面、Na 與滲透質、CBC 的 in-vitro vs in-vivo 溶血，都要先確認**究竟測量哪個對象**；沒有真病例時不必為了列舉每個 Lab 項目而編造病人、抽血或治療結果。

另可參考 [NHS SPS 急性低鎂用藥評估](https://sps.nhs.uk/articles/treating-acute-hypomagnesaemia-in-adults/) 和 [ESC 2025 心衰竭心室心律不整共識](https://onlinelibrary.wiley.com/doi/full/10.1002/ejhf.3645/)，但本篇真實病例**沒有**報告低鎂導致 PVC 的確定因果，也沒有依這些來源核准任何鎂製劑醫囑。[AABB 2023 輸血指引](https://pubmed.ncbi.nlm.nih.gov/37824153/) 則有穩定住院患者與不同心血管族群的限定；不能由 AML 病例一個 Hb 數字推成所有病人的輸血準則。

## 5. 檢驗是臨床問題的工具，不是每天必填的欄位

[Society of Hospital Medicine: Choosing wisely in adult hospital medicine, 2013](https://pubmed.ncbi.nlm.nih.gov/23956231/)；[Choosing Wisely Canada: Using Labs Wisely](https://choosingwiselycanada.org/hospitals/labs-test/)。

以上建議限於**clinical and laboratory stability** 時避免無目的重複抽 CBC/chemistry，不應用來減少持續 AKI、電解質異常、治療風險或不穩定病人的必要監測。是否重測由預期對處置的資訊增量決定。

## 6. 圖 1 如何讀：時間軸、研究分母和不能識別的因果

[返回正文原創圖 1](lessons/2026-10-28-lab-morning-sheet.md#lab-three-clocks)。圖的第一部分是 2024 年 AML **同一位病人**的四次檢體時序：**A 12:00 K3.0（plasma、家中採血、courier／步行）→ B 20:03 K6.7（whole blood、氣送管）→ C 20:48 K7.8（whole blood、氣送管）→ D 23:37 K3.6（whole blood、步行）**。D 是**降鉀治療開始後約 30 分鐘**才取得，因此 C 與 D 的檢驗差異**不能**解釋為「單獨把氣送管改成步行」的效果。資料與採樣方法源自 [2024 AML 原文 Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11462689/)；此圖僅重排必要數據，不複製原表版面。

第二部分是 **另一篇 2025 年、2,440 位「初次 K≥5.0 且當日有重抽」的急診患者**研究：[研究原文與 Figure 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC11908522/)。按研究操作性分類，2,440 中有 **1,576（65%）**重抽仍高與 **864（35%）**重抽正常；**只有在 864 人裡**，才有 **597／864（69%）**初始檢體有溶血，以及 267／864（31%）未見溶血。不能把 597／864 的 69% 當成 597／2,440，也不能把 864／2,440 推成所有急診高鉀患者的真實盛行率，因為研究只納入當日有重抽的人。原文 Figure 2 已整理上述分母；本站用**獨立的時間軸＋巢狀分母圖**再呈現「治療混雜」與「選擇性重抽」兩個不同學習點，沒有翻拍原圖。

另外 [2020 低風險研究 n=66](https://pmc.ncbi.nlm.nih.gov/articles/PMC7673871/) 是**第三份獨立證據**，並非上面 2,440 人的子群；研究有嚴格排除 65 歲以上、腎功能較差、血液惡性疾病及調鉀藥物等條件。因此圖旁的 n=66 只能做外推界線提示，不能合併進 2,440 的分母，也不能替 AML 病人或高齡心衰竭病人核准安全等待。

以上都是**原始研究數據的證據關係圖**，不是已驗證的診斷決策法則，不提供任何固定藥物、抽血時間與處置療效。臨床危急分流仍以真實病況與 [UKKA 原始指引](https://www.ukkidney.org/health-professionals/guidelines/treatment-acute-hyperkalaemia-adults-0) 適用條件為準。
