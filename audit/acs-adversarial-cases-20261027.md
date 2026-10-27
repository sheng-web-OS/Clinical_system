# ACS #169｜對抗式臨床遷移測試與來源定位

日期：2026-10-27。**此處是作者回合的對抗式測試設計及來源查核，不是與作者分離的獨立 EPQC receipt，也不是醫師同儕審查、正式發布許可或讀者學習實驗。** 本檔僅供內部審稿，絕不能編入公開教學 reader 或新建立 metadata 分類。主文：`content/clinical-os/acs.md`；PR：#169。

## 基線已發現並修正的可證缺陷

- 第一版 ACS 僅連結外部 33 單元，Clinical System 本身不具獨立可閱讀深度；已將主文擴展為病理、急診、ECG、hs-cTn、風險、再灌流、藥物、休克、MI 後併發症、國考和反例教學。**全文長度不是達標證明**。
- 章節標題改動但 `site/pages.json` 七個 `related_exams[].concept_heading` 未同步，2026-10-27 commit `7d7c5b4` 工作流程 #40501500188 重現 `Related exam concept heading missing or ambiguous`。commit `af256e4` 修補七筆，後續 #40502015186 的 editorial regression tests 已通過。最終 site build 被 `SEMANTIC_HOLD` 擋下：這是規範預期，非可繞過的失敗。
- 2026 UDMI5 之 sex-specific 99th percentile、secondary MI 的疑似／確認、MINOCA *myocardial injury* 的工作診斷角色均在本回合核對後修稿；與 113 年國考舊 Type 5 定義明確分開。
- STEMI 以外的疑似 OMI 不可不分型套用 fibrinolysis；de Winter 應加速冠脈評估，不等於一般只有 STD 患者有溶栓適應症。
- 先前前壁 LAD 單一假設病例與典型 posteromedial papillary muscle rupture 的解剖學關聯不清；已區分 inferior/lateral 梗塞和 anterior/LAD 的不同高疑病灶，不把血管定位當作排除檢查的替代。

## 必須由獨立審稿脈絡實際使用的反事實題

| 驗收 case（均為自編假設，不得混成考選部真題） | 單一關鍵條件的改變 | 應能獨立導出的決策／推論 | 若回答相反，問題是什麼 |
| --- | --- | --- | --- |
| A：55M 壓迫胸痛、首張非診斷性 ECG、首管 hs-cTn 未超 URL | 反覆胸痛＋下一張 de Winter 型態 | 優先緊急冠脈阻塞評估／通知心臟團隊；不能只等 cTn。也不能將「急評 PCI」直接等同「所有 STD 均溶栓」。 | 把 injury 時鐘當 reperfusion 時鐘；把 OMI 框架冒充通用 fibrinolysis 許可 |
| B：相同 ECG／疼痛 | 完成當地驗證的序列 hs-cTn rule-out，臨床低危險且症狀消退 | 個別化非侵入性評估／追蹤可以成立；不是所有胸痛都直接 PCI | 完全忽略後驗風險與 assay 特性 |
| C：敗血症，cTn 12→68→145 ng/L，缺局部缺血證據 | 新出現局部 ST 變化、ischemic regional wall-motion abnormality | 先辨認 ischemic MI 及原發冠脈競爭解釋；不能因感染而宣告 confirmed secondary MI，更不能把所有 cTn 上升皆當 plaque rupture | 把 biomarkers 當 etiology，忽略 UDMI5 分層診斷 |
| D：造影無 ≥50% 狹窄的疑似 MI | CMR 顯示 myocarditis pattern | 更正工作診斷 MINOCA，不能繼續當已確認冠脈 MI | 過時 MINOCA 定義及病因過度推論 |
| E：NSTE-ACS 穩定，GRACE >140／動態 ST 變化 | 轉為 refractory pain／shock | 原本 ESC <24h 早期侵入性考量，現在需要 immediate 評估，不能等「算完分數」 | 沒有依當下不穩定度升級 |
| F：3 小時 STEMI、非 PCI 中心，不能於診斷後 120min 完成 PPCI | 存在疑似主動脈剝離或出血性腦中風史 | 原本可考慮及時 fibrinolysis＋立即轉送；改變禁忌後不可溶栓，須協調替代緊急路徑 | 忘記 competing catastrophic bleed |
| G：已溶栓 STEMI | 60–90min ST resolution <50% 或持續胸痛 | Rescue PCI；若再灌流成功也須轉送，通常 2–24h angiography | 把症狀改善當治療終點 |
| H：有 AF 接受 OAC 的 ACS DES 病人 | 新診斷 LV thrombus | 加入 systemic embolic risk 的抗凝目標；不能用「延長 DAPT」代替 OAC，也不能長期無條件 triple therapy | 混淆凝血環節、支架與心室血栓 |
| I：AMI-CS、culprit 已開通但另有多支病變 | 造影 nonculprit 也有狹窄 | 不例行同期處理所有 nonculprit，除非存在需個別判斷的特殊解剖或持續危險 | 把穩定期 complete revascularization 套到 shock |
| J：Anterior/LAD STEMI 第三天新低血壓與肺水腫 | Echo 發現新 VSR，而非單純 LV stunning | 同步血流動力支持與 urgent structural intervention evaluation；若是 inferior MI＋acute severe MR，特別想到 posteromedial papillary rupture | 只看 EF、忽略破口；忽略乳突肌雙／單供血區別 |

**注意：** 本表列的是預期的臨床概念反事實，尚未有盲測讀者或獨立審稿者答題結果，故不應報稱「10/10 通過」。

## Source-to-claim 研究對照（要由下一位 reviewer 再核）

1. **2026 Fifth UDMI**：JACC, published online Aug 27 2026, DOI 10.1016/j.jacc.2026.07.025。Section 6.1：sex-specific 99th percentile cTn; Section 7.2.1/7.2.2：primary／secondary MI，對 secondary MI 的客觀確認更重視 coronary/cardiac imaging；Section 11：MINOCA 改為 *myocardial injury with non-obstructive coronary arteries*，非最終病因；Section 7.2.3：procedure-related MI 30-day context。https://www.jacc.org/doi/10.1016/j.jacc.2026.07.025
2. **2025 ACC/AHA ACS**：JACC DOI 10.1016/j.jacc.2024.11.009。Top Things #1/#2 DAPT 預設 12 months、GI-risk PPI 與 OAC PCI 後 1–4 weeks aspirin stop；#6 shock 不 routine concurrent nonculprit PCI；#7 selected microaxial pump benefit／risk；正文 §8.1 shock culprit、§5 PPCI/fibrinolysis。https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know
3. **2023 ESC ACS**：EHJ 44:3720。§5.2 high-risk NSTE <24h *consider* early invasive strategy, very-high-risk immediate; §5.3 fibrinolysis and immediate transfer if PPCI ≤120min unavailable, post-lysis ST resolution <50% at 60–90min triggers rescue PCI, successful lysis 2–24h angiography。https://academic.oup.com/eurheartj/article/44/38/3720/7243210
4. **2021 AHA mechanical complications**：Damluji et al., PMID 34126755；§Papillary muscle rupture：posteromedial typical inferior/lateral infarct with single coronary supply, anterolateral dual LAD/LCx supply；§VSD/free-wall rupture urgent echocardiography and multidisciplinary repair decision。https://pmc.ncbi.nlm.nih.gov/articles/PMC9364424/
5. **考選部考題來源與更正**：`content/xiaoma-internal-medicine/acs-exam-sources.md` 之 113（二）醫學（三）Q6、114（二）Q6/Q9、115（二）Q11-Q13；不可因 2026 新版定義回寫舊考卷行政答案。主文 `site/pages.json` 七筆 related_exams 中含 108（一）Q76 既有題，不可重複計入新增六題。

## 發布閘門（未完成不宣稱合格）

1. 與作者不同的 reviewer context 真正閱讀**當前全文版本**，逐段依 `site/semantic_gate.py` 生成 reading-unit packet，退修存在的 missing bridge，不得以同一回合自評造 `independent_ai_pass`。
2. 新版每次內容改動後，舊 receipt 失效；僅當真正完成獨立審查時按 `docs/editorial-semantic-release-gate.md` 更新 `audit/editorial-semantic-reviews.json`。禁止更新 `audit/editorial-semantic-baseline.json` 來豁免。
3. 真正跑 `tools/validate.py`、`tools/build_site.sh` 與最新 HEAD CI；檢查七個 exam anchor、來源链接和四章入口；用 360/375/390px 真實瀏覽器檢查 ACS 專屬長表與標題閱讀，而不是以 Sepsis 全站共用檢查冒充。
4. 原教材 150 頁 PPT/ECG 原圖及互動未回收或未確認權利，若要採用必須完成來源與使用權核對；不拷貝未驗證圖像進公網。
5. 未有 #169 針對性發布核准不得 merge/main/production；即使全部 QA 通過，仍將可核驗 HEAD/CI/真正醫學審查供 L2 核准。

**下一輪不是重述這份 TODO，而是獨立 reviewer 找到具體退修段落後實際提交修正，重審新 blob，再跑發布 gate。**
