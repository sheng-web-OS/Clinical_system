# ACS 原站研究擷取｜把治療接到病程

> 私有研究快照｜2026-10-27｜**DRAFT/HOLD，不是已通過醫學審查的正式教材**。來源：[ACS｜理解與臨床判斷](https://acs-deep-learning.dreamycarp4.chatgpt.site/) 的 data/units.json。經第三方 HTML 清洗後逐單元 JSON 解析而得，**不具有來源 bytes 保真性**；原圖、可執行互動、第三方 PPT/ECG 影像均未匯入，不能冒充完整原站。章節計畫為 10 主線＋1 延伸，本快照實際完整擷取 11 節。個別單元保留 sourceOrder、來源 PPT 頁次、來源 URL、figure caption 與安全註記；需要對原網與原始投影片逐段比對。

## 17｜初始治療：支持循環、抗栓與再灌流並行

*每一筆醫囑各改變哪個環節。*

- 原站 ID：`initial-treatment`；原課順序：16；核心主線；課程頁：65、66、67、68、69、70。

**起始問題：**胸痛、血氧和血壓，哪一個才是這筆醫囑要改善的？

**本節核心判斷：**低氧才補氧，疼痛與循環依條件處理；症狀改善後仍須接續抗栓與再灌流評估，因為疼痛減少沒有證明血栓已解除。

**原課承接：** 原課程前段已訓練高風險 ECG 的辨識；p.65 轉入 Treatment。能辨識危險之後，接著要把判斷轉為即時行動。 p.66 先並列 Medication 與 Reperfusion，p.67 暫時聚焦 Medication；p.68–70 以 MONA 打開初始用藥，先拆除反射性處方。這個轉折為原頁明示。

**下一步：** 止痛、補氧與血流動力學支持仍未處理持續形成的冠狀動脈血栓，因此下一段進入抗凝血與抗血小板兩條不同的抗栓路徑。

### 藥給下去時，也要繼續準備再灌流

病人正在胸痛，我們會同時看ECG、血壓與末梢灌流。藥物可以改善氧合、疼痛、供需失衡與血栓；造成缺血的血管問題，則要靠再灌流處理。

給藥與聯絡導管室可以並行。若循環開始不穩，循環支持也要跟上，別等藥一項項給完才決定要不要緊急開通。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### 血氧已經足夠，多給氧還能幫上什麼？

冠狀動脈堵住時，問題出在血流。血液本身若已有足夠的氧，再把飽和度拉高，能不能讓病人活得更好？DETO2X-AMI就比較了這件事：6,629名疑似MI、SpO₂≥90%的患者，隨機給氧或呼吸室內空氣。

一年死亡率是5.0%對5.1%，HR 0.97（95% CI 0.79–1.21）。常規補氧沒有顯示出預期的死亡獲益。因此血氧足夠時，不必因為懷疑MI就反射性給氧。

若SpO₂降到<90%，或新出現呼吸衰竭，眼前已多了一個氧合問題，這時就需要相應的呼吸支持。DETO2X納入的是血氧≥90%的人，沒有回答低血氧患者也不補氧會怎樣。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [DETO2X-AMI 2017：常規氧氣與室內空氣RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1706222)
- [2025 AHA/ACC ACS guideline：官方臨床投影片](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)

### Nitrate減少回心血量，為何有時舒服、有時血壓更低？

Nitrate經NO–cGMP讓血管平滑肌鬆弛。靜脈一擴張，回到心臟的血就少一些，心室前負荷和壁張力下降，耗氧也跟著減少，胸痛因此可能緩解。

右室梗塞時，右室已經打不太動，左室能收到多少血，更依賴足夠的靜脈回流。此時再減少回心血量，輸出量可能往下掉，血壓與冠脈灌流壓也一起下降。

這就接回低血壓、右室梗塞、severe AS、顯著bradycardia或tachycardia時的用藥限制。近期若用過PDE-5 inhibitor，兩者都增強cGMP，還可能造成嚴重低血壓；24–48小時間隔要依實際藥名與作用時間確認。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### Morphine讓病人不痛了，剛吞的ticagrelor呢？

口服藥先要被吸收，才有辦法抑制血小板。IMPRESSION的70人藥動/藥效試驗，先給morphine 5 mg，再給ticagrelor 180 mg。結果前12小時的藥物暴露下降36%，達峰時間由2小時延到4小時，早期血小板抑制也比較弱。

病人不痛了，但剛吞下去的loading可能還沒充分起效。Opioid留給確實需要止痛的情境，同時繼續處理缺血。至於morphine是否因此增加死亡，這個小型藥動/藥效試驗回答不了。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [IMPRESSION：morphine與ticagrelor，藥動/藥效RCT全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC4712351/)
- [2025 AHA/ACC ACS guideline：官方臨床投影片](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)

### 痛少了之後，回頭看ECG與灌流

Nitrate後不痛了，接著看ECG有沒有改變、血壓撐不撐得住、末梢灌流如何，再連上後續檢驗。疼痛本來就可能有其他來源，血管也可能只有暫時再通，單靠止痛反應很容易判斷過頭。

若血壓下降，要重想nitrate還能不能給；若ECG仍很危險，再灌流的急迫性就還在。抗栓前也要持續確認ACS的判斷是否合理，有沒有出血或其他病因需要改變做法。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

**推理邊界**

藥物改善與再灌流評估可以並行。

止痛反應不足以判定冠狀動脈已持續通暢。

新低血氧就補上氧合支持；低血壓或右室受累就重想nitrate。眼前的高危缺血仍要繼續處理。

**反事實自問：**STEMI已吞ticagrelor，morphine後不痛了，能否認為抗栓已到位、暫時不用急？

Morphine可能讓口服藥吸收變慢；不痛不代表loading已充分起效，緊急再灌流仍須繼續。給藥時間要記清楚，這項藥動試驗沒有告訴我們該自行再補一倍loading。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.66：藥物改善氧合、疼痛與血栓，再灌流處理受阻血流。
- PPT p.69：低血氧需要補氧，血氧正常時常規給氧沒有臨床獲益。
- PPT p.70：Nitrate 減少回心血量，因此低血壓與右室梗塞時可能惡化灌流。

**原站修訂／危險邊界註記：**

- p.68：除了 Antithrombotic agents，其他不應該是反射性給予。 → 保留反對常規 MONA 的教學重點；抗栓仍需合理工作診斷及出血／替代診斷評估，不能延伸成所有胸痛皆反射性抗栓。（來源註記：已核對｜指引條件補回; https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009）
- p.70：PDE-5 inhibitor use within 24–48 h。 → 原圖概括常見作用時間；實際停藥間隔與特定藥物相關，網站不產生統一 24 小時安全倒數。（來源註記：已核對｜原表述範圍補回; https://academic.oup.com/eurheartj/article/44/38/3720/7243210）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [DETO2X-AMI 2017：常規氧氣與室內空氣RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1706222)
- [2025 AHA/ACC ACS guideline：官方臨床投影片](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)
- [IMPRESSION：morphine與ticagrelor，藥動/藥效RCT全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC4712351/)

**接續：**抗凝與抗血小板同時出現，是因為血栓由兩套互相放大的系統形成。

---

## 18｜抗凝：等待期與 PCI 需要的保護不同

*從出血與導管血栓的反向結果，追到接觸凝血。*

- 原站 ID：`anticoagulation`；原課順序：17；核心主線；課程頁：71、72、73、74、75。

**起始問題：**Fondaparinux已經在抗凝，進PCI為何還要補UFH？

**本節核心判斷：**等待期使用 fondaparinux 的 NSTE-ACS，進 PCI 要補 UFH；fondaparinux 不能單獨支援 primary PCI。器械表面的接觸促凝，解釋了這個差別。

**原課承接：** MONA 段落已說明支持與止痛各有條件；接下來需要處理與冠狀動脈粥樣血栓較直接相關的藥物。 p.71 展示急性抗栓全圖，p.72 放大 anticoagulation 並依 STEMI／NSTE-ACS 與導管時程區分；p.73–74 依次放入美國劑量表及 ESC 腎功能表；p.75 才把抗凝與抗血小板標的分開。

**下一步：** 這一段先解釋凝血系統，再讓 p.75 的藥物標的圖銜接 p.76 的 Choice→Pretreatment→Duration。抗凝時程不能直接套到抗血小板。

### 血小板與fibrin互相放大

DAPT壓低血小板活化，抗凝藥壓低thrombin–fibrin。兩邊會互相放大，常需要一起處理；藥合併得越多，止血也越困難。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### 先辨認這次抗凝保護的是哪個時段

<table><tr><th>時段</th><th>正在處理的來源</th><th>判斷的實際改變</th></tr><tr><td>診斷後等待</td><td>冠狀事件的持續成栓與再缺血</td><td>依侵入時程、出血與腎功能選初始抗凝。</td></tr><tr><td>PCI 操作中</td><td>病灶加上導管與器械的接觸表面</td><td>核對先前給藥、時間與操作抗凝；fondaparinux 使用者加 UFH。</td></tr><tr><td>操作結束後</td><td>操作風險結束，但 ACS／支架與其他病因可能仍在</td><td>分開決定抗血小板療程，以及是否另有 OAC 適應症。</td></tr></table>

STEMI準備primary PCI時，常用UFH；enoxaparin或bivalirudin則依情境作替代。NSTE-ACS即使還在等導管，冠脈血栓與再缺血風險也沒有停下來，等待期仍要安排適合的抗凝。

若不預計早期導管，2023 ESC偏好fondaparinux，無法取得時考慮enoxaparin；2025 AHA/ACC把兩者列為UFH的推薦替代選擇。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### 出血比較少，為什麼導管血栓反而比較多？

OASIS-5預先規劃的6,238位PCI子分析。Fondaparinux對enoxaparin，第9天major bleeding是2.4%對5.1%，確實少了出血；但導管血栓是0.9%對0.4%，方向反過來。

保留等待期較少出血的好處，進PCI時補UFH處理操作風險。因此fondaparinux不能單獨拿來支援STEMI primary PCI。

補UFH不是在這個子分析裡獨立隨機比較的；醫囑仍依指引、原先給過的藥與時間安排。也別把這個特定補藥情境，當成可以任意交替UFH與LMWH。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [OASIS-5 PCI：出血與導管血栓，預先規劃子分析](https://pubmed.ncbi.nlm.nih.gov/17964037/)
- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [2025 AHA/ACC ACS guideline：官方臨床投影片](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)

### 多出來的接觸表面，如何啟動凝血？

Yau的實驗發現，拿掉血漿裡的factor XII，導管的促凝作用就消失了。

在這種接觸誘發凝血裡，fondaparinux單用沒能阻止凝血；補上heparin或bivalirudin才改善。這讓「已經抑制Xa，為何還缺保護」有了機轉上的解釋。

這一步來自體外與動物實驗；補UFH的臨床依據仍須接上臨床資料與指引。

- [Yau 2011：導管誘發凝血的體外/兔模型](https://pubmed.ncbi.nlm.nih.gov/21937693/)

### 這一劑用於初始治療，還是支援PCI？（延伸深讀）

2025 AHA/ACC的UFH初始方案是60 IU/kg loading，上限4,000 IU；接12 IU/kg/h infusion，初始上限1,000 IU/h，再依aPTT調整。若尚未抗凝、現在準備PCI，bolus是70–100 U/kg，後續看ACT與操作情況。

Enoxaparin初始治療通常是1 mg/kg皮下每12小時；CrCl<30 mL/min改每24小時。若走fibrinolysis，還有年齡、bolus與時程規則。劑量須銜接已給過的藥與院內protocol。

- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### 腎功能變差，藥效可能留得更久

LMWH、fondaparinux與bivalirudin的藥物暴露會受腎功能影響。清除減少時，出血風險可能上升，所以要按各藥規則調整。UFH可用凝血檢驗調整，也能以protamine逆轉，但反應有變異，且要留意heparin-induced thrombocytopenia（HIT）；已知HIT就要改選替代藥。

看到檢驗單上的eGFR，還要確認劑量規則用的是不是Cockcroft–Gault CrCl。兩個數字不是自動相同，先核對計算方式、治療情境與地區標示，再決定劑量。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### PCI結束後，哪一個抗栓理由還留下來？

器械操作完成，操作抗凝通常就結束；bivalirudin若有指定的短時程infusion，則把該方案完成。接著問有沒有AF、已確認左室血栓或其他需要繼續抗凝的原因。

另一方面，ACS與支架帶來的血小板風險還在，適合的抗血小板療程要繼續。

快速轉送會影響藥在急診或導管室給，但不會把等待期的風險拿掉。2025 AHA/ACC與2023 ESC都涵蓋診斷後等待、或不採早期侵入的ACS抗凝。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

**推理邊界**

抗凝與DAPT的目的、時程可以不同。

等待期的較低出血率，不能取代PCI操作抗凝。

導管延遲就重想等待期選藥；進PCI就核對操作抗凝；做完後再問有沒有AF或左室血栓，決定抗凝是否繼續。

**反事實自問：**已用fondaparinux的NSTE-ACS，隔天決定PCI；「已抗凝」為何不足以刪掉UFH bolus？

UFH補的是PCI操作風險。病人已接受抗凝，還須核對已用藥、時間、腎功能與出血，不能當成從未抗凝。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.71：急性抗凝選擇取決於 ACS 類型與預計導管時程。（補充）
- PPT p.73：初始治療、PCI 與 fibrinolysis 使用不同抗凝劑量及監測。
- PPT p.74：腎功能下降會改變藥物暴露、劑量間隔與可用性。
- PPT p.75：凝血因子與血小板訊號互相放大，需要不同藥物標的。（補充）

**原站修訂／危險邊界註記：**

- p.72：NSTEMI 確定要 24 小時內做導管才會給 heparin。 → 原講者實務描述與一般指引範圍不同。2025 AHA/ACC §4.4 及 2023 ESC §6.2 支持在診斷時給 ACS 急性期抗凝，且明確涵蓋不採早期侵入者；不應當成只在早期導管者才抗凝。（來源註記：已核對｜地方實務與指引分開; https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009）
- p.72：Fondaparinux 只能用在 NSTEMI 且沒有要馬上做導管的狀況。 → 本段情境是 NSTE-ACS 等待期與 primary PCI；核心限制是不可單獨支援 PCI，進 PCI 須加 UFH。不能把這句外推至它所有核准適應症或溶栓路徑。（來源註記：已核對｜適用範圍補回; https://academic.oup.com/eurheartj/article/44/38/3720/7243210）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [OASIS-5 PCI：出血與導管血栓，預先規劃子分析](https://pubmed.ncbi.nlm.nih.gov/17964037/)
- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [2025 AHA/ACC ACS guideline：官方臨床投影片](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)
- [Yau 2011：導管誘發凝血的體外/兔模型](https://pubmed.ncbi.nlm.nih.gov/21937693/)

**接續：**再看血小板這一邊：不同 P2Y12 的活化、起效與限制如何影響選擇？

---

## 19｜P2Y12 選藥：起效、治療路徑與出血一起看

*先建立活化與暴露，再讀藥物比較試驗。*

- 原站 ID：`p2y12-choice`；原課順序：18；核心主線；課程頁：76、77、78、79、80、81、82、83、84、85、86、87、88、89、90、91、92。

**起始問題：**Prasugrel或ticagrelor比較強，為什麼還會選clopidogrel？

**本節核心判斷：**ACS 已決定 PCI，通常優先 ticagrelor 或 prasugrel；既往 stroke／TIA 排除 prasugrel。另需 OAC 時通常優先 clopidogrel；口服不可行則另處理途徑與銜接。

**原課承接：** p.75 已把抗凝與抗血小板的標的分開。p.76 接著明示抗血小板的三個問題：Choice、Pre-treatment、Duration。 p.77–83 先建立 aspirin＋P2Y12 的共同底座與指引選擇，p.84–88 插入 prasugrel 區域劑量與課程實務，p.89–92 再用三個主要 RCT 解釋療效、出血與歐洲對 prasugrel 的相對偏好。這個先機轉、再選藥、再回試驗的局部順序予以保留。

**下一步：** 即使選定了可能適合的 P2Y12，冠狀動脈解剖未知時是否立刻給，仍是另一題；ISAR–REACT 5 的給藥時點差異正好把 Choice 接到 Pretreatment。

### 兩條血小板訊號

Aspirin抑制COX-1/TXA₂，P2Y12抑制劑阻斷ADP放大訊號。兩條都壓低，血栓較不容易延續。新支架需要保護，ACS本身也有血栓風險，因此DAPT的用途不只在支架。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### Clopidogrel先要活化，反應就多了一個變數

Clopidogrel是prodrug。多數先變成無活性產物，只有少部分經CYP活化；CYP2C19 loss-of-function或交互作用，都可能讓活性代謝物減少，血小板抑制也跟著改變。

Prasugrel也要活化，但效率較高；ticagrelor本身就能直接、可逆地抑制P2Y12，另外還有活性代謝物。這解釋它們為何通常較快、反應較一致。

但不能看到族群就猜個人基因型。若出血風險高、合併OAC，或potent drug有禁忌、無法取得，clopidogrel仍可能更適合。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### 先看口服選藥的臨床交換：少哪些事件，多哪些代價

代謝較快、抑制較一致，必須再接到患者結局。TRITON 與 PLATO 分別提供 prasugrel／ticagrelor 相對 clopidogrel 的證據；每項試驗的族群與出血定義都要保留。

<table><tr><th>比較</th><th>核心結果</th><th>對選藥的意義</th></tr><tr><td>TRITON：預計 PCI 的 ACS，prasugrel 對 clopidogrel</td><td>缺血複合事件較少，non-CABG TIMI major bleeding 較多。</td><td>較強抑制要用缺血保護與出血代價共同解釋；既往 stroke／TIA 等限制仍須先排除。</td></tr><tr><td>PLATO：ACS，ticagrelor 對 clopidogrel</td><td>CV death／MI／stroke 較少；total major 未顯著增加，但 non-CABG major 較多。</td><td>「出血相近」必須說明終點，不能解讀成沒有額外出血代價。</td></tr><tr><td>ISAR-REACT 5：ticagrelor 與 prasugrel 整體策略</td><td>藥物與 NSTE-ACS 給藥時點同時不同。</td><td>比較結果含有策略差異，不能全部算成單一分子的藥力。</td></tr></table>

完整曲線、事件率與入選條件保留在下方深讀。這三項試驗不能跨研究拼成不分情境的藥物排名。

- [TRITON–TIMI 38｜NEJM 2007 原研究](https://www.nejm.org/doi/full/10.1056/NEJMoa0706482)
- [PLATO｜NEJM 2009 原研究](https://www.nejm.org/doi/full/10.1056/NEJMoa0904327)
- [ISAR-REACT 5：兩種P2Y12給藥策略RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1908973)
- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)

### 藥物排序取決於治療路徑

ACS準備PCI，2025 AHA/ACC推薦ticagrelor或prasugrel優於clopidogrel。2023 ESC對將接受PCI的ACS，還列出可考慮prasugrel優於ticagrelor（IIa B）。

若病人曾有stroke/TIA，prasugrel就不能用；高齡或低體重，還要重看出血與劑量。若改成保守治療、CABG或fibrinolysis，也要重新選擇。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [AHA 2025 ACS｜官方重點摘要，第 1–2 點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)

### 把條件直接接到選擇

<table><tr><th>已知條件</th><th>對應安排</th></tr><tr><td>ACS，已決定 PCI，沒有相應禁忌</td><td>通常優先 ticagrelor 或 prasugrel，並衡量出血。</td></tr><tr><td>既往 stroke／TIA</td><td>排除 prasugrel，從其他合適方案選擇。</td></tr><tr><td>另需長期 OAC 的合併療程</td><td>P2Y12 通常優先 clopidogrel，並另定 aspirin 的短期安排。</td></tr><tr><td>現在要 PCI、P2Y12-naïve，口服吸收不可行</td><td>可考慮 IV cangrelor；同時安排之後口服銜接，避免藥效空窗。</td></tr></table>

高出血風險還會影響總體策略與療程。先選可用的藥，再到下一節決定是否在 anatomy 未知前給；兩項決策分開成立。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [AHA 2025 ACS｜官方重點摘要，第 1–2 點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)

### 口服吸收失敗時，再處理給藥途徑

口服藥先要進到血中。嘔吐、休克或 opioid 可能延遲暴露；換成另一顆口服藥，並不保證能立即起效。

若已決定 PCI、尚未用 P2Y12 而口服吸收不可行，可考慮快速靜脈抑制，再按轉換規則銜接口服。這是特定操作情境的安排，不是所有患者都另加針劑。

- [2025 AHA/ACC ACS §4.3.3與Table 9：IV P2Y12及轉換時點](https://www.ahajournals.org/doi/pdf/10.1161/CIR.0000000000001309)
- [CHAMPION PHOENIX：cangrelor與clopidogrel的PCI RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1300815)

### TRITON：少一些缺血，代價是多少出血？（延伸深讀）

13,608位預計PCI的中高風險ACS患者，都先有aspirin，再比較prasugrel 60/10 mg與clopidogrel 300/75 mg。追蹤6–15個月，CV death/nonfatal MI/nonfatal stroke為9.9%對12.1%，prasugrel較少。

non-CABG TIMI major bleeding是2.4%對1.8%，prasugrel較多。STEMI子群沒見到出血顯著增加，也不能替眼前高齡、低體重或有stroke/TIA的病人消除風險與限制。

- [TRITON–TIMI 38｜NEJM 2007 原研究](https://www.nejm.org/doi/full/10.1056/NEJMoa0706482)

### PLATO說出血相近，指的是哪一種出血？（延伸深讀）

PLATO的18,624位ACS包含侵入與非侵入治療。在aspirin上，比較ticagrelor 180 mg loading/90 mg twice daily與clopidogrel；12個月CV death/MI/stroke為9.8%對11.7%，ticagrelor較少。

若只看total major bleeding，11.6%對11.2%，沒有顯著差異。把CABG相關出血拿開，再看non-CABG major bleeding，就變成4.5%對3.8%，ticagrelor較多。

- [PLATO｜NEJM 2009 原研究](https://www.nejm.org/doi/full/10.1056/NEJMoa0904327)

### ISAR連給藥時間也一起改了（延伸深讀）

ISAR的4,018位ACS都預計侵入評估，約84%最後接受PCI。一年全因death/MI/stroke，ticagrelor策略9.3%、prasugrel策略6.9%；BARC 3–5出血為5.4%對4.8%，未顯著不同。

Ticagrelor普遍先loading；prasugrel在NSTE-ACS則等解剖確認、決定PCI才給。藥物換了，時間也換了，因此看到的差異無法全算到分子藥力上。

劑量也要看清：prasugrel的維持量標準10 mg，特定≥75歲或<60 kg者才5 mg，並非全體都用5 mg。

- [ISAR-REACT 5：兩種P2Y12給藥策略RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1908973)
- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)

### PRASFIT的兩條曲線，究竟比較了哪兩種用法？（延伸深讀）

PRASFIT把日本1,363位ACS/PCI患者，分成prasugrel 20/3.75 mg與clopidogrel 300/75 mg。24週MACE是9.4%對11.8%，HR 0.77，95% CI 0.56–1.07。曲線看起來偏向prasugrel，但CI跨1，還不能宣稱優越。

它沒有把prasugrel 20/3.75和60/10 mg放在同一試驗比較。所以這張圖回答不了兩種prasugrel劑量是否等效。實際開藥時，要回到當地核准、年齡體重與禁忌，而不是用「亞洲人」三個字決定劑量。

- [PRASFIT–ACS｜Circ J 2014，日本隨機試驗](https://www.jstage.jst.go.jp/article/circj/78/7/78_CJ-13-1482/_article)
- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### Loading先起效，maintenance再把抑制維持住（延伸深讀）

<table><tr><th>藥物</th><th>劑量</th><th>條件</th></tr><tr><td>Aspirin</td><td>美國 loading 162–325 mg；ESC 150–300 mg；維持 75–100 mg daily</td><td>300／100 mg 符合範圍；急性 loading 使用適當非腸溶製劑。</td></tr><tr><td>Clopidogrel</td><td>非溶栓 ACS loading 300 或 600 mg；75 mg daily</td><td>PCI、fibrinolysis 與高齡情境分開。</td></tr><tr><td>Ticagrelor</td><td>180 mg loading；90 mg twice daily</td><td>急性 ACS 方案；延長治療另看適應症及劑量。</td></tr><tr><td>Prasugrel</td><td>日本 PRASFIT：20／3.75 mg；ESC／美國：60 mg loading、10 mg daily</td><td>西方方案中，特定高齡／低體重採 5 mg；須依地區標示與適用條件。</td></tr></table>

體重、已給過的藥與再灌流方式會影響劑量；prasugrel須區分地區方案。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [PRASFIT–ACS｜Circ J 2014，日本隨機試驗](https://www.jstage.jst.go.jp/article/circj/78/7/78_CJ-13-1482/_article)

### 靜脈替代深讀：cangrelor 證據與口服銜接（延伸深讀）

口服藥必須先進到血中。若現在就要PCI、尚未用P2Y12，口服吸收又不可行，2025美國指引列IV cangrelor為可考慮選項（IIb B-R）。它直接、快速作用，停輸後約1小時血小板功能恢復，可以把藥效安排在操作時段。

CHAMPION PHOENIX和clopidogrel比較，48小時缺血複合事件是4.7%對5.9%。這個對照沒有比較ticagrelor或prasugrel，也沒有回答已吞loading的人是否都要再加針劑。

轉口服時，針劑已停、口服卻還沒起效，中間就可能少了一段抑制。

- [2025 AHA/ACC ACS §4.3.3與Table 9：IV P2Y12及轉換時點](https://www.ahajournals.org/doi/pdf/10.1161/CIR.0000000000001309)
- [CHAMPION PHOENIX：cangrelor與clopidogrel的PCI RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1300815)

**推理邊界**

Potent P2Y12 可減少合適 ACS／PCI 族群的缺血事件，選擇仍須權衡出血與禁忌。

PLATO的總出血與non-CABG出血要分開；ISAR連給藥時間也不同；PRASFIT沒有直接比較兩種prasugrel劑量。

看到stroke/TIA就排除prasugrel；另有OAC就重想組合；解剖和PCI計畫確定後，再決定給哪個、何時loading。

**反事實自問：**為何 prasugrel 在 ISAR 表現較好，仍不能推成所有亞洲 ACS 都用 3.75 mg？

ISAR連用藥時點一起比較，主要維持劑量是10 mg；3.75 mg來自日本PRASFIT，MACE未達優越。兩者不能證明所有亞洲患者都適用同一劑量；仍須符合PCI計畫、stroke/TIA、出血、年齡體重與當地標示。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.76：P2Y12 的選擇、開始時點與療程，分別影響缺血及出血。
- PPT p.78：Clopidogrel 需代謝活化，CYP2C19 變異會影響藥效。
- PPT p.83：PCI、CABG、非侵入與 fibrinolysis 的選藥條件不同。
- PPT p.86：日本 PRASFIT 的 MACE 信賴區間跨 1，未證明優越。
- PPT p.88：Prasugrel 20／3.75 mg 為區域方案，不能與美國／ESC 劑量混用。（補充）
- PPT p.89：TRITON 的缺血下降伴隨 major bleeding 增加。
- PPT p.90：PLATO 的 total major 相近，non-CABG major bleeding 仍較多。
- PPT p.92：ISAR 比較包含不同 loading 時點的整體策略。

**原站修訂／危險邊界註記：**

- p.78：Asian: 8–23% poor metabolizer。 → 原頁缺乏可核對的地區／族群與來源。保留 clopidogrel 需活化及個體反應變異，不使用該比例推算個人無效或作族群通用選藥規則。（來源註記：來源比例未核｜推論範圍受限; https://academic.oup.com/eurheartj/article/44/38/3720/7243210）
- p.85：台灣仿單沒有 &gt;75 歲禁忌，因為 PRASFIT-ACS 沒有該排除條件。 → 試驗納入條件不能直接證明核准理由。原課程仿單截圖保留，本次未獨立取得現行 TFDA 全文；不得把該因果與高齡安全性當成已證實。（來源註記：地方核准標示待核; https://www.jstage.jst.go.jp/article/circj/78/7/78_CJ-13-1482/_article）
- p.87：Prasugrel 要用亞洲劑量。 → 20／3.75 mg 為日本 PRASFIT-ACS 與課程採用的區域策略；不能依「亞洲」身分生成通用劑量。（來源註記：已核對｜研究與地區範圍補回; https://www.jstage.jst.go.jp/article/circj/78/7/78_CJ-13-1482/_article）
- p.89：STEMI subgroup 不會增加出血風險。 → 子群未達顯著差異不等於無出血風險，也不取消已知禁忌與高出血限制。（來源註記：已核對｜統計解讀修正; https://www.nejm.org/doi/full/10.1056/NEJMoa0706482）
- p.90：Ticagrelor 降低 MACE，且不會增加 major bleeding。 → PLATO-defined total major bleeding 未顯著不同，但 non-CABG major bleeding 4.5% 對 3.8% 有增加。（來源註記：已核對｜出血終點修正; https://www.nejm.org/doi/full/10.1056/NEJMoa0904327）
- p.91：ISAR–REACT 5 用的劑量是 5 mg QD。 → 主要為 60 mg loading／10 mg daily；≥75 歲或 &lt;60 kg 才採 5 mg daily。（來源註記：已核對｜實質校正; https://www.nejm.org/doi/full/10.1056/NEJMoa1908973）
- p.91：Ticagrelor 7.2% 沒有 PCI／CABG，prasugrel 1.7%。 → 未能由原研究核成這個 revascularization 定義；不作確定事實。保留可核實的總體約 84% PCI、兩組 loading 時點不同、open-label 與非 PCI 外推限制。（來源註記：數據定義未核｜不據此下結論; https://www.nejm.org/doi/full/10.1056/NEJMoa1908973）
- p.92：三項主要試驗都概括為 CV death／MI／stroke。 → ISAR–REACT 5 的 primary composite 使用 death from any cause；與 TRITON／PLATO 的 cardiovascular death 有差異。（來源註記：已核對｜複合終點定義修正; https://www.nejm.org/doi/full/10.1056/NEJMoa1908973）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [AHA 2025 ACS｜官方重點摘要，第 1–2 點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)
- [TRITON–TIMI 38｜NEJM 2007 原研究](https://www.nejm.org/doi/full/10.1056/NEJMoa0706482)
- [PLATO｜NEJM 2009 原研究](https://www.nejm.org/doi/full/10.1056/NEJMoa0904327)
- [ISAR-REACT 5：兩種P2Y12給藥策略RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1908973)
- [PRASFIT–ACS｜Circ J 2014，日本隨機試驗](https://www.jstage.jst.go.jp/article/circj/78/7/78_CJ-13-1482/_article)
- [2025 AHA/ACC ACS §4.3.3與Table 9：IV P2Y12及轉換時點](https://www.ahajournals.org/doi/pdf/10.1161/CIR.0000000000001309)
- [CHAMPION PHOENIX：cangrelor與clopidogrel的PCI RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1300815)

**接續：**藥選對之後，還要決定是否在解剖未知前就開始承受藥效。

---

## 20｜P2Y12 時點：早期 NSTE-ACS 不常規先給

*選哪顆藥，與在解剖未知前給不給，是兩個決策。*

- 原站 ID：`pretreatment`；原課順序：19；核心主線；課程頁：93、94、95、96。

**起始問題：**已經懷疑ACS，為什麼還不立刻loading P2Y12？

**本節核心判斷：**NSTE-ACS、anatomy 未知、預計 &lt;24 h 造影，不常規 P2Y12 pretreatment。若需等 &gt;24 h，可衡量出血後考慮 clopidogrel 或 ticagrelor；不穩定者先改導管急迫性。

**原課承接：** Choice 段落已確定 potent P2Y12 的主要實證，並在 ISAR–REACT 5 看見兩組 loading 時點不同。 p.93 定義 pretreatment，p.94 看 ESC，p.95 對照美國建議，p.96 收成講者個人實務：STEMI 可 loading，NSTEMI 若要先給不選 prasugrel。原文由選藥轉到給藥時間，脈絡清楚但部分病理理由需要補正。

**下一步：** 確定什麼時候開始後，仍有「作用要維持多久、何時減少出血」的問題，所以 p.97 轉入 Duration。

### 先落下結論，再看它如何成立

未知 anatomy、預計早期造影的 NSTE-ACS，不常規先給 P2Y12。這段時間仍給適用的 aspirin、抗凝與監測，並安排侵入評估。等 anatomy 清楚、決定 PCI 再 loading，仍能完成 PCI 的血小板抑制。

理由連成三步：等待短，提前給藥能增加的保護有限；造影後可能轉向 CABG 或不需 PCI；出血與持續藥效卻已發生。下方 ACCOAST 用實際比較檢驗這個交換。等待超過 24 小時則增加另一段風險，需另判，不能直接沿用短等待的答案。

### Loading和pretreatment差在哪裡？

Loading是用較大的起始劑量，讓藥較快起效。Pretreatment問的是另一件事：冠狀動脈還沒照、解剖還不知道，要不要現在就先給P2Y12？

如果先等攝影，確認要做PCI時再loading，仍然有loading，只是沒有pretreatment。真正要比較的，是提早這幾個小時，能多減少多少缺血，又會多出多少出血。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### STEMI已經準備PCI，和解剖還不清楚的NSTE-ACS不同

STEMI已準備primary PCI時，下一步比較明確。2023 ESC認為可考慮P2Y12 pretreatment；若還沒給，就在PCI時loading。診斷有疑慮、出血或其他限制，仍要在給藥前處理。

NSTE-ACS裡，Type 1 NSTEMI也可能有急性血栓。先等P2Y12的理由，是很快就能知道血管、決定後續治療，而不是認為這群人沒有血栓。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### 在問先不先給以前，先看病人還能不能等

假設病人穩定，幾個小時內就能做導管，我們才會細談等待期間要不要先加P2Y12。若治療後仍反覆或持續缺血、開始不穩，或出現致命心律不整，先要改的是導管的急迫性。

多開一筆P2Y12，不能讓原本不安全的等待變安全。Aspirin、適用的抗凝、監測與緊急評估要繼續；P2Y12的藥物和時點，則跟著實際要走的治療安排。

- [ESC 2023 ACS：診斷與侵入策略](https://doi.org/10.1093/eurheartj/ehad191)
- [AHA 2025 ACS：官方重點第1–2點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)

### ACCOAST：先給的這幾個小時，換到了什麼？

4,033名troponin陽性、預計2–48小時造影的NSTE-ACS患者，一組現在先給，另一組等血管看清、決定做PCI才給：

<table><tr><th>比較的時點</th><th>解剖未知先給</th><th>等到決定PCI再給</th></tr><tr><td>造影之前</td><td>Prasugrel 30 mg</td><td>Placebo</td></tr><tr><td>確認做PCI</td><td>再補30 mg</td><td>給60 mg</td></tr><tr><td>7日缺血複合終點</td><td>10.0%</td><td>9.8%</td></tr><tr><td>7日TIMI major bleeding</td><td>2.6%</td><td>1.4%</td></tr></table>

兩組做PCI時都完成loading；提前給藥未見明顯缺血獲益，卻增加出血，major bleeding HR為1.90（95% CI 1.19–3.02）。

等待很短時，提早抑制能多保護的時間有限；但最後不需PCI或需要手術的人，也已承受了藥效。這是可能解釋，試驗沒有逐一證明原因。

結果限於此prasugrel方案，不能直接外推STEMI、其他P2Y12或更長等待。

- [Montalescot 2013 ACCOAST：原研究摘要](https://pubmed.ncbi.nlm.nih.gov/23991622/)
- [ESC 2023 ACS：診斷與侵入策略](https://doi.org/10.1093/eurheartj/ehad191)

### 如果導管改到兩天後，還是同一個問題嗎？

<table><tr><th>情境</th><th>2023 ESC</th><th>2025 AHA/ACC</th></tr><tr><td>NSTE-ACS，解剖未知，預計 <24 h 導管</td><td>不建議 routine P2Y12 pretreatment。</td><td>無證據支持常規提前給藥。</td></tr><tr><td>預計 >24 h 才能導管</td><td>可依出血風險考慮 pretreatment。</td><td>可考慮 upstream clopidogrel 或 ticagrelor（IIb B-NR）。</td></tr><tr><td>未先給藥，已決定 PCI</td><td>PCI 時給適當 loading。</td><td>按 PCI 用藥及既有療程處理。</td></tr></table>

等待超過24小時，提早給clopidogrel或ticagrelor可能多爭取一些等待期保護；clopidogrel還需要代謝活化，時間尤其要放進考量。但出血與CABG的顧慮也沒有消失，所以美國列的是IIb B-NR的「可考慮」。

這是在處理已經發生的延遲，不是叫我們為了先給藥而把導管往後排。高風險者要繼續找早期侵入或轉送的可能；病人若不穩，直接重排緊急處理。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [AHA 2025 ACS｜官方重點摘要，第 1–2 點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)

### 解剖確定後，銜接PCI或CABG

等攝影確認要做PCI，就處理PCI需要的loading；若改走CABG，就處理手術前後的抗血小板安排。先等這段資訊，是為了知道藥接下來要幫哪一種治療。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [2025 AHA/ACC ACS guideline：官方臨床投影片](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)
- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)

**推理邊界**

解剖未知、預計早期導管的 NSTE-ACS 不 routine P2Y12 pretreat；延遲導管者可依出血風險考慮。

ACCOAST回答的是prasugrel的給藥時間。STEMI、其他藥物與更長等待者，需要看各自的資料。

排程從幾小時變成兩天，就重想等待期給藥；一旦決定PCI或CABG，則按確定的治療接藥。病人惡化時，先改導管急迫性。

**臨床遷移｜造影後轉向 CABG：前一筆藥效仍在**

教學情境：原本穩定、兩小時後造影的 NSTE-ACS，造影後團隊改評估 CABG。

等待短時沒有常規先給 P2Y12，保留了造影後的安排空間。若先前已給，重新選擇手術路徑不會讓那段藥效消失。

帶入藥名、最後給藥時間與手術急迫性，衡量等待及出血；不能只依固定停藥天數延誤必要急救。

**反事實自問：**同一位穩定NSTE-ACS，原訂2小時導管改成兩天後；原本「先不loading」能否原封不動沿用？

較長等待期可能增加提早給藥的價值，應重評clopidogrel/ticagrelor的條件性建議；出血高、另用OAC或可能CABG時，顧慮仍在。ACCOAST並未證明這時提早給prasugrel較好。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.94：解剖未知且預計早期導管時，不 routine P2Y12 pretreatment。
- PPT p.95：美國 upstream 建議限於預計導管 &gt;24 h 的 NSTE-ACS。

**原站修訂／危險邊界註記：**

- p.93：NSTEMI 不一定是 thrombus 造成，antiplatelet 要謹慎。 → 區分「MI 病因多元」與「已推定 type 1 NSTE-ACS 的 pretreatment 時機」。後者不 routine 提前給的依據是策略試驗與出血權衡，不能由 NSTEMI 標籤推定沒有血栓。（來源註記：已核對｜病因與時機問題拆開; https://academic.oup.com/eurheartj/article/44/38/3720/7243210）
- p.95：美國指引，相對自由，視臨床決定 loading；頁腳卻引 2023 ESC。 → 圖表內容對應 2025 AHA/ACC：NSTE-ACS、預計侵入策略且 anticipated &gt;24 h，upstream clopidogrel 或 ticagrelor may be considered（IIb B-NR）。頁腳來源誤植。（來源註記：已核對｜來源與條件校正; https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009）
- p.96：NSTEMI 確定要做導管，可以考慮 clopidogrel 或 ticagrelor。 → 補回 &gt;24 h 延遲導管、出血風險與解剖未知條件；「確定要導管」本身不足以支持 routine pretreatment。（來源註記：已核對｜條件補回; https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [AHA 2025 ACS｜官方重點摘要，第 1–2 點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)
- [ACCOAST：prasugrel pretreatment RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1308075)
- [2025 AHA/ACC ACS guideline：官方臨床投影片](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)
- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [Montalescot 2013 ACCOAST：原研究摘要](https://pubmed.ncbi.nlm.nih.gov/23991622/)
- [ESC 2023 ACS：診斷與侵入策略](https://doi.org/10.1093/eurheartj/ehad191)
- [AHA 2025 ACS：官方重點第1–2點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)

**接續：**藥效已經開始後，下一個問題是哪些治療理由會持續多久。

---

## 21｜DAPT 療程：先辨認停哪顆、從何時開始

*研究在何時隨機分派，限制了能回答的臨床問題。*

- 原站 ID：`dapt-duration`；原課順序：20；核心主線；課程頁：97、98、99、100、101、102。

**起始問題：**滿一個月就能停aspirin，那PCI當天為什麼不直接停？

**本節核心判斷：**無高出血風險的 ACS，DAPT 預設至少 12 個月。縮短雙藥、停 aspirin 與 P2Y12 降階是不同策略，必須符合各自的族群、時點與藥物條件。

**原課承接：** Choice 與 Pretreatment 已回答用什麼、何時開始；PCI 完成不等於粥樣血栓風險與出血風險一起消失。 p.97 以 12 個月為預設，p.98 分拆 short DAPT 與 de-escalation，p.99 用研究比較不同單藥與族群，p.100–101 回到歐洲／美國策略，p.102 用舊指引回扣預設。本單元依這段原序閱讀，p.103–104 另處理 OAC 與課程總結，p.105–107 再處理一年以後。

**下一步：** 原 p.103 在 Duration 中加入新的條件：如果另有適應症須長期 OAC，原本兩條抗血小板的權衡會如何被第三種藥改寫？

### 十二個月是預設，風險仍會改變

ACS剛發生時，culprit lesion、新支架和全身斑塊帶來的血栓風險較高，之後通常逐漸下降。出血卻可能持續累積，還可能陸續出現貧血、腎功能變差、癌症或手術需求。

2023 ESC與2025 AHA/ACC因此保留一般ACS的12個月預設，同時讓符合條件的人調整。十二個月是研究建立的療程長度，不是到了第365天，血栓風險就突然歸零。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [AHA 2025 ACS｜官方重點摘要，第 1–2 點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)

### 減一種藥，和把藥換弱，改變的地方不同

Short DAPT是提早把兩種抗血小板減成一種。例如停aspirin、留ticagrelor，或者改留clopidogrel；留下哪個藥，也就是治療的一部分。

De-escalation通常還是DAPT，只是把prasugrel/ticagrelor換成clopidogrel，或按研究減量。此時改的是抑制強度，clopidogrel反應差異又會回到問題裡，所以有些guided strategy會用基因型或platelet function幫助選擇。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### 把研究時間畫對，才知道結果能用在哪裡

若研究只在首月無重大事件者分派，結論回答的是「這群人從一個月後如何調整」。PCI 當天就有出血、再缺血或未符合條件的人，並未被同樣比較。先看這條時間線，再讀兩組事件率，才能知道推薦的邊界。

### 研究是從PCI當天開始分組，還是先等一段時間？

TWILIGHT先用3個月DAPT，耐受、沒有重大事件，才隨機停不停aspirin。ULTIMATE-DAPT則在ACS/PCI首月沒有重大事件後比較。

STOPDAPT-2 ACS不一樣：出院前、中位PCI後第5天就隨機，之後照分組早減藥。若眼前病人首月剛發生支架血栓，就不能只因日期滿月，直接套用那些先無事件才分組的結果。

- [TWILIGHT：耐受3個月後停aspirin的RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1908419)
- [ULTIMATE-DAPT：無事件1個月後的ACS RCT](https://www.sciencedirect.com/science/article/pii/S0140673624004732)
- [STOPDAPT-2 ACS：隨機時點與限制](https://pmc.ncbi.nlm.nih.gov/articles/PMC8892373/)

### 兩邊都3.9%，就能說風險完全相同嗎？

TWILIGHT的death/MI/stroke：3.9%對3.9%。數字四捨五入後一樣，但絕對差的95% CI仍從−0.97到+0.84百分點，只是落在預設+1.6點的非劣界限內。

ULTIMATE的MACCE為3.6%對3.7%，差的CI是−1.4到+1.2點，界限是+2.5點。研究排除了較大的劣勢，較小的增減仍可能存在。

STOPDAPT-2 ACS，早改clopidogrel單藥，淨終點HR的CI上限1.62越過1.50界限，沒達到非劣。不能拿不同試驗硬湊成ticagrelor對clopidogrel的單藥頭對頭優越。

- [TWILIGHT：耐受3個月後停aspirin的RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1908419)
- [ULTIMATE-DAPT：無事件1個月後的ACS RCT](https://www.sciencedirect.com/science/article/pii/S0140673624004732)
- [STOPDAPT-2 ACS：clopidogrel單藥RCT全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC8892373/)

### Aspirin／clopidogrel單藥：族群與結果

<table><tr><th>研究</th><th>比較與結果</th><th>界限</th></tr><tr><td>REDUCE（2019）</td><td>1,496 位 ACS／COMBO stent，3 對 12 個月 DAPT，短程後 aspirin；淨終點達非劣。</td><td>特定支架與複合終點，不等於各缺血成分相同。</td></tr><tr><td>One–Month DAPT（2021）</td><td>1 個月 DAPT 後 aspirin，對比較長策略；淨終點達非劣。</td><td>穩定 CAD／UA、非複雜 PCI，兩組支架也不同。</td></tr><tr><td>SMART–CHOICE（2019）</td><td>3 個月後 P2Y12 單藥，多數 clopidogrel；心腦血管終點達非劣，出血較少。</td><td>混合 ACS／穩定患者及 P2Y12 藥物。</td></tr><tr><td>STOPDAPT–2（2019）</td><td>1 個月後 clopidogrel；複合缺血／出血終點達非劣。</td><td>日本、低事件率、混合 PCI 族群。</td></tr><tr><td>STOPDAPT–2 ACS（2022）</td><td>ACS／成功 PCI，1–2 個月後 clopidogrel 對比 12 個月 DAPT；未達淨終點非劣。</td><td>出血較少，但心血管事件數值較多。</td></tr></table><table><tr><th>研究</th><th>比較與結果</th><th>界限</th></tr><tr><td>GLOBAL LEADERS（2018）</td><td>1 個月後 ticagrelor 至 2 年；all-cause death／new Q-wave MI 未達優越。</td><td>混合穩定／ACS、open-label、跨兩年策略。</td></tr><tr><td>TWILIGHT（2019）</td><td>耐受 3 個月 DAPT 後，留 ticagrelor；出血較少，death／MI／stroke 未增加。</td><td>隨機前無重大事件，排除 STEMI。</td></tr><tr><td>TICO（2020）</td><td>ACS 含 STEMI，3 個月後單藥；1 年 NACE 3.9% 對 5.9%，主要由出血改善帶動。</td><td>韓國、特定 DES、open-label、低事件率。</td></tr><tr><td>ULTIMATE–DAPT（2024）</td><td>首月無重大事件後停 aspirin；BARC 2／3／5 出血 2.1% 對 4.6%，MACCE 達非劣。</td><td>已通過首月耐受與無事件條件，出血及 MACCE 為分開的共同主要終點。</td></tr></table>

若要縮短DAPT，2023 ESC讓無事件、非高缺血者在3–6個月轉單藥，偏好P2Y12；HBR可在1個月後考慮。2025 AHA/ACC則對已耐受ticagrelor-based DAPT的ACS/PCI，推薦≥1個月後轉ticagrelor單藥減少出血（I A）。

若要降階，ESC不建議ACS前30天常規改clopidogrel，之後可考慮；2025 AHA/ACC為PCI 1個月後可考慮（IIb B-R）。TALOS-AMI支持的是韓國AMI/PCI、首月無重大事件者。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [AHA 2025 ACS｜官方重點摘要，第 1–2 點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)
- [TALOS–AMI｜Lancet 2021 原研究](https://www.sciencedirect.com/science/article/pii/S0140673621014458)

### 同一個人，可以同時怕缺血、也怕出血

年齡、腎功能下降和貧血，可能把兩種風險一起推高。ARC-HBR以至少一個major或兩個minor criterion定義HBR；算完之後，還要回頭看病人現在發生什麼。

若新出血，減藥的理由變強；若是支架血栓，原本認為缺血風險低的想法就要改。首月事件、複雜支架、手術、OAC及耐受性，都要放回這次決定裡。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

**推理邊界**

12 個月是一般 ACS 的基準；選擇縮短或降階時，須保留用藥、時點與無事件條件。

非劣仍容許較小的缺血差異，並非完全相同。

新出血與支架血栓會改變缺血、出血的權衡，不能只按日期減藥。

**反事實自問：**ACS/PCI後第35天無事件、耐受ticagrelor，與第35天剛發生支架血栓，為何不能用同一張單藥醫囑？

第一位較接近首月無事件者的單藥證據，可討論ticagrelor單藥；第二位須查支架血栓原因、重評抗栓，不能只因滿月就減藥。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.98：Short DAPT 減少藥物數量，de-escalation 降低抑制強度。（補充）
- PPT p.99：單藥的藥名、ACS 比例與切換時點不同，結果不能直接互用。
- PPT p.100：ESC 的 short DAPT 與降階有不同時間條件。
- PPT p.101：美國 2025 對 ticagrelor 單藥、降階與 HBR 給予不同推薦強度。
- PPT p.102：較早指引已建立 ACS 12 個月基準，現行指引增加條件化的替代策略。

**原站修訂／危險邊界註記：**

- p.99：REDUCES-ACS，1460 ACS。 → 原研究名稱為 REDUCE，隨機分派 1,496 人；部分分析數與隨機總數不可混用。結論限 COMBO stent 與試驗複合終點。（來源註記：已核對｜研究名稱／母數修正; https://doi.org/10.4244/EIJ-D-19-00539）
- p.99：STOPDAPT-2 ACS，76% ACS。 → 該 ACS 分析是合併來源試驗的 4,169 位 ACS，需與 STOPDAPT-2 mixed cohort／總體合併族群比例分開，不能把 ACS-only 結論寫為 76%。（來源註記：已核對｜族群修正; https://jamanetwork.com/journals/jamacardiology/fullarticle/2789701）
- p.99：ULTIMATE DAPT（2025）：NACE superiority。 → 原研究發表於 2024；共同主要終點分別為 BARC 2／3／5 出血（superiority）與 MACCE（noninferiority），並保留 PCI 後首月無重大事件的條件。（來源註記：已核對｜年份／終點修正; https://www.sciencedirect.com/science/article/pii/S0140673624004732）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [AHA 2025 ACS｜官方重點摘要，第 1–2 點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)
- [REDUCE｜EuroIntervention 2019 原研究](https://doi.org/10.4244/EIJ-D-19-00539)
- [One–Month DAPT｜JACC Cardiovasc Interv 2021 原研究](https://www.jacc.org/doi/10.1016/j.jcin.2021.06.003)
- [SMART–CHOICE｜JAMA 2019 原研究](https://jamanetwork.com/journals/jama/fullarticle/2736564)
- [STOPDAPT–2｜JAMA 2019 原研究](https://jamanetwork.com/journals/jama/fullarticle/2736563)
- [STOPDAPT–2 ACS｜JAMA Cardiol 2022 原研究](https://jamanetwork.com/journals/jamacardiology/fullarticle/2789701)
- [GLOBAL LEADERS｜Lancet 2018 原研究](https://www.sciencedirect.com/science/article/pii/S0140673618318580)
- [TWILIGHT｜NEJM 2019 原研究](https://www.nejm.org/doi/full/10.1056/NEJMoa1908419)
- [TICO｜JAMA 2020 原研究](https://jamanetwork.com/journals/jama/fullarticle/2767161)
- [ULTIMATE–DAPT｜Lancet 2024 原研究](https://www.sciencedirect.com/science/article/pii/S0140673624004732)
- [TALOS–AMI｜Lancet 2021 原研究](https://www.sciencedirect.com/science/article/pii/S0140673621014458)
- [STOPDAPT-2 ACS：clopidogrel單藥RCT全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC8892373/)

**接續：**若患者另有 AF，還要保留另一個來源的抗凝需求。

---

## 22｜合併 OAC：分開 AF、防支架血栓與出血

*三個治療成分有不同的理由與結束時間。*

- 原站 ID：`oral-anticoagulation`；原課順序：21；核心主線；課程頁：103、104。

**起始問題：**AF患者做完PCI，三種抗栓藥要一起留多久？

**本節核心判斷：**AF 的抗凝需求不因 PCI 消失。合併抗栓時通常保留 OAC 加 clopidogrel，aspirin 採短期並依支架血栓與出血風險調整；美國與 ESC 的預設時程分開讀。

**原課承接：** Duration 主線已說明一般 ACS 的 12 個月預設與縮短／降階。 原 p.103 插入「另外有原因必須吃 anticoagulant」的特例，p.104 再用一週 triple→DOAC＋clopidogrel→單 DOAC 整理；本單元補解釋這個時間軸為何不同，並分開 ESC 與美國版本。

**下一步：** p.104 先回扣 Choice／Pretreatment／Duration，再在 p.105 把時間軸推至 12 個月以後；下一單元沿原序讀延長治療與風險表。

### AF與冠狀動脈的防栓目標不同

AF要預防的是心房血栓造成的栓塞；ACS與新支架，則有冠狀動脈的血小板血栓風險。前者需要適當OAC，後者早期需要抗血小板，所以兩邊要一起安排。

若只有一般PCI，沒有其他原因，不會自動接長期抗凝。Aspirin加rivaroxaban 2.5 mg twice daily是慢性血管保護方案；AF需要的足量抗凝，要按AF的適應症另外選。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### DAPT、DAT、TAT，差在留下哪幾個成分

DAPT是aspirin加P2Y12；DAT是OAC加一種抗血小板；TAT則是OAC、aspirin和P2Y12三種一起用。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### 指引中的aspirin停藥時間

2023 ESC預設最多約1週TAT，之後OAC加單一抗血小板，通常clopidogrel，接到12個月。多重HBR可在6個月停抗血小板；若缺血或操作風險高，可把TAT延到最多1個月。超過一年且穩定、仍需OAC時，通常改OAC單藥。

2025 AHA/ACC的建議是PCI後1–4週停aspirin，留下OAC加P2Y12，也偏好clopidogrel。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [AHA 2025 ACS｜官方重點摘要，第 1–2 點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)

### 這時為何常留clopidogrel，而不是potent P2Y12？

因為主要OAC合併試驗多用clopidogrel。加入ticagrelor或prasugrel，能多保護多少、又多出多少出血，資料比較少。2023 ESC因此不建議把兩藥放入TAT（III C）；DAT的相關證據也有限，通常仍偏好clopidogrel。

這個限制跟眼前的組合有關。病人有OAC適應症，不表示未來任何情況都絕對不能碰兩藥；

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)

### Aspirin的好處，會不會隨時間變少？

AUGUSTUS的4,614位AF合併近期ACS/PCI患者，都接受P2Y12，並隨機比較OAC方案。事後把時間拆開看：隨機後前30天，aspirin比placebo多0.97百分點嚴重出血，也少0.91點嚴重缺血。

再往後看到6個月，出血仍多1.25點，缺血差卻只剩−0.17點，CI跨零。

這讓高支架風險者短期多留aspirin有了討論空間。但出血與缺血的嚴重度不同，每個人的起始風險也不同，不能把兩個百分比相減，就當成他的淨獲益。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [AUGUSTUS：隨機後前30天與之後的事後分析](https://pubmed.ncbi.nlm.nih.gov/32223444/)

### 這三十天，是從PCI當天開始嗎？（延伸深讀）

不是。AUGUSTUS的隨機分組，距index事件中位已約6天。前30天是從那一刻起算，最早幾天的部分用藥已經發生。若問PCI當天完全不給aspirin安不安全，這段比較沒有把它完整包進來。

- [AUGUSTUS：隨機後前30天與之後的事後分析](https://pubmed.ncbi.nlm.nih.gov/32223444/)
- [AUGUSTUS：AF合併ACS/PCI，原始RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1817083)
- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [2025 AHA/ACC ACS guideline：官方臨床投影片](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)

### 機械瓣、沒做PCI，或新出血，都會改變接藥方式

AF若沒有機械瓣、中重度mitral stenosis等限制，ESC偏好DOAC；若有機械瓣，就不能直接照這條換成DOAC。ACS若沒有做PCI，少了新支架這個風險，也要用相應的療程。

若現在出血，就依嚴重度、發生時間和各藥用途重新安排；若首月出現支架血栓，則要重想aspirin是不是停得太早。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

### DAPT縮短、降階與OAC合併，各有時間條件（延伸深讀）

一般ACS預設12個月DAPT；要提早轉ticagrelor單藥，先看PCI、耐受與指定時點。

降階到clopidogrel，ESC是30天後可考慮，美國是PCI 1個月後（IIb B-R）；3–6個月則是部分short-DAPT轉單藥的時間。若另有OAC，現在要走的是合併抗凝的安排，不能把這幾張時間表混成一張。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

**推理邊界**

獨立 OAC 適應症加 ACS／PCI，通常採短 TAT→DAT→穩定期 OAC 單藥。

AUGUSTUS未完整比較PCI當天零aspirin。

早期複雜PCI或支架事件會讓人想多留幾天aspirin；後來穩定了，就重新看繼續三藥多出來的出血值不值得。

**反事實自問：**試驗顯示後期aspirin多出血，為何不能回推PCI當天就零aspirin？

隨機距事件中位已約6天，未完整比較最初幾天零aspirin；後期減藥的結果，不能直接回推PCI當天。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.103：縮短 TAT 可減少出血，potent P2Y12 的限制特指三重組合。
- PPT p.104：停 aspirin 與之後減少抗血小板，須依缺血、出血和 OAC 需要調整。

**原站修訂／危險邊界註記：**

- p.103：有其他原因須 anticoagulant 的病人不能吃 prasugrel 或 ticagrelor。 → 原 ESC 推薦的 Class III C 指不建議將它們納入 triple antithrombotic therapy；DAT 中證據亦有限且通常偏好 clopidogrel，但不能擴成所有 OAC 情境的絕對藥物禁忌。（來源註記：已核對｜組合範圍校正; https://academic.oup.com/eurheartj/article/44/38/3720/7243210）
- p.104：Triple 一週→clopidogrel＋DOAC 6–12 月→一年後 DOAC。 → 這是 ESC 預設策略的簡化。高支架／缺血風險可 TAT 至一個月，高出血可縮短 DAT；2025 AHA/ACC 的停 aspirin 窗為 PCI 後 1–4 週。DOAC 適用性及劑量減量規則另須成立。（來源註記：已核對｜指引版本與例外補回; https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know）
- p.104：降階 guideline 仍建議 3–6 個月再考慮（IIb）。 → 3–6 個月與特定 short-DAPT 轉單藥分支相關。2023 ESC 不建議首 30 天常規降階，之後可考慮；2025 AHA/ACC 為 PCI 後 1 個月後可考慮（IIb B-R）。兩種策略分開。（來源註記：已核對｜課程總結時程校正; https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)
- [AHA 2025 ACS｜官方重點摘要，第 1–2 點](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes/top-things-to-know)
- [AUGUSTUS：隨機後前30天與之後的事後分析](https://pubmed.ncbi.nlm.nih.gov/32223444/)
- [AUGUSTUS：AF合併ACS/PCI，原始RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1817083)
- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [2025 AHA/ACC ACS guideline：官方臨床投影片](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)

**接續：**接著回到介入：操作究竟恢復了哪一層血流，還留下什麼？

---

## 23｜PCI 的結果：管腔、微循環與功能分開看

*手術多做一步，必須帶來患者層次的獲益。*

- 原站 ID：`pci-procedure`；原課順序：23；核心主線；課程頁：108、109、110、111、112、113、114、115。

**起始問題：**看到大量血栓或多支狹窄，還要多做哪些處理？

**本節核心判斷：**PCI 恢復大血管通路，心肌灌流與收縮功能仍須另評估。休克時不常規立即做 non-culprit PCI；穩定後再安排完整血運重建。

**原課承接：** p.65–107 已討論藥物與抗血栓策略；p.108 明示由 Medication 轉入 Reperfusion。 p.109–110 先把 STEMI 放回再灌流流程，p.111–115 再以真實導管影像展開 CAG、wiring、stenting 與前後比較。以下操作關係是補足原圖未逐字說明的教學橋接；不能由靜態圖補造該次手術的完整紀錄。

**下一步：** 知道 PCI 如何恢復管腔，才有辦法理解為何計時到 wire/device，以及不同發作時間的獲益為何改變。

### 導絲跨過病灶，器材才進得去

CAG讓我們看到管腔與顯影劑往遠端走的情形。找到病灶後，先讓導絲跨過去，球囊與支架才有路徑前進；球囊擴開管腔，支架留下來支撐。

### 大血管已通，為何EF還沒恢復？

血從大血管回來，還要通過微循環才能到達組織。微血管阻塞、遠端栓塞與再灌流損傷，都可能使這一段走得不好；已壞死的心肌也無法靠開通立即恢復。

還有一種情況：心肌活著，收縮卻暫時受抑，稱stunned myocardium。因此EF的恢復可能晚於管腔改善。

- [2023 ESC ACS：microvascular obstruction、住院影像風險評估](https://academic.oup.com/ehjacc/article/13/1/55/7280662)

### 把「開通成功」拆成三個可觀察結果

<table><tr><th>層次</th><th>可能已經改善</th><th>仍要另外確認</th></tr><tr><td>大血管</td><td>管腔與心外膜血流恢復</td><td>殘餘狹窄、再閉塞、其他病灶。</td></tr><tr><td>組織灌流</td><td>血液有機會到達缺血區</td><td>微循環阻塞／no-reflow；管腔通暢不保證每一處組織都獲灌流。</td></tr><tr><td>心肌功能</td><td>可存活心肌可能逐步恢復</td><td>不可逆壞死、暫時性 stunning 與之後重塑；用症狀、echo 與追蹤分辨。</td></tr></table>

因此剛做完 PCI 的低 EF，不能單靠這一刻就決定永遠不會恢復；新的喘與低血壓，也不能只歸咎於尚未恢復，要立即排查再缺血與機械性併發症。

### 抽走血栓，換來的結果是什麼？

血栓很多，直覺會想先抽掉，減少遠端栓塞。TOTAL就比較primary PCI加常規手動抽吸，與PCI單獨處理：180天CV death/再MI/shock/NYHA IV HF為6.9%對7.0%，HR0.99；30天中風則為0.7%對0.3%。

局部血栓少了，或ST看起來改善，還要把操作帶來的傷害一起算進來。這個結果讓常規抽吸失去理由；若是大量殘餘血栓需要bailout，問的則是當下能否把PCI完成，TOTAL沒有比較每一種救援情境。

- [TOTAL：常規血栓抽吸RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1415098)
- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)

### 其他血管也窄，休克時要一起做嗎？

先看病人現在撐不撐得住。CULPRIT-SHOCK在MI合併休克中，比較先做culprit與立即多血管PCI；30天死亡或需RRT為45.9%對55.4%，RR0.83。多做一段，可能增加操作、顯影與生理負荷；試驗確認了兩種做法的結果，沒有逐一證明是哪項負荷造成差異。

穩定下來後，問題變成剩下的病灶會帶來多少長期風險。COMPLETE在culprit已成功處理的穩定STEMI，完整再血管化使中位3年CV death/MI由10.5%降至7.8%，HR0.74。

- [CULPRIT-SHOCK：休克的culprit-only與立即多血管PCI](https://www.nejm.org/doi/full/10.1056/NEJMoa1710261)
- [COMPLETE：穩定STEMI的完整再血管化RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1907775)

### 回到同一條血管看前後變化

先找到同一條主幹與分支，確認投影，再比截斷、管腔與遠端充盈。顯影較亮，只告訴我們這次影像的樣子；要判斷微循環，還需要其他資料。若胸痛、ST或循環沒有改善，就沿著殘餘缺血、灌流與併發症重新找原因。

**推理邊界**

管腔開通、組織灌流與心肌功能，恢復可以不同步。

TOTAL研究常規抽吸，CULPRIT-SHOCK研究休克當下做多少，COMPLETE研究穩定STEMI剩餘病灶的處理；使用結果前，先確認患者是哪種情況。

循環穩定後，重新評估其餘病灶的長期風險；若又缺血或不穩，先找culprit、併發症與灌流問題。

**臨床遷移｜造影已通，cTn 仍高、EF 仍低**

教學情境：PCI 後通路已恢復，cTn 還高，早期 echo 的 EF 仍低。

前面用 cTn 確認傷害，現在仍不能用它單獨推論此刻的冠狀血流。EF 低也可能同時含有壞死與暫時性 stunning，需要結合灌流與後續恢復。

按症狀、ECG、造影及 echo 分別評估通路、灌流與功能；若新低血壓或肺水腫，立即找再缺血及結構併發症。

**反事實自問：**多支CAD患者從shock穩定下來，接著如何看其他血管？

休克時先處理culprit，是為了完成當下最重要的介入，減少額外負荷。穩定後再看解剖、缺血與可行性，評估其餘病灶是否值得完成重建；CULPRIT-SHOCK沒有要求之後永遠只留一條血管做過PCI。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.111：CAG顯示哪裡狹窄，以及顯影劑能否走到遠端。
- PPT p.112：導絲先跨過病灶，球囊與支架才有路徑前進。
- PPT p.113：連續影像讓我們追器材與遠端充盈的變化，但沒有列出完整操作過程。
- PPT p.114：支架留下來支撐管腔，後續用抗血小板降低支架血栓風險。
- PPT p.115：管腔改善之後，接著看心肌灌流與功能有沒有跟上。

**原站修訂／危險邊界註記：**

- p.110：In Taiwan：院外 90 分、院內 60 分 → 保留為講者標示的台灣流程目標；本次未核對醫院、品質指標版本及「院內」定義，不作全台統一規範。（來源註記：地方實務待核; https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes）
- p.113：無操作文字的連續影像 → 僅讀實際可見影像；不由課程位置擅自補成完整球囊操作紀錄。（來源註記：已核對原圖; https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [原課程 p.108–115：CAG、wiring、stenting、PCI 前後圖](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)
- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [已下載核對：2025美國ACS官方Clinical Slides 18](https://professional.heart.org/-/media/PHD-Files-2/Science-News/Clinical-Slide-Series/2025-Acute-Coronary-Syndromes-Guideline-Clinical-Slides.pptx?sc_lang=en)
- [TOTAL：常規血栓抽吸RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1415098)
- [CULPRIT-SHOCK：休克的culprit-only與立即多血管PCI](https://www.nejm.org/doi/full/10.1056/NEJMoa1710261)
- [COMPLETE：穩定STEMI的完整再血管化RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa1907775)

**接續：**若功能尚未恢復，必須再問心肌是否仍可挽救，以及何時開通有益。

---

## 24｜再灌流時機：時間窗必須連著病況讀

*可挽救心肌、當下危險與試驗族群共同決定效益。*

- 原站 ID：`reperfusion-timing`；原課順序：24；核心主線；課程頁：116、117。

**起始問題：**血管仍然閉塞，為何晚期不一律開通？

**本節核心判斷：**早期 STEMI 儘速再灌流。晚到但仍缺血、休克或電氣不穩者仍須緊急評估；穩定晚期閉塞的例行開通，則要依指引時間窗與 OAT 族群判斷。

**原課承接：** p.111–115 已展示 PCI 恢復管腔的操作。 p.116 並列 ESC 2023 與美國 2025 的完整推薦，p.117 壓縮成 takeaways。這裡必須先讀完整表格，再檢查口訣省略了什麼。

**下一步：** STEMI 的再灌流後，課程返回 NSTE-ACS 的侵入策略；兩者都評估急迫性，卻不能共用同一條時間口訣。

### 症狀時間與醫療系統時間

症狀開始到治療，幫助估計心肌缺血多久，但間歇症狀、回憶與側枝循環都會讓這個估計有誤差。

醫療流程還有另一組時間：FMC、ECG診斷、到院、wire crossing與device activation，各有起點和終點。Door-to-wire 90分鐘算的是到院後的流程；若轉院已耽擱很久，院內達標也沒有把前面的延誤補回來。

### 早期開通是在保住尚未壞死的心肌

阻塞持續越久，可挽救心肌通常越少，所以早期要把延誤壓低。美國2025對症狀<12小時的STEMI推薦PPCI，FMC-to-device目標≤90分鐘，需轉院時≤120分鐘。

ESC2023對≤12小時且有相應缺血表現者推薦再灌流，以診斷至wire能否在120分鐘內完成來選擇做法。

- [2025 美國 ACS：原課程 p.116 引用表與官方指南入口](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)
- [2023 ESC ACS §5.2–5.3](https://academic.oup.com/ehjacc/article/13/1/55/7280662)

### 晚到又不穩，先處理眼前危險

美國對ACS合併shock或血流動力不穩，推薦不論發作時間緊急處理culprit血管。

ESC對>12小時STEMI，若仍有缺血症狀、血流動力不穩或致命心律不整，推薦PCI；美國對>24小時且持續缺血或致命心律不整列IIa。

### 穩定晚到，才進入這組時間比較

美國對12–24小時STEMI的PPCI列IIa；ESC對12–48小時例行PPCI列IIa。到了24–48小時，兩套指南確實有不同判斷。

美國Class III No Benefit的條件是穩定、IRA完全閉塞、>24小時，且沒有持續缺血、急性嚴重HF或致命心律不整；ESC針對>48小時、無持續症狀者的例行occluded-IRA開通。

### OAT：血管開了，長期結果卻沒有更好

如果晚期開通能改善灌流與重塑，應該能在後續事件看見好處。OAT納入2,166位MI後3–28天、IRA仍閉塞的穩定患者；PCI對藥物的四年死亡/再梗塞/NYHA IV HF為17.2%對15.6%，HR1.16，沒有證明例行PCI獲益。

持續缺血、休克或其他高危者，不屬於這項穩定晚期比較的人群。

- [Occluded Artery Trial 原研究](https://www.nejm.org/doi/10.1056/NEJMoa066139)
- [OAT：穩定晚期閉塞的PCI RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa066139)

### 還有viability，為何仍不能只看這項檢查？

看到viability，知道至少還有存活組織，會想把血流再送回去。OAT-NUC的124人中，70%仍有中度以上保留的viability；但viability高低，沒有讓PCI對重塑的效果出現交互作用。

人數少，也未比較每種現代影像選人的做法。因此還缺少用viability選人後，晚期PCI能改善哪些臨床事件的直接答案。

- [OAT-NUC：viability與重塑子研究](https://pubmed.ncbi.nlm.nih.gov/21392619/)

### 本來無痛，又開始胸痛了

若穩定無痛的患者，又反覆胸痛並出現動態ST變化，現在已有新的缺血要評估。發作已晚、操作風險也還在，但這時問的是如何處理正在發生的缺血，不能讓晚期Class III成為延後的理由。

**推理邊界**

穩定、無持續缺血的晚期閉塞，沒有例行開通的普遍獲益。

OAT研究的是穩定晚期閉塞；持續缺血或shock要另看緊急處理。OAT-NUC人數少，也未逐一測試所有viability亞群。

反覆胸痛伴動態ST變化，使患者轉入持續缺血的評估；只有viability陽性時，則尚不足以決定例行PCI。

**反事實自問：**MI第5天、IRA閉塞，患者穩定無缺血但有viability，這項檢查足以決定例行PCI嗎？

還不足。Viability告訴我們有存活組織，OAT與小型子研究卻沒有證明單靠這一點開通會減少事件。若接著出現持續缺血或不穩，就改問如何處理當下危險，處理時機也會跟著變。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.116：先找持續缺血與循環不穩，再讀晚期Class III所需的完整條件。
- PPT p.117：24／48小時口訣省略了患者狀態，使用時要連回完整表格。

**原站修訂／危險邊界註記：**

- p.117：症狀開始 &gt;24 hr → III（AHA）；&gt;48 hr → III（ESC） → 此口訣缺穩定、IRA 閉塞與無持續危險等關鍵限定。完整推薦見 p.116；不可直接寫成互動的單一時間分支。（來源註記：已核對原課程完整推薦表及 ESC 全文; https://academic.oup.com/ehjacc/article/13/1/55/7280662）
- p.116：症狀時間很重要 → 症狀起點、FMC、ECG 診斷、door、wire/device 各為不同計時量；保留各指南定義。（來源註記：已核對原表; https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2025 美國 ACS：原課程 p.116 引用表與官方指南入口](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)
- [2023 ESC ACS §5.2–5.3](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [Occluded Artery Trial 原研究](https://www.nejm.org/doi/10.1056/NEJMoa066139)
- [已下載核對：2025美國ACS官方Clinical Slides 18](https://professional.heart.org/-/media/PHD-Files-2/Science-News/Clinical-Slide-Series/2025-Acute-Coronary-Syndromes-Guideline-Clinical-Slides.pptx?sc_lang=en)
- [OAT：穩定晚期閉塞的PCI RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa066139)
- [OAT-NUC：viability與重塑子研究](https://pubmed.ncbi.nlm.nih.gov/21392619/)

**接續：**NSTE-ACS 用相同的急迫性原則，再依穩定後的風險安排時程。

---

## 25｜NSTE-ACS：先處理不穩，再用分數排時機

*「現在就要做」與「較早做有多少獲益」分開。*

- 原站 ID：`nste-risk`；原課順序：25；核心主線；課程頁：118、119、120、121、122、123、124。

**起始問題：**高風險分數，如何影響導管時機？

**本節核心判斷：**難治性缺血、休克、危及生命的心律不整或缺血相關急性 HF，需要即刻侵入評估。穩定後再用風險分層安排時機，GRACE 不能覆蓋眼前惡化。

**原課承接：** p.116–117 已分清 STEMI 再灌流與晚到例外。 p.118 回到美國總流程，p.119–121 分開 immediate、early 與住院／選擇性策略，p.122–124 才補 GRACE 與 TIMI。這個安排是先提出行動問題，再提供預後分層工具。

**下一步：** 決定侵入策略後，仍須處理及時 PCI 不可達成時的 STEMI 再灌流替代方案：fibrinolysis。

### ST沒有持續抬高，診斷還要接著分

無持續ST elevation的胸痛，可能是NSTE-ACS，也可能是非缺血性心肌損傷或其他病因。要診斷NSTEMI，需同時看到急性心肌損傷與缺血證據；有缺血而未達MI損傷條件，則可能是UA。

另一方面，沒有明顯ST elevation的患者，也可能有閉塞或危險缺血，所以分診後還要繼續看症狀與變化。

### 血壓正常，也可能現在就要導管

患者治療後仍反覆胸痛，或開始肺水腫，就要想到缺血還在傷害心肌。ESC的immediate是儘速處理，包含shock／血流動力不穩、治療後仍反覆胸痛、缺血相關急性HF、致命心律不整、機械性併發症或反覆動態ECG等。

美國2025以<2小時表達，亦列難治angina、新惡化MR／肺水腫與電氣不穩。這些訊號有時早於低血壓，不能只等血壓掉下來。

- [2023 ESC ACS §5.2.2–5.2.4](https://academic.oup.com/ehjacc/article/13/1/55/7280662)

### TIMACS為何特別看GRACE&gt;140？

TIMACS比較NSTE-ACS在<24小時或≥36小時導管；六個月death/MI/stroke為9.6%對11.3%，HR0.85（95% CI 0.68–1.06），整體未達顯著。預先指定GRACE>140子群則為13.9%對21.0%，HR0.65。

因此較早做的好處，在高風險患者更值得注意；但140上下的生理狀態不會突然跳變，子群結果也有不確定性。

- [TIMACS：早期與延後導管RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa0807986)
- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [2025 AHA/ACC ACS guideline：官方臨床投影片](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)

### GRACE把哪些危險加在一起？

年齡、心率、血壓、creatinine、Killip class、心搏停止、ST deviation與biomarkers，整合患者儲備、循環失代償與心肌損傷。

GRACE 2.0可估不同時間與終點；<109／109–140／>140常見於住院風險分層。估六個月死亡時要使用相應模型，才能正確解讀分數。

- [GRACE 2.0 開發與外部驗證原研究](https://bmjopen.bmj.com/content/4/2/e004425)
- [不同 GRACE 版本對導管時機的影響](https://pubmed.ncbi.nlm.nih.gov/37421436/)

### TIMI先估接下來會出多少事件（延伸深讀）

UA/NSTEMI七項各一分，預測14天death/MI/需urgent revascularization的嚴重再缺血。它把年齡、已知CAD、近期症狀、ECG與標記等加總，算的是這組事件，並非單看死亡，也與TIMI STEMI score不同。

- [TIMI UA/NSTEMI 原研究：Antman et al., JAMA 2000](https://pubmed.ncbi.nlm.nih.gov/10938172/)

### 為何aspirin反而加一分？（延伸深讀）

先前用aspirin的人，可能本來就有CAD、基礎風險也較高。TIMI記錄的是這群患者後來發生多少事件，不是用藥與不用藥的隨機比較。若為了少這一分就停aspirin，改變的是治療，沒有研究證明這樣會讓事件變少。

### 分數低，病況卻正在變壞

難治胸痛、shock或sustained VT/VF出現時，患者已經有需要處理的危險；等分數重新算高，只會拖延評估。反過來，分數高告訴我們風險較高，接著仍要靠診斷、解剖與可行性，決定哪個病灶怎麼處理。

**推理邊界**

難治缺血與循環不穩決定立即處理；預後分層用於安排穩定患者。

TIMACS的整體與子群結果，均不授權讓不穩定患者等候。

新shock、難治胸痛、急性缺血相關HF或電氣不穩出現，就升級處理，不用等分數跨140。

**反事實自問：**GRACE 138卻難治胸痛，另一位GRACE 145但已穩定，為何可能先處理前者？

前者正在缺血，等待可能繼續傷害心肌；後者雖有較高預後風險，當下卻已穩定。140幫助研究與分流，眼前症狀和循環才決定此刻能不能等。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.119：Immediate、early與selective，先按眼前危險分流，再安排時間。
- PPT p.120：Very-high-risk與high-risk要連同症狀、ECG及循環狀態判斷。（補充）
- PPT p.121：難治angina、急性HF或電氣不穩，都可能要求立即處理。
- PPT p.122：先看GRACE或TIMI在估哪群患者的哪個結局。（補充）
- PPT p.123：計算六個月風險前，先確認GRACE使用的模型與分數層級。（補充）
- PPT p.124：Aspirin這一分記錄預後風險，沒有證明停藥能減少事件。（補充）

**原站修訂／危險邊界註記：**

- p.120：若沒有上述 STEMI／高風險 ECG，則落入 NSTEMI → 應先進入 NSTE-ACS／其他病因的評估；NSTEMI 必須另滿足急性損傷與缺血證據。（來源註記：已核對診斷層次; https://academic.oup.com/ehjacc/article/13/1/55/7280662）
- p.121：Unstable 才要2小時內做 → 圖中 refractory angina、急性HF／惡化MR、電氣不穩均屬急迫條件；不能只用低血壓解讀 unstable。（來源註記：已核對原圖; https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes）
- p.123：GRACE 2.0：6-month mortality；&lt;109、109–140、&gt;140 → 不同 GRACE 模型有不同終點／時間；常見分層與 6 個月死亡標題不能無條件拼接。網站不實作混合版計算器。（來源註記：已核對原研究／模型差異; https://bmjopen.bmj.com/content/4/2/e004425）
- p.124：TIMI 0–2 低風險 → 課程預後分層保留，但美國導管圖的 lower-risk TIMI &lt;2 是特定流程條件；不是同一個切點。（來源註記：已核對 p.121 與 p.124; https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2023 ESC ACS guideline](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [2025 AHA/ACC ACS guideline：官方臨床投影片](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)
- [GRACE 2.0 開發與外部驗證原研究](https://bmjopen.bmj.com/content/4/2/e004425)
- [TIMI UA/NSTEMI 原研究：Antman et al., JAMA 2000](https://pubmed.ncbi.nlm.nih.gov/10938172/)
- [已下載核對：2025美國ACS官方Clinical Slides 21](https://professional.heart.org/-/media/PHD-Files-2/Science-News/Clinical-Slide-Series/2025-Acute-Coronary-Syndromes-Guideline-Clinical-Slides.pptx?sc_lang=en)
- [TIMACS：早期與延後導管RCT](https://www.nejm.org/doi/full/10.1056/NEJMoa0807986)
- [不同 GRACE 版本對導管時機的影響](https://pubmed.ncbi.nlm.nih.gov/37421436/)

**接續：**若 STEMI 的 PCI 無法及時做到，就要接續另一條恢復血流路徑。

---

## 26｜溶栓後仍轉 PCI：再通不等於病灶已處理

*把成功、失敗與殘餘病灶接回同一條策略。*

- 原站 ID：`fibrinolysis`；原課順序：26；核心主線；課程頁：125、126、127、128。

**起始問題：**溶栓看起來成功，接著為何還要導管？

**本節核心判斷：**STEMI 無法及時 PCI 且符合溶栓條件時，可先溶栓並立即安排轉送。失敗或再不穩走 rescue PCI；穩定成功者通常 2–24 h 造影。

**原課承接：** 課程已展示 primary PCI 及 NSTE-ACS 的侵入時機。 p.125–126 比較及時 PCI 與 fibrinolysis，p.127 補 fibrinolytic／抗血栓共同治療，p.128 最後用禁忌檢查收益的可接受性。

**下一步：** 再灌流完成後仍有心肌損傷與併發症；因此 p.129 轉入 Post-MI care。

### 等PCI太久，能不能先讓血流回來？

先確認是STEMI、症狀<12小時、沒有溶栓禁忌。若ESC2023所用的診斷至wire無法於120分鐘內完成，就推薦溶栓；美國則用FMC至device估計延遲。

選擇溶栓，是希望少掉等待中的缺血時間，因此一旦決定，ESC目標是診斷至bolus<10分鐘。120分鐘用來比較預期PCI延遲，不是決定後再等那麼久。

### 血栓溶掉後，斑塊還留著

Fibrin分解後，血流可能比等轉院PCI更早恢復，但也增加全身及顱內出血。斑塊與殘餘狹窄仍可能使血管再次閉塞。

所以給藥後就轉PCI中心，依反應決定救援或早期導管。先用藥恢復灌流，再接介入評估，稱pharmaco-invasive strategy。

### ST與症狀決定救援或早期造影

給藥後追ECG：ESC把60–90分鐘ST回落<50%列為失敗訊號之一。若持續胸痛、缺血惡化，或血流動力／電氣不穩，也要考慮rescue PCI。

若ST回落、胸痛改善，表示治療可能已讓血流恢復，接著仍於給藥後2–24小時造影，查看殘餘病灶與通暢情形。

- [2023 ESC ACS §5.3.1.2：pharmaco-invasive strategy](https://academic.oup.com/ehjacc/article/13/1/55/7280662)

### 不同藥物，給法為何要逐一看？（延伸深讀）

ESC2023 Table S10列alteplase：先15mg IV bolus，接0.75mg/kg、30分鐘（最多50mg），再0.5mg/kg、60分鐘（最多35mg）；reteplase分兩次10units、相隔30分鐘；streptokinase為150萬units、30–60分鐘。

Tenecteplase是依體重30–50mg單次bolus，高齡另有減量。投影片左右表對75歲邊界寫法不一致，真正給藥前要先確認採用規範的年齡條件，才知道要給哪個量。

### 溶掉現有血栓，也要減少再形成

Fibrin被分解後，血小板與凝血反應還可能繼續，因此合併aspirin、clopidogrel與抗凝。表列aspirin loading150–300mg、維持75–100mg/day；clopidogrel一般loading300mg、維持75mg/day，高齡給法不同。

抗凝持續到再血管化，未做者住院最長8天。Enoxaparin按年齡／腎功能調整，UFH按體重及凝血監測；表中的fondaparinux限streptokinase做法。

### 能不能溶栓，先問哪裡可能出血

既往顱內出血、顱內結構病變、活動性出血，以及疑似／確定主動脈剝離，會使溶栓的代價變大。還要問手術、外傷、不可壓迫穿刺、抗凝、嚴重高血壓與懷孕，連同時間及分類判斷。

缺血性中風的窗口，ESC列前6個月，美國列前3個月並有特定註腳，兩套要分開讀。有禁忌時，接下來改評估PCI；即使轉院會延遲，也不能因此略過出血風險。

### 有禁忌時，把再灌流路徑接下去

診斷還不確定、超出時窗或有重大禁忌，就重新安排緊急轉送與導管評估。尤其有主動脈剝離線索時，即使ECG像缺血，也要先釐清病因，因為抗血栓與溶栓可能使另一個出血問題更嚴重。

**推理邊界**

穩定成功者早期造影；失敗或再不穩者緊急救援。

這條路徑用在符合條件的STEMI，不是所有NSTEMI；ST改善後，殘餘病灶與再閉塞風險還需要處理。

問出近期中風、手術或剝離線索，就重新決定能否溶栓，同時接著安排其他再灌流評估。

**反事實自問：**溶栓後ST回落60%，後來又胸痛、ST回升，接著怎麼想？

改善可能只是短暫的，復發缺血需要緊急評估rescue PCI。若持續穩定，則按成功溶栓路徑於2–24小時造影。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.125：先看STEMI診斷、症狀時間、預期PCI延遲與溶栓禁忌。
- PPT p.126：給藥後立即轉送，失敗時救援，成功者在2–24小時造影。
- PPT p.127：把年齡、體重與腎功能放進藥物表，再讀對應劑量。
- PPT p.128：中風距今多久會影響溶栓，先確認採用美國或ESC的時間窗與註腳。

**原站修訂／危險邊界註記：**

- p.127：Table S10：fibrinolytics及共同抗血栓療程 → 保留為ESC2023來源表；年齡／體重／腎功能及當地藥品規範須另核，不將表格轉成自動處方。原頁75歲邊界有&gt;與≥寫法差異。（來源註記：已核對原圖；當地標示未核; https://academic.oup.com/ehjacc/article/13/1/55/7280662）
- p.128：Ischemic stroke：ESC6個月、美國3個月 → 版本與例外須分開；不得合併成無來源的單一時間窗。（來源註記：已核對原圖; https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2023 ESC ACS §5.3.1.2：pharmaco-invasive strategy](https://academic.oup.com/ehjacc/article/13/1/55/7280662)
- [2025 美國 ACS：非PCI中心再灌流與溶栓後導管；原課程 p.125](https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes)
- [已下載核對：2025美國ACS官方Clinical Slides 19–20](https://professional.heart.org/-/media/PHD-Files-2/Science-News/Clinical-Slide-Series/2025-Acute-Coronary-Syndromes-Guideline-Clinical-Slides.pptx?sc_lang=en)

**接續：**進入梗塞後：血管處理完成，心肌結構與功能還可能出問題。

---

## 27｜一年後延長抗栓：重新估計剩餘獲益

*急性期理由改變後，重新做長期交換。*

- 原站 ID：`dapt-extended`；原課順序：22；延伸閱讀；課程頁：105、106、107。

**起始問題：**過了一年，還需要第二種抗栓藥嗎？

**本節核心判斷：**缺血風險仍高、出血風險可接受，才考慮延長第二種抗栓。延長 DAPT 與加入血管劑量 rivaroxaban，證據與適用人群不同。

**原課承接：** p.97–104 已完成首年 DAPT、縮短／降階與 OAC 特例，並在 p.104 總結。 p.105 明示 beyond the first 12 months，先畫一般路徑與延長選項；p.106 把候選藥物、劑量及 NNT／NNH 列出；p.107 才補上誰屬高／中度血栓風險。這段保持原來「先見選項，再讀適用風險」的順序。

**下一步：** 完成藥物這一大段後，原課程在 p.108–109 回到 Medication／Reperfusion 雙主軸，轉向再灌流時機。

### 斑塊還在，為何不直接永久用兩種？

一年後，近期ACS與新支架帶來的風險通常下降，但其他冠脈斑塊、其他血管床的疾病，以及出血，仍然要照顧。留下第二種藥，還要看它能多減少多少事件。

一般預設是aspirin單藥；prolonged DAPT、第二種抗栓或P2Y12單藥，按條件選。若病人另有長期OAC需求，就回到上一節的合併治療安排。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)

### 延長DAPT，和加低劑量rivaroxaban，動到的地方不同

Aspirin加clopidogrel/prasugrel/ticagrelor，繼續壓低兩條血小板訊號；aspirin加rivaroxaban 2.5 mg twice daily，則多抑制凝血factor Xa，叫dual-pathway inhibition。

這些方案分別來自已耐受一年DAPT的PCI患者、既往MI或穩定CAD/PAD。Rivaroxaban這個劑量不是AF足量抗凝；已用足量OAC的人，也不能因此再任意加aspirin。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)

### NNT與NNH取決於族群、終點與時間（延伸深讀）

NNT是特定期間內，絕對事件減少量的倒數；NNH則看某種傷害增加多少。同一個藥用在不同起始風險、不同對照或不同追蹤時間，數字都可能變。

NNT 63和NNH 84不能直接相減：兩者的終點嚴重度、追蹤時間與族群未必相同。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)

### 哪些資料會讓我們想多留一種藥？

增加血栓的臨床因素包括：需用藥的糖尿病、recurrent MI、多血管CAD、提早或快速進展CAD、polyvascular disease、CKD及部分全身發炎疾病。Complex CAD加至少一個增強因子，會讓延長治療更值得評估。

操作資料也重要，例如≥3支架、≥3病灶、總支架長度>60 mm、left main、兩支架bifurcation、CTO，或治療中仍發生支架血栓。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)

### CKD讓人想加藥，也可能讓人不敢加

CKD增加缺血，也會改變藥物清除與血小板功能，出血可能一起增加。因此還要看ARC-HBR、貧血、近期出血與年齡，才知道加一種藥是否划算。

若新發消化道出血，原本能耐受的療程可能已經撐不住；若反覆MI或支架血栓，則要重想缺血保護是否不足。危險因子控制與其他次級預防則持續做。

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

**推理邊界**

延長第二種抗栓，需高殘餘缺血、可接受出血與適合的方案。

延長DAPT與dual-pathway inhibition來自不同族群；rivaroxaban 2.5 mg twice daily也不是AF足量抗凝。

新出血會減少延長的吸引力，反覆MI或支架血栓則增加再保護的需求。

**反事實自問：**PCI 一年無事件，但 CKD 且近期消化道出血，為何不能只因 CKD 延長 DAPT？

CKD讓缺血與出血都更令人擔心，而這位患者最近已經消化道出血。先把這次出血的原因與後續耐受看清楚，再衡量多留第二種藥能少多少缺血、會多多少出血。

**原圖定位（僅保留記錄、未複製圖像）：**

- PPT p.105：超過一年，延長第二種抗栓需重新權衡缺血與出血。
- PPT p.106：藥物選項來自不同族群與研究期間，NNT／NNH 不能直接排名。
- PPT p.107：複雜 CAD 與臨床／技術因子提高血栓風險，仍需評估出血。

**原站修訂／危險邊界註記：**

- p.106：各延長抗栓研究列有 NNT／NNH。 → 不同族群、終點、觀察時間不能直接橫向排名。低劑量 rivaroxaban＋aspirin 是血管保護方案，不能替代 AF 的足量抗凝。（來源註記：已核對｜比較與適應症界限; https://academic.oup.com/eurheartj/article/44/38/3720/7243210）

**原站列出的來源（未重新逐頁獨立核讀）：**

- [2023 ESC ACS guideline｜§4.2、§6；原文與圖表](https://academic.oup.com/eurheartj/article/44/38/3720/7243210)
- [2025 ACC/AHA ACS guideline｜§4.3–4.4、DAPT 與長期抗凝段落](https://www.jacc.org/doi/10.1016/j.jacc.2024.11.009)

**接續：**同樣的長期決策也會出現在降脂與心室功能治療。

---

