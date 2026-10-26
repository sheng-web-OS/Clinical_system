# Secondary stroke prevention｜2026-10-26 接收、逐點醫學 QA 與圖表出版界線

## 來源身分與範圍

- 稿名：〈分數都算到七分了，為什麼我還是不知道該用什麼藥？〉；正文自述 2026-09-10、神經內科病房，住院第三天。
- 原文來源：2026-10-26 使用者在 ChatGPT 對話直接提供的**完整文字**；原樣封存於 `archive/xiaoma-reading/teaching-scenarios/2026-09-10-secondary-stroke-prevention.md`；這證明「對話收件稿」，**不等於已核對 Facebook 正式出版版或其他公開版本**。目前未靜默修改原文。
- 隨附截圖：使用者當輪上傳之 1120×589 PNG，標頭 `Secondary stroke prevention (Stroke 2021;52:e364)`，附抗血小板、抗凝、血壓脂質及頸動脈介入摘要。該截圖已由本次對話可見、可目視讀取；**其在 Pocket Medicine 第九版的確切頁碼、caption/相鄰註腳、所在 PDF 全頁尚未查核**。原上傳檔仍是對話附件，尚未作為 Git blob 寫入儲存庫；此文件只保存來源描述與判斷，不宣稱圖像入庫、完成全頁核對或公開引用權利已通過。
- **作品性質（使用者 2026-10-26 明確更正）**：這是**自行設計的臨床教學情境（simulated teaching vignette）**，不是實際病人紀錄、實習心得或病房真實對話。故事裡的日期、病房、住院第三天、疑似 AF、CHA₂DS₂-VASc 七分、PUD、用藥與教師／總醫師對話均屬教學敘事條件；不得作為經查證的真實病例、病例報告或治療結果證據。此前以「可能是真實病房案例」推定的隱私與輪訓內容發布排除理由**撤銷**。公開頁必須清楚標示為設計情境，避免讀者誤認觀察事實。
- 公開狀態：**編輯候選／尚未發布**。模擬教學情境本身不構成排除條件，已可進入小麻閱讀公開候選池；目前仍因原書圖表全頁核讀／來源與醫學發布門檻未完成而暫不加入 `site/pages.json`，也未觸發 Cloudflare 發布。

## 作者已完整建立的概念（A，不可冒認成 AI 增益）

作者已使用病例敘事完整論證：① CHA₂DS₂-VASc 不等於當次 stroke 嚴重度，也不能倒證 AF；② antiplatelet 與 anticoagulation 是病因／適應症分支而非強度階梯；③ 出血危險與適應症不可互相替代；④ 不要以一個檢查或量表取代更上游的 clinical question。原文結尾「不要用下一層的工具，替上一層還沒回答的問題作答」是作者原有洞見，禁止在新版說成系統發明。

## 高影響細節與必修限定（D）

| 原稿論點 | 必須維持的證據界線與修正 |
|---|---|
| 「先有 AF，才談 CHA₂DS₂-VASc」 | 作為**決定 AF 相關抗凝適應症**的脈絡可成立；此分數不是 AF 的診斷工具，也不是 stroke severity score。但不能寫成此分數在其他任何研究／風險分層場合完全不能用；且非 AF 的其他抗凝適應症（如 LV thrombus、部分瓣膜情境）不能被這句排除。|
| 「沒有 AF 不先給 DOAC」 | 對未證實 AF、又沒有**其他獨立抗凝適應症**的未定來源 stroke／ESUS，不能以高分或推測 AF 經驗性給 DOAC。2024 ESC 針對 ESUS 指出現有 RCT 不支持 DOAC 相較 aspirin；必須評估既有其他機轉與 prolonged rhythm monitoring。未查出 AF ≠ 已確診 noncardioembolic。|
| 「若後來證實 AF」 | AF 合併既往 ischemic stroke 通常強烈支持口服抗凝，但**發現 AF 不會反向證明此次 index stroke 必定由 AF 栓塞所致**。DOAC 優於 warfarin 的一般建議不適用於機械瓣及中重度風濕性二尖瓣狹窄；需核對影像出血／轉化、腎功能與開始時機。|
| 「minor stroke ≠ 一定 DAPT」 | 強化具體門檻：2026 AHA/ASA 對 NIHSS≤3 的 noncardioembolic minor AIS 或 ABCD²≥4 的 high-risk TIA、未接受 IVT、通常 24 小時內起始 clopidogrel＋aspirin **21 天**後單藥（Class 1）。部分推測粥樣硬化（相關狹窄≥50%）且 NIHSS≤5／高風險 TIA，24–72 小時仍有 21 天 DAPT 的 Class 2a 路徑；另有 ticagrelor 選項 30 天的特定條件。「住院第三天」**不等於**「發作後 72 小時」；原文缺 NIHSS 量值、onset、IVT、血管狹窄與影像，不可擅自斷言單藥或 DAPT 哪一個在此個案最佳。 |
| 「PUD history → clopidogrel」 | 只能說 clopidogrel 是合法單藥選項，不可宣稱有 ulcer history 一律比 aspirin+PPI 安全。對已有 aspirin 相關潰瘍出血且潰瘍癒合的試驗族群，aspirin＋esomeprazole 的再次潰瘍出血風險反而低於 clopidogrel 單藥。這不是將該結果外推為所有 PUD 病人都應用 aspirin＋PPI。|
| 「先機轉，後出血」 | 是認知拆解，不是可延遲出血評估的絕對時間順序。**active GI bleeding／血流動力學不穩定可立即改變給藥安全性與時機**；indication 和 bleeding risk 實際上須並行權衡，不能因病因未知而放棄急性處理。既往 PUD 單獨不足以要求先作內視鏡，也不足以自動禁止所有抗栓藥。|
| 「維持原樣」 | 在**模擬個案**中用於教學：合理的不變動需要條件成立，不可將故事的選擇當成已驗證的真實病人醫囑。情境未提供 onset、NIHSS、血管影像與出血狀態，讀者不應推定唯一治療答案；這些是尚未給定、應在延伸決策練習處標明的未定變數。 |

## 來源逐項定位／當代更新（2026-10-26）

1. AHA/ASA, *Guideline for the Early Management of Patients With Acute Ischemic Stroke*, 2026. 4.8 Antiplatelet Treatment 與 DAPT Figure 4／Table 9（2026 增加可能 24–72h 起始的 atherosclerotic 路徑）：https://www.ahajournals.org/doi/10.1161/STR.0000000000000513 。可核對 Guidelines Central Table 9 / recommendation 12–15：https://eguideline.guidelinecentral.com/i/1542862-aha-asa-early-management-of-acute-ischemic-stroke-2026/42 。
2. AHA/ASA, *2021 Guideline for Prevention of Stroke in Patients With Stroke and TIA*, Stroke 52:e364–e467, DOI 10.1161/STR.0000000000000375。使用者截圖引用本來源，但**截圖是否從 Pocket Medicine 複述該指南**，待原書與頁面核對：https://www.ahajournals.org/doi/10.1161/STR.0000000000000375 。
3. 2023 ACC/AHA/ACCP/HRS AF guideline, Section 6.1/6.3.1：CHA₂DS₂-VASc 估計 AF 患者血栓風險，該條件下 OAC 建議及 aspirin 非抗凝替代：https://www.jacc.org/doi/10.1016/j.jacc.2023.08.017 。
4. 2024 ESC AF guideline, ESUS section：在未證實 AF 的 ESUS 中，現有試驗不支持 routine DOAC；持續監測依個案風險選擇：https://academic.oup.com/eurheartj/article/45/36/3314/7738779 。
5. Chan et al. *Clopidogrel versus Aspirin and Esomeprazole to Prevent Recurrent Ulcer Bleeding*. NEJM 2005;352:238–244, DOI 10.1056/NEJMoa042087 ：對已有 aspirin 相關潰瘍出血之特定試驗族群，單獨 clopidogrel 並非消化道保護最佳方案：https://www.nejm.org/doi/full/10.1056/NEJMoa042087 。
6. ELAN／OPTIMAS 與 2026 AHA 急性中風指引：證實 AF 後何時啟用 DOAC 必須綜合 infarct size、神經影像及 hemorrhagic transformation；不能憑單一「小中風／第 3 天」指定時點。2026 guideline 同上。

來源讀取層級：本輪讀到線上指引／試驗摘要與部分全文文字／表格及使用者提供的**裁切截圖**，沒有取得 Pocket Medicine 9E 相鄰全頁與足以完成圖像權利裁決的授權資料。未做獨立醫師審查或手機實機驗收；因為全篇屬設計教學情境，不存在需要核實的真實患者病歷。

## 編輯與發布判定

- **保存教學情境原稿：PASS**（原始文本 329 行、逐字保存；與審查分離）。
- **核心概念：可信，應以「作者設計的教學情境」定位，並就關鍵醫學適用條件增補獨立編輯註解；不須去真實病歷識別。**
- **情境用藥結論：未定**（情境未設定 AF 細節、onset、影像、病因、DAPT eligibility、出血嚴重度；不應當作已核實真實醫囑。這些未定處應明確教學化）。
- **圖片：HOLD**（截圖非完整原書頁，未能證實 PDF 註腳、版次頁碼及公開重製權利；私人對話附件與 Git blob 不可混說）。
- **公開候選資格：PASS**（作者已確認為設計教學情境，原先因疑似實習心得／病人隱私而限制公開的判斷無效）；**正式發布：HOLD**（醫學與圖表核讀／Figure gate 尚未完成，未加入發布白名單）。
- **後續最低條件**：以這篇**原創設計情境**作為教學主文候選，開頭醒目註明「以下為設計教學情境，非真實病例紀錄」；私下補 Pocket 全頁對讀與來源頁；用已製作的原創 DAPT／OAC／GI 決策圖，將未知變數寫成可檢驗的臨床條件；通過 Figure gate、EPQC 醫學 QA、build/tests/CI，部署後 HTTPS 回讀。不要稱為真實 case report；作者全文另存不被 AI 修改覆蓋。
