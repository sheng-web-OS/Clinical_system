# 2026-10-28 Lab Medicine 01｜原始證據與缺口的可核對矩陣

狀態：作者執行脈絡之原始來源**局部目視與內容改寫紀錄**，**不是**獨立醫學／段落 EPQC 通過票據。
對應 Draft PR #186；本文件位於私有 `audit/`，不應成為公開 reader 正文。上一輪 HEAD `ce19fa1d23819b955721ad07da04a683a40f5756`，本次新增理論推導與來源註記後需重新取得 final HEAD blob 才能做獨立逐段審查。

## 原始來源：哪張表圖真的看過

| 內容/用途 | 實際核對範圍與來源 | 結果與限制 |
|---|---|---|
| AKI 定義、尿量與分期 | [KDIGO AKI 2012 原 PDF](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf)，印刷 p.19（PDF p.21，零起算）**Table 2**、正文 §2.1.1–2.1.3，實際畫面截圖核對 | Cr 1.16→1.68 的增量 0.52 mg/dL/約 24h 符合 Cr-AKI；240 mL/8h/75kg 的平均值為 0.4 mL/kg/h，但**8 小時總量不足以單獨證明連續 6 小時**區間符合尿量條件；須核對分時紀錄、採集完整性，才可判斷 KDIGO 尿量條件。Cr 已升不等於已知是 prerenal/overdiuresis。 |
| AKI 分期管理圖與處置限制 | 同 PDF 印刷 p.25（PDF p.27）**Figure 4: Stage-based management of AKI**；已目視框列、深淺色與 figcaption | Volume status/perfusion、藥物檢視、SCr/尿量監測是多階段管理；陰影是優先度，不是「每個病人都給 saline」或固定透析門檻。不在公開網站直接重製原圖。 |
| 偽高鉀／配對檢體核對 | [UKKA July 2026 official guideline PDF](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf)，印刷 p.14（PDF p.13，零起算），Guideline 15.3；已目視 | 對疑似偽高鉀，推薦採用 paired lithium-heparin / clotted serum specimen；本篇因明顯 hemolysis＋快速全新樣本驗證臨床推論，並未聲稱該案例完成完整 paired protocol；若仍有不一致應向檢驗室討論配對驗證。 |
| ECG、治療與風險 | UKKA 同 PDF 印刷 pp.14–15，Guidelines 14.1/14.2（p.13 與正式章節 p.64）、16.2a、16.3.1–.3、17.1–17.2；已目視 | 指引列 K 6.0–6.4 moderate，合併急性病、AKI 或快速升鉀需高警覺；16.2a 對有 ECG 變化的 calcium 建議於2026改 **2C**。Moderate insulin-glucose 為 suggested 2C；需要 glucose/K 適當監測；正常 ECG 非安全排除證據。 |
| 高鉀療法原始附錄表 | UKKA 同 PDF 印刷 p.162（PDF p.161）Appendix 1 insulin-glucose literature comparison **已目視** | 不把各小型研究觀察降鉀幅度套作本合成病例藥效，且未完成 Appendices 其他頁全部目視。公開只提供官方來源連結。 |
| BMP 檢驗錯誤 | Takieddine & El-Khoury, *AJKD* 2025;85(1):104–114; PMID 39396361; DOI 10.1053/j.ajkd.2024.06.019；[PubMed](https://pubmed.ncbi.nlm.nih.gov/39396361/)、[期刊摘要與搜索可讀正文](https://www.sciencedirect.com/science/article/pii/S0272638624009211) | 作者、期頁、abstract、preanalytical/analytical/postanalytical 對照確認；個別全文讀取端點曾回 403，**未完成所有原 Figure／Table 影像目視**。不能自填 Figure Gate「全部 represented」，亦不冒稱其病例提供本稿合成數據。 |

## 2026-10-28 第二輪逐圖回看：UKKA 五步驟與 insulin-glucose 原表

已實際目視以下原始 PDF 畫面，並與正文增補互證。這是作者側 source-verification，**非獨立 Figure Gate PASS**。

- **UKKA July 2026 Figure 4，印刷 p.75（PDF 索引 74）**：[官方 PDF 原圖](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=75)，實際畫面含一組由心肌保護→shift→remove→K/glucose monitor→prevent recurrence 的五階段階梯。原圖註明必須完成適用的後續環節；**不是**「所有 K6.4、ECG 正常者都要給鈣」的醫囑算法。本文新反事實依其意涵說明真性高鉀不可只靠 insulin 的暫時 shift。
- **UKKA July 2026 Table 22，印刷 p.98（PDF 索引 97）**：[官方 PDF 原表](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=98)，逐項載明 treatment-before glucose、insulin-glucose、條件式後續葡萄糖、鉀與血糖重測；原表下方額外提醒腎衰竭患者的補液體積限制、重複胰島素易低血糖。正文以判斷與監測邊界而非固定處方劑量呈現，避免跨國 protocol 套用。
- **KDIGO AKI Table 2 印刷 p.19 / Figure 4 印刷 p.25**：本次 web 原 PDF 畫面已再次目視，分別為 AKI stage based on measured creatinine/urine and stage-based management priority shading；正文不重製圖，避免將 shading 誤解為所有病人都需相同補液。
- **AJKD 2025**：PubMed 與 ScienceDirect 可讀文本/figure caption 確認書目、TTP Figure1 描述；其 PDF 原畫面在此回合下載端點 403，故不能宣告 Figure1/2 等原像素已目視。正文不使用該圖；保留公開期刊網址作合法原站來源。

## Mobile prepublication engineering QA（非發布）

在 CI [#40608142986](https://github.com/sheng-web-OS/Clinical_system/actions/runs/40608142986) 已執行獨立 `tools/qa_lab_morning_draft.py` 私人 browser：它以 **`site/build.py:Renderer` 和 `render_reader`** 渲染未進 manifest 的文章，讀入網站真實 CSS，測 360/375/390/1280px。四種寬度均沒有整頁水平溢出，table 在容器內捲動，病例三證據格呈現直排或並排。Screenshot/artifact 已取回並目視 mobile 375、desktop 1280：375 版元素局部 screenshot 顯示一處「跳到正文」固定連結疊圖疑似 Chromium element screenshot clipping artifact；比對同次 viewport screenshot 不含這個疊字。QA 程序後續修改為先拍 true top viewport、另拍 figure viewport，並修正不恰當的 `missingZhGlyph` 欄名；修訂後仍需再次查 CI。這不是已發布站的 360/375/390 畫面驗證，也未產生獨立教學理解通過票。

## 新發現的兩個教學缺口及已修改（未由獨立 reviewer 驗收）

1. 原文指出 serum CO₂20 不等於 pH，但缺同一張表的量化連結；已補入同時點 07:15 Na133−(Cl100+serum CO₂20)=13 mmol/L，明示這是 **uncorrected AG 的條件式近似計算**，albumin 未知且不能由此排除 lactic acidosis／混合障礙。
2. 原本真性 K6.4、AKI、ECG 無明顯變化的反事實，只說按指引分層，沒有交代 moderate 6.0–6.4 與 clinically ill / AKI 下為何不能明天再查；已據 UKKA 2026 指引補 clinical monitoring、insulin-glucose 為條件式選擇、血糖與 K 回測風險、不同病人不應套同一醫囑。

## 硬性 HOLD：下一個真正要做的事

- **同名衝突，現已在草稿階段修復**：PR #181 已由其編輯脈絡將 pneumonia/hypotension/oliguria 另案更名，維持 Draft/HOLD，#186 保留唯一 Lab Medicine 01 總論候選。發布前仍須核對兩邊 HEAD／原檔 title 與 main manifest，禁止競爭性 overview。
- **獨立來源＋教學審核**：下一次不同執行脈絡應重新讀取最終 blob 全文、這份 audit 和相關原始 PDF 並以盲式／對抗式逐段重新提出具體修改，修完再生成 exact-blob EPQC paragraph packet。不得由原寫稿脈絡直接發 `independent_ai_pass`。
- **Figure Gate**：原創病例三證據線已具資訊增量，但 AJKD 不完整原圖、Pocket 原圖相關性與權利仍需決定 source_link 或明確 HOLD。對合法來源與表圖的精確位置按 figure-gate 要求填寫，不可自評充數。
- **工程**：每次 source/blob 更新後需重跑完整測試及 site build；正式 manifest、來源頁與知識地圖、reader-specific 360／375／390px、CI head SHA、main merge、Cloudflare production 各自留紀錄。
- **考古題**：不得宣稱本稿已對應 113-1／115-2 真題，直到原卷與更正答案**目視**核定年度／梯次／醫學科目／題號；不以 PR #181 的機器索引冒充完成。

本輪工具未使用付費 TinyFish。病人/合成病例資訊全為教學。人工介入分鐘 NOT_MEASURED，未完成的獨立審查不算 0 次也不算成功。
