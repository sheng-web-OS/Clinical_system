# 肝膽與慢性腹瀉四篇整合教材｜原始圖表、證據及改判界線

2026-10-27 獨立 AI 整合版來源頁（**出版候選，非獨立醫師審查或發布許可**）。

## 先界定來源層級與著作權

四篇文章原文均由作者於 2026-10-26 對話提供，逐字保留在私有 `archive/xiaoma-reading/intake`；Facebook 已刊原帖 canonical 身分尚未外部核對。因此網站擬發布的**只有新撰寫並明示 AI integrated 的教材**，不把這批快照當成經核實的歷史 Facebook 原稿。

本文所提原書為 *Pocket Medicine: The Massachusetts General Hospital Handbook of Internal Medicine*, Ninth Edition。使用者 Library 內的 PDF 已實際翻閱、核讀 Figure 3-2／3-3／3-4 與 Cirrhosis 段落；相關頁數是**該 PDF viewer 的 1-based 頁次**，不是擅自標示印刷頁碼，也不推定與另一份記錄為 464 頁之 PDF 完全相同。出版社原圖僅供私人比對；公開整合稿**沒有直接重製原書圖像素，也沒有逐格描摹原圖**。所有本站圖皆為臨床推論／反證界線之自編表格。

### <span id="cholestasis">Cholestasis｜Figure 3-3</span>

原始定位：**Pocket Medicine 9E Figure 3-3, “Approach to abnormal liver tests with cholestatic pattern”**；PDF pp.137–139，主要原流程圖在 p.139。p.137 包含 abnormal liver tests 與 hepatobiliary ALP origin（GGT 等）；p.138 是 hepatocellular differential 與 Figure 3-3 標題導入，p.139 圖像呈現 ultrasound 依 ductal dilation 的分支與 intrahepatic possibilities。

最有教育增益的重新組織不是照抄 `US dilated/nondilated` 兩個箭頭，而是把兩項不等價任務 **diagnostic localization × urgency/source control** 分開；新圖一將影像證據、下一步行動與推論上限排成矩陣。「沒有擴張」改變機率，不排除阻塞；「懷疑膽管炎且不穩定」須走緊急治療，不等待完整的 elective workup。

- ACG, *Evaluation of Abnormal Liver Chemistries* (2017), [official source](https://gi.org/guideline/evaluation-of-abnormal-liver-chemistries/)：isolated ALP hepatic origin, RUQ ultrasound, PBC/PSC/DILI 等。
- ASGE, *Guideline on the management of cholangitis* (2021), [official source](https://www.asge.org/home/resources/publications/guidelines/asge-guideline-on-the-management-of-cholangitis)：cholangitis GI emergency, endoscopic drainage, ≤48h evidence time window（不穩定者要按臨床急迫性及時處置）。
- 2026-10-27 Q3 重新以**同一虛構病人的條件式證據更新**（stable febrile with nondilated US → new hypoperfusion → hypothetical CT-visible distal CBD stone → alternate extra-biliary source）書寫；虛構值班案例嚴格和真實 CT 個案分開，不能將後續治療／休克數值誣植到文獻。
- [TG18 診斷與嚴重度](https://onlinelibrary.wiley.com/doi/10.1002/jhbp.512)：A+B 是 suspected，A+B+C 才 definite；C 可以是 stone／stricture，不需要一定擴張；嚴重度與是否看到擴張也非同一向度。
- [Hong et al., *Br J Radiol* 2012, 原始全文與 Figure 1(a)(b)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3611727/)；54 歲女性原始 CT，未增強影像 distal CBD calcified stone，增強影像 common hepatic duct **not dilated** 並見 gallbladder stones。CT 選擇的回顧性研究 n=93，無擴張 n=17，有擴張 n=76；Table 4 的 ALP 約 316.47 vs 322.77 IU/L（p=0.939），bilirubin 約 4.58 vs 8.53 mg/dL（p=0.001）。**不能**將沒有顯著差異解釋為等效，不能把 17/93 當一般族群 prevalence，也不能替 54 歲女性杜撰 shock、ERCP 時點或處置結果。來源頁 © 2012 **British Institute of Radiology**，沒有查到允許直接公開再製 Figure 1 CT 像素的開放授權；正式網站僅提供可查核原文連結及**獨立製作的文字證據比較圖**，絕不放虛構 CT。
- [Sepsis-induced cholestasis 2022 open-access review](https://pmc.ncbi.nlm.nih.gov/articles/PMC9218521/)：細胞激素與 LPS 可降低 NTCP／BSEP／MRP2 等轉運，作為**非 mechanical duct obstruction** 的競爭機轉；機轉不能當單例已確診證據。
- [SSC 2026 原始指南](https://www.sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026)：先辨認需要 source control 的 anatomy；適用時及早處理、理想 ≤6h 的 **conditional very-low certainty** 一般性建議；不是任何 ALP elevation 都有膽管引流適應症。
- [ESGE 2019 CBD guideline](https://doi.org/10.1055/a-0862-0346) 與上引 ASGE 2021：急性膽管炎/敗血症病人 ERCP 的 timing 和 initial extent 視病況、感染源和耐受程度決定，不能只用任一單一時數。
- 新增 `fig-cholangitis-decision-pivot` 呈現**同一個 US 陰性結果下三次決策改判、加上其他感染源反事實出口**；`fig-cholangitis-real-ct-evidence` 分離原文 Fig1 a/b 的「stone 可見」與「duct 未擴張」，並連回原始影像。這兩個 figure 的原創構圖與來源註記不等於出版授權或作者醫學審查。
- 既有私人醫學稽核 `audit/cholestasis-20260719-pocket9e-figure3-3.md`（**非公開來源圖複製檔**）。

### <span id="infiltrative">Infiltrative ALP｜Figure 3-4</span>

原始定位：**Pocket Medicine 9E Figure 3-4, “Approach to abnormal liver tests with infiltrative pattern”**；PDF p.139；同頁四列示意 malignancy、granuloma、abscess、other／amyloid。Figure 3-4 的 `SPEP to r/o amyloid` 只可理解為提醒考慮 monoclonal proteins，**不可作為單一 SPEP 陰性足以排除 AL amyloidosis 的現行結論**。

新圖一把 ALP biochemistry、影像、病史與可反證病因分開；圖二限定不同檢驗的可推論上限。這兩圖均**不推導浸潤體積與 ALP 數值成比例**，也不把影像陰性當作 infiltrative disease 已被排除。

- ACG, [official ALP / cholestasis recommendations](https://gi.org/guideline/evaluation-of-abnormal-liver-chemistries/)。
- ASH 2026, [Guideline on diagnosis of light-chain amyloidosis](https://pmc.ncbi.nlm.nih.gov/articles/PMC13425172/)：SIFE、UIFE、serum free light chains 在懷疑 AL 時的組合與組織診斷原則；並非所有 ALP elevation 的普篩。
- 真實病例反例：[Doe-Williams et al., *Massive Hepatomegaly Secondary to Amyloidosis with Normal Liver Chemistries*](https://pmc.ncbi.nlm.nih.gov/articles/PMC7265701/), *Case Reports in Gastroenterology* 2020;14:271–278, PMID 32518538。50 歲男性肝切片**受檢部分**約 95% 為 amyloid 沉積；同時 ALP **85 IU/L**、ALT **14 IU/L**、AST **24 IU/L**、total bilirubin **0.57 mg/dL**。只能作為「局部組織受累程度不直接等於 ALP 高低」的單例反證，不能據此推估 ALP 敏感度或把 95% 說成全肝體積比例。文章中的病例圖根據這些數值獨立排版，未重製原病例照片或顯微圖。
- 既有私人稽核 `archive/xiaoma-reading/intake/2026-07-19-infiltrative-pattern-review.md`。

### <span id="diarrhea">Chronic diarrhea｜Figure 3-2</span>

原始定位：**Pocket Medicine 9E Figure 3-2, “Workup of chronic diarrhea”**。General evaluation 在 PDF p.124、functional/malabsorption/inflammatory 討論在 p.125；**Figure 3-2 圖題在 p.125 下方，實際視覺流程圖在 p.126**。流程先評估 fecal fat 和 inflammatory signals，再依情境考慮 stool osmotic gap；原圖用 `<100` 對 `≥100` 分界。

新圖一不是複製原書流程，而是呈現 **alarm features / fecal fat / inflammatory clues / watery physiology** 何者能改變檢查方向；圖二顯示原書 cutoff 與方法學灰區並非單一確診閾值。不同文獻常以 `<50`、`>100–125` 作解釋性線索；中間範圍存在不確定性，不把公式定成例行所有病人的檢驗。[下列文獻均須依其適用範圍解讀。]

- AGA 2019, [Laboratory evaluation of functional diarrhea and IBS-D](https://gastro.org/clinical-guidance/laboratory-evaluation-of-functional-diarrhea-and-diarrhea-predominant-irritable-bowel-syndrome-in-adults-ibs-d/)：immunocompetent watery diarrhea, not all chronic diarrhea with alarm features.
- BSG 2018, [Investigation of chronic diarrhoea](https://pmc.ncbi.nlm.nih.gov/articles/PMC6204957/)：microscopic colitis 的左右結腸 biopsy、bile acid diarrhea、定向檢查。
- [Sweetser 2012 case-based approach](https://pmc.ncbi.nlm.nih.gov/articles/PMC3538472/)／[Camilleri et al. 2017 physiologic review](https://pmc.ncbi.nlm.nih.gov/articles/PMC5285476/)：osmotic gap 與混合機轉的方法學限制。
- 既有私人稽核 `audit/chronic-diarrhea-2026-10-26-source-and-clinical-review.md`。

### <span id="cirrhosis">CIRRHOSIS｜原書段落／Child–Pugh／MELD</span>

原始定位：**Pocket Medicine 9E “CIRRHOSIS”**, PDF p.145 下方開始，**p.146 definition / etiologies / physical examination / laboratory studies / workup**，p.147 接 **Prognosis / Child–Pugh / MELD-Na 或 3.0**。正文確實指向一份 Appendix Child–Pugh 原表，但**該附錄在已查 Library 檔案中尚未完成直接目視核讀**。候選教材沒有複製原表的分數對照欄位；只說明變數和臨床功能，因此不得把未讀附錄錯記為「已完整核對」。

新圖一分開 structure、CSPH、function、decompensating events、prognosis；圖二對照 **有 varices 而無失代償事件** 與 **有 variceal bleeding** 的事件性分界。此圖非原書表格的版面重製。新 Baveno VIII 規範不回填冒稱 2026-07-23 作者原稿已引用。

- [Baveno VIII (2026)](https://www.journal-of-hepatology.eu/article/S0168-8278%2826%2902778-9/fulltext), especially Panels 1, 3 and 7：cACLD / CSPH diagnostic limits, first decompensation and stringent recompensation.
- [Kim et al., MELD 3.0 (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8608337/)：variables and 90-day mortality modeling.
- 既有私人稽核 `archive/xiaoma-reading/intake/2026-07-23-cirrhosis-figure-review.md`。

## 驗收未通過事項

此來源頁只完成檢索定位與 AI 審核紀錄，**不能**替代獨立醫學審查、原創圖在桌面及手機的實際閱讀理解測試，也不等於原書有版權重製授權。若未來要嵌入原書像素、改用真實個案圖或聲稱已完成 Child–Pugh Appendix 原表對讀，必須另行取得來源與合法性證據後再更新。
