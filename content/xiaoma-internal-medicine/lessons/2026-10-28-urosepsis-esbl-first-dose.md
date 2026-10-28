# 為何這樣選抗生素？從真實 ESBL 尿源性感染理解證據與決策

**閱讀定位｜醫學生深讀，不是藥囑指南。** 這篇文章的主要問題不再是「看到數字，當班 PGY 應該直接開什麼藥」，而是「我們從真實病人的病程、微生物學與臨床試驗，究竟可以知道什麼？」臨床藥囑需要上級醫師、藥師、當地 antibiogram/formulary/ASP 與當下病況共同驗證。本文不提供可直接複製的劑量、間隔或輸注處方；如遇真實危急病人，應立即依當院流程求援與處置，不因閱讀教材而延誤照護。

## 第一問｜真實病人發生了什麼？先看病程，而不是先選藥

一篇已發表的[尿源性敗血性休克病例報告（81 歲女性）](https://pmc.ncbi.nlm.nih.gov/articles/PMC8633641/)描述：病人有**左側輸尿管被泌尿上皮癌阻塞**的情境，發生上泌尿道感染與難治的循環衰竭；之後接受緊急**經皮腎造瘻（percutaneous nephrostomy）**，引流感染相關阻塞。報告記載，住院第 4 天回報的血液與尿液培養均為 **ESBL-producing *Escherichia coli***，團隊維持初始使用的 carbapenem 治療，病人在後續約兩週逐漸恢復，並於較後期接受腫瘤處置。

這裡先不要把病例整理成「遇到 ESBL 就開 carbapenem」的速查表。病程至少有三條不同但互相牽連的線：

- **感染線**：出現危急感染表現時，當次微生物鑑定及 AST 還沒有回來；初始治療依當下感染機率、嚴重度和既有抗藥資訊選擇，隨後再用實際培養重新評估。
- **解剖線**：被阻塞的集尿系統無法只靠抗菌藥恢復引流。這篇真實報告涉及腫瘤性阻塞及之後的 nephrostomy；它讓「抗菌治療」與「source control」的不同功能具體可見。
- **循環線**：作者也報告使用 polymyxin B hemoperfusion 與 hydrocortisone 等個別輔助治療。**這只是單一病例曾採取的措施，不能視為這些措施已被證明有效、也不能由此建議一般病人常規採用。** 其適應與療效要另查對照研究、現行 sepsis 指引及適用情境。

**這篇 case report 沒有證明：**任何同樣有 ESBL 尿培史的病人都會出現相同病原；腎造瘻與抗生素的個別療效百分比；本次病例的處置對其他患者必然最佳。病例報告是觀察材料，不是有對照組的因果試驗。原文未提供給教材的數據應標示 **NOT_REPORTED**，不能自行替病人補 Cr、lactate、MIC、劑量與完整病情細節。

另一個[已發表的 ESBL *E. coli* 腎盂腎炎合併菌血症病例](https://www.sciencedirect.com/science/article/pii/S1341321X24002897)有左腎多發膿瘍及特殊 CO₂-dependent 生長，作者記錄 meropenem 與 nephrectomy。它提醒我們微生物鑑定、感染灶與外科處置可能共同影響決策，但**特殊菌株與膿瘍不能代表一般 cUTI 病人**。這兩個病例也不可剪貼為同一位虛構病人的時間線。

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

## 反事實應用練習｜原本的 02:10 夜班情境（以下全為 AI 合成資料）

以下原稿保留為**第二層練習**，而非本文的真實病人故事。68 歲男性、所有 Cr/lactate/尿培/影像、T0/T48 時序、藥敏與選藥比較均為為了教學而設計的**合成情境**，沒有發表病例報告能證明整套數值及處置實際發生。閱讀時須把每一項治療主張退回上面列出的指引/試驗及當地專業審查，**不要把下文的「最合理做法」「先選 meropenem」等當成已驗證醫囑**。此練習尚未通過完整獨立臨床／藥學重新審查；任何供臨床使用的處方須依當院制度另行核實。

### 02:10｜在合成情境中辨認風險，而不是背一張首劑醫囑

護理師來電：「68 歲男性，糖尿病、CKD G3、BPH。發燒 39.1°C，HR 124，RR 26，BP 92/56 mmHg；平常會對答，現在反應變慢，右腰痛。能不能先開 ceftriaxone？」

兩週前 creatinine 1.3 mg/dL，現在 2.0；lactate 3.8 mmol/L，尿液 pyuria。兩個月前尿培曾長 **ESBL-producing *E. coli***，但你還沒讀到完整 susceptibility。床邊超音波見**右側 hydronephrosis**，尚不知是結石、狹窄或其他阻塞。電子病歷過敏欄只有「penicillin allergy」四字，未知當年實際反應。

此刻如果你只查「ESBL 治療首選」，你會漏掉兩個更先發生的危險：**（一）病人可能正在經歷感染相關器官功能障礙與灌流不足；（二）如果是感染性阻塞，任何抗菌藥都不能直接讓受阻的集尿系統排空。**

對這通電話，最合理的初步立場是：**高度懷疑 systemic UTI／可能菌血症，存在 sepsis 與灌流惡化的重大疑慮，必須立即同時啟動 resuscitation、cultures、合理涵蓋 ESBL 的 empiric IV therapy 評估，以及緊急 urology source-control 評估。** Meropenem 是本情境優先考慮的候選初始藥物；不是因為 ESBL 這三個字自動等於某一支藥，而是「近期相關抗藥菌＋危重程度＋可能侵襲性／菌血症＋疑似阻塞」共同改變了給錯第一劑的代價。

**尚不可宣告：**由 BP 92/56、lactate 3.8 就已完整符合 Sepsis-3 septic shock 定義；也不能把超音波 hydronephrosis 當作已證實阻塞結石。**第三個尚未確診的項目是 AKI：兩週前 Cr 1.3、現在 2.0 mg/dL（約上升 54%），但尚無近 48 小時、近 7 天的 Cr 時序與 6 小時尿量資料，尚不足以單憑兩筆數值確認 KDIGO AKI 或分期。** 這不代表腎功能沒問題，而是 CKD G3 之上高度懷疑急性惡化，須立即回查過去一週檢驗、留置尿量、容量與阻塞情況。KDIGO 2012 的一般判準為 Cr 48 小時內增加 ≥0.3 mg/dL、已知或推定 7 天內上升 ≥1.5 倍，或尿量 <0.5 mL/kg/h 持續至少 6 小時；這裡目前**無法確認時間窗**。([KDIGO AKI guideline 2012 §2.1](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf))

**同一個問題也出現在 MAP。** 依 BP 92/56 粗估 MAP 約 68 mmHg，並非已經小於 65；但一個 MAP 數字在 65 以上，**不代表灌流必定充分**，也無法排除病人正在惡化。意識變慢、乳酸升高、心搏過速及疑似感染性阻塞要求床邊連續評估。2026 SSC 一般 septic shock 的初始 MAP 目標約 65 mmHg；對 **65 歲以上**另提出 60–65 mmHg 的條件性起始範圍建議。這是治療已確認 shock 的循環支持目標，不是用來排除 sepsis 的單一診斷閾值。([SSC 2026，MAP recommendations 13–14](https://sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026))

**危急辨識與正式定義，應同時被尊重但不可互相替代。** 病人需要即時的上級、抗菌治療與源控制評估，並不要求 PGY 先把 AKI stage、septic shock 定義及結石診斷全部填完。

### 合成練習 A｜若是這名虛構病人，哪些危險不能等？

值班團隊同步分工，而非排成「等檢驗→讀藥敏→開藥→隔天找泌尿科」的序列：

1. **立即親評及求援。** 再測血壓、意識、氧合、四肢灌流、體溫、尿量；確立 IV access、監測與容量評估，通知總醫師／主治與 sepsis/急重症團隊；依循環評估開始適當 crystalloid resuscitation，對持續低灌流者評估早期 vasopressor 和 ICU。既有 CKD 不代表一律不補液；也不代表機械給固定大量輸液、不回頭評估肺水腫與反應。2026 SSC 建議 septic shock 以 norepinephrine 為首選升壓劑，一般初始 MAP 目標約 65 mmHg（65 歲以上可條件性考慮 60–65 mmHg）；細節依床邊反應、基礎高血壓與院內流程。
2. **立即採得來的血培與尿培。** 以標準無菌方式採適當血培（通常兩套）與 urine culture，標明採檢與首劑時間，並辨認尿液來源、留置導管及更換需求。理想是在第一劑前抽血培，但**採檢不能造成危急病人治療的顯著延誤**。CBC、electrolytes、K、renal trends、lactate、必要 blood gas 及相關影像同步取得；不等每一張檢驗回來才開始治療。
3. **同時開啟 first-dose 核藥與泌尿科路線。** 讀最近可用的 prior isolate/AST；確認藥物過敏到底是噁心、皮疹、即時呼吸道反應還是嚴重延遲型反應；即刻聯絡藥師與上級依本院 policy 確認 ESBL-active IV 方案、首劑時點與劑量。超音波 hydronephrosis＋ systemic infection 應緊急聯繫泌尿科，確認是否為 obstructed infected collecting system、是否需 ureteral stent 或 percutaneous nephrostomy（PCN）。

**時鐘的意義。** 2026 SSC 對 possible/probable/definite septic shock，以及 probable/definite sepsis without shock，建議立即給抗菌藥，理想上辨認後 1 小時內；對 possible sepsis without shock 可容許快速限時調查、若仍疑感染則於懷疑後 3 小時內給藥。這個病例不能被降格成低風險「再觀察幾小時」：有血流動力與器官功能惡化訊號。指南對需要 source control 的確定解剖病灶，傾向儘早處置，理想上診斷後 6 小時內；這是協作目標，不是「可以安全等滿六小時」。([SSC 2026：Blood culture、Antibiotic initiation、Source control](https://sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026))

## 合成練習 B｜哪些資料在改變抗藥的先驗風險？

**反事實練習案例為人工合成，病例為人工合成而非真實報告**；本練習尚未由醫師或藥師驗證可下單。

先把五種資訊分開：

| 問題 | 此刻掌握 | 不能從中推論 |
| --- | --- | --- |
| **Syndrome／器官狀態** | 發燒、CVA tenderness、意識改變、相對低血壓、CKD 下 Cr 上升（疑似 AKI）、乳酸上升 | 不能用 pyuria 單獨確診感染；MAP ≈68 不等於灌流正常；Cr 兩週比較尚未符合可核對 KDIGO 的時間窗；不能僅用血壓與 lactate 宣告 septic shock |
| **Anatomic source** | 右 hydronephrosis，可能 obstructed pyelonephritis | 不等於已看見結石，也不等於一定要某一種引流方式 |
| **Prior microbiology** | 兩個月前 ESBL *E. coli* | 不等於本次同一菌；不等於本次對 carbapenem 一定 S；完整 prior AST 尚需核對 |
| **Empiric coverage** | 急重症＋舊 ESBL 增加 ceftriaxone inactive 的疑慮 | 不等於所有人見 ESBL 都要 carbapenem；也不是 meropenem 涵蓋一切病原 |
| **Actual drug exposure** | CKD 合併疑似急性腎功能惡化，清除率可能變動 | 不可拿單次 eGFR 精確代表當下清除率；也不可把首劑與維持劑量混作一題 |

2025 IDSA cUTI 提供四步：**① 病況嚴重度 → ② 既往抗藥菌與抗生素暴露 → ③ 過敏、腎功能、交互作用等病人限制 → ④ 有 sepsis 時參考該院適合族群的 antibiogram。** 指引明說近期既往尿培若有 ESBL，ceftriaxone 可能不再是適當的經驗性選擇。這仍是**機率決策**，不是把歷史培養複製成這次的新培養。([IDSA cUTI 2025：Selection of Antibiotic Therapy，Figure 1.1](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections))

[IDSA 2025 cUTI 原 Table 1.1（不同嚴重度下的候選類別及註腳）](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-1-table-1.1.pdf) 提供的是進入四步篩選前的候選藥物集合，並非每一個 septic 病人都要使用列出的所有藥物；若既往 ESBL、當地抗藥率或個體禁忌不允許，應回到四步選擇，而不是照抄表格。

**原始 Figure 1.1 有兩個容易被誤解的數字。** 在有符合條件的**當院、最近 12 個月、相似病人族群** antibiogram 時，IDSA 提出可考慮讓最相關菌種對經驗性藥物的敏感性，在 septic shock 達 **≥90%**、sepsis without shock 達 **≥80%**；這是來自「經驗性處置不適當的風險」模型的參考閾值，**不是**每個病人必須機械套用的單一政策，更不代表目前這間醫院的實際 ESBL 敏感率。這位病人尚無當院資料，又有兩個月前具體的 resistant isolate，所以「以前的 AST 是否仍有預測力」及「現在對錯誤涵蓋能容忍多少風險」都必須拿出來與上級／藥師討論，而不是憑一個百分比自動給藥。([IDSA 2025 cUTI：原 Figure 1.1、Table 1.1 註腳](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-1-figure-1.1.pdf))

ESBL（extended-spectrum β-lactamase）是可使多種延伸型 cephalosporins 等 β-lactam 抗生素失效的酵素機轉。關鍵不是背「ESBL＝抗所有藥」，而是辨識：**ceftriaxone 這類原本常用於 UTI 的抗生素，在這位病人的先驗抗藥風險下，可能成為沒有足夠活性的第一劑。** 抗生素的譜必須對上病原及感染位置，不是藥名聽起來更廣就必然安全。

### 從酵素、抗生素靶點到臨床選藥：為什麼「ESBL」不是完整 AST？

先建立最基本的藥物作用路徑：**β-lactam 要接近並結合細菌的 penicillin-binding proteins（PBP），干擾細胞壁交聯，才有機會發揮殺菌作用。** 某些革蘭陰性菌的 β-lactamase 可先在周質空間水解 β-lactam ring，使藥物尚未有效到達 PBP 就失去活性。ESBL 是此類酵素中能擴大水解譜的一群，典型涵蓋 cefotaxime／ceftriaxone 等延伸型 cephalosporins 與 aztreonam；**傳統 ESBL 酵素本身一般不會水解 carbapenem，故菌株往往仍對 carbapenem 敏感。** 但「往往」不是「必然」：同一細菌可同時有其他 β-lactamases、porin 變化、efflux 等不同抗藥性機轉，導致其他抗生素失效，甚至減弱 carbapenem 活性。

同理，**TMP-SMX 或 fluoroquinolone 的作用靶點不是 β-lactam ring**，所以 ESBL 酵素本身不能直接水解它們；但攜帶 ESBL 的菌株常伴有其他抗藥基因。因此既不能看見 ESBL 就宣稱 TMP-SMX 必定 R，也不能反過來宣稱必定 S。這也解釋 **T0 先依既往菌和重症風險選能合理涵蓋的藥，T48 再以當次 AST 改變治療**，而不是把「ESBL」當成一張完整且永遠有效的 susceptibility panel。([IDSA 2026 AMR §1 開頭：酵素、co-resistance 與 susceptibility boundary](https://www.idsociety.org/practice-guideline/amr-guidance/))

**一個常被省略的機轉：為什麼 pip-tazo 體外測得 S，也不等於此例第一劑安全？** Tazobactam 透過抑制部分 β-lactamases 保護 piperacillin，但效果會受 ESBL 表現量、其他酵素（例如 OXA-1）、菌量（inoculum）、β-lactamase inhibitor 暴露與 MIC 測試重現性影響。在 ESBL 菌血症的 MERINO 隨機試驗中，piperacillin–tazobactam 組的 **30 天存活約 88%（164/187）**，meropenem 組 **96%（184/191）**；事後限制為參考方法驗證的 pip-tazo MIC 範圍，差距縮小且不再達統計顯著，但方向並未反轉。**這項結果直接支持對侵襲性 ESBL 菌血症的謹慎，不能機械推成「每一位輕症、無菌血症的 ESBL UTI 都必須使用 carbapenem」。** 2026 IDSA 對這兩群情況給出不同定位，正是臨床決策要區分的內容。([IDSA 2026 AMR §1.3–1.4：MERINO trial and susceptibility limitations](https://www.idsociety.org/practice-guideline/amr-guidance/))

### T0 的競爭方案：為什麼此例偏向 meropenem，而不是其他常見選項？

| 策略 | 在這位 68M 的意義 | 必須守住的界線 |
| --- | --- | --- |
| **Meropenem IV：此例優先討論的候選** | 危重 systemic UTI＋近期 ESBL＋可能菌血症／阻塞，初始需可靠 ESBL-active coverage；如同時有 Pseudomonas 風險，須再核其實際感受性 | 不是對所有 carbapenem-resistant 病原有效；首劑與後續劑量仍需嚴重過敏、疑似 AKI 的動態清除率、藥師與本院制度核對 |
| **Ceftriaxone IV** | 適合部分無顯著 ESBL 風險、病況與在地敏感率允許的 cUTI | 此例最近 ESBL 史強烈削弱經驗性可靠性；不應當作預設值 |
| **Piperacillin–tazobactam** | 在某些 ESBL cUTI 情境仍有角色 | **2026 IDSA AMR 明確將其 ESBL cUTI 替代定位限定於非危重且沒有 concomitant bacteremia 者；不建議用於危重或合併菌血症者。** 因此本例不應將可能「S」或一般廣譜印象視為與 meropenem 等價 |
| **Ertapenem** | 可在更穩定、病原確認與適應症吻合時，作為 carbapenem 策略之一 | 對 Pseudomonas 無可靠覆蓋；危重或低白蛋白情境下不宜未經判斷直接與 meropenem 當作同等首選 |
| **TMP-SMX / ciprofloxacin / levofloxacin** | 若**當次**體外敏感且病人條件允許，是 ESBL cUTI 合理的確定性、某些情況口服治療候選 | 現在沒有當次 AST；不能用「以後可能 S」支持危重病人 T0 冒險先開口服 |
| **Cefepime（不含 enmetazobactam）／nitrofurantoin／口服 fosfomycin** | 各自對其他 syndrome 有位置 | 2026 AMR 不建議 cefepime 單方治療 ESBL cUTI，即使體外 S；nitrofurantoin 及單劑口服 fosfomycin 不能當這種侵襲性／上泌尿道感染或菌血症首選。不要把 cefepime-enmetazobactam 和 cefepime 單方混為一談 |

注意 2026 IDSA AMR 的**精確語義**：對「確認 ESBL-E cUTI」且已證實 susceptible，TMP-SMX、ciprofloxacin、levofloxacin 屬 preferred；若因抗藥／禁忌等不能用，cefepime-enmetazobactam 或 carbapenem 屬 preferred，IV fosfomycin、aminoglycosides、piperacillin–tazobactam 屬 alternative；**piperacillin–tazobactam 在危重與伴菌血症者不建議**。在尚無 AST 的 T0，則要先用 2025 empiric 四步思考；不能拿「definitive treatment preferred」倒推當下藥敏尚未得知的第一劑。([IDSA AMR 2026：ESBL-E Questions 1.2–1.6](https://www.idsociety.org/practice-guideline/amr-guidance/))

同樣不應機械加入 vancomycin、雙重 gram-negative 或抗黴菌藥：「多蓋一點」只有在來源不確定、MRSA/Enterococcus/Pseudomonas 等特定風險或嚴重不穩定而需要不同病原譜時才有可辯護的理由；盲目堆疊會增加毒性及不必要暴露。當院 antibiogram 是在地 prior probability，不是病人當次 AST；臺灣跨院監測亦不是一間醫院單位的 antibiogram。

### 合成練習 C｜為何即使討論 meropenem，也還不能產生病人醫囑？

因為處方是**藥物種類 × 能否安全給入 × 在正確時間產生足夠的暴露**。

β-lactam 多屬 time-dependent killing，重要 PK/PD 維度是游離藥物濃度高於病原 MIC 的時間（fT>MIC）。敗血症初期體液分布與腎清除率可急速改變；負荷暴露與維持清除是兩個不同問題。**在疑似或已確認的 AKI 下簡單用低 eGFR 把第一劑一律減很低，可能讓危急的首次暴露不足；但忽略腎衰竭累積也可能增加神經毒性。** 並不存在一條「所有敗血症／所有 meropenem 都固定用同一 loading」的無條件規則。2026 SSC 對 β-lactam 建議在 initial bolus 後採 prolonged infusion 維持方案的方向，但實際 bolus、infusion duration、輸注相容性、腎調整仍須以該藥品與當院 protocol 辦理。([SSC 2026：Beta-lactam antibiotics](https://sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026))

在這份合成情境，「第一劑醫囑草案」應包含下列**待即時核對欄位**，而不是把未知資訊補成看似精確的數字：

| 醫囑欄位 | 這一例應填的推理內容 | 尚缺的病人或當地資料 |
| --- | --- | --- |
| **Indication** | Suspected severe systemic UTI / possible bacteremia with infected obstruction | 其他 source 與影像確認 |
| **Candidate agent / route** | 優先與上級／藥師核對 meropenem **IV** | prior AST、當院 formulary / restricted approval |
| **First dose timing** | 立即評估開立與執行；記錄下單、調劑、實際給入時間 | 護理給藥與流程狀態 |
| **Dose / interval / infusion** | **NOT VERIFIED，禁止從本稿直接複製** | 實際體重、目前器官支持、藥品說明書、當院 renal dosing/infusion 規範 |
| **Loading vs maintenance** | 區分早期有效暴露與隨後清除率變化；每次腎功能變化重估 | 實際 CrCl 計算法、尿量、Cr trend、RRT/CRRT、必要藥師 PK 判斷 |
| **Allergy** | 查是哪一個 penicillin、發生什麼反應、何時發生、是否曾耐受其他 β-lactams | 即時病人／家屬與給藥紀錄；如嚴重即時或嚴重延遲反應需專家決策 |
| **Monitoring** | 血壓、尿量、意識、感染源、K/renal、神經症狀、給藥成功 | 動態觀察與藥物交互作用清單 |
| **Source-control order** | 立即泌尿科評估 stent vs PCN；必要腎臟影像 | 臨床穩定度、解剖、可用介入方式 |

**特別注意過敏誤區。** 「penicillin allergy」標籤不等於每種 carbapenem 絕對禁用；反過來，沒有描述也不等於可忽略。皮疹、過敏性休克、SJS/TEN 等會導向完全不同決策。危急病人應即刻由上級、藥師／感染科共同辨認風險與可行替代，不能用等待完整過敏門診調查作為不採取任何抗菌治療的理由。

## 第三問｜病人第一劑得到了，為什麼仍可能惡化？

### T+6｜抗菌藥處理病原，卻沒有解除腎臟中的堵塞

假設病人接受初始 IV 治療後 BP 持續下降，開始需升壓劑、尿量減少，右側 hydronephrosis 仍在。即使抗菌藥對病原有活性，感染性阻塞腎盂仍可能是一個未排空、持續帶來病原與炎症刺激的感染灶。你不應把「再加一種藥」當成解除阻塞的替代品。

這時要追問：**影像是否已確認 obstructed infected system？泌尿科能否盡快以輸尿管支架或 PCN 引流？若是阻塞結石，感染控制前是否應延後 definitive stone surgery？** EAU Urolithiasis 對「sepsis with obstructing stones」強烈建議緊急減壓、於減壓後再取培養並延後最終結石處置；對本病例只能先說「高度懷疑需確認與緊急評估」，不能偷換為已確診結石。([EAU Urolithiasis：Management of sepsis and/or anuria in obstructed kidney](https://uroweb.org/guidelines/urolithiasis/chapter/guidelines))

此刻同時檢查休克支持、抗菌藥是否實際給入、有沒有另個感染源、腎功能與 drug exposure 是否快速變動。**不能等待行政性的 48–72 小時 antibiotic time-out 才處理正在惡化的病人。**

### T+48｜新的 blood / urine AST 讓我們能「縮小」，但不等於立即口服

合成培養結果：血與尿均為 ESBL *E. coli*，**ceftriaxone-R、meropenem-S、TMP-SMX-S**。新資訊確認原先 ESBL 覆蓋思考合理，也讓較窄方案成為可能；然而培養報告的「S」只回答一定測試條件下的 susceptibility，不能回答血流動力、阻塞是否解除、是否能吸收口服藥、是否另有 abscess/prostatitis，或 TMP-SMX 的鉀離子與交互作用能否接受。

**分支甲：**仍在使用 vasopressor、尿路尚未減壓、Cr 進一步上升且尿量減少，現在高度懷疑正在發展或加重 AKI。**不因 TMP-SMX-S 就立即口服轉換。** 先處理源控制與器官支持，確認 IV regimen 與實際暴露；再動態調整。

**分支乙：**T+24 已完成腎臟引流，T+48 血流動力穩、退燒、可吞與吸收，沒有未處理深層感染，已有 susceptibility，鉀離子與腎功能及交互作用評估許可。這時**可考慮改為有足夠血中／尿中／相關組織濃度的 susceptible oral agent**，例如 TMP-SMX（以個別禁忌和院內劑量為限）；菌血症**本身並非永遠不能口服**，但支持證據多來自穩定、已源控制者。（[IDSA 2025 cUTI 原 Figure 1.2：改善時才評估改口服，未改善時先排除 drug-bug mismatch／未解決 source](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-2-figure-1.2.pdf)；[完整 IV-to-oral 推薦及菌血症限制](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections)）

### T+72｜療程並非「一律 7 天」或「一定 14 天」

2025 IDSA 對有臨床反應的 cUTI、尤其有效治療後，傾向較短療程：部分 fluoroquinolone 情境約 5–7 天，非 fluoroquinolone 約 7 天；療程以**第一天 effective therapy** 起算，而非任何曾給過但對病原無效的藥。**若當次確定合併 Gram-negative bacteremia**，同一指引另對**臨床改善、已接受有效抗菌治療**者提出 **7 天而非 14 天**的**條件性**短療程建議，證據確定性為**低**；這不等於每位菌血症或阻塞性休克患者都能直接套用 7 天。若 source control 延遲、重症、CKD、完全阻塞、腎／攝護腺膿瘍、男性 acute prostatitis 疑慮或臨床反應不佳，研究適用性受到限制，需個別化。指南對可能 acute bacterial prostatitis 的男性 febrile bacteremic UTI 提及可能需要 10–14 天以上的差異評估，不能因男性就自動宣告每位都 14 天。（[IDSA 2025 cUTI 原 Figure 1.3：臨床改善與未改善須走不同分支](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-3-figure-1.3..pdf)；[Duration 推薦及納排限制](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections)）

## 反事實測試：四個改動，醫囑應如何翻轉？

**A｜只有舊 ESBL＋本次尿液白血球、但沒有感染症狀。** 一位長期 Foley 患者尿培 ESBL、pyuria 卻穩定、沒有可歸因感染的症狀或全身訊號。不是「既然 ESBL 就打 meropenem」；通常是無症狀菌尿（ASB），不需抗菌治療。懷孕或特定會造成黏膜創傷的泌尿手術前是不同適用情境。([IDSA ASB 2019](https://www.idsociety.org/practice-guideline/asymptomatic-bacteriuria/))

**B｜舊菌株其實不是 ESBL *E. coli*，而是 carbapenem-resistant *Klebsiella*。** 先前路線即失去可靠性；meropenem 不是萬能。要立刻讀完整歷史 AST／MIC，依感染風險、本院 formularies、2026 IDSA CRE 機轉分類與專家意見改選，不能硬把 ESBL 治療清單移植過去。

**C｜已證實本次為 ESBL cUTI，但不危重、無菌血症、藥敏支持。** 不再將所有病人的利益風險等同於本例；2026 IDSA AMR 對 piperacillin–tazobactam 才有特定 alternative 地位，且若有適當 susceptible oral agents，應評估更窄更方便方案。**起始 empiric、已知 pathogen 的 definitive treatment 與可以換 PO，是三次不同時點的決策。**

**D｜改成另一位 38 歲患者：只有下泌尿道症狀，生命徵象穩定、沒有發燒或 flank pain、沒有近期 resistant isolate。** 這不再是原本危重 systemic UTI：先確認是 *localized UTI*、是否真的需要培養，以及能否使用適當窄譜口服治療；**不能把原本 meropenem 路線原封不動套上去**。若沒有任何感染症狀，只是 routine urine test 有 pyuria 或 positive culture，還要回到前述 ASB 非治療分支。兩個病例一樣可能有白血球尿，真正改變經驗性抗菌藥決策的，是**感染症候群、危重性、病原風險及可用證據**；不是把兩人的尿液檢驗結果排在同一表，就期待得到同一張處方。([IDSA 2025 cUTI severity-first selection](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections))

## 真正的二階國考對題｜111 年第二次・醫學（三）第 60 題

**考點不是「有 ESBL 就開哪一支」；而是用機轉劃出抗菌藥**不能**與**仍可能**有效的邊界。**

> 考選部 111 年第二次醫師第二階段考試，醫學（三）第 60 題（代號 1302）：ESBL 能水解哪些 β-lactam 抗生素，導致它們失效？選項是 ① cefotaxime、② aztreonam、③ ertapenem；A 僅①②、B 僅①③、C 僅②③、D ①②③。**官方標準答案 A**，核對原始更正清冊後，本題**沒有更正**。

**逐選項解析：** ① **Cefotaxime 正確**——它是第三代 cephalosporin，屬典型 ESBL 可水解的延伸型 β-lactam，和本例為何不直接以 ceftriaxone 當可靠經驗性第一劑相連。② **Aztreonam 正確**——雖屬 monobactam，但「單環」不代表可逃過 ESBL 水解；不能把對某些其他 β-lactamases 的穩定性外推至 ESBL。③ **Ertapenem 錯誤**——它是 carbapenem，**典型 ESBL 酵素本身**通常不能有效水解 carbapenem；不過若同時具其他抗藥機轉，真實分離株仍可能對 ertapenem 不敏感，所以「③ 錯」不是臨床上保證 ertapenem-S。

**選項辨識：** A（①②）正確；B（①③）錯在把 carbapenem 納入典型 ESBL 水解譜、卻漏掉 aztreonam；C（②③）錯在漏掉 cefotaxime、且多選 ertapenem；D（①②③）錯在把 ESBL 與 carbapenemase 混為一談。

這題再向臨床推一步：**正確知道「ESBL 不直接水解 ertapenem」，仍不足以在本案例選 ertapenem 當第一劑。** 本例不穩定、疑似菌血症、未知 Pseudomonas 風險與 albumin/藥動狀態，和酵素能不能水解是**不同層級的問題**；這就是國考辨識題到 PGY 用藥決策之間的中介。

考選部原始來源：[111-2 醫學（三）正式試題 PDF（第 60 題，紙本第 13 頁／PDF index 12–13）](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=111080&q=1&s=11&t=Q)｜[標準答案](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=111080&q=1&s=11&t=S)｜[答案更正清冊](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=111080&q=1&s=11&t=M)。已實際目視原 PDF 的題幹與答案行，不依賴有亂碼的機器匯入題庫。

## 值班交班，用一段話而不是只交「我已開 meropenem」

「68M DM/CKD，現在 suspected severe systemic UTI with right hydronephrosis、hypotension、altered mentation、possible AKI（兩週前 Cr 1.3 → 現 2.0，需補近七天與尿量資料）/lactate elevation；兩個月前 urine ESBL *E. coli*，本次血/尿培已於 __ 採送。經與 __ 核對過敏、腎功能及本院規範，__ 時已開始 __ IV（首劑與維持劑量分開審核），目前 BP/MAP、尿量與 vasopressor 趨勢 __。已於 __ 聯絡泌尿科，疑 infected obstruction 的影像／減壓計畫 __。**任何血壓、意識、尿量惡化立即重評；有培養/AST 結果再依 source control、敏感性、臨床穩定與腎功能決定降階與口服。**」

### 自我檢驗：能不能在 90 秒答出這三問？

1. **危險與時序**：哪些證據讓你現在不能等？又有哪幾個診斷不能從單一數字斷言？
2. **First-dose decision**：為何此例偏向 meropenem IV，而不是照 UTI 慣例先用 ceftriaxone、piperacillin–tazobactam 或 ertapenem？你仍欠哪些處方安全欄位？
3. **破除過度推論**：如果已給合適藥仍低血壓、或 T48 TMP-SMX-S，為何「再加藥」與「立即改口服」都不必然是正確反應？

本文引用的指引、原始流程圖與考題官方 PDF，整理於 [證據來源與適用界線](../urosepsis-esbl-first-dose-sources.md)。值班時必須以實際病況、當院 antibiogram、藥師及上級核對結果決策；本教學無法替代實際的核藥與源控制。

> **臨床使用界線**：本篇是合成病例的醫學推理教材，不是任何臺灣院所已核准的 order-ready 處方。實際第一劑須由照護團隊即時核對病人過敏史、腎功能、體重、既往培養與本院 antibiogram／藥典／限制用藥規範，並同步進行復甦與感染源控制；不可直接將候選藥名複製成 EMR 醫囑。
