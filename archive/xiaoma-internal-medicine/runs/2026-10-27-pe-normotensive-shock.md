# 2026-10-27｜每日小麻內科國考：PE normotensive hypoperfusion

**私人執行紀錄；不得列入 site/pages.json、公開站或搜尋索引。**

## 今日判斷與優先序

先讀 main 的 `archive/xiaoma-internal-medicine/current-plan.md` 第 0–12 節，尤其 §10 每日自主選題及 §12 2026-10-26 COPD 後的候選。再讀 EPQC、xiaoma-depth-standard、xiaoma-publishing、figure-table-publication-gate、main 70 筆 manifest、目前 VTE 原創整合與 VTE sources、歷屆題庫索引、既有真題與 2026-10-26 COPD 執行紀錄；核對 open PR 包含 CTICU oxygen delivery #110、GI/liver #98、國考 #51、VTE #60。**現有網站已有 VTE 共同預防／DVT vs PE 診斷分流**，本次不再重寫相同 Wells 表或修飾既有圖。

缺口排序：① A 級肺栓塞的診斷不確定性 → 氣體交換／RV 失代償 → 抗凝／再灌流閾值，能串接低氧、NIV、酸鹼、VTE；② COPD 原圖公網權利與像素驗收（另一 PR #49 已在處理）；③ CTICU DO₂ V2（已有 PR #110 HOLD）；④ 國考 108（一）第 5/6 批（已有 PR #51/#87）。選①是因為尚無獨立 PE 深度主文、危及生命的風險轉折未建立；並避免重複正在處理的 PR。

學習狀態：沒有使用者新的個人作答／閱讀／投入時數證據。2026-10-22 二十題基線仍不得算已施測；2027-01-17 優先／01-24 最晚內科 A/B 首輪，考前 10–14 天混合題與錯題修補維持；不把稿件存在當成使用者已掌握。

## 本次實際產物

- **主文 V1** `content/xiaoma-internal-medicine/lessons/2026-10-27-pe-normotensive-shock.md`：以 Rouleau et al. 2026 44F 真實病例建立 7 節連續論證。三個互不蘊含的問題（diagnosis／physiologic severity／reperfusion threshold），逐步拆開 HFNC SpO₂ 98%、乳酸 13、VBG 與 chemistry、RV afterload→LV filling→CO、插管後氧合與循環不同步、抗凝 vs 再灌流，並納入 2026 指引與 HI-PEITHO／PRAGUE-26 的證據時序。
- **來源核讀頁** `content/xiaoma-internal-medicine/pe-normotensive-shock-sources.md`：原始病例的同一病人資料／圖說、Pocket 9E p97–101 原書定位、2026 指引與 2026-07-14 勘誤、三項試驗及權利邊界。
- **自編遷移題 T1/T2**：先作答後展開逐選項推理，沒有假冒考選部正式題目；官方 PE 真題未核驗，**未加入年份索引**。
- **本紀錄**：保留來源不足、圖像與醫學 HOLD、工程及人工介入邊界。沒有修改歷史作者原稿、既有 VTE 文章、shared runtime、manifest 或公開白名單。

## 來源查核與發現的 P0

1. **真實病例全文**：Rouleau et al., *Case Reports in Critical Care* 2026, DOI 10.1155/crcc/4107549。實讀 Case Report、Discussion，核對 HR/BP/RR/HFNC/VBG、lactate、troponin/BNP、插管/ROSC/ECMO/取栓、重大出血與圖說；原 Figure 1 是 ECG、Figure 2 是取出血栓，**不是 CTPA**。原像素尚未目視。
2. **P0：原始資料數值不一致**。原文初始 VBG pH 7.06、pCO₂ 15 mmHg，同段 chemistry bicarbonate 9 mEq/L；Henderson–Hasselbalch 若同時同樣本，推得 HCO₃ ≈ 4.1 mEq/L，與 9 明顯不符。原文未能核實採樣時間差或誤植。**不修改原病例數據，不以其計算 Winter 或混合障礙**；主文及來源頁明列疑義，正式發布前需釐清或進一步縮減數值推論。
3. **公開原始流程補位**：實際開啟 NICE NG158 3 頁 visual summary，目視 PDF 第 2 頁 suspected PE 流程、分支與頁底 5 項 footnote；主文已附可點入的原 PDF，**清楚標明不是 Pocket Figure 2-3**，不以原創抽象圖冒充。\n4. **Pocket 9E 原頁**：Library 找到原 PDF，使用 files.read p98–101 取得文字、表格標題與部分 footnote；圖像不可用，原 bytes materialization 被權限拒絕。本次**未完成 Figure 2-3 與 p100 初始抗凝表原像素／caption／footnote 的親自重核**。既有 VTE sources 曾有 p97–100 目視紀錄，可作定位但不能冒稱本次完成。p100 rivaroxaban `15 mg qd ×21d` 與 EINSTEIN-PE `15 mg BID ×21d` 不符，來源頁明確警示，不作處方。
5. **2026 AHA/ACC**：查正式 guideline 及 AHA 要點、JACC at-a-glance，核對 A–E、診斷 vs 風險、A1–C2 不常規全身溶栓、D1–D2 可考慮、E1 合理；**2026-07-14 correction** 原文已核讀，更新 Table 4 RV echo assessment 與 §3.1.2 reference 44。原 Figure 1/2 像素尚未目視，D2 描述在正文與圖註有語義差異，未把真實病例硬貼精確 subcategory。
6. **新試驗**：HI-PEITHO 544 人（4.0% vs 10.3%；major bleeding 4.1% vs 2.2%）核 ACC 2026 同步報告與後續評論；PRAGUE-26 558 人（0.7% vs 6.8%；ICH 2 vs 0）核 NEJM 摘要；PEITHO 原文摘要／歷史結論。未讀所有 supplementary appendix，不能宣稱跨試驗比較已完成。
7. **圖像權利與品質**：第三方 Pocket、JACC、Wiley 原像素均未重製。沒有用 AI 卡片或未驗證外部圖片湊圖；原書 Figure/Table Gate **pending**。真實病例 ECG／取栓照片若將來嵌入，需先核對圖像像素、caption、授權、與正文實際認知角色，且 360/390px 可放大。
8. **考題**：找到高度相關的 **112 年第二次・醫學（三）第 51 題**（PE Wells、D-dimer、右心衰竭），第三方逐字題目與答案 D 可查，但**尚未實際核對考選部原卷、標準答案與更正**；因此只保留 T1/T2 自編，Q51 僅為下一步官方核題候選，不得將其記成已完成國考題數。

## EPQC 初稿篩選（同上下文自評，非獨立審查）

A 命題 3：一篇聚焦診斷／失代償／介入三個層次，後半試驗段仍可更緊密；B 解混 4：SpO₂/CO、診斷/分層/治療、抗凝/再灌流清楚；C 中介 4：PVR→RV→LV filling→CO，代償失敗接插管；D 證據 3：保留病例數值矛盾與試驗時間順序，但 P0 未解；E 連續 3：病例回到每一個問題，後半 trial 需減少資訊負荷；F 遷移 4：T1/T2 與三種反事實；G 語言 3：術語前提已有，但專業讀者以外需測試。平均 **3.43/4**，僅供內部修稿定位；**不達使用者的「90 分以上且硬性門檻通過才發布」要求**，也不是獨立醫師審查。P0 數值衝突與圖像 gate pending 為不可用分數補償的 HOLD。

## 工程與發布

- 只在 `draft/xiaoma-pe-normotensive-shock-20261027` 分支保存主文、來源與本紀錄，準備 Draft PR。**main 沒有新增 PE 教材；site/pages.json 未改，沒有公開部署。**
- 本輪使用 GitHub connector 編輯，未取得本機 repository checkout；**未執行 tools/build_site.sh、unittest、360/390px 真實瀏覽器、CI 同 SHA 驗證或 Cloudflare 正式 HTTPS 讀回**。PR CI 若有結果，另核對，不以其他 PR 成功代替。
- 不公開私人計畫、個人答題、原書 PDF 或病人識別資料。真實病例採已發表匿名資料；AI 自編反事實獨立標示。
- 人工介入：本輪未請使用者做可由 Agent 處理的來源與編輯工作；時間與次數若無外部紀錄，不推估為零。

## 下一步與停止條件

先修 P0（原病例血氣／chemistry 來源一致性，或撤除不能支持的精確酸鹼推論），取得可驗證 Pocket Figure 2-3 與 p100 原表像素／caption／footnote；NICE 原圖已目視並有可點入的 PDF，但不能代替 Pocket 原圖核對；再決定真正需要的原圖引用與手機閱讀方式。之後補一題可核實的官方 PE 真題與更正、按年份雙向連結，做獨立 V2 醫學複讀、圖像 QA、build/CI、main 與 Cloudflare 同 SHA 讀回。**上述完成前 HOLD，不自動合併或發布。**


## 2026-10-27 接續 V2｜官方真題與來源對抗式修訂

此節是**V1 首次交付之後的獨立第二次提交**；原始 V1 版本保留於 `6cd612d69306ea5f3791bb63d31e038699f01aea`，原本 3.43/4 的初次自評、原始 P0 疑義及未過圖像 gate 沒有被追溯改寫。

- **V2 改動**：主文 `§03` 以 chemistry HCO₃／AG／lactate 作高陰離子間隙酸中毒判斷基礎，保留初次 VBG 7.06/15 作「來源待核」而不是自動判定精確呼吸代償；`§05` 撤回「兩次 VBG pCO₂ 可證明代償喪失」的過強因果敘述，改以臨床意識與呼吸狀態惡化支持急救升級。這是收縮推論範圍，**不是解決原論文的採檢時間／誤植**。
- **官方真題**：考選部 112（二）醫師（二）醫學（三）第 51 題，原卷 PDF（p.12/18）、標準答案與更正公告逐項核對。正式正解 D；更正表 35、43 更動但**51 未更正**；新增 A–D 逐項深入解析。原卷 https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=112080&q=1&s=11&t=Q ；更正 https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=112080&q=1&s=11&t=M 。尚未公開年份索引，因整篇文章仍 HOLD；不能計入發布國考題數。
- **Pocket 9E 再取證**：Library `內科_Pocket Medicine The Massachusetts General Hospital Handbook of Internal Medicine, 9th Edition_625A_Flatten.pdf` p.99–100 的解析文字可以回讀，但影像本次顯示 `Image unavailable`，原 bytes materialization 再次被拒（`This Project file does not have an authorized raw-byte materialization path`）。因此 Figure 2-3、p100 anticoagulation table 完整原圖／caption／footnote **仍未完成重新目視**。不要使用其他機構的 PE 流程圖冒稱 Pocket 原圖。原書 rivaroxaban 15 mg qd ×21d 疑似藥物劑量錯誤仍標示，不按原表開立。
- **外部核查**：重新核對 2026 AHA/ACC Table 7：A1–C2 systemic lysis 3:Harm、D1–D2 2b may be considered、E1 2a reasonable，C3 不確定；NEJM HI-PEITHO 544 人、4.0%/10.3%、重大出血 4.1%/2.2%；PRAGUE-26 558 人、0.7%/6.8%、ICH 2/0。試驗族群／技術各異，不能互相替代，也不能將 2026 年後續新試驗倒灌進 2 月指南。
- **QA 狀態**：稿件 P0 原文矛盾仍存在，V2 已消除錯誤定量推論；Pocket Figure/Table 實際像素仍待核，因此醫學／圖像綜合發布 gate = **HOLD**。本輪未進行獨立真人醫師審查、正式手機 360/390 Chromium 頁面驗收、主分支部署或 Cloudflare HTTPS 讀回。沒有更改 `site/pages.json`。工程 CI 是否通過須依最新 V2 SHA 個別查核。
- **V2 commit**：主文 `daf08826617bb04605aae52a5aee88f544a5be36`；來源頁 `9c2def63f85f4b4a44ea4fa76cff1dc8b0a921f4`。未新增重複排程。

## 2026-10-27 V3｜去重、臨床因果補橋與跨 PR 衝突排除

**版本身分**：V1 `6cd612d69306ea5f3791bb63d31e038699f01aea` 與其原始評分永久保留；V2 的官方 112（二）Q51 查核與資料矛盾警示亦保留，不得被本次自評回填取代。以下是增量編輯，沒有改動過往原稿或公開 VTE 正文。

- **主文 V3**：以 2026-10-26 已上線的 VTE 文章作為 Wells、D-dimer、陰性 CUS／CTPA 停止條件唯一基準；`§01–02` 取消第二套診斷演算法，保留「影像無法安全取得時，診斷和循環支持必須並行」及不能把未確診 PE 寫成已確診的關鍵分歧。
- **深度新增**：`§04` 將 RV afterload → RV dilatation／septal shift → LV filling／CO 下降，進一步接到 RV 壁張力增加、冠狀灌流可能下降、RV ischemia 形成回饋惡化；`§05` 增加 metabolic acidosis 對有效肺泡換氣的要求與 PE dead space 的疊加，但不假稱原病例量到了 dead-space fraction／cardiac index。
- **介入證據辨識**：HI-PEITHO 的 ultrasound-facilitated catheter-directed fibrinolysis 與 PRAGUE-26 的 catheter-directed alteplase 不可和單純 mechanical thrombectomy 混成同一組隨機試驗。保留相對風險、出血及試驗時間界線，不宣稱 mortality benefit 或無出血風險。
- **來源一致性**：主文／來源頁均有考選部官方原卷、標準答案、更正公告核對的 112（二）醫學（三）Q51：D，未更正；先前 V1「尚未官方核題」是**歷史當時狀態**，不可當作 V3 現況。V3 修來源檔內誤呈現的跳脫換行，增加清楚的跨篇責任分界。年度索引因未公開仍沒有新增 Q51。
- **並行分支風險**：PR #60 舊 VTE 整合稿仍開著、來源與新 VTE 正式頁覆寫風險高。比對原始作者 snapshot 與 main：原始全文的 blob SHA 同為 `9a6d2ff41ab48b6fd4800ac44f45cc2613f577a2`，證明原文已保存於 main；舊 PR 特定 CSS／插圖不是不可重建的合格資產。建議不合併 PR #60，保留閉合 PR 的 git history 作稽核。PR #110 CTICU 氧輸送是獨立生理主線，不與本稿併稿。

**驗收／未過**：此輪只完成 connector 原始檔逐段核對、定點文字修訂、跨 PR diff／blob identity 與正式 2026 AHA/ACC 指引、NEJM 研究網頁交叉確認；尚未對 PR #111 的這個新 SHA 跑 CI、真實手機 360／390px 截圖或 Cloudflare 讀回。Pocket 9E p99 Figure 2-3 與 p100 原表的原像素／註腳仍待補，病例初始 VBG／chemistry 數據不一致仍是原文疑義（僅有安全收縮推論），獨立醫學審查也未完成。**維持 Draft/HOLD，不改 main／公開白名單，不宣稱網站已更新。**

後續優先：驗證 Pocket 原圖完整頁與 caption/footnotes；按讀者認知角色決定是否需要合法展示 2026 AHA/ACC original categories 圖；獨立檢查 Q51 與介入試驗描述；完成 360／390px 與 build/CI，再依門檻另行決定正式發布與建立 VTE 反向閱讀入口。


## 2026-10-27 限定醫學驗收：真實病例可保留，禁止矛盾血氣的定量推論

- 專案擁有者針對本篇 **Rouleau 2026 normotensive shock 真實病例的安全使用邊界**答覆「可以，繼續推進發布進度」。明確接受：保留匿名真實病例作為肺栓塞疑似診斷、灌流失代償、再灌流淨效益之連續教學骨架；**完全排除**將 pH 7.06／venous pCO₂ 15／chemistry HCO₃ 9 組合做 Winter、混合酸鹼判定、精確代償或氧債定量推算。這是單項醫學編輯自審接受，不是全文、圖像或正式合併部署授權。原接受時主文 Git blob `cdbe475b95157910e541b283532b670b161e679c`，PR 討論證據：[bounded owner acceptance](https://github.com/sheng-web-OS/Clinical_system/pull/111#issuecomment-6431804648)。
- 新版主文首段明示不同來源檢驗不可拼成單一同步酸鹼樣本；來源頁保留原值及不一致警示，移除讀者可誤作患者 bicarbonate 的衍生算式。病例後續血壓、乳酸、氧氣／心臟停搏時序仍不得冒稱 PE 已於當下確診，亦不把溶栓／ECMO 結果當因果證明。
- 已透過 File Library 的 **第二份 Pocket Medicine 9E PDF** 實際目視 reader 第 99 頁 Figure 2-3（Wells likely／unlikely → D-dimer／CTA，陰性但高懷疑時追加影像）及第 100 頁原始 Initial Anticoagulation Options 三欄表、caption 與 footnote 附近文字。**圖檔只供私人核讀，未授權嵌入公網**；以已有 VTE 站內診斷圖與 NICE 來源連結代替重製，保留名稱／來源分辨。
- 發現第 100 頁 rivaroxaban 初始欄位原書寫 **15 mg once daily ×21 days**，與 [DailyMed FDA 標示](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=10db92f9-2300-4a80-836b-673e1ae91610) 成人 DVT／PE 起始 **15 mg twice daily for 21 days** 不符；來源頁明確標記不能照抄該行開方。其他原表選藥限制也不能脫離指引版本與病人出血風險。
- 這個階段只屬來源、編輯及原圖**私人核對**，不是對 Figure Gate、同提交 browser screenshots、全篇臨床意義或正式發布的自動放行。維持 Draft/HOLD，禁止直接合併或部署。
