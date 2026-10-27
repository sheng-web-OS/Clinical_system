# ACS 原站研究擷取｜建立診斷

> 私有研究快照｜2026-10-27｜**DRAFT/HOLD，不是已通過醫學審查的正式教材**。來源：[ACS｜理解與臨床判斷](https://acs-deep-learning.dreamycarp4.chatgpt.site/) 的 data/units.json。經第三方 HTML 清洗後逐單元 JSON 解析而得，**不具有來源 bytes 保真性**；原圖、可執行互動、第三方 PPT/ECG 影像均未匯入，不能冒充完整原站。章節計畫為 5 主線＋1 延伸，本快照實際完整擷取 5 節。個別單元保留 sourceOrder、來源 PPT 頁次、來源 URL、figure caption 與安全註記；需要對原網與原始投影片逐段比對。

## 02｜症狀與初始分類：ECG 分流不等於最終診斷

*把胸痛特徵、眼前危險與分類放在同一個情境。*

- 原站 ID：`symptom-context`；原課順序：2；核心主線；課程頁：7、8、9、10、11、12、13。

**起始問題：**病人怎麼痛，會讓我們更懷疑 ACS？

**本節核心判斷：**持續難治性缺血、休克或致命心律不整要立即處理；穩定患者才接續序列 ECG 與 hs-cTn。沒有 STE，尚不能命名為 NSTEMI。

**原課承接：** 第 6 頁提出 symptoms、ECG、cardiac enzymes，還沒有說明任何一項的辨別力。 原文先用症狀的缺血可能性圖、angina 特徵與病史 likelihood ratio，再提出 UA／NSTEMI／STEMI，接著以血栓圖及導管影像顯示共同病理與再灌流。

**下一步：** 症狀與 ECG 可以形成懷疑及分流，卻尚未區分有無急性心肌損傷，因此自然進入 troponin 的結構、定義與序列採樣。

### 哪些疼痛特徵較支持缺血？

胸骨後壓迫、緊縮或沉重較支持缺血；瞬間、局部，或隨呼吸與姿勢改變的疼痛則降低機率，但單一描述還不足以定下診斷。

不適也可能在手臂、下顎、頸部、背部或上腹部，以喘、噁心、冒汗或疲倦為主。位置、感受與伴隨症狀，都比「不典型胸痛」這個標籤更具體。

- [2022 ACC pathway §5.1：症狀與初始評估](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)

### 原本活動才痛，現在休息也痛，改變了什麼？

較少活動就痛，甚至坐著也持續不適，表示需求還沒明顯增加，供應就可能已經不足。新發嚴重心絞痛、發作變頻繁，或近期 MI 後再痛，也提示冠狀病灶可能不穩定。

休息時痛超過 20 分鐘是警訊，少於 20 分鐘卻沒有因此變安全，持續時間也不能換算梗塞大小。是否反覆或持續、與活動的關係、伴隨症狀及目前是否仍痛，才能幫忙判斷缺血是否持續。

### 右臂放射痛的 LR 4.7，要怎麼用？

病人有右臂／肩或雙臂／肩放射痛、運動誘發或冒汗，會增加 AMI 的可能性；胸膜性、姿勢性或按壓可重現的疼痛，則把機率往下降。右臂／肩放射的 LR 約 4.7，胸膜性約 0.2，這些數字要乘在問診前的勝算上。

也就是：先驗勝算 × LR＝後驗勝算。症狀常一起出現，相關的 LR 不可任意連乘；信賴區間則告訴我們估計有多不確定。這張表估的是 AMI，其他 ACS 或致命胸痛的機率，還得由各自的資料回答。

### NTG 後不痛，ECG 也改善了嗎？

NTG 可降低壁張力與耗氧，也能影響食道等平滑肌；休息、其他藥物與症狀自然波動也可能伴隨改善。因此用藥後不痛，無法確診或排除 ACS。

若疼痛改善，ECG 卻仍有危險變化，就不能取消原本的緊急處理；病況與 ECG 是否一起改善，才是當下要核對的變化。

- [2023 ESC ACS guideline §3：NTG response 不作診斷動作](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)

### 同樣胸痛，為何最後分成 UA、NSTEMI、STEMI？

ECG 上的持續 ST elevation 或其他需緊急再灌流的型態，決定初始分流；缺血證據與序列 cTn 則確認是否 MI。ACS 包括 UA、NSTEMI、STEMI，其中 UA 與 NSTEMI 合稱 NSTE-ACS。

UA 有急性缺血，卻沒有急性心肌損傷，所以單純 cTn 低還不能叫 UA。NSTEMI 已符合 MI，但沒有典型持續 ST elevation；hs-cTn 抓得到較小損傷，因此部分過去的 UA 現在歸入 MI。

- [2022 ACC pathway §5.7：injury／MI 判定](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)

### 沒有 ST elevation，冠狀動脈就一定還通嗎？

病人可能仍有急性完全阻塞，ECG 卻沒出現 ST elevation。表現會受到受影響區域、導程能否看見、發病時間、側枝、再灌流與傳導異常影響，因此部分／完全血栓的示意，不能直接用來判定眼前血管的通暢程度。

導管再把當時的管腔與血流呈現出來，UA／NSTEMI 與 STEMI 都可能找到能處理的病灶。但微循環尚未被完整看見；要決定 PCI 時機與預期長期獲益，還要回到病人的整體狀態，不能只比較兩張導管影像。

- [2022 ACC pathway §5.2：無 ST elevation 的閉塞線索](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)

**推理邊界**

病史讓缺血機率上升或下降，ECG 與急性心肌損傷再幫忙分出 ACS 類別。

NTG 後減輕不能確認 ACS；沒有 ST elevation 時，也可能有急性完全阻塞。

若 ECG 新出現缺血變化，處理會更急；若序列 cTn 找到急性損傷，原先考慮的 UA 就可能改為 NSTEMI。

**反事實自問：**胸痛按壓可重現，NTG 後減輕，ECG 也沒有 ST elevation，能叫 UA 嗎？

按壓疼痛降低缺血機率，NTG 反應不專屬 ACS，初次 ECG 也可能漏掉短暫缺血或閉塞。UA 還需要確認急性缺血，並用適當序列檢驗確認沒有急性損傷。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.7：胸骨後壓迫感較支持缺血，呼吸或姿勢相關疼痛較少支持，兩端都還要結合其他資料。
- PPT p.10：LR 乘在原本的 AMI 勝算上；若症狀彼此相關，不能把倍率一路連乘。
- PPT p.11：ECG 分出 STEMI／NSTE-ACS，急性損傷再區分 UA 與 NSTEMI。
- PPT p.12：血栓與 ECG 的常見對應，無法保證每位患者都是完全／部分阻塞。
- PPT p.13：兩類 ACS 都可能找到可處理的病灶，PCI 時機還要看當下病況。

**原站修訂／危險邊界註記：**

- p.9：NTG 後緩解可能增加 ACS 可能性 → 原頁同時明示不具特異性、不建議作診斷試驗；網頁不可把反應設為 ACS rule-in／rule-out 分支。（來源註記：已核對; https://academic.oup.com/eurheartj/article/44/38/3720/7243210）
- p.12：STEMI 完全塞住；NSTEMI 顯著狹窄 → 保留原圖常見機轉的教學用途；ECG 分類不能保證血管是完全或部分阻塞。（來源註記：已核對; https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2021 AHA/ACC Chest Pain Guideline 官方 slides](https://professional.heart.org/en/science-news/-/media/dec633637f414ad5bd6937b3059ecab9)
- [2022 ACC pathway §5.2：無 ST elevation 的閉塞線索](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)
- [2023 ESC ACS guideline §3：NTG response 不作診斷動作](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)

**接續：**病況穩定後，第一筆 cTn 的意義取決於何時發作、何時採血。

---

## 03｜Troponin：同一個低值，採血時間決定意義

*先放回發作時間，再解釋數字與升降。*

- 原站 ID：`troponin-time`；原課順序：3；核心主線；課程頁：14、15、16、17、18。

**起始問題：**兩次 cTn 沒有明顯上升，什麼時候還不能放心？

**本節核心判斷：**0 h 是第一次採血，不是胸痛開始。早期一管低於 URL，尚未完成排除；要依症狀時間、ECG 與該試劑的正式路徑接續採樣。

**原課承接：** 症狀與初始 ECG 已形成工作診斷；UA／NSTEMI 的差別要求說明是否有急性心肌損傷。 原文先解釋 troponin 結構，再引用 2018 MI 定義、介紹 hs-cTn 與濃度判讀，最後放入 0/1 h 或 0/2 h 流程。脈絡重建：先懂測量意義，才懂門檻與分流。

**下一步：** 即使已支持急性損傷與缺血，病因仍不只有急性粥樣血栓，因此接著需要 MI 分型與替代解釋。

### 試劑、單位與上限決定數字怎麼讀

檢驗單上的試劑、ng/L 單位與第 99 百分位上限（URL），決定數字怎麼讀。高於 URL 表示心肌損傷，新舊與病因則由時間及其他資料判斷。

high-sensitivity 讓低濃度量得更清楚，因此能看見更小的損傷，也會偵測到冠狀動脈血栓以外的損傷。

- [ACC 2022 §5.2、5.4：ECG、採樣時序與快速分流](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)

### 胸痛 30 分鐘就抽血，0 h 到底在哪裡？

病人胸痛 30 分鐘就抽第一筆，這次採血才叫 0 h；初採後再過 1 h，第二筆已經是發病後 90 分鐘。若把 0 h 當成發病，就可能以為第一次低值已經排除了比實際更多的 MI。

所以同時記下症狀開始、實際採血、結果回報。Delta 算的是兩次採血間的變化，報告晚回來，採血間隔也沒有跟著拉長。若想靠單筆極低值排除，還有試劑與症狀時間的條件；ACC 流程採較保守的發作至少 3 小時，而且 ECG 不能有新缺血。

- [ACC 2022 §5.2、5.4：ECG、採樣時序與快速分流](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)

### 16 變 22，或降到 12，現在多知道了什麼？

第一筆 16 ng/L 若高於當地試劑 URL，顯示心肌損傷。第二筆 22 或 12 增加升降方向；是否有意義，要依採血間隔、分析變異與試劑驗證門檻判斷。短時間的一點差異，可能還不足以判定急性 MI。

確認急性損傷後，相符缺血症狀、新缺血 ECG 或影像才把診斷連到 MI。血栓、供需失衡或其他機轉，則是下一步的病因判斷。

- [ACC 2022 §5.2、5.4：ECG、採樣時序與快速分流](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)
- [ESC 2023 ACS：診斷與侵入策略](https://doi.org/10.1093/eurheartj/ehad191)

### 兩筆差很小，是太早，還是太晚？

早到的病人，第一筆可能尚未升高；晚到的病人，卻可能已經走到下降曲線較平的區段。今天兩筆差不多，看不出昨天是否曾經升高，所以要補上整段症狀、舊 ECG、以前數值，並考慮拉長採樣時間。

同樣地，接近 URL 時，小誤差換成百分比就可能很大，一律用變動 20% 會誤判。快速流程的 absolute delta 是按試劑與時間窗制定；兩筆都低於 URL，或百分比相近，還要放回完整分流條件才知道怎麼走。

- [ACC 2022 §5.2、5.4：ECG、採樣時序與快速分流](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)

### 腎病患者：舊數值與本次升降有何不同？

腎病可伴慢性心肌損傷，也提高真正 MI 的基礎風險。舊數值、本次升降、症狀與 ECG，才能幫忙區分這次高值是哪一種情況。

只用「腎病本來就會高」解釋數字，可能漏掉 MI；反過來，一見高值就照 Type 1 MI 抗栓，也可能把慢性損傷當成血栓處理。

- [2021 AHA/ACC slides：依各院 assay 的 URL 判讀](https://professional.heart.org/en/science-news/-/media/dec633637f414ad5bd6937b3059ecab9)
- [Twerenbold 2018：腎功能不全的0/1小時流程，原研究全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC5794234/)
- [2022 ACC 胸痛急診共識：§5.2、§5.7](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)

### cTn 還在等，眼前的病人已經不能等了嗎？

ECG 新出現缺血變化，病人就已離開低風險快速出院路徑。不過，一次新 ST 下降，和經治療仍控制不住的缺血，急迫程度還有差別。明確 STEMI、不穩定或難治性缺血，則要按眼前病況啟動處理，抽血同時繼續。

若數字還沒達到 rule-out 或 rule-in，就留在 observation 再採血、再看病況。走到 rule-in 時，知道的是異常／高風險，之後還要分清是否 Type 1 MI；走到 MI 排除時，也要回頭解釋胸痛及其他危險疾病。

- [ESC 2023 ACS：診斷與侵入策略](https://doi.org/10.1093/eurheartj/ehad191)
- [ACC 2022 §5.2、5.4：ECG、採樣時序與快速分流](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)

### 腎功能不全時，為何更多人還要留下觀察？（延伸深讀）

Twerenbold 追蹤 3,254 人，其中 487 人 eGFR<60。用 hs-cTnT 時，腎功能不全組的 rule-out 敏感度是 100%，但只有 18% 能直接 rule-out；腎功能正常組則有 68%。因此，能安全排除與能讓多少人快速排除，是兩個不同結果。

另一端也有差別：rule-in 特異性為 88.7% 對 96.5%。腎病沒有讓流程完全不能用，卻使更多人卡在需要觀察的位置；這些結果沒有支持為了多讓人出院，就自行把門檻抬高。透析患者在這組資料裡也沒有被充分代表。

- [Twerenbold 2018：腎功能不全的0/1小時流程，原研究全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC5794234/)

**推理邊界**

cTn 濃度、急慢性、缺血與病因各有不同證據，快速分流還須符合試劑與採樣條件。

互動裡的數字與 URL 是教學設定；實際分流按試劑、採樣窗與病況。晚到 MI 可能只有小 delta，新缺血也不會因 delta 小就消失。

若出現動態缺血，就加快急性冠狀動脈評估；若找到長期穩定高值，慢性損傷較容易解釋這筆數字，但當下仍可能另有缺血。

**反事實自問：**昨晚持續胸痛，今天 120→118 ng/L；另一人發作 30 分鐘初採 8。都能因為沒上升而排除嗎？

第一人可能在上升段之後才來，今天這兩筆看不見昨晚發生了什麼；第二人則可能抽得太早，接著要看序列。若有人同時出現危險 ECG 或病況不穩，就先按當下急迫性處理。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.14：損傷指標的量測意義，是解讀後續序列變化的基礎。（補充）
- PPT p.15：16→22／12 加上升降方向，還要結合採血間隔、試劑門檻與缺血資料才能判斷 MI。
- PPT p.17：同樣濃度的 PPV 會隨情境改變，分流要使用對應試劑的門檻。（補充）
- PPT p.18：適合快速分流者，依同試劑濃度、delta 與時間窗分至三個區域。

**原站修訂／危險邊界註記：**

- p.15：第一次 troponin 16 ng/L 高於正常 → 新發生心肌損傷 → 一筆高於 assay URL 的結果支持損傷，不能獨立確認急性；序列與臨床資料才支持新發生與 MI。（來源註記：已核對; https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/）
- p.17：&gt;5× URL 有 &gt;90% PPV，≤3× URL 的 PPV 約 50–60% → 保留原圖數字作閱讀對象；PPV 依族群與情境改變，不當成所有 assay 的 rule-in cutoffs。（來源註記：已核對; https://academic.oup.com/eurheartj/article/44/38/3720/7243210）
- p.18：有上升 → rule-in；很正常 → rule-out → 須加入 assay-specific baseline／absolute delta、症狀時間、ECG 與 observation 區；rule-in 尚非 Type 1 MI 的最終診斷。（來源註記：已核對; https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2021 AHA/ACC slides：依各院 assay 的 URL 判讀](https://professional.heart.org/en/science-news/-/media/dec633637f414ad5bd6937b3059ecab9)
- [2022 ACC pathway §5.4–5.5：rule-out、intermediate、abnormal](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)
- [原課程引用的 2018 Fourth Universal Definition](https://doi.org/10.1093/eurheartj/ehy462)
- [Twerenbold 2018：腎功能不全的0/1小時流程，原研究全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC5794234/)

**接續：**確認有傷害後，即使造影沒有阻塞，病因也還要追查。

---

## 04｜確認 MI 後：按病因分開治療理由

*ECG 分流、心肌傷害與病因分類各回答不同問題。*

- 原站 ID：`mi-types`；原課順序：4；核心主線；課程頁：19、20。

**起始問題：**已確認缺血性心肌傷害，接著如何解釋病因？

**本節核心判斷：**先確認急性損傷與缺血，再查急性冠狀病理或其他供需失衡。感染、心搏過速或 cTn 很高，都不能單獨替病因定案。

**原課承接：** 前段已建立急性損傷需序列 cTn、MI 還需缺血；尚未確認這個缺血過程的病因。 原文先列 Type I–V 與 Type II 誘因，接著用 MINOCA 及大血管／微血管圖擴展機轉，再提醒其他危險疾病，最後以 Takotsubo 影像示例。此處保留原課程的 2018 定義語境。

**下一步：** 病因不能從 enzyme 自動讀出，於是課程回頭檢查「還有沒有其他 biomarkers 能幫忙」，並交代講者實務中為何看 CPK。

### 先定位三個問題，再讀兩套分類

STEMI／NSTE-ACS用 ECG 與病況處理初始分流；injury／MI釐清傷害與缺血；病因分類再回答缺血從哪裡來。它們不是互斥病名，同一患者可以同時具有這三層描述。

先把急性冠狀病理與其他供需條件分開，後面的抗栓、再灌流與誘因處理才有各自理由。投影片採 2018 用語，下表讓它與 2026 定義接得起來。

### 2018 與 2026：保留機轉，依版本使用名稱

<table><tr><th>正在分類的來源</th><th>2018 原課程</th><th>2026 定義</th></tr><tr><td>急性粥樣血栓</td><td>Type 1</td><td>屬 primary MI；primary 的範圍更廣，並不等於 type 1。</td></tr><tr><td>SCAD、冠狀栓塞、痙攣等急性冠狀病理</td><td>可歸於非粥樣血栓的 type 2 機轉</td><td>納入 primary MI，與其他急性冠狀病理一起釐清。</td></tr><tr><td>另一急性疾病造成供需失衡</td><td>符合缺血性傷害時屬 type 2</td><td>評估 secondary MI；須依定義補足冠狀／心臟影像的客觀條件。</td></tr></table>

因此 primary 不能逐字替換 type 1，secondary 也不能涵蓋整個舊 type 2。2026 secondary 的客觀條件涉及無急性冠狀病理的阻塞性 CAD，和／或新出現、推定新出現的區域壁運動異常或存活心肌喪失；分類須連同原定義及治療指引使用。

- [2026 Fifth Universal Definition：Table 1、§7、§11](https://pmc.ncbi.nlm.nih.gov/articles/PMC13523810/)

### 回讀原課程：Type 1 與 Type 2 在分什麼

已確認 MI 後，再問心肌為何缺血。2018 分型把斑塊破裂或糜爛後形成急性血栓，歸為 Type 1；其他原因使供氧追不上需求、造成缺血性損傷，則歸 Type 2，這類患者可以有，也可以沒有固定 CAD。

STEMI／NSTEMI 告訴我們 ECG 怎麼呈現，還沒有回答上述病因。所以 NSTEMI 可能不是 Type 2，ST elevation 也沒有單獨證明 Type 1。急性血栓試驗是在處理血栓；若這次是別的供需問題，cTn 一樣高，卻不能因此沿用整套血栓治療。

- [2022 ACC pathway §5.7.1–5.7.2：Type 1／2 與治療證據的界限](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)

### 供血沒有完全堵住，氧為何還會不夠？

供應端，貧血降低攜氧量，呼吸衰竭使氧合下降，休克與低血容量使灌流不足。需求端，心跳加快增加耗氧，卻縮短舒張供血時間。慢心律、瓣膜病、主動脈病變、高血壓／左室肥厚與肥厚型心肌病，也可經低輸出、灌流受限或壁張力增加造成失衡。

2018 分型另包含冠狀痙攣、栓塞、血管炎與內皮功能異常等非粥樣血栓機轉。誘因須與缺血的時間及程度相符；例如敗血症只有 cTn 高、沒有缺血證據，可能是非缺血性損傷，也可能同時另有急性血栓。

- [2022 ACC pathway §5.7：Type 2 亦需 ischemia，與 nonischemic injury 可重疊](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)

### PCI 或 CABG 後酵素高了，怎麼判斷？（延伸深讀）

PCI 或 CABG 本身可造成心肌損傷。程序相關 MI 則需符合該版本的門檻，以及新增的缺血、影像或血管證據。

2018 Type 3 處理特定死亡情境，Type 4 涉及 PCI，Type 5 涉及 CABG，各有相應條件。

- [原課程的 2018 Fourth Universal Definition](https://doi.org/10.1093/eurheartj/ehy462)

**推理邊界**

分流、傷害與病因各有證據，不能由單一標籤互相代替。

2018 與 2026 的名稱與部分診斷條件不同；程序相關 MI 也須依實際採用版本判讀。

一旦找到急性冠狀病理，就重新評估其針對性治療；只有誘因、沒有缺血證據時，維持對 injury 病因的追查。

**臨床遷移｜把傷害層次用在感染患者**

教學情境：感染患者 cTn 動態升高，目前沒有相符症狀、ECG 或影像支持缺血。

cTn 的變化先確認新的傷害，感染則提供一個可能誘因；兩者尚未補上缺血證據。

先處理感染並追查傷害原因。若後來出現新缺血證據，立即重新評估病因與急迫性。

**反事實自問：**感染合併動態 cTn，但沒有相符缺血證據，目前可以先確定什麼？

先確認急性心肌損傷，尚不能只由感染與 cTn 直接命名 MI；繼續查缺血與非缺血原因。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.19：Type I–V 在分病因，STEMI／NSTEMI 則在描述 ECG；同一個患者可以同時有這兩種分類。
- PPT p.20：看到供需失衡的疾病後，還要找到急性損傷與相符缺血，才能稱 Type 2 MI。

**原站修訂／危險邊界註記：**

- p.19：Myocardium injury → enzyme↑；Type I–V → 保留原課程 2018 框架；MI 不只需 injury，還需缺血條件。2026 第五版分類已更新，另以版本註記呈現。（來源註記：已核對; https://academic.oup.com/eurheartj/advance-article/doi/10.1093/eurheartj/ehag101/8766309）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [原課程的 2018 Fourth Universal Definition](https://doi.org/10.1093/eurheartj/ehy462)
- [2022 ACC pathway §5.1：早期辨識 ACS、dissection 與 PE](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)
- [AHA 2019 MINOCA statement 官方摘要：診斷、機轉與評估](https://professional.heart.org/en/science-news/contemporary-diagnosis-and-management-of-patients-with-minoca/top-things-to-know)
- [2018 International Expert Consensus on Takotsubo，InterTAK criteria](https://academic.oup.com/eurheartj/article/39/22/2032/5025412)
- [2026 Fifth Universal Definition §1、§7、§11](https://academic.oup.com/eurheartj/advance-article/doi/10.1093/eurheartj/ehag101/8766309)
- [Reynolds 2026：MINOCA的OCT與CMR，原研究公開摘要](https://pubmed.ncbi.nlm.nih.gov/41903131/)
- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [2026 Fifth Universal Definition：Table 1、§7、§11](https://pmc.ncbi.nlm.nih.gov/articles/PMC13523810/)

**接續：**若造影沒有明顯阻塞，哪些急性冠狀或心肌病因仍未被看清？

---

## 05｜造影無阻塞：沿血管壁、血流與心肌找原因

*管腔未阻塞之後，下一項檢查必須對準尚未解決的問題。*

- 原站 ID：`minoca-workup`；原課順序：4；核心主線；課程頁：21、22、23、24、25。

**起始問題：**造影未見阻塞病變，為何仍不能結束病因評估？

**本節核心判斷：**造影未見 ≥50% 狹窄，仍須釐清這次損傷的原因。OCT／IVUS 看血管壁，功能檢查看血流，CMR 看心肌組織；後續治療跟著找到的機轉改變。

**原課承接：** 前段已建立急性損傷需序列 cTn、MI 還需缺血；尚未確認這個缺血過程的病因。 原文先列 Type I–V 與 Type II 誘因，接著用 MINOCA 及大血管／微血管圖擴展機轉，再提醒其他危險疾病，最後以 Takotsubo 影像示例。此處保留原課程的 2018 定義語境。

**下一步：** 病因不能從 enzyme 自動讀出，於是課程回頭檢查「還有沒有其他 biomarkers 能幫忙」，並交代講者實務中為何看 CPK。

### 先分清管腔影像已回答與尚未回答的事

造影已告訴我們拍攝當下未見阻塞性病變；它沒有排除已再通的血栓、細微血管壁病變、痙攣、微循環異常，或非缺血性心肌傷害。先把疑問分成血管壁、血流與心肌組織，才能選下一項檢查。

MINOCA 是需要繼續找原因的工作診斷。原課程 2018／2019 用 myocardial infarction；2026 改為 myocardial injury with non-obstructive coronary arteries。閱讀時保留版本，不能把「無阻塞」直接當成同一種疾病。

- [2026 Fifth Universal Definition：Table 1、§7、§11](https://pmc.ncbi.nlm.nih.gov/articles/PMC13523810/)

### 從原課程辨認仍可能存在的病因

小斑塊破裂、已再通血栓、痙攣、栓塞、SCAD 或微血管異常，都可能藏在非阻塞造影之後。檢查取得的時點也重要：發作已緩解，動態問題可能不再出現在當下影像。

- [AHA 2019 MINOCA statement 官方摘要：診斷、機轉與評估](https://professional.heart.org/en/science-news/contemporary-diagnosis-and-management-of-patients-with-minoca/top-things-to-know)

### 三個疑問，對應三種檢查

<table><tr><th>還沒解決的問題</th><th>主要觀察方法</th><th>找到後會改變什麼</th></tr><tr><td>管腔看不清的 plaque disruption／血管壁病變？</td><td>依疑問選 OCT／IVUS</td><td>支持急性冠狀病理時，重新確立針對性治療理由。</td></tr><tr><td>痙攣或微循環，是否能解釋發作時的灌流不足？</td><td>合適時機的冠狀功能評估</td><td>處理對應血流機轉，並核對是否符合這次事件。</td></tr><tr><td>心肌是缺血型傷害、心肌炎或其他組織型態？</td><td>CMR 等心肌評估</td><td>讓傷害回到正確病因，重新安排治療與追蹤。</td></tr></table>

固定斑塊限制流量儲備；痙攣若已解除，攝影時可能看不到；下游微血管異常，也可在大血管外觀尚可時造成組織灌流不足。

攝影與發作相隔的時間，可能使當時的灌流問題已經改變。發現微血管異常後，要確認它能否解釋這次事件；診斷 Takotsubo 則另需相符的心肌與其他資料。

### 找到斑塊破壞或心肌炎，出院用藥會怎麼改？

若檢查找到斑塊破壞，就更有理由處理粥樣血栓的後續風險。若 CMR 顯示心肌炎，這次損傷就要按心肌炎重新解釋，而不是一直當冠狀動脈血栓治療。

痙攣、栓塞與 SCAD 也各有不同處理。造影寫「無阻塞」時，還沒有替病人選好長期抗栓：永久 DAPT 或停止所有冠病預防，都需要回到查出的原因。

- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)

### 突發胸背痛、低氧或休克，先看哪裡？

突發胸背痛合併灌流缺損或休克，要想到主動脈病變；低氧、右心負荷與 cTn 升高，也可能來自肺栓塞。即使沒有 STEMI，除了 NSTEMI／UA，還有心包膜炎、心衰竭與 Takotsubo 等原因要分辨。

cTn 高只告訴我們心肌受損，尚未替這些病人選好 ACS 抗栓。若眼前已休克、嚴重心律不整或呼吸衰竭，就同時找原因、處理不穩定，不能先等低風險抽血流程跑完。

- [2022 ACC pathway §5.1：早期辨識 ACS、dissection 與 PE](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)

### 造影正常，下一個問題在血管壁還是心肌？（延伸深讀）

若懷疑血栓一度形成、之後已溶開，就用 OCT 尋找管腔攝影沒看清的 culprit。若要問心肌究竟有沒有缺血型組織傷害，CMR 更能幫忙區分；兩項檢查看的部位與問題不同。

2026 多中心研究中，兩項都完成的人，有 79% 找到病因：59% 為缺血性，20% 為非缺血模仿病況；造影正常的人，也有 27% 在 OCT 找到 culprit。這說明查下去可能找到不同原因；至於所有人都做兩項，是否能改善預後，這個診斷研究沒有用治療 RCT 回答。

- [Reynolds 2026：MINOCA的OCT與CMR，原研究公開摘要](https://pubmed.ncbi.nlm.nih.gov/41903131/)

### 左室短暫收縮變差，何時考慮 Takotsubo？（延伸深讀）

胸痛、ECG／cTn 改變合併短暫左室功能異常，會讓人考慮 Takotsubo。常見 apical ballooning，也可呈中段或其他壁運動型態；停經後女性較常見，但壓力誘因可以缺乏，顯著 CAD 也可共存。

冠狀評估、壁運動分布及後續恢復共同協助診斷，必要時用 CMR 分辨心肌炎等原因。急性期仍可能休克或出現心律不整，不能因預期會恢復就延後處理。

- [2018 International Expert Consensus on Takotsubo，InterTAK criteria](https://academic.oup.com/eurheartj/article/39/22/2032/5025412)

**推理邊界**

急性損傷與缺血確認 MI；ECG、冠狀解剖及其他檢查再釐清病因。

影像研究說明檢查能找到哪些病因；它還沒有證明每位 MINOCA 都做同一套檢查、吃同一套抗栓，預後就會更好。

找到斑塊破壞，就朝粥樣血栓處理；找到心肌炎或其他原因，就調整相應治療，已發生的損傷與不穩定也繼續處理。

**反事實自問：**造影無阻塞，為何不能直接決定永久 DAPT 或停止所有治療？

無阻塞尚未確定傷害機轉。須追查血管壁、血流與心肌原因，再讓治療對準找到的病因。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.22：固定斑塊、動態痙攣與微血管異常，都可能在不同位置減少心肌灌流。
- PPT p.25：Takotsubo 的 ECG 與壁運動可像 MI，冠狀與心肌評估再幫忙分清原因。

**原站修訂／危險邊界註記：**

- p.21：&lt;50% 狹窄＋酵素高 → MINOCA，損傷不是來自 epicardial narrowing → 在原課程語境須先成立 MI 並找原因；非阻塞不排除 epicardial plaque disruption／spasm。2026 名稱又改為 injury，勿把兩版本無標記地混合。（來源註記：已核對; https://professional.heart.org/en/science-news/contemporary-diagnosis-and-management-of-patients-with-minoca/top-things-to-know）
- p.23：If not STEMI, think of other cardiac possibility → 用作擴大鑑別提醒；不表示已排除 NSTEMI／UA，也不表示必須等 STEMI 排除後才評估其他致命原因。（來源註記：已核對; https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/）
- p.24：無 culprit &gt;50% 狹窄、通常情緒壓力、apical±midsegment → 原頁是簡化描述；InterTAK 允許 CAD 共存、誘因可缺乏，壁運動也可有其他型態。（來源註記：已核對; https://academic.oup.com/eurheartj/article/39/22/2032/5025412）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [原課程的 2018 Fourth Universal Definition](https://doi.org/10.1093/eurheartj/ehy462)
- [2022 ACC pathway §5.1：早期辨識 ACS、dissection 與 PE](https://pmc.ncbi.nlm.nih.gov/articles/PMC10691881/)
- [AHA 2019 MINOCA statement 官方摘要：診斷、機轉與評估](https://professional.heart.org/en/science-news/contemporary-diagnosis-and-management-of-patients-with-minoca/top-things-to-know)
- [2018 International Expert Consensus on Takotsubo，InterTAK criteria](https://academic.oup.com/eurheartj/article/39/22/2032/5025412)
- [2026 Fifth Universal Definition §1、§7、§11](https://academic.oup.com/eurheartj/advance-article/doi/10.1093/eurheartj/ehag101/8766309)
- [Reynolds 2026：MINOCA的OCT與CMR，原研究公開摘要](https://pubmed.ncbi.nlm.nih.gov/41903131/)
- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [2026 Fifth Universal Definition：Table 1、§7、§11](https://pmc.ncbi.nlm.nih.gov/articles/PMC13523810/)

**接續：**病因評估持續進行；下一章用 ECG 補上當時的方向與動態資訊。

---

## 06｜CPK 延伸：酵素下降不能證明缺血結束

*保留原課程的實務延伸，主線可直接進入 ECG。*

- 原站 ID：`beyond-troponin`；原課順序：5；延伸閱讀；課程頁：26、27、28。

**起始問題：**CPK 或 CK-MB 的升降，能告訴我們什麼？

**本節核心判斷：**CPK 或 cTn 下降描述血中訊號的變化；目前是否仍缺血，要回到新症狀、ECG、循環與影像。

**原課承接：** MI 分型與替代診斷已說明：酵素升高不自動揭示病因，非阻塞管腔也不代表沒有損傷。 原文先說其他 biomarker 不作常規 ACS 診斷，再介紹 CPK 同工酶與心肌來源比例，最後用「In practice」切換成講者以 CPK 追蹤的心得。這個身分切換本身就是必須讀懂的課程脈絡。

**下一步：** 生物標記有時間延遲與病因限制，因此接下來要回到 ECG：哪些電氣型態能比等待 peak 更早揭示危險？

### CK 高了，先問是心肌還是骨骼肌

看到總 CK 上升，先找肌肉來源，因為骨骼肌也會釋出 CK。CK-MB 比總 CK 更偏向心肌，特異性與敏感度卻仍不如 cTn。

再看 CK-MB／CK 比例時，分母、採樣時點與共存肌肉損傷都會改變數字。因此這個比例只能增加來源資訊，診斷 MI 還要接上病況與其他證據。

- [2021 AHA/ACC 官方 slides：有 cTn 時 CK-MB／myoglobin 無額外診斷用途](https://professional.heart.org/en/science-news/-/media/dec633637f414ad5bd6937b3059ecab9)

### 數字下降了，血管與微循環恢復了嗎？

CPK 下降反映標記釋放與清除的時間曲線，尚未確認血管通暢、微循環恢復或沒有再缺血。

晚到患者是否開通，仍由目前的症狀、ECG、循環及晚期 PCI 證據判斷，不能只看是否已過 peak。

### 數字與病人看起來不同，先查哪一邊？

症狀惡化而檢驗不相符時，處理病況與重新找原因同步進行。核對檢體、採樣時點、單位及分析干擾後，追查心肌與非心肌來源，也重新評估初步診斷。

**推理邊界**

總 CK 與 CK-MB 提供組織來源資訊；抽血看到的曲線，會隨釋放、清除與採樣時間改變。

CK-MB 比例還不能診斷 MI，CPK 沒升或已下降時，也可能仍有缺血。

若又胸痛、ECG 改變或循環惡化，就加快處理；新找到的肌肉傷害可解釋總 CK，但不能抹去另外已確認的心肌損傷。

**反事實自問：**PCI 後 CPK 已下降，病人卻又胸痛並出現新 ST 變化，現在看哪個？

新胸痛與 ST 變化提示可能有新缺血或介入相關問題，應立即重評。CPK 下降不能成為等待下一筆數值的理由。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.27：CK 同工酶與比例先幫忙找組織來源，MI 診斷再接上缺血與損傷資料。（補充）
- PPT p.28：標記各有不同釋放與清除速度，下降時冠狀灌流未必已恢復。（補充）

**原站修訂／危險邊界註記：**

- p.27：CK-MB／CPK &gt;5–6% 支持心肌來源 → 保留原課程與教材的來源辨認線索；並非 MI 定義，activity／mass assay、單位與情境需核實，未將該值轉成網站通用決策。（來源註記：原文數值保留；院內 assay／relative index 待核）
- p.28：真正 MI 其 CPK 會顯著上升；密集追蹤至下降 → 明標講者經驗；不是所有 MI 的必要條件。cTn 已可用時，常規加做 CK-MB／myoglobin 不增加急性損傷診斷價值；CPK 下降不能證明無 ongoing ischemia。（來源註記：已核對; https://professional.heart.org/en/science-news/-/media/dec633637f414ad5bd6937b3059ecab9）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [原課程引用：2023 ESC ACS guideline](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2021 AHA/ACC 官方 slides：有 cTn 時 CK-MB／myoglobin 無額外診斷用途](https://professional.heart.org/en/science-news/-/media/dec633637f414ad5bd6937b3059ecab9)

**接續：**同樣的區分會在 PCI 後再次出現：血管、組織與功能各自量測。

---

