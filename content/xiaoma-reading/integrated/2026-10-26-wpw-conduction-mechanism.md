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

<figure id="wpw-baseline-original" class="diuretic-figure" role="group" aria-label="正常房室傳導與 WPW 預激的真實公開學術原圖">
<div class="diuretic-figure-head"><span>REFERENCE ECG · WHY DELTA WAVE APPEARS</span><strong>先比較 normal conduction 和 pre-excitation 的 QRS 起始</strong></div>
<a href="https://upload.wikimedia.org/wikipedia/commons/f/f5/Electrocardiographic_findings_during_normal_atrioventricular_conduction_and_during_pre_excitation.jpg" target="_blank" rel="noopener noreferrer" aria-label="開啟 ECG 原始大圖"><img src="https://upload.wikimedia.org/wikipedia/commons/f/f5/Electrocardiographic_findings_during_normal_atrioventricular_conduction_and_during_pre_excitation.jpg" alt="正常房室傳導與 WPW pre-excitation 對照，標出 short PR、delta wave 及提早啟動的心室；Khan 2024 開放授權原圖" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;max-width:100%;border:1px solid #dde5e3;border-radius:8px;background:white"/></a>
<figcaption>正常傳導只有 AV node–His–Purkinje 作為心室啟動入口；預激時 AP 提前啟動部分心肌，形成 delta wave，隨後與正常傳導融合。原圖：Khan Z, Khan A, Cureus 2024, <a href="https://commons.wikimedia.org/wiki/File:Electrocardiographic_findings_during_normal_atrioventricular_conduction_and_during_pre_excitation.jpg">Wikimedia Commons</a>，<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>。未修改；此圖展示典型 ECG，不代表所有 AP 必然可在 resting ECG 看見。</figcaption>
</figure>

## 同一條旁路，在三種情況下做的是三種工作

**AVRT（atrioventricular reciprocating tachycardia）** 是心房、心室與兩條房室傳導途徑形成的 reentry：訊號由其中一條路下行，經另一條路返回心房，使迴路得以重複。它不是「一條旁路自己突然放電」，而是**旁路與正常傳導系統之間出現可持續的循環**。

在 **orthodromic AVRT**，衝動經 **AV node／His–Purkinje 下行**，再沿 **AP 逆行回心房**。既然心室仍由 His–Purkinje 系統啟動，通常呈 regular narrow QRS；合併 bundle branch block 等情況仍可能寬 QRS。這也解釋為什麼 concealed AP 雖無 resting delta wave，卻仍能形成 orthodromic AVRT：它只需要逆傳的一段。

在 **antidromic AVRT**，衝動改走 **AP 順向下行**，再經 AV node 或另一條 AP 回到心房。心室大部分由旁路所激發，QRS 因而通常既寬又規則。從表面 ECG 看，它可以與 VT 很相似，不能只靠「年輕、有 WPW history」就宣稱已經區分。

<figure id="wpw-pathway-figure" class="diuretic-figure" role="group" aria-label="醫學期刊公開授權：pre-excitation、orthodromic AVRT、antidromic AVRT 傳導與 ECG 原圖">
<div class="diuretic-figure-head"><span>FIGURE 01 · ORIGINAL MEDICAL FIGURE</span><strong>旁路作為「去程」或「回程」，QRS 外觀如何改變</strong></div>
<a href="https://upload.wikimedia.org/wikipedia/commons/2/26/Electrocardiographic_features_of_pre_excitation%2C_orthrodromic%2C_and_antidromic_AVRT.jpg" target="_blank" rel="noopener noreferrer" aria-label="開啟 ECG 原始大圖"><img src="https://upload.wikimedia.org/wikipedia/commons/2/26/Electrocardiographic_features_of_pre_excitation%2C_orthrodromic%2C_and_antidromic_AVRT.jpg" alt="Khan 與 Khan 2024 原圖：竇性預激、orthodromic AVRT、antidromic AVRT 的心臟傳導方向與 ECG 對照；可點圖放大" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;max-width:100%;border:1px solid #dde5e3;border-radius:8px;background:white"/></a>
<figcaption><strong>圖 1｜三種傳導情境不是三個病名階段。</strong> 左：sinus pre-excitation，正常與旁路傳導共同啟動心室；中：orthodromic AVRT 下行走 AV node–His–Purkinje，通常窄 QRS；右：antidromic AVRT 順向經旁路，通常寬 QRS。<strong>讀圖時對照 ECG，不是只記住箭頭顏色。</strong> 原圖：Khan Z, Khan A. Cureus 2024, <a href="https://doi.org/10.7759/cureus.62928">doi:10.7759/cureus.62928</a>，<a href="https://commons.wikimedia.org/wiki/File:Electrocardiographic_features_of_pre_excitation,_orthrodromic,_and_antidromic_AVRT.jpg">Wikimedia Commons 原檔</a>，<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>。未裁切／重繪；點圖可放大。這張圖呈現典型迴路，不足以由單張表面 ECG 證明真正的 AP 位置。</figcaption>
</figure>

三格圖透露一個差異：sinus pre-excitation 雖同時啟動兩條路，但沒有持續 reentry；orthodromic AVRT 的 AP 是**回程**，antidromic AVRT 的 AP 是**去程**。所以 QRS 描述的是「心室怎麼被啟動」，不是「迴路的所有必要組件」。

## Adenosine 可以中斷 AVRT，為什麼還不能說它一定安全？

Adenosine 可短暫阻斷 AV nodal conduction。對 hemodynamically stable、regular narrow-complex、機轉支持 AV-node-dependent 的 orthodromic AVRT，AV node 是迴路不可缺的一段；暫時切斷它，迴路便可能終止。這是機轉支持的處置理由，不是僅憑「長得像 SVT」試一顆藥。

但 adenosine 反應不會獨立證明 diagnosis：AVNRT 也會因 AV node 被阻斷而終止；某些 atrial tachycardia 和 adenosine-sensitive VT 也可有反應。並且 adenosine 有可能誘發 AF；有 antegrade-conducting AP 的病人一旦轉為 pre-excited AF，風險將截然不同。使用時需監測與準備緊急電復律／去顫能力。

這一篇解決了「**旁路在迴路裡的方向**」。但前面偷偷倚賴一項前提：心房訊號是**有組織的 reentry**。若心房改為大量快速、不規則的 AF 衝動，AP 甚至不需要參與任何 AVRT，也能使心室陷入危險。

[**接續 02｜Pre-excited AF：旁路不再是迴路，為什麼反而更危險？**](2026-10-26-preexcited-af.md)

*原始材料：Pocket Medicine 9E，私人 PDF 第 66–67 頁；[ESC 2019 SVT 指引 §11.3](https://academic.oup.com/eurheartj/article/41/5/655/5556821)。本稿為新的 AI 系列整合教材；2026/7/11 歷史 WPW 原稿全文尚未核得，並未冒稱其作者定稿。*


[**原圖、病例與 2025 AHA／2023 AF 來源逐項核對**](../arrhythmia-sources.md)。
