# E06 先導實驗｜Native GPT-6 → Clinical OS Lite 增量審查（2026-10-28）

**狀態：Artifact + retrospective pilot / NOT VALIDATED / NO PUBLICATION.**
**資料保護：只保留抽象化臨床特徵，不存病人姓名、病歷號、日期、原始影像或院內檔案。**

## 研究問題
在 GPT-6 已完成一次自發性氣胸 CBD 討論後，套用 Clinical OS v5.1 的原始來源回查、概念邊界、因果、反事實及證據審查，是否增加**有臨床意義的洞見**及**發現原回答沒有處理的證據缺口**？

本次不能回答「Clinical OS 是否因果性地優於 GPT」：同一對話已看到基準稿，並為增量審查加入額外文獻查核；非獨立上下文、非同工具預算、非盲評。

## 固定的既有 Native baseline（2026-10-28 同對話已發出的 CBD Discussion）
A 級既有洞見，不得重新認領：
1. 肺尖囊泡可提供解剖機轉，但不是已證明的破裂點。
2. 育齡女性＋右側氣胸＋月經同步＋既往氣胸史，需要釐清 catamenial pneumothorax；仍未證實。
3. 氣胸影像縮小與手術再發預防屬不同治療終點；既往氣胸側別／是否自發性尚未核對。
4. Wedge resection、pleurectomy、abrasion pleurodesis 的作用不同，不能據此排除胸腔子宮內膜異位。
5. 拔管前 air leak / 專屬引流量未取得，拔管後胸片不能反推決策當時的全部條件。
6. 原回答設定四個 Discussion：病因、選擇 VATS、手術目標、拔管。

## Enhanced pass（同一模型；ClinOS Lite 查核與來源限定）

| 審查項目 | 基準稿 | 增量發現 | 分類 | 是否已證實 |
|---|---|---|---|---|
| 既往與經期線索 | 已辨識，並保留不確定度 | 不新增核心病因結論；先核對既往側別和月經關聯 | A | 是：基準稿已有 |
| 2 cm 'bleb' 影像術語 | 直接沿用 CT 的 bleb | 形態學教科書通常稱 bleb <1 cm、bulla >1 cm。約 2 cm 的標記存在**術語不一致**，須核對完整影像和正式病理；不可僅用尺寸擅自改診斷。『2 cm』也不是氣胸寬度，且不能套用『>2 cm bullae recurrence』的關聯敘述 | D | 來源定義已查；個案病理未知 |
| 文獻估計量的血緣 | 原回答僅概括提 2026 回顧並警告觀察性研究，**沒有引用 17.3% 數字** | 2026 review 陳述 17.3% vs 54.2%，內文註明沿用 Elsayed 2022 meta，不是 2026 以 1,800+ 人重新計算；2022 meta 的荷爾蒙治療群 111 例，無治療比較數為 19/35，非隨機且有出版偏差。不該用 2026 樣本數為上述效應背書 | D（防未來錯誤） | 兩篇原文摘要＋2026 正文核對 |
| 反事實臨床決策 | 有談手術及胸管目標 | 若原先發作不屬自發性／沒有前次紀錄，引用「第二次同側或第一次對側」的手術指引前提改變；若仍有週期性胸痛／再發，既往手術成功不應終止對肋膜／橫膈病因的評估 | B/D | 條件式，不是本例已發生 |
| 術後追蹤的時間尺度 | 已談再發預防及婦科評估 | 將每次症狀與月經起始日做同期紀錄；第一年追蹤的週期性再發症狀值得作為專項，理由是可能仍有未處理的週期性胸腔病灶；**並非**直接建議本例使用賀爾蒙藥 | C（臨床問題增量） | 一般文獻支持，對此患者未確診 |
| 胸管是否符合安全拔除 | 已說明漏氣與胸片的資訊界線 | 原始資料缺 air leak chart，不能判定當時已滿足條件；不給『拔管成功』替代『拔管前條件已證』 | A | 是，沒有新增事實 |

## 真正可觀察的 pilot 結果
- **主要臨床議題保留：4/4**（病因、手術理由、手術內容、胸管）。
- **新增具文獻核對的限定：2 項**：2 cm bleb/bulla 術語；2026 回顧引用 2022 效果估計的來源血緣。
- **新增條件式臨床遷移題：1 項**：週期性術後症狀追蹤。
- **糾正基準稿中已明確說錯的重大醫學事實：目前 0 項已證實**。注意：預防未來引用錯誤，不等於「這次已攔截錯誤」。
- **獨立盲審者：0；隔離模型運行：0；原生 GPT 同等延長檢索預算控制：0；成本精算：未取回**。
- **判斷：該輪查核提供了增量限定，但沒有證明 Clinical OS 具因果性品質淨增益，或會在未提示下自動自糾。**

## 來源定位與查核深度
- BTS Pleural Disease guideline 2023, summary/full searchable text：<https://thorax.bmj.com/content/78/Suppl_3/s1.long>；<https://thorax.bmj.com/content/early/2023/08/08/thorax-2023-220304>（主要建議摘要）。用於 catamenial vigilance、第二次 ipsilateral／第一次 contralateral 可考慮手術。
- ERS/EACTS/ESTS 2024 guideline, original abstract + selected operative text：<https://pubmed.ncbi.nlm.nih.gov/38806203/>；<https://academic.oup.com/ejcts/article/65/5/ezae189/7682526>。早期手術 conditional，方法比較不確定。
- 2026 review, open-access full text，特別是 hormone table、limitations：<https://link.springer.com/article/10.1186/s13019-026-04227-1>。注意其 17.3% 效果引用 2022 meta，而非本回顧自行再 pool。
- Elsayed et al. 2022, PubMed abstract（**未查完整全文所有統計方法**）：<https://pubmed.ncbi.nlm.nih.gov/36179536/>。11 studies; 111 treated; 19/35 controls; author reported publication bias。
- ERS cystic lung disease educational review，形態學定義：<https://publications.ersnet.org/content/breathe/16/2/200041>；NCBI MedGen bleb <1 cm <https://www.ncbi.nlm.nih.gov/medgen/341774>、bulla >1 cm <https://www.ncbi.nlm.nih.gov/medgen/537120>。
- BTS Pleural Procedures 2023, drain removal：<https://thorax.bmj.com/content/78/Suppl_3/s43>。
- 個案病歷與前次去識別化 clinical_course_20261028.pdf 僅在使用者授權對話／Library 裡閱讀，**未存入本 repo**。

## 下次需要的真正受控 E06
- 在 3 個尚未曝光的新病例或臨床主題，預先固定原始來源包、來源深度、模型版本、思考 effort、工具/時間/token budget；使用**獨立模型上下文**跑 A Native、B Native+Evidence Gate、C Clinical OS Lite。臨床高風險硬性終止、次要增量按 A/B/C/D/X 評分，另一個未知來源手臂的 reviewer 對匿名稿盲審。
- 排除「多拿一份原始資料」或「有較長思考時間」造成的假增益。測量臨床 P0/P1、證據準確率、未提示下的錯誤偵測、條件反轉時改判、讀者遷移，以及人工介入次數／分鐘與工具 token 成本。
- E06 在完成上述資料前始終 **Design + retrospective pilot / NOT VALIDATED**；不得以本檔申請正文發布、對外宣稱胜出或刷新既有實驗總表的 Validated 狀態。
