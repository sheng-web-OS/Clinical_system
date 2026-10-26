# 2026-07-19 HBV phase / ALT：原稿附表核讀與出版界線（私人審查）

## 收件與身分
- 作者提供完整〈我們看見的是病程，還是病程留下的訊號？〉，2026.07.19 小麻閱讀（9E），已逐字保存於 [原稿接收檔](2026-07-19-hbv-signals-user-supplied.md)。
- 同則對話另附一張表格圖片，標題 **Phases of Chronic HBV Infection**，欄位：Phase、ALT (ULN)、sAg、DNA (IU/mL)、eAg、Liver histology (inflam/fibrosis)、Rate of cirrhosis。
- 對話上傳圖片（目前未複製進 Git）：檔名 `CF06F493-971D-4129-A6EE-0BCBA09E936F.png`；SHA-256 `80bd5f2e030e1a7c7d9e14eea60ec75a7a216848eec9b084985a68ca0ce97128`；大小 1114×516。此 fingerprint 僅作對話圖來源比對，**不表示原始像素已入庫**。
- 圖腳標示 *Adapted from Hepatology 2018;67:1560*，其文獻為 Terrault et al., AASLD 2018 Hepatitis B guidance, DOI 10.1002/hep.29800。作者稱來源為 Pocket Medicine 第九版；**尚未取得對應 PDF 原頁、實際書頁／圖表編號／完整圖說，故不能標記 Pocket 原頁逐圖對讀完成。**

## 對已提供圖片的可見內容核對（逐欄摘要，不作公網原圖重製）
| 表中列 | ALT | HBV DNA (IU/mL) | HBeAg | Histology | 表內 cirrhosis rate |
|---|---|---|---|---|---|
| HBeAg-positive infection / “immune tolerant” | normal | ≥10^6 | + | minimal | <0.5%/y |
| HBeAg-positive hepatitis / “immune active” | ≥2× ULN | ≥20,000 | + | moderate–severe | 2–5.5%/y |
| HBeAg-negative infection / “inactive carrier” | normal | ≤2,000 | − | minimal necroinflammation; variable fibrosis | 0.05%/y |
| HBeAg-negative hepatitis | ≥2× ULN | ≥2,000 | − | moderate–severe | 8–10%/y |
| Resolved | normal | not detectable in table | − | no inflammation | variable |

- 表註腳顯示 ALT ULN 男性 <35 U/L、女性 <25 U/L，不能當所有當代指引或檢驗室通用的正常值。
- 表內 **HBeAg-positive immune-tolerant 的 DNA 門檻 ≥10^6**，與 2025 AASLD/IDSA 定義 **>10^7 IU/mL** 不一致；治療／追蹤判斷應依查閱當下指引，不能從舊表直接轉成治療規則。
- **表中逐 phase 的 annual cirrhosis rates** 未查明原研究族群、追蹤期間、分母及診斷方式，不得直接作個別患者預後數值；本篇作者原稿未引用這些比率，維持不引用。
- 圖片來源是提供者對話截圖，不代表出版社允許公開轉載。**原書像素公網重製 = HOLD（rights assessment pending）**。

## 當代醫學核查：2026-10-26
1. AASLD/IDSA 2025 HBV guidance（2025-11-04 發布）：Phase 定義包含 immune-tolerant、immune-active、inactive、indeterminate；indeterminate phase 的人群可考慮 shared decision，持續正常 ALT 不可排除 significant fibrosis；對 immune-tolerant >40 歲或 ≥F2／顯著發炎可考慮治療，推薦為 conditional、證據確定性 very low。
   - https://doi.org/10.1097/HEP.0000000000001549
   - https://www.aasld.org/aasld-announces-new-practice-guideline-treatment-chronic-hepatitis-b
2. EASL 2025 HBV guideline：治療指示整合 HBV DNA、ALT、fibrosis 與 HCC/疾病進展風險；normal ALT **alone** 不足以拒絕治療，肝硬化及可偵測 HBV DNA 即是重要治療情境。
   - https://www.journal-of-hepatology.eu/article/S0168-8278%2825%2900174-6/fulltext
3. WHO 2024 HBV guideline：≥F2／肝硬化可不依賴 ALT/HBV DNA 決定抗病毒適應症；ALT 與 HBV DNA 為另一組條件，使用 WHO 指定 ULN（男 30／女 19 U/L），不能和 AASLD 表門檻混用。
   - https://www.ncbi.nlm.nih.gov/books/NBK614987/

## 原稿知識角色與嚴格界線
- **保留的主論點**：HBV DNA 表示病毒量，ALT 表示有限時窗內的 hepatocyte injury 生化訊號；phase 是 marker 組合和縱向資料的臨床推論，並非 direct observation；treatment threshold 不是疾病發生的生物學起點。
- **補充必要限定**：ALT 為 hepatocellular injury 指標但非 HBV-specific，正常不排除隱匿 necroinflammation／fibrosis；需要 longitudinal ALT/HBV DNA、fibrosis assessment、個別 HCC/其他風險與其他 ALT 異常原因。HBV DNA 高不等於組織發炎高，正常 ALT 不等於絕無肝細胞損傷。
- **出版規則**：保存作者原稿不暗改；若後續建立整合版，以獨立檔案註明現行指南、個體化適應症、圖表來源；原圖不經權利評估不得公網重製。不要以舊表 rate of cirrhosis 或舊版免疫耐受 DNA cutoff 直接驅動床邊治療。
- **目前狀態**：author manuscript = archived; supplied screenshot = visually reviewed in conversation / fingerprint recorded, **not stored as image asset in Git**; Pocket Medicine actual PDF page = not verified; copyright = pending; independent hepatology peer review = not completed; site/pages.json = not registered; production deployment = not requested/executed on this snapshot.
