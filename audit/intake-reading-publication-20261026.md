# 入庫整併、閱讀脈絡與選擇性發布

使用者授權：整合所有目前已入庫未發布稿、建立閱讀脈絡、發布適合文章；後續更正以「系統網站」為目標。正式目標經 Cloudflare 專案 API 確認為 sheng-clinical-system.pages.dev，GitHub sheng-web-OS/Clinical_system，production main。舊私人 Sites v5.1 未修改。

輸入主版本：4241e082723d99c7dfb52563c22179627838b4bb。分支稿依 PR 57–69 的實際 head 讀回全文、逐檔 SHA 比較；未整批合併任一舊分支的出版目錄、樣式或接收總數。原稿快照原 bytes 保留；本次8篇公開稿都是獨立 AI 整合版本。

## 整合與選稿

| 主題 | 決策與必要理由 |
|---|---|
| 肝臟檢驗 → HBV phase → ALT 訊號 | 3篇構成量測／狀態結構／推論行動的連讀。補 R-value 前提、急性肝衰竭界線、灰區共享決策，對讀完整小麻 PDF 137、140–141頁。 |
| WPW → pre-excited AF → WCT／ACLS | 3篇共用傳導模型；補原創方向／安全界線圖，修正「心跳停止」為「終止心搏過速」，避免將 AV node 描述成能篩選平行旁路。核小麻66–68頁與AHA2025。 |
| VTE | 出版附3張原創圖的獨立整合版；補「proximal DVT 可支持 VTE 治療但不是直接顯示肺栓子」及機械預防仍有適用限制。原圖97–100頁完成目視。 |
| 便祕 | 出版明示虛構的整合版；補術語、原創定位圖及多藥時序歸因，保留腸阻塞／神經警訊、DRE限制及PAMORA禁忌。原書127頁完成目視。 |
| Cholestasis、infiltrative ALP、cirrhosis、腹水上下篇、慢性腹瀉 | 原文與既有審查完整收攏，保留待出版。需完成各篇獨立原書分支／註腳核讀、臨床修訂與原創圖解後再納入；不因同屬肝膽而全批放行。 |
| 急性AF、Syncope、中風二次預防 | 原文／模擬情境保存；AF轉律時間與抗凝前提、syncope神經檢查例外、中風已證實AF與DAPT族群仍須各自完整審查。 |
| ABG／CABG首次成稿、國考第五批、舊NIV重寫分支 | 保留原工作分支；本輪不將實驗或另一條未完驗收線順帶發布。ABG首稿仍需模型級修訂，不能覆蓋V1；現有公開NIV教材不被未完稿取代。 |

## 實際來源與品質界線

小麻原PDF SHA256 ad283f7db19b6575775341972360a5ca1e5b40f51383ce02d9c11c8d21a0b3c5，共464頁。讀回且實際目視66–68、97–99、127、137、141頁；第100、140頁另核讀本輪範圍與上下文。不是只用截圖或摘要當作原頁。舊審查寫463頁的總頁數於本輪來源頁更正，歷史原稿不改。

新8篇共11張原創圖（肝1、HBV3、心律3、VTE3、便祕1；以實際figure計數為準），原書像素不公開重製。權利決策為link_or_original_only：私人研究逐圖核讀；公開以獨立因果解析和出版社合法入口達成教學目的，不臨摹原表版式，不提供替代教材市場的完整表格。該處置不冒認法律裁判或出版社授權。真實病例僅轉述已發表事實並連回原PDF，虛構情境明示，不混充case report。

本輪為同一Agent的AI來源／安全與EPQC編輯審查，非獨立盲審、真人醫師同儕審查或學習成效驗證。按A命題／B解混／C中介／D因果／E證據／F臨床遷移／G負擔逐篇查核：各篇主要前提均已建立；剩餘不確定性於來源頁及對應正文保留。沒有以自評分數取代P0/P1安全檢查。

## 工程缺陷與最小修復

既有main清單已含source_snapshot_archived，檢查器僅認得imported／conversation_only，造成corpus inventory失敗。本輪採既有PR62的限定狀態解析與兩個回歸例，明確區分snapshot與canonical original，仍拒絕未知狀態、遺失／越界檔案。未移除、繞過或放寬醫學／figure gate。入庫21篇為6 imported＋11 snapshots＋4 conversation_only；HCM、肝臟檢驗、腹水及中風情境不塞進原21篇基數。

## 驗收紀錄

來源與必要安全修改已完成；建置、既有測試、行動版圖解與同commit部署驗證逐項執行後記於下方，不預先記成功。


### 2026-10-27（Asia/Taipei）已執行驗證

- `python3 tools/validate.py` 通過；正式公開頁來源與連結可解析。
- `python3 tools/check_corpus_inventory.py --json` 通過：21＝6 originals＋11 source snapshots＋4 conversation-only，未將快照計成公開歷史版本。
- `python3 -m unittest discover -s tests`：68項通過，包含Figure gate、公開白名單、原稿指紋、MathML與單一知識地圖；本輪採PR62兩項真實故障回歸。
- `bash tools/build_site.sh` 通過，既有3張DCM出版社圖片下載驗證；64個公開來源頁、DOM錨點、搜尋索引、私有邊界與本地資產檢查通過。
- 使用實際Chrome預覽，八篇各在390px iframe（扣捲軸後375px內容寬）讀回版面；八頁html與11張figure的scrollWidth−clientWidth全為0。目視WPW、VTE、HBV與pre-excited AF卡片的手機呈現，以及桌面知識地圖；未測真人學習成效。
- 深色圖表背景使用既有主題變數；未增加新的導覽框架或出版器。

正式部署及HTTPS狀態待本提交的遠端部署結果，未預先標記已發布。
