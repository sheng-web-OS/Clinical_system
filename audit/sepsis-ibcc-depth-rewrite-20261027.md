# Sepsis IBCC 深度重寫：來源與差距驗收紀錄

> **版本校正（2026-10-27 18:15 台灣）**：以下「67M 教學虛構病例」、「尚未修改 site/pages.json」及早期 71 分自評，均屬本 PR **較早版本的歷史快照**，不得視為當前 head 的狀態。最新主教材已改以 **Jin et al. 2025 Case 1 的真實 78M 阻塞性尿路感染病例**作主線，並明示其他 PHR 監測為反事實；兩篇正文已列入 PR 的 `site/pages.json`，另新增公開來源圖像頁與 Fig 1 provenance audit。這些只表示病例來源與工程索引進度，不是已獲獨立 EPQC／手機／正式發布驗收。正式評估一律以當次 head 與原檔 blob、最新 CI 和獨立審稿 receipt 為準；未驗證仍 HOLD。


日期：2026-10-27。僅限 PR #164 的私人審查；此報告不是公開教材，不是獨立審稿通過聲明。
正式待審正文：`content/clinical-os/2026-10-27-sepsis-from-infection-to-resuscitation.md`；最新 blob 必須依 PR head 重新讀取，不可沿用此前版本。

## Input / before
- 起點為 branch `study/ibcc-sepsis-foundations-20261027` 的原 Sepsis 中文草稿，約 8,385 UTF-8 字元，含定義、機轉、治療與單獨連回 Tamponade 病例。
- 舊稿缺口：缺少從 PAMP/DAMP/內皮到血管失張與器官功能障礙的中介；venous return/stressed volume 尚未論證；fluid responsiveness/tolerance 沒有完整改判；IBCC PHR 的監測介入回饋尚未形成主幹；未充分敘述 cardiomyopathy/ARDS/AKI/de-resuscitation 的時間演變。
- 原稿是 Git history 的前版，不改作者歷史作品，也未變更已發布 `content/tamponade.md` 或 PR #163/#165。

## New draft
- 新版約 20,450 字元，十九段主要論證節，兩張原創文字 Mermaid 機轉圖。
- 使用明示「教學虛構」的 67M obstructive pyelonephritis 長時序；不冒充 Case Report、PGY 個人病人或 IBCC 實測。
- 重要新橋樑：source×host×perfusion×feedback；PAMP/DAMP→glycocalyx/vasoplegia/capillary leak→microcirculation；stressed/unstressed volume；CO/SVR/DO2 vs MAP/SpO2；source control as distinct action；fluid responsiveness ≠ fluid requirement/tolerance；NE raises pressure but CO may worsen；CRT/DBP/perfusion across PHR challenges；cardiomyopathy and load-dependent EF；ARDS/AKI and de-resuscitation.
- 對照反例：同 MAP 不同 CRT；PLR positive 但 fluid intolerance；NE 達標但少尿；shock control 後 fluid overload；PCT/lactate 不能單獨指定 Sepsis。

## Sources read and observed (source scope)
1. IBCC Farkas `https://emcrit.org/ibcc/sepsis/`，2025-11-11；本輪實際閱讀 Definitions，Presentation，Source & mimics，Initial package，PHR（CRT／DBP／lactate／vasopressor & fluid challenge），Septic cardiomyopathy、相關腦病變章段落。其 challenge、lactate 的較強主張保留為 expert interpretation，不當作 SSC guideline。
2. SCCM 官方 2026 recommendations `https://www.sccm.org/clinical-resources/guidelines/guidelines/surviving-sepsis-campaign-international-guidelines-for-management-of-sepsis-and-septic-shock-2026`：直接核對 antibiotic 時限、source control ideally six hours、30mL/kg conditional low、NE comparison certainty、MAP 65/age>=65 60-65、serial lactate/CRT、inotropes、steroids、ARDS/bicarbonate/deresuscitation。
3. ANDROMEDA-SHOCK-2 原文 `https://jamanetwork.com/journals/jama/fullarticle/2840823`：n=1467、win ratio 1.16 (CI 1.02–1.33)、28 日死亡率 26.5% vs 26.6%（未見單獨死亡率獲益），區分 bundled intervention 與 isolated CRT。
4. Sepsis-3 original consensus `https://doi.org/10.1001/jama.2016.0287`；經編輯與來源頁互核定義，全文及附錄未獨立逐頁驗證。
5. van der Poll 2017 `https://www.nature.com/articles/nri.2017.36`，使用 host response 原理；原文非本輪全文逐段重核。
6. CLASSIC `https://www.nejm.org/doi/full/10.1056/NEJMoa2202707` 與 CLOVERS `https://doi.org/10.1056/NEJMoa2212663` 原研究摘要／結果，以臨床外推的限制為主，不使用未查核分組數據。

## Adversarial edit checkpoints
- 首輪後發現 first-use abbreviation gaps：CRT、NE、ARDS、MIC、AKI/RRT；已修正能定位者，應由不同脈絡再逐段檢查。
- 新版明示『Sepsis-3 操作性定義不應延遲治療』、感染與 shock mechanism 不互斥、IBCC 高裁量 challenge 不適合直接當個人醫囑。
- 指標被刻意拆開：BP/MAP 不是 CO，SpO2 不是 DO2，lactate 不是感染診斷，fluid responsiveness 不代表需要補液，CRT 目標研究未直接證實降低單獨死亡率。
- 未核原始圖像像素，未重製 IBCC 圖表；Mermaid 為自創定性關係，正式發布前須做手機圖像與文字後備驗證。
- **缺席事項**：尚無與寫作者分離的全文醫學／EPQC 逐段審查、真人專科審查、讀者學習效果測量、正式手機實測；不應將本次自身檢查偽稱 independent editorial approval。

## Status / release boundary
`DRAFT / HOLD`。未動 site/pages.json、正式 production、舊稿源或其他 PR。GitHub Actions 通過時僅代表工程完成，獨立語義 gate、權利與醫學驗收不因此視為通過。下一步優先做獨立段落審查，再以最小 diff 修正；不要擴張維護系統。


## 2026-10-27 自評與五題真題回歸（不等於獨立審查）

### EPQC 七軸（同稿單輪模型自評）
| 項目 | 0–4 | 具體可見增量與缺陷 |
| --- | ---: | --- |
| A 命題與取捨 | 3 | 全篇圍繞感染→器官障礙→循環瓶頸→介入回饋，但 20+ 段落偏廣 |
| B 概念解混 | 4 | Infection／SIRS／Sepsis／shock、fluid responsiveness／tolerance／requirement、MAP vs CO、lactate vs infection 已拆開 |
| C 中介推導 | 3 | Glycocalyx/vascular tone→venous return/CO→organs，仍有部分免疫與病程的解釋跳幅 |
| D 證據決策 | 3 | SSC 2026 vs IBCC expert practice，ANDROMEDA-SHOCK-2 separate composite vs mortality；需獨立逐項醫學 QA |
| E 敘事連續性 | 2 | 虛構病例雖串起時序，19+ 節及多條公式仍使初學者切換負擔偏高 |
| F 臨床遷移 | 3 | 反事實含 PLR responsive 但 intolerant、MAP 達標 CRT 不佳、adrenal crisis mimic |
| G 語言與認知成本 | 2 | 多縮寫、英文與高密度段落，初學者的基礎導讀尚不足 |

合計 **20/28，約 71/100**，是嚴格但主觀的模型自評，不具對外醫學或教學驗證效度。內部 EPQC 逐軸至少 3、平均至少 3.3；E/G <3，故 **HOLD**。既有使用者要求公開品質至少 90 分，此版未達發布條件。

### 可以被真正測量的退稿理由
1. **E｜敘事分岔**：從微循環轉到靜脈容量模型、再到抗生素藥動學時，讀者可能忘記最初病例目前在等待哪項檢查。下版應減少章節切換並使用同一時間序列重構，但不可為修稿而省略重症必需內容。
2. **G｜認知成本**：使用 PHR、DAMP、stressed volume、DO2、AKIN 等術語時，先備知識雖多已補，但濃度太高。要對照初學者能否無教學者講出因果，不能只看寫作者是否理解。
3. **D｜來源與實例**：主案例為明示的教學虛構，尚未讓讀者完整看到有原始時間序列、POCUS/液體/升壓反應的真實 Sepsis case report；不能把合成患者冒充真實臨床研究。
4. **臨床安全**：PHR vasopressor/inotrope challenges 需要患者選擇與監測前提，寫有安全邊界但未完成獨立專家核查。帶有即時改藥效果的敘述不宜直接發布。

### 本輪新增國考真題
新檔：\`content/xiaoma-internal-medicine/exams/sepsis-core-112-114-med3.md\`。主文在 §4、§6、§8、§15 及專門考題小節建立向外連結；考題詳解亦連回 Sepsis 正文，**只是未發布的 Markdown 雙向連結，不等於已測過公開網站的雙向連結**。

| 考選部真題 | 官方原始答案 | 更正狀態 | 教學焦點 | 來源 |
| --- | --- | --- | --- | --- |
| 112-1 醫學（三）33 | A | 該題未更正 | IL-5 vs TNF/IL-1/IL-6 | official 112020 Q/S/M |
| 112-1 醫學（三）64 | D | 該題未更正 | 海水、肝硬化、Vibrio vulnificus、source control | official 112020 Q/S/M |
| 113-1 醫學（三）48 | B | 本科該題未更正 | bicarbonate 不可當首要目標 | official 113020 Q/S |
| 114-1 醫學（三）51 | B | 該題未更正 | SVR: distributive vs cardiogenic | official 114020 Q/S/M |
| 114-1 醫學（三）57 | C | 該題未更正 | Sheehan/adrenal crisis，採檢不延誤 hydrocortisone | official 114020 Q/S/M |

正式官方頁：
- 112-1 https://wwwq.moex.gov.tw/exam/wFrmExamQandASearch.aspx?e=112020&y=2023
- 113-1 https://wwwq.moex.gov.tw/exam/wFrmExamQandASearch.aspx?e=113020&y=2024
- 114-1 https://wwwq.moex.gov.tw/exam/wFrmExamQandASearch.aspx?e=114020&y=2025

已用官方「醫學（三）」答案圖頁核對：112 標準 A33/D64，112 更正只有 47 與本次無關；113 標準 B48；114 標準 B51/C57，更正只有 23、42，與選用題無關。官方題目本文在 Repository 的五年 \`structured/\` 擷取可回查；114 Q51/Q57、113 Q48 另由官方 PDF 文字確認題意。因官方 PDF 題目頁的網頁 screenshot 服務部分回報 cache miss，**不可宣稱所有題目原像素目視核對完成**；本輪五題皆是無原附圖的文字題。題面以「重述」呈現，官題、官方答案與 2026 指南需分開。

### 結論
- **能確認**：PR 上已保存深度新版與真題詳解，並且有相互 Markdown 連結，官題答案與更正情形已依上述查核。
- **不能確認**：獨立審稿已完成、正式站題頁可點開、手機版已通過、真實讀者能更快理解。
- **仍然 HOLD**：E/G 未過內部 EPQC，並無獨立醫學審查；不把自評寫成審稿完成或為了擺放國考題直接改 site/pages.json。


## 2026-10-27 18:44+08｜獨立排程上下文：逐段 EPQC 實查（INCOMPLETE；不得作為 PASS receipt）

- **Reviewer context**：與原 Sepsis 撰稿回合分離的排程執行上下文；此輪對一段正文實際提出並寫入修訂，因此**本輪不是該修訂段落的獨立最終驗收者**。未建立 `independent_ai_pass` receipt，未聲稱人類專科審查。
- **精確起點**：PR #164 head `05e51fcf7cbeb9e107166d3fc151fac72525101f`，main `9321f7bce4288d12f74d5be1dea183edc7e70bc2`。主文 blob `c307f60e872ec7603ce475c414cb875001371449`（350 行），題解 blob `26abad21004a55f3d74999e71f196bc85c9bafe5`（182 行）。以 `site/semantic_gate.py:reading_units` 的同等分段條件盤點：主文 **107** 個有效單元、題解 **37** 個。
- **實際閱讀／裁定範圍**：已讀兩篇全部 Markdown（350／182 行）以掌握全文結構，但**逐單元批判性評閱只完成主文第 1–35／107 單元**（原稿第 4–121 行，從真實病例、四軸模型、Sepsis-3、宿主反應、血流公式至初始感染診療）；題解 **0／37 單元正式裁定**，其全文閱讀不等於逐段審稿。主文剩餘 72、題解 37 單元均為未完成。不得把初輪閱讀或局部查證換算成七軸整篇通過。
- **實際缺陷 E/G（原稿 unit 5／第 19 行）**：前文已用**否認發燒**的 Jin 78M 真實病例建立問題，緊接著卻另起「想像病人感染後持續發燒、意識變差」，無必要地更換病例框架、重複前一段四問，造成病例時間序列與敘事焦點跳轉。這不是醫學 P0，卻是具體的 reader continuity / nonredundancy 缺陷。已在**原 PR 分支**以最小編輯將該段接回「沒有發燒、已有 AKI／循環惡化」的真實病例；commit `bbcad5cbebb6c3e4337cce038923b1ce1056de99`，主文新 blob `6116b04c3e7a2ddb77c393ab72bed8db79f06cac`。這是**已提交編輯**，不是已獨立複審或已發布。
- **待補來源界線（原稿 unit 8／第 47 行）**：Jin Case 1 記載 solitary kidney 與左側 hydronephrosis，但原文 Case 1 未明言唯一腎臟的側別；教材目前只陳述「單腎病史」而未捏造側別。後續審查及圖說**不可擅自補成『左腎是唯一腎』**。這是需維持的來源限制，非現有已證實錯誤。
- **來源實查**：已對讀 Jin et al. 2025 原始 Case 1 正文及 Fig. 1 caption：78M、weakness/cough、否認發燒與泌尿症狀、HR120、BP96/70、RR25、POCUS plethoric IVC／normal cardiac contractility／左腎積水、WBC24K、lactate6.6、pH7.24、Cr4.8、CT 左遠端輸尿管結石、NE、緊急支架及數日後出院；未讀／目視核實原圖完整像素。另讀 IBCC Septic Shock 2025 的定義、來源、mimics 與復甦索引；讀 SSC 2026 官方推薦，核對 Sepsis 篩檢、初期復甦、source control、bicarbonate 等部分。**並未逐條查完兩篇所有引用與六題官方試卷原像素**，source 全通過 = NOT_VERIFIED。
- **Q48 防假陽性**：依既有已更正官方查核，113-1 醫學（三）Q48 是 Sepsis／bicarbonate、答案 B；此輪**沒有**重跑舊錯誤 COPD 假陽性，也沒有刪除正確雙向連結。
- **七軸暫態**：A 主命題可辨；B infection/sepsis/shock 與 source/hemodynamics 的區分在已審範圍可見；C/D 仍須完成後文介入與來源對照；E/G 有上述真實缺陷並已局部修訂、尚未複驗；F 未審後文反事實。**A–G 不給全篇分數**，hard_stops 未完成判定，`audit/editorial-semantic-reviews.json` **不得新增 PASS**。
- **執行／發布狀態**：`L0_eligible_found=1`（純敘事連續性小補丁）；`L0_attempted=true`；`L0_commit_SHA=bbcad5c`；`RED_failing_fixture=NOT_APPLICABLE`（非機械性規則、屬需獨立語義判斷的 L1 編輯）；`GREEN_CI=PENDING`；`release_gates=SEMANTIC_HOLD`，手機 360/375/390 與 production 均 NOT_VERIFIED。**不合併、不發布**。
- **下輪精確接續**：重新核對最新 PR head、兩篇 blob 與 CI；先由**另一個**獨立 reviewer 對修後 unit 5 重新裁定，再從主文第 36/107 單元（原第 123 行 SSC 抗生素時機表）逐段審到 107/107，逐項查證 2026 SSC／IBCC／原研究，最後對題解 1–37/37 做真題來源與 EPQC；有 revise/remove 就先修再重新生成 current-blob packet，**兩篇全部 keep 且 hard stops 解決後**才可寫正式 receipt、跑 CI、手機與發布驗收。此處進度不是發布完成。

## 2026-10-27 18:48+08｜下一輪 EPQC 逐段初審接續及 reader metadata RED/GREEN（INCOMPLETE）

- **精確接續版本**：承接上輪主文 1–35／107 初審，先檢視主文原先 unit 5（第 19 行）的修訂，確定已接回「無發燒、已有 AKI 與循環異常」的 Jin 78M 病例，未再插入無端虛構發燒病例。此輪讀回主文全部 350 行，依 `site/semantic_gate.py:reading_units` 規則盤點 **107** 個有效單元，逐單元檢視 **36–107／107（新增 72 個）** 的閱讀功能、重複、推理跳接與主要醫學限制；題解全文 182 行及六題分段內容亦讀回，**37 個有效單元作初輪讀者／結構檢查**。這是逐段初審，不是每一條臨床引用的 source audit，也不是逐段最終 `keep` 裁定；兩篇正式 receipt 仍缺，**INCOMPLETE / SEMANTIC_HOLD**。
- **新發現並修復的實際缺陷（非醫學 P0/P1）**：主文 unit 78（原第 262 行）在 Sepsis/bicarbonate 教學段落中，突然提到「因曾有錯誤審查而刪除」的內部工作史；主文 unit 107（原第 349 行）把「尚非真人專科同儕審查或實測學習成效」的內部 QA 狀態塞入正文；題解最後「來源邊界」段（第 181 行）提到「內部存檔」、「尚處 Draft」和「未完成正式公開網站與手機版發布 QA」。這些與讀者臨床推理無關，違反 metadata／reader 分離與 nonredundancy，應標 **REVISE**，不能在舊 blob 上填 `keep`。
- **已執行 test-first**：在唯一 PR #164 原分支先提交 `37b0941cc19c646dbac08385964929f474dd5cc7`，於 `tests/test_sepsis_figure_source_gate.py` 增加讀者正文不含上述審計語句的 fixture；在舊正文實查四組禁止字串皆命中，故 RED 具可重現的文字證據，但 **RED GitHub Actions 尚未確認有完成失敗 run**，不得冒稱 CI RED。隨後主文最小修訂 commit `a9dd665c33be1bdc9b2b0a5dcf0857f33f09b304`（新 blob `b467ac79ef9d9f0bc62f9b21ce54dfaf1e9431cd`），題解最小修訂 commit `7d4d40d2fb47778eaecb36d2a06e18287a9f581f`（新 blob `47c52ede0fc7a6411b8e2e5722c8239e46cccd56`）。兩篇原四組字串再查皆已不存在；**GREEN CI 待核對**。修訂沒有變更 Q48 的正確題號、B 答案或 canonical 連結。
- **本輪有核對的原始來源**：Jin 2025 Case 1（PMC12487450 Case 1 及 Fig.1 caption；僅文字與 caption，非原圖逐像素）、SSC 2026 官方 2026-03-23 推薦（抗菌藥時機、30 mL/kg 個別化、NE/MAP、CRT、bicarbonate、RRT、去復甦）、IBCC Septic Shock 2025-11-11 的定義／PHR 結構、ANDROMEDA-SHOCK-2 JAMA 原始摘要與結果表（1467、win ratio 1.16、28-day mortality 26.5% vs 26.6%）。對讀未發現上述範圍的新的醫學 P0/P1；**未完成** CLASSIC/CLOVERS 原文逐表、所有六題官方原卷／勘誤原像素、完整原始 Figure、手機 viewport 與正式部署驗收。113-1 Q48 已由前輪正確校正，**本輪沒有重跑或移除**。
- **審查身分**：本輪與原 Sepsis 撰稿脈絡分開，但**本輪親自修改主文與題解**，因此不能對這兩個最新 blob 自稱完全獨立的最終 `independent_ai_pass` reviewer。須由另一個未撰寫這兩份新 blob 的 reviewer 重新逐單元驗證 source、七軸、`reader_gain`、`nonredundancy_reason`、硬性問題；未完成前不寫 `audit/editorial-semantic-reviews.json` PASS，也不得合併。
- **L0 執行指標**：`L0_eligible_found=2`（兩篇的 reader/editorial metadata 汙染），`L0_attempted=true`，`L0_commit_SHA=a9dd665c,7d4d40d`，`RED_failing_fixture=37b0941`（舊內容命中；CI RED NOT_VERIFIED），`GREEN_CI=PENDING`，`release_gates=SEMANTIC_HOLD`，`mobile=NOT_VERIFIED`，`production=UNCHANGED`。
- **下輪精確接續**：先核最新 PR head／兩篇 blob、讀取 CI jobs；由未參與本輪兩篇編輯的審稿脈絡逐段驗證 current-blob `reading_units`（主文 107、題解 37，改動可能影響 unit ID，須重算）及全部七軸、sources／figures，退回任何 `revise`；兩篇完整 `keep` 且 hard stops 清零後才可寫有真實 `reviewer_reference` 的 receipt、重跑 required CI、360/375/390px 與 production gate。既有使用者對 #164 的附條件發布授權有效，但尚未達成條件。
