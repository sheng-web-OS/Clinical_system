# U01｜PGY 處方演練：比較兩個方案，不把「藥物名稱」等同「已完成醫囑」

狀態：**EDUCATIONAL — NOT ORDER READY**。此病例是合成教學個案；因病人體重、藥物過敏細節、最新 CKD/AKI 動態、院內抗菌譜／核准權限、Sanford Guide 授權全文與本院腎劑量/輸注標準尚未核實，本檔**故意不捏造 mg、q-hour、infusion rate 作現實可用處方**。將缺失欄位明確標示，比填入看似精確的錯誤數字更接近安全醫囑能力。

## T0：有疑似 sepsis、兩個月前 ESBL E. coli、AKI 與阻塞風險

| 比較策略 | 何時支持 | 何時不支持／必要核對 |
|---|---|---|
| **A：Meropenem IV 作為候選 empiric agent** | 近期既往 ESBL E. coli；可能侵襲性感染、血流動力學不穩；取得適當培養後不延遲給首劑。2026 IDSA AMR 對危急侵襲性 ESBL 感染偏好 meropenem 或 imipenem 而非 ertapenem | 仍須確認嚴重 β-lactam allergy 真實反應、prior culture susceptibility、當院限制用藥、是否真的需 carbapenem、藥師對不穩定腎功能的首劑與維持劑量判定 |
| **B：Ceftriaxone IV 作為替代候選** | 一般未具高度 ESBL 風險的 cUTI 病人，可在符合症候群、當院 antibiogram、對藥物過敏與病況條件時考慮 | **本例**近期既往 ESBL + 可能重症／菌血症使 empiric inactive-therapy 風險上升；不應不看舊藥敏就套常規 CAP/UTI 路線。若本次有 susceptibility 才可重新評估 |
| **C：Piperacillin-tazobactam** | 2026 IDSA 對 ESBL-E cUTI 的部分情境列為替代，而非絕對禁止；其他 pathogen/susceptibility 與 local policy 會影響抉擇 | 不能把體外「S」直接外推到所有 ESBL 侵襲性菌血症；此例高風險第一劑須查本院菌株歷史與感染科判斷，不能等同 A |
| **D：Ertapenem** | 非危急且適合的 ESBL 感染可能作為簡化治療選項 | 不應假定危急或 hypoalbuminemia 與 meropenem 等價，還需看非發酵菌覆蓋需求 |

實際候選藥物選完後才進入 **order-check**，不可跳過：

\`\`\`text
Indication / site: suspected bacteremic complicated UTI +/- infected obstruction
Cultures sent at: [date/time] ; before/after first dose: [ ]
Suspected organisms + prior isolates/AST: [ ]
Empiric drug: [generic name]  / local restricted approval: [ ]
First dose time: [ ] ; Loading strategy: [ ]
Dose (mg or g): [SOURCE+VERSION+POPULATION PENDING]
Route: [IV] ; infusion duration: [LOCAL POLICY PENDING]
Maintenance dose / interval: [AKI + local pharmacist verification pending]
Actual weight / height: [ ] / [ ]
Baseline Cr: 1.3 ; current Cr: 2.0 mg/dL ; trend: [ ]
CrCl method + urine output + RRT status: [ ]
Allergy nature / prior beta-lactam tolerance: [ ]
Drug interactions / potassium / neurologic adverse effect: [ ]
Source-control consult & result: [ ]
Review trigger: patient worse NOW; otherwise reassess when new cultures/AST and at 48-72h
\`\`\`

**差異測試**：假設明天腎功能恢復或惡化，first dose ≠ maintenance。不能在未知體重／CrCl 的情況下擅自填一組「腎調整後標準值」，也不能因腎功能差而無條件削減初始負荷造成低暴露；實際策略須藥師與當院流程核對。

## T48：本次血＋尿培養 ESBL E. coli，ceftriaxone-R / meropenem-S / TMP-SMX-S（虛構藥敏）

**Scenario 1**：仍需升壓劑、右側 obstructed system 未減壓→不因 TMP-SMX-S 就直接口服；仍追源控制/灌流，評估活性 IV 與支持。

**Scenario 2**：已減壓、血壓穩、能吸收口服、菌血症已被評估且無其他深部感染→可在核實當次藥敏、CKD/K/interaction、本院 SOP 後考慮以 TMP-SMX 等 active oral agents 完成療程。IDSA 2026 ESBL-E cUTI 建議 susceptible 時優先 TMP-SMX / ciprofloxacin / levofloxacin，但**不能把 susceptible 當成病人已適合改 PO 的充分條件**。

**T 段落監測**：藥物毒性／K/Cr、感染灶/血流動力變化、負荷 vs 維持劑量、源控制完成日、第一天 effective therapy、若合併 prostatitis/abscess/deep infection 的額外條件。推薦療程長短以前述完整因果與 2025 IDSA 納排條件個別化，非全員自動七天。

依據：IDSA 2025 cUTI [empiric / IV-oral / duration](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections)；IDSA 2026 [ESBL Question 1.2–1.3](https://www.idsociety.org/practice-guideline/amr-guidance/)；EAU [infected obstruction](https://uroweb.org/guidelines/urolithiasis/chapter/guidelines)。未取得 Sanford 付費正文與實際院內政策前，**不可從本演練複製入真實 EMR**。
