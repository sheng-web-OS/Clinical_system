# VTE｜發布前專業圖像客觀審查（2026-10-27）

**裁決**：2026-10-27 此文章舊版三張文字框圖，以及 PR #83 首輪替換的三圖組合，均未通過教學圖像驗收。第二輪在 PR #83 移除兩個任務不符的圖，將一組真實影像移至解剖定位段落。**目前仍 HOLD，未宣稱正式網站驗收或獨立臨床同儕審查通過**。

## 誰負責判斷

專業編輯／研究 AI 必須在發布前給出可複核的結論；**不得以「讀者沒使用過，不知道有沒有用」推卸驗收責任**。事前客觀判斷以來源證據、正確的圖形語義、與文章中當下需解答的問題，以及可操作的不同下一步為依據。真正的用戶研究是發布後的外部驗證，不是發布前的必要前提，也不能替代專業品質監督。

## 五個不可妥協的拒收門檻（任一失敗即退件，不以加權平均掩蓋）

1. **醫學語義**：解剖位置、因果方向、時間先後、統計尺度、閾值和臨床決策的箭頭沒有誤導；每一個箭頭能對應有出處的主張。推論不足的部分以明確限制表示，不硬畫成必然。
2. **圖與段落對題**：預先寫出「此位置的唯一認知任務」。遮住正文只看圖／圖說，必須真的能回答該問題；若回答的是相鄰但不同的問題，移位或移除。
3. **不可替代的資訊增量**：把圖刪掉，關鍵的空間結構、量化關係、觀察證據或診斷分支是否流失？若沒有，只是重排文字，應改為正文／表格，不稱作原創視覺化。
4. **來源、權利與辨識**：真實影像必須對到原文的 figure、原說明和病人資料；不能把 color Doppler 冒充 compression ultrasound，或把單病例變成普遍因果命題。公網引用需有可辨識的授權與原始來源，不能在未核合法情境時嵌圖。
5. **實際畫面**：正式 build 中 360px、390px、桌面尺寸的圖中文字／標記／箭頭都可辨識，無裁切／橫向溢出／外連失效；單純有 CSS media query、HTML alt、CI 測試通過不算完成。須保留實際渲染的可追查證據，不能捏造截圖。

五條是**否決制**，而非任意美感評分或合計 90 分便可強行發布。用圖的必要性本身也要受審；**「不畫圖，只連到更好的原始醫學圖」是可接受而常常更好的編輯結論**。

## 本次實際查核

| 稿內位置／版本 | 問題應該是甚麼？ | 直接檢查 | 事前判斷／動作 |
|---|---|---|---|
| 舊圖 1：三危險因子 → DVT/PE 平行 | 共同生成條件與從 venous thrombus 到 pulmonary artery 的可能栓塞路徑 | 並排箭頭缺少 embolus 經 IVC、右心的解剖中介 | **FAIL**：撤回 |
| PR #83 首輪圖 1：Blausen DVT 圖 + 文字 | 靜脈血栓如何可能進入肺動脈 | 真實圖只畫腿部 DVT；右心、肺動脈完全不在視野，路徑仍仰賴正文 | **FAIL**：撤回嵌圖，改提供 AHA 2026 原始解剖圖連結 |
| 舊圖 2／PR #83 首輪 Wells 雙欄圖表 | 相同 VTE 背景為何啟動兩套不同 pretest → 不同 imaging／stop rule | 文字重述兩組症狀或閾值，沒有真實 decision branches | **FAIL**：撤回，指向 NICE NG158 官方 DVT/PE 原始流程與條文 |
| 舊圖 3：D-dimer 文字分流 | 低臨床可能性與陰性 D-dimer 何時可以停、高可能性為何仍需影像 | 格子平行排列，沒有完整條件/停止分支；可能讓人錯用在不穩定 PE | **FAIL**：撤回，連至原始 NICE 決策圖／正式條文 |
| PR #83 首輪圖 3：JKMS 2022 CTPA/CTV/Doppler | 被放在「D-dimer 停止條件」之下，卻只顯示確診部位 | 真實 Figure 5 的 A/B = PE CTPA；C/D = popliteal DVT CTV/彩色 Doppler，不能回答 stop rule | **FAIL placement**：移到不同影像解剖定位問題之後，保留病例真實影像 |
| PR #83 第二輪保留的 JKMS 圖 | 兩個解剖位置到底用什麼影像證實？ | 有兩組實際病例影像，標有可逐項核對的原 Fig.5 panel | **內容與位置暫可接受；整體未通過**：授權使用情境／手機實際畫面與外連載入仍待檢查 |

## 重建圖與發表的區別

- 原創圖不必多。每張圖要能顯示一個真正存在的結構或決策差異；否則寧可刪除。
- AHA 的原始完整解剖圖是所有權保留，只放來源連結。NICE 官方演算法亦只放連結，不聲稱站內重製；原始連結的可達性要實測。
- JKMS 臨床圖為 CC BY-NC 4.0，不保證所有網站場景可合法嵌入；若不能確認非商業條件，改成來源連結。
- **機器檢查只能驗證圖號、連結、檔案存在與版面條件，不能判斷醫學因果或認知增量。** 即使 PR CI 全綠，編輯仍有義務主動拒收不合格圖。

## 發布狀態

PR #83 保留 **draft／HOLD**。尚未有對此 PR 最終版本的完整實際 360px／390px／桌面截圖、獨立醫學審查，及對外部影像嵌入授權的最終核可；這些缺口不能靠編輯自評「看起來好」或詢問使用者補驗收來通過。

## 第三輪：真實 Chromium 360／390／1365px 截圖裁決

依 PR #83 建置成品於隔離瀏覽器實際渲染：
- docScrollWidth 均與 viewport 相符，未見橫向溢出
- 外部 JKMS 圖的 `naturalWidth=0`，在測試環境呈現空白大區塊；不能外推正式網站，但本圖的有效載入**無法驗收**
- 390px 手機四格影像在 318px 的內容區域內縮得過小，即使載入，也不能可靠辨識箭頭與 filling defect

**裁決：舊版的站內 JKMS 圖正式拒收**；撤除站內 `<img>` 和整張站內偽教學圖，以高解析原始 Figure 5 連結替代。這是本次專業品質判斷，不需等待任何讀者測試。AHA、NICE 已提供官方原始圖入口，NICE 另補可讀鏡像。修訂版不再有任何必須依賴外部圖片載入的 inline figure。

最終仍保留臨床醫學與知識來源獨立審查的界線；不因 GitHub build 過關直接宣稱正式發布。


## 最終四輪：Bayesian 原創圖的事前量化／真實渲染驗收

`vte-decision-resolution` 雖有正確的問診分流，但實際看過 390px 與桌面截圖後仍判定為**文字卡重排、視覺增量不足**，已撤回。替換為 `vte-d-dimer-bayes`，放置在介紹陰性 D-dimer 機率更新與影像定位之間。此圖不是血栓解剖，也不能替代完整 NICE DVT/PE 原演算法。

**數學驗收**：以刻意假設的 LR− = 0.10，前測 5% 得後測 0.5235602%，前測 50% 得後測 9.0909091%。圖中線性 0–100% 機率條與標示值分別四捨五入為 5%、0.52%、50%、9.09%，沒有把 odds 與 probability 混淆；**未宣稱 D-dimer 的 LR− 恒等於 0.10，也未標示安全的停查門檻**。

**實際 Chrome 渲染**：以本 PR GitHub Actions run `40372878603` 的建置 ZIP、相同完整 `styles.css`，於 Chromium `set_content` 內嵌 stylesheet、移除不影響正文的遠端 analytics JS 後擷取 `figure#vte-d-dimer-bayes`：
- 360px viewport：document width 360px；figure 314px 寬、約 879px 高；無横向溢出，實際兩個百分比比較可見。
- 390px viewport：document width 390px；figure 344px 寬、約 790px 高；100% 量尺、數值和註解均完整可讀。
- 1365px viewport：document width 1365px；figure 790px 寬、約 702px 高；數值軸和標籤均可讀，無截斷。
- 這個測試是本機隔離 Chromium、**不是正式 Cloudflare HTTPS 體驗**；截圖未作為醫學同儕審查證明。

**教學增量**：刪圖後雖仍能口頭說「前測影響停查」，但讀者無法立即比較同一 LR− 下兩個不同 residual probability 的具體量級。圖有真正數量比例及可重新計算的數值；和原本三張文字卡有可驗證的差異。完整 Wells 分層及陰性 CUS／CTPA 例外仍由原始 NICE 流程與正文保留，圖不嘗試替代。

**醫學及出版限度**：本檔屬 AI 編輯與數學／來源查核，**不是獨立醫師同儕審查**，也無使用者學習效果研究。對無治療劑量處方的教學文章，以來源稽核、逐圖語義檢查、各尺寸視覺驗收與機器建置為預發布閘門；發布後如發現醫學錯誤必須回退，而不能以作者提供的資料視為一切都已驗證。


## 2026-10-27 PR #105：二張站內向量分支圖首次及第二輪真實 QA

檢查對象：`vte-native-diagnostic-pathways`（Desktop 原生兩個 SVG；360/390px 轉為兩套 mobile-native 分支）；同篇 Bayesian 圖仍保留。不再以原始來源連結充當圖像完成。

**首次瀏覽器驗收及實際拒收**：從 GitHub CI 40418562208 產出的 `clinical-system-static-site` ZIP 抽取完整 HTML 與 styles.css，直接以 Chromium render `#vte-native-diagnostic-pathways`：
- 360px viewport：document scrollWidth 360，figure width 314；只有兩個 mobile diagram 顯示，desktop SVG display:none。
- 390px：document scrollWidth 390，figure width 344；兩個 mobile diagram 可讀，無 overflow。
- 1365px：document scrollWidth 1365，figure width 790；兩個有條件分支的 inline SVG 顯示。
- 第一版 desktop 正負結果標籤壓到 arrowhead，而且 proximal ultrasound 節點英文字接近邊框 → **FAIL**，不得發布。

**明確修復**：將陽性／陰性標籤移到水平分流連線上方，對文字加白色描邊，縮短過長的 Ultrasound node 字串；第二輪在 CI 40418957934 的同尺寸渲染中，上述標籤與箭頭分離且內容可讀，三尺寸 `document.scrollWidth == viewportWidth`。其後把 DVT 第二層結果名改成完整 **「D-dimer 陰性／D-dimer 陽性」**，避免下游「再做 6–8 天超音波」誤被解讀成初次 proximal CUS 的陽性出口。須以最終 CI 生成結果驗證此處修改未造成排版退化。

**編輯醫學檢查**：對照 NICE NG158 原圖 p1/p2 與 recommendation 1.1：
- DVT likely ≥2 → proximal CUS+ diagnosis；CUS− / quantitative D-dimer+ → repeat proximal US 6–8 days；D-dimer− → alternatives；DVT unlikely ≤1 先 D-dimer。
- PE likely >4 → CTPA 或適當 V/Q；positive diagnosis；negative 對照臨床與影像品質，若疑 DVT 可考慮 proximal leg ultrasound；PE unlikely ≤4 D-dimer first，unstable suspected PE 不等 routine stable route。
- 上述僅是**有診斷作用的選定分支**，不是 NICE 2023 完整臨床算法，也不是 Pocket Medicine 三層 DVT Wells 的重新繪圖；不給劑量與未經驗證的固定 D-dimer 截點。
- 合法性：原創 SVG 與手機 HTML 僅使用公開指南臨床建議的事實，不複製 NICE / Pocket 原流程畫面，無第三方圖片 hotlink。
- **仍未取得獨立醫師同儕審查**；發布僅按此臨床編輯、來源追溯、CI 與真實多裝置 QA 判斷，不能稱為療效或醫學同儕認證。

