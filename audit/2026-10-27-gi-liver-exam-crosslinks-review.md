> **CURRENT OWNER RELEASE DECISION — ACCEPTED, 2026-10-27 Asia/Taipei.** The owner explicitly replied 「發佈」 to the publication of PRs #129/#120/#121. In PR #129 this means P0/P1, all figure semantics, complete manuscript, official exam link semantics and PR-only merge/production deploy **AUTHORIZED**, scoped to article blob `f1f82f86894d94628efc8c4b7386e55297b543db` at review. [Decision evidence](https://github.com/sheng-web-OS/Clinical_system/pull/129#issuecomment-6433081794). This is author/editor clinical signoff, NOT independent peer review. The historical PENDING/HOLD snapshots below are superseded for this PR and date, but the technical CI and production readback must still be verified separately. 原卷答案 D/D/D、Wilson 單項 ceruloplasmin 非確診、CTP 不含 ALT、SAAG + 腹水總蛋白並讀；不宣稱獨立醫師同儕審查。

# 2026-10-27｜肝膽國考三題來源驗證／醫學編輯驗收

## 核對範圍
本文 `content/xiaoma-internal-medicine/lessons/2026-10-27-gi-liver-exam-trio.md`；候選正文 Git blob `1f8104609cca41a410cf0eac1ca0c603f2f0bd6c`。來源為考選部 **醫師第二階段・醫學（三）** 原試題 PDF、標準答案／標準答案更正 PDF；已目視核對以下**原始題目頁**與**更正表**（不是單憑 OCR 純文字）。

| 題號 | 原始來源 | 原卷頁 | 更正答案表 | 官方給分 | 正文核心推論 |
|---|---|---|---|---|---|
| 112（一）醫學（三）Q1 | [原卷](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=112020&q=1&s=11&t=Q) | PDF viewer p.1 | [更正](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=112020&q=1&s=11&t=M) | D（未更正） | 19 歲、ALP274 不指定病因；低 ceruloplasmin 11.1 提高 Wilson 懷疑，不能單項確診 |
| 114（一）醫學（三）Q22 | [原卷](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=114020&q=1&s=0103&t=Q) | PDF viewer p.6 | [更正](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=114020&q=1&s=0103&t=M) | D（未更正，該卷 Q23 另為全題給分） | CTP 不含 ALT；injury、function、clinical event 不可混同 |
| 114（二）醫學（三）Q22 | [原卷](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=114070&q=1&s=0101&t=Q) | PDF viewer p.6 | [更正](https://wwwq.moex.gov.tw/exam/wHandExamQandA_File.ashx?c=302&code=114070&q=1&s=0101&t=M) | D（未更正；該卷 Q20 是答 C/D 皆給分，不可誤用） | 四組 SAAG 1.0／1.7／0.8／1.6，D 高梯度低腹水蛋白最符合肝硬化 |

**來源驗收：** 題號、考試日期（年度與梯次）、科目、原題文字及非影像作答條件、四選項數值、官方更正表**均已比對**。**未使用**同一試卷其他題的「一律給分」誤改 Q22。考選部原卷官方來源僅透過連結引用，來源版本不可由 AI 教學推論竄改。

**工程驗證：** 單篇跨年度三個 `exam_questions` 正規 metadata，加入年度題庫資料庫；#67 公開主文一筆 Q112-1 `related_exams` 指回可精準定位的 Q1，年度索引也能回到 #67 Q1 概念節；其餘兩題在尚未發布 #69 時不生成指向不存在的公開文章連結。後續 #121 核准時再補 CTP/SAAG 連結。**#120／#121 各兩道舊題的連結在各自 Draft 分支，尚未正式上線。**

**尚需完成：**
- [ ] 最新 SHA 的 editorial regression、year-first exam links、Figure Gate、靜態建置
- [ ] 360／390／1280px 實際 Chromium 文章與年度索引
- [ ] 作者的逐題醫學深度及來源敘述驗收（目前僅 AI 複核，非獨立醫師同儕審查）
- [ ] 針對本單篇新題庫內容的明確合併／部署授權

**發布 HOLD：** 本 PR 將來源已核實的官方三題**編入 Draft 發布候選**；不能僅憑官方答案確認或 CI PASS 逕行發布。#120 Chronic diarrhea、#121 Cirrhosis 的醫學 HOLD 不受這份題庫 PR 影響。
