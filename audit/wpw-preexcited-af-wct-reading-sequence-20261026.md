# WPW → Pre-excited AF → WCT／ACLS｜整合閱讀與驗收紀錄

日期：2026-10-26｜狀態：**三篇 AI 整合草稿完成、來源部分查核；HOLD 待醫學獨立校閱與出版驗收**。

## 正式閱讀順序：同一機轉模型，三個逐步改變的問題

1. [WPW：同一條旁路，為什麼可以產生窄 QRS，也可以產生寬 QRS？](../content/xiaoma-reading/integrated/2026-10-26-wpw-conduction-mechanism.md)  
   **問題**：心房訊號在哪個方向、經哪條路啟動心室？  
   **必備理解**：AV nodal decremental conduction、manifest/concealed AP、short PR＋delta wave 的融合機轉；orthodromic down AV node/up AP 與 antidromic down AP/up AV node（或第二 AP）。  
   **讀完檢核**：有 WPW pathway，為什麼一場 tachycardia 可以 QRS 窄，另一場卻寬？為什麼沒有 resting delta wave 不能排除 concealed pathway？

2. [同樣有 accessory pathway，為什麼 adenosine 一次是治療，一次可能致命？](../content/xiaoma-reading/integrated/2026-10-26-preexcited-af.md)  
   **問題**：當心房由 single reentry 改為 AF，多個快速衝動從哪個路徑抵達心室？  
   **必備理解**：pre-excited AF 不等於 antidromic AVRT；不規則 QRS 可因不同程度預激與 fusion 而變化；AV node 阻斷在 pre-excited AF 危險；SPERRI 與 accessory pathway ERP 不能當同一數字。  
   **證據錨點**：24 歲男性 2018 case report（原始 irregular wide QRS、極快速 pre-excited beats、轉律後 delta wave、EP 消融）；**病例中先給 IV amiodarone 是歷史事實，非建議**。  
   **讀完檢核**：把原本的 regular narrow AVRT 換成 irregular pre-excited AF，為何 adenosine 的用途由「中斷迴路」變成「禁忌」？

3. [還不知道是什麼，憑什麼治療：從 WPW 走到 WCT／ACLS](../content/xiaoma-reading/integrated/2026-10-26-wct-acls-decision.md)  
   **問題**：血流動力學與 rhythm morphology 只提供部分資訊，何時已足以行動？  
   **必備理解**：causing shock vs compensatory tachycardia；WCT 的 activation route ≠ diagnosis；stable regular monomorphic WCT 是可考慮特定處置的**局部條件**；unstable WCT、polymorphic VT、pre-excited AF 的不同電擊與藥物邊界。  
   **讀完檢核**：同為 WCT，哪個條件改變時要從 diagnostic attempt 轉為立即 synchronized cardioversion？何時必須用 unsynchronized shock？

**此序列不另外建立第二套公開知識地圖。** 發行通過後只需在既有 `content/clinical-os/index.md` 的急症／心臟節點補上一條最短的因果閱讀路線，並以 `site/pages.json` 明列三頁；不為此增加網站導航框架或常駐 agent。

## 原稿與增量分界

- 2026-07-17 作者〈還不知道是什麼，憑什麼治療〉已在 `archive/xiaoma-reading/intake/2026-07-17-wct-acls-user-supplied.md` 原文保存；新的第三篇是不同檔案，不修改、冒充或取代歷史版本。
- 2026-07-11 作者〈Accessory pathway ＆ WPW syndrome〉曾存在早期對話／編輯記錄；本次尚未取得可逐字核對的 **完整最終作者原文**，不建立杜撰的 originals 檔。新第一篇為 AI 整合稿，不能主張新增了作者當年已掌握的 orthodromic／antidromic／pre-excited AF 概念。
- 作者已完成的 A 類理解：WCT 不是 VT 診斷、hemodynamic consequence 不是 rhythm 固定屬性、regular/monomorphic 是局部操作限制、adenosine response 不能證明 SVT。整合文章只保留該理路並補必要的 B 跨篇傳導及 D 安全限定。
- B 類跨篇橋：同一 accessory pathway 隨 rhythm 改變在 circuit／ventricular conduction 的功能，進一步決定 AV nodal blocker 角色。這是整組閱讀主線，不另建大型依賴圖。
- D 類醫學校正：2025 AHA 的 **stable regular monomorphic WCT adenosine Class IIb**，unstable/irregularly irregular/polymorphic WCT **Class III Harm**；2023 AF §10.6 pre-excited AF 的 AV nodal blockers（含 amiodarone）**Class III Harm**，與一般 stable WCT antiarrhythmic 列表不得混合。持續性 polymorphic VT 需 immediate **unsynchronized** shock，hemodynamically unstable pre-excited AF 原則使用 **synchronized** cardioversion。無脈搏另外進入 arrest algorithm。

## 證據查核與圖像

| 項目 | 核對層級 | 尚未完成 |
|---|---|---|
| Pocket Medicine 9E WPW、SVT、WCT | 本次由 Library 原 PDF **逐頁讀取含頁面圖像的 PDF 第 66–68 頁**；含 SVT Figure 1-3、表格註腳及 accessory pathway/WCT 頁面 | 不能公開重製出版社原圖；正式 published edition 別頁碼未比對 |
| AHA ACLS tachyarrhythmia | **2025 官方流程圖 PDF** 及 HTML ALS 指引 §15–17，並以 web PDF screenshot 視覺核對 | 公開站只合法連結，不直接複製完整圖像 |
| Pre-excited AF | 2023 ACC/AHA/ACCP/HRS AF guideline §10.6 recommendation table and rationale | 新稿仍待獨立醫學審稿 |
| 2018 24 歲病人 | Case report https://pmc.ncbi.nlm.nih.gov/articles/PMC6166305/（可讀網路摘要與報導內容） | ECG image 不重製；目前個別全文開啟遇網站驗證，圖像未實際目視，因此稿內只轉述已取得的文字描述 |
| 2018 adenosine 後 AF 病人 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5840850/ 本次讀到內文、圖說、結果；可作風險反例 | 若公開要附 ECG，仍需逐圖合法性判斷 |

## 反事實測試（與內容一致）

1. **Same patient, same accessory pathway, rhythm changes**：stable regular narrow orthodromic AVRT → irregular WCT/pre-excited AF；adenosine 從可考慮轉為禁忌。若讀者依 WPW 標籤而非節律選藥即為安全失誤。
2. **Same rhythm, hemodynamic status changes**：stable regular monomorphic WCT → hypotension attributable to rhythm；可討論用藥轉為 prompt cardioversion，避免診斷延誤。
3. **Same wide QRS, morphology changes**：monomorphic → sustained polymorphic VT；不能繼續使用只為 monomorphic WCT 的 synchronized-shock 假設；需 immediate unsynchronized shock。
4. **Same rate, different causality**：septic shock 的 compensatory sinus tachycardia vs shock-causing VT；不能只依 HR 或 BP 選擇電擊。
5. **Same antidromic WCT appearance, different mechanism**：疑 antidromic AVRT vs VT；不可因有 WPW history 而忽略 VT。

## 發行判準

- 原稿保真：作者 WPW 正稿未找回，因此 **originals 未增加**；7/17 完整 source snapshot 保留。
- 目前新增的是三份 **AI integration drafts**，不是公開教材；`site/pages.json` **未新增**；正式 Cloudflare 部署 **未觸發**。
- 需要完成：對第一篇「concealed vs manifest AP」及 antidromic 描述的獨立醫學核對；對第二／三篇之 preexcited AF、polymorphic VT、高危用藥的 P0/P1 reviewer check；合法原創視覺圖設計與手機可讀性；EPQC 審查；`bash tools/build_site.sh`、完整測試、再確認 HTTPS 公網。
- Source PDF/圖像保存在使用者 Library／本次對話，**不得將私人出版社原 PDF 或頁面直接寫入公開站**。未獲正式授權也不重製原像素。

結論：本輪完成了「從傳導方向經過 AF risk，再走向急救決策」的**完整可閱讀稿件與因果閱讀序列**；目前屬於 GitHub draft，不得以稿件完整或 model 自評冒稱醫學審查與網站發布完成。
