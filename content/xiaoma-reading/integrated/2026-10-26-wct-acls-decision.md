# 還不知道是什麼，憑什麼治療

*小麻閱讀（9E）｜心律急症系列 03／03：從 wide-complex tachycardia 回看 ACLS。以 2026/7/17 作者原稿的核心論證為主幹，另作安全性與跨篇整合。*

**系列閱讀：[01｜WPW：QRS 為何有時寬、有時窄？](2026-10-26-wpw-conduction-mechanism.md) → [02｜Pre-excited AF：何時不能阻斷 AV node？](2026-10-26-preexcited-af.md) → 本篇「診斷未定時的行動理由」**

ACLS tachyarrhythmia algorithm 看起來很直觀：病人不穩定就 cardioversion；若還穩定，再依 QRS 寬窄選擇處置。

但讀完小麻的 wide-complex tachycardia（WCT），這條路徑反而變得不再直觀。

## 先看完整流程，再討論流程為何不能直接等於診斷

<figure id="wct-acls-main-algorithm" class="acls-core-figure" role="group" aria-label="2025 AHA 有脈搏成人心搏過速主流程的獨立解讀圖，含是否由心搏過速造成不穩定、QRS 寬窄、規則性與危險例外">
<div class="acls-core-head"><span>CLINICAL REFERENCE · AHA 2025</span><strong>Adult Tachyarrhythmia With a Pulse：真正的 Yes／No 分支</strong><p>先閱讀官方完整原圖，再將同一套問題對照 WPW／pre-excited AF。以下為本站獨立設計的閱讀路徑，非 AHA 原圖的複製或官方翻譯。</p><a class="acls-official-link" href="https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-Tachycardia-250514.pdf" target="_blank" rel="noopener noreferrer">開啟 2025 AHA 官方完整流程圖（原始 PDF，可放大／下載） ↗</a></div>
<svg class="acls-desktop-graph" viewBox="0 0 1120 995" role="img" aria-labelledby="acls-flow-title acls-flow-desc" xmlns="http://www.w3.org/2000/svg">
<title id="acls-flow-title">有脈搏成人 tachyarrhythmia：血流動力學決策優先，穩定後再以 QRS 寬窄進入不同分支</title>
<desc id="acls-flow-desc">成人有脈搏與持續性心搏過速，先同時做初始支持、監測與十二導程心電圖。若目前血流動力學失衡是由心搏過速造成，迅速處理並通常使用同步電復律。若否，判斷 QRS 是否至少 120 毫秒，狹窄者依規則性考慮迷走神經手法與腺苷等；寬大者只有穩定、規則且單形態時才可考慮腺苷，並考慮抗心律不整治療與專科協助。不規則或多形態寬 QRS 不應套用腺苷，且 polymorphic VT 和 pre-excited AF 需要另辨別高風險處置。</desc>
<defs><marker id="acls-arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0 0L0 6L8 3Z" fill="#42636e"/></marker></defs>
<rect x="338" y="19" width="450" height="115" rx="13" fill="#edf4f2" stroke="#426f69" stroke-width="2"/>
<text x="563" y="54" font-size="23" font-weight="750" fill="#1b3c3c" text-anchor="middle">成人有脈搏 · 持續性 tachyarrhythmia</text>
<text x="563" y="82" font-size="17" fill="#354d4d" text-anchor="middle">先評估心率與病況（通常 ≥150/min）</text>
<text x="563" y="109" font-size="17" fill="#354d4d" text-anchor="middle">Airway／必要氧氣／監測 · IV · 12-lead ECG</text>
<path d="M563 134V172" stroke="#42636e" stroke-width="3" fill="none" marker-end="url(#acls-arrow)"/>
<path d="M563 179L811 278L563 377L315 278Z" fill="#fdf0e6" stroke="#b97543" stroke-width="2.5"/>
<text x="563" y="262" font-size="22" font-weight="750" text-anchor="middle" fill="#543f2d">是否由 tachyarrhythmia</text>
<text x="563" y="290" font-size="22" font-weight="750" text-anchor="middle" fill="#543f2d">造成當下不穩定？</text>
<text x="563" y="319" font-size="15" text-anchor="middle" fill="#694f38">Shock／低壓／意識改變／缺血／急性 HF</text>
<path d="M315 278H244V415" stroke="#42636e" stroke-width="3" fill="none" marker-end="url(#acls-arrow)"/>
<text x="261" y="258" font-size="19" font-weight="800" fill="#985034" text-anchor="middle">YES</text>
<rect x="40" y="423" width="414" height="174" rx="12" stroke="#a85740" stroke-width="2" fill="#fdf0ed"/>
<text x="247" y="459" font-size="23" font-weight="750" text-anchor="middle" fill="#783629">迅速處置不穩定節律</text>
<text x="247" y="495" font-size="20" text-anchor="middle" fill="#543d3b">通常 synchronized cardioversion</text>
<text x="247" y="524" font-size="16" text-anchor="middle" fill="#543d3b">鎮靜可行時使用，不延誤必要電擊</text>
<text x="247" y="551" font-size="16" text-anchor="middle" fill="#543d3b">若 regular narrow，可考慮 adenosine</text>
<text x="247" y="575" font-size="15" text-anchor="middle" fill="#7c3432">polymorphic VT 要另判電擊模式 *</text>
<path d="M811 278H910V405" stroke="#42636e" stroke-width="3" fill="none" marker-end="url(#acls-arrow)"/>
<text x="858" y="258" font-size="19" font-weight="800" fill="#315b65" text-anchor="middle">NO</text>
<path d="M910 414L1080 485L910 556L740 485Z" fill="#e8f2fa" stroke="#397d9a" stroke-width="2.5"/>
<text x="910" y="477" font-size="22" font-weight="750" text-anchor="middle" fill="#264b60">Wide QRS?</text>
<text x="910" y="506" font-size="20" font-weight="700" text-anchor="middle" fill="#264b60">≥ 0.12 秒</text>
<path d="M740 485H652V642" stroke="#42636e" stroke-width="3" fill="none" marker-end="url(#acls-arrow)"/>
<text x="699" y="466" font-size="18" font-weight="800" text-anchor="middle" fill="#315b65">NO</text>
<path d="M1080 485H1100V615H960V642" stroke="#42636e" stroke-width="3" fill="none" marker-end="url(#acls-arrow)"/>
<text x="1081" y="465" font-size="17" font-weight="800" text-anchor="end" fill="#315b65">YES</text>
<rect x="486" y="650" width="325" height="153" rx="12" stroke="#426f69" stroke-width="2" fill="#eef6ef"/>
<text x="648" y="686" font-size="22" font-weight="750" text-anchor="middle" fill="#2a534a">NARROW QRS</text>
<text x="648" y="717" font-size="17" text-anchor="middle" fill="#254e46">規則者：vagal／adenosine</text>
<text x="648" y="746" font-size="16" text-anchor="middle" fill="#254e46">可考慮 β blocker 或 CCB *</text>
<text x="648" y="776" font-size="16" text-anchor="middle" fill="#254e46">評估節律與專家協助</text>
<rect x="822" y="650" width="277" height="153" rx="12" stroke="#426f69" stroke-width="2" fill="#eef6ef"/>
<text x="960" y="684" font-size="22" font-weight="750" text-anchor="middle" fill="#2a534a">WIDE QRS</text>
<text x="960" y="712" font-size="15" text-anchor="middle" fill="#254e46">Adenosine：僅穩定＋規則＋單形態</text>
<text x="960" y="744" font-size="16" text-anchor="middle" fill="#254e46">考慮 antiarrhythmic infusion</text>
<text x="960" y="771" font-size="16" text-anchor="middle" fill="#254e46">專科協助、隨時再評估</text>
<rect x="38" y="841" width="1047" height="115" rx="12" fill="#f8ecea" stroke="#b5634d" stroke-width="2"/>
<text x="62" y="876" font-size="22" font-weight="750" fill="#783629">* 必須另外辨識的例外：不能從主流程的藥物格直接開藥</text>
<text x="62" y="906" font-size="18" fill="#6b3e35">Irregular／polymorphic WCT → 不給 adenosine；pre-excited AF → 避免 AV nodal blockers／IV amiodarone。</text>
<text x="62" y="934" font-size="17" fill="#6b3e35">Sustained polymorphic VT → immediate unsynchronized shock；若無脈搏，改用 cardiac-arrest algorithm。</text>
</svg>
<div class="acls-mobile-graph" aria-label="有脈搏成人 tachyarrhythmia 手機版完整決策流程">
<div class="acls-m-step acls-m-entry"><strong>有脈搏的成人 tachyarrhythmia</strong><span>先確認心率與病況是否相符（tachyarrhythmia 常 ≥150/min）；Airway／氧氣（若低氧）／ECG、血壓監測／IV／12-lead ECG</span></div>
<div class="acls-m-down" aria-hidden="true">↓</div>
<div class="acls-m-decision"><strong>目前的不穩定，是由 tachyarrhythmia 造成嗎？</strong><span>Hypotension、shock、意識改變、缺血性胸痛、急性 HF</span></div>
<div class="acls-m-branch-label">YES ↓</div>
<div class="acls-m-step acls-m-urgent"><strong>迅速處置節律：通常 synchronized cardioversion</strong><span>鎮靜可行時使用，不延誤電擊；sustained polymorphic VT 為非同步電擊的特殊情境。</span></div>
<div class="acls-m-branch-label acls-m-no">NO ↓（另一條分支，並非接續電復律）</div>
<div class="acls-m-decision"><strong>QRS ≥ 0.12 秒？</strong></div>
<div class="acls-m-split">
<div class="acls-m-step"><small>NO · NARROW</small><strong>依規則性判讀</strong><span>Regular：vagal maneuvers／adenosine；其他降心率藥物仍須核對節律、心功能與禁忌。</span></div>
<div class="acls-m-step"><small>YES · WIDE</small><strong>先確定 regular 與 monomorphic</strong><span>兩者皆成立且病人穩定時，才可考慮 adenosine；另考慮 antiarrhythmic infusion 與專科協助。</span></div>
</div>
<div class="acls-m-warning"><strong>主流程之外的高風險界線</strong><span>Irregular／polymorphic WCT 不使用 adenosine；pre-excited AF 不套用一般 AV nodal blockers 或 IV amiodarone。持續 polymorphic VT 需非同步電擊；若無脈搏改走 cardiac-arrest algorithm。</span></div>
</div>
<div class="acls-rescue-footer"><strong>若初始介入仍無效：重新評估</strong><span>核對造成 tachyarrhythmia 的因素、是否需要調整下一次電復律能量、增加抗心律不整治療，以及專科協助；病情改變時重新回到最上游判斷。</span></div>
<figcaption><strong>本站原創流程解讀｜2025 AHA Adult Tachyarrhythmia With a Pulse Algorithm。</strong> 圖上流程為對照本文 WPW／WCT 的教學重構，不是 AHA 正式圖像、完整指引翻譯或個別病人處方。成人有脈搏是適用前提；本圖為優先決策架構，**劑量與電擊能量需回讀官方原圖**；主流程的藥物選項需連同 2025 ALS 的 WCT 禁忌和 2023 AF guideline 的 pre-excitation 限制閱讀。<a href="https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-Tachycardia-250514.pdf">官方 Figure 6 原圖（直接開啟）</a>；<a href="https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/adult-advanced-life-support">2025 ALS 文字建議</a>。</figcaption>
</figure>

現在才能準確提出後面的問題：ACLS 已經將 **causing instability**、**QRS duration**、**regular／monomorphic** 放在不同判斷層次，但它們沒有一個可以單獨證明「這是 VT、SVT 或 accessory pathway」。流程先定義當下安全的處置空間，病因機轉再決定不能外推哪些藥物選項。



Wide QRS 不是診斷。它可能來自 VT、SVT with aberrancy、accessory-pathway conduction，也可能是 ventricular pacing；有時 hyperkalemia 或 sodium-channel blocker toxicity 也讓 ventricular conduction 異常。即使確認是 VT，monomorphic 與 polymorphic 的機轉及立即處置也可能不同。

[第一篇](2026-10-26-wpw-conduction-mechanism.md)進一步說明，同一條 AP 在不同節律可以是迴路的回程、去程，或者根本不是維持節律的組件。[第二篇](2026-10-26-preexcited-af.md)則讓我們看見：同一種 AV nodal block，可能中斷 orthodromic AVRT，卻在 pre-excited AF 造成致命風險。

然而，ACLS 並沒有等這些分類全部完成，才允許治療。這表示它真正管理的，不是已知病名的清單，而是：**當答案還不完整時，憑什麼開始行動？**

## Tachycardia 是不穩定的原因，還是不穩定的反應？

ACLS 2025 的第一個決策點，並不只寫 hypotension、acute altered mental status、shock、ischemic chest discomfort 或 acute heart failure；它寫的是 persistent tachyarrhythmia **causing** 這些表現。

這個 causing 是全篇最重要的字。

Tachycardia 與 hypotension 同時存在，不能自動建立因果。敗血性休克病人的 sinus tachycardia，可能來自交感活化與維持 cardiac output 的代償；如果急著以電擊消除心跳過快，而沒有處理感染、血管擴張與有效循環問題，就選錯了介入目標。

相反地，若病人突然發作 sustained monomorphic VT，緊接著出現低血壓、意識改變或肺水腫，心室活化異常、舒張充盈時間縮短、房室同步消失與原有的 myocardial substrate，都可能讓心律本身造成 hemodynamic collapse。此時電復律不是單純追求正常 ECG，而是在移除造成灌流失敗的主要機轉。

所以 unstable 並不是「某一種心律」的固定標籤；它是目前 rhythm、cardiac substrate、代償餘裕共同造成的血流動力學結果。同一個 VT 可以被某位病人短暫承受，在另一位嚴重 cardiomyopathy 病人身上迅速造成 shock；極不穩定的 sinus tachycardia 也仍可能是代償，而不是該被電擊的原因。

這裡的因果判斷必須**迅速而不僵化**。它不是要求在急救前證明 causality；若臨床已高度懷疑 tachyarrhythmia 正在造成灌流失敗，不可因還缺精確 EP mechanism 而延誤電擊。當原文說「需要先判斷」，指的是找對正在破壞 circulation 的環節，不是延後必要救援。

## 同樣是要電擊，為什麼不能一律 synchronized？

這是原稿需要加入 2025 指引後，最重要的安全限定。

如果病人 **有 pulse，且 unstable 的 WCT 屬於可同步辨識的單形態節律**，應迅速 synchronized cardioversion，鎮靜在可行時使用，但不能因此耽誤治療。若已是 **sustained polymorphic VT**，AHA 2025 要求 **immediate unsynchronized high-energy shock**：多變 QRS 可能使可靠的 R-wave synchronization 困難，拖延或誤同步增加風險。若失去 pulse，則不再使用「with a pulse」流程，而走 VF／pulseless VT cardiac-arrest／CPR 與 defibrillation 路徑。

**Pre-excited AF 與 sustained polymorphic VT 不能只因看起來都是不規則寬 QRS 就視為同一節律。** 前者若因 AF 造成 hemodynamic instability，依 2023 AF guideline 採 synchronized electrical cardioversion；後者不論是否仍有 pulse，持續性 polymorphic VT 的治療方向是立即 unsynchronized shock。當 ECG 診斷難分，復甦團隊需依實際節律與可否可靠同步迅速作出電擊模式判斷，而不是讓一張簡化的成人 tachycardia algorithm 取代臨床辨識。

這並沒有破壞「不能等確診才治療」的原則。它反而更精確：**可以尚未知道 VT 的起源或 AP 位置，但不能不知道某些當下可辨認、會改變電擊類型的危險界線。**

## 病人暫時 stable，QRS width 究竟替我們回答了什麼？

當 tachyarrhythmia 暫時沒有使病人失去灌流，ACLS 才獲得觀察 ECG、嘗試取得 12-lead、建立 IV、持續監測與備妥救援的空間。此時 QRS duration ≥0.12 秒，首先只說明**心室激發的時間變長**。它沒有說明 impulse 從心室起源，還是經正常房室傳導系統以外的路徑進入心室。

小麻把 WCT 按 origin、conduction、substrate 分開：VT、SVT with aberrancy、AP pre-excitation、pacing。這些是**病因與機轉分類**，不會因流程圖把它們放在同一格就變成同一疾病。

甚至「hemodynamically stable」本身也不能替 VT 除名。過去 MI、LV dysfunction、AV dissociation、capture／fusion beats 等線索有其診斷價值；反過來，沒有這些 finding 或暫時血壓穩定，也不足以將 WCT 宣稱為 benign SVT。以 WCT 存疑處理時，應優先考慮可能的 VT 與危險的 pre-excited AF，而不是任意測試 AV nodal blocker。

問題是：如果還不知道它是什麼，為何 2025 ACLS 又允許某些藥物試探？

## Regular 與 monomorphic，不是病名，是某一項介入的狹窄許可

先分辨兩個表面特徵：**regular** 是 RR intervals 大致一致；**monomorphic** 是各搏 ventricular activation 形成相近的 QRS 外觀。兩者都無法證明這是 SVT。Scar-related VT、idiopathic VT、SVT with fixed BBB，以及某些 antidromic AVRT，都可能是 regular monomorphic WCT。

但如果病人**確實 hemodynamically stable、regular 且 monomorphic**，2025 AHA 成人 ALS 對原因仍不明的 WCT，允許 **IV adenosine *may be considered*（Class IIb）**，作為治療或幫助診斷；這不是 routine recommendation，也不是宣稱 ECG 排除了所有高風險可能。持續 ECG／BP 監測、救援與專科協助是必要背景，無法安全試探就不試。

為什麼 adenosine 仍有資訊價值？它能短暫造成 AV nodal block。如果 AV node 是 tachycardia 的必要迴路（例如 orthodromic AVRT、AVNRT），阻斷後可能終止；若 atrial tachyarrhythmia 仍持續，短暫 block 可能揭露原先被 ventricular response 遮蔽的 atrial activity；若機轉不依賴 AV node，可能沒有明顯效果。

但治療反應不是 diagnosis 的同義詞。某些 idiopathic outflow-tract VT 也可能對 adenosine 有反應，所以「給了 adenosine，節律停了」不能用來宣稱已確診 SVT。

這條試探邊界也有不能跨過的地方。2025 AHA 明列 **hemodynamically unstable、irregularly irregular 或 polymorphic WCT 不應給 adenosine（Class III: Harm）**；成人 WCT 也不應經驗性給 IV **verapamil／diltiazem（Class III: Harm）**。若 ECG 暗示 **pre-excited AF**，2023 AF guideline 進一步禁止 adenosine、beta blockers、verapamil、diltiazem、digoxin、amiodarone，因為正常 AV nodal conduction 被抑制後，AF impulses 仍可經 AP 快速順傳，造成 VF。**一般 stable WCT 可考慮 amiodarone 的建議，不能外推到 pre-excited AF。**

這就是 [第二篇](2026-10-26-preexcited-af.md)與 ACLS 真正接合的地方：regular monomorphic 只縮小了嘗試特定操作的風險範圍；當改成 irregular pre-excited AF，**操作本身的安全前提被推翻**。藥物沒有變，變的是被阻斷的 AV node 在當下 rhythm 中到底是迴路必需元件，還是限制心房衝動抵達心室的一道屏障。

<figure id="wct-decision-figure" class="diuretic-figure" role="group" aria-label="實際病例 irregular WCT 與轉律後預激對照，連結 ACLS 決策界線">
<div class="diuretic-figure-head"><span>FIGURE 04 · ECG BEFORE THE DIAGNOSIS</span><strong>原始 WCT 長這樣：不能從 QRS 寬度直接開藥</strong></div>
<a href="https://journals.sagepub.com/cms/10.1177/2324709618802870/asset/b2fc7153-320e-4d2b-a28a-0443e25d3345/assets/images/large/10.1177_2324709618802870-fig1.jpg" target="_blank" rel="noopener noreferrer" aria-label="開啟 ECG 原始大圖"><img src="https://journals.sagepub.com/cms/10.1177/2324709618802870/asset/b2fc7153-320e-4d2b-a28a-0443e25d3345/assets/images/large/10.1177_2324709618802870-fig1.jpg" alt="Silverman 2018 發作中的 irregular wide-complex tachycardia：RR 間距不規則、QRS 外觀及寬度不同" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;max-width:100%;border:1px solid #dde5e3;border-radius:8px;background:white"/></a>
<p><strong>現在的判斷不是猜出 accessory pathway 位置。</strong> 這張 ECG 足以辨認「不規則＋QRS 寬度變異」，因此不能套用 stable regular monomorphic WCT 才可考慮 adenosine 的限定條件。尚未出現明確灌流衰竭時，也不能由 WCT 一詞直接推定一律需要電擊。</p>
<p><strong>轉律之後才補上的資訊：</strong></p>
<a href="https://journals.sagepub.com/cms/10.1177/2324709618802870/asset/ad05d429-0d11-4942-8d83-53da56dd71c1/assets/images/large/10.1177_2324709618802870-fig2.jpg" target="_blank" rel="noopener noreferrer" aria-label="開啟 ECG 原始大圖"><img src="https://journals.sagepub.com/cms/10.1177/2324709618802870/asset/ad05d429-0d11-4942-8d83-53da56dd71c1/assets/images/large/10.1177_2324709618802870-fig2.jpg" alt="Silverman 2018 復律後 ECG：sinus tachycardia 合併 delta wave，支持 manifest pre-excitation" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;max-width:100%;border:1px solid #dde5e3;border-radius:8px;background:white"/></a>
<figcaption><strong>圖 4｜先判操作邊界，再補齊病因。</strong> 真實病例：Silverman A, Taneja S, Benchetrit L, Makusha P, McNamara RL, Pine AB. 2018. <a href="https://doi.org/10.1177/2324709618802870">doi:10.1177/2324709618802870</a>；<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>；圖像未裁切或重繪。 第一張是治療前的證據，第二張是 100 J 同步電復律後的觀察；兩者不可倒置。2025 AHA <a href="https://www.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-Tachycardia-250514.pdf">成人 tachyarrhythmia 官方演算法原檔</a>和<a href="https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/adult-advanced-life-support">ALS 詳細建議</a>另行對照；原 AHA 圖未複製或冒稱本站重繪。</figcaption>
</figure>

## 從真實病例回看：哪些資訊可以等，哪些不能？

在[第二篇](2026-10-26-preexcited-af.md)的 Silverman 2018 真實病例中，病人急診收縮壓仍約 130 mmHg，原始 ECG 卻已有快到 300/min 的 irregular WCT，部分搏動的 QRS 寬度不同。轉律後才出現清楚的 delta wave，次日才確定右後中隔 AP 並消融。

這個時間序列最重要的不是「後來知道原來是 WPW」，而是兩種知識有不同的時鐘。

**當下可以不知道的**，包括 AP 位於哪一側、是否是單一通道、EP study 的精確 conduction properties；這些關係到 definitive diagnosis、ablation 與長期風險。**當下不能假裝不知道的**，則是 irregularly irregular、極快且可能 pre-excited 的 WCT 不適合任意 adenosine 或 AV nodal blockade，以及 rhythm 一旦造成 hemodynamic failure 就須迅速選擇正確的 electrical treatment。

原病例曾以 IV amiodarone 治療，當時無效，之後才同步轉律。這段歷史不能回頭當作現行建議；2023 AF guideline 已對 pre-excited AF 明列 amiodarone 為 Class III Harm。**Case report 告訴我們醫師如何在現場形成與修正判斷；guideline 才回答今天應如何選擇安全治療。**

再做兩個**明示的反事實思考，而非病例真實觀察**：如果同樣的 WCT 變得 regular、monomorphic，且灌流穩定，可以討論有限的 ECG-based 診斷與治療；若仍是相同節律卻迅速出現 shock 並可歸因於 tachyarrhythmia，資訊等待的代價改變，應優先電復律。若節律明確是 sustained polymorphic VT，又要改採 immediate unsynchronized shock。**改變的不是「醫師懂得更多」，而是某些仍未知的事情，已不再阻止當下救援。**

## 病名可以尚未完整，行動的理由不能不完整

小麻 WCT 的分類告訴我們：ECG 看起來相似，origin、conduction 和 substrate 可能完全不同。ACLS 則依據當下已知的灌流後果、節律特徵與治療延誤代價，決定哪些情況可以暫時合併處置，哪些風險不能混在一起。

急救中的專業，不是用較少資訊冒險，也不是為了防錯而等到所有病因都明確；而是知道**哪些診斷可以稍後追查，哪些操作前提現在就必須釐清**。

第一篇使我們看見路徑，第二篇讓我們看見路徑在不同節律下的危險角色；回到第三篇，臨床決策終於有了清楚的共同尺度：**不確定的不是行動理由，而是行動之後仍待完成的診斷。**

**病名可以尚未完整，行動的理由不能不完整。**

---

*本文以 2026/7/17 作者同名原稿的核心論證為起點，另製 AI 整合稿，未修改私人封存原稿。來源：[Pocket Medicine 9E，私人 PDF 第 67–68 頁](https://www.wolterskluwer.com/zh-tw/solutions/ovid/pocket-medicine-15398)（出版社書目，不是私人 PDF）；[2025 AHA ALS](https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/adult-advanced-life-support)；[2023 ACC/AHA/ACCP/HRS AF §10.6](https://www.jacc.org/doi/10.1016/j.jacc.2023.08.017)；[Silverman et al. 2018 真實病例](https://journals.sagepub.com/doi/10.1177/2324709618802870)。原始 WCT 圖與 ACLS 圖已核讀；本文直接嵌入經確認為 CC BY 4.0 之 2018 病例 ECG 並附完整來源與授權；AHA 2025 完整演算法僅提供原始來源連結，不複製 AHA 授權圖。*


[**原圖、病例與 2025 AHA／2023 AF 來源逐項核對**](../arrhythmia-sources.md)。
