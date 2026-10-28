# 2026-10-28 Lab Medicine 01｜原始證據與缺口的可核對矩陣

狀態：作者執行脈絡之原始來源**局部目視與內容改寫紀錄**，**不是**獨立醫學／段落 EPQC 通過票據。
對應 Draft PR #186；本文件位於私有 `audit/`，不應成為公開 reader 正文。上一輪 HEAD `ce19fa1d23819b955721ad07da04a683a40f5756`，本次新增理論推導與來源註記後需重新取得 final HEAD blob 才能做獨立逐段審查。

## 原始來源：哪張表圖真的看過

| 內容/用途 | 實際核對範圍與來源 | 結果與限制 |
|---|---|---|
| AKI 定義、尿量與分期 | [KDIGO AKI 2012 原 PDF](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf)，印刷 p.19（PDF p.21，零起算）**Table 2**、正文 §2.1.1–2.1.3，實際畫面截圖核對 | Cr 1.16→1.68 的增量 0.52 mg/dL/約 24h 符合 Cr-AKI；若收集可信，240 mL/8h/75kg=0.4 mL/kg/h 且持續8h符合尿量條件。缺可信尿量則不能以尿量條件定案。Cr 已升不等於已知是 prerenal/overdiuresis。 |
| AKI 分期管理圖與處置限制 | 同 PDF 印刷 p.25（PDF p.27）**Figure 4: Stage-based management of AKI**；已目視框列、深淺色與 figcaption | Volume status/perfusion、藥物檢視、SCr/尿量監測是多階段管理；陰影是優先度，不是「每個病人都給 saline」或固定透析門檻。不在公開網站直接重製原圖。 |
| 偽高鉀／配對檢體核對 | [UKKA July 2026 official guideline PDF](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf)，印刷 p.14（PDF p.13，零起算），Guideline 15.3；已目視 | 對疑似偽高鉀，推薦採用 paired lithium-heparin / clotted serum specimen；本篇因明顯 hemolysis＋快速全新樣本驗證臨床推論，並未聲稱該案例完成完整 paired protocol；若仍有不一致應向檢驗室討論配對驗證。 |
| ECG、治療與風險 | UKKA 同 PDF 印刷 pp.14–15，Guidelines 14.1/14.2（p.13 與正式章節 p.64）、16.2a、16.3.1–.3、17.1–17.2；已目視 | 指引列 K 6.0–6.4 moderate，合併急性病、AKI 或快速升鉀需高警覺；16.2a 對有 ECG 變化的 calcium 建議於2026改 **2C**。Moderate insulin-glucose 為 suggested 2C；需要 glucose/K 適當監測；正常 ECG 非安全排除證據。 |
| 高鉀療法原始附錄表 | UKKA 同 PDF 印刷 p.162（PDF p.161）Appendix 1 insulin-glucose literature comparison **已目視** | 不把各小型研究觀察降鉀幅度套作本合成病例藥效，且未完成 Appendices 其他頁全部目視。公開只提供官方來源連結。 |
| BMP 檢驗錯誤 | Takieddine & El-Khoury, *AJKD* 2025;85(1):104–114; PMID 39396361; DOI 10.1053/j.ajkd.2024.06.019；[PubMed](https://pubmed.ncbi.nlm.nih.gov/39396361/)、[期刊摘要與搜索可讀正文](https://www.sciencedirect.com/science/article/pii/S0272638624009211) | 作者、期頁、abstract、preanalytical/analytical/postanalytical 對照確認；個別全文讀取端點曾回 403，**未完成所有原 Figure／Table 影像目視**。不能自填 Figure Gate「全部 represented」，亦不冒稱其病例提供本稿合成數據。 |

## 新發現的兩個教學缺口及已修改（未由獨立 reviewer 驗收）

1. 原文指出 serum CO₂20 不等於 pH，但缺同一張表的量化連結；已補入同時點 07:15 Na133−(Cl100+serum CO₂20)=13 mmol/L，明示這是 **uncorrected AG 的條件式近似計算**，albumin 未知且不能由此排除 lactic acidosis／混合障礙。
2. 原本真性 K6.4、AKI、ECG 無明顯變化的反事實，只說按指引分層，沒有交代 moderate 6.0–6.4 與 clinically ill / AKI 下為何不能明天再查；已據 UKKA 2026 指引補 clinical monitoring、insulin-glucose 為條件式選擇、血糖與 K 回測風險、不同病人不應套同一醫囑。

## 硬性 HOLD：下一個真正要做的事

- **同名衝突**：PR #181 含同名 pneumonia 版本。提案 #186 保留 Lab Medicine 01 唯一總論；#181 內容保留為獨立「另一種情境」候選、正式入口只能擇一。不得由 CI PASS 取代 owner coordination。
- **獨立來源＋教學審核**：下一次不同執行脈絡應重新讀取最終 blob 全文、這份 audit 和相關原始 PDF 並以盲式／對抗式逐段重新提出具體修改，修完再生成 exact-blob EPQC paragraph packet。不得由原寫稿脈絡直接發 `independent_ai_pass`。
- **Figure Gate**：原創病例三證據線已具資訊增量，但 AJKD 不完整原圖、Pocket 原圖相關性與權利仍需決定 source_link 或明確 HOLD。對合法來源與表圖的精確位置按 figure-gate 要求填寫，不可自評充數。
- **工程**：每次 source/blob 更新後需重跑完整測試及 site build；正式 manifest、來源頁與知識地圖、reader-specific 360／375／390px、CI head SHA、main merge、Cloudflare production 各自留紀錄。
- **考古題**：不得宣稱本稿已對應 113-1／115-2 真題，直到原卷與更正答案**目視**核定年度／梯次／醫學科目／題號；不以 PR #181 的機器索引冒充完成。

本輪工具未使用付費 TinyFish。病人/合成病例資訊全為教學。人工介入分鐘 NOT_MEASURED，未完成的獨立審查不算 0 次也不算成功。
