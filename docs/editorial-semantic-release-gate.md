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

## 獨立推理連續性閘門（2026-10-27）

推理連續性不是 EPQC E 軸高分可以概括代替的項目。每個新編／實質修改的長篇教材須另填 `continuity_gate`，審核 **concept／causal／decision／narrative** 四類斷裂；任一類判定 HOLD、未完成審查或存在 `unresolved_gaps`，即使其餘 EPQC 七軸滿分也不能發布。另將 `broken_narrative_continuity` 納入不可補償的 `hard_stops`。

- 審稿者通讀原文，逐一檢視相鄰教學段落的接續，尤其是術語首次出現、圖表與公式引入、從檢查走到處置的位置；標明 `all_transitions_checked`。不得將清單、編輯筆記或空洞過渡詞當作因果橋梁。
- 四種 `checks` 各自記錄 `verdict=pass` 及**對本稿特定內容的** `evidence`；填入一組真實相鄰單元的 `sample_handoff`（`from_id`／`to_id`／`reader_question`／`bridge_justification`）。`unresolved_gaps` 必須為空，文章版號與獨立 reviewer provenance 仍遵循同一筆 semantic receipt。
- 本項 gate **只新增精簡的審查證據，不要求逐段複製全套交接文字**；原本 paragraph receipt 仍負責覆蓋每個實質段落。任何重大斷裂必須先回到正文補上推理，再重做版本化審查。

`site/semantic_gate.py` 只能驗證欄位、已宣告的判定與例證 ID 是否真是相鄰段落；**無法證明「全部已讀」或文字真的連貫**。其成功不等於臨床品質、獨立審查的真實性或讀者學習成效已證明。舊版 frozen baseline 不因新增 gate 而宣稱通過，也不可藉修改舊 SHA 規避本規範。

## Agent 的最短交付流程

1. 撰稿／修訂完成後執行 `python site/semantic_gate.py --packet content/.../article.md`，產出帶有段落 ID、來源位置、摘錄與當前 Git blob 的**未核准草稿封包**；它不會自動填通過。
2. **與撰稿分開的獨立審稿脈絡**閱讀完整文章和必要原始來源，逐段辨認關係／冗餘，填寫每段 `role`、`reader_gain`、`nonredundancy_reason`、`verdict`；如有缺口，先退回修改正文，再生成新版封包。只允許全部 `keep` 及已解除硬性阻塞的版本發布。
3. 在私有 `audit/editorial-semantic-reviews.json` 的 `reviews[path]` 記錄已審完的封包、A–G 與 `reviewer_context`（`independent_ai_pass` 或 `human_editor`）及可追溯 `reviewer_reference`。**產生內容的 agent 不得把自己的同一輪自評偽裝成獨立審查。**
4. `python tools/validate.py` 加上正常 `bash tools/build_site.sh`，逐一確認版本一致、涵蓋全部段落、無空泛／重複的審查理由與七軸／hard-stop 通過。CI 任一失敗不得合併發布。修改任一正文後，先前 receipt 自動失效。

## 不能被誇大的部分

這套執行碼只驗證 **proof of review 的形式與精確文字覆蓋**：它無法可靠知道 reviewer 是不是在說真話，也不能靠 18 個字的理由或 A–G 自填分數證實讀者實際學會了。評論者是否真正獨立、醫學事實是否正確、Figure/Table 是否合法與忠實、實際手機可讀性和學習效率，都需要其他獨立的審查或量測。此工具從未呼叫推論 API，也不會在 CI 中自行生成「已通過」票據。

**最小維護原則**：僅新增／改動文章時審查；不把既有已發布稿一次重寫，不建全文 Claim Graph，不公開評分台帳，不要求使用者逐段下指令。重大 P0/P1 或發布權限問題仍依既有高風險決策閘門處理。既有 EJE 對 AI 是否能在使用者指出前獨立發現問題的研究，與這個 release receipt 是不同檢驗，不能互相冒充。
