# 肺切除 POD3 低氧｜V2 修訂附錄（私人 Draft/HOLD）

本文件為 PR #216 的獨立增量修訂，不覆寫凍結的 V1（commit 22e92306a9b7d967650ac5453694fa51c3cdbedf；blob 4291525e1771f0d47437823f9d24a25089ae5b9b）。對應獨立 AI review #5691732826，尚未取得 V2 獨立 PASS。

## 修正 P1-01：原始病例呼吸支持紀錄互相衝突

Liu et al. 2025 Case 1 記載患者 POD3 因急性呼吸窘迫轉 ICU，接受插管與侵入性機械通氣；後續敘述又出現 NIPPV、HFNC 與鼻導管降階，卻同時記載 ICU 第 11 天才拔管。這些文字無法直接拼成單一連續時間線。原文未足以判定是敘述順序錯置、日期誤植或中途再插管；均應標示 UNKNOWN。僅能確認患者曾接受呼吸支持且後續改善，不應捏造每次轉換的日期、模式或決策理由。

## 修正 P1-02：術後血小板結果須先評估檢體可信度

原文 Case 1 術前血小板曾為 64 × 10⁹/L，並提及血小板製品與疑似 pseudothrombocytopenia；POD3 報告 24 × 10⁹/L。後者不等於已證實 DIC、消耗性血小板低下或藥物不良反應。若影響出血或抗凝處置，需結合出血徵象、凝血數據、前後趨勢及檢體品質，必要時確認周邊血抹片有無凝集並使用合適替代抗凝劑複驗。這是臨床條件式辨別方案，不是聲稱原作者當時已執行這些檢查；真實病因仍 UNKNOWN。

## 修訂邊界

保留原稿關鍵推論：POD3 PaO₂ 49 mmHg 不可在缺乏同期 FiO₂/PEEP 下獨立重算 Berlin P/F；術前 EF 61% 不足以排除 POD3 hydrostatic edema；術中輸血不等於 POD3 符合 TRALI 六小時時窗。BNP 4,299 pg/mL 不應當作與 POD3 ABG 同時採血。原始 Figure 1 僅連結、不嵌入。不得從其他病例補證據或將本病例納入公開 site/pages.json。

Source: Liu et al. SAGE Open Med Case Rep 2025; DOI 10.1177/2050313X251400426, Case 1, https://pmc.ncbi.nlm.nih.gov/articles/PMC12696315/

Status: PRIVATE DRAFT/HOLD. This is an author correction appendix, not independent reviewer approval, final EPQC, or Figure Gate.
