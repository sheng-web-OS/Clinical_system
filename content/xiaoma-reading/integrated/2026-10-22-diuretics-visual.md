# 利尿效果不夠，為什麼下一步不一定是加量？

*小麻閱讀 9E｜以 2026.07.20 原稿為論證主軸，補入來源定位與原創圖解。*

閱讀 diuretics，很容易將不同藥物排成一條由弱到強的直線。

Potassium-sparing diuretics 只影響 collecting duct 少量的 sodium reabsorption；thiazide 作用在 DCT；loop diuretics 則阻斷 thick ascending limb 的 NKCC2，而這個區段原本負責回收約四分之一的 filtered sodium，看起來最強。

小麻後面的處置流程也像沿著這條直線向上：先使用 oral loop，反應不足便加入 thiazide，再改成 IV loop 或 continuous infusion。

依照這個順序，利尿治療似乎只是強度問題。水腫越嚴重，就需要更強的藥；尿量不夠，就繼續增加劑量。

但臨床上的利尿反應並不隨劑量等比例增加。

同一位病人使用 40 mg furosemide，可能幾乎沒有反應；增加到 80 mg 後，尿量卻突然明顯上升。可是當 80 mg 已經有效，再增加到 160 mg，尿量不一定跟著加倍。有時增加給藥頻率，比提高單次劑量更有效；有時加入原本看起來較弱的 thiazide，反而能重新產生明顯的 natriuresis。

## 藥物真正抵達作用位置之前，增加劑量不會帶來線性效果

同一顆藥，為什麼會先像完全無效，跨過某個劑量後才突然有效？

Loop diuretic 進入血液，還不等於抵達作用位置。藥物必須先到達腎臟，經 proximal tubule 分泌進入 tubular lumen，再從管腔側阻斷 NKCC2。

低劑量時，藥物可能已經進入管腔，有效濃度卻仍不足以抑制足夠的 sodium transport，因此尚未形成臨床上可測得的 natriuresis。等到管腔內濃度跨過某個界線，dose–response curve 才迅速變陡。

這個反應開始明顯出現的界線，就是 threshold。

因此，初始劑量無效時，只增加一點劑量，可能仍停留在 threshold 以下；將 dose 加倍，則比較可能真正進入有效區。

但有效區也有盡頭。

當可進一步抑制的 sodium transport 已所剩無幾，單次劑量便逐漸接近 ceiling。此後繼續加量，很難再提高 peak natriuresis；即使總效果仍略有增加，也主要來自濃度高於 threshold 的時間延長，而不是 peak 持續上升。

Threshold 使加倍劑量變得合理；ceiling 則說明為什麼加量不能無限延伸。

<figure class="diuretic-figure" id="loop-dose-response">
<div class="diuretic-figure-head"><span>FIGURE 01 · PHARMACODYNAMICS</span><strong>同一種 loop，劑量增加為何不等於排鈉等比例增加？</strong></div>
<div class="diuretic-svg-scroll" role="region" aria-label="利尿劑劑量反應曲線，可水平捲動">
<svg viewBox="0 0 760 400" width="760" height="400" role="img" aria-labelledby="dose-curve-title dose-curve-desc" xmlns="http://www.w3.org/2000/svg">
<title id="dose-curve-title">Loop diuretic 的 sigmoid 排鈉反應曲線示意圖</title>
<desc id="dose-curve-desc">管腔內有效藥物暴露偏低時，排鈉幾乎無反應；跨越 threshold 後反應迅速增加；接近 ceiling 後再加量，峰值效應增加有限。這是定性示意，並非劑量計算表。</desc>
<rect x="0" y="0" width="760" height="400" fill="#f8fbf9"/>
<rect x="94" y="56" width="610" height="248" fill="#fff" stroke="#dce8e3"/>
<path d="M94 56 V304 H704" stroke="#2c4543" stroke-width="2.6" fill="none"/>
<line x1="255" y1="56" x2="255" y2="304" stroke="#b47e43" stroke-dasharray="6 6" stroke-width="2"/>
<line x1="551" y1="56" x2="551" y2="304" stroke="#a46b55" stroke-dasharray="6 6" stroke-width="2"/>
<path d="M105 290 C175 290 209 285 246 266 S314 146 393 105 S535 76 688 76" stroke="#0a7770" stroke-width="5" fill="none" stroke-linecap="round"/>
<circle cx="255" cy="261" r="7" fill="#b47e43" stroke="#fff" stroke-width="2"/>
<circle cx="551" cy="78" r="7" fill="#a46b55" stroke="#fff" stroke-width="2"/>
<text x="128" y="248" font-size="18" fill="#53675f">反應不足</text>
<text x="327" y="144" font-size="18" font-weight="700" fill="#0a7770">陡峭有效區</text>
<text x="585" y="108" font-size="18" fill="#53675f">平台期</text>
<text x="225" y="340" font-size="18" font-weight="700" fill="#995e26">Threshold</text>
<text x="528" y="340" font-size="18" font-weight="700" fill="#8a5743">Ceiling</text>
<text x="399" y="386" font-size="20" text-anchor="middle" fill="#2c4543">管腔內有效藥物暴露 →（定性）</text>
<text x="42" y="183" transform="rotate(-90 42 183)" font-size="20" text-anchor="middle" fill="#2c4543">瞬時排鈉反應 →</text>
<text x="690" y="50" font-size="14" fill="#53675f" text-anchor="end">非線性示意 · 無臨床劑量刻度</text>
</svg>
</div>
<div class="clinical-mobile-diuresis" role="group" aria-label="手機版 loop 劑量反應完整曲線，包含 threshold、有效區與 ceiling">
<svg viewBox="0 0 360 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="loop-phone-title loop-phone-desc">
<title id="loop-phone-title">Loop diuretic 劑量反應：跨過 threshold 後上升，接近 ceiling 後變平</title>
<desc id="loop-phone-desc">橫軸為定性有效管腔暴露，縱軸為瞬時排鈉反應。左側幾乎沒有反應，中段陡峭上升，右側平台。無真實劑量刻度。</desc>
<rect width="360" height="340" fill="#f8fbf9"/>
<text x="21" y="29" font-size="16" font-weight="700" fill="#244944">瞬時排鈉反應 ↑</text>
<path d="M44 57 V266 H337" fill="none" stroke="#2c4543" stroke-width="2.5"/>
<path d="M53 253 C104 253 120 247 146 211 S198 117 233 98 S282 87 325 87" fill="none" stroke="#0a7770" stroke-width="5.5" stroke-linecap="round"/>
<path d="M141 62 V266" stroke="#b47e43" stroke-width="1.8" stroke-dasharray="5 5"/>
<path d="M267 62 V266" stroke="#a46b55" stroke-width="1.8" stroke-dasharray="5 5"/>
<circle cx="141" cy="217" r="5" fill="#b47e43" stroke="#fff" stroke-width="1.5"/>
<circle cx="267" cy="89" r="5" fill="#a46b55" stroke="#fff" stroke-width="1.5"/>
<text x="68" y="229" font-size="14" fill="#385650">反應不足</text>
<text x="171" y="155" font-size="14" font-weight="700" fill="#0a7770">有效區</text>
<text x="285" y="75" font-size="13" fill="#385650">平台期</text>
<text x="141" y="289" text-anchor="middle" font-size="14" font-weight="700" fill="#995e26">Threshold</text>
<text x="276" y="289" text-anchor="middle" font-size="14" font-weight="700" fill="#8a5743">Ceiling</text>
<text x="190" y="320" text-anchor="middle" font-size="14" fill="#2c4543">管腔內有效藥物暴露 →</text>
</svg>
<p>這是同一條定性 S 型曲線的手機重排版；不是臨床劑量刻度或原書原圖。</p>
</div>
<figcaption><strong>圖 1｜Threshold 與 ceiling 是兩個不同的限速因素。</strong> 曲線為依小麻第九版 PDF 第 179–180 頁文字獨立繪製的概念示意，<strong>不是原書的截圖或實測數據圖</strong>。CKD、藥物分泌、腸道吸收及其他條件會改變真正抵達管腔的暴露。手機改用完整可視的定性曲線，無須橫向捲動。</figcaption>
</figure>

Gut edema 或不穩定的口服吸收，可能使藥物無法可靠地形成足夠 tubular concentration，改成 IV 是讓藥物更確實抵達。Renal insufficiency 則使分泌進入管腔的有效藥量下降，dose–response curve 因而向右移，需要更高劑量才能重新跨過 threshold。

## 單劑有效，並不等於一天已經形成負鈉平衡

可是，有些病人每次使用 furosemide 後都會大量排尿，daily weight 與 congestion 卻沒有持續改善。

藥明明有效，為什麼沒有累積成治療效果？

一種可能，發生在兩次給藥之間。

Loop diuretic 只在濃度高於 threshold 的幾小時內有效。濃度下降後，sodium reabsorption 恢復，RAAS 與 sympathetic activation 也促使腎臟重新留鈉。病人早上服藥後尿很多，下午到夜間卻將鈉收回，全天未必形成負鈉平衡。

這時缺少的不是更高的 peak，而是更長的有效作用時間。增加 dosing frequency，縮短兩次有效區間之間的空隙，可能比繼續堆高單次劑量更合理。

Continuous infusion 改變的也是 exposure 的時間分布，而不是進入更高一級的治療。只要 intermittent bolus 能建立足夠而持續的反應，continuous infusion 並沒有普遍優勢。

## 下游腎元為何能抵消上游已經成功的阻斷？

另一種可能，發生在 loop 作用位置的下游。

腎元本來就是一條連續的 sodium reabsorption 路徑。當 thick ascending limb 被阻斷，更多鈉會流向 DCT 與 collecting duct；下游腎元因而增加 sodium reabsorption，長期使用 loop 後，這種 distal compensation 還會進一步增強。

因此，加入 thiazide 不是因為它比 loop 更強，而是因為它封住了 loop 之後的回收位置。

Sequential nephron blockade 也不是固定的下一步。主要作用位置尚未得到足夠曝露時，應先讓 loop 跨過 threshold；等到 loop 已經明確增加，反應仍受到其他 nephron segments 限制，才需要阻斷另一段 sodium reabsorption。

Cirrhosis 使這個關係看得更清楚。

Cirrhosis 的留鈉受到 secondary hyperaldosteronism 驅動，spironolactone 即使作用在只能處理少量鈉的 distal nephron，仍能阻斷這個疾病最重要的回收力量。它命中的不是容量最大的區段，而是當下最關鍵的病理機轉。

疾病名稱本身沒有指定哪一顆藥最強；它提示的是，利尿效果最可能在哪一層受到抵消。

## 在急性心衰竭，早期反應能告訴我們什麼、不能告訴我們什麼？

在 acute heart failure 中，這些原本看不見的關係，可以透過早期反應被觀察。

給予 IV loop 約兩小時後，spot urine sodium 高於 50–70 mEq/L，可視為這一劑已產生大致足夠的 early natriuretic response；前六小時平均 urine output 高於 100–150 mL/h，則支持這個反應已轉化為可見的 fluid removal。

但它們只能告訴我們這一劑有沒有開始發揮作用，不能證明全天已形成足夠的負鈉平衡，更不能證明 congestion 已經解除。

若早期 urine sodium 或 urine output 不足，當下的 IV loop 可能尚未產生足夠阻斷，因此先將 dose 加倍，再重新評估。若經過 loop escalation，連續觀察到的反應仍不足，且已達 moderate-to-high dose，才考慮加入 thiazide。

相反地，若每一劑的早期反應大致足夠，只是病人仍有 congestion，未必代表需要立刻加藥；他可能只是尚未累積足夠的負鈉平衡，需要持續給藥並觀察全天結果。

## 去鬱血的終點，不是最高尿量

但即使藥物已經生效，病人也確實開始移除水分，仍有最後一個問題：

他是否還需要繼續排鈉？

Urine output 增加，證明這一劑產生了作用；daily weight 下降，比較接近一整天累積的水分移除；JVP、edema、ascites 與呼吸症狀是否改善，才顯示 congestion 有沒有真正解除。

病人可以在一劑藥後大量排尿，卻因其餘時間重新留鈉而沒有減重；也可以已經減重，卻仍殘留明顯 congestion。相反地，當 congestion 已經解除，繼續追求更多尿量便不再增加治療效果，只會逐漸逼近低血容量與低灌流。

Creatinine 的變化，也必須放回這段病程理解。

去充血會改變 glomerular hemodynamics，也可能造成 hemoconcentration，creatinine 因而暫時上升。若病人仍然 congested，血壓與 perfusion 尚可，這個變化不必然代表新的 tubular injury，也不能單獨要求停止利尿。

若同時出現 hypotension、progressive oliguria 或其他低灌流表現，就不能再將 creatinine 上升單純視為去充血中的功能性變化，而必須重新判斷目前的治療強度是否仍可承受，並排除 low-output state 或其他造成腎功能惡化的機轉。

<figure class="diuretic-figure" id="response-pathway">
<div class="diuretic-figure-head"><span>FIGURE 02 · RESPONSE-GUIDED DECISIONS</span><strong>小麻的五步驟處置表，應先用哪個生理問題來讀？</strong></div>
<div class="diuretic-decision-grid" role="group" aria-label="依早期排鈉、全天平衡、代償回收與灌流安全決定利尿策略">
<div class="diuretic-decision-card"><span>01 · EXPOSURE</span><strong>第一劑反應不佳</strong><p>先確認是否抵達管腔並跨過 threshold：劑量、給藥途徑、口服吸收與腎功能。急性心衰竭使用 IV loop 時，依早期反應重新評估，必要時增加劑量。</p></div>
<div class="diuretic-decision-card"><span>02 · DURATION</span><strong>每劑有效，全天仍未負平衡</strong><p>留意給藥空窗、post-diuretic sodium retention、攝鈉及實際排鈉量。重排給藥頻率，未必只追求更高 peak。</p></div>
<div class="diuretic-decision-card"><span>03 · COMPENSATION</span><strong>Loop 已充分加強，反應仍差</strong><p>考慮遠端腎元補償與 sequential nephron blockade；合併 thiazide 等藥物時，須嚴密監測血鈉、鉀、鎂與腎功能。</p></div>
<div class="diuretic-decision-card"><span>04 · STOP / REASSESS</span><strong>鬱血解除，或灌流開始惡化</strong><p>目標不是最大尿量。檢查體重、JVP、症狀、血壓、灌流與腎功能，調整或停止升級；必要時重新判斷病因。</p></div>
</div>
<figcaption><strong>圖 2｜原表不是所有疾病共同適用的固定升級階梯。</strong> 依《Pocket Medicine》9E PDF 第 180 頁〈Approach to Diuresis〉及 <a href="https://academic.oup.com/eurheartj/article/42/36/3599/6358045">2021 ESC 心衰竭指引 Figure 13</a> 的適用條件，另行整理的原創判斷圖；<strong>不是原表的翻拍或逐格重製</strong>。ESC 的 2 小時尿鈉／6 小時尿量參考值針對使用 IV loop 的 acute HF，不能直接套用所有水腫病人。</figcaption>
</figure>

因此，小麻的流程並不是一條從弱藥走向強藥的階梯。

沒有早期反應時，先確認藥物是否抵達並跨過 threshold；每一劑有效、全天效果卻不足時，重新安排有效作用時間；loop 已經明確增加，反應仍受到下游回收限制時，再加入 thiazide。等到 congestion 消失，或病人開始無法承受目前的去充血強度，治療方向便需要重新評估。

真正流暢地使用利尿劑，不是記得流程圖的下一格，而是能從病人的反應判斷：

這一劑有沒有真正生效？已經產生的效果，主要受限於作用時間，還是其他腎元區段的補償？而病人此刻，是否仍需要、也仍能承受繼續去充血？

只要這三個問題還能被重建，藥物、劑量、頻率與組合便不再是彼此分離的記憶。

---

原稿維持[獨立典藏](../originals/2026-07-20-diuretics.md)；本頁為附圖的 AI 整合閱讀版，不把重繪圖冒稱小麻原圖。關於原書第 179–180 頁的內容、原始試驗與指引圖表，請參閱[來源與圖表核對](../diuretics-sources.md)。
