# RR 已經 40/min，為什麼 PaCO₂ 仍然上升？

<div class="opening-question"><span class="small-label">Respiratory Failure｜圖表三問 · 通氣篇</span><p>第一天 RR 24/min、PaCO₂ 39.9；第六天 RR 增加到 40/min，PaCO₂ 卻上升至 54.9，而且開始意識混亂。究竟是病人沒有呼吸驅動，還是呼吸肌有努力、卻推不動足夠的潮氣量？補氧讓 PaO₂ 上升，為什麼也沒能阻止呼吸衰竭？</p></div>

這不是假想題目。**Kim 等人 2010 年的 MG 病例**就是這樣惡化；但如果只把兩次數據貼進「PaCO₂ 與有效肺泡通氣成反比」的公式，仍沒有真正理解患者。這篇依《Pocket Medicine》第九版 PDF 第 106 頁 **Etiologies of High PaCO₂** 原表，從驅動、呼吸肌、胸壁到肺部負荷分層追問，再以另一例真實 OHS 病例檢查：何時需要機械通氣、為何有些人不能安全使用 NIV。

<figure id="pocket-hypercapnia-original" class="pocket-source-shot">
<div class="pocket-source-head">《Pocket Medicine》第九版原表｜PDF 第 106 頁 Etiologies of High PaCO₂</div>
<a href="pocket-medicine-9e-high-paco2.png" target="_blank" rel="noopener" aria-label="開啟小麻第九版高碳酸血症病因表與公式，可放大閱讀">
<img src="pocket-medicine-9e-high-paco2.png" width="1102" height="745" loading="eager" alt="Pocket Medicine 9E 原始 Hypercapnia 公式與 Etiologies of High PaCO2 病因表，Won't Breathe 和 Can't Breathe 四欄、呼吸驅動、神經肌肉、胸壁胸膜、肺氣道疾病" />
</a>
<figcaption><strong>小麻原圖表：Etiologies of High PaCO₂。</strong>擷取自你提供的第九版 PDF 第 106 頁，保留上方 V̇CO₂／RR(VT−VD) 公式、Won't Breathe／Can't Breathe 分類與腳註。手機點圖片可開啟原尺寸放大；以下三問將四欄重新串成因果鏈。<a href="../respiratory-deep-dive-sources.md#pocket-hypercapnia">原表來源與限制</a>。</figcaption>
</figure>

## 第零問｜高 PaCO₂ 不是「呼吸少」，而是 CO₂ 清除跟不上產生

先把四個不該互換的量講清楚。**V̇CO₂** 是組織每分鐘產生並由肺排出的 CO₂ 量（mL/min）；**VT** 是一口氣的 tidal volume（潮氣量，mL）；**RR** 是每分鐘的呼吸次數；**V̇E = RR × VT** 是每分鐘總共進出呼吸系統的空氣。這些氣體不是全部都參與 CO₂ 清除。

每次吸氣必須先經過沒有氣體交換的傳導氣道；而某些肺泡即使有空氣，灌流不足，仍沒有有效排除 CO₂。將這些無效通氣在適當模型下合稱每口 **VD（dead-space volume）**，則**V̇A = RR × (VT − VD)** 才是在近似穩態下有助於排除 CO₂ 的有效肺泡通氣量。這裡的 V̇A 是計算用生理量，不是一般呼吸器或脈搏血氧機直接量到的數值。

<div class="equation"><strong>PaCO₂ ≈ 0.863 × V̇CO₂ / V̇A</strong><strong>V̇A ≈ RR × (VT − VD)</strong><small>V̇CO₂ 為 mL/min、V̇A 為 L/min、PaCO₂ 為 mmHg；0.863 含氣體條件及單位換算。此為相對穩態的生理關係，不可用病人瞬間 RR、未知的 VT/VD 虛構同期 PaCO₂。</small></div>

**呼吸得快，是增加 RR；換氣真正有效，還要有足夠 VT 以及不太高的 VD/VT。**因此，PaCO₂ 上升既可能由 V̇A 真正降低，也可能 V̇A 沒降低卻已跟不上發燒、感染或呼吸肌活動引起的 V̇CO₂ 增加。健康人通常能增加通氣代償；儲備已接近極限的病人則可能失去這種彈性。

## 第一問｜呼吸頻率翻倍，為什麼有效換氣反而可能下降？

先不要代入任何病例；用一個**刻意固定總分鐘換氣量**的數學模型看出公式隱藏的比例關係。假設 V̇E = **6 L/min**、每次 VD = **150 mL**、V̇CO₂ = **200 mL/min**。

| | 深慢換氣 | 快淺換氣 |
| --- | ---: | ---: |
| RR | 12/min | 30/min |
| VT | 500 mL | 200 mL |
| V̇E | 6 L/min | 6 L/min |
| 每口 VD/VT | 30% | 75% |
| 計算 V̇A | 4.2 L/min | 1.5 L/min |
| 穩態預測 PaCO₂ | 約 41 mmHg | 約 115 mmHg |

<figure id="deadspace-example" class="diuretic-figure">
<div class="diuretic-figure-head"><span>FIGURE 01 · WHERE EACH BREATH GOES</span><strong>同樣 6 L/min，快淺呼吸可把更多比例浪費在 dead space</strong></div>
<div class="resp-mobile-panel" role="group" aria-label="深慢與快淺呼吸有效換氣比較"><p class="resp-mobile-label">FIG 01｜同樣 V̇E 6 L/min，哪種換氣更有效？</p><div class="resp-mobile-case"><b>深慢：RR 12，VT 500 mL</b><div class="resp-mobile-meter"><i style="width:30%">VD 30%</i><span style="width:70%">有效 70%</span></div><strong class="resp-mobile-stat">V̇A = 4.2 L/min</strong></div><div class="resp-mobile-case"><b>快淺：RR 30，VT 200 mL</b><div class="resp-mobile-meter"><i style="width:75%">VD 75%</i><span style="width:25%">25%</span></div><strong class="resp-mobile-stat">V̇A = 1.5 L/min</strong></div><p class="resp-mobile-foot">每次 VD 固定 150 mL 的自編模型，不是 MG 或 OHS 病人的 VT／VD。藍色表示有效換氣、橘色表示死腔比例。</p></div>
<div class="diuretic-svg-scroll" role="region" tabindex="0" aria-label="兩種潮氣量下每次150毫升死腔所占比例，可水平捲動">
<svg xmlns="http://www.w3.org/2000/svg" width="760" height="314" viewBox="0 0 760 314" role="img" aria-labelledby="vd-title vd-desc">
<title id="vd-title">同樣總分鐘通氣下，潮氣量變小使每口死腔比例上升</title>
<desc id="vd-desc">深慢呼吸每口500毫升，其中死腔150、有效350；每分鐘12口，總有效換氣4.2升。快淺呼吸每口200毫升，其中死腔150、有效50；每分鐘30口，總有效換氣1.5升。全是模型並非患者測值。</desc>
<rect width="760" height="314" fill="#f8fbfa"/><g font-family="sans-serif" fill="#28443f">
<text x="25" y="35" font-size="18" font-weight="700">每口氣各去哪裡？（長度代表 VT 比例）</text>
<text x="25" y="73" font-size="17">RR 12 · VT 500 mL</text><text x="25" y="190" font-size="17">RR 30 · VT 200 mL</text>
<text x="25" y="277" font-size="13">橘色＝沒有有效 CO₂ 交換的氣體；藍色＝有效肺泡換氣。</text>
<text x="25" y="297" font-size="12">固定 VD 150 mL /口及 V̇E 6 L/min 的教學模型，不是 MG 或 OHS 病例數值。</text></g>
<rect x="25" y="88" width="198" height="62" rx="5" fill="#dc9957"/><rect x="223" y="88" width="462" height="62" rx="5" fill="#3186a6"/>
<rect x="25" y="205" width="495" height="42" rx="5" fill="#dc9957"/><rect x="520" y="205" width="165" height="42" rx="5" fill="#3186a6"/>
<g font-family="sans-serif" font-weight="700" text-anchor="middle"><text x="123" y="114" fill="#3d2b1b" font-size="15">VD 150</text><text x="123" y="137" fill="#3d2b1b" font-size="13">30%</text><text x="453" y="114" fill="#fff" font-size="16">有效 350 mL /口</text><text x="453" y="137" fill="#fff" font-size="14">V̇A 4.2 L/min</text><text x="267" y="231" fill="#3d2b1b" font-size="16">VD 150＝75%</text><text x="602" y="231" fill="#fff" font-size="13">有效 50</text></g>
</svg></div>
<figcaption><strong>圖 1｜比例，而不是呼吸次數，決定了這個模型的有效換氣。</strong>為使兩口氣長度可比較，各橫條刻意畫成同樣寬度代表各自 100% 的 VT，**不以橫條絕對長度代表 500 與 200 mL**。原創計算圖，對照 Pocket Medicine「RR × (VT − VD)」公式。固定 VD 是教學假設，實際死腔與換氣需求會隨疾病及時間改變。</figcaption>
</figure>

這解釋一種最容易誤判的表現：病人呼吸愈急促，胸廓起伏卻愈小，醫師若只看 RR，可能以為呼吸努力正在提高；但如果 VT 同時下降，有效換氣不一定改善。更重要的是，**原始病例若沒有同期的 VT、VD、V̇CO₂，不能只用 RR 和 PaCO₂ 倒算出患者真正的 V̇A**。下面的 MG 個案只證明通氣代償沒有成功，不提供確切分量。

## 第二問｜Won't Breathe / Can't Breathe 是不同的「故障位置」，怎樣用病人的證據辨識？

原表不是把病人分成不想呼吸和不能呼吸兩種人格；它把呼吸作用拆成一條功能路徑：腦幹產生呼吸驅動、周邊神經與神經肌肉接點傳送訊號、橫膈及其他呼吸肌產生力量、胸壁和肺克服彈性與氣道阻力，最後有多少空氣真正參與氣體交換。

<figure id="ventilatory-chain" class="diuretic-figure">
<div class="diuretic-figure-head"><span>FIGURE 02 · FROM DRIVE TO CO₂ REMOVAL</span><strong>PaCO₂ 上升，可以是供需鏈的不同環節失效</strong></div>
<div class="resp-mobile-panel" role="group" aria-label="從呼吸中樞到氣體交換的連續生理流程"><p class="resp-mobile-label">FIG 02｜有效通氣由四個環節串聯</p><div class="resp-mobile-steps"><div><small>01｜Respiratory drive</small><b>呼吸中樞產生驅動</b><span>鎮靜藥、腦幹病變、代謝狀態</span></div><div><small>02｜Neuromuscular</small><b>神經肌肉產生壓力</b><span>MG、GBS、膈神經、橫膈</span></div><div><small>03｜Mechanical load</small><b>克服胸壁與氣道阻力</b><span>肥胖、胸廓受限、COPD auto-PEEP</span></div><div><small>04｜Ventilation efficiency</small><b>只有部分通氣能排出 CO₂</b><span>VD/VT、V/Q 不均與灌流</span></div></div><p class="resp-mobile-conclusion">最後的共同結果：V̇A 相對 V̇CO₂ 不足 → PaCO₂ 上升。</p></div>
<div class="diuretic-svg-scroll" role="region" tabindex="0" aria-label="由腦幹到肺泡氣體交換的因果圖，可水平捲動">
<svg xmlns="http://www.w3.org/2000/svg" width="850" height="348" viewBox="0 0 850 348" role="img" aria-labelledby="drive-title drive-desc">
<title id="drive-title">通氣驅動與呼吸機械能力到有效肺泡通氣的路徑</title><desc id="drive-desc">由腦幹神經驅動、周邊神經和橫膈產壓、胸壁與肺力學負荷、肺泡灌流及死腔效率，接到有效肺泡通氣並決定PaCO2；病因可同時影響多個環節。</desc>
<rect width="850" height="348" fill="#f8fbfa"/>
<g font-family="sans-serif" text-anchor="middle">
<rect x="18" y="65" width="184" height="113" rx="13" fill="#dfeff4" stroke="#4b93ac" stroke-width="2"/><text x="110" y="94" font-size="19" font-weight="700" fill="#22536d">呼吸中樞</text><text x="110" y="120" font-size="14" fill="#22536d">drive</text><text x="110" y="150" font-size="13" fill="#395e6f">藥物、腦幹、代謝</text>
<rect x="229" y="65" width="184" height="113" rx="13" fill="#e4f2e9" stroke="#569978" stroke-width="2"/><text x="321" y="94" font-size="19" font-weight="700" fill="#275b43">呼吸肌產壓</text><text x="321" y="120" font-size="14" fill="#275b43">neuromuscular</text><text x="321" y="150" font-size="13" fill="#466a54">MG、GBS、橫膈</text>
<rect x="440" y="65" width="184" height="113" rx="13" fill="#fff0dc" stroke="#be9253" stroke-width="2"/><text x="532" y="94" font-size="19" font-weight="700" fill="#7a5430">胸壁、氣道</text><text x="532" y="120" font-size="14" fill="#7a5430">mechanical load</text><text x="532" y="150" font-size="13" fill="#805b3d">肥胖、auto-PEEP</text>
<rect x="650" y="65" width="184" height="113" rx="13" fill="#f0e8f5" stroke="#9371aa" stroke-width="2"/><text x="742" y="94" font-size="19" font-weight="700" fill="#634581">有效交換</text><text x="742" y="120" font-size="14" fill="#634581">V̇A / V̇E</text><text x="742" y="150" font-size="13" fill="#745b86">VD/VT、V/Q</text>
</g>
<g stroke="#6b837e" stroke-width="4" fill="none"><path d="M203 121 H229"/><path d="M414 121 H439"/><path d="M625 121 H649"/></g><g fill="#6b837e"><path d="M222 113 L231 121 L222 129"/><path d="M432 113 L441 121 L432 129"/><path d="M643 113 L652 121 L643 129"/></g>
<g font-family="sans-serif" fill="#344f48" text-anchor="middle"><text x="425" y="33" font-size="17" font-weight="700">V̇CO₂ ↑ 會提高整條鏈必須負擔的換氣需求</text><text x="425" y="230" font-size="17" font-weight="700">無論失效位置在哪，只要 V̇A 相對 V̇CO₂ 不足 → PaCO₂ ↑</text></g>
<path d="M110 190 V256 H742 V190" fill="none" stroke="#b18b57" stroke-dasharray="5 6" stroke-width="2"/>
<text x="425" y="295" text-anchor="middle" font-size="15" font-family="sans-serif" fill="#5d7167">Won't Breathe 主要指第一段；Can't Breathe 可發生在後面三段。</text>
<text x="425" y="322" text-anchor="middle" font-size="12" font-family="sans-serif" fill="#5d7167">一個病人可同時有多處問題：OHS 不只是胸壁，COPD 也不只是 dead space。</text>
</svg></div>
<figcaption><strong>圖 2｜從神經輸出到有效肺泡換氣的連續功能圖。</strong>依 Pocket Medicine 第九版 PDF 第 106 頁「Etiologies of High PaCO₂」四欄重新繪製，不照搬表格；此圖不把臨床疾病強行限定在互斥分類。<a href="../respiratory-deep-dive-sources.md#pocket-hypercapnia">原表與腳註</a>。</figcaption>
</figure>

**Won't Breathe：驅動不足或適應性下降。** 鎮靜藥、opioid、部分腦幹病變會減少對 CO₂ 上升的呼吸反應。但原表中的 *metabolic alkalosis* 是另一種性質：高 HCO₃⁻ 和 alkalemia 使呼吸代償性降低，PaCO₂ 相應升高；不能見 PaCO₂ 高就直接診斷原發性呼吸性酸中毒。自願換氣能否增加及 PImax（最大吸氣壓）是否保存，可作定位線索，不能單靠配合意願或一次 PImax 確診中樞問題。

**Neuromuscular：驅動有了，壓力卻做不出來。** MG 侵犯神經肌肉接點；GBS 及其他神經病變阻礙訊號傳遞；脊髓、橫膈與肌病可影響產壓。這裡的床邊問題不只是「PaCO₂ 到幾了」，還包括 **VC（vital capacity，肺活量）**、**MIP／PImax（最大吸氣壓）**、**MEP／PEmax（最大呼氣壓）**、咳嗽能否有效清痰、是否有球部肌肉無力和吞嚥問題。吸氣肌無力使 VT 下降；呼氣／球部肌肉無力也可能造成分泌物清除與氣道保護失敗。仰臥 VC 相對坐姿明顯下降，是橫膈無力的線索；進展性 GBS 的 VC 和呼吸肌力量危險門檻只能結合惡化速度與臨床狀態使用，不能用單一數字自動決定插管。

**胸壁／胸膜：能產生壓力，不保證肺能擴張。** 嚴重肥胖、kyphoscoliosis、胸壁限制或胸水，可能讓產生同樣 VT 需要更多呼吸功。胸水能造成肺塌陷和低氧，但本身不是 hypercapnia 的充分條件；只有當有效肺泡通氣追不上需求時，PaCO₂ 才持續上升。

**肺／氣道：阻力與死腔增加。** COPD 或急性嚴重氣喘使呼氣流速受限，尚未吐完下一口就開始，發生 dynamic hyperinflation。患者必須先克服 auto-PEEP 才能吸入下一口，RR 再上升卻可能進一步縮短呼氣時間，造成更多 air trapping。高 V/Q／dead space 使維持相同 V̇A 需要更大 V̇E；若呼吸泵尚有儲備，PaCO₂ 可正常或偏低，像部分 PE 患者。這不是說 PE 的 dead space 自動造成高碳酸血症。

### 真實病例一：MG 為什麼到 RR 40，反而更需要通氣支持？

Kim 等人報告的 **68 歲女性**，起初沒有典型眼肌與肢體症狀。第一天她在室內空氣下 RR **24/min**、pH **7.441**、PaCO₂ **39.9**、PaO₂ **64.7**。第六天呼吸困難惡化，**RR 40/min**、意識混亂，在 **10 L/min 氧氣面罩**下 pH **7.324**、PaCO₂ **54.9**、PaO₂ **94.4**。肺影像沒有足以解釋全部衰竭的明顯實質病灶，神經生理檢查的 repetitive stimulation decrement 與 AChR antibody 支持 MG；之後病人轉 ICU 接受機械通氣及相應治療。[原始病例與 Figure 1–4](https://doi.org/10.3904/kjim.2010.25.1.101)。

<figure id="mg-trajectory" class="diuretic-figure">
<div class="diuretic-figure-head"><span>FIGURE 03 · OBSERVED CLINICAL TRAJECTORY</span><strong>RR ↑、PaCO₂ ↑、pH ↓：不是病人沒有試著呼吸</strong></div>
<div class="resp-mobile-panel" role="group" aria-label="MG 病例兩個時間點呼吸頻率及動脈血氣"><p class="resp-mobile-label">FIG 03｜RR 更快，CO₂ 反而更高</p><div class="resp-mobile-times"><div><small>Day 1｜室內空氣</small><b>RR 24/min</b><strong>PaCO₂ 39.9</strong><span>pH 7.441｜PaO₂ 64.7</span></div><div><small>Day 6｜O₂ 面罩 10 L/min</small><b>RR 40/min</b><strong>PaCO₂ 54.9</strong><span>pH 7.324｜PaO₂ 94.4</span></div></div><p class="resp-mobile-conclusion">PaO₂ 隨補氧提高，pH 與換氣卻惡化。原研究未提供 VT／VD，無法倒算 V̇A。</p></div>
<div class="diuretic-svg-scroll" role="region" tabindex="0" aria-label="MG真實病例第一天與第六天兩次血氣並列及箭頭，可水平捲動">
<svg xmlns="http://www.w3.org/2000/svg" width="750" height="300" viewBox="0 0 750 300" role="img" aria-labelledby="mg-title mg-desc">
<title id="mg-title">MG病例住院第一天與第六天的呼吸頻率、二氧化碳與酸鹼變化</title><desc id="mg-desc">第一天室內空氣RR24、PaCO2 39.9、pH7.441、PaO2 64.7；第六天氧氣面罩10升每分鐘RR40、PaCO2 54.9、pH7.324、PaO2 94.4。PaO2因給氧條件不同不能直接視為本身肺功能改善。</desc>
<rect width="750" height="300" fill="#f8fbfa"/><g font-family="sans-serif" text-anchor="middle">
<rect x="20" y="47" width="290" height="197" rx="17" fill="#e8f2f7" stroke="#6f9eb2" stroke-width="2"/><rect x="440" y="47" width="290" height="197" rx="17" fill="#f9e8e4" stroke="#c88b7d" stroke-width="2"/>
<text x="165" y="79" font-size="19" font-weight="700" fill="#294c60">Day 1 · 室內空氣</text><text x="585" y="79" font-size="19" font-weight="700" fill="#7c423b">Day 6 · O₂ 面罩 10 L/min</text>
<text x="165" y="117" font-size="18" fill="#294c60">RR 24 /min</text><text x="165" y="150" font-size="18" fill="#294c60">PaCO₂ 39.9</text><text x="165" y="183" font-size="18" fill="#294c60">pH 7.441</text><text x="165" y="215" font-size="18" fill="#294c60">PaO₂ 64.7</text>
<text x="585" y="117" font-size="18" fill="#7c423b">RR 40 /min</text><text x="585" y="150" font-size="18" fill="#7c423b">PaCO₂ 54.9</text><text x="585" y="183" font-size="18" fill="#7c423b">pH 7.324</text><text x="585" y="215" font-size="18" fill="#7c423b">PaO₂ 94.4</text>
</g>
<path d="M320 145 H430" stroke="#ae7556" stroke-width="6"/><path d="M415 133 L435 145 L415 157" fill="none" stroke="#ae7556" stroke-width="6"/>
<text x="375" y="108" font-size="16" font-family="sans-serif" text-anchor="middle" fill="#91604a">惡化</text>
<text x="375" y="277" font-family="sans-serif" font-size="13" fill="#5f7169" text-anchor="middle">同期 VT、VD 未報告，不以 RR 差額推算患者 V̇A</text>
</svg></div>
<figcaption><strong>圖 3｜同一病人不同日期的實測血氣。</strong>完整數據來自 Kim 2010 病例；兩天 FiO₂ 並不相同，**PaO₂ 上升不能當成呼吸泵恢復的證據**。此圖僅重繪原研究報告的數字，沒有插入不存在的 VT、VD 或肺泡換氣量；原文 Figure 1 及後續神經檢查圖請由 <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC2829406/">PMC 全文</a>核讀。</figcaption>
</figure>

這個病例回答了原圖的第二問：**肺能被提高氧分壓，卻不能靠氧氣補足吸氣肌沒有產生的有效 VT。**神經肌肉性呼吸衰竭的危險也不是要等 PaCO₂ 很高才開始；VC、呼吸肌力量、咳嗽／吞嚥與意識的變化，可能比某一次 PaCO₂ 更早讓人決定必須準備氣道支持。

### 真實病例二：OHS PaCO₂ 125，為什麼不是直接「試 NIV 看看」？

2024 年 Miyoshi 等人報告一名 **39 歲男性**，量測設備達上限，只能確定體重**至少 250 kg、BMI 至少約 81.1 kg/m²**；不是量到精確 250 kg。入院 **GCS 8**、RR **22/min**，在 **15 L/min O₂** 下 SpO₂ **87%**。ABG：pH **7.103**、PaCO₂ **125**、PaO₂ **80** mmHg、HCO₃⁻ **37.3** mmol/L。影像同時有肺浸潤、心臟擴大；作者推測可能有感染、心衰因素共同促成 OHS 的急性失代償。[原始 Table 1、Figure 1–3 與完整病程](https://pmc.ncbi.nlm.nih.gov/articles/PMC11460406/)。

先解讀時間尺度：HCO₃⁻ 37.3 提示先前已有慢性 CO₂ retention 的腎臟適應可能，但目前 pH 7.103 是嚴重急性酸血症。**這不是慢性 PaCO₂ 高、所以此刻可以安心等待。**

更重要的是，原文特別交代：入 ICU 後患者**躁動且不配合**，因此未施行 NIV，而是經家屬同意進行氣管插管。**NIV（noninvasive ventilation）** 是以貼合口鼻的面罩等介面，在不插入氣管內管的情況下提供正壓通氣；常用 bilevel NIV 以較高的 **IPAP（吸氣期正壓）**與較低的 **EPAP（呼氣期正壓）**形成 pressure support，協助提高 VT、降低部分呼吸肌負荷。它不是只增加 FiO₂，更不能替代病人保護氣道、清理大量分泌物或保證面罩可持續密合。

所以 OHS 病人的決策不在於「PaCO₂ 125 一定不能用 NIV」，而是**他當時能否安全、有效而可持續地接受非侵入介面**。這名個案的意識、躁動與不配合，再加上嚴重呼吸失衡，使經氣管支持更可行。GCS 低與嚴重酸血症是高度警訊，但仍不是所有病因、所有場景的單一絕對排除值。

治療後的資訊也值得一併閱讀。原文在第 **15 天**、FiO₂ **0.5** 的自主呼吸模式下記錄 pH **7.385**、PaCO₂ **56.9**、HCO₃⁻ **33.9**，病人隨後拔管並短期使用非侵入正壓支持；第 **20 天**離開 ICU，第 **60 天**出院。這時 PaCO₂ **仍高於 45 mmHg**，不能因此判定治療失敗；因為當時的酸鹼穩定性、呼吸負荷、氣道與支持需求已經不同。這也說明治療的終點不是所有患者都回到 PaCO₂ 40。<a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC11460406/">原始 ICU 時間線與呼吸器設定</a>。

<figure id="ohs-trajectory" class="diuretic-figure">
<div class="diuretic-figure-head"><span>FIGURE 04 · SUPPORT DECISION CHANGES WITH THE PATIENT</span><strong>同一個人：入院不能安全配合 NIV，拔管後反而可以使用</strong></div>
<div class="resp-mobile-panel" role="group" aria-label="OHS 病例從入院插管到拔管後 NIV 的時間線"><p class="resp-mobile-label">FIG 04｜NIV 的適用性隨病程改變</p><div class="resp-mobile-steps"><div><small>入院</small><b>GCS 8、pH 7.103</b><span>PaCO₂ 125；嚴重急性失代償</span></div><div><small>急性治療</small><b>躁動、無法配合面罩</b><span>因此未先使用 NIV，而採氣管插管</span></div><div><small>Day 15</small><b>pH 7.385、PaCO₂ 56.9</b><span>拔管後短期使用 NIV</span></div><div><small>Day 20 / 60</small><b>離開 ICU／出院</b><span>PaCO₂ 未回到 40 也不等於治療失敗</span></div></div><p class="resp-mobile-foot">節點依實際時間排列，但間距不代表天數比例；原病例接受多種同步治療。</p></div>
<div class="diuretic-svg-scroll" role="region" tabindex="0" aria-label="OHS病例入院、插管、第15天拔管和第20天離開ICU的病程，可水平捲動">
<svg xmlns="http://www.w3.org/2000/svg" width="805" height="300" viewBox="0 0 805 300" role="img" aria-labelledby="ohs-title ohs-desc">
<title id="ohs-title">OHS案例治療時間線</title><desc id="ohs-desc">入院GCS8、pH7.103、PaCO2 125，因躁動不配合NIV而插管；第15天pH7.385、PaCO2 56.9、FiO2 0.5，拔管後短期NIV，第20天離開加護病房，第60天出院。</desc>
<rect width="805" height="300" fill="#f8fbfa"/><line x1="80" x2="723" y1="145" y2="145" stroke="#74918b" stroke-width="6"/>
<g font-family="sans-serif" text-anchor="middle">
<circle cx="100" cy="145" r="12" fill="#bd675c"/><circle cx="311" cy="145" r="12" fill="#bd855c"/><circle cx="523" cy="145" r="12" fill="#438da0"/><circle cx="713" cy="145" r="12" fill="#4e9074"/>
<text x="100" y="42" font-size="19" font-weight="700" fill="#8b443f">入院</text><text x="100" y="66" font-size="15" fill="#8b443f">GCS 8</text><text x="100" y="87" font-size="15" fill="#8b443f">PaCO₂ 125</text><text x="100" y="110" font-size="15" fill="#8b443f">pH 7.103</text>
<text x="311" y="42" font-size="19" font-weight="700" fill="#895937">氣管插管</text><text x="311" y="66" font-size="15" fill="#895937">躁動、無法配合</text><text x="311" y="87" font-size="15" fill="#895937">不適用當時 NIV</text>
<text x="523" y="42" font-size="19" font-weight="700" fill="#2a6676">Day 15</text><text x="523" y="66" font-size="15" fill="#2a6676">pH 7.385</text><text x="523" y="87" font-size="15" fill="#2a6676">PaCO₂ 56.9</text><text x="523" y="110" font-size="15" fill="#2a6676">拔管 → NIV</text>
<text x="713" y="42" font-size="19" font-weight="700" fill="#376d56">Day 20</text><text x="713" y="66" font-size="15" fill="#376d56">離開 ICU</text><text x="713" y="87" font-size="15" fill="#376d56">Day 60 出院</text>
<text x="402" y="211" font-size="18" font-weight="700" fill="#355a53">支持策略改變，不是因為 PaCO₂ 已降到正常</text>
<text x="402" y="244" font-size="13" fill="#5e746c">非同 FiO₂ 的連續 ABG；此圖不以 PaCO₂ 下降幅度量化插管單獨效果。</text>
<text x="402" y="275" font-size="12" fill="#6e7e76">資料據 Miyoshi 2024 原病例文字與 Table 1、Figure 3；教學重繪非原文影像。</text>
</g>
</svg></div>
<figcaption><strong>圖 4｜支持策略要隨時間重新評估。</strong> 圖上節點以教學順序並列，**間距不代表真實經過時間**。取自 Miyoshi et al. 2024 個案文字與圖表的時間點；插管後同時接受感染、體液負荷、營養及復健介入，不能把病程改善全部歸因於單一呼吸器設定。第 15 天的 ABG 是拔管前後評估脈絡，不是與入院同一 FiO₂ 的直接比較。</figcaption>
</figure>

這正好接回你的治療問題：**使用 NIV 的條件不是單純「PaCO₂ 偏高且還沒昏迷」**。必須同時問：是否有可逆的通氣不足、面罩能否密合並被接受、能否保護氣道與清痰、是否在最初治療後確實降低呼吸功及改善 pH。若有持續惡化的意識或氣道危險，不能為了延長 NIV 而延誤更可靠的氣道處置。進一步比較支援模式與真題情境，可接續閱讀[NIV 的介面、雙壓支持與插管決策](2026-10-22-hypercapnic-failure.md)。

## 第三問｜哪些「看起來變正常」的數字，可能反而掩蓋通氣失代償？

**第一個陷阱：PaCO₂ 正常化。** 患者原本嚴重肺炎，因呼吸刺激而 PaCO₂ 25 mmHg；數小時後若呼吸功更大、VT 更小、意識下降，即使 PaCO₂ 回到 40，也不能自動說恢復。對這名患者而言，原本的低 PaCO₂ 可能是付出極大通氣需求才維持的代償，現在這份能力正在失去。當然，疼痛、發燒或代謝需求下降也可以讓 PaCO₂ 回升，所以**一定要結合前後症狀和 V̇CO₂ 的變動**；這段 25→40 僅是條件式分析，不是另一名被發明的「病例」。

**第二個陷阱：同樣 PaCO₂ 60，卻忽略 pH 和 HCO₃⁻。** 急性呼吸性酸中毒的 HCO₃⁻ 可粗估約 26 mEq/L、pH 約 7.26；慢性 CO₂ retention 在腎臟代償後 HCO₃⁻ 可約 32、pH 約 7.35。這只是典型生理估算，不能代替同時存在的 metabolic alkalosis、利尿劑或腎病評估。因此 OHS 病例入院 HCO₃⁻ 高，和他同時發生極端急性酸血症並不矛盾。

**第三個陷阱：EtCO₂ 的低值。** End-tidal CO₂（EtCO₂）測量**每次呼氣末端**的 CO₂；PaCO₂ 是動脈血氣。肺灌流與 V/Q 分布相對均勻時兩者往往接近，但高 V/Q／dead space、低心輸出量、採樣漏氣或嚴重肺異質性，會讓 EtCO₂ 低估 PaCO₂、兩者差距增大。不能因 Pocket Medicine 表格在 lung/airways 下寫「↓ EtCO₂」，就以為每一種肺病的 EtCO₂ 都下降；單純低通氣反而可使兩者一起升高。

也不要混淆 EtCO₂ 與一整口氣**所有呼出氣混合後的平均 CO₂（mixed expired PCO₂）**。Bohr dead-space equation 使用後者；Enghoff modification 以 PaCO₂ 取代理想肺泡 PCO₂，因此還會受低 V/Q 和 shunt 影響。僅憑 PaCO₂－EtCO₂ gap，不能精確求得 VD/VT 或診斷 PE。

| 床邊觀察 | 最需要重新評估 | 不能直接得出的結論 |
| --- | --- | --- |
| RR 24→40，PaCO₂ 也上升 | VT、呼吸肌儲備、dead-space 與 CO₂ 需求 | 「病人沒有努力呼吸」 |
| 補氧後 PaO₂ 上升，pH／PaCO₂ 惡化 | 氧合與有效通氣是否分離 | 「肺功能已恢復」 |
| GCS 下降、無法配合 NIV | 氣道保護、介面可行性與及時插管 | 「PaCO₂ 高的人一定都得插管」 |
| 插管後 PaCO₂ 仍 56.9，pH 接近正常 | 慢性代償與目前穩定性、能否脫離支持 | 「PaCO₂ 未達 40 表示治療失敗」 |
| EtCO₂ 偏低、PaCO₂ 偏高 | 死腔／V/Q、肺灌流、儀器與波形 | 「一定是 PE」 |

**結論。** 這張表不是讓人把病名丟進四欄，而是在呼吸中樞、神經肌肉、胸壁及肺泡換氣效率間，尋找哪個環節讓**ventilatory demand 超過 ventilatory capacity**。當病人仍在提高 RR，真正危險的可能是 VT 已無法再提供足夠有效通氣；當病人已需要 NIV 或插管，真正必須重新評估的是治療能否安全提供所需的通氣，而非追求漂亮的 PaCO₂ 數字。

[回到 A–a / shunt 病例篇](2026-10-25-hypoxemia-mechanisms.md)・[NIV 治療篇與國考題](2026-10-22-hypercapnic-failure.md)・[原表、病例與圖說審查範圍](../respiratory-deep-dive-sources.md)
