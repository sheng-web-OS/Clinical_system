# BA aneurysm CBD｜原九頁 Discussion 退稿測試（RED baseline）

- 日期：2026-10-28
- 來源：2026-09《BA_aneurysm_discussion_9_slides_v2.pptx》（九頁含 Speaker Notes）、《BA_aneurysm_discussion_逐字稿.md》（完整 Slide 1–9）。兩份來自使用者歷史檔案；逐字稿已封存為私有 [frozen text fixture](fixtures/ba-aneurysm-discussion-202609-frozen.md)，Git blob SHA `afe6acddeb9d8ca5d677724635b7431100d07a68`，供後續 reviewer 在同版上比較。**這是原稿的封存副本，不等於取得原始 PPT 圖像的所有細節；本輪作者側 RED 評估不是 blinded/automated regression，也不是獨立 reviewer receipt**。
- 回饋基準：使用者轉述當時主治醫師認為「整份報告缺乏臨床推理深度，任何一點都能深入，但沒有說到重點」。不虛構正式分數、教授問答逐字紀錄。
- 關聯：[SOP](../docs/clinical-discussion-depth-sop.md)／[#203](https://github.com/sheng-web-OS/Clinical_system/issues/203)／[Draft PR #205](https://github.com/sheng-web-OS/Clinical_system/pull/205)。
- **判定身分**：作者側 adversarial editorial baseline，**NOT_INDEPENDENT**。這個檔案雖列 RED，也**不能**勾選 #203 的「獨立 reviewer 盲審」完成。

## 1｜先審選題：Question Triage FAIL

舊版 Slide 1 把問題預先切成「止血、腦脊髓液循環、長期追蹤」三個風險時鐘，隨後固定九頁，涵蓋術式、neck、支架、EVD、DSA、DCI 與追蹤。這是**良好的全貌導覽**，但沒有先回答本案最值得集中深入的 1–2 個臨床張力：選這個問題會真正影響何種決策？本案哪些證據能改判？

**反事實測試**：若把病人換成另一個 ruptured BA aneurysm，舊稿多數 Slide 仍可原封不動使用 → 案例特異性不足。這是選題品質的問題，不能只靠段落變長修復。

## 2｜Slide 2：「Why coiling」— Gate D / E：FAIL

原稿**已有**「先看是否需緊急清除大型血腫／減壓」「amenable to coiling」「保留 BA/PCA/SCA 等 branches」，不可不實批評它完全沒想到其他選項。真正缺陷是：

- 用深部解剖和 access route 說明 clipping 暴露較困難，**未把「機轉上較合理」與「有比較研究支持較好 outcome」分離**。
- 未真正比較 BA apex vs trunk、neck/branch incorporation、需不需要 adjunctive device/DAPT、手術可及性與後續治療限制如何左右兩方案；Slide 3–4 只描述 narrow/wide neck 與 BAC/SAC，未統整成臨床反事實。
- 沒有原始個案血管影像／術式紀錄支持「實際團隊因此選 coiling」；原稿自己說是 conceptual explanation，這個誠實邊界正確，但也表示它**不能被評為已完成個案式選擇論證**。

**非預告問答預期阻擋**：
- Why：如果動脈瘤將 PCA/SCA 分支納入 neck，單純 coiling 如何影響 decision？
- Evidence：後循環「通道深」與 coiling 相對 clipping 的臨床功能性結局證據是否同一類證據？
- What if：若存在造成意識惡化、需緊急清除的大型顱內血腫，原本「coiling 優先」還成立嗎？
原稿有碰到第三題，但第一、二題無足夠比較證據支撐，**原版本不應 PASS**。

## 3｜Slides 5–6：「Hydrocephalus / EVD timing」— Gate D / E：FAIL

原稿正確說明 coiling 不會清除 CSF space 的血、symptomatic hydrocephalus 需引流、EVD timing 無普遍固定公式、DAPT 增加導管出血顧慮；亦正確標明 CT hemorrhage 圖像是**其他文獻病例**。缺陷不是缺少這些標籤，而是**三種互相競爭的風險從未真正被量化或檢驗**：

- ICP ↑ → CPP 可能下降、神經學惡化；EVD 降低 CSF 壓力可能改善，但也可能增加尚未封閉瘤壁的 transmural pressure（生理假說，不可直接宣稱已證明再出血）。
- 原稿對「EVD 造成再出血」的競爭性觀察研究完全未深入處理；2017 Cagnazzo、2023 Yang meta-analysis 結果不同，為什麼不能簡單挑一篇？
- 「DAPT 前置 EVD 較合理」是風險管理思路，不能自動等同有強比較證據的普遍標準；2024 單中心研究仍有樣本與 baseline 差異。
- 缺「如果病人正快速惡化 vs 穩定、若預計 SAC/DAPT vs primary coiling」兩端臨床反事實，和本案可用事實的回扣。

**非預告問答預期阻擋**：
- Why：EVD 降 ICP 為何同時可能是收益與風險？
- Evidence：2017 EVD／再出血關聯 OR 3.92 與 2023 術前 EVD meta-analysis OR 1.60、95% CI 0.82–3.22 能否直接互相否定？哪些選擇偏差會讓它們不同？
- What if：臨床 CT 顯示急性水腦且意識惡化、動脈瘤尚未封閉，而 EVT 要數小時才可行，如何比較延遲引流與再出血顧慮？
原稿只能答「看狀況、協調」，**不能視為深入**。

## 4｜Slide 8：「Coiling 後惡化」— Gate D：FAIL

**原稿並非單純鑑別診斷清單**：它已指出大致時間窗、先評估 bedside／noncontrast CT、再視情況用 CTA/CTP/DSA，以及 angiographic vasospasm ≠ clinical DCI。應承認這些優點。

缺口在於：新 deficit 的類型與時間如何改變不同假說的相對優先序？CT 陰性後哪一個 evidence 會使 DCI、seizure、EVD blockage、metabolic/sedative cause 相對前移？DCI 的多機轉與影像狹窄不一致如何解釋？若同樣出現 vasospasm 而沒有 neurological deterioration，能推論什麼、不能推論什麼？

僅說「新惡化要找新原因」是正確結論，不等於展示推論過程。

## 5｜Reviewer calibration：舊式審稿 **FALSE NEGATIVE**

- 2026-10 事後 AI 在讀取原稿後仍先評 78/100，正面加權清晰架構、圖表與文獻，之後聽到主治回饋才下修甚至否決。
- **必須避免再發**：新 reviewer 不能根據「三個風險時鐘完整、來源有列、結論合理」判 PASS，應先提可能改判的 competing options、源頭證據衝突與 case-specific unknowns。
- 這裡的 FAIL 來自**本輪同一類 AI 重新審查**，不是外部專科主治醫師審核實驗或盲審有效性證明。

## 6｜可審計的失敗條件與當前狀態

| Gate | 舊稿現有優點 | 必須攔下的缺口 | 本輪作者側裁決 |
| --- | --- | --- | --- |
| Q：選題 | 三風險時鐘有整體性 | 未先聚焦最有改判力的臨床矛盾 | FAIL |
| D：論證 | 有概念、對象、部分條件分層 | 未充分比較 competing mechanisms、discriminator、反事實 | FAIL |
| E：EBM | 引用 AHA/ASA、SNIS、追蹤共識 | 缺原始比較證據與混雜、適用性檢驗 | FAIL |
| R：獨立審稿 | 無可核實的獨立口試證據 | 同型 AI 曾給 78 高分 | NOT_DONE |

**結論**：可證明 *作者側* 能用這份 SOP 指出舊稿深度缺口；**尚未證明獨立審稿者會自行攔下**。無任何 CI/production 的醫學驗收放行含義。

## 7｜不能用表面數量代替的後續測試

1. 以 frozen transcript blob SHA 固定文字來源；若要檢驗圖像與實際簡報表達，另讀回原始 PPT，不能以文字副本冒稱完整視覺重現。
2. 對沒有看到上面預期裁決的另一個審稿脈絡，提供原九頁、用途與原始來源；先獨立寫「最重要臨床矛盾」再給 Q/D/E/R 裁決。
3. 使用 [EVD 單題深修示範](../experiments/clinical-discussion-depth/evd-timing-deep-rewrite-20261028.md) 進行同等可用時長／同等來源之口試，使用**新的未知反事實題**，不能把本檔提供的考題直接拿來背。
4. 正文資料沒有完整個案 CT/DSA/手術記錄 → Back-to-patient gate 只能 **CONDITIONAL/UNKNOWN**，不可藉 AI 造病例讓測試變綠。
5. 記錄是否獨立攔截，及 escaped P1/每案、使用者需要修正幾次；缺分母寫 NOT_MEASURED。

## 核對來源（本次比對其摘要或全文）

- Hoh BL et al. *Stroke* 2023;54:e314–e370, §8.4（2023 AHA/ASA aSAH guideline）。https://www.ahajournals.org/doi/10.1161/STR.0000000000000436
- Cagnazzo F et al. *Acta Neurochir* 2017;159:695–704（16 篇，6,804 人；EVD related association，不能推為因果）。https://pubmed.ncbi.nlm.nih.gov/28243810/
- Yang C et al. *Clin Neurol Neurosurg* 2023;224:107563（14 篇，3,671 人；preop rebleeding pooled OR，信賴區間跨 1）。https://pubmed.ncbi.nlm.nih.gov/36580739/
- Lim YC et al. *Neurointervention* 2019;14:35–42（122 人；術前/術後 EVD）。https://pubmed.ncbi.nlm.nih.gov/30636388/
- Tang Y et al. *Front Surg* 2024;11:1403668（83 人；DAPT 與 EVD hematoma）。https://www.frontiersin.org/journals/surgery/articles/10.3389/fsurg.2024.1403668/full
