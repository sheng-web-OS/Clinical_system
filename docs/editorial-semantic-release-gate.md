# EPQC Semantic Release Gate｜讀者收益逐段審查

**目的**：阻止「每一句都可能正確，整頁卻不幫助理解」的教材上線。這個 gate 會驗證**實際完成逐段編輯審查的證據**，不以統計長度、引用數、圖量或 CI 綠燈冒充語意品質，也不自稱程式能判斷醫學真偽。

## 納管範圍與版本界線

- 任何公開 `/lessons/`、獨立 `/exams/` 詳解、`kind=ai_integrated` 或 `content/clinical-os/acs.md` 都屬於正式長篇教學稿，須納入語義審查。
- 導覽索引和純書目／圖像來源頁仍有讀者語氣規範，但主要由編輯資料外洩檢查及對應來源契約守護；不強迫把來源清單按長篇教學七軸評閱。
- 原始作者歷史稿保持 immutable，不因新制強迫改稿。
- `audit/editorial-semantic-baseline.json` 是導入本 gate 前的 **49 篇版本指紋（含啟用前已先發布的 HF／LVEDP）**，不是「舊稿品質全部通過」。不得因內容改寫而刷新 baseline；如正文與此版本不同，必須新增或更新 review receipt。新收錄的教材同理。版本指紋依 Git blob SHA 直接比對。

## 真正的語義審稿內容

對每一段有效閱讀文字（含具實質敘事的列表項）提問：

1. **讀者此處得到什麼**：補了哪個概念、機轉因果中介、證據解釋、處置選擇、例外、時間軸或必要導航？要能具體說明，不能只填「增加理解」。
2. **為何不能刪或合併**：若刪去這段，哪一個理解／決策關係失去前提？若只是重述前文，應標 `revise` 或 `remove`，不得宣稱 `keep`。
3. **推論是否超界**：資料只能支持什麼，不能推什麼？病例是實測還是假設？新指南、歷史考題、影像與圖表身分是否分清楚？

另按 [EPQC 七軸](editorial-prose-quality-contract.md) 做文章層級 A–G 評分（每軸至少 3，平均至少 3.3），附核心讀者問題、本文新增的理解以及對「其實不需要此稿／此段」最有力的反對理由。**任一醫學安全、證據虛構、因果斷裂、metadata 混入正文或重大來源衝突尚未解決，直接 HOLD，不可用平均分數補償。**

**全篇反向匹配（不得被段落 KEEP 補償）**：獨立審稿者在 A–G 與逐段審查之外，須直接對照**文章標題所承諾的臨床問題**、真正使用的病例在各時點已知／未知的資料、競爭機轉、所引研究的證據角色，以及正文**實際已回答**的問題。每段皆正確，卻用另一名病人的資料填上同題缺口，或用「新培養第 3 天才確認 ESBL」冒充「首劑前已有舊 ESBL AST」，仍屬**article-level topic–evidence mismatch**，先退回縮題／拆篇／重新研究；不可用七軸均分、真實病例標籤或 CI 綠燈解除。作者須先依 [EPQC §1A](editorial-prose-quality-contract.md) 完成開寫前可行性判斷；審稿者須**獨立重新檢驗**，不能僅採信作者自述。必要的判斷記入既有 PR／獨立審稿理由，**不變更 review JSON schema 或新增公開 metadata**。

## Agent 的最短交付流程

1. 撰稿／修訂完成後執行 `python site/semantic_gate.py --packet content/.../article.md`，產出帶有段落 ID、來源位置、摘錄與當前 Git blob 的**未核准草稿封包**；它不會自動填通過。
2. **與撰稿分開的獨立審稿脈絡**閱讀完整文章和必要原始來源，逐段辨認關係／冗餘，填寫每段 `role`、`reader_gain`、`nonredundancy_reason`、`verdict`；如有缺口，先退回修改正文，再生成新版封包。只允許全部 `keep` 及已解除硬性阻塞的版本發布。
3. 在私有 `audit/editorial-semantic-reviews.json` 的 `reviews[path]` 記錄已審完的封包、A–G 與 `reviewer_context`（`independent_ai_pass` 或 `human_editor`）及可追溯 `reviewer_reference`。**產生內容的 agent 不得把自己的同一輪自評偽裝成獨立審查。**
4. `python tools/validate.py` 加上正常 `bash tools/build_site.sh`，逐一確認版本一致、涵蓋全部段落、無空泛／重複的審查理由與七軸／hard-stop 通過。CI 任一失敗不得合併發布。修改任一正文後，先前 receipt 自動失效。

## 不能被誇大的部分

這套執行碼只驗證 **proof of review 的形式與精確文字覆蓋**：它無法可靠知道 reviewer 是不是在說真話，也不能靠 18 個字的理由或 A–G 自填分數證實讀者實際學會了。評論者是否真正獨立、醫學事實是否正確、Figure/Table 是否合法與忠實、實際手機可讀性和學習效率，都需要其他獨立的審查或量測。此工具從未呼叫推論 API，也不會在 CI 中自行生成「已通過」票據。

**最小維護原則**：僅新增／改動文章時審查；不把既有已發布稿一次重寫，不建全文 Claim Graph，不公開評分台帳，不要求使用者逐段下指令。重大 P0/P1 或發布權限問題仍依既有高風險決策閘門處理。既有 EJE 對 AI 是否能在使用者指出前獨立發現問題的研究，與這個 release receipt 是不同檢驗，不能互相冒充。
