# U01｜Evidence-first 來源核對及發布 HOLD（2026-10-28）

**範圍**：PR #189 的真實病例與療效研究；不是具資格醫師／藥師審核或正式發布收據。

## 真實病例與對照研究：來源、可用結論及限制

| Source | 可核實觀察 | 不可外推 |
|---|---|---|
| [Evins 2021 原始 Case / Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC8147929/) | 28F、初診 BP 83/44、HR117；初用 ceftriaxone；day 3 urine ESBL-positive XDR E. coli，ceftriaxone MIC >64 R、meropenem <0.25 S、pip-tazo 64 I、TMP-SMX >320 R；day 4 改善，day 5 出院接居家 IV，總計 10 天 carbapenem | 不是所有 cUTI 的 10 天固定療程。沒有「兩個月前舊尿培 ESBL」紀錄；個人臨床改善不能當作 meropenem 獨立療效的隨機對照 |
| [81F tumor obstruction case](https://pmc.ncbi.nlm.nih.gov/articles/PMC8633641/) | 目前公開摘要可核：泌尿上皮癌致左輸尿管阻塞、ESBL E. coli 尿源性敗血性休克、PMX hemoperfusion／hydrocortisone、後續 percutaneous nephrostomy | 只有摘要層級與部分可見內文核對；逐項原始 lab、AST、時間、劑量仍 NOT_FULL_VERIFIED。PMX 與 hydrocortisone 個案使用不能推論標準效果 |
| [MERINO 2018 JAMA RCT](https://pmc.ncbi.nlm.nih.gov/articles/PMC6143100/) | Ceftriaxone-resistant E. coli / K. pneumoniae 菌血症 definitive therapy；30d deaths pip-tazo 23/187（12.3%） vs meropenem 7/191（3.7%），absolute difference 8.6 percentage points；沒有達成非劣性 | 不是未知病原首劑或所有輕症 cUTI 的 RCT；研究不是每株皆經基因確認 ESBL。事後 MIC 次群不顯著並不證明等效 |
| [IDSA 2025 cUTI](https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections) | Empiric 依 severity、prior culture/exposure、patient restrictions、適用且近期的本院 antibiogram 進行四步評估 | 無法由美國指引推得單間臺灣醫院抗藥率、院內藥典或病人級處方 |
| [IDSA 2026 AMR](https://www.idsociety.org/practice-guideline/amr-guidance/) | 指引區分已知 ESBL-E cUTI susceptibility、危重／菌血症、與未知 AST 的 empiric decisions | 不是可直接照抄 loading、dose、interval 或 infusion 的本地醫囑 |
| [SSC 2026](https://sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026) | 感染嚴重程度、快速抗菌治療、必要時及時 source control 的條件性建議 | 理想 source control 六小時不是可以安全等滿六小時；不能由單一案例支持輔助裝置療效 |

## 修正的結構性缺陷

原讀者稿雖然標記合成，卻以合成 68M 的 first-dose、T+6/T+48/T+72、藥物選擇表、醫囑草案及交班填空占據大部分正文；這種篇幅與命令語氣會讓醫學生誤以為模型已驗證正確臨床處置。本次已把公開主文轉為真實病例 → ESBL / MIC / AST 機轉 → MERINO 主要比較結果 → 指引條件 → 短篇證據缺口反事實，沒有讓合成病例成為臨床醫囑的權威。原模擬研究資產另保留在私有 archive。

## 尚未完成，維持 HOLD
- [ ] 81F case report 原文全部時點、檢驗及註腳核對。
- [ ] 獨立具資格臨床醫師／藥師核對高風險處置主張；獨立語義與來源 QA。
- [ ] 官方 111-2 醫學（三）Q60 與更正答案本輪重新核驗及圖片／原表使用權利。
- [ ] Exact PR HEAD 的 CI 和 source/figure/phone 360/375/390 閘門。
- [ ] 合併及正式部署需要另外核准，之後核對 production SHA 與 HTTPS。

**先前 CI 顯示 SEMANTIC_HOLD review stale after a content change 是保護用的有效阻擋，不應為求綠燈複製自評或偽造臨床簽核。**
