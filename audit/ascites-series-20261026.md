# Ascites 上下篇｜2026-10-26 原稿回收與出版前醫學／圖表審核

## 狀態與邊界

- **已完成：** 使用者本輪完整提供 2026-07-22 與 2026-07-23 兩篇文字；以獨立 Markdown 原文快照儲存在 `archive/xiaoma-reading/intake/`，未修改其敘事或藥物建議。
- **來源身分：** user-supplied source snapshot；尚未獨立核對 Facebook 發表版或作者最後編輯版本，**不可冒稱 canonical historical original**。
- **原書實查：** 使用者 Library 內《Pocket Medicine: The Massachusetts General Hospital Handbook of Internal Medicine》9E、reader PDF 第 **147、152、153、154 頁**（全檔 463 頁）。在工具返回之圖片中目視核查過這四頁的圖／表版面，不僅是全文檢索結果。公開網站不可直接貼入書籍原像素。
- **公開狀態：HOLD**。尚無經驗證的原創閱讀版、對題來源頁、可驗收的原創圖解與 site/pages.json 發行項目。此稿只進入 **feature branch / draft PR**，不得宣稱正式網站已上線。
- **範圍：** 本次 source audit 是有跡可循的編輯初審，**不是**獨立專科醫師審稿或學習成效證明。

## 原書逐頁回收

| PDF reader 頁 | 原頁項目 | 跟文章的依賴 | 原像素公網 |
|---|---|---|---|
| 152 | `ASCITES / Pathophysiology` 開始：portal HTN → splanchnic vasodilatation → low effective arterial volume → RAAS/ADH | 下篇雙軸邏輯之起點；同時解釋上篇 high SAAG 生理背景 | 未重製 |
| 153 | `Etiologies` 雙欄（Portal HTN Related／Non-Portal HTN Related）、SAAG cutoff、AFTP cutoff、PMN 與 culture 等 | 上篇必須解讀的「形成原因 vs 病因延伸」原表，應避免把 presinusoidal→sinusoidal→postsinusoidal 畫成病程 | 未重製 |
| 153–154 | `Bacterial peritonitis`：ascitic PMN × culture 的 2×2 表、SBP/CNNA/NNBA、secondary peritonitis Runyon thresholds，含分頁接續內容 | 上篇第二個分類維度與 secondary source 的 source-control 分支；須在新圖中還原至少 PMN/culture 的判斷範圍 | 未重製 |
| 147 | `Cirrhosis / Ascites`：鈉、利尿、refractory ascites、LVP + albumin、TIPS；`Spontaneous bacterial peritonitis` 段 | 下篇多介入位置、albumin 用途異質性與 SBP 急症補足 | 未重製 |

對照舊書特別留意：其 `LVP >5 L` 補充 albumin 的簡述可能讓讀者誤以為只按「超過 5 L 的部分」計算；現行 AASLD／AGA 說明應以**放出的總公升數**計算。舊書也有「Avoid LVP if SBP present」的簡短提醒，並不能未經情境分析就直接當作跨所有病人的絕對禁忌。不同年代 SBP 風險與 HRS 診斷標準，亦應回對現行來源。

## 與現行指引對讀（未直接將修正寫入作者快照）

1. **兩次判斷不是兩條自然史：** SAAG = serum albumin – ascites albumin；≥1.1 g/dL 為 portal hypertensive physiology 的線索，並非特定肝硬化病名。Ascitic total protein ≥2.5 g/dL 在 **high SAAG** 情境支持 cardiac congestion，但應同時留意 mixed etiologies、BNP／echocardiography 與臨床先驗。
2. **PMN 是治療分流，不是病因證明：** PMN ≥250 cells/mm³ 在 cirrhotic ascites 應及早治療並考慮 SBP；若 traumatic bloody tap 須矯正，且 neutrophilic ascites 也可能由 secondary infection 或其他腹膜發炎造成。Culture negative 不應延遲必要 antibiotics；PMN <250 而 culture positive 的無症狀者通常重抽觀察，有感染症狀則臨床判斷處置。
3. **Runyon 2/3 只屬警訊，不能用來排除：** AFTP >1 g/dL、ascitic glucose <50 mg/dL、ascitic LDH > serum ULN，典型研究的目標是以 biochemical clues 識別可能的 bowel perforation 等 secondary peritonitis；不同研究的敏感度／特異度不一致，尤其在 baseline high-protein ascites 不宜將高蛋白理解為新發組織破壞的專一證據。需要合併 polymicrobial patterns、嚴重／持續腹痛、影像及 48h PMN 趨勢。首次 PMN 250 已足夠啟動合適治療，不可等待 2/3 才開始。
4. **治療雙軸：** 對 portal hypertensive ascites，moderate sodium restriction（一般以約 2 g sodium/day 級距討論）、利尿與尿鈉監測調整 Na balance；free-water restriction 不是每位腹水病人的常規。LVP 為 tense 或 refractory ascites 緩解機械負擔；超過 5 L 給 albumin **6–8 g/每 1 L 總移除量**，而非 5 L 後的增量，低於 5 L 若 hypotension／AKI 等高危因素需個別評估。
5. **SBP albumin 需交代人群與時序：** antibiotics 針對感染，albumin（常用 1.5 g/kg 診斷時／day 1、1 g/kg day 3）降低腎損害等風險；不同指南對高危選擇條件／廣泛使用略有不同。AASLD quality measures 強調早期使用，BSG 對 rising/elevated Cr 作較明確限定。不能將「SBP 需 albumin」誤讀為只要 albumin 濃度低就輸注或所有情境無條件適用。
6. **TIPS 與 transplant evaluation：** TIPS 減低 portal pressure，但須評估心臟功能、肺高壓、肝性腦病、感染與肝功能等風險；失代償／refractory ascites 的 transplant assessment 不可完全被藥物、放液或 TIPS 遮蔽。

## 在正式整合版加入的兩張**原創**圖（尚未製成公開成品）

**Figure A／同一管腹水的兩個正交提問。**
- 左欄：「形成機轉」：同時血清 albumin → SAAG ≥/<1.1 → 若 high SAAG 再看 AFTP <／≥2.5；病名只作例示，不畫互斥的確診樹。
- 右欄：「現在有沒有感染及是否有 secondary source」：PMN ≥/<250 × culture +/− 交叉矩陣；PMN ≥250 的即時 antibiotics；Runyon 2/3 + 臨床／影像警報再指向 source control；不將 Runyon 放在 SBP 的必要條件。
- 橫向疊合示例：自編 **SAAG 1.6、AFTP 1.8**，同時可低於 2.5 且高於 1；應用 1 g/dL cutoff 時須明言先有 suspected infected ascites，且 protein 單項不能確診 secondary infection。
- 不臨摹原表樣式，使用可以垂直堆疊的手機版卡片與清楚的 caption：「AI 原創示意；非 Pocket Medicine 原表」。

**Figure B／量太多 vs 有效動脈充盈不足。**
- 主因果路徑：portal HTN／splanchnic vasodilatation → ↓ effective arterial filling → RAAS/ADH → Na retention → ascites；並標明全身體液過多可以與 arterial underfilling 並存。
- 在不同因果位置放置 sodium restriction/diuretics（balance）、LVP（accumulated fluid）、albumin after LVP（circulatory protection）、SBP antibiotics + indicated albumin（感染 + 循環）、TIPS（portal hemodynamics）；圖中的箭頭不可暗示治療必須依序升級。
- 安全性註解：LVP albumin >5 L 計算依 total removed；重症 AKI/hyponatremia/HE 重新評估利尿，transplant referral 視情境另有路徑。
- 不臨摹 Pocket 原圖，caption 附書版與 PDF reader 頁數。完整的因果說明須存在主文，不可被圖取代。

## 可追溯外部來源

- [AASLD 2021 Practice Guidance｜Ascites, SBP and HRS](https://www.aasld.org/practice-guidelines/diagnosis-evaluation-and-management-ascites-spontaneous-bacterial-peritonitis)；[全文 DOI](https://doi.org/10.1002/hep.31884)。
- [BSG／BASL guideline｜Management of ascites in cirrhosis](https://pmc.ncbi.nlm.nih.gov/articles/PMC7788190/)；BSG 在 2024 年再次審閱且表示仍有效。
- [AGA Clinical Practice Update｜Ascites, volume overload, hyponatremia](https://gastro.org/clinical-guidance/management-of-ascites-volume-overload-and-hyponatremia-in-cirrhosis/)（2025；albumin per total liter removed）。
- [Runyon & Hoefs 1984｜ascitic fluid analysis and gut perforation](https://pubmed.ncbi.nlm.nih.gov/6724512/)；[Runyon prospective algorithm 1990](https://pubmed.ncbi.nlm.nih.gov/2293571/)。
- [2023 multicentre study｜SecP vs SBP, limitations of Runyon](https://pmc.ncbi.nlm.nih.gov/articles/PMC10000989/)。
- [ACG 2026 Clinical Guideline｜Preventive care for patients with cirrhosis](https://doi.org/10.14309/ajg.0000000000004186)：近期相關 key concept；不可據此取代完整肝病指引。

## 發行前不可略過

- [x] Git 原稿快照與版本來源身分
- [x] Pocket 9E PDF 指定原頁及表格目視查閱（無原像素公網複製）
- [x] 高風險 cutoff、治療門檻、albumin 劑量與 Runyon 限制的初步外部來源查核
- [ ] 作者 canonical 發表版本身分最終比對（若查無發表版，明示用戶提交版）
- [ ] 獨立建置完整 **AI-integrated** 連續敘事及 Figure A/B 原創圖
- [ ] 對圖建立出版來源頁、copyright disposition 與 `audit/figure-gate.json` review
- [ ] EPQC／必要時的獨立醫學審稿與 site build/CI 正式驗收
- [ ] 根據通過結果再加入 `site/pages.json`、唯一知識地圖的公開路線與 Cloudflare 部署
