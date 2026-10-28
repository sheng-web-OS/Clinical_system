# 2026-10-28 09:00｜胸水主線：來源、圖表、真題與發布稽核（PRIVATE）

## 事實基線
- 核對當次起點 main SHA：`c6225ec59127b623b0801ffc2868dd5268715473`；本次僅在獨立 draft 分支寫入新稿，不改 main、manifest 或公開目錄。
- 依 `archive/xiaoma-internal-medicine/current-plan.md` 第 10–12 節選擇 A 級胸水。main `site/pages.json` 106 項中**沒有同等深度的獨立胸水主文**；肺炎主文與 113（二）醫學（三）Q49 只觸及感染性胸水。沒有將舊文改名重發。
- 私人主稿：`archive/xiaoma-internal-medicine/drafts/2026-10-28-pleural-effusion-decision.md`。主題三層：取樣的資訊價值 → transudate/exudate 的病因分類 → infected pleural space 的 source control。含 2 病人對照、連續病例、3 組條件改變、Light 計算、pseudoexudate、pH/LDH/glucose 及救援治療、3 題歷屆題與 2 題自編遷移題。
- 沒有個人讀書進度、病人識別資訊、原書 PDF 或原始影像公開。

## 原書 Pocket Medicine 9E｜已實際取得的證據與不可逾越界線
- Library 檔：`內科_Pocket Medicine The Massachusetts General Hospital Handbook of Internal Medicine, 9th Edition_625A_Flatten.pdf`，463 頁，**私人受版權保護資料**。
- **實際閱讀 PDF 頁 94–96 的完整可抽取文字**；第 94 頁 `PLEURAL EFFUSION`：Pathophysiology / Transudates / Exudates；第 95 頁 `Initial diagnostic studies`、`Transudative vs. Exudative Effusions`（左右 `Light’s Criteria` 與 `Three-Test Rule`）、`Additional pleural fluid studies`；第 96 頁 `Treatment`。
- 第 95 頁表的文字門檻：Light 三條 >0.5、>0.6、>2/3 ULN；Three-Test Rule 胸水 cholesterol >55 mg/dL、LDH >200 U/L、cholesterol ratio >0.3；本次公開候選只採 Light 原理及**獨立教學整理**，沒有複製原表或將另一欄冒充 Light。
- 文字核讀到原書：CHF 利尿後 pseudoexudate、胸水 glucose <60 mg/dL 可能感染／腫瘤／RA、Hct ratio >50% 血胸、TG >110 mg/dL 乳糜胸、pH <7.2／glucose <60 舊式 complicated effusion 概念。
- **圖像硬門檻：未通過。** Files pages 模式曾回傳第 95、96 頁 image pointer，但像素渲染為 `Image unavailable`；嘗試合法 Library raw-byte materialization 被拒絕（無 authorized raw-byte path）。因此**沒有逐像素確認表框、caption、footnote、相鄰圖表與版面**；不把文字提取冒稱目視原表。原書圖像的合法公開引用／授權也未評估完成。不可將 PDF、擷取圖片或私有書檔加入網站。
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
- Figure gate：**HOLD**（Pocket 原表視覺與 caption/footnote 未完成；BTS decision tree 原像素未核對）；考題：**HOLD**（官方原卷/更正本輪未核實）；獨立醫學審稿：**NOT_VERIFIED**；手機/深色模式：**NOT_VERIFIED**；CI：提交 PR 後另讀 workflow，未驗證不得填 PASS；production：**NOT_PUBLISHED**。
- 不更新 `site/pages.json` 或 `audit/figure-gate.json`，不冒用 `represented`。權利不明的原書圖不公開。

## 下一輪最小可行修復
1. 以有授權、能真正顯示像素的 PDF 讀取方式目視第 94–96 頁，逐欄核 Light/Three-Test/Additional studies/Treatment，寫明 footnote 與原表引用邊界；若權限持續阻擋則保持 HOLD，不能換成裝飾圖湊數。
2. 取得官方 112（一）Q45、114（一）Q48、115（二）Q49 的原卷及正式更正表影像，逐題確認身分、答案、選項與頁次；對已存在 113（二）Q49 只做跨頁引用。
3. 獨立臨床/教學審稿，特別反測 pH 7.3 + LDH 高、pH ≥7.4 + septations、心衰 pseudoexudate、無安全窗口與抗凝/出血風險；視審查結果修正文稿。
4. 原圖與真題過關後才移入 `content/xiaoma-internal-medicine/lessons/`、建立公開來源頁與 figure gate、更新 manifest，完整 CI + Cloudflare production SHA + HTTPS body + 360/375/390px 驗收。

**本次付費 TinyFish：未使用；事前成本估算 US$0；實際費用 NOT_MEASURED（無付費呼叫）。**
