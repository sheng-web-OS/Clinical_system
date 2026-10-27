# U01｜一個發燒、低血壓、舊尿培養 ESBL 的病人：第一劑只是治療的開始

> **醫學教學 Draft v0.1（2026-10-27）；合成病例，非真實病歷，禁止當成病人專屬醫囑。** 目前未取得實際輪訓院所 antibiogram、限制用藥規則及 Sanford Guide 授權內文；具體藥物劑量／輸注時程尚不得直接照抄。延伸執行規格見 Issue #179。

## 02:10 的電話：這不是先問「哪種尿路感染要用什麼藥」

PGY 值班接到護理師來電：68 歲男性，有糖尿病、CKD G3、攝護腺肥大，住院中寒顫發燒，T 39.1°C、HR 124/min、RR 26/min、BP 92/56 mmHg，反應較平時遲鈍。右側敲擊痛，尿液有 pyuria。肌酸酐 2.0 mg/dL（約兩週前 1.3），lactate 3.8 mmol/L。尿液培養兩個月前曾有 ESBL *E. coli*，但**還沒有**這次的菌種與藥敏。床邊超音波看到右腎水腫（hydronephrosis），尚未確認造成阻塞的解剖原因。**以上數值、時序與微生物學皆為本單元人工構造，不是引自案例報告。**

首先不是「開一支常見尿路感染藥」：血壓偏低、意識改變、乳酸升高和 AKI 告訴你可能已經發生嚴重器官灌流／功能問題；疑似尿源性敗血症要迅速啟動上級／急救支援，評估 ABC、氧合、末梢灌流、尿量、容量狀態與動態血壓，並同步建立檢體與治療路徑。**單一 BP 或 lactate 數值不足以斷定已符合 Sepsis-3 septic shock 的完整定義**；反過來，未能正式完成定義也不能合理化延誤復甦、抗菌藥或源控制。SSC 2026 對 probable/definite sepsis 或 septic shock 的高風險情況建議立即抗菌治療，理想上辨認後 1 小時內；對低感染可能且無 shock 者則可在監測下暫緩。([SSC 2026](https://sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026))

血液培養宜儘早且理想上於抗菌藥之前取得；此例並行採兩套適當部位血培與尿培，記錄抗生素是否已開始，核對採檢方式及是否已有尿管。若取得檢體會顯著延遲危急病人的抗菌治療，不應硬等。CBC/DC、CMP、K、腎功能趨勢、血氣／lactate、尿量與必要影像不是「所有檢驗結果出來才給藥」的勾選表；它們用來同時確定灌流危險、合併疾病和用藥限制。

## 第二個問題：舊 ESBL 到底改變了什麼？

2025 IDSA complicated UTI（cUTI）提出依序查核四個決策維度：**(1) 嚴重度；(2) 既往尿培養／抗藥菌及抗生素暴露；(3) 過敏、交互作用等個人限制；(4) septic 情境的 local antibiogram**。順序是有目的的：嚴重病人首先要避免選到 inactive empiric therapy，但「廣越多越安全」會增加副作用、菌相與抗藥性代價。([IDSA cUTI 2025](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections))

舊 ESBL *E. coli* 不證明此次仍是同一菌株，也不表示只要培養到 *E. coli* 就永遠給 carbapenem；但是**兩個月前的高度相關 resistant isolate**，比完全沒有歷史時更會提高 empiric ceftriaxone 不涵蓋病原的擔憂。此例兼有血流動力學不穩與可能菌血症，在完整過敏與地方規範核對後，**以 meropenem 為候選的初始 IV carbapenem 策略**具有合理性；若患者危急、albumin 低或 ESBL 侵襲性感染風險高，不能想當然把較窄的 ertapenem 當成同等首選。2026 IDSA AMR Guidance 支持在危急侵襲性 ESBL 情境優先考慮 meropenem 或 imipenem，但患者實際處方仍須以本院藥敏、現行院內藥物規則及藥師核對。([IDSA AMR 2026](https://www.idsociety.org/practice-guideline/amr-guidance/))

PGY 的「開立」應是將抉擇轉成具體待核對處方：藥品、劑量、首次給藥時點、route、interval、infusion duration、loading 與 maintenance 差異、當時體重、近期腎功能趨勢、CrCl/eGFR 估算方式、透析狀態、過敏反應型態、藥物交互作用、神經毒性等不良反應及追蹤項目。這例正有**進行性 AKI**，不能只拿一次 eGFR 或一般腎功能表把首次給藥與後續維持劑量視作相同問題。**本版在院內腎劑量／Sanford 逐條核對前不提供可直接抄用的 mg、q-hour 醫囑**；詳見 [order-worked-example](order-worked-example.md)。

## 第三個問題：如果選對藥，為什麼仍可能死亡？

Hydronephrosis 加上全身性感染意味著**必須迅速釐清有無感染性尿路阻塞**：若真的有 obstructed, infected collecting system，就要即時請泌尿科評估減壓，不是等次日 rounds 或等待培養才決定。可選擇輸尿管支架或經皮腎造瘻，視臨床與解剖條件而定；若病因是結石，正式結石處置通常須等感染受控。超音波所見不直接證明必定是 stone 或支架一定最佳。([EAU Urolithiasis：3.4.2](https://uroweb.org/guidelines/urolithiasis/chapter/guidelines))

這揭露抗菌藥的極限：它有機會降低敏感菌負荷，卻不能讓受阻的集尿系統自動排空。**抗菌適當性與 source control 是兩個平行且皆必要的目標**，不能因病人退燒、SpO₂ 正常或第一劑給了就延遲處理阻塞。

## T+6h：病人更不穩定時，不能機械等待 48h

假設 BP 進一步下降、尿量減少且需要 vasopressor，並且尚未完成尿路減壓。此時立刻重新評估：是否已接受活性足夠的藥、處方是否適當給入、是否另有感染源、目前器官支持是否足夠、泌尿科是否已安排緊急解除阻塞。此時的關鍵介入可能是縮短 source-control 延誤，而不是永遠再加一支抗生素。**「48–72 小時 time-out」是穩定之後的 stewardship checkpoint，不是限制危急病人的重新評估頻率。**

## T+48h：血培與尿培真的長 ESBL *E. coli*，可以馬上換口服嗎？

本合成病例設定血、尿培養一致為 ESBL *E. coli*；假設當次 susceptibility：**ceftriaxone-R、meropenem-S、TMP-SMX-S**。這次資料比歷史培養更直接，但 susceptibility 回答的是「在檢驗條件下病原可能對哪些藥有效」，**不是**「感染灶排乾淨了、病人可以吸收口服藥、尿路通了、療程一定七天」的證明。

2026 IDSA AMR Guidance 對 ESBL pyelonephritis/cUTI 在 *in vitro* susceptible 時將 TMP-SMX、ciprofloxacin、levofloxacin 列為 preferred agents，適當情境支持從 IV 轉 oral；但真實轉換需同時確認血流動力學穩定、臨床改善、可口服吸收、感染部位／血液組織濃度、source control 與病人禁忌。若 obstruction 尚未解除、仍需升壓劑、AKI 波動或有 TMP-SMX 的 hyperkalemia／腎功能與交互作用顧慮，**不能因 lab 一個 S 就立刻轉口服**。([IDSA AMR 2026](https://www.idsociety.org/practice-guideline/amr-guidance/)、[IDSA cUTI IV-to-oral 2025](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections))

## T+72h：如果已減壓、退燒、血流動力學穩定，再問怎樣精準收尾

假設完成減壓、尿量及臨床狀態改善，能吸收口服藥、病原已確認，才具備評估 narrow/IV-to-PO、療程與出院追蹤的前提。IDSA 2025 cUTI 對有反應的病人支持較短療程，許多細菌性 cUTI 約 7 天有效治療、部分 fluoroquinolone 情境更短；療程一般從**第一天有效抗生素**計算，不是從最早任何抗生素、也不是自動從拔除或減壓日計算。**但相關研究大量排除了嚴重 sepsis、嚴重腎功能不全、尿路完全阻塞、CKD、泌尿手術等病人**，因此本例不能把「七天」硬定成通用處方；應依 source control、臨床反應、男性可能攝護腺炎與院內指引個別化。([IDSA cUTI duration 2025](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections))

## 反例：如果病人根本沒有症狀？

再想一位長期尿管患者：沒有發燒、沒有不穩定、沒有尿路症狀，僅尿培養長 *E. coli* 並伴隨 pyuria。即使菌落量高、甚至 resistant，通常也不能因此直接給抗生素；這較可能是導管相關 asymptomatic bacteriuria。例外如懷孕或預計進行某些侵入性泌尿道處置，應另依對應指引評估；不能把「不治」當成一律規則。([IDSA ASB 2019](https://www.idsociety.org/practice-guideline/asymptomatic-bacteriuria/)、[EAU urinary infections](https://uroweb.org/guidelines/urological-infections/chapter/the-guideline))

**本單元的遷移能力**：能說明為何感染源、宿主危險性、抗藥性、實際暴露劑量、解剖性 source control、當次檢驗結果與時間走勢會**共同而非互相替代**地決定處方。開始治療時不知道所有答案，是臨床現實；重要的是先處理迫切危險，讓後續證據能改變而非只是裝飾原決策。

延伸閱讀：[值班卡](oncall-card.md)｜[示範處方核對](order-worked-example.md)｜[臨床測試與評分](case-test.md)｜[來源與缺口](sources-qa.md)。
