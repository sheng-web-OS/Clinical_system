# Lab Medicine 01｜真實病例證據封包（供 PR #187 重寫；非發布收據）

2026-10-28 編輯方向修正：使用者不應被要求以 AI 自創的 70M 心衰竭數據批准實際醫囑。本封包提供「有原始報告、可看見採檢與量測方法」的真實病例錨點，並把可觀察事實、作者推論、普遍臨床規則嚴格分層。**本封包為資料核對，不是獨立醫學審稿、合法原圖重製許可或已發布正文。** 如需重製原表或原圖，另核著作權及圖說；建議原表直接連結來源。

## Case A｜2018 血小板增多造成假性高鉀（最適合整張 Lab panel 主故事）

**原文**：Šálek T. *Pseudohyperkalemia - Potassium released from cells due to clotting and centrifugation - a case report.* Biochem Med (Zagreb). 2018;28(1):011002. DOI [10.11613/BM.2018.011002](https://doi.org/10.11613/BM.2018.011002)，[PMC 全文／Table 1／Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC5806620/)，[PubMed PMID29472808](https://pubmed.ncbi.nlm.nih.gov/29472808/)。

### 原文直接報告（observed，不是 AI 合成）

62 歲女性、JAK2 V617F 的 essential thrombocythemia，因胃潰瘍出血性休克接受手術；手術期間有輸血；hydroxycarbamide 因出血停藥。術後第 12 天的檢驗見 serum K **6.3 mmol/L**、platelets **1305 ×10^9/L**、WBC **39.8 ×10^9/L**，serum creatinine **114 μmol/L**、serum Na **131 mmol/L**。後續使用不同基質／方法測 K：lithium-heparin plasma **4.6 mmol/L**，whole blood（blood-gas analyzer）**3.4 mmol/L**；原文 Table 1 還列 plasma Na 132、whole blood Na 128，說明不能把不同檢體與方法自動當作相同檢測條件。**這些測值並非同一個方法下對同一試管的三次重測。**

真實工作時序：第一組 sample 在 **08:10** 進入實驗室、**09:19** 結果報告且電話通知臨床；血氣用的後續 sample **09:34** 採集、**09:37** 報告（詳原文 Case/Methods，該樣本由 femoral artery 採血）。原研究還有術後追蹤 11 組 platelet／serum K 配對、Spearman ρ **0.64（P <0.05）**，但這是**單病人**配對時序關聯，不能把相關係數說成普遍診斷特異度或此病人血鉀體內濃度之絕對真相。

### 作者可支持的推論範圍

- Platelets 在 serum clotting 可釋放 K；高 platelet 與 leukocyte 數量可使血清檢測受到嚴重的 preanalytical / sample matrix 干擾。原文同時指出 plasma 經 centrifuge 後 4.6 高於 whole blood 3.4，提示機械處理與脆弱細胞等複合因素。
- 本例 serum 看不到主要溶血干擾，**不等於沒有 pseudohyperkalaemia**。這是比「溶血 K6.3→重抽4.9」的合成例更能教會「同一張 panel 的 CBC 不只是陪襯」的真實素材。
- 不能把三個檢體結果的差異全用單一機轉定量歸因，也不能把「所有血小板高者的全血 K 都是 3.4」當成規則。這例個別病人的胃出血、術後用藥、腎功能與心電數值是否存在、採檢與輸血後的完整治療判斷，僅能依原文有記載的部分描述；未報資料一律 NOT_REPORTED。
- Case report 支撐這位病人的測值與臨床／實驗室處置，**不證明**所有危險高鉀都應先重驗而延遲 ECG／急救，亦不證明任何標準補液、利尿、透析或降鉀療法優劣。

## Case B｜2019 venous blood gas 運送直接接觸冰塊約 15 分鐘

**原文**：Salvagno GL, Demonte D, Lippi G. *A paradigmatic case of haemolysis and pseudohyperkalemia in blood gas analysis.* Biochem Med (Zagreb). 2019;29(1):011003. DOI [10.11613/BM.2019.011003](https://doi.org/10.11613/BM.2019.011003)，[PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC6366946/)，[PubMed PMID30799980](https://pubmed.ncbi.nlm.nih.gov/30799980/)。

### 原文直接報告（observed）

51 歲男性、長期氣喘，喘與喘鳴惡化就醫；採的是**靜脈**血氣，不是動脈血氣。第一次用 **3.0 mL heparinized syringe** 抽血，GEM Premier 4000 檢出 whole-blood K **5.2 mmol/L**（當地 whole-blood 參考 3.5–4.5）；研究註明初次血氣儀器未提示溶血警示。因結果出乎臨床預期，再從另外 venipuncture 採 **3.5 mL lithium-heparin tube**，Cobas 8000 得到 plasma K **4.6 mmol/L**（當地 plasma 參考 3.5–5.0）、hemolysis index **5（0.05 g/L）**。

研究者隨後把**第一次血氣 syringe 剩餘血**轉到 plastic tube、centrifuge，測得同一來源樣本 K **5.5 mmol/L**、hemolysis index **50（0.5 g/L）**；追查採檢流程，發現 syringe 運送時約 **15 分鐘直接貼著冰塊**。這組資料比簡單「5.2 vs 4.6」更重要，因為第一次 syringe 經後續檢測確實有顯著的溶血干擾證據。**兩次 K 不同時也改了 specimen/assay；不可把 0.6 mmol/L 差值定量全部歸因於冰塊，或宣稱兩個機器可完全互換。**

該篇初次 venous blood gas 同時回報 pO₂ **16 mmHg**、SO₂ **38%**、pCO₂ **57 mmHg**；它們是**靜脈檢體**的數值，不能像動脈 PaO₂／SaO₂ 一樣解讀。這能直接支持「看到一張 Lab，先問採樣位置／檢體類型」的教學主題。沒有足夠資料能由此 alone 判病人的動脈氧合程度。

### 原文不能證明的事

- 病人之後的臨床治療為氣喘照護，**不是**心衰竭或 AKI 的藥物與輸液療效證據；不能偷移到原合成 70M 的病程。
- 作者確認了這次運送流程的缺陷與假性高鉀的實驗室解釋；原文**沒有**發表「普遍危急高鉀應等候重驗、不必急救」的 randomized treatment recommendation。
- 若須再討論如何選擇重驗、配對 serum/plasma 或何時立刻救治，改引 [UKKA 2026 高鉀指引](https://www.ukkidney.org/health-professionals/guidelines/treatment-acute-hyperkalaemia-adults-0)、當地 lab SOP 與 clinical stability/ECG，而不是只從此 case 下 universal order。

## 要如何把兩份原始病例寫成一篇有效的第一課

1. **先問測量對象／方法**：serum clotting vs heparin plasma vs immediate whole blood、lysis index、blood gas 的靜脈／動脈差異，並把「檢驗室看到的濃度」與「病人體內的濃度」分開。
2. **再將同一病人的真正原始數據與時間放回來**：以 Case A 的 Table 1/2（CBC 與 serum/plasma/whole blood K 的衝突）作主軸，Case B 的 ice contact（明確可回查的 preanalytical error）作對照。原作者報告 vs AI 編輯的因果推理，逐句標清楚。
3. **才回到臨床邊界**：不因 pseudohyperkalaemia 可能性延誤已不穩病人的急救；沒有以本案例實際觀察到的 AKI/ADHF 路徑，就不可在主線把 HF 腎灌流、低鎂、輸液、利尿編成已被實證支持的「09:00 正確醫囑」。
4. **把原本合成的 70M 時序移至後段**，作題目／反事實練習且明確標示 **非病例報告**。這部分只能說在不同前提下有什麼不能推論、應查何種證據，不能冒稱正確的臨床治療時間與劑量。建議全文標籤用自然語句呈現，不將內部 EPQC/metadata 直接貼在讀者正文。
5. **國考題**：僅納入真實核實年份梯次科別題號與答案的官方試題；沒找到與 specimen matrix 直接對應的題，不要自行貼標官方。正式發表仍須 source gate／Figure Gate／獨立醫學 EPQC 與手機/production QA。

**來源使用提醒**：2018/2019 原始論文均有公開全文入口，但原 Table/Figure 的大量逐字重製與圖像權利需另外核對。這裡僅整理對案例推理必要的有限數據，讀者若需原表整體應連到原文，不在本站翻印。Web 檢索的可讀內文不能冒稱原 PDF 每一張原圖像素皆已目視。所有數值均採用原文原始單位，未轉換成其他單位的數值不要擅自換算後混入報告。

**出版標記**：RESEARCH_ONLY / NOT_IN_ARTICLE_YET / CLINICAL_PEER_REVIEW_NOT_VERIFIED / EDUCATIONAL_TRANSFER_NOT_VERIFIED。
