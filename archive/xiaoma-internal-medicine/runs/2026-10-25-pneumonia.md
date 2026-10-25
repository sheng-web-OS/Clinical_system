# 2026-10-25｜肺炎：低 CURB-65 與當下器官支持

## 輸入與選擇

來源基準 main：49efc819206a28729ba2352248c79594d5109259。使用者問「今天的文章？」並要求繼續。核對現行 current-plan 第 10 節、出版目錄及最近提交：10/24 氣喘已製作；10/25 當時僅有氣喘圖表 CSS 修復，不能算新醫學文章。

候選為 COPD 持續性阻塞、肺炎的分流與抗菌決策、既有圖表缺口。選擇肺炎：承接已提供的低血氧、NIV、酸鹼與氣喘前提，補 A 級急症中的「死亡風險≠支持需求≠抗藥菌風險」，同一來源工作可完成兩道正式題、兩張圖與感染源控制推理。未取得新個人作答或投入時間，不推定任何章節已讀／精熟，也不把可提供教材視為學習進度。

## 產物

- 主文：content/xiaoma-internal-medicine/lessons/2026-10-25-pneumonia-severity.md
- 原表與來源：content/xiaoma-internal-medicine/pneumonia-sources.md
- 114（二）醫學（三）Q45、113（二）醫學（三）Q49 的獨立年份索引與逐項解析
- HTML/CSS 原創 Figure 01／02、自編病例與兩道遷移題

## 實際來源核查

- Pocket Medicine 9E PDF p247–248 已目視完整原頁：Microbiology of Pneumonia、Treatment 原表及相鄰診斷、未改善、PCT、steroid、duration 文字。未發布教科書 PDF 或原表像素。
- ATS 2025 更新：取得出版社正式 HTML，核讀 Question 2–4、Table 1／2／5／6 及相鄰腳註。另核讀學會 clinician summary；未以其替代未取得的 supplement forest-plot 像素審查，未引用效益數字。
- IDSA 2019 executive summary 與 CAP clinical pathway：核讀對題推薦及表格文字。原始 web screenshot 工具未回傳可視像素，故不記為該 PDF 的目視審查；severe criteria 另以 ATS 原始 HTML Table 2 交叉核對。
- ATS 2026 NIRS guideline：核讀正式 HTML Summary／PICO 1 及 implementation／monitoring、Figure 2 圖說；不宣稱已目視圖像或重做全部 RCT 審查。
- NICE NG250 原站 403，只核對官方可檢索 Box 2，明列取得層級；不是全文審查證據。
- 考選部兩份原卷及標準／更正答案 PDF 均實際取得、渲染並目視：113（二）Q49 在 p12；114（二）Q45 在 p11–12，補看跨頁 B–D。Q49=C、Q45=A，兩題均未更正。

## 反向複讀與修訂

- 嚴重低氧不由 CURB-65 低分排除；三項 minor criteria 不是自動插管處方。
- HFNC 對傳統氧療的強推薦，不跨比較解讀成對 NIV 必然優越。
- 90 天內住院＋IV antibiotics 的非重症風險與重症處置分開，未直接將所有近期住院者廣效涵蓋。
- 短療程必須考慮有效暴露天數、臨床穩定與新氧氣需求；severe CAP 至少五天，併發症另判。
- steroid 不是 CRP 單值門檻；保留 conditional、low-quality 與 influenza 例外。
- 既往中風未補造成吞嚥障礙；肺炎鏈球菌染色未冒稱培養確診；評估胸水未改寫成一律穿刺／置管。
- 新真題維持年份、梯次、階段、科目、題號；不沿教材發布日分類。

AI 同脈絡自查七軸：A4（單一主張）、B4（三種判斷解混）、C3（從肺泡病變連到支持與重評）、D3（明列來源與條件）、E3（同病例推進，後段延伸仍受主線約束）、F4（低分重症／新增菌株／胸水反事實）、G3（用來源頁分離查核記錄）。平均 3.43。此為有理由的內部篩選，不是隔離 AI 盲審、獨立醫師審查、原作者認可或讀者效益實證。

## 工程與每日任務缺陷

- 從基準來源取得本地快照，核對 Git blob fingerprint，修正本地取檔過程的行尾差異；歷史原稿沒有提交變更。
- 首次新稿檢查指出 manifest 的 review enum 不接受 ai_editorial_review；沿既有 lesson 契約改為 author_source_check，來源頁明示「AI 作者來源與編輯自查」，未冒認 independent_ai_review／human_review，也未放寬驗證器。
- 發現既有 test_exam_year_archive.py 把全目錄固定為三篇、全是108年，會阻擋正常新增年份。只將108年固定題數驗收限縮到108年子集，並讓總篇數檢查隨已註冊頁面變動；保留不可變題號、碰撞與未來年份排序測試。沒有改 runtime 驗證器。
- 既有每日任務當時 disabled；最後 run 為10/24 09:00，recorded completed，但結果空白、requires_user_action=true、delivery unknown。停用的底層機制未確定，不能擅稱已找出權限或平台根因。依使用者持續的每日授權，僅恢復同一任務 is_enabled=true，保留原09:00 Asia/Taipei與prompt；未建新任務。未來成功啟動與送達仍未驗證。
- 人工介入時間未量測；本次由使用者查詢才觸發補交，不能記為已成功自主出刊。

## 交付狀態

醫學範圍已完成上述AI自查；未經獨立醫師審查。出版候選須再通過61項既有測試、完整build、GitHub CI、同SHA Cloudflare deployment及HTTPS正文／來源／年度索引讀回。尚未取得的成功不得先記錄。最終提交、PR、CI與部署以GitHub和Cloudflare實際記錄為準。

下一優先缺口：COPD 持續性阻塞與肺氣腫的氣流／交換面區別，再接急性惡化；若出現實際作答證據，先處理能定位的前提錯誤。不能持續只修排版而不推進A/B範圍。
