# 跨文章語義重疊｜2026-10-29 source-backed pilot

狀態：**Artifact / editorial pilot；非盲審、非獨立醫學驗證、未更動任何公開正文**。時間：2026-10-29（Asia/Taipei）。基底：`main` commit `c657352cb52640b1a276a8dc30d9b90e896a60ff`。本紀錄保存在私人 `audit/`，不可當作公開教學內容。

## 問題、母體與限制

PR #213 修正 115（二）醫學（三）Q28 因歷史原稿＋整合版同時索引造成的兩次教材入口；PR #217 增加標題正規化與明示 `replaces_original` 的 deterministic gate。兩者**無法**抓出標題不同、字句不同，但核心病例、因果命題與決策轉折可能重複的文章。

`site/pages.json` 有 122 筆公開頁面。排除歷史原稿、正式題庫原卷／彙編及來源頁後，本次人工候選初篩有 46 筆文章／閱讀入口（其中含練習頁）。對 14 篇最接近的正文進行跨篇比對（下方五組；另外查了肝膽候選，未列入本次判讀分母）；**這不是全站 46 篇逐對掃描**。沒有新模型盲測，也沒有讀者理解實測；診斷／治療內容沿用現有文章表述，不藉這份編輯比較宣稱重新核實醫學文獻。

每組分開回答：
1. 前稿**已經真正解決**什麼臨床疑問？共同的必要基礎不算第二篇的發現。
2. 後稿能否指出新增病例、原圖、可區辨證據、反事實、處置分歧或不可省略的橋接？
3. 若刪去後稿，讀者是否會失去一項實質不同的推論／行動？若只失去不同說法，優先縮減／整合，而非增添新頁。
4. 結論是 **KEEP distinct**、**KEEP + NAV/TRIM**、**REVIEW/HOLD** 之一；這是候選編輯決策，不是合併或修改已發布文章的授權。

## 個案對照（已讀正文與現有跨頁連結）

### A. HF 四象限圖 vs HF 主文 vs LVEDP 主文 — KEEP + NAV

- 圖表補充：`content/xiaoma-reading/integrated/2026-10-23-hf-lvedp-figures.md`（blob `d67998c1aa65643f3961c7802a3980a8cce61d36`）；2026-10-27 HF 主文（`78f584845c0305c1f140fa208cf364b1faa871e6`）與 LVEDP 主文（`0e33cb39ecfc0f1e1a505389f12a8480570a7a10`）。
- **已共同出現**：wet/dry 與 warm/cold 是獨立軸、肺水腫不等於全身總水量增加、PAWP／LAP 不等於單次 LVEDP、同 LVEDP 未必同 LVEDV。
- **圖表頁獨特收益**：有實際的 HF phenotype matrix 與 LV filling branches 兩幅原創圖示；兩份新主文各自連到這份圖的精確 anchor，但它不是另一篇與 LVEDP 深文競爭的完整測量／決策推理。
- **新主文獨特收益**：HF 主文解決臨床症候群、急性失衡與去鬱血／灌流處置順序；LVEDP 主文增加 mean LAP、PCWP、LVEDP、transmural pressure 及 MR／心包限制／量測條件的分歧。
- **導航缺口**：2026-10-23 圖表頁只明示「搭配兩篇歷史原稿」，末尾也只連兩篇原稿與來源；**沒有返回已發布 10/27 HF 與 LVEDP 完整整合稿的連結**。若讀者從知識地圖先進圖表，容易誤以為舊原稿才是主教材。建議在下次獨立語義／手機審查過關的導覽修訂中補兩條精確 backlink；不刪圖，不以摘要替代。

### B. 低血氧總論 vs A–a／shunt 深究；PaCO₂/NIV vs RR 40 生理 — KEEP distinct

- `content/xiaoma-internal-medicine/lessons/2026-10-21-hypoxemia.md`（`be780f1ae3567c60f3a108c8fa489ca8005f39d3`）vs `2026-10-25-hypoxemia-mechanisms.md`（`491715947e489aec50b54107c2e1f756225f5c2d`）。
- `2026-10-22-hypercapnic-failure.md`（`67bac856e6cc1ea7ded35c05f95d2f8677a4c320`）vs `2026-10-25-hypercapnia-physiology.md`（`82cac3651f12a6084377af7a9f7479a1fb4089a9`）。
- **共同前提**：alveolar ventilation、CO₂ clearance、A–a、V/Q、氧療不能替代通氣支持。這些必須短暫提示，但不該每篇重新完成一樣的推論。
- **不同核心任務**：總論以「SpO₂ 改善卻惡化」整合辨識；A–a 深究以原始 figure 與病例回答為何擴大不代表 shunt；NIV 主文處理適用性、氣道安全與升級；RR 40 生理稿以 MG、OHS 的實際病例和通氣機制查找故障位置。現有多處精確前後篇連結，可保留。
- **出版前復檢點**：日後每篇新稿重用 V̇A 與 PaCO₂ 公式時，須檢查是否新增會改變機轉區辨的病例證據，而非重新撰寫上一章所有定義。

### C. PE 代償性低灌流病例 vs PESI／2026 AHA/ACC A–E — KEEP + NAV

- `content/xiaoma-internal-medicine/lessons/2026-10-27-pe-normotensive-shock.md`（`e3cef0d9e97b149c2f276454f2516471004ff13e`），`2026-10-29-pe-pesi-aha-acc-2026.md`（`d98fac13a3ccfda337438db25b857250d77b11e0`）。
- **重合**：RV afterload／LV preload／CO／正常血壓掩蓋低灌流，以及 diagnosis→severity→treatment 三階層，在兩篇均佔重要位置。
- **不同增量**：前篇用 44 歲病人的 CTPA 無法完成、HFNC SpO₂ 98%、乳酸 13 等實際當時資料討論「未確診下是否還能等」；後篇以已確診 PE 病人為主，獨立解析 PESI/sPESI、Hestia、A–E/R、RV/biomarkers 與照護層級。不能只因同樣討論 normotensive shock 就合併。
- **導航缺口**：新分級文有回到 10/27 病例的連結；10/27 病例是較早發表，未直接連到新分級文。可在下次導航維護時補雙向連接，而非重寫病例主線。

### D. HBV phase/state/stage vs HBV signals — REVIEW / TRIM FIRST，不得自動合併

- `content/xiaoma-reading/integrated/2026-10-26-hbv-phase-state-vs-stage.md`（`e9d4e2e407d3fcc1dedcfccae04b796f77b044a2`）；`2026-10-26-hbv-signals.md`（`cf8c85e31f0d7ad0262caee02279cd990b79d932`）。
- **同一論點已重述**：病毒量高而 ALT 正常並不矛盾；HBV DNA 是複製訊號、ALT 是 hepatocyte injury 的間接訊號；ALT 正常不能排除既有纖維化或預設免治療。第一篇已建立病毒量、ALT、fibrosis 為不同維度，並談 2025 EASL/AASLD 門檻。
- **第二篇仍可能獨特**：將 `marker (observation) → phase (inference) → treatment threshold (action rule)` 明確分成三個認知層次，進一步解釋為何檢驗跨過閾值不是疾病開始，這是先前 phase/state 分類未完整展開的認知論焦點。兩篇目前已有雙向連結。
- **精修假說**：第二篇開頭「病毒明明大量複製，ALT 為什麼可以正常？」與「ALT 正常，究竟沒有看見什麼？」相當一部分與前篇重合；可改成僅必要的短橋，保留真正新命題和由觀測到治療閾值的推理。但這是**待獨立逐段 review 的候選**：不能憑同一輪模型評語直接剪掉醫學限定條件、替使用者重寫作者原稿，或宣稱已發布修訂。

### E. WPW → Pre-excited AF → WCT/ACLS — KEEP distinct（負對照）

- `content/xiaoma-reading/integrated/2026-10-26-wpw-conduction-mechanism.md`（`187cd98c967a300c2958884070047e371be2dfba`）、`2026-10-26-preexcited-af.md`（`54fcbc1d90d32af88d4065e9ebedede33964d3ce`）、`2026-10-26-wct-acls-decision.md`（`c04d4ab15295b2c84b2812dea58688713ea8f842`）。
- 三篇反覆出現 AP、AV node、adenosine，但其推理任務逐級變化：reentry 路徑與 QRS 形態 → irregular pre-excited AF 用藥危險 → 臨床尚未確診時依 pulse、instability、rhythm 性質作安全行動。文內本就明示 series reading。若偵測器只看關鍵詞，很可能產生嚴重 false positive，損害完整的教學序列。

## 對系統的最小回饋

- **目前確證的 bug**：題庫 Q28 原稿與整合稿重複入口，已由 PR #213/#217 修復；本輪沒有發現「應立即公開刪除一整篇」的充分證據。
- **值得編輯審查而非直接改稿**：HBV signals 部分段落有可疑的重複教學投資；需要與改稿脈絡分離的 reviewer，依兩篇全文判定 `keep / trim / integrate`，並檢查醫學限定條件的保全。
- **已找到具體低風險導航缺口**：HF/LVEDP 圖示頁缺至新整合版的返回入口；10/27 PE 病例缺至後來 PESI/A–E 專題的往前入口。這些是讀者路徑問題，不是證明正文醫學錯誤。
- **最小機制**：沿用 `docs/editorial-semantic-release-gate.md` 的現有 `new_understanding` 和 `strongest_counterargument`，在新稿審查時用最接近 1–3 篇做跨篇反證；不新增常駐 embedding、全文 Claim Graph、第二 publication registry 或固定語意重複百分比閾值。

## 下一輪真正的驗證

這輪由同一模型挑題、讀文、做編輯判斷，**不是獨立盲測的 precision/recall、人工省時或臨床正確性成果**。在下一批**尚未看過的**新稿發布前，將「作者／模型原本不經跨篇檢查」與「按需跨篇審查」對照；分開記錄：有無在使用者指出前定位真重複、誤把必要共通前提判成刪稿（false positive）、漏檢、審查增加分鐘數、使用者救援次數與耗時、重大醫學安全錯誤。各稿保留 source SHA、抽查段落與 reviewer 判定。沒有顯著淨收益就只保留原生按需閱讀，不擴張演算法。

任何對公開正文的刪段／加導覽仍遵從**exact blob** 的獨立語義審稿、現有來源／醫學硬閘與手機 QA；未完成前僅存私稿／HOLD。
