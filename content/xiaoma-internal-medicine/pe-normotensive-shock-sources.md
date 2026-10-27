# 肺栓塞：診斷、灌流與再灌流｜原始證據與圖表定位

本頁是〈血壓還正常，為什麼肺栓塞病人已經不能等下一張 CT？〉的來源對照。主文是重新撰寫的臨床教材；真實病例資料與自編反事實分開。**本篇目前是 GitHub 私有草稿，未列入公開目錄，未完成圖表與發布驗收。**

## 1. 真實病例與圖像

Rouleau SG, et al. **Management of Presumed Pulmonary Embolism With Normotensive Shock.** *Case Reports in Critical Care*. 2026;2026:4107549. Published 2026-02-20. DOI: [10.1155/crcc/4107549](https://doi.org/10.1155/crcc/4107549)。

已讀全文 Case Report 與 Discussion。本文直接使用其公開報告的下列**同一位病人**資料，不將不同來源拼接成一人：

| 原文時間點 | 真實記錄 | 教學可推出／不可推出 |
| --- | --- | --- |
| 急診初始 | 44F、BMI 54、近期 COVID-19、右下肢不適；HR 147、RR 33、BP 125/86、HFNC 50 L/min FiO₂ 0.50 時 SpO₂ 98% | 仍需氧療與高呼吸功；正常 BP／補氧後 SpO₂ 不保證 CO 正常 |
| 初始檢驗 | **VBG** pH 7.06、pCO₂ 15；lactate 13、chemistry HCO₃ 9、AG 29、glucose 493、β-hydroxybutyrate 0.27；hs-TnT 27、NT-proBNP 74 | 高 AG 代謝性酸中毒與極高乳酸；**初始 pH/pCO₂ 與 chemistry HCO₃ 不相容，不能當同一時間點計算補償**；乳酸不能單獨證明 PE |
| 診斷障礙 | 不能平躺接受 CTPA；POCUS views limited/nondiagnostic；ECG S1Q3T3 | 影像未證實前是 presumed PE；ECG 與 RV 線索非確診 |
| 惡化 | HFNC 下 SpO₂ 85%、意識混亂；repeat **VBG** pH 6.98、pCO₂ 48；仍 normotensive | 呼吸代償與氣道安全正在失敗，不以 SpO₂ 或 BP 單獨評估 |
| 插管後 | 先給 norepinephrine；插管後 SpO₂ 100%，約 10 分鐘後 arrest；CPR 中 tenecteplase 後 ROSC，VA-ECMO | 不能將「插管造成 arrest」或「tenecteplase 單獨造成存活」寫成已證實因果 |
| 後續 | 次日 CT 右主肺動脈殘餘血栓、mechanical thrombectomy；VA→VV-ECMO→脫離；雙側股部血腫與出血性休克；神經學良好存活 | 支持後續確實存在肺動脈血栓；同時顯示救援效果與重大出血代價 |

原始 Figure 1 是 **S1Q3T3 ECG**；Figure 2 是**機械取栓取出的血栓**，不是原始 CTPA filling defect。圖像目前僅讀取到網站 caption／figure 標題與原文敘述，**尚未完成原像素目視與手機版驗收**，因此不把它們複製到公開稿或宣稱已有可放大的原圖。

**原始病例內部數值一致性 QA：** 若 pH 7.06、pCO₂ 15 mmHg 為同一血氣檢體，Henderson–Hasselbalch 近似反推 HCO₃⁻ ≈ 0.03×15×10^(7.06−6.1) ≈ **4.1 mEq/L**，與另列 chemistry HCO₃ **9 mEq/L** 明顯不一致。原文未交代可確認的抽血時間差或誤植原因，不能私自修正原始資料；主文已將此列為來源疑義並避免用其計算混合酸鹼診斷。後續應向原文作者／期刊或 supplementary data 查證。\n\n## 2. Pocket Medicine 第九版

使用者 Library：*Pocket Medicine: The Massachusetts General Hospital Handbook of Internal Medicine*, 9th ed., Flatten PDF，**reader PDF p.97–101**（檔案解析共 463 頁；既有 VTE 來源紀錄曾以 464 頁表示，頁數 metadata 尚需核對）。本次讀到 **p.98–101 的文字解析與圖表位置**，但頁面影像讀取返回 unavailable，原 PDF 原始 bytes 亦未能 materialize。既有 GitHub [VTE 圖表來源紀錄](../xiaoma-reading/vte-sources.md) 曾記錄 2026-10-26/27 目視 p.97–100，**不冒稱本次已重新目視 p.98–101 的像素**。

- **p.97**：Virchow triad 與 *Thromboprophylaxis* 情境表，屬 VTE 共同預防上游問題；本篇不重新抄錄預防藥物表。
- **p.98**：DVT modified Wells 三層模型、**Figure 2-2 Approach to suspected DVT**，以及 PE Wells 開始；DVT 三層分組不應移植成 NICE 的 DVT 兩層演算法。
- **p.99**：PE Wells 續表、**Figure 2-3 Approach to suspected PE**；注意陰性 CTPA 與 pretest probability 不一致時的限制。這是本篇「診斷證據」的原圖定位；**完整原圖分支／caption／footnote 本次尚未逐像素重核**。
- **p.100**：sPESI、RV/biomarker 分層、初始抗凝與 reperfusion table；原書的分類主要依 ESC 2019，不能把 2026 AHA/ACC 的 A–E 直接說成原書內容。
- **p.101**：mechanical intervention、IVC filter、抗凝療程與長期後果；本篇只抽取與「抗凝 vs 再灌流」直接相關的概念。

**安全勘誤（不可忽略）**：PDF p.100 *Initial Anticoagulation Options* 將 rivaroxaban 起始療程印為 **15 mg qd ×21 d →20 mg/d**。這與 EINSTEIN-PE 原始 RCT 的 **15 mg twice daily for 3 weeks →20 mg once daily** 不符。核對 [EINSTEIN-PE, NEJM 2012](https://doi.org/10.1056/NEJMoa1113572) 的 methods。主文不給具體抗凝處方，以免錯誤表格被誤當床邊醫囑；實際處方另依藥品仿單、腎肝功能、禁忌與在地指引確認。

圖像權利：Pocket PDF 不進公開站，不以文字圖或 AI 重繪冒稱 Figure 2-3 原圖。若原圖像素未能重核，這份新教材的 Figure/Table Gate 為 **pending**。出版社合法取得入口：[Pocket Medicine 9E](https://shop.lww.com/Pocket-Medicine/p/9781975242978)。

## 3. 當代正式指南

Creager MA, et al. **2026 AHA/ACC/ACCP/ACEP/CHEST/SCAI/SHM/SIR/SVM/SVN Guideline for the Evaluation and Management of Acute Pulmonary Embolism in Adults.** *JACC*. 2026;87:1626–1710. DOI [10.1016/j.jacc.2025.11.005](https://www.jacc.org/doi/10.1016/j.jacc.2025.11.005)；[AHA 官方要點](https://professional.heart.org/en/science-news/2026-guideline-for-the-evaluation-and-management-of-acute-pulmonary-embolism-in-adults/top-things-to-know)；[JACC 2026 Guideline-at-a-Glance](https://www.jacc.org/doi/10.1016/j.jacc.2025.12.023)。

- **診斷**：先臨床機率，低機率可在適用條件下使用 PERC；低／中等機率採經驗證 D-dimer／YEARS／age-adjusted 方法，較高機率與陽性者影像。CTPA 優先；echo 是 RV 評估，不是 PE 確診。
- **分層**：A（incidental）、B（symptomatic low risk）、C（elevated risk）、D（incipient failure）、E（cardiopulmonary failure）；D2/normotensive hypoperfusion 需綜合臨床與器官低灌流證據。JACC 主文對 D2 transient hypotension 與 normotensive shock 的敘述在不同段落存在可能的語義張力；**不將病例機械指定精確 D2 subtype，須再以原始 Figure 與 footnote 核對**。
- **治療**：2026 指引對 A1–C2 的常規 systemic thrombolysis 有 harm 建議；D1–D2 在適當條件可考慮進階治療；E1 具較強再灌流理由。LMWH/UFH、DOAC/VKA 與出血禁忌依情境判斷，並非所有病人同一藥物。
- **時序**：此指引 2026-02-19 公布，**不可能已納入 2026 年 3 月 HI-PEITHO 或 2026 年 8 月 PRAGUE-26 的最終結果**。**2026-07-14 正式勘誤已核讀文字全文**：[Circulation correction DOI 10.1161/CIR.0000000000001462](https://doi.org/10.1161/CIR.0000000000001462) 更正 **Table 4（RV echocardiographic dysfunction assessment methods／thresholds）** 與 §3.1.2 reference 44（ASE 2025 右心超音波指引）。本篇未以舊 Table 4 的個別數值定義 RV dysfunction；未重製原表像素，正式原圖及 360/390px 仍待驗證。
- **原圖**：JACC Guideline-at-a-Glance 的 clinical categories Figure 1 有原始 footnotes；本次取得文字註腳，未取得可驗證的完整原像素，暫不重製。

NICE [NG158 recommendations](https://www.nice.org.uk/guidance/ng158/chapter/recommendations) 與 [原始 DVT／PE visual summary（Thrombosis UK 保存副本）](https://thrombosisuk.org/wp-content/uploads/2024/12/WellsScore.pdf) 是既有 VTE 篇的診斷流程定位；**不把 NICE 兩層 Wells 與 AHA 三層風險演算法拼成單一流程**。

## 4. 介入試驗與證據邊界

1. **PEITHO 2014**：Meyer G, et al., *NEJM*. [10.1056/NEJMoa1302097](https://doi.org/10.1056/NEJMoa1302097)。有 RV dysfunction 與 troponin elevation、但未持續低血壓的 PE；全身溶栓降低 hemodynamic decompensation，卻增加 major bleeding／hemorrhagic stroke，未證明死亡率改善。未本次逐讀 supplement。
2. **HI-PEITHO 2026**：*NEJM*. [10.1056/NEJMoa2516567](https://doi.org/10.1056/NEJMoa2516567)；[ACC 同步發布摘要](https://www.acc.org/Latest-in-Cardiology/Articles/2026/03/25/21/27/sat-930am-hipeitho-acc-2026) 與 [ACC 詳解](https://www.acc.org/Latest-in-Cardiology/Articles/2026/09/08/14/17/HI-PEITHO-and-the-Evolution-of-Reperfusion-Strategies-in-Pulmonary-Embolism)。n=544；主要七日複合事件 4.0% vs 10.3%，重大出血 4.1% vs 2.2%（未顯著）；非死亡率已證實改善，也非出血等效。
3. **PRAGUE-26 2026**：*NEJM*. [10.1056/NEJMoa2608012](https://doi.org/10.1056/NEJMoa2608012)。n=558；七日複合事件 0.7% vs 6.8%，主要由較少心肺惡化驅動；導管組 ICH 2/280 vs 0/278。全文摘要與結果可讀，**supplement 未逐表核讀**。此試驗為 catheter-directed alteplase，不能等同機械取栓或 HI-PEITHO 的 ultrasound-assisted 方案。

## 5. 官方真題、著作權與未完成項

本輪**沒有取得並核對與本篇直接相關的考選部原題、官方答案及更正**；因此正文僅有明示的 T1／T2 自編遷移題，**不計入任何年度正式題號索引**。後續找到官方 PE 真題，須先核實年份／梯次／醫學科目／題號與更正，再在既有按年份頁面建立雙向連結。

第三方 ECG、血栓照片、Pocket Figure 2-3、JACC 分類原圖均未公開重製。此版本沒有假稱可放大的原圖入口；亦未完成手機 360/390px、深色模式、CI、Cloudflare 或正式 HTTPS 正文讀回。**發布判定 HOLD：原圖像素／註腳未重核、試驗 supplement 未核、官方真題未核、版面及獨立醫學 QA 未驗證。指引 2026-07-14 correction 的文字已核讀，但原圖未完成目視。** 這些是不同缺口，不能以單次 AI 自評或 GitHub 提交取代。
