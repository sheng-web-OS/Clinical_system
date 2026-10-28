# 早晨一張 Lab sheet（第一篇）：先確認數字是否真的代表病人

一張化驗單最危險的錯誤，有時不是不知道高血鉀怎麼治療，而是把**試管裡發生的變化**誤認成**病人體內發生的變化**。然而反過來，只因懷疑檢體失真就延後必要的急症處置，也同樣危險。

這個難題在 2024 年一名急性骨髓性白血病（AML）患者的急診病程中，並非抽象考題：同一天，他的 K 從 3.0、6.7、7.8 變成 3.6 mEq/L；而最後一次抽血前，團隊已經開始治療高血鉀。要理解這四個數字，必須先還原病人為何到急診、每次檢體怎麼取得、醫師當時知道什麼，以及哪些證據其實無法分離。

## 第一問｜這個人為什麼來急診？在 K 7.8 出現前，哪些事已經發生？

Cao 於 *International Journal of Emergency Medicine*（2024）記錄一位 **55 歲男性**。他先前罹患多發性骨髓瘤，經骨髓增生不良症候群演變為 AML；病況惡化，周邊血液充滿 blasts。4 月 2 日，他曾因血鉀 **2.8 mEq/L** 在門診接受 **40 mEq 靜脈補鉀**；平時也有口服鉀補充及治療腎上腺功能不足的藥物。[Cao 原始病例、Case presentation 與 Table 1](https://link.springer.com/article/10.1186/s12245-024-00734-x)（[PMC 開放全文與原表](https://pmc.ncbi.nlm.nih.gov/articles/PMC11462689/)）。

4 月 3 日中午，居家護理採血測得 **Hb 4.5 g/dL**（兩天前 7.5）及 **K 3.0 mEq/L**。原本讓他被送到急診的理由是**疑似嚴重貧血，需要輸血**，不是高血鉀。到急診時，原文描述生命徵象穩定，沒有急性不適；但院內 CBC 顯示 **WBC 206.8 × 10³/µL，90% blasts，Hb 7.9 g/dL，platelets 38 × 10³/µL**。

第一個資訊衝突其實是 Hb：幾小時內從 4.5 變 7.9，沒有記錄能解釋這種幅度的生理恢復。作者認定居家 4.5 為錯誤結果；但原文沒有交代其確切干擾機轉，因此不能因為它和 K 發生在同一人，就推說兩者都是白血球裂解造成。**病人確實有 AML 與貧血；其中一個 Hb 數字不可靠，不等於整張 CBC 都是假的。**

真正改變急診優先問題的，是隨後出現的 **K 6.7**，再次採血甚至達 **7.8 mEq/L**。在尚未知道最後一筆結果前，醫師不能直接宣布這是「檢驗誤差」。

## 第二問｜高血鉀與假性高血鉀，當時各有哪些合理機轉？

血鉀檢驗量的是**送到分析儀時檢體中的鉀濃度**。這個值常可反映體內血鉀，前提卻是採樣後的細胞完整性、採血管、運送與分析步驟沒有造成足以影響結果的偏差。細胞內鉀濃度遠高於細胞外；如果細胞離開人體後才破裂，分析儀照樣會量到被釋出的鉀。這是 *in-vitro* 假性升高，不等於病人體內已經高血鉀。

**先考慮真實的體內升高。** 此人前一天剛接受補鉀；若有體內細胞破壞、鉀排泄能力改變或其他電解質移動，也可能造成血鉀真的增加。AML 的極高腫瘤負荷使細胞破壞相關問題需要被想到，但「有 AML」本身並不證明發生 tumor lysis syndrome。原病例報告 BUN **9 mg/dL**、Cr **1.2 mg/dL**、磷 **2.6 mg/dL**、尿酸 **4.7 mg/dL**；這些是當時可用的背景訊息，仍欠缺完整基線、連續趨勢、尿量與其他條件，不能單憑其中一筆排除所有急性體內變化。

**再考慮離體造成的假性升高。** 紅血球溶血、脆弱白血球受機械運送破壞、血小板在 serum 凝血過程釋鉀，都可能讓測得的 K 高於循環中的濃度。機轉並不相同：白血病細胞在氣送管運送時受損，未必會呈現典型的紅血球溶血訊號；血小板相關問題則要注意 serum 與 anticoagulated plasma 的差異。當 WBC 高達 **206.8 × 10³/µL**，這些原本可忽略的檢體條件忽然變成核心鑑別資訊。

關鍵不是把「真」與「假」視為二選一的最終標籤，而是問：**下一筆什麼證據，能把體內變化與運送造成的變化區分開？**

### 四次檢體並不是同一種實驗

| 4 月 3 日採檢 | K（mEq/L） | 當時真正不同的條件 |
|---|---:|---|
| A，12:00 | **3.0** | 居家採血；lithium-heparin **plasma**，courier／步行；Beckman Coulter 分析 |
| B，20:03 | **6.7** | 急診 **whole blood**，**氣送管**；NovaBiomedical 分析 |
| C，20:48 | **7.8** | 再次採取 whole blood，**仍經氣送管**，同類分析儀 |
| D，23:37 | **3.6** | whole blood **改由人員步行送檢**；但抽血時**已接受降鉀治療約 30 分鐘** |

從 A 到 B，不只運送方式改變，連 **plasma／whole blood 和分析儀**也不同。因此不能把兩者差距全部看成病人體內 K 上升。

B 到 C 的問題更有教學意義：重抽確實可以排除某些偶發採樣錯誤，但如果第二次檢體仍走過**相同的氣送管**，它並沒有驗證「氣送管會不會破壞脆弱血球」這個假說。**重抽是再取得一個數值；改變可能的干擾條件，才是在測試機轉。**

D 結果回到 3.6，是支持假性高血鉀的重要線索，卻仍有一個不可忽略的混雜：團隊已經治療。從 C 到 D 同時發生**運送改變**與**治療作用**，不能把 7.8 → 3.6 的全幅下降歸功於改成步行送檢。原作者結合極高 WBC、不同送檢程序與後續調查，認為氣送管造成假性高血鉀；這是合理的病例判讀，但不是控制其他變項的因果試驗。

## 第三問｜既然懷疑檢體是假，急診為何仍然治療？

當團隊看到 K 6.7、接著 7.8 時，病人沒有典型高血鉀症狀，ECG 也沒有相應改變。這些是**降低某些當下危險線索的資訊**，並不是能排除危急高血鉀的陰性檢查。高血鉀可能在沒有典型 ECG 改變時仍有嚴重後果；反之，對假性高血鉀給予移鉀治療，可能使真實血鉀降得過低。

原報告記載急診給予 **IV calcium gluconate、insulin/dextrose、sodium bicarbonate 與吸入 albuterol**，並會診腎臟科評估是否需要透析。這裡必須把「**團隊實際做了什麼**」與「**今天應給每個類似患者什麼處方**」分開。這份病例無法證明所有藥物在當時均屬必要，也不能因最後判斷是假性高鉀，就用後見之明斷言初始防範致命心律不整完全不合理。

在病人真正有立即心臟危險時，查核假性高鉀與急症評估／處理須**並行**，不能為了證明檢體有錯而放棄救治。當臨床狀態與數值高度矛盾、又有極高白血球時，應盡快與檢驗部門合作，使用合適、避免機械損傷的送檢與分析方法取得**真正能回答疑問的新證據**；同時監測血鉀及治療相關低血糖、反彈等風險。具體治療與監測應依個別病人和當地流程參照 [UK Kidney Association 2026 急性高血鉀指引](https://www.ukkidney.org/health-professionals/guidelines/treatment-acute-hyperkalaemia-adults-0)。當需要比較心肌保護、暫時移鉀、真正移除與監測這些不同目標時，應直接閱讀其[原 Figure 4（PDF p.75）](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=75)及[原 Table 22（PDF p.98）](https://www.ukkidney.org/sites/default/files/documents/FINAL%20VERSION%20-%20UKKA%20CLINICAL%20PRACTICE%20GUIDELINE%20-%20MANAGEMENT%20OF%20HYPERKALAEMIA%20IN%20ADULTS%20-%20UPDATED%20JULY%202026_0.pdf#page=98)。它們是按臨床情境使用的原指引，不是由這個病例推得、可以原樣複製的個人處方。

腎臟科醫師曾建議以 heparinized plasma 重新確認；作者事後查明，院內的急診檢體本來就用了 lithium-heparin 管。**再次指定抗凝方式不等於已經排除氣送管的機械傷害**，這正是問題定位必須精確到「採樣—運送—處理—測定」各環節的原因。

原文接著記載：團隊確認 K 正常後輸注一單位 packed RBC，患者選擇舒適照護，翌日生命徵象穩定出院，一週後過世。後續死亡不能從這份報告歸因於假性高血鉀或降鉀治療。真正值得追問的系統問題，是醫院原有「WBC 過高需警示 Chemistry 並避免氣送管」的人工提醒**那晚未能傳遞成功**；作者事後向當班人員查證，才釐清這個失效點。只看到某次正確檢驗結果，不代表流程原本就在正常運作。

## 把病例帶回臨床：另外兩條機轉，為什麼不能照抄 AML 的解法？

若病人不是白血球極高，而是血小板極高，可能出現不同的 *pseudohyperkalemia*。Šálek（2018）記載一位 **62 歲 essential thrombocythemia** 患者，platelets **1305 × 10⁹/L**，serum K **6.3**，plasma K **4.6**，動脈全血分析 **3.4 mmol/L**。Serum 在凝血過程中可能因大量血小板釋鉀而升高；這與 AML 案例的**氣送管機械傷害**不同。三份血也有不同採樣部位與分析條件，不能將全部差距直接算成血小板釋鉀量。[Šálek 真實病例與原表](https://pmc.ncbi.nlm.nih.gov/articles/PMC5806620/)。

再把視野移到一般急診：Stephan 等人（2025）分析 **2,440 位初次 K ≥5.0 且當天確實重測**的病人，**864 位（35%）**重測正常，而其中 **597 位（597/864，69%）**的第一次檢體有溶血證據。這不是「所有急診高鉀都有 35% 是假的」，因為只選進**當天有重測**的患者；也不是「有溶血便可不重抽」。另一項 Wilson 等人（2020）的 **66 人低風險**研究排除了高齡、腎功能不佳、血液惡性疾病及部分相關藥物族群，不能搬來保證這名 AML 患者安全。[Stephan 原始研究](https://pmc.ncbi.nlm.nih.gov/articles/PMC11908522/)；[Wilson 原始研究](https://pmc.ncbi.nlm.nih.gov/articles/PMC7673871/)。

這些研究沒有取代先前病例的推理，而是幫忙界定**何種病人、何種重抽程序和何種推論才有研究支持**。以下圖表把病例檢體時序與研究的分母並排；上圖回答「為何這幾次 K 不可直接比」，下圖回答「研究中究竟觀察了哪些病人」。

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

## 回到這張 Lab sheet：真正得到的三種能力

第一次看到極端 K 值時，先辨認**病人是否可能立即有危險**；危險評估不能因為數字看似不合常理而停止。接著把至少兩條競爭路徑分開：**體內鉀真的變了**，還是**採血後的檢體變了**；兩者可同時存在，不能靠單次 ECG 或一次重抽定論。最後選擇能區分路徑的證據：不是無目的重複抽血，而是檢查標本類型、極端 CBC、溶血訊號、氣送管／手送、儀器、治療時間與後續動態。

晨間 Lab 的其他項目也同樣要先確認「測到什麼」；例如 Hb 可能有檢驗矛盾，Cr 需要基線與尿量才能討論腎功能趨勢。但它們各有不同的病理生理和臨床問題，不能因為出現在同張化驗單，就把另一個心衰竭病人的 AKI 敘事拼進 AML 病程。**Cr 上升與去鬱血的競爭機轉應在有相應真實病例及循環資料的獨立教材完整推導**。

這是本系列第一篇只解決的問題：**臨床推理從確認資料是否真的描述病人開始；而資料可疑，也不能成為忽略病人安全的理由。** 其他檢驗領域的延伸資料和原始圖表來源可從[原始來源與適用界線](../lab-morning-sheet-sources.md)繼續查閱。
