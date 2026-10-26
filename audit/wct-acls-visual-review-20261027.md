# WCT／ACLS 核心流程圖：來源與視覺品質驗收（2026-10-27）

審查對象：`content/xiaoma-reading/integrated/2026-10-26-wct-acls-decision.md#wct-acls-main-algorithm`；作者 2026-10-27 明確指出舊文缺少最基本 ACLS 主流程，因此新圖不得退化為三段文字卡片或把原圖連結藏在 ECG 圖說中。

## 醫學／原圖對照

已查對官方 [2025 AHA Adult Tachyarrhythmia With a Pulse Algorithm](https://cpr.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-Tachycardia-250514.pdf) 的完整單頁圖及其 Doses/Details，並參照 [2025 ALS §15–16](https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/adult-advanced-life-support) 和 [2023 AF guideline §10.6](https://pmc.ncbi.nlm.nih.gov/articles/PMC11104284/)。

| 必須讀到的決策 | 新圖位置 | 限制 |
|---|---|---|
| 有脈搏，心率是否符合臨床情境（tachyarrhythmia 常 ≥150/min） | 起點框，desktop/mobile 各一份 | ≥150/min 是典型情境，**不是**可否治療的單一硬門檻 |
| Airway、低氧才補氧、監測、IV、12-lead | 起點框 | 初始支持不能延誤急救 |
| persistent tachyarrhythmia 是否 **causing** 低灌流／休克、意識、缺血、急性 HF | 第一個 Yes/No 分支 | 不能把代償性 sinus tachycardia 自動當成可電擊病因 |
| 若 Yes → usually synchronized cardioversion | 左側急救分支 | **sustained polymorphic VT** 需 immediate **unsynchronized** shock；無脈搏改 cardiac-arrest algorithm |
| 若 No → QRS ≥0.12 秒？ | 第二個 Yes/No 分支 | QRS 寬本身不是 VT 的確診 |
| stable wide QRS：adenosine only if regular **and** monomorphic；考慮 antiarrhythmic infusion、expert | wide 分支 | 不規則、polymorphic、unstable WCT 不給 adenosine；pre-excited AF 禁用 AV nodal blockers 與 IV amiodarone |
| stable narrow QRS：vagal／adenosine when regular；其他藥須對照適應症與禁忌 | narrow 分支 | 不是所有 narrow tachyarrhythmia 都適合 AV nodal blockade |
| refractory → 重估原因／下次電擊能量／藥物／專科 | 主圖後續行動框 | 原圖有完整藥物劑量／電擊設備細節，本站圖不複製也不取代 |
| 官方完整原圖應在文章開頭可直接取得 | 圖首醒目原始 PDF 連結，圖說再附一次 | AHA 原圖有授權限制；本站採獨立排列的教學決策圖，不宣稱為 AHA 正式演算法圖像 |

## 可視驗收觀察

1. **第一輪桌面截圖不合格**：起點第二行字跑出邊框；已縮短文字至「先評估心率與病況（通常 ≥150/min）」。
2. **第一輪 GitHub CI 截圖不合格**：缺少繁體中文字型，顯示成方框；已強制安裝 Noto CJK 字型且缺字時阻擋驗收。
3. **第一輪 CLI screenshot 手機 viewport 不可靠**：改用 Playwright 的明確 `viewport.width = 360 / 390`，另取桌面 1440px。
4. Playwright 改為檢查頁面實際 CSS viewport、水平溢出、桌面 SVG 起點前三行文字不得超出框架，並截取整張圖而非整個空白頁。這些檢查不能取代觀看實際截圖。
5. **保留完整文獻 ECG**：Silverman 2018 原始 ECG 以驗證過的 CC BY 4.0 原始像素使用，不以自生成 ECG 或缺檔占位圖替代。
6. **生圖因果界線**：圖只描繪操作前提和流程，不能從「irregular wide QRS」確診特定心律，也不能由暫時 stable 推論排除 VT。

## 發布決策邊界

- 單元測試、靜態連結、GitHub CI build 通過分別記錄，不互相代表。
- 真正桌面／手機截圖必須有可閱讀中文、沒有裁切，且相同圖的手機版不得只將 desktop SVG 縮小到模糊。
- 若無獨立人類醫師審核，記為 **AI source-checked／browser-QA reviewed**，不得標為已通過 human peer review。
- AHA 官方流程圖採原站直接連結，不鏡像原像素；若日後有合法授權再考慮嵌入官方原圖。
- **本記錄不憑自行填寫便使教學圖「合格」**；正式准入還需觀察 CI 中的三張實際截圖與對照圖意。

