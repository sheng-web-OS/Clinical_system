# 2026-07-23 cirrhosis｜原稿與小麻截圖交叉審查（2026-10-26）

## 身分、範圍與交付閘門

- 私人 source snapshot：`archive/xiaoma-reading/intake/2026-07-23-cirrhosis-user-supplied.md`。2026-10-26 使用者在對話直接提供全文，內文自述日期 2026-07-23。保持原論述，不把這份對話快照宣稱為已核對的 Facebook 發布 canonical version。
- 同一則訊息附一張 Pocket Medicine 9E 的「CIRRHOSIS」段落截圖，984×1536 JPEG，SHA-256 `f2d6123cbaa9fe2a48789be3c7efd902d626f7cf9071082c83d9c5ee45232c19`。已目視逐節讀取 **Definition / Etiologies / Clinical manifestations / Physical exam / Laboratory studies / Workup / Prognosis**。截圖不是完整 Pocket Medicine PDF，沒有直接取得同頁完整 PDF、印刷頁碼或附錄 Child-Pugh 表。
- 截圖影像**未**傳入此 Git branch，保留在使用者對話附件；不可宣稱原圖已嵌入網站。截圖屬受著作權保護的教科書內容，不因用於私人審查而可推定公開重製授權。
- 發布現況：**INTAKE ONLY / PUBLICATION HOLD**。不可在 `site/pages.json` 加此快照作 `historical_original`；待 canonical 來源認定、完整原書頁／圖表定位及臨床查核後才決定以原稿或獨立 AI-integrated 教材公開。
- 既有主分支接收台帳 `archive/xiaoma-reading/intake/2026-10-21-chat-manuscripts.md` 原列本稿 `conversation_only`；本次變更為 `source_snapshot_archived`，並不等於已經公開部署。

## 原稿對圖文字核讀

1. **病名與結構**：截圖定義直接將 fibrosis、regenerative nodules、hepatic vascular distortion 與 elevated portal pressure 聯結；原稿用來證明「共同結構不等於共同臨床表型」，屬 A（源文件已有）與 B（將列出的檢驗整成不同判斷軸線）。
2. **不等速後果**：截圖將 platelet、AST/ALT、bilirubin、albumin、PT/INR、Na、creatinine、variceal bleeding、ascites、encephalopathy 放在不同 sections，並無宣稱這些按線性先後順序發生。原稿提出的多軸模型為有根據的教學整合 B；仍須限制「fibrosis -> reserve 減少」不是每位病人等比例必然。
3. **工作流程**：截圖提到 U/S with Doppler、病因檢查、fibrosis biomarkers、elastography、biopsy (gold standard; not always needed)；原稿「gold standard 只回答 histology，不回答所有決策」與來源一致，但需要補充 biopsy sampling error 與 coagulopathy/ascites 使經皮 biopsy 風險不同；transjugular 是部分情境選項。
4. **Child-Pugh 與 MELD**：截圖把 Child-Pugh A/B/C 與 MELD-Na 或 3.0 同列 Prognosis，但二者含不同終點、不同臨床面向。原稿反對當成單一嚴重度量尺是合理的；「Child-Pugh 比較是描述當下臨床功能」不可否認它的預後用途。

## 2026 年重要補充、反例及發布前修正

| 層次 | 保留或補充 | 需要避免的錯誤推論 |
|---|---|---|
| 組織 / non-invasive risk | Baveno VIII 2026 明確區分 compensated cirrhosis（組織 / 臨床診斷）與 cACLD（風險連續體，非侵入性分類），二詞不可互換。LSM under fasting，單次 ≥10 kPa 應複測或與其他可靠 NIT 互證。 | cACLD ≠ 一定 biopsy-proven cirrhosis；肝硬度受發炎、鬱血、膽汁鬱積等因素干擾。 |
| 門脈高壓 | Baveno VIII 1.15–1.16：在 cACLD 中，LSM ≤15 kPa + platelet ≥150×10^9/L 可排除 CSPH（NPV >90%）；特定 viral/alcohol/nonobese MASLD 群 LSM ≥25 kPa 可確認 CSPH，不能外推所有疾病／體型。 | Platelet 低不是 CSPH 單獨確診；脾大或 varices 也不是已失代償。非肝硬化門脈高壓如 PSVD / vascular liver diseases 可有相似徵象。 |
| 失代償 / recompensation | Baveno VIII 3.1–3.3：首次失代償包括 portal hypertensive clinically evident ascites / hepatic hydrothorax、variceal bleed、overt HE（West Haven ≥II）。7.1–7.6：recompensation 必須病因有效控制、離開治療而腹水 / HE 解決、無相關再出血且維持 >6 個月、肝功能達 Child-Pugh A5/A6 水準等條件；與 histological regression 不同。 | **Varices without bleeding ≠ decompensation**；一兩天藥物控制腹水或 HE、Child-Pugh 改善 ≠ 已 recompensated。 |
| 功能與 coagulation | Albumin / bilirubin / INR 是功能、排泄與血流動力學相關訊號，各受非肝因素影響。截圖另有註記 `PT/INR (poor correlation w/ bleeding risk; factor VIII nl b/c not synthesized by liver)`。 | INR 升高不能直接推估自發出血率、也不能單靠 INR 決定術前矯正；肝硬化有 rebalanced hemostasis，不代表完全沒有凝血風險。 |
| FIB-4 / APRI | 利用常規生化與血小板估計 advanced fibrosis 的風險，解讀需病因、年齡、疾病活性與適用 cutoff；非 cirrhosis 確診試驗。 | 不要把特定 cutoff 直接轉譯為 portal pressure 或短期死亡危險。 |
| Child-Pugh | Bilirubin、albumin、INR 加上臨床 ascites、HE，兼有預後與臨床分類用途。 | 狀態改善不能解釋為 fibrosis 即時逆轉；也不能說它只描述症狀、完全沒有 prognostic value。 |
| MELD 3.0 | 2021 原始模型對 90-day mortality 建模，包括 female sex、bilirubin、INR、creatinine、sodium、albumin 及交互作用。移植分配應依所在國家與制度確認。 | 不要稱 MELD 3.0 僅為 bili/INR/Cr，也不能用低 MELD 排除重要 ascites/HE、HCC 或 HRS 等問題。|
| Biopsy | 當組織型態、未解病因或非侵入性結果衝突會改變行動，biopsy 才有增量決策價值。 | `Gold standard` 限定 histology，不是每人的 portal hypertension 分級或移植風險的唯一真相。 |

## 規範的證據定位（2026-10-26 可直接讀到之官方／原文）

- **Pocket Medicine 9E**：使用者提供的 CIRRHOSIS 單頁截圖，sections 如上；圖片 hash 見上。未取得完整 PDF、出版社公開重製授權或附錄表，故不宣告全圖／表 / footnote 門檻完成。
- **Baveno VIII – Advancing consensus in portal hypertension**, Journal of Hepatology, **published online 2026-08-19**, DOI `10.1016/j.jhep.2026.07.030`; especially **Panel 1 1.1–1.19**, **Panel 3 3.1–3.3**, **Panel 4 4.1–4.2**, **Panel 7 7.1–7.6**, **Panel 8 8.38–8.48**. Original open-access full text: https://www.journal-of-hepatology.eu/article/S0168-8278%2826%2902778-9/fulltext
- **MELD 3.0**: Kim WR et al. “MELD 3.0: The Model for End-stage Liver Disease Updated for the Modern Era.” Gastroenterology 2021;161:1887–1895.e4. Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC8608337/
- **AASLD 2021 Ascites, SBP, HRS guidance** (background and decompensation): https://www.aasld.org/practice-guidelines/diagnosis-evaluation-and-management-ascites-spontaneous-bacterial-peritonitis
- **Baveno VII** for historical contrast, not to replace newer Baveno VIII: https://pmc.ncbi.nlm.nih.gov/articles/PMC11090185/

## 最小下一步

1. 核對作者認可的 Facebook 完稿 / 發表身分，不能把使用者本次 conversation snapshot 靜默升成公開 historical original。
2. 補讀完整 Pocket Medicine 9E CIRRHOSIS 頁與 Child-Pugh appendix（現僅 JPEG 截圖）；不公開原圖像素，除非另行完成合法引用／授權評估。
3. 若要供網站正式閱讀，新增獨立 integrated 文章並將 **Baveno VIII 的 cACLD–CSPH–first decompensation–recompensation** 自然嵌入原命題，而非用勘誤附錄拼貼；保留作者 7/23 原稿不變。
4. 對已擬出版文章執行 EPQC/P0-P1 證據與版權驗收、site/pages.json、build/CI、Cloudflare 與實際 HTTPS 狀態查核，四者分別紀錄。此稿當次不進公開白名單。
