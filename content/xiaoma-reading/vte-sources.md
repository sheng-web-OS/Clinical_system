# VTE：預防整合、診斷分流｜來源與原圖審查

**來源身分。** 本篇初始文章為使用者於 2026-10-26 對話中提供的〈同樣屬於 VTE，為什麼可以一起預防，診斷卻必須分開？〉，標示 2026.07.24 小麻閱讀（9E）。已逐段保存在私有 `archive/xiaoma-reading/intake/2026-07-24-vte-user-supplied.md`；尚未以 Facebook 發表版本或公開網址核實作者 canonical 身分。網站整合稿是另加圖的編輯版本，不改動私有底稿。

## 小麻原書核讀範圍

《Pocket Medicine: The Massachusetts General Hospital Handbook of Internal Medicine》，第九版；使用者上傳之 Flatten PDF 共 463 頁。已以 PDF 文字層核對：

- **PDF 第 97 頁**（VTE definitions、Virchow’s triad / risk factors、原始 `Thromboprophylaxis` 表）。原表以 patient/situation 對 prophylaxis；依情境調整 anticoagulation 與 mechanical prophylaxis，而非一張所有疾病通用的單一醫囑。此處有原始 **prophylaxis table**。
- **PDF 第 98 頁**（`Modified Wells Pretest Probability Scoring of DVT`；`Figure 2-2 Approach to suspected DVT`；PE signs 與 PE Wells 的開頭）。原文指出 DVT Wells 對門診病人的效用較好，住院者適用性有限；並區分 proximal ultrasound 的限度。
- **PDF 第 99 頁**（PE Wells 分數的續表、`Figure 2-3 Approach to suspected PE`、D-dimer、CTA、下肢 US 的診斷角色）。原文強調 CTA 陰性/陽性與 clinical suspicion 是否 concordant 的重要性。
- **PDF 第 100 頁**（高風險 PE 的 hemodynamic risk stratification、初始治療與 thrombolysis 概論）。

**圖像查核狀態：待補。** 上述四頁的 PDF 文字及圖表標題已取回，但原始 Figure 2-2、Figure 2-3 的圖像在本次檔案讀取時未能顯示，**未完成對分支箭頭、caption、footnote 與每個停止節點的目視核對**。因此三張新圖只可以說是依已核文字與外部指南原創的教學概念圖；不可說「原圖已核對」或把本文放進 `site/pages.json` 的正式出版 allowlist。

## 現行外部指引及其限制

1. NICE guideline NG158, *Venous thromboembolic diseases: diagnosis, management and thrombophilia testing*. Official recommendations: https://www.nice.org.uk/guidance/ng158/chapter/recommendations
   - DVT 2-level Wells：likely ≥2；unlikely ≤1；PE 2-level Wells：likely >4；unlikely ≤4。這兩張都是 **suspected disease 的 pretest**，不是住院 thromboprophylaxis 風險分數。
   - DVT high likelihood → proximal ultrasound；若 initial proximal US negative 但 D-dimer positive，repeat scan **6–8 days later**。若 whole-leg US 或不同方案，不能不加限定照搬。
   - PE likely → CTPA（或依適用條件選 alternative imaging）；PE unlikely → D-dimer 檢驗及後續分流。嚴重不穩定的 PE 病人不能一律照搬穩定門診規則。
2. ASH 2018 *Prophylaxis for Hospitalized and Nonhospitalized Medical Patients*: https://pmc.ncbi.nlm.nih.gov/articles/PMC6258910/
   - Hospitalized medical patients 需同時評估 VTE 和 bleeding risk；bleeding risk acceptable 時通常偏向 pharmacologic prophylaxis；若不能用藥，可選 mechanical prophylaxis。不同專科、手術、急性腦出血等情境不能一律套用。
3. European Society of Cardiology / European Respiratory Society 2019 guideline, acute PE: https://academic.oup.com/eurheartj/article/41/4/543/5556136
   - PE 需先分辨 hemodynamically unstable/high-risk pathway 與 stable diagnostic pathway；床邊評估、緊急治療與確診影像的時序依病人狀態決定。

## 新增圖與原書元素的對照

| 原創圖 | 圖形應傳達的不可省略差異 | 教學來源 | 未能推論 |
|---|---|---|---|
| Figure 01 · Shared substrate | Virchow triad → 形成血栓的共同上游 → DVT/PE 可能呈現；不存在 DVT 必然進展 PE 的直線 | PDF p97 definitions / risk factors / prophylaxis table；ASH ppx | 不能以血栓背景判斷目前是否存在 DVT/PE；不給預防劑量 |
| Figure 02 · Two hypotheses | 同樣 risk factors，腿部與心肺症狀產生不同的 competing diagnoses 和 Wells pretest | PDF p98 DVT Wells、p98–99 PE Wells | 不是可以替代 Wells 原表的完整計分器；不能直接套用住院與特殊族群 |
| Figure 03 · D-dimer/stop | D-dimer 是定位能力低的纖維蛋白分解訊號；診斷演算法由 pretest probability 決定排除／成像；CUS 與 CTPA 有不同陰性邊界 | PDF p98–99 Fig 2-2/2-3 文字定位；NICE NG158 | 尚未核對 Fig 2-2/2-3 原圖；不是完整 algorithms，無法取代臨床判斷 |

**醫學需要主動保留的例外：** (a) hemodynamic instability / high-risk PE 優先急救，不等待正常 D-dimer 流程；(b) negative proximal ultrasound ≠ negative whole-leg ultrasound；(c) 若 PE 不能直接做 CTPA，V/Q scan 及有時候確診 proximal DVT 都可能影響是否需要 CTPA，但不能把腿部 US 寫成能顯示肺動脈 filling defect；(d) 若已使用 anticoagulation、症狀持續時間異常或 D-dimer test sensitivity 有限制，陰性解讀需小心。

## 公網著作權處置與發行狀態

- 原書 Figure 2-2／2-3、prophylaxis table **未重製／未公開**；其出版用權利評估仍未完成。
- 本文三張 HTML/CSS 概念圖均為原創，沒有描摹原書幾何路線或逐欄複製計分表。
- **Status: DRAFT / FIGURE-CROSSCHECK-PENDING / NOT PUBLISHED.** 此狀態是醫學出版程序要求，不可藉由 CI 通過或補填 audit marker 取消。確認原圖的分支、caption、腳註與當代 NICE/ASH 分歧後，才進行正式發布審查。
