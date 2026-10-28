# 早晨一張 Lab sheet（第一篇）：先確認數字是否真的代表病人

早晨的報告上出現 K 7.8 mEq/L，第一個問題未必是「要配哪一項降鉀藥」，而是：**這個值是病人體內的濃度，還是採血與檢體處理後才出現的數字？**但檢體可能有問題，也不等於病人沒有立即危險。理解一張 Lab sheet，需要把**量測的來源、病人當下的危險，以及能支持什麼臨床推論**分開。

**同一個人、同一天，血鉀可能因為採樣與運送條件而得到完全不同的數字。** 數值差異也可能出現在治療前後；若沒有看清時間線，就會把檢體變化誤讀成病情變化。這不只影響 K：Hb、Cr、Na 和酸鹼檢驗都有各自的測量前提。先辨認數值是否可信，才能進一步討論病因與處置；而即使數值可靠，也未必已經知道該如何治療。

## 第一問｜檢驗值量到的是什麼？同一天，K 為何從 3.0 變成 7.8？

2024 年 *International Journal of Emergency Medicine* 報告一名 **55 歲急性骨髓性白血病（AML）男性**的經歷。4 月 3 日，他原本因居家抽血顯示 Hb **4.5 g/dL**、疑似需要輸血而被轉送急診；同一份居家檢體的 K 是 **3.0 mEq/L**。可是到了急診，血鉀突然變成 **6.7 mEq/L**；45 分鐘後重抽，竟升到 **7.8 mEq/L**。究竟是病人在短時間內發生危險的高血鉀，還是檢體離開身體後改變了？

不能只因為數字起伏大，就認定其中一筆是錯的。這名患者前一天才因 **K 2.8 mEq/L** 接受靜脈補鉀 **40 mEq**，平時也使用口服鉀及其他慢性病藥物；真正的鉀變化仍有可能發生。另一方面，急診 CBC 顯示 **WBC 206.8 × 10³/µL、90% blasts**，Hb **7.9 g/dL**、platelets **38 × 10³/µL**。極端增多、可能較脆弱的白血病細胞，使採血後細胞受損、釋放鉀到檢體中的可能性必須被認真考慮。[原始病例與 Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11462689/)

要理解血鉀為何變化，還得知道四次血並不是以相同方式處理的：

| 4 月 3 日採檢時間 | K（mEq/L） | 當次檢體與運送 |
|---|---:|---|
| A／12:00 | **3.0** | 居家抽血；lithium-heparin **plasma**，由 courier 與步行送檢；Beckman Coulter AU5800 |
| B／20:03 | **6.7** | 急診 lithium-heparin **whole blood**，經氣送管；NovaBiomedical pHOx Ultra |
| C／20:48 | **7.8** | 急診再次採 whole blood，仍以氣送管送檢，使用相同分析儀 |
| D／23:37 | **3.6** | 急診 whole blood 改由人員步行送檢，使用相同分析儀；**採樣時已開始降鉀治療約 30 分鐘** |

第一筆是居家的 **plasma**，後三筆則是急診的 **whole blood**，兩者連分析儀都不同，所以不能把 A 到 B 的差距直接當作體內鉀的上升幅度。更關鍵的是 B 到 C：醫師雖然重抽了一次，檢體卻再次經過**相同的氣送管路徑**。若機械運送對脆弱血球造成傷害，重抽而不改變運送條件，仍可能得到偏高的結果。這也說明，**「重抽仍高」不一定等於已排除採檢誤差**。

當時患者沒有典型高鉀症狀，ECG 也沒有相應變化；但這些陰性發現不足以保證他沒有危急高血鉀，臨床團隊仍先給予降鉀治療並會診腎臟科。後來因懷疑 *pseudohyperkalemia*（假性高血鉀），重新檢視檢體運送程序，改由人員步行將血送到實驗室，得到 K **3.6 mEq/L**。這是診斷方向轉變的重要線索，卻還不能證明「只要停止氣送管，K 就從 7.8 降到 3.6」：**最後一筆是在降鉀治療開始約 30 分鐘後採得**。運送方式與治療時序同時改變，兩者各貢獻多少，無法從這四筆資料單獨算出。作者據其他檢驗、運送調查及臨床情境判斷存在假性高鉀成分，並追查醫院原有的高白血球檢體提醒流程為何失效。

還有一個容易被血鉀搶走注意力的問題：**這名患者為什麼會被送到急診？**居家 Hb **4.5 g/dL**（兩天前 **7.5 g/dL**），看起來像是嚴重貧血急遽惡化；然而急診 Hb 卻是 **7.9 g/dL**。如此大的差距不能用短短幾小時內的正常造血恢復解釋；原作者判斷居家 Hb 4.5 是錯誤讀值。這個 Hb 問題與 K 假性升高發生於同一名病人，**卻沒有證據顯示它們具有相同的檢體干擾機轉**。病人仍確實患有 AML 與貧血；單一 Hb 讀值有疑問，不等於其餘 CBC 數據都不可信。原病例記載，確認後續 K 正常後才輸注一單位 packed RBC；這個先後次序本身不能證明何種輸血時機比較安全。

這起病例揭露的是兩個必須同時處理、但不能互相抵銷的風險：一方面，**把檢體假高鉀當作真高鉀治療**，可能帶來醫源性低血鉀；另一方面，**只憑白血球極高或 ECG 正常就宣布高鉀是假的**，也可能錯過真正的危急狀態。原病例報告的一次 creatinine **1.2 mg/dL**，沒有完整基線與尿量，也不能單憑它判斷患者不存在 AKI。臨床需要同步追問的是採檢／運送方式、治療前後的時間、其他生理證據與即刻危險，而不是讓單一數字代替整個判斷。

[AJKD *Laboratory Anomalies in the Basic Metabolic Panel: Core Curriculum 2025*](https://pubmed.ncbi.nlm.nih.gov/39396361/) 將採血、運送、保存、分析與報告等環節放在同一條檢驗鏈中。細胞內鉀遠高於細胞外；若細胞在**身體外**的檢體中破裂，量得的 K 就可能高於病人體內的濃度。這與病人體內真正發生溶血或高血鉀不是同一件事。**先釐清測量值如何形成，再判斷它是否反映病人體內的變化**，才不會把檢驗誤差誤認為疾病，也不會用「可能是誤差」排除急症。

### 如果不是白血球，而是血小板特別高？

AML 患者的問題可能出現在運送途中，但另一種情況是在**試管凝血的過程**才使血鉀升高。2018 年 Šálek 報告一位 **62 歲 essential thrombocythemia 女性**，因胃潰瘍出血接受手術並暫停原本的血液疾病治療。她的 **platelets 1305×10⁹/L、WBC 39.8×10⁹/L**，血清（serum）K **6.3 mmol/L**；改採抗凝的靜脈 plasma，K 是 **4.6 mmol/L**，左股動脈全血的血氣分析則是 **3.4 mmol/L**。[原始病例與 Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC5806620/)

為什麼同一名病人的三份檢體會相差這麼多？Serum 採檢須經凝血，當血小板數量極高，凝血過程可能使血小板釋出更多細胞內的鉀；抗凝 plasma 避開了相同的凝固程序。因此，**血小板增加可能讓 serum K 高於病人當下的體內血鉀**。不過，這三次採血連部位與分析方法也不相同，還不能把 6.3 與 3.4 的全部差距都算在血小板釋鉀上。即使 serum free haemoglobin 只有 **0.09 g/L**，也不能只憑沒有明顯紅血球溶血訊號，就排除這種檢體失真。

這個病例也追蹤了 **11 組**血清 K 與 platelet 的變化，兩者呈正相關（Spearman ρ **0.64**）。它強化了「血球數量會影響某些檢體血鉀」的懷疑，卻不能據此為每位血小板偏高的患者訂出固定的 K 扣除值。**讀 chemistry panel 時，CBC 有時不是另一張獨立的報告，而是解釋化學數值可信度所必需的資訊。** 但這並不能取代患者當下的急症評估。

## 第二問｜醫師取得新證據後，為什麼可能改變判斷？先看研究真正包含哪些病人

2020 年正式發表的前瞻性急診研究 [Accuracy of Hemolyzed Potassium Levels in the Emergency Department](https://pmc.ncbi.nlm.nih.gov/articles/PMC7673871/) 從有溶血高血鉀且曾在 12 小時內重抽的個案中，最後留下**66 個低風險遭遇**；初次溶血 K 中位數 **5.8 mmol/L**，重抽後中位數 **3.9 mmol/L**，這 66 人沒有持續性真高鉀（該小樣本真高鉀比例的 95% 信賴區間上界約 **6%**）。

這結論**不能搬到所有病房病人**。原研究刻意排除 **65 歲以上、eGFR <60、使用可能影響 K 的藥物、血液惡性疾病**等情況，也排除重抽前已接受降鉀治療者。例如一名 70 歲、使用 ACEi 且懷疑 AKI 的心衰竭病人，**不在這 66 人的驗證族群內**；不能以這項研究保證「檢體有溶血，就不需評估或處理危急高鉀」。

如果進一步問：「既然這 66 人重抽都正常，遇到下一名檢體溶血的病人，是否可以省去重抽？」答案仍然是否定的。Wilson 等人起初找到 **399 次**已經有重抽紀錄的急診就診，排除 **333 次**不符合條件者，才留下 66 次；研究另外提到 **35 例未重抽即離院**，並未納入這個分析。也就是說，**研究只觀察了符合條件而且實際重抽的人，沒有比較『不重抽』和『重抽』兩組病人的臨床結局**。66 人中未觀察到持續性高鉀，不能轉換成對 AML、CKD、心電異常或循環不穩患者「不必追查」的保證。[研究方法與限制](https://westjem.com/articles/accuracy-of-hemolyzed-potassium-levels-in-the-emergency-department.html)。

接著讀 2025 年 *West J Emerg Med* 回溯性研究 [Hyperkalemia or Not? A Diagnostic Pitfall in the Emergency Department](https://pmc.ncbi.nlm.nih.gov/articles/PMC11908522/)：研究的是**初次 K ≥5.0 且當日有重抽的 2,440 名急診患者**，其中 **1,576（65%）**重抽仍高、**864（35%）**重抽恢復正常；在 864 名「初次高、重抽正常」者中，**597（69%）**初次檢體還有溶血證據。

這些數字不能簡寫成「急診高血鉀有 35% 都是假」，因為 **2,440 人全都是當天完成重抽的患者**，不能拿這個比例估計所有急診高鉀患者。即使 864 人重抽後恢復正常，也不能將其中 597 人首次檢體的溶血，當成每一例異常的唯一原因。遇到下一名 K 升高的患者，還需要知道**兩次血如何採集、重抽前是否已接受治療，以及當下有無危急徵象**，才不會把研究中的比例誤當作個別患者的答案。

<figure id="lab-three-clocks" style="max-width:950px;margin:1.5rem auto">
<div style="border:1px solid #80909b;border-radius:10px;padding:1rem;margin-bottom:0.9rem">
<h3 style="margin-top:0">① 真實 AML 病例：同一天，採樣條件和治療同時改變</h3>
<p>2024 年 4 月 3 日，從居家採血到急診重驗，四筆 K 值的採檢與送檢方式並不相同。</p>
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
<figcaption>圖 1｜上：55 歲 AML 患者同日四次血鉀結果，特別注意 D 的治療時序（Cao，2024，Table 1）。下：另項急診研究中，同日重抽者的結果分布（Stephan 等，2025）；66 人資料來自第三項獨立研究（Wilson 等，2020），不能與 2,440 人合併計算，也不能直接當成不重抽的處置規則。</figcaption>
</figure>

**血鉀不是唯一受檢體與測量方法影響的項目。** Serum total CO₂ 主要與 bicarbonate 相關，卻**不是動脈 pH 和 PaCO₂**；Na 需連同水與滲透質的背景解讀，部分測定方法（例如間接 ISE）還可能受樣本組成干擾；BUN／Cr 各有生成與清除機轉，單憑比值不能確定 AKI 病因。但這些機轉本身並沒有出現在前述兩名病人的原始檢驗紀錄中，不能因此替他們加上酸鹼障礙、低鈉或 AKI 的診斷。面對新的異常值，仍須先找出相應的檢體方法、採檢時間與尚未測到的生理資訊。

## 第三問｜Cr 上升就代表利尿過多？哪些推論無法從 Lab sheet 得到？

**當檢驗值本身可信時，另一個問題才真正開始：數字改變代表什麼病理生理？** 急性心衰竭病人的 creatinine 上升，就很適合檢驗這個問題。

在急性失代償心衰竭，serum creatinine 可能因多種機轉上升：動脈灌流下降、靜脈鬱血、治療中的血流動力改變、真正腎實質受傷、合併感染或藥物傷害等。[*Acute kidney injury in acute heart failure—when to worry and when not to worry?*](https://pmc.ncbi.nlm.nih.gov/articles/PMC11879425/) 整理了相關臨床研究：**成功去鬱血伴隨的輕度 Cr 變化**，與**持續鬱血合併惡化腎功能**，在研究中的預後關聯並不相同。它不是說「Cr 上升可以忽略」；而是指出，**單看 Cr，無法分辨去鬱血、腎灌流下降及實質傷害**。

[密西根大學住院心衰竭利尿指引 Q18](https://www.ncbi.nlm.nih.gov/books/NBK589894/) 指出：若鬱血尚未解除，治療中 SCr 輕度上升不一定表示應停止利尿；但若同時出現**明顯低血壓、血管內容量不足、尿量惡化或其他 AKI 線索**，便必須重新評估循環狀態與治療反應。這些資訊回答的是不同問題：**Cr 告訴我們腎功能指標變了，鬱血與灌流的證據才能幫助判斷為何改變；單憑一筆 Cr，不能決定停利尿或補液。**

AKI 的診斷本身另有時間維度：請核對 [KDIGO 2012 原始 Table 2（AKI 分期，PDF p.22）](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf#page=22) 的定義，並閱讀 [Figure 4（Stage-based management，PDF p.28）](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf#page=28) 如何將風險分層與腎毒性藥物、容量／灌流、Cr／尿量監測連起來；這張圖不是固定補液或透析處方。KDIGO 要求核對 **48 小時內 SCr ≥0.3 mg/dL 增加、7 天內 ≥1.5 倍基線，或連續至少 6 小時尿量 <0.5 mL/kg/h**。光有「尿量 8 小時總計」不能保證每一個 6 小時區間都符合門檻；光有一筆孤立的 Cr 數值，沒有基線、變化時間與尿量，就不能推得出 CKD、AKI stage 或確切病因。更不能把用於穩態的 eGFR 當成急性變化期間即時的腎臟清除能力。

如果臨床在看完整的 Lab sheet，要分辨的是：

| 檢驗領域 | 該欄實際量到什麼 | 要理解機轉仍缺哪一層證據 |
|---|---|---|
| K／Na／Cl | 電解質檢體濃度與可能的採檢旗標 | 同一時間的檢體類型、血糖/滲透狀態、藥物、心電風險及重驗時序 |
| Serum total CO₂ | 以 bicarbonate 為主的總 CO₂ 量 | 若要談酸鹼障礙，仍欠 pH／PaCO₂、氯及 AG 的同時點資料 |
| BUN／Cr | 代謝物濃度與時間趨勢 | baseline、尿量、循環灌流、鬱血、藥物、尿液與影像 |
| CBC／DC、Hb、platelet | 血球數量和分類 | 感染、出血、稀釋、骨髓或檢體干擾的其他證據；WBC 上升≠感染定論 |
| Mg、Ca、PO₄ | 礦物質濃度 | 心律、症狀、藥物及重複測量；缺乏這些就不能自行設定治療必要性 |

**尚未取得的證據不能由推測補齊。** 若沒有 ECG、尿量、影像或連續檢驗，就只能根據現有資料辨認危急風險與下一個必須釐清的問題，不能替病人假定正常結果或推導出已完成的醫囑。

## 破除過度推論｜把原始研究與個人決策分開

**誤解一：高 K 檢體有溶血，表示患者一定不需要急救。** 錯。溶血增加假性高鉀可能，危險症狀、ECG、快速複查與個體高危條件仍需並行評估；正常 ECG 不是排除真性高鉀的檢查。原始 66 人研究不涵蓋高齡、CKD 和 RAAS 用藥患者。

**急救風險與檢體確認必須並行**，而不是「懷疑假的就一律等」或「看到紅字就無差別給藥」。[UKKA 2026 原始 Figure 4（PDF p.75）](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=75) 將有危險時的心肌保護、鉀轉移、實際排鉀、K／血糖監測及防復發分開；[Table 22（PDF p.98）](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=98) 則提醒 insulin-glucose 後低血糖與反彈監測。原始流程有其適應症與證據強度，不代表每名 K 6.4、ECG 正常者都需要相同 IV calcium、insulin 或補糖量，更不能以本站文章直接替代醫囑。

**誤解二：K 7.8 重抽後 3.6，就等於從未真高鉀。** 不成立。AML 病例的後段樣本有**降鉀介入後**的時序污染，必須回查原始 Table 1 的檢體別及採血方式，不能假裝有無治療的成對試驗。

**誤解三：發現 AKI 就代表利尿藥造成缺水。** AKI 的**定義**不直接提供**病因**。如果患者仍有鬱血、灌流改變或其他腎損傷風險，就必須繼續依血流動力、尿量與治療反應判斷，而不是單憑 Cr 變化停止利尿或給予補液。

**誤解四：CBC、Mg 或 Na 出現紅字，總要配上一條明確醫囑。** 沒有對應臨床症候群、病程、症狀、危險性與測量品質的支持，教材只能呈現**可能機轉與需要查證的訊息**，不能編造使用某藥後的好轉來合理化處置。

## 臨床自我檢核｜三個問題

1. **構念**：實驗室的 K 是病人體內濃度，還是也可能包含檢體外釋放的鉀？AML 原始 Table 1 哪些資訊證明這個問題很重要？
2. **臨床推理**：66 人的低風險研究，為什麼不能幫 70 歲 CKD 心衰竭患者做完整治療決策？2,440 人研究的分母又是誰？
3. **破除推論**：為何「Cr 上升」同時可能見於有效去鬱血和病況惡化？還要補哪些床邊證據，才有資格從生理假說進入治療討論？

[原始病例、研究條件與相關臨床指引](../lab-morning-sheet-sources.md)。**實際採檢與治療**仍須依患者當下的症狀、危急風險、檢驗可信度及醫療機構規範決定；不同患者的數字和研究結果，不能直接代替眼前患者的臨床評估。
