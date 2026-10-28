# U01｜證據對照、原圖核讀、醫學風險與正式發布閘門

核查日期：2026-10-28｜狀態：**DRAFT / HOLD / NOT ORDER-READY / NOT PUBLISHED**｜對應 [Issue #179](https://github.com/sheng-web-OS/Clinical_system/issues/179)、[PR #182](https://github.com/sheng-web-OS/Clinical_system/pull/182)

## 0｜內容定位和版本一致性

- **唯一候選正文**：`archive/pgy-antibiotics/u01/lesson.md`，v0.2，合成 68M、T0/T6/T48/T72。不是取自有姓名與原始時序的真實 case report，**不可**假裝為 case report。
- 附件：`oncall-card.md` 教學值班卡、`order-worked-example.md` 非可下單處方演練、`case-test.md` 未經真實考生施測的雙站 rubric。
- `archive/antibiotics-pgy/U01-urosepsis-simulation-v0.md` 為保留歷史設計情境的私有 fixture，不應同時發布成第二篇類似公開教材。與正文相同合成案例的重疊不是臨床獨立證據。
- 私人研究、內部 QA、未驗證 dosing 表和本文進度都不能當讀者正文或 metadata 公開；不得把 issue/workflow 研發資訊置入網站。
- 主文三問順序：**第零問急迫時序 → 第一問 ESBL 舊菌/empiric coverage → 第二問真正可執行的 first-dose exposure → 第三問 source control、T48 AST、療程與反事實**。不得由 ESBL 標籤直接跳 meropenem 數字醫囑。

## 1｜原始來源：對應 claim 與可稽核定位

| 關鍵論點 | 一手文件／精確定位 | 查核結果／不得越界 |
| --- | --- | --- |
| 一開始以 severity 決定急迫性，再看 resistant history、病人限制與當院 antibiogram | [IDSA 2025 cUTI §1.B](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections)，[原 Figure 1.1](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-1-figure-1.1.pdf)；[原 Table 1.1](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-1-table-1.1.pdf) | **已逐頁目視**。Figure 1.1 分 sepsis with shock、sepsis without shock、no sepsis；local antibiogram 僅適合 sepsis 分支；當院相關族群須近 12 個月；shock ≥90%、sepsis without shock ≥80% *susceptibility* 是模型導出之考量而非固定處方門檻，對本例無在地資料不得虛構 |
| 兩個月舊 ESBL 對 empiric ceftriaxone 之風險 | [IDSA cUTI 2025 Step 2](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections) | 先前 resistant urine isolates 應影響選藥；近的比遠的有用，但本次不一定相同菌。完整舊 AST 未取得，不能斷言本次 meropenem-S |
| ESBL cUTI 的本次 AST 下 preferred / alternative、口服選項 | [IDSA AMR 2026 §ESBL Q1.2](https://www.idsociety.org/practice-guideline/amr-guidance/) | TMP-SMX/FQ 在 in vitro S 時 preferred；不能把確定性感受性導回未知菌 T0；cefepime-enmetazobactam 與 cefepime 不同 |
| Piperacillin–tazobactam 適用限制與高菌量／菌血症 | [IDSA AMR 2026 Q1.4](https://www.idsociety.org/practice-guideline/amr-guidance/) | 僅非危重、無 concomitant bacteremia 的 ESBL cUTI 為 alternative；critically ill／concomitant bacteremia **不建議**；不是說所有 cUTI／非 ESBL 均禁 |
| **ESBL 酵素機轉與雙重抗藥性、MERINO 證據鏈** | [IDSA AMR 2026 §1 Overview, Q1.3–1.4](https://www.idsociety.org/practice-guideline/amr-guidance/) | ESBL 水解多數 cephalosporins、aztreonam，但本酵素通常不水解 carbapenems；可合併不同抗藥機轉而對 carbapenem 不敏感。MERINO 391 patients，30 天存活 pip-tazo **164/187 (88%)** vs meropenem **184/191 (96%)**；重新限定 MIC 標準方法者方向一致但不再達統計顯著；不得混為「所有 ESBL UTI 用 carbapenem」。 |
| 重症/低白蛋白下 meropenem vs ertapenem；菌血症可 PO 之限定 | [IDSA AMR 2026 Q1.3](https://www.idsociety.org/practice-guideline/amr-guidance/) | 鑑別危重和 hypoalbuminemia；注意 source stability、吸收及足夠血中暴露；病人非已確診 ESBL 菌血症 |
| 避免用 cefepime 單方處理 ESBL cUTI | [IDSA AMR 2026 Q1.5](https://www.idsociety.org/practice-guideline/amr-guidance/) | 即使 cefepime-S 仍不建議 ESBL cUTI；不得把 cefepime/enmetazobactam 與 cefepime 單方混為一談 |
| 2026 指南完整藥物表 | [IDSA 2026 AMR Table 1](https://www.idsociety.org/globalassets/idsa/practice-guidelines/amr-guidance/5.0/table-1.pdf) | **已逐頁目視首頁標題與 meropenem 所在頁**；原題頭限定「Assuming Normal Renal and Hepatic Function」，此案例 AKI on CKD + 體重/RRT/CrCl 不明，**禁止用該表直接指定 mg / interval / infusion**，亦不可聲稱已核當院藥典 |
| Sepsis 時效、血培、緊急源控制、β-lactam infusion | [SSC 2026](https://sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026)，Blood culture、Antimicrobial initiation、Source control、Beta-lactam antibiotics | 高度懷疑 sepsis/possible shock 不能等文化；blood cultures before first dose **if no material delay**；initial bolus then prolonged infusion maintenance 為方向，非指定病患數值；診斷 source control 目標理想 6h，非可安全延後 6h |
| Hydronephrosis + infection 之源控制 | [EAU Urolithiasis §3.4.2](https://uroweb.org/guidelines/urolithiasis/chapter/guidelines) | 強建議對 **sepsis with obstructing stones** urgent decompression（stent 或 PCN）；本合成病例只有疑似 obstruction，不能說石頭已確診。仍需 urgent urology/影像判斷 |
| 有反應的 cUTI：降階/口服/療程 | [IDSA cUTI 2025，IV→PO、Duration](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections)，[原 Figure 1.2](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-2-figure-1.2.pdf)，[原 Figure 1.3](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-3-figure-1.3..pdf) | **兩張原圖均已逐頁目視**。流程最重要的根分支是 *clinically improving vs not*；不改善先查 drug-bug mismatch / unresolved source / diagnosis，再考慮 long course。圖中 7 days 是概念總體分支，不可抹去嚴重 CKD、結構異常、完全阻塞、sepsis 等試驗 exclusion；prostatitis 疑慮可需延長 |
| **合併 Gram-negative bacteremia 的療程分支** | [IDSA cUTI 2025 §Duration, Recommendation II](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections) | 對 **clinically improving** 且接受 **effective therapy** 的 cUTI-associated GN bacteremia，另建議 **7 天而非 14 天**（conditional、low certainty）；不應把一般 cUTI 的 FQ 5–7 天規則直接當作菌血症通則。此合成病例有疑似 infected obstruction、CKD/AKI、重症，仍須依源控制、實際改善與個別風險判斷，**不是固定七天處方** |
| 無症狀導管菌尿不是自動 ESBL 治療 | [IDSA ASB 2019](https://www.idsociety.org/practice-guideline/asymptomatic-bacteriuria/) | 無症狀（非只缺尿路主訴）、穩定時一般不治；懷孕／預期黏膜創傷泌尿術前特殊處理 |

## 2｜原始圖表 vs 本課使用方式

1. **Figure 1.1**：「選擇 empiric 藥」四步與 shock/sepsis/no sepsis 三分支已目視。Table 1.1 註腳之 90/80% 是決策時可參考的 modeled thresholds，**非在這家醫院已驗證之常模**。
2. **Figure 1.2 / 1.3**：「改善→口服候選→轉換→相應療程；不改善→檢查藥菌 mismatch、感染源與診斷→是否需延長」已目視。需在敘事中先讓讀者看到 T48 血流動力與尿路減壓事實再引用原圖；不能先貼七天結論。
3. **AMR 2026 Table 1**：經逐頁目視，題頭明示 normal renal/hepatic function；本例劑量不能直抄。原圖均採官方深連結，**不擅自搬運未確認公開重製權利的 PDF 截圖**。
4. **Pocket Medicine 9E、Sanford Guide《熱病》付費來源**：**NOT_ACCESSED / NOT_VERIFIED**；不聲稱已對讀原書表、caption、footnote。此缺口須保持 publication gate，不假造頁碼或劑量。
5. **國考真題**：已獨立目視考選部 **111 年第二次醫師二階醫學（三）Q60** 原試題 PDF **p13（PDF p12–13）**、標準答案與更正答案清冊；問的是 cefotaxime、aztreonam、ertapenem 哪些會被 ESBL 水解；答案 **A（僅前兩者）**，更正清冊只有 Q6、Q29 修正，**Q60 不變**。機器解析原先符號亂碼，**由官方頁面可見的①②③取代**。這一題可確實放入正文；其他近五年對題仍須逐題核對，不能一概標完整。參考：[官方試題](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=111080&q=1&s=11&t=Q)、[官方標準答案](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=111080&q=1&s=11&t=S)、[官方更正](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=111080&q=1&s=11&t=M)。
6. **真實 case report**：目前是合成教學示例；真實案例的逐時病程、原圖和引文尚未補，不可誤稱 PubMed 連續真實病例。

## 3｜臨床風險 Hard Gate（分別判定，不能以文字品質平均分抵銷）

| 發布必檢項 | 本輪客觀結果 | 狀態 |
| --- | --- | --- |
| 低血壓/意識改變/AKI 的危急性和 early antimicrobials | T0 第一段與第零問明寫 | **AI text check PASS，尚非獨立 clinician review** |
| 舊 ESBL 的 posterior inference、不誤當本次確診或唯一選藥依據 | T0 decision 與三反例 | **AI text check PASS** |
| 2026 pip-tazo / cefepime / ertapenem 辨識 | 主文競爭表、order、test | **AI source cross-check PASS** |
| Infected obstruction → 緊急 urology source control | T0/T6 和 OSCE hard-fail | **AI text check PASS** |
| AKI / penicillin allergy / dosage / infusion / restricted approval | 所有實際 mg、interval 均 NOT_VERIFIED | **ORDER-READY BLOCKED** |
| 重要解剖與影像前提 | Hydronephrosis ≠ stone confirmed | **AI text check PASS** |
| 與撰稿者分離的獨立醫學/藥師處方 QA | **未取得可證實之另一審查者簽核** | **HOLD** |
| 四種敘事斷裂的獨立對抗性審查 | 可做多角度自查，但由同一編輯流程生成不足視作「獨立」 | **PENDING independent review** |
| 近五年官方對題與原書圖表實證 | IDSA Figures 已目視；官方 111-2 醫學（三）Q60 題幹及答案/更正已目視；Pocket/Sanford 仍缺、其餘題待查 | **PARTIAL / HOLD** |
| 網站 CI/build、實際 360/375/390px、production | 尚未執行／未取得 head-specific results | **NOT_VERIFIED** |
| 讀者使用成效 | case-test rubric 存在但無真實作答 | **NOT_TESTED** |

**裁決：本輪已實際深化主要正文與三個配套，但只可維持 Private Draft/HOLD。** 不可只因有多份文稿、AI 語意審查或 CI 綠燈，默默修改 `site/pages.json`、合併 main 或宣稱正式發布。內容可候選為公開**教育型**文章，但實際患者首劑 order-ready 屬另一層級，必須有本院 local antibiogram、藥品仿單、renal dosing/infusion/approval 與藥師正式核對。

## 4｜明確下一輪可執行的最小修復

1. 對照 [IDSA 2025 Figure 1.1](https://www.idsociety.org/globalassets/idsa/practice-guidelines/cuti/clinical-question-1-figure-1.1.pdf) 的 90/80% 適用限制；針對「低重症或沒 ESBL 過往」加第二個 full counterfactual，避免教成一律 meropenem。
2. 以**未參與撰寫**的醫學／藥師審核者，對第一劑危急性、過敏、AKI 暴露、decompression 與菌血症口服降階逐項查驗並留可稽核結果；如無法取得者明確 HOLD，不得由 AI 自評替代。
3. 111-2 醫學（三）Q60 已完成官方三份原 PDF 目視核查並寫入主文；繼續搜尋 2022–2026 其餘 ESBL／尿路感染關聯二階題，逐題核年度、梯次、科目、號、原圖與更正，未核實不加入。
4. 只有通過醫學硬閘，才開放教育版 publication candidate 註冊、CI/build、360/375/390px、HTTP production read-back、Cloudflare SHA，並依現行合併／發布授權審核。

**影響主線**：不變更每日 09:00 小麻／雙考期排程，不建立與 Issue #179 重複的週三／週日自動化。不將本稿的私人研究 metadata 放到面向讀者的文章中。
