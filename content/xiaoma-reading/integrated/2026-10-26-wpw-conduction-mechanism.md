# WPW：心室明明只有一個，為什麼同一條旁路能讓 QRS 又窄又寬？

*小麻閱讀（9E）｜心律急症系列 01／03：從傳導方向開始。*

**系列閱讀：本篇「傳導路徑」 → [02｜Pre-excited AF：被阻斷的是哪一條路？](2026-10-26-preexcited-af.md) → [03｜WCT／ACLS：診斷未定時如何行動？](2026-10-26-wct-acls-decision.md)**

讀到 Wolff–Parkinson–White（WPW）時，最容易被三個 ECG 名詞困住：short PR interval、delta wave、wide QRS。它們看似是一組能直接認出病名的訊號；然而，下一次病人心悸發作時，QRS 可能是窄的，也可能又寬又規則，甚至寬度不一、快得驚人。

如果 WPW 就是「有一條 extra pathway」，為何它產生的 tachycardia 沒有固定的 QRS 形態？

答案必須先把三件事分開：**旁路是否存在、這一搏心室從哪裡被啟動、以及這個 tachycardia 是否依賴某條路徑持續循環**。三個問題彼此相關，卻不是同一件事。

## QRS 不是路徑的名稱，而是心室如何被啟動的結果

正常 sinus impulse 先經心房，再通過 AV node、His bundle 與 Purkinje system，最後快速啟動心室。AV node 的生理延遲形成 PR interval 的一部分；它具有 decremental conduction，當心房輸入愈快，傳導常愈慢，因此對心室形成重要的篩選作用。**AV node 不只是一段電線，也是一個會限制傳導速度的節點。**

Accessory pathway（AP）是心房與心室之間額外存在的肌性傳導連結。典型 AP 的傳導與 AV node 不同：有能力讓心房衝動繞過正常 AV nodal delay，直接提前激發部分心室肌。

在 sinus rhythm，若這條 AP 能順向（atrium → ventricle）傳導，同一個心房衝動可沿 **AV node／His–Purkinje** 與 **AP** 同時抵達心室。AP 先激發的一小部分心室肌，以肌肉間相對緩慢的方式擴散，形成 QRS 開始時鈍化的 *delta wave*；接著由 His–Purkinje 快速到達的波前參與激發，產生 fusion QRS。因此 short PR、delta wave 與 QRS widening 不是三個互不相干的病徵，而是 **部分心室提前啟動** 的不同面向。

但不是每條 AP 都能順向傳導。有些只准許 ventricle → atrium 逆傳（**concealed AP**），因此 resting sinus ECG 可以完全沒有 delta wave；某些具順傳能力的 AP 也可能因傳導速度、位置與融合程度而沒有明顯的 resting pre-excitation。**沒有 delta wave，不能排除可參與 tachycardia 的 AP。**

此處先區分：**accessory pathway** 是通道；**WPW pattern** 是 ECG 呈現的 ventricular pre-excitation；**WPW syndrome** 還涉及相關的臨床 tachyarrhythmia。Pattern 不代表當下正在發作 AVRT，也不代表所有發作必須經 AP 順傳。

## 同一條旁路，在三種情況下做的是三種工作

**AVRT（atrioventricular reciprocating tachycardia）** 是心房、心室與兩條房室傳導途徑形成的 reentry：訊號由其中一條路下行，經另一條路返回心房，使迴路得以重複。它不是「一條旁路自己突然放電」，而是**旁路與正常傳導系統之間出現可持續的循環**。

在 **orthodromic AVRT**，衝動經 **AV node／His–Purkinje 下行**，再沿 **AP 逆行回心房**。既然心室仍由 His–Purkinje 系統啟動，通常呈 regular narrow QRS；合併 bundle branch block 等情況仍可能寬 QRS。這也解釋為什麼 concealed AP 雖無 resting delta wave，卻仍能形成 orthodromic AVRT：它只需要逆傳的一段。

在 **antidromic AVRT**，衝動改走 **AP 順向下行**，再經 AV node 或另一條 AP 回到心房。心室大部分由旁路所激發，QRS 因而通常既寬又規則。從表面 ECG 看，它可以與 VT 很相似，不能只靠「年輕、有 WPW history」就宣稱已經區分。

<figure id="wpw-pathway-figure" class="diuretic-figure" role="group" aria-label="三種 accessory pathway 傳導角色的原創示意圖">
<div class="diuretic-figure-head"><span>FIGURE 01 · CONDUCTION, NOT DIAGNOSIS</span><strong>同一套解剖通道，改變下行路徑就改變 QRS</strong></div>
<div role="region" aria-label="三種傳導路徑示意圖，手機可水平捲動" tabindex="0" style="max-width:100%;overflow-x:auto">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 366" width="900" height="366" role="img" aria-labelledby="wpwfig-title wpwfig-desc">
<title id="wpwfig-title">Sinus pre-excitation、orthodromic AVRT、antidromic AVRT 傳導路徑</title>
<desc id="wpwfig-desc">三個面板共用心房、AV node、心室與 accessory pathway。左：竇性預激沿 AV node 與旁路同時下傳形成 fusion；中：orthodromic AVRT 走 AV node 下行、旁路逆傳，通常窄 QRS；右：antidromic AVRT 走旁路下行、AV node 或其他路逆傳，通常寬 QRS。顏色與箭頭只顯示方向，不代表真實心臟空間位置。</desc>
<defs><marker id="wblue" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="#147b9a"/></marker><marker id="worange" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="#bc693e"/></marker></defs>
<rect width="900" height="366" rx="14" fill="#f7faf9"/>
<rect x="15" y="18" width="280" height="325" rx="10" fill="white" stroke="#d8e3e0"/><rect x="310" y="18" width="280" height="325" rx="10" fill="white" stroke="#d8e3e0"/><rect x="605" y="18" width="280" height="325" rx="10" fill="white" stroke="#d8e3e0"/>
<g font-family="sans-serif" text-anchor="middle" fill="#203938">
<text x="155" y="43" font-size="17" font-weight="bold">Sinus pre-excitation</text><text x="450" y="43" font-size="17" font-weight="bold">Orthodromic AVRT</text><text x="745" y="43" font-size="17" font-weight="bold">Antidromic AVRT</text>
</g>
<g fill="#e6eeeb" stroke="#607c74" stroke-width="1.5"><rect x="94" y="73" width="120" height="40" rx="12"/><rect x="94" y="240" width="120" height="40" rx="12"/><rect x="389" y="73" width="120" height="40" rx="12"/><rect x="389" y="240" width="120" height="40" rx="12"/><rect x="684" y="73" width="120" height="40" rx="12"/><rect x="684" y="240" width="120" height="40" rx="12"/></g>
<g font-family="sans-serif" fill="#203938" font-size="17" text-anchor="middle"><text x="154" y="98">心房 A</text><text x="154" y="266">心室 V</text><text x="449" y="98">心房 A</text><text x="449" y="266">心室 V</text><text x="744" y="98">心房 A</text><text x="744" y="266">心室 V</text></g>
<g font-family="sans-serif" font-size="13" fill="#36546b" text-anchor="middle"><text x="106" y="184">AV node</text><text x="401" y="184">AV node</text><text x="696" y="184">AV node</text></g>
<g font-family="sans-serif" font-size="13" fill="#965b34" text-anchor="middle"><text x="246" y="184">AP</text><text x="541" y="184">AP</text><text x="836" y="184">AP</text></g>
<g stroke="#147b9a" stroke-width="5" fill="none" stroke-linecap="round"><path d="M127 116 L127 224" marker-end="url(#wblue)"/><path d="M422 116 L422 224" marker-end="url(#wblue)"/><path d="M718 230 L718 120" marker-end="url(#wblue)"/></g>
<g stroke="#bc693e" stroke-width="5" fill="none" stroke-linecap="round"><path d="M199 116 L199 224" marker-end="url(#worange)"/><path d="M493 231 L493 120" marker-end="url(#worange)"/><path d="M792 116 L792 224" marker-end="url(#worange)"/></g>
<g font-family="sans-serif" font-size="16" text-anchor="middle"><text x="155" y="312" fill="#315a53">fusion → δ wave</text><text x="450" y="312" fill="#315a53">通常窄 QRS</text><text x="745" y="312" fill="#315a53">通常寬 QRS</text></g>
</svg></div>
<figcaption><strong>圖 1｜路徑、方向與心室激發是不同層次。</strong> 藍色為 AV node／His–Purkinje 相關路，橘色為 AP；箭頭代表該情況的主要傳導方向。右圖僅示典型 AV node 逆傳情境，亦可能經另一條 AP 逆傳。依 Pocket Medicine 9E 與 ESC 2019 的傳導敘述重新設計，非原圖、非依 ECG 判定實際 pathway 位置。手機可左右滑動，圖後仍提供完整文字推導。</figcaption>
</figure>

三格圖透露一個差異：sinus pre-excitation 雖同時啟動兩條路，但沒有持續 reentry；orthodromic AVRT 的 AP 是**回程**，antidromic AVRT 的 AP 是**去程**。所以 QRS 描述的是「心室怎麼被啟動」，不是「迴路的所有必要組件」。

## Adenosine 可以中斷 AVRT，為什麼還不能說它一定安全？

Adenosine 可短暫阻斷 AV nodal conduction。對 hemodynamically stable、regular narrow-complex、機轉支持 AV-node-dependent 的 orthodromic AVRT，AV node 是迴路不可缺的一段；暫時切斷它，迴路便可能終止。這是機轉支持的處置理由，不是僅憑「長得像 SVT」試一顆藥。

但 adenosine 反應不會獨立證明 diagnosis：AVNRT 也會因 AV node 被阻斷而終止；某些 atrial tachycardia 和 adenosine-sensitive VT 也可有反應。並且 adenosine 有可能誘發 AF；有 antegrade-conducting AP 的病人一旦轉為 pre-excited AF，風險將截然不同。使用時需監測與準備緊急電復律／去顫能力。

這一篇解決了「**旁路在迴路裡的方向**」。但前面偷偷倚賴一項前提：心房訊號是**有組織的 reentry**。若心房改為大量快速、不規則的 AF 衝動，AP 甚至不需要參與任何 AVRT，也能使心室陷入危險。

[**接續 02｜Pre-excited AF：旁路不再是迴路，為什麼反而更危險？**](2026-10-26-preexcited-af.md)

*原始材料：Pocket Medicine 9E，私人 PDF 第 66–67 頁；[ESC 2019 SVT 指引 §11.3](https://academic.oup.com/eurheartj/article/41/5/655/5556821)。本稿為新的 AI 系列整合教材；2026/7/11 歷史 WPW 原稿全文尚未核得，並未冒稱其作者定稿。*
