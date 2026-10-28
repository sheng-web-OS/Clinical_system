# 早晨一張 Lab sheet（第一篇）：先確認數字是否真的代表病人

早晨的報告上出現 K 7.8 mEq/L，第一個問題未必是「要配哪一項降鉀藥」，而是：**這個值是病人體內的濃度，還是採血與檢體處理後才出現的數字？**但檢體可能有問題，也不等於病人沒有立即危險。理解一張 Lab sheet，需要把**量測的來源、病人當下的危險，以及能支持什麼臨床推論**分開。

我們先讀一份有完整檢體時間、方法和運輸紀錄的真實病例；再對照兩組經過不同納排篩選的急診研究；最後借助腎臟與心衰竭的臨床證據，釐清為何**檢驗值即使可靠，也不等於病因與治療方向已確定**。每一份資料都保留自己的病人、分母與適用界線，不會把不同研究拼成同一張虛構的病例。

**本篇的範圍是「檢驗可信度」而非整張抽血單的完整醫囑教學。** 先用有原始採檢時序的高鉀／CBC 真實病例拆開「樣本數字」、「病人體內狀態」與「危急風險」；Cr、Na、酸鹼與其他檢驗只引出下一層問題。要判斷實際檢驗選擇與處置，必須另有涵蓋相應器官及病程的真實病例、試驗與指引，不能把本篇的偽高鉀研究外推成整張 Lab sheet 的通用決策規則。

## 第一問｜檢驗值量到的是什麼？先看一份真的誤導過臨床的 Lab

2024 年 *International Journal of Emergency Medicine* 刊登一名**55 歲男性、急性骨髓性白血病（AML）**患者的病例報告：[Manual flagging failed to identify pseudohyperkalemia in acute myeloid leukemia](https://pmc.ncbi.nlm.nih.gov/articles/PMC11462689/)。作者有原始 **Table 1：不同檢體、採集處理方式與 K 值**，這使得本篇不必自行捏造「第一次抽 6.3，第二次抽 4.9」的情節。

原文 Table 1 的採檢時間與運送方式，比單純比較 K 的大小更值得先看。以下是從原表抽出、重新整理的四筆**同一名 AML 患者**資料，並沒有把不同檢體視為同條件重測：

| Sample／2024-04-03 採樣時間 | K（mEq/L） | 檢體與實驗室方法 | 運送方式及不可省略的限制 |
|---|---:|---|---|
| A／12:00 | 3.0 | 家中採血；lithium-heparin **plasma**；Beckman Coulter AU5800 | Courier＋步行送檢；採樣場所、方法與 B–D 不同 |
| B／20:03 | 6.7 | 急診；lithium-heparin **whole blood**；NovaBiomedical pHOx Ultra | **Pneumatic tube**，無離心 |
| C／20:48 | 7.8 | 急診；同為 lithium-heparin whole blood／pHOx Ultra | **Pneumatic tube**，重新採樣仍經相同運送環節 |
| D／23:37 | 3.6 | 急診；同為 lithium-heparin whole blood／pHOx Ultra | **步行送檢**；但是**已開始降鉀治療約 30 分鐘**，不能當無治療的對照 |

原病例還有一個不容易從「6.7→7.8→3.6」的簡短摘要看出的前提：**前一天曾因 K 2.8 mEq/L 接受靜脈補鉀 40 mEq，且有長期口服補鉀及相關慢性病用藥史**。因此，判讀必須同時保留真的高鉀風險與檢體失真風險，不能看極端 WBC 便從事後結局反推臨床當下必然安全。這是資料所允許的比較：A 與 B 不只時間不同，也改了檢體基質及儀器；B 與 C 再抽一次，卻保留了同一條氣送管運輸路徑；C 與 D 同為全血儀器、卻同時改變運送方式且介入降鉀治療，因此 **K 下降既可能受採檢方式影響，也受到治療時序混雜，無法定量拆解**。

| 資料（原文） | 值或條件 | 這筆資料能支持什麼 |
|---|---|---|
| WBC | **206.8 × 10³/µL**（90% blasts） | 嚴重白血球增多，某些檢體在抽血／處理時存在細胞脆弱與鉀釋放可能 |
| Hb／platelet | **7.9 g/dL／38 × 10³/µL** | 確認這不是可套用「一般低風險成年人」研究的族群 |
| Creatinine | **1.2 mg/dL**（報告當次） | 是當次一個血清數值；沒有完整 baseline 或尿量，不能由此判定無 AKI |
| Potassium（樣本 B） | **6.7 mEq/L** | 初次化學檢驗顯示高值 |
| Potassium（重新採樣 C） | **7.8 mEq/L** | 「重抽仍高」並不能單獨排除檢體處理造成的假性升高 |
| Potassium（後續樣本 D） | **3.6 mEq/L** | 原作者據此支持假性高鉀；**但 D 是降鉀治療開始約 30 分鐘後採得，不能當未治療的純粹重驗對照** |


**同一名真實病人，也有另一項不能直接相信的檢驗值。** 4 月 3 日居家抽血 Hb **4.5 g/dL**（兩天前 **7.5 g/dL**）而被轉送急診評估輸血；急診 Hb 卻是 **7.9 g/dL**。原作者認為居家的 4.5 是檢驗錯誤，而**不是**幾小時內真正造血恢復的證據。後續 packed RBC 輸血是在 K 重新確認正常之後；這是作者記載的順序，並非有對照組的輸血時機試驗。Hb 的不一致與 K 6.7／7.8 的不一致出現在同一個患者，**但不能推斷兩者都是相同的採血／氣送管機轉所致**；也不能因其中一次 Hb 不可信，就忽視白血病、嚴重貧血或其他 CBC 結果。這才是跨項 Lab 判讀的關鍵：每個 analyte 的測量干擾與病理生理，必須個別確認。[原文 Case presentation](https://pmc.ncbi.nlm.nih.gov/articles/PMC11462689/)。

該病人沒有典型高鉀症狀，ECG 也沒有相應變化；但臨床團隊仍先給了抗高鉀治療，之後由腎臟科懷疑 pseudohyperkalaemia，與檢驗室重新核對檢體類型、採樣和處理過程。原文也特別提到：這不是一般「抽血管有紅血球溶血警語」的簡單個案；當時有**極端白血球增多**，而且醫囑介入與檢體時間互相交錯。作者最後的診斷不能被本篇簡化成「ECG 正常，所以 K 7.8 一定假」。

這段讀法，和照抄一張「高鉀就打什麼藥」的表不同。要問的是：**K 這個數字來自哪種檢體、在哪個時間採集、怎麼送達與處理、在治療前還是後、其他資料是否支持真性高鉀？** 試管外破壞細胞與病人體內溶血是兩件不同的事，前者不能自動拿來解釋患者的 Hb 下降。

[AJKD *Laboratory Anomalies in the Basic Metabolic Panel: Core Curriculum 2025*](https://pubmed.ncbi.nlm.nih.gov/39396361/) 進一步指出，採檢、運送、保存、分析方法乃至檢驗後報告都會影響結果。細胞內鉀遠高於細胞外；抽血後溶血或特殊血球狀態可能改變樣本的 K，這是**檢體層面的機轉**。臨床上必須將分析干擾與真正急症的安全評估**並行**，不能拿一項去否定另一項。

### 另一個真實病人：這次是 platelet，而不只是極端 WBC

不要把 AML 個案的「氣送管＋脆弱白血球」當成唯一一種偽高血鉀。2018 年 Šálek 報告的是**另一位 62 歲女性**，她有 essential thrombocythemia，因胃潰瘍出血接受手術後暫停原本的血液疾病用藥。[原始病例與 Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC5806620/) 當次抽血顯示 **platelets 1305×10⁹/L、WBC 39.8×10⁹/L、serum K 6.3 mmol/L**。改看不同採樣位置與方法的檢體，**靜脈 lithium-heparin plasma K 4.6、左股動脈 whole blood（blood-gas analyzer）K 3.4 mmol/L**。這並非只改變試管基質、其他條件完全相同的配對實驗；採血位置及分析方法也不同，不能把數值落差全歸因於凝血時血小板釋鉀。即使原文 serum free haemoglobin **0.09 g/L**，仍可見血清和其他檢體之間明顯矛盾；這說明**沒有明顯紅血球溶血警訊，也不能單憑它排除偽高血鉀**。

為什麼 platelet 會影響 K？**Serum 需要凝血，血小板在此過程可能釋出細胞內的 K**；抗凝的 plasma 不經相同凝固過程，而 whole blood 的前處理又不同。作者認為血小板與白血球增加、檢體離心時細胞可能受損，均有助於解釋結果。原文還有**11 組**血清 K 與 platelet 配對（Spearman ρ **0.64**）；這是同一位病人的時間序列相關，**不是**證實每個血小板高的病人都可直接把 serum K 扣掉固定數值，也不是敏感度／特異度。這段不同病人的真實資料，讓你看到 **CBC 可以成為 chemistry panel 的解釋前提**；然而臨床危險是否須立即處理，仍不能由個案報告單獨批准。

## 第二問｜醫師取得新證據後，為什麼可能改變判斷？先看研究真正包含哪些病人

2020 年正式發表的前瞻性急診研究 [Accuracy of Hemolyzed Potassium Levels in the Emergency Department](https://pmc.ncbi.nlm.nih.gov/articles/PMC7673871/) 從有溶血高血鉀且曾在 12 小時內重抽的個案中，最後留下**66 個低風險遭遇**；初次溶血 K 中位數 **5.8 mmol/L**，重抽後中位數 **3.9 mmol/L**，這 66 人沒有持續性真高鉀（該小樣本真高鉀比例的 95% 信賴區間上界約 **6%**）。

這結論**不能搬到所有病房病人**。原研究刻意排除 **65 歲以上、eGFR <60、使用可能影響 K 的藥物、血液惡性疾病**等情況，也排除重抽前已接受降鉀治療者。例如一名 70 歲、使用 ACEi 且懷疑 AKI 的心衰竭病人，**不在這 66 人的驗證族群內**；不能以這項研究保證「檢體有溶血，就不需評估或處理危急高鉀」。

**研究設計還有一個更根本的限制：** Wilson 等人從 EHR 找到有「初次溶血高 K、後續重抽」紀錄的 399 次就診，再依事先條件排除 333 次，才得到 66 次。原文 Limitations 另記載 **35 例未重抽就已離院**而排除在分析外。換言之，這項前瞻性觀察研究檢驗的是「符合條件、且實際有重抽者」的結果；**它並沒有把『不重抽』與『重抽』隨機比較，也未直接驗證省略重抽後的安全結局**。因此 0/66 不是醫囑層級的『可放心不追查』保證，尤其不能推給 AML、CKD、心電異常或循環不穩者。[原研究 Methods／Limitations](https://westjem.com/articles/accuracy-of-hemolyzed-potassium-levels-in-the-emergency-department.html)。

接著讀 2025 年 *West J Emerg Med* 回溯性研究 [Hyperkalemia or Not? A Diagnostic Pitfall in the Emergency Department](https://pmc.ncbi.nlm.nih.gov/articles/PMC11908522/)：研究的是**初次 K ≥5.0 且當日有重抽的 2,440 名急診患者**，其中 **1,576（65%）**重抽仍高、**864（35%）**重抽恢復正常；在 864 名「初次高、重抽正常」者中，**597（69%）**初次檢體還有溶血證據。

這些數字不能簡寫成「急診高血鉀有 35% 都是假」，因為研究**事先選了有當日重抽的人**，不是所有送檢者或所有病房患者的盛行率。也不能用「69% 有溶血」推論溶血是所有異常唯一原因：研究分類建立的是抽樣與重測之間的關係，仍要辨別治療時序、患者危急風險和其他機轉。

<figure id="lab-three-clocks" style="max-width:950px;margin:1.5rem auto">
<div style="border:1px solid #80909b;border-radius:10px;padding:1rem;margin-bottom:0.9rem">
<h3 style="margin-top:0">① 真實 AML 病例：同一天，採樣條件和治療同時改變</h3>
<p>作者的 2024-04-03 Table 1；以下為原始採血時間、K（mEq/L）與方法的教學重排，並非另造病例。</p>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,175px),1fr));gap:0.65rem" role="group" aria-label="AML 病例四次檢體時序">
<div data-evidence-node="case-sample" style="border:1px solid #8999a1;border-radius:8px;padding:0.7rem"><strong>A　12:00</strong><p style="font-size:1.4em;margin:0.2rem 0">K 3.0</p><p>家中抽血 → courier＋步行；plasma／另一種分析儀。</p></div>
<div data-evidence-node="case-sample" style="border:1px solid #8999a1;border-radius:8px;padding:0.7rem"><strong>B　20:03</strong><p style="font-size:1.4em;margin:0.2rem 0">K 6.7</p><p>急診 whole blood → 氣送管；與 A 的基質、儀器不同。</p></div>
<div data-evidence-node="case-sample" style="border:1px solid #8999a1;border-radius:8px;padding:0.7rem"><strong>C　20:48</strong><p style="font-size:1.4em;margin:0.2rem 0">K 7.8</p><p>再次 whole blood → <strong>仍經氣送管</strong>。</p></div>
<div data-evidence-node="case-sample" style="border:2px solid #9c7a4b;border-radius:8px;padding:0.7rem"><strong>D　23:37</strong><p style="font-size:1.4em;margin:0.2rem 0">K 3.6</p><p>whole blood → <strong>改步行</strong>；也已開始降鉀治療約 30 分鐘。</p></div>
</div>
<p style="margin-top:0.8rem"><strong>不能分離的兩個改變：</strong>C→D 不只換了運送方式，也經過治療。這組觀察支持作者追查偽高鉀，<strong>不能</strong>把 K 下降全歸因於改成步行送檢。正常 ECG 也不代表當時沒有急症風險。</p>
</div>
<div style="border:1px solid #80909b;border-radius:10px;padding:1rem">
<h3 style="margin-top:0">② 研究分母樹：35% 到底是哪些人的 35%？</h3>
<div data-evidence-node="cohort-root" style="border:2px solid #6b8797;border-radius:9px;padding:0.8rem;text-align:center;max-width:590px;margin:0 auto 0.7rem">
<strong>n=2,440</strong>　初次 K ≥5.0 且<strong>當日確有重抽</strong>的急診患者
</div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:0.7rem">
<div data-evidence-node="cohort-subgroup" style="border:1px solid #80909b;border-radius:9px;padding:0.75rem">
<strong>1,576／2,440（65%）</strong>
<div style="height:0.6rem;background:#dce4e6;border-radius:5px;margin:0.5rem 0"><div style="width:65%;height:100%;background:#57788b;border-radius:5px"></div></div>
同日重抽仍升高（研究定義的持續高鉀）。
</div>
<div data-evidence-node="cohort-subgroup" style="border:1px solid #80909b;border-radius:9px;padding:0.75rem">
<strong>864／2,440（35%）</strong>
<div style="height:0.6rem;background:#dce4e6;border-radius:5px;margin:0.5rem 0"><div style="width:35%;height:100%;background:#a68154;border-radius:5px"></div></div>
同日重抽正常；接著<strong>只在這 864 人內</strong>分層。
<div style="border-top:1px dashed #8999a1;margin-top:0.7rem;padding-top:0.65rem">
<div data-evidence-node="cohort-subgroup"><strong>597／864（69%）</strong> 初次檢體有溶血</div>
<div data-evidence-node="cohort-subgroup"><strong>267／864（31%）</strong> 未見溶血證據；原因尚不明</div>
</div>
</div>
</div>
<p style="margin-top:0.75rem"><strong>分母限制：</strong>864／2,440 是在「當日被選擇重抽」者中的比例，並非所有急診或病房抽血者的假性高鉀盛行率。597／864 的 69% 也<strong>不是</strong> 597／2,440 的百分比。</p>
</div>
<div data-evidence-node="lowrisk-cohort" style="border-left:4px solid #6d7f98;padding:0.6rem 0.8rem;margin-top:0.85rem">
<strong>另一份獨立研究：n=66</strong> 嚴格篩選的低風險溶血高鉀患者，重抽 K 中位數 <strong>3.9 mmol/L</strong>，無持續性真高鉀，但 95% CI 上界約 6%；排除高齡、eGFR &lt;60、相關藥物與血液惡性疾病等。<strong>不能把 n=66 合併進 n=2,440 的分母，也不能推及 AML 病人。</strong>
</div>
<figcaption>圖 1｜兩種原創證據可視化：上半部依 2024 AML 病例 Table 1 重排採樣時序、運送與治療混雜；下半部依 2025 急診同日重抽研究整理 2,440→1,576／864→597／267 的不同分母。n=66 為另一獨立研究。三條不混同的證據線，並非同一位病人的三個時點，亦非 validated clinical decision rule；不是出版社原圖重製。</figcaption>
</figure>

**以下是測量原理的類比，不是上述 AML、血小板或急診 K 研究直接驗證的其他電解質結論。** Serum total CO₂ 主要與 bicarbonate 相關，卻**不是動脈 pH 和 PaCO₂**；Na 需連同水與滲透質的背景解讀，部分測定方法（例如間接 ISE）還可能受樣本組成干擾；BUN／Cr 各有生成與清除機轉，單憑比值不能確定 AKI 病因。這些延伸可作為下一篇檢驗學習的問題，**不能**從前述兩名真實患者推論他們有特定酸鹼障礙、低鈉病因或 AKI 處置。初見結果時，先問哪些未測量的生理量、檢體方法與時間點會使解釋改變。

## 第三問｜Cr 上升就代表利尿過多？哪些推論無法從 Lab sheet 得到？

**這裡切換到另一批不同病人與不同證據，不是在前述 AML 病人身上加寫心衰竭。**

在急性失代償心衰竭，serum creatinine 可能因多種機轉上升：動脈灌流下降、靜脈鬱血、治療中的血流動力改變、真正腎實質受傷、合併感染或藥物傷害等。[*Acute kidney injury in acute heart failure—when to worry and when not to worry?*](https://pmc.ncbi.nlm.nih.gov/articles/PMC11879425/) 整理了相關臨床研究：**成功去鬱血伴隨的輕度 Cr 變化**，與**持續鬱血合併惡化腎功能**，在研究中的預後關聯並不相同。它不是說「Cr 上升可以忽略」；而是指出，**單看 Cr，無法分辨去鬱血、腎灌流下降及實質傷害**。

[密西根大學住院心衰竭利尿指引 Q18](https://www.ncbi.nlm.nih.gov/books/NBK589894/) 也明確解釋：持續有鬱血時，適度 SCr 上升不一定需要自動停止利尿；但顯著低血壓、血管內容量耗竭與其他 AKI 病因仍要辨認。這是**有臨床評估條件的敘事與建議**，不是看到一個 Cr 便由 AI 遠端判定「繼續打利尿劑」或「立即補 saline」。

AKI 的診斷本身另有時間維度：請核對 [KDIGO 2012 原始 Table 2（AKI 分期，PDF p.22）](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf#page=22) 的定義，並閱讀 [Figure 4（Stage-based management，PDF p.28）](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf#page=28) 如何將風險分層與腎毒性藥物、容量／灌流、Cr／尿量監測連起來；這張圖不是固定補液或透析處方。KDIGO 要求核對 **48 小時內 SCr ≥0.3 mg/dL 增加、7 天內 ≥1.5 倍基線，或連續至少 6 小時尿量 <0.5 mL/kg/h**。光有「尿量 8 小時總計」不能保證每一個 6 小時區間都符合門檻；光有一筆孤立的 Cr 數值，沒有基線、變化時間與尿量，就不能推得出 CKD、AKI stage 或確切病因。更不能把用於穩態的 eGFR 當成急性變化期間即時的腎臟清除能力。

如果臨床在看完整的 Lab sheet，要分辨的是：

| 檢驗領域 | 該欄實際量到什麼 | 要理解機轉仍缺哪一層證據 |
|---|---|---|
| K／Na／Cl | 電解質檢體濃度與可能的採檢旗標 | 同一時間的檢體類型、血糖/滲透狀態、藥物、心電風險及重驗時序 |
| Serum total CO₂ | 以 bicarbonate 為主的總 CO₂ 量 | 若要談酸鹼障礙，仍欠 pH／PaCO₂、氯及 AG 的同時點資料 |
| BUN／Cr | 代謝物濃度與時間趨勢 | baseline、尿量、循環灌流、鬱血、藥物、尿液與影像 |
| CBC／DC、Hb、platelet | 血球數量和分類 | 感染、出血、稀釋、骨髓或檢體干擾的其他證據；WBC 上升≠感染定論 |
| Mg、Ca、PO₄ | 礦物質濃度 | 心律、症狀、藥物及重複測量；缺乏這些就不能自行設定治療必要性 |

這裡的空格**就是應該承認的未知數**，而不是由教材為了好看把 ECG、尿量、影像或「09:00 新證據」自己補出來。讀者要學的是如何發現**資訊不足以支持結論**，不是記住一位從不存在的病人在 09:00 做了哪種醫囑。

## 破除過度推論｜把原始研究與個人決策分開

**誤解一：高 K 檢體有溶血，表示患者一定不需要急救。** 錯。溶血增加假性高鉀可能，危險症狀、ECG、快速複查與個體高危條件仍需並行評估；正常 ECG 不是排除真性高鉀的檢查。原始 66 人研究不涵蓋高齡、CKD 和 RAAS 用藥患者。

**急救風險與檢體確認必須並行**，而不是「懷疑假的就一律等」或「看到紅字就無差別給藥」。[UKKA 2026 原始 Figure 4（PDF p.75）](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=75) 將有危險時的心肌保護、鉀轉移、實際排鉀、K／血糖監測及防復發分開；[Table 22（PDF p.98）](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=98) 則提醒 insulin-glucose 後低血糖與反彈監測。原始流程有其適應症與證據強度，不代表每名 K 6.4、ECG 正常者都需要相同 IV calcium、insulin 或補糖量，更不能以本站文章直接替代醫囑。

**誤解二：K 7.8 重抽後 3.6，就等於從未真高鉀。** 不成立。AML 病例的後段樣本有**降鉀介入後**的時序污染，必須回查原始 Table 1 的檢體別及採血方式，不能假裝有無治療的成對試驗。

**誤解三：發現 AKI 就代表利尿藥造成缺水。** AKI 的**定義**不直接提供**病因**。血流動力、鬱血程度及治療反應是另一組必須解釋的證據；來源是心衰竭研究與專業指引；**不應藉虛構的 Hb、Mg 或 Cr 數據**替病人補寫未曾觀察的病程。

**誤解四：CBC、Mg 或 Na 出現紅字，總要配上一條明確醫囑。** 沒有對應臨床症候群、病程、症狀、危險性與測量品質的支持，教材只能呈現**可能機轉與需要查證的訊息**，不能編造使用某藥後的好轉來合理化處置。

## 自己練習三問，而不需要擔任處方審稿人

1. **構念**：實驗室的 K 是病人體內濃度，還是也可能包含檢體外釋放的鉀？AML 原始 Table 1 哪些資訊證明這個問題很重要？
2. **臨床推理**：66 人的低風險研究，為什麼不能幫 70 歲 CKD 心衰竭患者做完整治療決策？2,440 人研究的分母又是誰？
3. **破除推論**：為何「Cr 上升」同時可能見於有效去鬱血和病況惡化？還要補哪些床邊證據，才有資格從生理假說進入治療討論？

[全部原始病例、研究納排、指引 Figure／Table 與來源界線](../lab-morning-sheet-sources.md)。本篇**不提供選抽血項目或醫囑的 AI 範本**；實際檢驗與治療需由照護團隊按病況及機構規範判斷。所列數字不是本站設計或合成的 Lab panel；原作者的觀察、分析性研究與指引共識並不被混寫成同一病人的時間線。
