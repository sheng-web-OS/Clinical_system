# Lab Medicine Pilot｜初稿來源稽核與發布閘門（2026-10-27）

## 狀態
Issue #180。四篇新 AI 教材目前在私有 feature branch，**DRAFT / HOLD**；本紀錄是撰稿脈絡內的初步自我校核，**不等於獨立審查或正式 release receipt**。不修改 site/pages.json、不更動現有 09:00 任務。

## 已核對來源與存取層級
- NICE AKI NG148（直接讀取建議文字）：https://www.nice.org.uk/guidance/ng148/chapter/Recommendations 。成人 SCr 48h +26 µmol/L、7d +50%、尿量 <0.5 mL/kg/h >6h；尿液 dipstick；超音波不是所有 AKI 都需例行安排。
- KDIGO AKI 官方頁（已核讀）：https://kdigo.org/guidelines/acute-kidney-injury/ 。2026 AKI/AKD 仍是 public-review draft，未正式出版。
- UK Kidney Association hyperkalemia 官方頁（已核讀）：https://www.ukkidney.org/health-professionals/guidelines/treatment-acute-hyperkalaemia-adults-0 。已開啟 July 2026 官方 PDF 180 頁，目視核對印刷第 7、14、15 頁（viewer pages 6、13、14），包含假性高血鉀 Guideline 15.3 的成對 heparin plasma / clotted serum、16.2-16.6 的重要安全處置與 17.1-17.2 重測及血糖監測；**沒有完成完整 Appendix 原圖分岔與台灣院內劑量審核**，稿件因此不提供固定劑量。
- BMJ 2026 急性高血鉀診療可見 HTML（已核讀）：https://www.bmj.com/content/394/bmj-2026-100287 。ECG 不能敏感排除，高風險立即處置與確認需並行。
- AHRQ PSNet 2017 Hemolysis Holdup（真實案例及專家評論全文已核對）：https://psnet.ahrq.gov/web-mm/hemolysis-holdup 。72M，K 7.4（溶血）→重驗 8.4，等待期間惡化與 cardiac arrest；不能用 case report 外推一般發生率或治療效果。
- Kanjee/Lippi/Freed 2026 Mayo Clin Proc（PubMed abstract/出版商 highlights，未取得訂閱全文逐頁）：https://pubmed.ncbi.nlm.nih.gov/42134749/ 。體外溶血、EDTA clumping、heparin-line 與凝血採樣干擾。
- Shean 2025 IV fluid contamination（可見正文）：https://jlpm.amegroups.org/article/view/10562/html ；ADLM vascular-line phlebotomy 教學資料（可見網頁）：https://myadlm.org/science-and-research/clinical-chemistry/clinical-chemistry-trainee-council/pearls-of-laboratory-medicine-in-english/2016/collecting-blood-from-patients-with-vascular-lines 。
- 2026 BMP IV contamination rules study（僅 PubMed abstract）：https://pubmed.ncbi.nlm.nih.gov/42275628/ 。異常告警有真正病理/治療效應造成者，不能視為已驗證本院工具。
- Choosing Wisely Canada Using Labs Wisely（網頁）：https://choosingwiselycanada.org/hospitals/labs-test/ 。反對穩定患者無理由 routine daily CBC/chemistry；不能外推到不穩定病人。
- KDIGO 2027 CKD medication focused update 2026-10-15 起公開審查，尚未正式生效：https://kdigo.org/kdigo-2027-ckd-guideline-focused-update-public-review-open/
- 已讀到本庫 115 年第二次醫師二階醫學（三）Q26：2026-s2-med3-q26，答案欄為 B；本次額外目視查核考選部官方試題 PDF 第 6 頁、標準答案 PDF 及更正答案 PDF：Q26 = B（vasopressin），且更正未涉及 Q26；原始 machine_parsed_visual_and_medical_review_pending 狀態屬資料檔原先 QA 狀態，不可因此聲稱所有題庫已驗證。

## 自行計算核對（非獨立審稿）
- UO：170mL/8h/70kg = 0.304 mL/kg/h；SCr 1.0→1.7 mg/dL，已符合 AKI stage 1 的功能條件。
- 07:00 AG = 134 − (102+18) = 14 mmol/L；albumin 2.8 g/dL 校正粗估 14 + 2.5×1.2 = 17。不可把校正 AG 當病因確診。
- 修訂後自編 ABG 與 07:00 生化同步採檢；pH 7.33、PaCO2 35、計算 HCO3 約 18，Winter 1.5×18+8±2=33–37。這是近似對照，不可拿非同步結果宣稱已完全辨識混合障礙。
- ANC = 17.5×0.88 = 15.4 ×10³/µL；WBC 3×0.10=ANC0.3 ×10³/µL。
- glucose 210 與 Na 133：ESE 2014 指引採 +2.4 mmol/L per 100 mg/dL，校正 133+2.4×1.1=135.64；Katz 常見 +1.6 算式得到 134.76。正文現已並列兩個近似式、明示來源與 2014 勘誤；不可把估值當真實張力或診斷。
- 已明確區分生化檢體 hemolysis 與 CBC 不同管別／方法；採檢後改變可能和真正疾病變化並存。

## 獨立發布閘門／待辦
1. 逐段 reviewer **必須與寫作者分離**，覆蓋每段 reader gain、redundancy、推論界線、EPQC A–G 與危險反例；此文件不能自簽 independent_ai_pass。
2. 高風險來源補查：2026 UKKA 高血鉀原 PDF 未讀的完整 Appendix 算法／2026 KDIGO 草案 vs 正式；Q26 題圖／官方答案 PDF；以及若新增精確治療劑量必須正式逐項審。
3. 使用 repo tooling 實際完成 python site/semantic_gate.py --packet、獨立 receipt、python tools/validate.py、bash tools/build_site.sh；手機 360/375/390px 與相互連結，不能只用 Markdown 已寫入假稱驗收。
4. 所有新公開教材必須先過 site/pages.json allowlist 的編輯發布流程；目前不提交出版 manifest。
5. Pilot 後以未見病例驗證理解遷移、重大安全錯誤、編輯返工次數與使用者投入；AI 自評不是教學效果。

## 歷史候選（已完成初稿）
原先規劃的 SCr/BUN/eGFR、尿量與 urine sediment 單元已在同分支成稿；後續應審稿和驗證，不應再依這段歷史安排重複寫作。

**最終狀態：HOLD。早期文章版本已有 GitHub Actions build success，但最新版文章／來源審查仍需依 exact SHA 讀回，且無獨立醫學與逐段語義審查、正式發布或讀者學習成效的合格證據。**

## 第三篇 AKI/SCr-urine 前期核對（新增，仍 HOLD）
- 新篇：content/xiaoma-internal-medicine/lessons/2026-10-27-lab-medicine-aki-creatinine-urine.md，三個病例均標示自編、不混為單一人。
- NICE NG148 官方完整 HTML：尿試紙、是否做超音波與感染阻塞的 6h、原因不明或阻塞風險 24h；NICE 的資源時間門檻需在台灣按醫療情境評估，不可機械外推。
- KDIGO 2024 CKD 官方摘要與 Ann Intern Med synopsis：eGFRcr/cys 與 chronicity 的適用脈絡，不可將急速變化的 eGFRcr 當作當下直接測量 GFR；2026 AKI 公開草案未升格。
- Meta-analysis 2024 (PMID 38768779) 與 2026 BMJ Open (DOI 10.1136/bmjopen-2025-100875) 對 FEUrea 的估計與研究選擇不一致；正文明確只稱中等/有限診斷資訊，不能單憑尿電解質決定是否繼續補液。
- 腎臟數學初驗：SCr 1.0→1.8 為 1.8 倍、1.1→2.0 為 1.82 倍、1.6→1.9 是 48h 上升 0.3，均符合相應功能性 AKI 判準。這些是自編場景，stage 不等於確定 tubular injury。
- 113-1 醫學（三）Q29 已目視核對考選部原題 PDF 第 8 頁、標準答案 PDF Q29=D；該年度更正表尚未成功取得。115-2 醫學（三）Q28 已目視核對原題 PDF 第 6–7 頁、標準答案與更正表 Q28=A，沒有更正；仍不代表醫學逐段獨立審查完成。
- 內部相對連結到早晨 Lab、既有利尿劑文章已讀回存在；讀者閱讀成效／獨立審查／正式發布仍全數待證。
- P1：獨立醫學 reviewer 再審可能過度簡化的 AKI staging、urine sediment specificities、FEUrea pooled estimates、動態 eGFR 與心衰去充血；未經放行不得合併。

## 第四篇 CBC/DC 判讀：來源、數學及真題 (新增)
- 正文：content/xiaoma-internal-medicine/lessons/2026-10-27-lab-medicine-cbc-differential.md；以 2024 年已發表 pseudothrombocytopenia 案例作起點（13-year-old，EDTA 17K、citrate 55K、heparin 175K；PMID39582446，只核 PubMed abstract）；其他教學病例明示自編，不融合病例身份。
- CBC 的三系列與 reticulocyte/RDW、ANC/AEC 解讀參考開放全文 2026 JMA J CBC practice framework（PMCID PMC13639491），2026 smear-review 實務文（PMCID PMC13555154）與 NCBI StatPearls 可見全文；圖像未取得合法再製／授權，不宣稱已目視核對所有 Figure。
- 讀數核算：WBC18 × 90%=ANC16.2k/µL；WBC1.2×90%=1.08k；WBC3×10%=0.30k；WBC14,200×25%=AEC3550/µL；retic3%×Hct21/45=1.4%（純示例，不能單以 corrected % 診斷 hemolysis）。
- 111 年第二次醫學（三）Q46，考選部官方原題第 11 頁、標準答案與更正表**已目視核對**：答案 D（BAL），該題未更正；112 年第一次醫學（三）Q28，官方原題第 6 頁、標準答案與更正表**已目視核對**：答案 C（eculizumab），該題未更正。兩題涉及鑑別與高風險用藥，**本稿僅連結生理判讀，不把舊考題推論為現行治療指南或完整逐項詳解**。
- 所有四篇的相對內部連結（包含先備教材、利尿舊文及 national-exam anchor）均以 GitHub API 逐一核對存在；這不是網站建置或行動版驗證。
- **HOLD 持續**：缺獨立醫學／逐段敘事 semantic reviewer、content-specific evidence-to-claim safety review、實際 360/375/390px 手機 screenshot；還未經正式發布授權。要先驗證四篇是否真正提升新情境推理，若沒有增量不應為 26 篇額外擴充架構。

## 2026-10-28 修復｜跨 PR 主教材重疊與 ECG 時序斷裂

- 在 PR #181 和 PR #186 對照發現：兩個 private branch 的早晨 Lab 主文原先**標題完全相同**「早晨一張 Lab sheet：真正要判斷的是什麼？」；但 #181 是 pneumonia / hypotension / oliguria，#186 是 HF / diuresis / congestion。現有 main 沒有這兩篇正式發布的同名副本，屬 prospective duplication，並非 production 事故。
- **Canonical 決議（限候選規劃）：** PR #186 保留為唯一公開總論候選；PR #181 的第一篇已實際更名為《肺炎、低血壓與少尿：同一張 Lab sheet 為何可能導向四種判斷？》，重新定位為感染／低灌流的延伸病例。另三篇 specimen-artifacts、AKI/urine、CBC/DC 為各自獨立深讀，不納入第二篇「同名總論」。此決議不表示 #186 已獲醫學審查通過、也不表示 #181 獲准發布；**不得在 site/pages.json 出現第二個同名總論**。
- 反向追查 #181 的原有病例：05:40 K 5.7 的 hemolysis flag → 07:00 K 5.2 之間，未交代 ECG 結果或是否使用 insulin/dextrose 等降鉀藥，導致後文以 K 變化討論溶血假象時缺少時序／介入前提。已對**明示的完全自編病例**加上 05:55 ECG（竇性心搏過速、無新高風險傳導變化）、未施降鉀介入、同時持續評估休克灌流以及 ECG 正常不能排除危險 K 的界線。讀者能確定這是未治療前的新樣本，但**仍不能**把兩管的 0.5 mmol/L 差額全部歸於溶血。
- 三篇 sibling 的連結已調整為「肺炎與少尿延伸病例」而非「總論第一篇」，避免為讀者製造不存在的發布層級；第二篇 [3] 後的斷句修復。
- 同輪來源覆核：NICE NG148 官方現行 recommendations、UKKA July 2026 指引官網、ESE 2014 高血糖校正 +2.4 /100 mg/dL、2024 兒童 EDTA PTCP PubMed 摘要（PMID39582446）、JMA J 2026 CBC framework 官方全文與 AHRQ 2017 溶血高血鉀病例。可追查，但這次仍為**同輪作者針對缺陷修復**，不是 independent semantic PASS。
- Release hard stop 未解除：完整逐段不同審稿脈絡與 P0/P1、source figure/footnote、藥物路徑、本稿頁面實際 360/375/390px、正式 site registry 與 production sha，均不得從 passing CI 推論。

## 2026-10-28 審稿／來源原圖回查：公開教材混入 QA metadata（新發現；已修，仍 HOLD）

### Defect -> minimal repair
- 本次對 #181 四篇所有正文作獨立於既有 CI 的逐段掃描，發現讀者可見段落把「本次目視核對」「QA」「原卷尚待確認」「Draft/HOLD」「本輪 AI 審查」「未曾讀全文」等內部進度直接印成文章段落／參考文獻註記。這種**作者研究狀態污染讀者敘事**與「來源有醫學適用界線」不同，違反 EPQC 的 `internal_metadata` 與使用者明確要求。CI 之所以沒有在既有綠燈擋下，是四篇仍不在 `site/pages.json`，既有公開頁面 copy-leak gate 不保證覆蓋 unpublished draft；綠燈不能回推正文合格。
- 對四個原檔進行最小替換：主文留下適用對象與可核實來源、臨床不確定性（例如未查 113-1 Q29 的更正答案，不當成最終版本），把「何時讀了原 PDF／AI 自查了什麼／完成哪些 QA／出版 HOLD」全保留在本私人 audit、PR、Issue，不再出現在公開面向的正文。未動原始歷史完稿、不做 public registry。
- **沒有**假裝出版社付費全文、原始圖像、正式答案更正表已讀；避免用自然語氣包裝未驗證醫學主張。四稿仍 Draft/HOLD，不能因移除警示文字就降低審查責任。

### 原始 Figure / Table 直接目視回核（本輪擴充）
- [KDIGO 2012 AKI 完整原 PDF](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf)：目視 PDF 零起算索引 **21、27、28**（印刷 p.19、25、26）。p.19 Chapter 2.1 **Table 2**：Stage 1 SCr 1.5–1.9× 或 +0.3 mg/dL，以及 UO <0.5 mL/kg/h 6–12h；p.25 Chapter 2.3 **Figure 4**：stage-based management 的 shading 在 caption 說明為措施的 priority，並非固定透析或輸液指令；p.26 **Figure 5**：依病史與檢查區分灌流、阻塞、腎小球／間質／血栓微血管等病因的評估路徑。已在 AKI 正文第 06→07 節間新增原圖**連結與教學解混**，**沒有複製圖片**，也沒有說這些圖可以直接確診病因。
- [UKKA July 2026 官方 180 頁 PDF](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf)：目視 PDF 索引 **13、14**（印刷 p.14–15）。15.3 為疑似 pseudohyperkalemia 的成對 lithium-heparin 與 clotted serum；16.2a ECG changes 下 IV calcium **2C**；16.3.1 severe K≥6.5 的 insulin-glucose **1B**，16.3.2 moderate 6.0–6.4 **2C suggestion**；17.1/17.2 potassium rebound 與 glucose monitoring。第 14 頁亦包含對高 K 6.0–6.4 的高風險病人心律監測條件。**未**通讀 180 頁或所有附錄；不以已核對的兩頁冒稱整套 algorithm figure gate 已過。
- FEUrea 2024 原研究 PMID [38768779](https://pubmed.ncbi.nlm.nih.gov/38768779/) 摘要確認 11 studies／1,108 patients、subset 的 sensitivity/specificity 差異；BMJ Open 2026 [e100875](https://bmjopen.bmj.com/content/16/1/e100875) 全文結果確認 12 studies／1,240 patients、sensitivity 0.74、specificity 0.78、I² >90%、certainty low。兩篇方向不同與異質性均已在正文保留，未偽稱 FEUrea 是確診工具。
- 2024 真實 pseudothrombocytopenia 案例 PMID [39582446](https://pubmed.ncbi.nlm.nih.gov/39582446/) 摘要直接核對 13F、EDTA 17K、citrate 55K、heparin 175K；這三筆不可作為獨立連續病例或通則。
- KDIGO [AKI/AKD 官方狀態頁](https://kdigo.org/guidelines/acute-kidney-injury/) 截至本輪仍明示 2026 為 public-review draft、Work Group 正整理正式發布，不以草案取代 2012 現行分期。

### 再驗收（執行中）
- 以 exact branch Git blobs 重新掃描四篇讀者正文中的高信心 metadata leakage、檢查標題／跨篇連結／原圖 URL、跑本 HEAD 的 GitHub Actions；這些僅是**結構與來源防退化**，不是另造同一脈絡的 independent_ai_pass。
- **真正 Release HOLD**：四篇及 #186 的 exact-blob 分離醫學／EPQC 審稿、來源圖表與權利的全項必要檢查、各稿實際 360/375/390px 讀者畫面；尚無真實學習遷移數據。絕不直接從 code CI 成功推論已發布或病人安全。

### 113-1 醫學（三）Q29 更正表定位：已透過官方科目索引消除不必要的「不明」
- 考選部原始 [113 年第一次考畢試題索引](https://wwwq.moex.gov.tw/exam/wFrmExamQandASearch.aspx?e=113020&y=2024) 在「醫師（二）醫學（三）」僅提供 **試題、答案** 兩個來源連結，**未提供「更正答案」連結**；同一場考試的醫學（一）、醫學（四）、醫學（五）等若有更正，平台會在各科目明確顯示「更正答案」。因此先前以「本次拿不到 113-1 醫學（三）更正表」為跨回合 HOLD 的理由不夠精確：**官方來源列表上本身未列出這一科目的更正答案檔**，不能虛構必然另有表。
- 直接開啟並目視原標準答案 PDF ([113020、醫學（三）、S](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=113020&q=1&s=11&t=S))，Q29 = **D**。已在 AKI 讀者正文改為「原公布標準答案 D，考選部該科目未列更正連結」，不再把先前工具不可讀問題寫成面向讀者的 QA 進度。此結論範圍僅限**截至查詢時官網索引**，不代表對其他年度、梯次或題目有同樣情況。
