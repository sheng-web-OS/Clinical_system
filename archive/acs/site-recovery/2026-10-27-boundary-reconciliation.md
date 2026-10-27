# ACS 第 01、33 單元｜來源擷取矛盾與正文校正

**2026-10-27／私有研究 QA／暫不發布完整原課**。對照原站 `https://acs-deep-learning.dreamycarp4.chatgpt.site/data/units.json` 的公開可讀資料，及 2026-10-27 瀏覽器代理返回的結構化物件。後者已保存在 `2026-10-27-boundary-units-browser-capture.json`，**並非原始 JSON 位元組，不能將其 `content_complete: true` 當成保真證明**。

## 核查層級及修正

| 位置 | 瀏覽器結構化擷取 | 原站獨立讀回文字 | 判定 |
| --- | --- | --- | --- |
| Unit 01，病人胸痛，ECG 有急迫性 | 「追文字列 cTn」 | 「追序列 cTn」 | 明顯錯字；以前者作全文快照**不合格**。原站主張應理解為持續 ECG／cTn 追蹤，而不是等待檢驗才啟動緊急處理 |
| Unit 33，context.next | p.151–154 再談 STEMI 溶栓 | 「回到整堂課：從高風險辨識、初始治療、再灌流，到尚存問題與持續重評」 | **發生內容幻覺**；原課僅 150 頁，該頁結束四章。不允許將 151–154 頁記作存在 |
| Unit 33，p.149 劑量表 | 將表格改成一段括號文字，遺失獨立限制欄 | 原站有原生 table（三欄：類別／劑量範例／限制） | **教學資訊遺失**；不得以展開藥單代替原始表的劑型與條件限制 |
| Unit 33，原圖 | 只有 PPT page + caption | p.148–150 圖表頁次可見，未取得原像素 | 仍為未回收圖，圖表授權與行動條件須獨立審查 |

## Unit 01｜已能可靠回到的教學命題

站上標題由瀏覽器結構化讀回為「心肌損傷與 MI：先分開三個診斷層次」（order 1，`acs-language`）；直接 HTTP 擷取因 HTML 清洗丟失此物件的開頭，故 **ID／標題尚不具備來源 bytes 層級保真**。可由獨立讀回正文交叉核對的核心是：

症狀先提出 ischemia 假說，ECG 提供同一時點的電位與急迫性線索，cTn 反映 myocardial injury；三者不必同時陽性。急性 injury 需要 rise/fall、至少一值 >99th percentile URL；要下 MI 診斷還需要 acute ischemia 的證據。並不是每一個 cTn 升高都源於 Type 1 MI，也不是所有立即需要再灌流評估的病人都會在第一管 cTn 呈現陽性。

**臨床安全反例：** 持續缺血或臨床不穩定，合併急迫性 ECG 改變，不能以首次 cTn 尚未升高作為延緩緊急評估的理由。本文只是研究校正，不替代正式 ECG／ACS 病況與現行指引的床邊判斷。

**原圖定位：** 原課 p.5 recommendation class / level / Class III；p.6 症狀、ECG、cTn 不同證據角色。兩張圖目前只有 caption，非已發布的原圖。

## Unit 33｜已能可靠回到的教學命題

原站直接讀回完整單元的起始辨識：`id=postmi-inflammation`、order 33，title「發炎治療延伸：CRP 與臨床結局分開」，p.148–150，六個正文段落。

**要分開的兩個問題：** colchicine 可下降發炎指標，和「是否減少病人重要臨床事件」不是同一個研究終點。COLCOT （近期 MI 後 4745 人）與 CLEAR SYNERGY（近期 MI 後 7062 人）顯示不同結果；這不能由 CRP 的生物學合理性解決，也不能由一個陰性試驗推成所有慢性冠病患者都無效。

對讀：
- [2023 ESC ACS guideline §13.3.9](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)：低劑量 colchicine 屬病人／剩餘風險條件下考慮的治療；有肺炎與非 CV mortality 的安全性訊號需要對題理解。
- [2025 ACC/AHA ACS guideline §11.4](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)：**Class 2b, LOE B-R**；ACS 後低劑量 colchicine *may be reasonable*，不是每位 ACS 出院者均必須加藥，並列有嚴重腎肝功能異常與藥物交互作用禁忌。
- [COLCOT（NEJM，DOI 10.1056/NEJMoa1912388）](https://www.nejm.org/doi/10.1056/NEJMoa1912388)：複合終點的相對獲益不可誤當各組成終點皆獲益。
- [CLEAR SYNERGY（NEJM，DOI 10.1056/NEJMoa2405922）](https://www.nejm.org/doi/10.1056/NEJMoa2405922)：主要複合終點 **9.1% vs 9.3%，HR 0.99（95% CI 0.85–1.16），P=0.93**；CRP 下降不能代替 clinical benefit。

### p.149 的藥物表必須保留限制欄

| 類別 | 原站起始／劑量範例 | 原站特別限制 |
| --- | --- | --- |
| Beta-blocker | Carvedilol 3.125 mg BID；metoprolol 25 mg QD；bisoprolol 1.25 mg QD | 起始範例；**metoprolol 未交代劑型**，不能視為完整開立處方 |
| Statin | Atorvastatin 40–80 mg QD；rosuvastatin 20–40 mg QD | 看耐受及實測 LDL |
| ACE inhibitor | Ramipril 1.25 mg QD；enalapril 2.5 mg QD；captopril 6.25 mg BID | 起始範例，非所有試驗的目標量 |
| Colchicine | 0.5 mg QD | 條件性選項，需看適應對象、腎肝功能、交互作用、耐受 |

這些只是**講者原課程的劑量範例與讀法**，不是當代臨床通用 order set。不能把表格自行替換成藥物清單而抹掉限制。

## Gate 狀態（本次更新）

- [x] 01、33 均已有可辨認主題、主要正文與來源位置的**語意擷取**。
- [x] 獨立發現並記錄至少兩個有證據支持的瀏覽器擷取錯誤與一個表格扁平化。
- [x] Colchicine 核心指南等級與 CLEAR SYNERGY 主要終點已對讀正式來源。
- [ ] 33/33 原始 JSON bytes 完整取得及 hash；尚未完成，**不能標為原站全文保真**。
- [ ] 33 個單元全部圖像／ECG 原像素、150 頁原投影片／授權、interactions／accessibility、正文 guideline 逐項審查。
- [ ] 完整 ACS 長篇教材及真實 iPhone 360／390px 測試；這些未完成時不能發布 33 節本地鏡像。

本文件不新增第二份知識圖、頁面編輯系統或獨立考題索引。
