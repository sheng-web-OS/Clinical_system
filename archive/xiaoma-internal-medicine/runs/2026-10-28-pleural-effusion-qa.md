# 2026-10-28 09:00｜胸水主線：來源、圖表、真題與發布稽核（PRIVATE）

## 2026-10-28 使用者指出「commit 後即停止」：實際 source-first 修訂，繼續驗收

- 起點：PR #188 head 93bf00ebefc3d3103dc864185fe34f36b4f52b3c；原 writer 的逐步停止由使用者截圖直接指出。本執行依使用者修正要求在**原 PR/原路徑**接手 writer 角色，未另建競爭稿。後續本執行不得自簽 independent_ai_pass。
- 原獨立退修：comment 6458991939；來源提案：comment 6459173189。已修的官方題 HOLD 句不重修；私人 Pocket 94–96/BTS/三組 Q/S/M 原頁成功證據沿用，不重跑舊失敗。
- 原始病例：El Zibaoui / Odeyemi / El Labban, Cureus 2024;16:e52986，DOI 10.7759/cureus.52986；出版社 8 頁原 PDF https://assets.cureus.com/uploads/case_report/pdf/222237/20240126-32324-1eaex2m.pdf 。本執行讀完整病例／Table 1 原文，並目視 p.3 Figure 2、p.4 Table 1；BTS supplement p.37 原流程圖亦重新查看。本次沒有重新取得私人 Pocket 原像素，不能冒稱本輪重新看過。
- **D 必要安全/來源更正**：主線移除合成74F/61M侵入性決策鏈，改56M肺炎症狀改善但積液分隔/增大的原始觀察。Day3 Table1 pH未報告；Day5 7.42為新樣本，不能倒填，也不能寫成已確診empyema。Day3 protein3.8/5.6≈0.68、LDH1254/169≈7.42是Light兩項比值，後者不是pH。pH7.29只保留為明示的獨立假想反事實；不把case report行動升格指南或EMR處方。
- **本輪另發現原文內部不一致**：Figure2B caption標Day2 post-thoracentesis，Table1標DayThree；後期換管/移管圖說也與敘事有一天標記差。本稿檢驗欄位依Table1，不自行修原文或推算精確介入間隔；不依賴這項差異建立療效因果。
- **A/B/C/D分類**：A 保留原已正確BTS pH/安全窗口/惡性及RA/pseudoexudate邊界；B 連接症狀軌與胸膜空間軌；C 真實Table1兩時點與原始樣本未知欄位是本稿新來源錨；D 移除混合合成主線、分開指南/反事實、刪公開讀者頁內部進度註記；X 不採納原病例綜述Table3的簡化Light/LDH200等作指南，不補未知數字。
- **圖像/權利**：新圖pleural-case-evidence是自行編碼的證據比較圖，非原刊/教科書圖像臨摹；原像素僅外連。Cureus原PDF載CC BY4.0；本稿以作者/刊名/DOI/原文連結署名。不公開Pocket/BTS原頁，沒有以版權不明阻止所有原創文字的自動結論。必要獨立figure語義/權利判斷仍未由writer簽PASS。
- **RED/GREEN**：新增6項來源身分/樣本時間/缺值/反事實隔離/原文差異/原有安全與官方身分回歸。原稿5FAIL+1PASS，本地修訂後6/6PASS。RED test-first commit edbc2be18429f1267058aec154fc148a3939d639；GitHub run須看真實結果，不用本地測試冒充整體CI。
- **實際接續工程**：同PR加入私人reader QA，經canonical Renderer/render_reader/CSS，用360/375/390/1280、light/dark、原病例表圖與官方連結做檢查並保留私人Actions screenshots/report。未改site/pages.json、不把archive/或dist公開；這不是正式手機或醫學審查。
- **現在尚未完成**：最新候選blob的不同脈絡逐段EPQC/臨床源證據/圖像判斷、完整CI與實際私人截圖核讀。通過後才進權限/正式部署門檻；原#188不自動改公開manifest/合併main/部署的邊界保留。任何自評、單一commit、CI綠燈、run_now都不是任務終點。

## 最新來源恢復狀態（2026-10-28；覆蓋下方 09:00 歷史阻擋判定）

- **Pocket 9E PDF p.94–96 ORIGINAL SOURCE IMAGE = VERIFIED（私人來源核讀）**。本輪從私人 ChatGPT Library 已授權原始檔成功取得原始 PDF bytes（PDF 共 **464 頁**），在私人環境以 180 dpi 實際渲染 PDF 第 94、95、96 頁並分頁目視；之前 "raw-byte materialization denied / images unavailable" 只代表先前工作階段的一次工具失敗，**不再是當下有效的 Pocket 來源阻擋**。不得把這個暫存位置、PDF bytes 或頁面影像加入 GitHub/公開網站。
- p.94：確認 PLEURAL EFFUSION 章節起點、systemic/local factors、transudates/exudates 病因列表和段落脈絡；不是獨立的決策流程圖。
- p.95：確認 **Transudative vs. Exudative Effusions** 原表為左右兩欄 **Light's Criteria / Three-Test Rule**，表格下方的 sensitive/specific 說明屬於各自欄位，不得錯配；並核對 pseudoexudate、parapneumonic/empyema 備註及 **Additional pleural fluid studies**。原表一個 Light 判準即屬陽性、兩項符合所附 Se/Sp 是特定敘述，勿將兩者混淆。
- p.96：確認原表標題 **Characteristics of Pleural Fluid (not diagnostic criteria)**；各列 WBC differential、pH、glucose 僅為典型特徵，**不可寫成診斷門檻**。同頁 Treatment 的舊式 >½ hemithorax 與 tPA/DNase 敘述仍須以 BTS 2023 等當代來源判斷。p.96 chylothorax 行為 TG >100 mg/dL，與 p.94–95 >110 mg/dL 的摘要表述不一致；標記為原書內部用值差異，不可抹平為單一 universal cutoff。
- **SOURCE ACCESS blocker = RESOLVED；POCKET IMAGE INSPECTION = VERIFIED；PUBLIC RIGHTS = NOT_VERIFIED（受版權保護，不公開重製）；MEDICAL APPROVAL = HOLD**。此為來源完整性驗證，**不是**獨立臨床醫師 peer review，也不是網站發布驗收。
- **已解的來源項**：Pocket p.94–96 原圖、BTS 2023 第 37 頁原始分支與註腳、三題官方 Q/S/M 均已核讀（見下方證據）。**仍待**：獨立醫學與教學 QA、著作權與原創圖表的可公開判定、同 HEAD semantic gate/CI、私人預覽與 360/375/390px 手機 QA。PR #188 繼續 Draft/HOLD，不更新公開 manifest、不部署。
- **恢復執行規則**：下一輪先讀本節，再檢查既有證據；同一來源同一階段已成功時禁止重試舊的 raw-byte 失敗路徑，直接處理尚未驗證的下一項。若來源又失效，須記錄新 failure 的「檔案版本/工具/時間/具體錯誤」，不能讓舊 failure 重新覆蓋成功狀態。來源可讀／醫學可採／版權可公開／工程已通過／正式已發布，必須分開記錄。


## 官方三題已核證（2026-10-28；覆蓋 09:00 的「原卷未開啟」）

- 本輪逐一打開**考選部官方試題 PDF**，實際核讀 Q45/Q48/Q49 題幹與四選項原頁，並打開其官方標準答案 **S** 及更正表 **M**；試題代號皆為 1302，原頁 PDF p.10/11/11（依 PDF 1-based 頁數，分別為 Q PDF index 10/11/11）。本輪不是僅由 archive JSON 轉述。
- **112（一）醫學（三）Q45**：原卷 `code=112020&s=11&t=Q`；S 答案 **B**，M 更正僅 Q47 一律給分，**Q45 最終 B**。
- **114（一）醫學（三）Q48**：原卷 `code=114020&s=0103&t=Q`；S 答案 **B**，M 更正 Q23 一律給分、Q42 A/D/AD，**Q48 最終 B**。
- **115（二）醫學（三）Q49**：原卷 `code=115070&s=0101&t=Q`；S 答案 **A**，M 更正 Q1/Q8/Q10/Q36/Q38/Q40，**Q49 最終 A**。
- 官方 URL 的完整 Q/S/M 連結已寫入私人草稿的來源註腳，便於下一 reviewer 重查；官方題目文字/答案身份 gate = **VERIFIED**，但選項的 **臨床推理 / current guideline applicability = AUTHOR_CHECK_ONLY，獨立醫學／教學審查仍 HOLD**。
- **後續已接續解決**：BTS 2023 原始 pleural infection decision tree 圖像與腳註也已核（見下一節）；剩下臨床分流逐條反例與獨立 QA。不得把「已核官方標準答案」推論為「整篇可發布」。

## BTS 官方流程圖已核證（2026-10-28；覆蓋 09:00 原圖 403 阻擋）

- **BTS 2023 官方原始 PDF 已從 BTS 站直接取得並目視**：[full supplement](https://www.brit-thoracic.org.uk/document-library/guidelines/pleural-disease/pleural-disease-full-supplement/)，PDF **zero-index p.44**、期刊印刷頁 **37**，原圖標題 *Suspected pleural infection, non-purulent fluid – initial decision tree*；已同頁核對分流示意圖、下方表格及 原始 **星號／† 註腳**。此前 BMJ 限制導致的 403 不再是此原圖的有效 source blocker。
- 流程本體：非膿性疑似感染 → 立即胸水 pH；pH ≤7.20 高風險；7.21–7.39 中間風險加查 LDH；pH ≥7.40 極低風險、通常不立即 ICD。中間分支原圖以 **LDH <900 / ≥900 IU/L** 畫出；同份指引敘述及表格寫 **>900 IU/L** 作考慮 ICD 的條件。稿件已避免誤稱剛好 900 IU/L 必然有單一正解。
- **星號註腳**：引流前需由 ultrasound 確認可安全接近的足夠積液。**†**：未立即 ICD 應重評 ongoing temperature、persisting inflammatory markers；**pH >7.4 且有 septations 也應考慮引流**。此註腳不能被表格中的「低風險」摘要遮蔽。
- 本次只目視核讀原圖並原創文字重述；BTS PDF/footer 明示著作權，**不得未經授權直接嵌入圖像**。**BTS ORIGINAL FLOWCHART = VERIFIED；RIGHTS TO REPRODUCE = NOT_VERIFIED；CLINICAL/EDITORIAL INDEPENDENT QA = HOLD**。
- **下一未通過的主要 gate**：由與寫作者不同的臨床／教學審查脈絡驗證整篇病例、BTS 反事實（尤其 pH ≥7.4 + septations；pH 7.3 + LDH 邊界；無安全引流窗；RA/惡性低 pH）、原圖/題目因果敘事、合法公開方式、同 HEAD semantic receipt/CI/mobile preview；仍保持 PR #188 Draft/HOLD。

## 事實基線
- 核對當次起點 main SHA：`c6225ec59127b623b0801ffc2868dd5268715473`；本次僅在獨立 draft 分支寫入新稿，不改 main、manifest 或公開目錄。
- 依 `archive/xiaoma-internal-medicine/current-plan.md` 第 10–12 節選擇 A 級胸水。main `site/pages.json` 106 項中**沒有同等深度的獨立胸水主文**；肺炎主文與 113（二）醫學（三）Q49 只觸及感染性胸水。沒有將舊文改名重發。
- 私人主稿：`archive/xiaoma-internal-medicine/drafts/2026-10-28-pleural-effusion-decision.md`。主題三層：取樣的資訊價值 → transudate/exudate 的病因分類 → infected pleural space 的 source control。含 2 病人對照、連續病例、3 組條件改變、Light 計算、pseudoexudate、pH/LDH/glucose 及救援治療、3 題歷屆題與 2 題自編遷移題。
- 沒有個人讀書進度、病人識別資訊、原書 PDF 或原始影像公開。

## 原書 Pocket Medicine 9E｜已實際取得的證據與不可逾越界線
- Library 檔：`內科_Pocket Medicine The Massachusetts General Hospital Handbook of Internal Medicine, 9th Edition_625A_Flatten.pdf`，**464 頁（本輪 pdfinfo 核實；取代前次誤記 463 頁）**，私人受版權保護資料。
- **實際閱讀 PDF 頁 94–96 的完整可抽取文字**；第 94 頁 `PLEURAL EFFUSION`：Pathophysiology / Transudates / Exudates；第 95 頁 `Initial diagnostic studies`、`Transudative vs. Exudative Effusions`（左右 `Light’s Criteria` 與 `Three-Test Rule`）、`Additional pleural fluid studies`；第 96 頁 `Treatment`。
- 第 95 頁表的文字門檻：Light 三條 >0.5、>0.6、>2/3 ULN；Three-Test Rule 胸水 cholesterol >55 mg/dL、LDH >200 U/L、cholesterol ratio >0.3；本次公開候選只採 Light 原理及**獨立教學整理**，沒有複製原表或將另一欄冒充 Light。
- 文字核讀到原書：CHF 利尿後 pseudoexudate、胸水 glucose <60 mg/dL 可能感染／腫瘤／RA、Hct ratio >50% 血胸、TG >110 mg/dL 乳糜胸、pH <7.2／glucose <60 舊式 complicated effusion 概念。
- **歷史圖像阻擋（09:00，現已解除；見頁首最新狀態）。** Files pages 模式曾回傳第 95、96 頁 image pointer，但像素渲染為 `Image unavailable`；嘗試合法 Library raw-byte materialization 被拒絕（無 authorized raw-byte path）。當時**尚未逐像素確認表框、caption、footnote、相鄰圖表與版面**；該歷史判定已被頁首本輪 180 dpi 核讀取代。原書圖像的合法公開引用／授權也未評估完成。不可將 PDF、擷取圖片或私有書檔加入網站。
- 舊書「>1 cm 一律抽」及 5–10% PTX 風險數字不可直接當現行程序規範；以 BTS 2023 的超音波安全評估與具體情境判斷為準。原書 glucose <60 與 BTS 2023 中間風險 glucose ≤4.0 mmol/L（72 mg/dL）及無 pH 時 <3.3 mmol/L 的**用途不同**，正文已分開，不能誤寫成互相矛盾或同一個通用胸管 cutoff。

## 2023 BTS 來源核查
1. BTS 2023 `Guideline for pleural disease`：https://www.brit-thoracic.org.uk/clinical-resources/guidelines/pleural-disease-full-guideline/；原文網頁可核對 pleural infection 非膿性分流：pH ≤7.2 高風險；>7.2、<7.4 中風險且 LDH >900 IU/L 時結合 glucose ≤4 mmol/L、持續發燒、積液量、CT enhancement、septation 考慮 ICD；≥7.4 低風險。原文也提醒 local anaesthetic/heparin 污染與延遲、低 pH 非感染專屬、未引流需重評。
2. BTS 2023 `Clinical Statement on pleural procedures`：https://thorax.bmj.com/content/78/Suppl_3/s43；已核對 ultrasound、慢速治療性抽液、一般單次 ≤1.5 L 與症狀停止訊號。
3. BTS `Guideline` 對 initial pleural infection drain ≤14F、殘留感染性積液的合併 tPA/DNase 與出血風險有明確建議；本稿不提供藥物院內處方。
4. **原始 BTS decision tree 圖像：尚未逐像素核對**（期刊 PDF web 截圖 403）；僅文字條款與網頁表格核對，原圖 footer 註腳另據 BTS 網頁轉錄。原創表是作者重新組織，未聲稱翻拍。

## 官方題來源（私有原卷結構化檔 ≠ 這次官方 PDF 已目視）
- 112 年第一次・醫學（三）Q45：`archive/national-exam/physician-stage2-2022-2026/structured/2023-s1-med3.json`，擷取答案 B；官方 Q: https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=112020&q=1&s=11&t=Q，S: 同 URL `t=S`，更正 `t=M`。已依擷取題幹/選項逐一推理，**官方 PDF 本次未開啟，待視覺與更正表核驗**。
- 114 年第一次・醫學（三）Q48：`.../structured/2025-s1-med3.json`，擷取答案 B；官方 `code=114020&s=0103`；同上待原卷與更正核驗。
- 115 年第二次・醫學（三）Q49：`.../structured/2026-s2-med3.json`，擷取答案 A；官方 `code=115070&s=0101`；同上待原卷與更正核驗。
- 113 年第二次・醫學（三）Q49 已有獨立正式詳解 `content/xiaoma-internal-medicine/exams/113-2-med3-q49.md`；本稿只以它作臨床前提銜接，不創建第二個同身分題目。
- 兩道 T1/T2 清楚標記自編，不偽稱官方。

## 10/27 P0 限縮核對：不是完整獨立醫學審查
- `site/pages.json` 已登錄 ACS、Sepsis、Tamponade、PE、心音主文及 29+20 題兩個獨立頁；主題各有獨立來源，**manifest 存在不代表每頁醫學 QA 或 HTTPS 可讀**。
- 讀回 29 題與新增 20 題的 `###` 題目身分並依「年度、梯次、科目、題號」正規化：29+20 = 49 個不同 canonical identities，**本次兩份間未見重複**。這不是全站歷年題目的完全去重。
- 29 題原文中 `115（二）醫學（五）Q9` 已寫明**更正 B、D、BD 均給分**，不是舊錯誤「僅 D」；但未重新打開官方更正 PDF。
- PR #169（ACS）、#166（Tamponade）、#171（49 題初稿）、#175（年度連結）已 merged；PR #172 closed/unmerged，不能把 #172 當成已合併修復證據。此處未全面檢查 Sepsis、PE 或 ACS 的所有醫學敘述與手機視覺，故 P0 = `limited audit only`。
- PGY 抗生素 U01：PR #182 在本輪開始前已 merged，main 有 `2026-10-28-urosepsis-esbl-first-dose.md`，不將 10/27 fixture 或既有 10/28 發布冒充本輪新增；院內 antibiogram／Sanford／renal dose 仍未核證，order-ready = NO。
- Cloudflare connector 讀取：production 部署 `1cd32101-7b9d-4708-94b9-8987191d3286`，commit `c6225ec59127b623b0801ffc2868dd5268715473`，status `success`；**HTTPS 本輪 Web 讀取失敗，故不聲稱完成當次 HTTP body readback**。Cloudflare project 的 `preview_deployment_setting=none`，雖有 preview 佇列紀錄，不表示草稿已成功公開。
- 這份 P0 查核**未發現上述兩項已知問題仍存在**，但不等於全站安全通過。

## 獨立 QA／工程／發布決策
- 自我臨床檢查：Light 分類≠病因；pH ≠ 動脈 pH；中間風險 pH 不可忽略 LDH/glucose/septation；膿液先引流；低 pH 需鑑別 RA/malignancy；胸管失敗需重評；原書過時抽液門檻不照抄。已完成作者側核查，**不是獨立醫師審查**。
- 因果與敘事：病例從兩人對照→抽液價值→超音波→Light→pseudoexudate→感染性積液引流→引流失敗→反事實；避免把作者 metadata 寫入正文。尚未完成獨立 EPQC 七軸盲審。
- Figure/source verification：**Pocket p.94–96 與 BTS decision tree 原圖皆 VERIFIED**；公開重製授權仍 NOT_VERIFIED，任何正式文章的新圖／表需另外做 figure/semantic release gate；考題身分/答案：**VERIFIED**（官方 Q/S/M 已核，詳頁首；逐選項醫學推論仍待獨立 QA）；獨立醫學審稿：**NOT_VERIFIED**；手機/深色模式：**NOT_VERIFIED**；CI：提交 PR 後另讀 workflow，未驗證不得填 PASS；production：**NOT_PUBLISHED**。
- 不更新 `site/pages.json` 或 `audit/figure-gate.json`，不冒用 `represented`。權利不明的原書圖不公開。

## 下一輪最小可行修復
1. **Pocket p.94–96、BTS 2023 原始 flowchart/footer、三道國考官方 Q/S/M 均已完成來源核讀**（見頁首三節）；停止重試已成功來源。聚焦獨立醫學/教學與法律權利審查，來源通過不自動解鎖發行。
2. **官方 112（一）Q45、114（一）Q48、115（二）Q49 原卷／答案／更正表已核**（詳頁首）；下一輪只需對已核選項作獨立現行臨床論證審核，113（二）Q49 保持跨頁引用、不新增重複題身分。
3. 獨立臨床/教學審稿，特別反測 pH 7.3 + LDH 高、pH ≥7.4 + septations、心衰 pseudoexudate、無安全窗口與抗凝/出血風險；視審查結果修正文稿。
4. 原圖與真題過關後才移入 `content/xiaoma-internal-medicine/lessons/`、建立公開來源頁與 figure gate、更新 manifest，完整 CI + Cloudflare production SHA + HTTPS body + 360/375/390px 驗收。

**本次付費 TinyFish：未使用；事前成本估算 US$0；實際費用 NOT_MEASURED（無付費呼叫）。**


## 後續核讀｜Pocket Medicine 9E 原頁影像驗證
- 使用者重新上傳原始 464 頁 PDF，工作容器實際取得並目視第 94–96 頁原始影像。先前 Library raw-byte 權限阻擋已解除；本段更新並取代先前『原圖不可用』狀態。
- p.94：PLEURAL EFFUSION 標題、pathophysiology、transudates/exudates 病因列表，以及 parapneumonic effusion 的 uncomplicated → fibropurulent → organization 時序已目視。
- p.95：原表 Transudative vs. Exudative Effusions（JAMA 2014;311:2422）含 Light’s Criteria 和 Three-Test Rule 兩欄。Light 任一條符合即分類為 exudate；Three-Test 為不同規則。表底分別註明 more sensitive / more specific 與各自效能，不能混為同一規則。相鄰 pseudoexudate、感染性胸水、additional pleural studies 文字已目視。
- p.96：另有 Characteristics of Pleural Fluid 表，標題明寫 not diagnostic criteria；含 WBC Diff、pH、Glc、Comments 及多種病因，不能把單一特徵當成確診或放胸管門檻。下方 Treatment 段落已目視。
- 原書表格與頁面不得直接公開重製；須原創教學表、來源註記並以現行 BTS 2023 指引判定臨床分層，不能照抄舊式 pH/glucose 或抽液門檻。
- 狀態：Pocket p.94–96 原頁視覺核讀 PASS；整體發布仍 HOLD，因 BTS 原始 decision-tree、官方原卷/更正答案、獨立醫學審查、手機與 production 驗收尚未完成。此處不冒稱完成這些關卡。


## BTS 2023 原始決策圖及註腳核證（追加）
- 已開啟 BTS 官方 full supplement: https://www.brit-thoracic.org.uk/document-library/guidelines/pleural-disease/pleural-disease-full-supplement/；官方頁面含「Suspected pleural infection, non-purulent fluid – initial decision tree」可視化流程及兩條註腳；核對 BTS guideline 正文：https://www.brit-thoracic.org.uk/clinical-resources/guidelines/pleural-disease-full-guideline/。
- pH ≤7.20：高風險，建議 ICD，但 * 註腳限定 ultrasound 有可安全進入的液體量；非任何情況一律置管。
- pH 7.21–7.39：中風險，先查 LDH；≥900 IU/L 時依積液量、glucose ≤4 mmol/L（72 mg/dL）、CT pleural enhancement、超音波 septations 等考慮 ICD；不是 LDH 單獨自動置管。
- pH ≥7.40：初步低風險，無立即 ICD 適應症；† 註腳要求持續發燒、發炎指標不退等時重評及考慮再抽液，且 pH >7.4 合併 septations 者仍應考慮引流。不能教成 pH≥7.4 永遠不引流。
- 與 Pocket p.96「Characteristics of Pleural Fluid (not diagnostic criteria)」交叉核對：病因典型值不能替代 BTS 決策圖；尤其感染性胸水引流是時間序列判斷，不是只讀一次 pH。
- 狀態：BTS decision-tree 本體及 footnotes 已核對；不公開翻印 BTS 原圖。下一個硬阻擋為三道官方真題的原卷與更正答案、獨立醫學/敘事 QA、發布後回歸驗證；仍維持 Draft/HOLD。


## 2026-10-28 獨立反例審查第一輪（與原作者稿分開的批判性審讀；非專科醫師簽核）
- 來源狀態校正：Pocket p.94–96 原頁、BTS 官方圖、112（一）Q45／114（一）Q48／115（二）Q49 官方 Q/S/M，依本 QA 前文最新核證均已 VERIFIED；前文歷史 HOLD 段落不可再當作現況。獨立醫師簽核、公開工程 gate 仍 HOLD。
- 反例 A：pH 7.29 + LDH 1200 + glucose 45 + septations + fever：原文採 BTS 中風險多因素決策，並要求安全窗口，PASS；不可由 exudate 自動推論 ICD。
- 反例 B：pH 7.45 + septations：原文表格有 BTS 註腳，PASS；但案例對照段 pH 7.45 的不引流情境必須同時明示「沒有分隔、退燒、縮小」才成立，原文已具備。
- 反例 C：pH ≤7.2 但沒有超音波安全窗口：原文已限制安全可及液體並要求專科替代策略，PASS。
- 反例 D：RA／malignancy 造成低 pH：原文已警示低 pH 非感染專屬，PASS。
- 反例 E：CHF 利尿後 pseudoexudate：原文 serum–pleural albumin gradient 1.5 >1.2，且明示不能排除雙重病因，PASS。
- 反例 F：Pleural fluid pH 採檢污染：原文已述 local anaesthetic/heparin、延遲及多 locules 差異，PASS。
- 新發現的教學風險：原文第 08 節前言仍寫『原始官方 PDF ... 尚未成功重新逐頁開啟，故 ... HOLD』，但下方三道題標題、引用段及 QA 新證據已標示核證完成，**同篇自相矛盾**。需修正文稿這一行，避免讀者誤解；不能以此宣稱已完成獨立臨床簽核。
- 原文臨床案例為明確標示的合成教學案例，不可冒稱真實 case report 或可直接照開醫囑；現有文字已標示此限制。抗生素／Lab Medicine 的 evidence-first 規則不可因本篇示例而放寬。
- 本輪屬可追溯的反例 QA，不是獨立醫師正式審查，故 gate 仍 HOLD。
