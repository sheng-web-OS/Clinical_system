# 還不知道是什麼，憑什麼治療：從 WPW 走到 WCT／ACLS

**小麻閱讀整合稿｜第三篇：急救決策（2026-10-26）**

[第一篇：WPW 的順向與逆向傳導](2026-10-26-wpw-conduction-mechanism.md) → [第二篇：Pre-excited AF 的 AV node 悖論](2026-10-26-preexcited-af.md)

前兩篇建立了傳導方向與旁路角色。這篇把同一個模型放回急救現場：診斷尚未完整時，哪些已知資訊足以改變行動？

## 一開始不該問 QRS 寬不寬，而要問心律正在造成什麼

先比較兩種機轉情境：病人心跳 180/min、血壓低，直覺上很想立刻把 ECG 的不正常節律消除。但 tachycardia 與 hypotension 同時發生，不代表前者必然造成後者。

在 septic shock 或失血時，sinus tachycardia 可能是交感活化、維持 cardiac output 的代償；單純「電擊數字 180」既不治療原因，還可能造成傷害。若病人突然發作 sustained ventricular tachycardia（持續性心室頻脈，VT），之後因舒張充盈時間縮短、房室時序改變與心室功能不足而休克，則 rhythm 本身可能是當下灌流失敗的近因，延誤轉律會付出代價。

所以 2025 AHA 流程寫的是 **persistent tachyarrhythmia *causing* hypotension、shock、altered mental status、ischemic discomfort 或 acute heart failure**。造成的判斷是迅速依情境與時間關係作出高可信度臨床歸因，不是要求在轉律前得到實驗室等級的因果證明。若高度懷疑 arrhythmia 已使病人失去灌流，應即時救援，不能把「先問因果」變成拖延的理由。

若是有 pulse、hemodynamically unstable 的 regular monomorphic WCT，應迅速 **synchronized cardioversion**。但 sustained **polymorphic VT** 不應套進這個同步支線，應立即 **unsynchronized high-energy shock**；若無脈搏，改走心跳停止／CPR＋defibrillation 路徑。電擊種類不是依「病人嚴不嚴重」一軸決定，而要考慮 ECG 節律可否可靠同步、是否已屬應除顫之節律。

<figure id="wct-action-boundaries" class="reasoning-figure"><div class="reasoning-title">仍不知道病名時，先確定不能失去的三種資訊</div><div class="reasoning-cards"><section><strong>有無脈搏？</strong><p>無脈搏 VT／VF → 立即 CPR 與除顫的心搏停止路徑。</p></section><section><strong>節律是否造成灌流失敗？</strong><p>有脈搏、因持續心搏過速而不穩定 → 迅速電復律；代償性 sinus tachycardia 應處理原因。</p></section><section><strong>電擊與用藥的節律限制</strong><p>規則單形態 WCT 可可靠同步；持續 polymorphic VT 需非同步高能量電擊。穩定、規則、單形態是可考慮 adenosine 的必要限制，非 SVT 診斷。</p></section></div><figcaption>原創風險分層圖，對讀 Pocket Medicine 9E PDF 第 67–68 頁 WCT 與 AHA 2025 ALS §15–16／官方 tachyarrhythmia algorithm；不是完整 ACLS 流程。</figcaption></figure>

## 2025 ACLS 為什麼先看 QRS width，又不相信 QRS width 是診斷？

QRS ≥0.12 秒描述 ventricular activation 花的時間較長。原因可能是心室本身發出節律（VT）、上心室訊號經 bundle branch block 傳導（SVT with aberrancy）、經 accessory pathway 先活化心室（pre-excitation），或 pacemaker、特定代謝／藥物造成的傳導異常。

這些來源在 ECG 都可能表現成 wide-complex tachycardia，治療卻不相同。**Wide QRS 是將處置風險提高的可觀察訊號，不是告訴你「它就是 VT」或「它一定不是 SVT」。** 在未確診的成人 WCT，VT 應被優先嚴肅考慮，尤其有結構性心臟病、過去心肌梗塞者；血壓尚可不能排除 VT。

而 WPW 正好提供重要反例：**orthodromic AVRT** 往 AV node 下行，通常窄 QRS；**antidromic AVRT** 經 bypass tract 下行，通常規則寬 QRS；**pre-excited AF** 則可呈極快且不規則、寬度可變的 QRS。三者可能涉及同一條旁路，但在不同 rhythm，旁路扮演的角色完全不同。

更重要的是，**irregular wide QRS 也不等於 pre-excited AF**：AF with aberrancy、polymorphic VT、其他病因都需鑑別；ECG 的不規則性與 morphology 變化提供安全邊界，卻尚不足以自動完成診斷。

## Adenosine：此刻的節律是否容許 AV node 阻斷？

2025 AHA 對 **hemodynamically stable、regular、monomorphic WCT，且原因尚不明確**，將 monitored IV adenosine 設為 **may be considered（Class IIb）** 來嘗試治療或輔助鑑別。這是有限授權，不表示規則單形態已排除 VT，也不是允許先給任何 AV nodal blocker 再說。WCT 之中 **verapamil／diltiazem 不應經驗性給予（Class III Harm）**；對 unstable、irregularly irregular 或 polymorphic WCT，**adenosine 也屬 Class III Harm**。

背後的機轉與第二篇相接：regular orthodromic AVRT 需要 AV node 成為迴路的一部分，阻斷它可能終止 reentry；pre-excited AF 則是 AF 的多個快速心房衝動可能繞過 AV node 經旁路進入心室。切斷 AV node 無法阻止 AF，也不會消除旁路，因而可能促使更快的 ventricular activation 與 VF。

所以「stable」只提供取得 12-lead ECG、監測、專科討論與考慮有限藥物介入的時間；**它不等於節律 benign，也不等於輸注藥物必然安全。** 真正需要確認的是，還不知道的部分是否仍在這項介入的可接受風險邊界內。

### 四個臨床分叉，在每一步改變什麼？

| 當下分支 | 能做的事 | 不能超出此資料推論 |
|---|---|---|
| Sinus tachycardia + shock，原因如感染、出血仍在 | 同步處理 underlying illness、補足灌流監測；檢查是否另有 arrhythmia | 不可因 HR 高、BP 低就電擊代償性的 sinus rhythm |
| Tachyarrhythmia 高度疑似造成 serious instability，regular monomorphic WCT、有 pulse | Prompt synchronized cardioversion，鎮靜不應延誤救援 | 不必等 VT 亞型／旁路位置確診 |
| Hemodynamically stable、regular monomorphic WCT，病因未明 | 12-lead ECG、監測／貼片備援、專家評估；依 2025 ALS 可考慮 adenosine 或適當 antiarrhythmic | 不能從 regular、monomorphic 或 adenosine 有效推出必為 SVT |
| Irregularly irregular WCT／高度疑 pre-excited AF | 停止套用一般 AF rate control；依不穩定程度選電復律，穩定時考慮 guideline-supported pathway-directed 藥物 | 不能盲用 AV nodal blockers 或由寬 QRS 一口咬定 VT |

2025 ALS 對一般 stable WCT 可考慮 IV **amiodarone、procainamide 或 sotalol**；但這並不覆蓋 **pre-excited AF** 的特殊禁忌：2023 AF guideline 明列 amiodarone 等 AV nodal blocking agents 在該情境的 VF 風險，穩定病人應使用 **IV procainamide／ibutilide** 或考慮電復律，並查 QT、心衰竭與血壓限制。**「廣義 WCT 的可選藥」和「特定 pre-excited AF 的禁藥」必須同時讀，不能互相代換。**

## 對照真實病例：同一個人，何時獲得足夠行動理由？

回到前篇 24 歲的真實病例。初見的是不規則 WCT，某些 pre-excited ventricular beats 快到 300/min；病人血壓一度仍維持。當下尚不一定能辨認哪一條 accessory pathway、是否典型左側或右側，也無法單靠 wide QRS 確診 VT。然而，高速且不規則、形態變化的 WCT 已足以禁止沒有明確適應症的 adenosine 或 AV nodal blocker 試探，並提醒團隊準備電復律／去顫與監測。

原病例曾在不確定機轉下使用 IV amiodarone，後續才 electrical cardioversion，轉律後見 delta wave，EP study 才確定 right posteroseptal accessory pathway。這些後得資訊改變了**最終病因診斷與長期策略（pathway ablation）**；卻不是當下是否必須避免危險藥物的必要前提。這就是 ACLS 所謂 **在不確定下仍能先行動** 的真實意義。

再把病例條件更改：如果同一張 ECG 其實是 *regular monomorphic* WCT、病人清醒且灌流良好，某些診斷性試探才可能進入容許範圍；如果下一分鐘出現 shock，等待的成本突然增高；如果節律明確為 sustained polymorphic VT，電擊必須改走 unsynchronized shock。**被改變的不是單純 diagnosis，而是診斷仍未知時可以承受的不確定程度。**

## 還需要知道什麼，已足以決定什麼？

Pocket Medicine 在 WCT 頁面問來源、傳導方向、心肌 substrate，讓我們知道 QRS 並非病名。ACLS 則把尚未查完病因的 rhythm，依當下灌流後果、ECG 可辨認的安全界線與治療延遲代價，暫時納入不同處置範圍。

兩者不是相反的方法，而是兩個不同時間尺度。機轉研究回答它為何發生；急救決策回答**在資料尚不完整時，哪一個錯誤不能發生**。

同一條 accessory pathway，能成為 reentry 的回程、順程，也能只是 AF 訊號進入心室的危險捷徑。先知道此刻在處理哪一種關係，才能理解為何一顆藥會從治療變成禁忌。

**病名可以尚未完整，行動的理由不能不完整。**

---

[完整來源、官方流程圖與界線](../arrhythmia-sources.md) · [從第一篇重新追傳導方向](2026-10-26-wpw-conduction-mechanism.md) · [回到知識地圖](../../clinical-os/index.md#rhythm)。

[AHA 2025 官方有脈搏心搏過速流程圖](https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-Tachycardia-250514.pdf?sc_lang=en)。
