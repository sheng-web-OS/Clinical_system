# 早晨一張 Lab sheet：真正要判斷的是什麼？

2026 年第一版的問題，不在於缺少正常值，而在於我們太容易把一張報告看成「病人體內已經發生的事」。實際上，報告上的每個數字都有一條來路：病人當時的生理狀態、採血部位、試管與添加物、運送與離心、測量方法、檢驗室的品質檢查，最後才是臨床醫師看見的數字。**如果不知道這條來路，檢驗值甚至可能在還沒有進入病人的鑑別診斷以前，就已經被誤解。**

本篇先跟著兩份**真實、可全文核對的已發表病例報告**，理解同一位病人為什麼會有截然不同的血鉀值。哪個數字是原研究實際量到的、作者在推論什麼、現行指引允許我們做多遠的臨床判斷，會刻意分開。最後才放一段**明確標示的合成心衰竭情境**，練習把量測可信度與疾病病因拆開；這段練習不是經臨床驗證的處方，也不是案例報告。

## 第一問｜一張 Lab sheet 上寫 K 6.3，我們究竟量到了什麼？

### 一張真正不尋常的檢驗單：血鉀很高，血小板也非常高

先讀 2018 年 Šálek 發表的原始病例。患者是 **62 歲女性**，有 JAK2 V617F 相關的 essential thrombocythemia，因胃潰瘍出血性休克接受手術；原有的 hydroxycarbamide 治療因出血暫停。術後第 12 天的實驗室檢驗顯示 **serum K 6.3 mmol/L、platelets 1305 ×10⁹/L、WBC 39.8 ×10⁹/L**，另有 serum Na 131 mmol/L、creatinine 114 µmol/L。這是研究者實際報告的數據，不是 AI 編出的完整晨間 Lab panel。來源：[Šálek, Biochem Med 2018，原文 Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC5806620/)。

你可能直覺把它說成：「血鉀 6.3，病人非常危險；先降鉀。」但在確認這個數字代表什麼以前，另一個紅字——**platelet 1305 ×10⁹/L**——已經提示一個完全不同的問題：這管血在形成 serum 的過程中，可能有大量鉀從**試管裡的細胞**釋出。

血鉀的生理意義，取決於**血液中細胞外液的鉀濃度**，而細胞內含有大量鉀。檢驗室的 serum 不是在病人體內原封不動存在的液體；它通常經歷凝血、細胞與血清分離。Platelets 在凝血時釋出鉀，對血小板數量極高的患者尤其明顯。另一方面，含抗凝劑的 lithium-heparin plasma 是在不讓血液凝固的條件下分離，whole blood blood-gas potassium 則可能在較少後續處理的情況下直接測得。這三種檢體和流程**並不等價**，更不能單看同一個「K」欄位就把它們當成同一個測量。

原文實際列出：

| 同一病例、不同檢體／方法 | 報告的 K（mmol/L） | 需要先知道的前提 |
|---|---:|---|
| Serum | **6.3** | 有凝血及分離過程；患者 platelet 和 WBC 極高 |
| Lithium-heparin plasma | **4.6** | 抗凝血漿，經離心後以臨床生化儀器測量 |
| Whole blood，blood-gas analyzer | **3.4** | 動脈全血，快速測量；採檢時間、方法與 plasma 不完全相同 |

這個表讓你看到的不是「最後一個 3.4 才必然百分之百正確」，而是**不同檢體得到彼此矛盾的數字**。Serum 明顯高於 plasma 與 whole blood，與作者懷疑的偽高血鉀相符；然而 whole blood 3.4 和 plasma 4.6 之間仍有差距，不能把所有差異都定量歸因於同一個機轉，因為檢體類型、處理程序與測量方式並未完全固定。

更值得注意的是：原文的 serum free haemoglobin **0.09 g/L**，在當地提供的 0–0.25 g/L 參考範圍內。**沒有明顯 hemolysis，不代表沒有 pseudohyperkalaemia。** 血小板在凝血時釋鉀、某些脆弱白血球在運送與離心時破裂，都可能造成差異。這時 CBC 已經不是旁邊另一項不相關的檢驗；它直接參與判斷 chemistry panel 的可信度。

### 為什麼「重抽 K」不是一個完全相同的檢查？

因為下一次採檢如果改用另一種試管、延遲時間、分離條件或儀器，你同時改了**被測量的樣本**及**測量方法**。這當然可能是合乎目的的確認策略，卻不能把兩個結果的差值當作單純的時間趨勢。

這份報告記錄了可以查核的時間：第一組檢體 **08:10** 送達實驗室、**09:19** 結果報告且聯絡臨床；後續 blood-gas 用的動脈檢體 **09:34** 採樣、**09:37** 報告。原作者沒有替我們提供所有抽血之間的每一分鐘血流動力或心電圖資訊；**未報告的臨床觀察，不能由 AI 補寫成病人已做過的評估。**

研究者也回查術後多組血小板與 serum K 的時序，例如 platelet **245→1305→1392→831→450 ×10⁹/L** 時，相應檢驗日的 serum K 分別有 **4.7、6.3、6.4、5.2、4.0 mmol/L**。原文對 11 組配對值報告 Spearman ρ **0.64（P <0.05）**。這使「血小板數與 serum K 的關係」不只是一次偶然的不一致；但它仍是**單一個案的觀察**，不是讓你用 platelet 反推每位病人的真實 K，也不是診斷工具的通用敏感度或特異度。

這裡要記住的不是「板高＝鉀假」。而是**當某個檢驗值違反病人的其他資料，請先問它經過了什麼檢體處理；同一張 CBC 可能正好提供解釋 chemistry 異常的關鍵線索。**

## 第二問｜原始資料可以讓我們推論多遠？哪個證據改變了對結果的解釋？

### 另一份真實報告：血氣的 K 5.2，為什麼重抽成 4.6？

2019 年 Salvagno、Demonte、Lippi 報告的是**另一名患者**：51 歲男性，長期氣喘，因喘、喘鳴與呼吸症狀惡化就醫。這次初始採的是**靜脈血氣**，放在 3.0 mL heparinized syringe，GEM Premier 4000 測得 whole-blood **K 5.2 mmol/L**（當地此種檢體參考區間 3.5–4.5）。檢驗室當時沒有收到血氣儀器對檢體溶血的自動警示。來源：[Salvagno et al., Biochem Med 2019，全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC6366946/)。

臨床對這個結果感到意外，另一次直接靜脈採血裝入 3.5 mL lithium-heparin tube，Cobas 8000 測得 plasma **K 4.6 mmol/L**，且 hemolysis index **5（約 0.05 g/L）**。若故事停在 5.2→4.6，你依然不能完全肯定這 0.6 mmol/L 是哪個環節造成的：血液檢體、儀器與時間都有差異。

作者真正有力的下一個證據，是把**第一次 syringe 裡剩下的血液**另外轉入塑膠管離心，得到 **K 5.5 mmol/L、hemolysis index 50（約 0.5 g/L）**。原來的檢體本身確實顯示明顯的體外溶血。追查運送流程後，確認 syringe 曾**直接接觸冰塊約 15 分鐘**；作者把這個不適當的運送條件視為本案偽高血鉀的重要原因。

在這裡，真正推動判讀的不是「重抽變正常」一句話，而是三個互相補強的證據：**另一管的 K 較低；原 syringe 的 hemolysis index 高；運送時存在可辨認的傷害樣本條件。**

這仍不等於說：「以後任何 K 5.2 都不用處理。」這名病人的血鉀、檢體傷害與運送歷史，是原始研究的觀察；**病人是否有心律危險、什麼時候該監測或治療，必須由臨床狀態、ECG 與現行高鉀處置指引另外決定**。單一 case report 不能驗證標準急救的治療效果，也不能批准另一名病人等待重抽的安全性。

### 同一個病例還揭露一個更基本的錯誤：你到底抽的是靜脈血還是動脈血？

這份 2019 年的第一次檢驗是**venous** blood gas。原文報告 pO₂ **16 mmHg**、SO₂ **38%**、pCO₂ **57 mmHg**。如果只把這些數字抄進「ABG」欄位，再拿動脈氧合的標準解釋，就會製造另一個錯誤。靜脈的 pO₂／氧飽和度**不能直接取代**動脈 PaO₂／SaO₂ 或脈搏血氧去判定全身動脈氧合。

這說明一張 Lab sheet 最前面應該有一個常被忽略的問題：**這究竟是從哪裡、用什麼方法取得的資料？** 對不同 analyte，樣本位置與檢驗法的影響並不相同；沒有確認檢體身分，再多的數字計算都可能是在解釋錯誤的測量對象。

### 從原始病例回到可普遍使用的原則

真正的高鉀會危及心肌電生理，因此不能因「可能是假性高鉀」就忽略不穩定病人的處置；另一方面，沒有臨床急症證據時，也不應僅憑單一受干擾樣本就自動給可能造成低血糖及低血鉀的療法。這個安全邊界來自 [UK Kidney Association 2026 高鉀指引](https://www.ukkidney.org/health-professionals/guidelines/treatment-acute-hyperkalaemia-adults-0) 與臨床風險評估，**不是兩篇病例各自證明了何時可以等待**。

以指引的分層語言來說，**K 6.0–6.4 mmol/L 屬 moderate hyperkalaemia**；若合併 AKI、快速升鉀、不穩定或危險 ECG，急迫性及處置與穩定病人不同。ECG 正常也不是排除真性高鉀的測試。若已有危險心電變化，需要按機構流程立即救治並平行確認檢體。若選用 insulin-glucose，還必須注意**低血糖與反彈**性升鉀的監測風險。指引 [Figure 4（原 PDF p.75）](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=75) 區分心肌保護、把 K 暫時轉進細胞、實際移除 K、持續監測與預防再發；[Table 22（原 PDF p.98）](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=98) 提醒 insulin-glucose 後血糖與鉀的追蹤。**不是每名 K 6.4、ECG 正常者都自動需要同一套 IV calcium／insulin 處方**；本站不重製原圖；這些原始表圖，實際決策仍須核對本院規範和病人狀態。

## 第三問｜把兩個真實案例改一個條件，哪些過度推論會立即失效？

**「血小板高，serum K 6.3，必然是假性高鉀」？** 不對。2018 個案的幾種測值與原始處理條件支持樣本干擾；但若換成另位 AKI、服用 RAAS 抑制劑或同時存在真性鉀升高的病人，高 platelet 並不能排除兩者並存。應同時評估真正危險及分析方法，不能將 CBC 當成免治療證明。

**「採血管溶血，所以 Hb 下降是溶血性貧血」？** 不對。抽血後試管內紅血球破裂造成的 *in-vitro hemolysis*，與病人體內的 *in-vivo hemolysis* 是不同事件。後者需結合貧血變化、reticulocyte、血片、LDH、bilirubin、haptoglobin 等資料；前者的 hemolysis index 並不能代替它們。這也是原先把 K 偽高直接連到病人的 Hb 下降為何是不當的因果跳躍。

**「同一張 chemistry panel 有 Na、CO₂、Cr，是否都可直接告訴我缺水或酸中毒？」** 也不對。Na 是水與有效滲透質關係的重要訊號，並不等於總體鈉量；serum total CO₂ 主要反映 bicarbonate 卻不直接提供 pH、PaCO₂ 或代償；Cr 是腎臟清除與生成、分布在時間上共同作用的濃度，急變時單一 eGFR 估算不能當成即時 GFR。**它們測量的物理量不同，不能通通被壓縮成「腎功能不好」。** 真正要判病因、酸鹼、容量或治療風險，需依正在回答的臨床問題與新取得的資料決定。

到這裡，你已經有第一課的主要方法：**先核對檢體與分析過程，才把數值放回病人的生理；先找可能使判斷改變的證據，才討論介入。** 這不是要鼓勵忽略危急值，而是避免把一個未經查核的測量當成已確定的疾病。

## 後段合成練習｜心衰竭病房的 Lab，能否把「真 AKI」和「可能假的 K」分開？

**以下患者、檢驗表、09:00 床邊資料、telemetry 與交班全部為 AI 設計的合成教學情境；不是上述 62F 或 51M 的延伸，沒有任何真實病人的醫囑經過這段故事驗證。** 它只能用來練習推論的界線與何種資料尚須查核，不能拿它做臨床安全性的地面真相。

合成 70 歲、75 kg 男性因心衰竭鬱血接受 IV loop diuretic。原先呼吸困難改善但 JVP 與肺底濕囉音仍存在；昨天 I/O −1.4 L，清晨護理紀錄最近 8 小時尿量 240 mL 且可能漏記。四時點合成資料如下：

| 項目（單位） | 10/26 08:00 | 10/27 06:00 | 10/28 06:00 | 10/28 07:15 重新採檢 |
|---|---:|---:|---:|---:|
| Na（mmol/L） | 136 | 135 | 132 | 133 |
| K（mmol/L） | 4.4 | 4.7 | **6.3*** | 4.9 |
| Cl（mmol/L） | 102 | 101 | 99 | 100 |
| serum total CO₂（mmol/L） | 24 | 23 | 20 | 20 |
| BUN（mg/dL） | 25 | 29 | 42 | 42 |
| Creatinine（mg/dL） | 1.05 | 1.16 | 1.68 | 1.69 |
| Glucose（mg/dL） | 128 | 132 | 151 | 151 |
| Hb（g/dL） | 11.3 | 11.0 | 10.2 | 10.4 |
| WBC（/µL） | 9,100 | 10,200 | 11,800 | 11,700 |
| Platelets（/µL） | 219,000 | 211,000 | 208,000 | 209,000 |
| Mg（mg/dL） | 1.8 | 1.7 | 1.5 | 1.5 |

*假設 06:00 K 6.3 的檢體有顯著溶血，而 07:15 新管無溶血、兩次間未接受降鉀治療；本段一切皆為合成設計，不是原始病例。*

此練習中的 Cr 由 1.16→1.68–1.69，約 24 小時增加 0.52–0.53，符合 KDIGO **48 小時內增加至少 0.3 mg/dL** 的血清 creatinine AKI 診斷條件。但 **8 小時平均值不能單獨證實連續 6 小時的尿量門檻**；240 mL/8h/75kg 平均為約 0.4 mL/kg/h，仍**必須核對分時尿量**及漏記才談尿量分期。K 6.3→4.9 且原管溶血、沒有治療，支持採檢干擾；卻不能讓已成立的 Cr-AKI 跟著被判成假，也不能保證後續不再真正升鉀。這是檢體與疾病兩層不同問題。

### 09:00：不要用這段合成故事自動核准補液／利尿

**09:00 的新病例資料（全為練習假設）：**BP 112/70、四肢溫暖、神智清楚，仍有 JVP 與肺底鬱血，體重 75.6 kg→75.0 kg，觀察到一次解尿後床邊 bladder scan 殘尿約 65 mL。這些資料提高「仍有殘餘鬱血」的合理性，卻未直接量到腎臟灌流或證明 Cr 上升只因腎靜脈壓。不能僅因 Cr 上升而**反射性補 saline**，也不能因此直接決定利尿劑量或把 AKI 當成無傷害。要確定實際治療，仍缺病人連續血壓、灌流、尿量、藥物、UA/尿沉渣及必要的心臟評估。此處刻意不提供「正確醫囑」，因為不存在真病例的驗證。

以下圖表保留合成 70M 的所有值，只改一組床邊灌流資訊，比較**需要補什麼證據**，而非用來宣稱療法療效：

<figure id="lab-three-clocks" style="max-width:940px;margin:1.5rem auto">
<p><strong>兩情境共用的合成數據：</strong>06:00 K 6.3（溶血）→ 07:15 K 4.9（無溶血、未治療），Cr 1.16 → 1.69，I/O −1.4 L；240 mL／8h ≈ 0.4 mL/kg/h，分時尿量<strong>待確認</strong>。檢體安全、病人風險與 AKI 原因須<strong>並行</strong>核對。</p>
<div role="group" aria-label="合成同數據、不同灌流的判讀反事實" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:0.85rem">
<section style="border:1px solid #a3a3a3;border-radius:10px;padding:1rem">
<h3>A｜09:00 本練習假設：仍鬱血、暫無明顯低灌流</h3>
<p><strong>新資料：</strong>112/70、四肢溫暖、意識清楚、JVP 與肺底濕囉音高。</p>
<p><strong>可推論：</strong>殘餘鬱血有實際線索，不能把 Cr 自動等同缺水。</p>
<p><strong>待補證據：</strong>灌流／鬱血趨勢、藥物與尿液資料；不能在此決定固定利尿或補液處方。</p>
</section>
<section style="border:1px solid #a3a3a3;border-radius:10px;padding:1rem">
<h3>B｜只改床邊證據的反事實</h3>
<p><strong>新資料：</strong>90/55、四肢冰冷、意識惡化；JVP 與濕囉音仍高、Labs 未改變。</p>
<p><strong>可推論：</strong>殘餘鬱血與低 forward perfusion 可能同時存在，需<strong>立即升級</strong>評估休克。</p>
<p><strong>待補證據：</strong>資深醫師／重症的循環與呼吸評估；不可因水腫就加大利尿，也不可不辨機轉大量補液。</p>
</section>
</div>
<figcaption>圖 1｜本站合成練習的反事實圖；KDIGO AKI 2012 與 AHA/ACC/HFSA HF congestion/perfusion 僅提供推理背景，不是對合成病人特定醫囑的臨床驗證。</figcaption>
</figure>

### 第四筆輔助資料：Mg 與心律的問題是「還須看什麼」，不是虛構的治療結果

再假設 08:40 telemetry 出現比昨天更多的單發 PVCs，且 Mg 1.5 mg/dL。**Mg 1.5 與 PVCs** 讓你有理由檢查心律原始波形、症狀、腎功能、用藥與 K/Mg，並**評估鎂補充**與監測的安全性。Loop diuretic 可造成低鎂，但**不等於已證明**這名虛構患者的 PVCs 是低鎂單獨造成；**不能根據一個 Mg 1.5** 就自行核准 IV magnesium 劑量，因 AKI 會增加過量風險。對照 [NHS SPS](https://sps.nhs.uk/articles/treating-acute-hypomagnesaemia-in-adults/) 與 [ESC 2025 急性心衰竭心律不整共識](https://onlinelibrary.wiley.com/doi/full/10.1002/ejhf.3645/) 的適用界線，這是「下一步要查證的臨床問題」，不是已完成的處置。

其他數字也不能硬湊結論。Na 133、glucose151 不能證明缺鹽；serum total CO₂20 不等於 pH。僅以同時點 Na133、Cl100 和近似 HCO₃⁻20 可算未校正 AG：**133 − (100 + 20) = 13 mmol/L**，但這**不是另一項實測**；**沒有 albumin** 時，**不能由 AG 13** 排除高陰離子間隙或混合酸鹼問題。Hb10.2、WBC11,800 需要與出血／感染的獨立臨床資料對照，不能自動導出輸血或抗生素。

**本段只示範如何說清楚已知與未知，不應成為實際查房的處方範本。**

回到原病例，今天的交班只能用下列**合成練習的口語示例**表達尚需核實的資料，而不是讓不存在的病人為醫囑背書：

> 「練習中的 06:00 K6.3 溶血、無治療重抽4.9 較支持採檢干擾；Cr1.16→1.69 滿足肌酐 AKI，尿量 240 mL/8h 不可靠。09:00 模擬 BP112/70 且仍有 JVP 高，不憑 Cr/I-O 判定補液或利尿；08:40 模擬 PVCs 增加且 Mg 1.5，應核對節律與鎂安全邊界。哪些病因、處置與重測時點能成立，須回到真實病人和院內規範確認。」

這樣的交班真正提供區分已觀察、待確認、不能推論的格式；但它**不能證明**照這個格式說話，就已完成真實臨床決策。

## 來源與繼續深讀

核心兩份原始個案：[Šálek 2018：serum/plasma/whole-blood K 與 platelet/WBC 的真實比較](https://pmc.ncbi.nlm.nih.gov/articles/PMC5806620/)，[Salvagno et al. 2019：blood-gas 運送溶血與兩管 K 的追查](https://pmc.ncbi.nlm.nih.gov/articles/PMC6366946/)。量測及前分析限制參見 [AJKD Core Curriculum 2025](https://pubmed.ncbi.nlm.nih.gov/39396361/)；AKI 定義核對 [KDIGO 2012 原 Table 2（PDF p.22）](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf#page=22)、管理框架 [Figure 4（PDF p.28）](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf#page=28)。高鉀判讀與治療選擇需另參照 [UKKA 2026](https://www.ukkidney.org/health-professionals/guidelines/treatment-acute-hyperkalaemia-adults-0) 及實際病人的病情與當地流程；心衰合併 AKI 的 congestion/perfusion 參考 [AHA/ACC/HFSA HF guideline](https://www.jacc.org/doi/10.1016/j.jacc.2021.12.012)。沒有原始數據或合格同儕審查的治療選擇，不在本文宣稱為已驗證。

本篇的第一個核心收穫是：**如果不分清病人的生理、檢體的物理化學過程及檢驗方法，就算臨床判斷看似流暢，也可能只是在替一個不可靠的數字編故事。**

[閱讀本篇原始案例、完整來源與適用界線](../lab-morning-sheet-sources.md)。
