# Constipation 原稿回收與醫學審查（2026-10-26）

**狀態：source captured / guideline checked / publication HOLD。** 與歷史作者原稿分離的 AI 編輯查核；尚無獨立醫師審查，不宣稱已出版。主題：〈糞便已經變軟，為什麼下一步不一定是再加一顆瀉藥？〉（文內日期 2026-07-26）。

## 來源身分與入庫

- 2026-10-26 使用者於對話完整提供全文，已原樣保存在私人 `archive/xiaoma-reading/intake/2026-07-26-constipation-user-supplied.md`（入庫 commit `3fa97afb07d50ebdc453033d3efa18fcae0facea`）。
- 這是直接取得的 user-supplied source snapshot；尚未比對 Facebook 已刊 canonical version，不能逕稱「歷史已發表原稿」或 AI 審稿通過。
- `site/pages.json` 尚未納入、沒有正式公開 HTML；不以此 audit 的存在冒稱 deploy。
- 本次未確認案例是否真實病人或教學合成情境；正式網站前須處理案例來源與去識別化，避免把自行編造細節當成真實病例。

## 小麻 9E 原文核對（實際閱覽層級）

- ChatGPT Library `內科_Pocket Medicine The Massachusetts General Hospital Handbook of Internal Medicine, 9th Edition_625A_Flatten(1).pdf`，reader PDF 第 **127 / 463 頁**；已查看該頁**頁面影像與文字**，不是只有關鍵字搜尋結果。
- 該頁 `Constipation` 段列出 Rome IV：straining、hard stools、incomplete evacuation、anorectal blockage、manual maneuvers、低頻率；primary slow transit vs pelvic floor dyssynergia、secondary causes 4 Ms（含 spinal injury、opioid）、DRE、ARM/BET、transit/defecography。治療段用一二三線排列 docusate、fiber／stimulant／osmotic、suppository/enema，之後列新藥。它是壓縮式治療表，不代表慢性便祕所有病人皆應嚴格順序加藥。
- 此為具版權教科書頁影像，**不得直接加進公開 Git／Cloudflare 檔案**；公開教材應用自己的原創示意圖及合法的出處定位。若未取得必要授權，不貼原表。

## 已查醫學來源（2026-10-26）

1. AGA/ACG 2023 chronic idiopathic constipation guideline, full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC10542656/ 。PEG 強建議；fiber、senna 等適用與證據強度不同；該指南**排除 OIC**，不可直接將 CIC 試驗外推至 OIC。
2. ASCRS 2024 Evaluation and Management of Chronic Constipation: https://www.ascrsu.com/ascrs/view/ASCRS-Toolkit/2851100/all/Evaluation_and_Management_of_Chronic_Constipation__2024_ 。DRE 檢查 impaction、anorectal pathology、Valsalva；確認 symptomatic pelvic floor dyssynergia 時 biofeedback 是一線。
3. AGA 2018 OIC guideline: https://gastro.org/clinical-guidance/medical-management-of-opioid-induced-constipation/ 。傳統 laxatives 首線；laxative-refractory OIC 才考慮 PAMORA。
4. AGA 2026 clinical practice update on refractory constipation: https://gastro.org/clinical-guidance/evaluation-and-management-of-refractory-constipation/ 。多數真正慢性 refractory 個案，先完成 ARM/BET 與需要時 biofeedback；本故事的住院第五天**不能單憑短期用藥貼上 refractory 標籤**。
5. NICE NG127 possible cauda equina: https://www.nice.org.uk/guidance/ng127/chapter/Recommendations-for-adults-aged-over-16 。嚴重腰背痛合併新的膀胱／腸道功能或會陰感覺異常需即時評估；如果病例出現新尿滯留、鞍部麻木、進展性下肢神經缺損，不應停留在常規便祕的出口測試。
6. WFNS cauda equina consensus: https://pmc.ncbi.nlm.nih.gov/articles/PMC10943478/ 。疑似 CES 需緊急 MRI；單次正常神經／肛門檢查不足以排除。
7. PAMORA 安全條件參照 2026 expert consensus: https://pmc.ncbi.nlm.nih.gov/articles/PMC13026780/ 。若已知／疑似機械性腸阻塞或反覆阻塞高風險，PAMORA 受禁忌或顯著限制；須依實際藥品仿單確認。

## 知識貢獻分類

- **A（原作者已建立）**：stool properties／propulsion／outlet 非同一個便祕強度軸；分開衡量藥物反應，不能以 overall non-evacuation 直接宣告全部藥物無效；biofeedback 是處理協調而非更強瀉藥。不得將此歸為 AI 新發現。
- **B（原書 × 作者）**：原書直列 first/second/third line，本文把它映射為作用節點與治療反應指標；保留原作者的臨床對話與論證。
- **D（公開前必要校正）**：
  1. **敘事證據不相容：** 原稿寫「病人在使用 opioid 以前，就已經存在 blockage 與 manual maneuver」，但此前只說「入院前兩、三天排便一次」；床邊詢得的 manual maneuver 時序未交代。應補一句追問其起始時間，否則不能認為 opioid 前已存在。
  2. **反應歸因過強：** PEG、senna 同時新增，又用 suppository；軟便不能單憑時間先後證實由 PEG 導致；便意增加也不能單憑 cramping 歸因於有效 propulsion。正確表述是『治療後 stool form／urge 有變化，仍須分辨各藥貢獻』。
  3. **急性危險排除不足：** 新／進展性尿滯留、鞍部感覺異常、下肢神經惡化（腰椎骨折脈絡）、劇烈腹痛／嘔吐／腹脹／停止排氣等，應早於單純升級瀉藥或慢性出口檢查進行鑑別；必要時查 obstructive process、ileus 或神經壓迫。
  4. **測試定位：** DRE（含 simulated evacuation）可提供重要訊號，不能確診或排除 dyssynergia；持續懷疑時 ARM+balloon expulsion；有結構異常假說且結果不明時再考慮 defecography。低頻率或便意少不等於已證實 slow-transit，transit study 的順序亦須考慮出口障礙。
  5. **治療安全：** impaction 位置與硬度影響 disimpaction／灌腸選擇；有阻塞疑慮時不應機械式追加 fiber、stimulant、灌腸或 PAMORA。磷酸鹽灌腸需考量腎功能和電解質風險。
- **X：** 未直接取得此案例原始病歷，無法驗證每項臨床反應的真實性或確切因果，不能自述為臨床驗證案例。

## 出版 Gate（保持最小維護）

- [x] 本次提供的原稿快照存入私人 repo，沒有改寫。
- [x] 小麻 9E constipation 段 **p127 原頁影像實看**，記錄表格排列與臨床推論的差別。
- [x] AGA/ACG、ASCRS、AGA OIC 和疑似 CES 的重要安全依據完成第一輪核對。
- [ ] 核對已發表作者版本身分；若不追溯已發表版，依新獨立編輯版另行標明作者／編輯責任。
- [ ] 在**新整合稿**修正上述 D 類缺陷，不改寫封存的作者快照；完成完整情境／藥物禁忌／來源 QA。
- [ ] 建立原創可讀示意圖並檢查行動版；不得擷取 Pocket 原書圖至公網。
- [ ] 將審查合格的公開版加入 `site/pages.json`、測試 build、Cloudflare deployment 並 HTTP 驗證。此前**沒有公開連結**。

**後續候選稿（已建立）：** [Draft PR #59](https://github.com/sheng-web-OS/Clinical_system/pull/59) 於獨立 `editorial/constipation-20261026` 分支保存 AI 改判與來源頁，不在 `site/pages.json`，尚未公開。該稿不覆蓋本文封存的原作者原文。

結論：本輪已**完成來源回收、首次 evidence audit 與獨立修訂候選 PR**，不是醫學內容與網站發布全部驗收。
