# A–a gradient 變大，為什麼還無法診斷 shunt？

<div class="opening-question"><span class="small-label">Respiratory Failure｜深入三問之一</span><p>一位病人的 PaO₂ 只有 55 mmHg。這究竟是肺泡本來就缺氧，還是氧氣已經進入肺泡，卻無法轉成足夠的動脈氧合？當你提高 FiO₂，答案又為什麼不一定立即清楚？</p></div>

這一篇不是再背五種 hypoxemia 原因。原書《Pocket Medicine》第九版 PDF 第 105 頁 **Figure 2-5 Workup of acute hypoxemia** 的三個判斷動作是：比較肺泡與動脈氧分壓、觀察增加吸入氧後的反應、再考慮運動及臨床條件。真正難的是，每個動作能回答什麼，以及**不能**回答什麼。先把測量位置釐清，再回到真實病例。

## 第零問｜從肺泡走到動脈，究竟哪個量在改變？

空氣進入肺泡，形成肺泡氧分壓 **PAO₂**；血液經過肺循環後，測到動脈氧分壓 **PaO₂**。PAO₂ 通常從氣體方程式推算；PaO₂ 則由動脈血氣測得。兩者差距 **A–a gradient = PAO₂ − PaO₂**，是在衡量「動脈為何沒有達到預期肺泡氧分壓」，**不是**穿過肺泡膜的擴散速度，也不是血液少了多少氧含量。

<div class="equation"><strong>PAO₂ ≈ FiO₂ ×（PB − 47）− PaCO₂/R</strong><strong>A–a gradient = PAO₂ − PaO₂</strong><small>海平面、室內空氣、37°C、呼吸商 R ≈ 0.8 時，PAO₂ ≈ 150 − PaCO₂/0.8；高海拔、FiO₂ 改變或不穩態時，不應機械套用 150。</small></div>

<figure id="oxygen-locations" class="vq-comparison"><div><span class="small-label">肺泡內</span><strong>PAO₂</strong><p>吸入氧分壓與肺泡 CO₂ 共同決定；低通氣使 PaCO₂ ↑，PAO₂ 相應下降。</p></div><div><span class="small-label">血液通過肺後</span><strong>PaO₂</strong><p>受全肺 V/Q 分布、分流、擴散及血液混合影響，並非某一肺泡的讀數。</p></div><div><span class="small-label">兩者落差</span><strong>A–a gradient</strong><p>定位氧合不良是否超出肺泡氧分壓降低所能解釋的程度，不能直接診斷單一疾病。</p></div><figcaption>依 Pocket Medicine 9E PDF 第 105 頁 Figure 2-5 的定位軸獨立重繪，不複製原書影像；同一位病人可能同時有低通氣與 V/Q 異常。完整來源與界限見<a href="../respiratory-deep-dive-sources.md#pocket-hypoxemia">圖表來源</a>。</figcaption></figure>

## 第一問｜A–a gradient 正常時，為什麼 PaO₂ 仍可能很低？

先比較三個**生理模型**。三組 ABG 是為了分解方程式而自行設定，**不是病例報告中的患者數值**。假設 40 歲、海平面、室內空氣，預期 A–a 上限約為 age/4 + 4 = 14 mmHg。

| 模型 | PaCO₂ | PaO₂ | 推得 PAO₂ | A–a | 生理判讀 |
| --- | ---: | ---: | ---: | ---: | --- |
| A：單純低通氣 | 70 | 53 | 62.5 | 9.5 | 肺泡氧分壓下降已解釋大部分低氧 |
| B：氧合障礙 | 40 | 55 | 100 | 45 | 肺泡與動脈出現額外落差 |
| C：混合型 | 70 | 35 | 62.5 | 27.5 | 低通氣加上肺內氧合障礙 |

A 與 B 的 PaO₂ 幾乎相同；如果只看低血氧程度，就看不出它們是不同問題。A 的氧氣本來就沒有在肺泡內建立足夠分壓，B 則是肺泡氧分壓尚足，卻無法在動脈保留相應的氧合。

但要注意另一個反例：**A–a 增大並不要求 PaCO₂ 正常。**在肺炎合併呼吸肌疲乏、COPD 合併 atelectasis 或肺水腫時，PaCO₂ 可同時升高；它不會把既有的 V/Q mismatch 自動消掉。原圖「↑ A–a + normal PaCO₂」只是典型說明，不是排他性條件。

A–a 也不是所有年齡固定小於 10。教學近似式可以使用 age/4 + 4 或 2.5 + 0.2 × age，但不同公式不完全相同；這些主要是**室內空氣、近似正常肺生理**的判讀輔助，不能搬到高 FiO₂ 仍沿用。

## 第二問｜為什麼低 V/Q 可以對氧氣有反應，true shunt 卻往往不行？

**V 是 alveolar ventilation，Q 是 perfusion。**肺是許多不同 V/Q 單位的集合，不是單一平均肺泡。當區域通氣減少但灌流保留，形成 low V/Q；如果通氣完全歸零但灌流仍有，便是 true shunt 的極端。另一端若肺泡有通氣卻沒有灌流，V/Q 趨近無限大，形成 alveolar dead space。

<figure id="vq-spectrum" class="vq-comparison"><div><span class="small-label">V/Q = 0</span><strong>True shunt</strong><p>血流經過完全不通氣的肺單位，或繞過肺循環；增加 FiO₂ 無法直接讓這部分血液接觸肺泡氧氣。</p></div><div><span class="small-label">V/Q 偏低但大於 0</span><strong>Low V/Q</strong><p>仍有氧氣進入肺泡；增加 FiO₂ 可提高局部 PAO₂，通常改善經此區域流出血液的氧合。</p></div><div><span class="small-label">V/Q 很高至無限大</span><strong>Dead-space physiology</strong><p>通氣相對浪費。沒有灌流的肺泡不會產生一股低氧血直接流出；但會增加呼吸的總換氣需求。</p></div><figcaption>依 Pocket Medicine 9E Figure 2-5 的 shunt、V/Q mismatch、diffusion 分支重新組合成連續光譜；不是原書分類樹的逐字複製。疾病可包含多種肺單位，並非選一格就完成診斷。</figcaption></figure>

為什麼高 V/Q 肺區不能完全補回低 V/Q 肺區損失的氧？因為**血液混合遵守 oxygen content，不是先平均 PaO₂。**在 Hb 氧解離曲線的平台區，正常肺區 Hb 已近 100% 飽和，提高 PaO₂ 只能使 Hb 結合氧小幅增加；但低 V/Q 區域的 Hb 飽和度可能下降很多。

用一個**數學模型，不是病例實測**說明：若 80% 的血流離開正常肺區時飽和度近 100%，20% 經完全無通氣單位、保留 SvO₂ 70%；在相同 Hb 且暫忽略溶解氧的情況下，混合後飽和度約 **0.8 × 100% + 0.2 × 70% = 94%**。這一步不是把兩個 PaO₂ 直接平均。

不過，原書寫「shunt 不能被 100% O₂ 克服」應讀作**反應受限**，不能理解為氧合絕對不變。吸入高濃度氧時，正常肺區血漿的**溶解氧**仍可增加：

<div class="equation"><strong>CaO₂ ≈ 1.34 × Hb × SaO₂ + 0.003 × PaO₂</strong><small>單位 mL O₂/dL blood；提高 PaO₂ 即使不再增加 Hb 飽和度，仍能增加溶解氧。它可以部分改善混合後的 CaO₂，但無法讓真正繞過氧合的血液直接接觸肺泡。</small></div>

再往深一層，分流造成的 PaO₂ 下降，也受到**混合靜脈氧含量**影響：

<div class="equation"><strong>Qs/Qt = (Cc′O₂ − CaO₂) / (Cc′O₂ − Cv̄O₂)</strong><small>Qs/Qt 為分流比例；Cc′O₂ 為理想肺毛細血管末端含氧量；CaO₂ 為動脈含氧量；Cv̄O₂ 為混合靜脈含氧量。必須以氧含量推算，並有適當採樣與模型條件。</small></div>

若同樣分流 20%，但休克使 cardiac output 下降、組織擷取增加、混合靜脈 SvO₂ 下降，進入分流的那股血就更缺氧，最終 PaO₂ 可能更差。**低氧惡化可能同時包含肺與循環的變化。**

### 真實病例｜為何平躺 SpO₂ 99%，站起來卻只有 80–83%？

Kakura 等人於 2026 年發表一名 **74 歲女性**的 platypnea–orthodeoxia syndrome（POS）病例。她在直立時 SpO₂ 約 **80–83%**，平躺時約 **95–99%**。TEE 發現 PFO、心房中隔瘤及姿勢依賴性的右向左分流；CT 見主動脈延長、右心房受壓。經導管 PFO closure 後，低氧獲得改善。[原始病例及出版社圖解](https://doi.org/10.1016/j.jaccas.2026.107626)。

這不是說所有 PFO 都要關閉，而是證明**解剖通道與姿勢、心房幾何、靜脈血流方向共同決定當下是否真的分流**。若檢查全程平躺，可能低估姿勢依賴性的異常。此處沒有把病例補造成帶有 PaCO₂、FiO₂ 或 A–a 數字的範例，因為文獻並未提供足以完成同一時間點計算的組合。

由這個病例回到原圖：A–a gradient 會隨當下狀態改變；「分流」不必然由肺部實質病灶造成，更不能從補氧反應單獨決定是哪一種分流。

## 第三問｜為什麼同樣肺炎會同時列在 V/Q mismatch 與 shunt？運動低氧又代表什麼？

肺炎或肺水腫不是單一 V/Q 狀態。同一個肺內，有的肺泡部分充滿液體但仍通氣（low V/Q），有的完全塌陷或充滿液體（接近 true shunt），有的仍正常，有的通氣相對灌流過多。臨床測到的 PaO₂，是這些肺區輸出血液依**氧含量**混合後的結果。

因此，FiO₂ 反應差是分流成分的線索，但不能將一整個肺炎病人都等同於完全 true shunt。**PEEP 也和提高 FiO₂ 在做不同工作：**前者可能重新打開可復張的肺泡，使某些原本 V/Q≈0 的區域恢復通氣；後者主要提高已能通氣之肺泡的氧分壓。過高 PEEP 可造成過度擴張、減少靜脈回流及灌流，並非保證改善氧合。

肺栓塞則提供相反的例子：受阻肺區可有高 V/Q 甚至 dead space，但低氧更多牽涉肺血流重新分配後的低 V/Q、心輸出量及有時的分流。**Dead space 的本質是通氣浪費，不是每一個無灌流肺泡都流出一股低氧血。**

原圖把 diffusion limitation 連到 exercise / ↑ cardiac output，是在對比「紅血球通過肺毛細血管的時間」與「氧氣完成擴散平衡的時間」。正常休息時通過時間常近似 0.75 秒，而氧氣平衡多在前約 0.25 秒完成；運動縮短通過時間，若 ILD 使膜增厚或有效交換面積減少，就可能暴露原本在休息時尚能補償的不足。這些是生理近似值，不是所有病人的固定秒數。

但 **exercise desaturation ≠ 單純 diffusion limitation**。ILD 的運動低氧也常同時受到 V/Q mismatch、肺血管床減少及混合靜脈含氧量影響；DLCO 低也不是單獨證明膜擴散速度異常，因為它還受 Hb 與肺毛細血管血液容積影響。

### 重新回到病人床邊

| 病人觀察 | 最合理的下一個問題 | 不能直接下的結論 |
| --- | --- | --- |
| 低 PaO₂、A–a 大致正常 | 是否低通氣、低吸入氧分壓？ | 沒有其他共存肺病 |
| A–a 擴大 | 哪些 V/Q 單位或分流造成動脈氧合落差？ | 一定是 diffusion limitation |
| 高 FiO₂ 後仍低氧 | 是否有顯著 shunt、塌陷或複合肺病？ | 所有肺單位都 V/Q = 0 |
| 運動時才低氧 | 是否有擴散儲備、V/Q 或肺循環問題？ | DLCO 低就可完成診斷 |
| 姿勢改變後明顯低氧 | 是否有姿勢依賴性的右向左分流？ | 平躺時一次正常檢查就能排除 |

**結論：** A–a gradient 幫忙發現「肺泡氧分壓不能完全解釋動脈氧合」；高 FiO₂ 反應則探索有多少血流能接觸被提高氧分壓的肺泡。但要理解真實病人，還必須把區域 V/Q、氧含量混合、混合靜脈血、循環與時間一起放回來。這些計算不能取代急性低氧的立即評估與氧合、通氣支持。

[接續深入：為什麼 RR 40/min，PaCO₂ 仍會升高？](2026-10-25-hypercapnia-physiology.md)・[原有低血氧基礎篇與正式國考題](2026-10-21-hypoxemia.md)・[病例、原圖與查核來源](../respiratory-deep-dive-sources.md)
