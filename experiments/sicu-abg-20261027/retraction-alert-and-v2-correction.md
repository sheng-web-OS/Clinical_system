# Source Integrity Alert — 2026-10-27 / V1 已凍結，不得改寫

## 發現

V1 最後的補充來源曾列 **Suttner et al., Anesth Analg 2004;99:2–11; PMID 15281492** 作為「CABG 術後生理研究」。在本輪後續追查原始 PubMed 紀錄時，發現其 Publication types 明確含 **Retracted Publication**，且「Comments and corrections」有 2011 年的 **RetractionIn**（PMID 21451079）。此文**已撤稿**，不能作為可信的術後氧輸送／輸血證據。

來源核查：[PubMed 原始紀錄](https://pubmed.ncbi.nlm.nih.gov/15281492/)（有 Retracted Publication 與 RetractionIn）；[撤稿紀錄](https://pubmed.ncbi.nlm.nih.gov/21451079/)。

## 影響與修復

- **P0 source-integrity gate**：V1 不得公開。V1 原文與首次評測 79/100 依 immutable baseline 保留，不事後擦除錯誤或竄改原分。
- **V2 必須刪除該文作為正面證據的所有引用**，僅可在私人 QA 記錄中以「撤稿來源」供反例追溯。
- 可靠替代：**Okamoto et al., Critical Care 2026;30:341, DOI 10.1186/s13054-026-06149-9**，1,352 位心血管外科 ICU 患者、單中心 retrospective、輸血前 Hb ≥7.5、肺動脈混合靜脈 SvO₂ 配對。平均 Hb 9.82→10.24 g/dL，平均 SvO₂ 73.79→73.86%，差異 0.08 percentage points（95% CI −0.28 至 0.43，P=0.671）。作者明確表示無法證明組織氧合或臨床獲益，探索性 69% 不能作為輸血 trigger。原文：[Critical Care 出版社](https://link.springer.com/article/10.1186/s13054-026-06149-9)；[PubMed](https://pubmed.ncbi.nlm.nih.gov/42332804/)。
- 不把 2026 研究當作 2025 單一病例的後續，也不把 retrospective association 當因果。

## 可驗收防錯機制

每篇 V1 完成後，對**所有引用的原始研究**做 PubMed status / retraction / expression of concern / correction 檢查，**在首次公開前**執行，不等讀者指出。此次屬 Agent 自主發現並修正；可觀察到使用者本輪即時介入 0 次，但無法證實人工耗時為 0。

此項揭露是 V2 及未來稿件的醫學來源硬門檻，不另建複雜常駐程式。