# Chronic diarrhea｜原稿接收與 Figure 3-2 醫學核對（2026-10-26）

**狀態：已保存使用者完整原文；原圖視覺對讀已完成（限本次提供的截圖）；醫學來源初審；出版 HOLD。** 本紀錄是 AI 編輯審查而非獨立醫師審查。作者原稿日期：2026-07-21；本次接收：2026-10-26。

## 身分、版本與原文保全

- 使用者於 2026-10-26 直接提供全文〈找到腹瀉的類型，為什麼仍然沒有找到病因？〉、註明 2026.07.21 小麻閱讀（9E）。
- 此對話版本**不作改寫**，保存在 `archive/xiaoma-reading/intake/2026-07-21-chronic-diarrhea-user-supplied.md`。未查 Facebook 已發表作者 canonical 版，不能以本存檔冒認已確認的歷史最終刊登稿。
- 2026-10-21 接收清單曾列為 `conversation_only`；本輪由該狀態提升為 `source_snapshot_archived`，**不是** `content/xiaoma-reading/originals` 已核實、醫學通過或網站已發布。
- 本文與小麻原圖不存在本庫公網重製。傳入的截圖是一張 Pocket Medicine 9E「Chronic Diarrhea (>4 wk)」頁面影像；Git 僅保存可追溯的圖表要點與審查，不存該版權圖原像素。

## 已實際目視查閱：使用者提供的原書截圖

截圖含 `Chronic Diarrhea (>4 wk)` 標題、general evaluation、osmotic／secretory／functional／malabsorption／maldigestion／inflammatory 文字段落以及 **Figure 3-2 Workup of chronic diarrhea** 及流程圖框線、標註、公式。這是**使用者提供的單張頁面截圖**，不是已自行翻閱完整 PDF 或核對全章。截圖未提供可獨立驗證的原書 PDF 頁碼，應以 Figure 3-2、章名與版次定位，不捏造頁碼。

辨識到的原圖分岔：
1. Chronic diarrhea 先分辨「增加的 fecal fat」→ malabsorption / maldigestion，或 inflammatory signals（FOB / WBC / calprotectin / lactoferrin）→ inflammatory 原因路徑。
2. 當上述訊號不足主導時，計算 `stool osmotic gap = 290 − 2 × (stool Na + stool K)`；原書圖在 `<100` 一側標「Secretory or Functional」、`≥100` 一側標「Osmotic」。
3. 原圖下一步例示 stool culture、colonoscopy；依病史定向檢查（tissue transglutaminase antibodies、stool elastase、呼氣試驗、endoscopy、EUS），以及 lactose-free diet、laxative screen 等。這些框是**診斷分流示意，不是每位病人都應逐項進行的醫囑順序**。
4. 頁面文字的臨床線索有 fasting、nocturnal diarrhea、weight loss、藥物、手術、旅遊、免疫抑制、家庭史。原稿解讀「病史反覆修正條件機率」與原表一致。
5. 已讀到 Figure 3-2 標題與可見流程；完整原 PDF 的相鄰頁、圖表原始頁次、印刷註腳尚未獨立查全，故整篇公開圖表完整性驗收暫不宣稱完成。

## 醫學事實與需要在新版加入的限定（不竄改作者原文）

**A，原稿已建立的核心：** mechanism phenotype ≠ etiologic diagnosis；不同形態可能共存；calprotectin 不是病原或疾病確診；fecal fat 不等於 pancreatic insufficiency；長短 ileal disease 可同時改變膽酸進結腸與小腸膽酸儲備；不能單由低 gap 證實 functional/secretory 病因。

**B，原圖所隱含但原稿已精彩展開：** 初始 history 與 stool inflammatory/fat/water 的判別，不是線性把病人塞進互斥桶，而是持續改變下一項最具診斷效益的檢查。不得將這解讀為 AI 額外創見。

**D，公開新版必須在原稿外獨立限定：**

1. **原圖 gap 門檻是教學簡化，不可作排他規則。** 原書 Figure 3-2 使用 <100 與 ≥100；常見臨床解釋較偏向 **<50 mOsm/kg 支持 secretory**、**>100 或 >125 支持 osmotic**、中間灰區難以判定（不同資料使用閾值略不同）。`290` 是對腸道內容物與血漿近似等滲的推算，並非從糞便實測的 osmolality 自動相減；檢體存放發酵與污染可造成扭曲。**此項檢驗不是所有慢性腹瀉必做的一線篩檢**，也不是腹瀉原因的單獨判準。
2. **Secretory 與 functional 同枝，並不代表 low gap 可以支持功能性診斷。** IBS-D/functional diarrhea 的臨床診斷須有相容症狀及適當的排除目標，特別要評估 celiac disease、Giardia、bile acid diarrhea 等；腹痛與排便的關係是 IBS 與 functional diarrhea 鑑別的重要線索。AGA 2019 的適用對象為免疫正常、非血性 watery diarrhea ≥4 週及特定低風險條件；有 alarm signs 者不可直接套用該簡化路徑。
3. **Negative fecal calprotectin 不是「腸黏膜沒有疾病」。** Calprotectin/lactoferrin 用於篩選 IBD，但 microscopic colitis 常有正常肉眼 colonoscopy，且低/正常 fecal markers 無法可靠排除；持續不明 watery diarrhea 按適應症做結腸左右側 biopsies。FOB/FIT 反映出血訊號，不等於 neutrophil-associated inflammation，亦不能用來排除非出血性病變。
4. **脂肪訊號不直接定位 pancreatic enzyme、bile pool 或 enterocyte。** 定性 stool fat 與真正 steatorrhea 的程度/飲食取樣、fecal elastase 及腹瀉樣本稀釋的假性偏低等都需要判讀。本文不應把任何單一 stool marker 升級為特定病名。
5. **Fasting/nocturnal 是臨床線索，不是二分確診。** Secretory diarrhea 經 fasting 通常持續，但不保證完全不變；晚間腹瀉較應提高器質病變懷疑，並不是 IBS 絕不夜間發作。
6. **Terminal ileal loss 的雙路徑是重要反例，但不是固定切除長度＝固定表現。** Ileal disease/resection 可造成較多膽酸達結腸刺激分泌；廣泛病變可耗損 circulating bile-acid pool、造成 steatorrhea。表現仍受剩餘腸長、發炎、飲食及菌叢等因素影響；不能單靠「短／長」診斷。
7. **臨床安全前置：** 血便、發燒、脫水或血流動力學問題、進展性體重減輕、貧血、免疫不全、可疑新發腫瘤情境，需先進行適當風險分流與檢驗，不應為等待 gap/型態鑑別而延誤處理。

**X／未完成：** 尚未取得作者 Facebook canonical 版本、此書完整相鄰 PDF 原頁與頁碼、獨立胃腸科醫師逐項審查，亦未執行合格讀者測試；不可宣稱上述已通過。

## 外部對照來源（已閱讀公開全文或摘要與主要推薦）

1. **AGA 2019** — [Laboratory evaluation of functional diarrhea and IBS-D](https://gastro.org/clinical-guidance/laboratory-evaluation-of-functional-diarrhea-and-diarrhea-predominant-irritable-bowel-syndrome-in-adults-ibs-d/)：calprotectin/lactoferrin、Giardia、IgA tTG/IgA deficiency、bile acid diarrhea 檢查。指南有嚴格適用範圍，並非所有慢性腹瀉。
2. **BSG 2018, 3rd ed.** — [Guidelines for the investigation of chronic diarrhoea in adults](https://gut.bmj.com/content/early/2018/04/13/gutjnl-2017-315909)：fecal calprotectin、bile acid diarrhea 的檢查、排除 microscopic colitis 的左右側 colonic biopsies。
3. **Sweetser 2012** — [Evaluating the Patient With Diarrhea: A Case-Based Approach](https://pmc.ncbi.nlm.nih.gov/articles/PMC3538472/)：示例性 diagnostic phenotype、osmotic gap、fasting 與理學邏輯。引用其個案情境需明確標記出版病例而非使用者親見病例。
4. **Camilleri et al. 2017** — [Pathophysiology, Evaluation, and Management of Chronic Watery Diarrhea](https://pmc.ncbi.nlm.nih.gov/articles/PMC5285476/)：watery diarrhea 多機制重疊、osmotic gap 分類驗證不足、轉運/蠕動交互作用。
5. **BSG 2003（舊版，僅作方法學史）** — [Investigation of chronic diarrhoea](https://gut.bmj.com/content/52/suppl_5/v1)：gap 常見 <50 與 >125 解釋，臨床效度證據有限；**不得把過時指南當現行臨床流程**。

## 圖像與發布決策

- **私人圖對讀：** 本對話附有原頁截圖，本文記錄 Figure 3-2 重要上下游分支；**截圖未複製進 repo**，並未公開。
- **公開圖片權利：** `link_or_original_only`（2026-10-26）：Pocket Medicine 為受著作權保護的商業醫療工具書，使用者提供截圖不等於公開重製授權；原書原像素暫不納入站點。新版若發布，使用原創「觀察訊號→待解生理問題→定向病因調查」圖，不逐格描摹原圖，並提供 Pocket Medicine 9E Figure 3-2 定位與合法出版社入口。
- **目前未建 `site/pages.json` 條目，未進入公開 HTML、CI／Cloudflare 驗證。** 本次只完成可追溯接收與第一輪 evidence audit。若要正式發布，先形成獨立 `integrated/` 教材（可選保留原稿作歷史典藏），完成來源頁、原創圖、figure gate、醫學審核與 build。未授權自稱作者正式改稿。

## 最小行動項（以免增加維護系統）

- [x] 完整 source snapshot 入私有 Git，與正式作者 originals 分開。
- [x] 對本次提供 Figure 3-2 截圖目視分支與標題，記錄公開權利邊界。
- [x] 檢核五篇外部指南／評論或方法學來源，指出會實際改變臨床推論的 D。
- [ ] 補齊原 PDF 完整頁碼／註腳與出版者來源定位，並比對 canonical 已發表版本身分。
- [ ] 獨立整合稿和具解釋力的原創圖；不以原圖像素公開重製。
- [ ] 通過 publication gate、CI/建站、部署後逐頁 HTTP 驗收，再回報正式網站連結。
