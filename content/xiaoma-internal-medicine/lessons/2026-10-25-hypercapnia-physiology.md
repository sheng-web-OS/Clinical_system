# RR 已經 40/min，為什麼 PaCO₂ 仍然上升？

<div class="opening-question"><span class="small-label">Respiratory Failure｜深入三問之二</span><p>一個病人從每分鐘呼吸 24 次變成 40 次，PaCO₂ 卻從 39.9 上升至 54.9 mmHg。是病人沒有增加呼吸驅動、橫膈無法提供潮氣量，還是更多呼吸被浪費在 dead space？在 PaCO₂ 尚未升高以前，怎麼知道呼吸泵已接近極限？</p></div>

先從一位**真實患者**開始。Kim 等人在 2010 年報告一名 **68 歲女性**，初次以呼吸困難就診，沒有典型複視、吞嚥困難或四肢肌力異常。第一天在室內空氣下 RR **24/min**、pH **7.441**、PaCO₂ **39.9**、PaO₂ **64.7**；第六天病況加重，RR **40/min**，意識混亂，在 **10 L/min 氧氣面罩**下 pH **7.324**、PaCO₂ **54.9**、PaO₂ **94.4**。她後來因神經生理檢查與 AChR antibody 證實 myasthenia gravis（MG），接受機械通氣及免疫治療。[原始病例全文與 Figure 1–4](https://doi.org/10.3904/kjim.2010.25.1.101)。

這個病例的重要性不是「MG 會導致呼吸衰竭」，而是：**呼吸頻率正在上升，卻不足以保證有效肺泡通氣；補氧讓 PaO₂ 上升，也不能證明 CO₂ 排除有改善。**原論文沒有提供可與兩次 ABG 同時間核算的 VT 與 VD，因此不能虛構這位患者的肺泡換氣量。

## 第零問｜原表究竟把哪種失敗分成 Won't Breathe 與 Can't Breathe？

《Pocket Medicine》第九版 PDF 第 106 頁的 **Etiologies of High PaCO₂** 表格，是一條由腦幹到肺泡的功能路徑：中樞產生呼吸驅動 → 神經肌肉把訊號轉為吸氣力量 → 胸壁與胸膜允許擴張 → 肺與氣道決定阻力、通氣分布及 dead space。這些不是互斥分類；同一名患者可同時在數個環節失敗。

<figure id="ventilatory-chain" class="vq-comparison"><div><span class="small-label">Won't breathe</span><strong>Respiratory drive ↓</strong><p>腦幹／藥物／代謝環境無法提供與 CO₂ 需求相稱的神經輸出；不表示病人主觀「不肯呼吸」。</p></div><div><span class="small-label">Can't generate pressure</span><strong>神經肌肉與胸壁</strong><p>即使神經驅動存在，也可能因 MG、GBS、橫膈無力、重度肥胖或胸壁限制而無法產生足夠 VT。</p></div><div><span class="small-label">Can't ventilate efficiently</span><strong>肺／氣道負荷</strong><p>阻力、dynamic hyperinflation 或 dead space 增加，使維持相同有效換氣需要更高呼吸功。</p></div><figcaption>根據 Pocket Medicine 9E PDF 第 106 頁 Etiologies of High PaCO₂ 原表與腳註重繪。分類用於尋找失敗位置，不代表所有疾病只占一欄。來源核對見<a href="../respiratory-deep-dive-sources.md#pocket-hypercapnia">原圖表與範圍</a>。</figcaption></figure>

## 第一問｜PaCO₂ 上升，到底是 RR、VT、VD，還是 V̇CO₂ 的問題？

在相對穩態下：

<div class="equation"><strong>PaCO₂ ≈ 0.863 × V̇CO₂ / V̇A</strong><strong>V̇A ≈ RR × (VT − VD)</strong><small>V̇CO₂ 單位 mL/min，V̇A 單位 L/min，PaCO₂ 為 mmHg；0.863 涉及單位及氣體條件轉換。V̇E = RR × VT 是總分鐘換氣量；V̇A 才是有效參與 CO₂ 排除的肺泡通氣量。</small></div>

這不是用 RR 直接算 PaCO₂ 的公式。因為 RR 多高，都還缺 **VT（每次真正移動多少氣體）**和 **VD（每次有多少氣體沒有完成有效 CO₂ 交換）**。更重要的是 V̇CO₂（身體每分鐘產生多少 CO₂），會隨發燒、肌肉活動及代謝改變。

<figure id="deadspace-example" class="vq-comparison"><div><span class="small-label">深慢｜數學模型</span><strong>RR 12、VT 500 mL</strong><p>V̇E = 6 L/min；假設 VD = 150 mL，則 V̇A = 4.2 L/min。</p></div><div><span class="small-label">快淺｜數學模型</span><strong>RR 30、VT 200 mL</strong><p>V̇E 仍是 6 L/min；相同 VD 下，V̇A 只剩 1.5 L/min。</p></div><div><span class="small-label">生理含義</span><strong>呼吸次數 ↑ ≠ CO₂ 清除 ↑</strong><p>若 V̇CO₂ 都為 200 mL/min，穩態模型 PaCO₂ 可由約 41 升到約 115 mmHg。這是代入演示，不是任何病例的真實血氣。</p></div><figcaption>原創有效通氣比較；刻意固定分鐘換氣量與每口死腔，凸顯快淺呼吸提高 VD/VT。實際患者的 VT、VD、V̇CO₂、動態平衡都可能同時改變，不能拿此模型預測個別病人的 PaCO₂。</figcaption></figure>

另一個更深的概念是「**相對通氣不足**」。若 V̇CO₂ 從 200 增加到 300 mL/min，V̇A 卻固定在約 4.3 L/min，模型中的 PaCO₂ 就可從約 40 升至約 60。這不代表 V̇A 絕對下降，而是**通氣能力沒有追上代謝需求**。健康人運動時通常能提高通氣來補償，因此 V̇CO₂ 增加很少單獨造成持續 hypercapnia；真正危險的是原已沒有儲備的病人。

同樣地，PE 造成 physiological dead space 增加，但患者常能用更高 V̇E 補償，有時還因低氧刺激而 PaCO₂ 偏低。Dead space ↑ 並不等於 PaCO₂ 必然 ↑；決定點是所需的總通氣量是否超出呼吸泵可提供的能力。

## 第二問｜Won't Breathe 與 Can't Breathe，哪些床邊證據真正改變定位？

### 呼吸中樞：低驅動，還是酸鹼代償？

Opioid、鎮靜藥、部分中樞神經病變可降低對 PaCO₂ 升高的呼吸反應，使呼吸神經輸出不足。表格中的 voluntary hyperventilation、normal PImax（最大吸氣壓）和大致正常 A–a gradient，只是支持「執行呼吸的機械能力尚可、驅動有問題」的線索，**不是單項確診試驗**；自願配合也受意識、肺力學和疲勞影響。

特別要將 **metabolic alkalosis 的低通氣代償**與原發性通氣衰竭區分。若 HCO₃⁻ 升高，降低通氣與提高 PaCO₂ 可能是酸鹼代償的一部分，而非新的肺疾病。若 PaCO₂ 比代謝性鹼血症的預期代償高得多，才更應考慮合併呼吸性酸中毒。不得把所有 PaCO₂ 高都先叫作「CO₂ narcosis」；意識障礙仍需另找藥物、感染、低血糖及其他原因。

### 神經肌肉：為什麼高 PaCO₂ 可能出現得太晚？

正常吸氣需要膈神經、神經肌肉接點與橫膈收縮產生胸腔負壓。MG 是 neuromuscular junction 傳遞失效；GBS 可涉及周邊神經；ALS、頸髓病變與部分 myopathy 又各自位於不同環節。

這些病人會以 RR 上升、使用輔助肌來暫時補償下降的 VT；因此 PaCO₂ 可能直到儲備不足才明顯上升。**Kim 的 MG 個案正是 RR 40/min 並沒有保護她免於高碳酸性呼吸衰竭。**而且她在起初已有 atelectasis 與增大的 A–a gradient：神經肌肉低通氣並不保證所有氧合異常都只有一種機轉。

床邊除 RR 與 ABG，還要看 vital capacity（VC，肺活量）、maximal inspiratory pressure（PImax/MIP）、maximal expiratory pressure（PEmax/MEP）、咳嗽效率、吞嚥和球部肌肉功能，以及短時間惡化速度。PImax 反映吸氣肌產壓能力；PEmax 反映呼氣力量與清痰相關能力。**不能將 MIP 正常等同有安全的氣道保護。**

坐姿轉為仰臥時，腹腔內容物向頭側壓迫橫膈，若橫膈原本無力，VC 可能明顯下降；姿勢相關 VC 下降約 20–30% 以上值得懷疑橫膈無力，但沒有單一通用確診門檻。GBS 等快速進展病況常參考 VC <15–20 mL/kg、MIP 絕對值 <30 cmH₂O、MEP <40 cmH₂O 等危險指標；這些是**評估呼吸儲備與插管準備的警訊，不是忽略趨勢、咳嗽、吞嚥後的自動指令**。

### 胸壁、胸膜與肥胖：能產生壓力，不等於能產生容積

呼吸肌必須克服胸壁與肺的彈性負荷。重度肥胖、kyphoscoliosis、胸壁限制與部分胸膜疾病可使呼吸肌需要更多力量才能產生相同 VT；當增加 RR 已不足以補償，PaCO₂ 才上升。胸水可同時引起限制性力學與肺泡塌陷，但胸水並**不必然**造成 hypercapnia。

**真實病例：**2024 年 *American Journal of Case Reports* 報告一名 **39 歲男性**、BMI **81.1 kg/m²**，入院有意識障礙與急性呼吸衰竭。ABG 記錄 pH **7.103**、PaCO₂ **125**、HCO₃⁻ **37.3**，RR **22/min**，即使給氧 15 L/min，SpO₂ 仍約 87%。病例最後按嚴重 obesity hypoventilation syndrome（OHS）合併急性失代償處理，並評估伴隨感染與心衰因素。[病例全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC11460406/)。

這組資料的重要性是：RR 並不慢，仍可以有極重度換氣不足；HCO₃⁻ 高表示可能早已存在 CO₂ retention 的腎臟代償，而目前 pH 7.103 說明有嚴重急性失衡。不能把肥胖僅理解成「胸壁厚」，因 OHS 同時可能涉及呼吸負荷、睡眠相關呼吸障礙與通氣驅動異常；診斷需排除其他原因。

### 肺與氣道：為什麼 COPD 提高 RR 反而可能更糟？

COPD 的 airflow obstruction 延長吐氣。病人若在上一口尚未吐完就開始下一口，end-expiratory volume 上升，形成 **dynamic hyperinflation** 與 intrinsic PEEP（auto-PEEP）。此時下一次吸氣要先克服殘存正壓，才能產生流量；呼吸肌同時在不利的機械長度工作。

此外，肺氣腫或其他肺實質／肺血管問題可增加 VD/VT，使患者需要更高 V̇E 才能維持一樣的 CO₂ 排出。提高 RR 雖然試圖增加換氣，卻可能縮短吐氣時間、加重 air trapping，造成**呼吸負荷 ↑、有效換氣效率 ↓**的惡性循環。

因此對嚴重阻塞病人，通氣策略不能只追求 PaCO₂ 迅速變 40 mmHg；還要保留足夠呼氣時間，防止 auto-PEEP、過度膨脹及循環受損。在特定情境允許一定高碳酸血症，是權衡壓力傷害與酸血症風險的策略，不代表任何 PaCO₂ 都可放任不管。

## 第三問｜如何區分代償與呼吸泵失代償？哪一個檢查不應被誤用？

### 相同 PaCO₂，不一定是相同的時間尺度

PaCO₂ 60 mmHg 的急性呼吸性酸中毒，HCO₃⁻ 常只上升到約 26 mEq/L，pH 約 7.26；慢性高碳酸血症經腎臟代償，HCO₃⁻ 可能約 32 mEq/L，pH 約 7.35。兩者都是**標準近似模型**，不是個別患者必然數值。HCO₃⁻ 另受利尿劑、腎病與混合代謝性障礙影響，不能由一次抽血精確判定 CO₂ 升高多久。

### 為什麼原表 Lung / Airways 寫「↓ End-tidal CO₂」？

EtCO₂（end-tidal CO₂）是**一次呼氣最後階段**量到的 CO₂ 分壓；PaCO₂ 是抽動脈血所得的 CO₂ 分壓。有效通氣大致均勻時兩者常接近；若嚴重 V/Q 不均或肺灌流受損，呼出的 CO₂ 不能充分代表動脈值，PaCO₂ − EtCO₂ gap 可能增大。

但「EtCO₂ 下降」**不是所有 lung disease 的必然結果**。單純 hypoventilation 時 PaCO₂ 與 EtCO₂ 反而可能一起上升。PE 或低心輸出量可因 CO₂ 送達肺泡減少而使 EtCO₂ 偏低；機械通氣、採樣漏氣、呼氣波形與肺內異質性還會影響判讀。

更細一層：EtCO₂ 不等於整口呼氣混合後的平均 CO₂（mixed expired PCO₂），不能直接把它塞進 Bohr dead-space equation 當成精確 VD/VT 測量。用 PaCO₂ 替代理想肺泡 CO₂ 的 Enghoff modification 也會受到 shunt 和 low V/Q 影響，並非純解剖死腔。

### 病人開始衰竭時，PaCO₂ 可能還在正常範圍

嚴重肺炎／ARDS 患者可能因缺氧刺激而過度換氣，PaCO₂ 原本 25 mmHg。幾小時後，即使 RR 與呼吸功持續增加，PaCO₂ 回升至 40 mmHg。**正常化本身未必是恢復**；它可能是 V̇A 相對於當時需求已經下降。但也可能是疼痛、發燒或其他代謝因素改善，因此不能只憑 25→40 就宣布呼吸肌疲勞。

應同時看呼吸幅度、輔助肌使用、胸腹不同步、意識、咳嗽能力、序列 ABG、肺部與循環狀態。神經肌肉疾病需更早觀察 VC 和呼吸肌力量，不能等到 CO₂ retention 才開始準備呼吸支持。

| 觀察結果 | 最該追問的問題 | 不可直接推論 |
| --- | --- | --- |
| RR 35–40、PaCO₂ 上升 | VT 是否下降？VD/VT 或 V̇CO₂ 是否增加？ | 病人沒有努力呼吸 |
| VC／MIP 快速變差 | 呼吸肌儲備是否正在耗盡？可否咳嗽、吞嚥？ | SpO₂ 正常就安全 |
| EtCO₂ 偏低、PaCO₂ 偏高 | 灌流、V/Q、採樣及波形為何異常？ | 可以單憑 gap 診斷 PE |
| 同 PaCO₂ 60、不同 pH | 急慢性代償與混合型酸鹼異常？ | 數字相同所以風險相同 |
| NIV 後 SpO₂ 改善，但更嗜睡 | 介面是否有效送達通氣？氣道是否安全？ | 補氧成功等於呼吸支持成功 |

**把生理連到決策：**氧氣提高肺泡可利用的氧分壓，不直接替病人排 CO₂；bilevel NIV 藉由吸氣與呼氣壓差提供壓力支持、減輕部分呼吸肌負荷，但無法替病人保護氣道或清除大量分泌物。插管可提供更可靠的氣道與侵入式通氣，但也承擔鎮靜、血流動力學及呼吸器傷害的代價。何時用哪種支持，取決於**可逆性、氣道安全、惡化速度與初始治療反應**，不是單一 PaCO₂ 或 pH 門檻。細節與官方國考三題見[既有 NIV 治療篇](2026-10-22-hypercapnic-failure.md)。

**結論：** Hypercapnia 不是「呼吸次數不夠」的診斷，而是 CO₂ production 與 effective ventilation 的供需結果。原圖將問題分成 Won't / Can't Breathe，是要辨識究竟哪個環節讓**維持正常 PaCO₂ 所需要的 ventilatory demand 超過當下 ventilatory capacity**。最有價值的早期訊號，可能不是 PaCO₂ 已經升高，而是患者為了讓它暫時正常，已付出無法持續的呼吸功。

[返回 A–a gradient 與 shunt 深入篇](2026-10-25-hypoxemia-mechanisms.md)・[NIV 治療決策與國考詳解](2026-10-22-hypercapnic-failure.md)・[原表、病例與來源界限](../respiratory-deep-dive-sources.md)
