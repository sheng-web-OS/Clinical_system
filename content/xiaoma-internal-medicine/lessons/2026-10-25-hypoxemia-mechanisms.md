# A–a gradient 變大，為什麼還無法診斷 shunt？

<div class="opening-question"><span class="small-label">Respiratory Failure｜圖表三問 · 氧合篇</span><p>PaO₂ 都在 50–60 mmHg：一位是橫膈無力、肺泡氧分壓先下降；另一位正在努力排出 CO₂，肺泡氧分壓仍高，動脈卻嚴重低氧。A–a gradient 如何分開這兩個問題？它又為何不能單獨診斷肺炎、擴散障礙或右向左分流？</p></div>

《Pocket Medicine》第九版 PDF 第 105 頁 **Figure 2-5：Workup of acute hypoxemia**，其實連續進行三項生理判斷：肺泡裡原本可提供多少氧、血液為什麼沒有拿到預期的氧、增加 FiO₂ 為什麼有時不能讓動脈氧合恢復。本篇用三個可追溯的病例和原創機轉圖展開這些判斷；保留病例原始觀察與本篇估算的差別。先閱讀[基礎篇的 SpO₂／PaO₂／CaO₂ 與換氣定義](2026-10-21-hypoxemia.md#part-1)，再進入以下深究也可以。

## 第零問｜A–a gradient 到底比較了哪兩個位置？

肺泡氧分壓 **PAO₂** 通常由吸入氧分壓和 CO₂ 估算；動脈氧分壓 **PaO₂** 由 ABG 實測。兩者的差 **PAO₂ − PaO₂** 回答「動脈血為什麼沒有達到肺泡預期的氧分壓」。它不是擴散速率，也不是血液攜氧量，更不能直接推出哪一個肺區有病。

<div class="equation"><strong>PAO₂ ≈ FiO₂ × (PB − 47) − PaCO₂/R</strong><strong>A–a gradient = PAO₂ − PaO₂</strong><small>PB 是大氣壓、FiO₂ 是吸入氧濃度、R 是呼吸商。海平面、室內空氣、R 約 0.8 時，PAO₂ ≈ 150 − PaCO₂/0.8；式中的 PAO₂ 是由假設估算，不是直接抽取肺泡氣體測得。</small></div>

這個比較之所以有用，是因為 **hypoventilation 會先使 PaCO₂ 增加，再依肺泡氣體方程式使 PAO₂ 降低**。PaO₂ 跟著降低可以不需要額外交換障礙。相反地，PaCO₂ 偏低表示病人正在相對增加 CO₂ 排出；若 PaO₂ 仍低，更應解釋肺泡到動脈之間的落差。

## 第一問｜兩個 PaO₂ 都很低的真實患者，為什麼 A–a 的結論相反？

先看原始病例，**不要先算公式**。

**病例甲：87 歲男性。** Reddy 與 Josephson（2014）報告一名反覆高碳酸呼吸衰竭的病人。室內空氣 ABG：pH **7.33**、PaCO₂ **53**、PaO₂ **64** mmHg，原作者報告 A–a **18** mmHg。他曾有反覆意識改變、上肢神經學異常；床邊出現吸氣時腹部反而內凹，胸片呈雙側橫膈抬高。平躺的 FVC 比坐姿**下降 22%**；最大吸氣／呼氣壓力也下降。神經檢查、肌電與頸椎影像最後支持頸椎 C3–C5 區域的病變牽涉膈神經根。[原病例全文](https://doi.org/10.1186/1752-1947-8-401)。

**病例乙：35 歲男性。** Li 等人（2026）描述從事含銦錫氧化物粉塵回收的工人。室內空氣 ABG：pH **7.41**、PaCO₂ **33**、PaO₂ **54** mmHg，原文 A–a **59.2** mmHg。HRCT 有雙側 ground-glass opacity、interlobular septal thickening，DLCO 約為預測值 **26%**。組織病理與含銦暴露證據支持 secondary pulmonary alveolar proteinosis（PAP）。經 whole-lung lavage 後部分指標改善，但後續仍有纖維化進展。[原始 Figure 1 病程、Figure 2 HRCT 與 Table 1 肺功能](https://doi.org/10.3389/fmed.2026.1856204)。

<figure id="oxygen-locations" class="diuretic-figure">
<div class="diuretic-figure-head"><span>FIGURE 01 · CASE-BASED A–a</span><strong>PaO₂ 相近，肺泡氧起點卻不同</strong></div>
<div class="diuretic-svg-scroll" role="region" tabindex="0" aria-label="87 歲與 35 歲真實病例的 PaO2 與推估 PAO2 比較，可水平捲動">
<svg xmlns="http://www.w3.org/2000/svg" width="760" height="378" viewBox="0 0 760 378" role="img" aria-labelledby="aagrad-title aagrad-desc">
<title id="aagrad-title">相近的動脈氧分壓，對應不同的肺泡動脈差距</title>
<desc id="aagrad-desc">87歲病例PaCO2 53、PaO2 64，海平面模型肺泡氧84，差約20，原文18；35歲病例PaCO2 33、PaO2 54，模型肺泡氧109，差約55，原文59.2。</desc>
<rect x="0" y="0" width="760" height="378" fill="#f8fbfa"/>
<g font-family="sans-serif" fill="#26433f">
<text x="30" y="35" font-size="18" font-weight="700">室內空氣 · 海平面近似式：PAO₂ ≈ 150 − PaCO₂/0.8</text>
<text x="30" y="81" font-size="17" font-weight="700">87 歲 · 呼吸泵不足</text>
<text x="30" y="107" font-size="14">PaCO₂ 53 → PAO₂ 約 84</text>
<text x="30" y="188" font-size="17" font-weight="700">35 歲 · 肺泡交換障礙</text>
<text x="30" y="214" font-size="14">PaCO₂ 33 → PAO₂ 約 109</text>
<text x="30" y="330" font-size="13">深藍：實測 PaO₂　 橘色：預期肺泡與動脈落差</text>
<text x="30" y="355" font-size="12">原文 A–a 分別為 18、59.2；圖為標準大氣壓假設下的教學重算。</text>
</g>
<rect x="30" y="117" width="384" height="33" rx="4" fill="#286f96"/><rect x="414" y="117" width="120" height="33" rx="4" fill="#dca15f"/>
<rect x="30" y="224" width="324" height="33" rx="4" fill="#286f96"/><rect x="354" y="224" width="330" height="33" rx="4" fill="#dca15f"/>
<g font-family="sans-serif" font-weight="700" font-size="14"><text x="206" y="139" fill="#fff">PaO₂ 64</text><text x="437" y="139" fill="#382914">A–a ≈ 20</text><text x="167" y="246" fill="#fff">PaO₂ 54</text><text x="477" y="246" fill="#382914">A–a ≈ 55</text></g>
<line x1="30" y1="290" x2="690" y2="290" stroke="#63817e"/><g font-family="sans-serif" font-size="12" fill="#4e6e6a"><text x="30" y="309">0</text><text x="260" y="309">40</text><text x="500" y="309">80</text><text x="658" y="309">110 mmHg</text></g>
</svg></div>
<figcaption><strong>圖 1｜先問肺泡的氧起點，再問額外落差。</strong>病例原始數值分別來自 Reddy 2014 與 Li 2026；橘色區塊是根據 **相同海平面模型**重算的差值，不是原研究提供的實測圖。87 歲患者原文 18、此處約 20；35 歲原文 59.2、此處約 55，作者使用的大氣壓／氣體條件未完全重現，不硬說兩者相等。不是 Pocket Medicine 原圖複製。<a href="../respiratory-deep-dive-sources.md#pocket-hypoxemia">對照 Figure 2-5 與計算限制</a>。手機可左右滑動。</figcaption>
</figure>

**病例甲的決策變化：** 87 歲時，原書 age/4 + 4 粗估約 26 mmHg，A–a 18 未必異常。這使「低通氣導致肺泡氧下降」合理，但不會直接確診橫膈無力。真正讓病因從肺部氧合移向呼吸泵的，是**仰臥 FVC 下降、paradoxical abdominal motion、最大呼吸肌壓力下降及頸椎神經學證據**。胸片仍有積液或肺鬱血等其他問題，不能誤寫成「肺一定完全正常」。患者後來心衰肺水腫，也再度增加受損呼吸泵的負荷。

**病例乙的決策變化：** PaCO₂ 33 並不高，肺泡預期仍有相對充足的氧，但實際 PaO₂ 只有 54。A–a 擴大只能將問題指向**額外的氧合障礙**。是 HRCT、DLCO、病理、暴露史與檢體證據，才逐步建立 PAP 及相關職業肺病。DLCO 很低，不等於已經測出「肺泡膜擴散速率」或證明這名患者所有低氧都由 diffusion limitation 單獨造成；部分肺泡填充也會形成 low V/Q 或 shunt-like 單位。

至此，A–a 已經幫我們把兩條診斷路徑分開，但仍沒有辦法在病例乙內部量出 V/Q mismatch、true shunt 或 diffusion 各占多少。這正是下一問要處理的事情。

## 第二問｜為什麼給 100% O₂，能改善 low V/Q，卻不一定克服 true shunt？

**V 是肺泡通氣量（alveolar ventilation），Q 是肺血流量（perfusion）。**真實肺臟是一群並聯的肺單位。Low V/Q 表示氣體有到，但相對於血流太少；**V/Q = 0** 是一端完全沒有通氣但仍有血流的 true shunt。反過來，有通氣卻完全無血流的區域，是 alveolar dead space 的極端。前者使血流未充分氧合，後者浪費通氣，兩者的危險並不等價。

<figure id="vq-spectrum" class="diuretic-figure">
<div class="diuretic-figure-head"><span>FIGURE 02 · VENTILATION × PERFUSION</span><strong>同樣是「異常肺泡」，流過的血並不一樣</strong></div>
<div class="diuretic-svg-scroll" role="region" tabindex="0" aria-label="三個肺泡與下方血流通道示意，可水平捲動">
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="325" viewBox="0 0 800 325" role="img" aria-labelledby="vq-title vq-desc">
<title id="vq-title">正常肺區、低 VQ 與完全分流的通氣血流配對</title><desc id="vq-desc">三個肺泡都與血流平行排列，正常肺區通氣多而血流完整，低VQ通氣減少血流完整，true shunt 完全沒有通氣仍有血流。只有低VQ仍可被提高吸入氧濃度直接補到肺泡。</desc>
<rect width="800" height="325" fill="#f8fbfa"/>
<g font-family="sans-serif" fill="#27463f" text-anchor="middle"><text x="134" y="30" font-size="19" font-weight="700">相對正常</text><text x="400" y="30" font-size="19" font-weight="700">Low V/Q</text><text x="668" y="30" font-size="19" font-weight="700">True shunt</text></g>
<g fill="#e3f0f6" stroke="#3688ab" stroke-width="4"><circle cx="134" cy="122" r="57"/><circle cx="400" cy="122" r="57" fill="#f4eee3" stroke="#c18b43"/><circle cx="668" cy="122" r="57" fill="#f6dede" stroke="#bc6464"/></g>
<g stroke="#3688ab" stroke-width="11" stroke-linecap="round"><line x1="134" y1="51" x2="134" y2="88"/><line x1="400" y1="57" x2="400" y2="76" stroke="#c18b43" stroke-width="5"/></g>
<line x1="668" y1="54" x2="668" y2="81" stroke="#bc6464" stroke-width="11"/><line x1="654" y1="68" x2="682" y2="68" stroke="#bc6464" stroke-width="6"/>
<g stroke="#ab5454" fill="none" stroke-width="11" stroke-linecap="round"><path d="M74 211 Q134 250 194 211"/><path d="M340 211 Q400 250 460 211"/><path d="M608 211 Q668 250 728 211"/></g>
<g stroke="#2a86a7" fill="none" stroke-width="7" stroke-linecap="round"><path d="M137 243 Q163 240 193 211"/><path d="M433 237 Q449 226 458 211" stroke="#b9a46c" stroke-width="4"/></g>
<g font-family="sans-serif" fill="#27463f" text-anchor="middle"><text x="134" y="131" font-size="15">O₂ 可進入</text><text x="400" y="131" font-size="15">O₂ 較少</text><text x="668" y="131" font-size="15">O₂ 無法進入</text><text x="134" y="277" font-size="14">Q 保留 · 氧合充分</text><text x="400" y="277" font-size="14">Q 保留 · 可改善</text><text x="668" y="277" font-size="14">Q 保留 · 反應受限</text></g>
<text x="400" y="309" text-anchor="middle" fill="#566f68" font-size="13">上方管道＝通氣；下方紅色弧線＝仍存在的血流；示意非解剖比例圖</text>
</svg></div>
<figcaption><strong>圖 2｜只有仍能通氣的低 V/Q 肺泡，才能直接接受提高的 FiO₂。</strong>此圖是原創肺單位示意，取代單純文字分類卡，並非 Pocket Medicine Figure 2-5 翻拍；真實肺炎可同時包含這三類及 high V/Q 區域。只用來辨認氧氣能否到達該單位，不按圖估算 shunt fraction。</figcaption>
</figure>

為什麼剩下的好肺不能替 shunt 血液完全補氧？答案不在於把不同肺區的 PaO₂ 直接平均。血液混合的是**氧含量 CaO₂**：

<div class="equation"><strong>CaO₂ ≈ 1.34 × Hb × SaO₂ + 0.003 × PaO₂</strong><small>Hb（g/dL）、SaO₂（0–1）、PaO₂（mmHg）；結果約為 mL O₂/dL blood。好肺的 Hb 通常已接近全飽和，不能變成 120% 以補償沒有被氧合的血。</small></div>

如果設計一個**純計算示範**：80% 血液離開正常肺區時 Hb 飽和度 100%，20% 完全未氧合的分流血液仍為 SvO₂ 70%，假設 Hb 相同且暫忽略溶解氧，混合後約為 94%。這不是任何病例的實測，也不允許反過來用 94% 直接算出真實的 shunt fraction。

小麻所寫「true shunt cannot be overcome with 100% O₂」應理解為**增加 FiO₂ 的效果受限**，不是動脈氧合絕對不改善。因為好肺內**溶解氧**仍可隨 PaO₂ 上升而增加，只是 Hb 結合氧已接近平台。分流血液的氧含量又受到混合靜脈血 **Cv̄O₂** 影響：若同樣 shunt fraction、但休克使混合靜脈血氧更低，最後的動脈氧合也可能更差。

<div class="equation"><strong>Qs/Qt = (Cc′O₂ − CaO₂) / (Cc′O₂ − Cv̄O₂)</strong><small>Cc′O₂＝理想肺微血管末端氧含量、CaO₂＝動脈氧含量、Cv̄O₂＝混合靜脈氧含量。這是分流估算的生理概念式，需要真正的含氧量及模型條件，不能把兩處 SpO₂ 差額直接當成 Qs/Qt。</small></div>

### 真實病例｜肺靜脈 97%，左心房卻剩 83%：哪一段血液被混入？

Allaham 等人（2025）報告一名 **80 歲男性**，跌倒肋骨骨折後有難治性低氧。疼痛造成淺呼吸原本是合理假說，但在高濃度氧支持下 SpO₂ 仍偏低，CTA 未發現能充分解釋低氧的肺栓塞或嚴重肺實質病變。Bubble echocardiography 顯示有右向左的心房層級分流，坐起來更明顯；心內超音波確認 **PFO**。

最有辨識力的是介入時的採血位置：**肺靜脈氧飽和度 97%，左心房氧飽和度 83%**。流出肺的血本來已充分氧合，到了左心房卻被低氧血拉低；這讓「氧氣不能通過肺泡」轉成「一股靜脈血繞過肺循環直接混進左房」的解釋。封堵 PFO 後無殘餘氣泡分流，次日室內空氣 SpO₂ **98%**。[原始病例 Figure 1–3 與介入前後敘述](https://doi.org/10.3389/fcvm.2025.1715242)。

<figure id="pfo-mixing" class="diuretic-figure">
<div class="diuretic-figure-head"><span>FIGURE 03 · SAMPLING LOCATION</span><strong>不是 A–a 97−83；而是同一個人的兩處血氧飽和度</strong></div>
<div class="diuretic-svg-scroll" role="region" tabindex="0" aria-label="PFO 病例的肺靜脈、右心房與左心房血流路徑，可水平捲動">
<svg xmlns="http://www.w3.org/2000/svg" width="760" height="294" viewBox="0 0 760 294" role="img" aria-labelledby="pfo-title pfo-desc">
<title id="pfo-title">肺靜脈氧合血與 PFO 分流血混入左心房的路徑</title>
<desc id="pfo-desc">肺靜脈取樣氧飽和度97%，右心側靜脈血經PFO直接分流進入左心房，左心房氧飽和度83%。封堵後次日室內空氣指尖血氧98%。這些是不同部位或時間的量測，不能直接算分流百分比。</desc>
<rect width="760" height="294" fill="#f8fbfa"/>
<g font-family="sans-serif" text-anchor="middle"><rect x="24" y="52" width="213" height="115" rx="16" fill="#e0eff7" stroke="#428dad" stroke-width="2"/><text x="130" y="87" font-size="18" fill="#24485d" font-weight="700">肺靜脈</text><text x="130" y="125" font-size="28" fill="#175c86">97%</text><text x="130" y="149" font-size="12" fill="#385b6d">原文採血飽和度</text>
<rect x="522" y="52" width="213" height="115" rx="16" fill="#f4e3d6" stroke="#c17d55" stroke-width="2"/><text x="630" y="87" font-size="18" fill="#6a4029" font-weight="700">左心房</text><text x="630" y="125" font-size="28" fill="#a25e34">83%</text><text x="630" y="149" font-size="12" fill="#775545">原文採血飽和度</text>
<rect x="280" y="200" width="200" height="67" rx="14" fill="#f4dee0" stroke="#be7377" stroke-width="2"/><text x="380" y="226" font-size="17" font-weight="700" fill="#75373f">右心房 → PFO</text><text x="380" y="251" font-size="14" fill="#75373f">靜脈血右向左分流</text>
</g>
<path d="M237 110 H514" stroke="#287ca0" stroke-width="14" fill="none"/><path d="M503 100 L520 110 L503 120" fill="none" stroke="#287ca0" stroke-width="6"/>
<path d="M454 200 Q515 189 555 154" stroke="#c66c71" stroke-width="13" fill="none"/><path d="M542 157 L560 150 L556 168" fill="none" stroke="#c66c71" stroke-width="6"/>
<text x="379" y="87" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#28607f">已氧合血</text>
<text x="380" y="22" text-anchor="middle" font-family="sans-serif" font-size="15" fill="#35514c">封堵後：次日室內空氣 SpO₂ 98%</text>
</svg></div>
<figcaption><strong>圖 3｜抽血位置回答的是血液從哪裡被混入。</strong>97% 和 83% 是原病例兩處血氧飽和度，不是肺泡－動脈氧分壓，也不能直接相減求 A–a 或分流比例。流程箭頭是病理生理示意，不暗示個案測得 PFO 通量；原文影像請參看 <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC12719297/">Figure 1–3</a>。</figcaption>
</figure>

2026 年 Kakura 等人另有一例直立 SpO₂ **80–83%**、仰臥 **95–99%** 的姿勢性分流，坐姿 TEE 比平躺更能看見 PFO 右向左流。這補上另一個維度：**同一患者的 shunt fraction 可因姿勢改變，而非影像上的肺泡填充突然改變**。[原始 Visual Summary](https://doi.org/10.1016/j.jaccas.2026.107626)。兩例都不能推論所有 PFO 有臨床危險或一律需要封堵。

## 第三問｜為什麼肺炎、ARDS、PE、ILD 沒有一對一對應的 A–a 分類？

肺炎與肺水腫中，有些肺泡還能吸入少量氣體（low V/Q），有些完全塌陷而血流保留（true shunt），也有仍保留交換的肺區。這解釋為什麼 **pneumonia** 同時出現在 Pocket Medicine 的 V/Q mismatch 和 shunt 欄：疾病名描述病灶，V/Q 描述**每個肺單位在該時刻**的生理。

提高 FiO₂ 主要增加仍有通氣之肺單位的 PAO₂；適當 PEEP 則可能打開可復張的塌陷肺泡，使一些 V/Q≈0 的肺單位重新變成 V/Q>0。因此兩者不能當成同一種氧合治療。但過高 PEEP 可造成過度擴張、靜脈回流或肺灌流下降，必須看呼吸力學與循環，不能把更高 PEEP＝更多 recruitment 當成定律。

PE 的高 V/Q／dead-space 單位，是通氣到不了血流的地方，**不會直接流出一股低氧血**；低氧更可能涉及血流重新分配後的 low V/Q、混合靜脈氧下降及特定分流。PaCO₂ 仍可因呼吸代償而正常或降低。

ILD 的運動低氧也不等於證明單一 diffusion limitation。肺微血管內氧分壓平衡有時間限制，運動可能縮短紅血球通過時間；但 ILD 同時常有 V/Q 異常、微血管床減少及較低混合靜脈氧。DLCO 的下降又受到膜、血液容積與 Hb 共同影響。這就是 Li 病例不能單憑 DLCO 26% 把全部低氧都標成 diffusion 的原因。

| 當下資料 | 它回答的事 | 它還不能回答的事 |
| --- | --- | --- |
| 已知室內空氣 ABG、A–a 正常 | 肺泡氧起點下降可解釋相當部分低氧 | 不能排除共存的肺部疾病，也不能直接診斷中樞／橫膈原因 |
| A–a 明顯擴大 | 有額外肺泡至動脈的氧合落差 | 不能單獨選定 V/Q、shunt、diffusion |
| 增加 FiO₂ 仍低氧 | 對補氧反應受限，應考慮分流與嚴重複合肺病 | 不能直接算 shunt fraction，更不是常規要求危急患者做 100% O₂ challenge |
| PV 97%、LA 83%＋bubble study | 支持心房層級的低氧血混合 | 不是 PAO₂−PaO₂；仍需因果評估與適當介入選擇 |
| 活動才低氧、DLCO 低 | 氣體轉移／V/Q 或肺循環儲備可能不足 | 不能由一個 DLCO 值確診單純膜擴散障礙 |

**結語。** A–a 是第一個定位問題，不是最後的病名。下一步真正要問的是：**血液流過了哪些肺單位？哪些血流根本沒有接觸到提高的氧氣？已氧合與未氧合的血如何混合？**最後再用影像、血氧採樣位置、病史和治療前後的證據，決定下一步是否合理。若病人已嚴重低氧，必要的氧療與呼吸支持不能因等待診斷計算而延誤。

[接續：RR 40/min，為什麼 PaCO₂ 仍上升？](2026-10-25-hypercapnia-physiology.md)・[回到原有低血氧整合篇與國考題](2026-10-21-hypoxemia.md)・[病例原文、圖說及本篇審查範圍](../respiratory-deep-dive-sources.md)
