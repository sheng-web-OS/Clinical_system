# CTICU Oxygen Delivery 02 — V2 審查（2026-10-27）

## 不可回填的版本紀錄

- V1 原始建立 commit **71fc876a260edcbd0c1623b81e03eebd994091d9**；首次非盲 AI screen **79/100**，不可改寫。
- V1 QA commit **c6bbbe0fd5ce17fd30ab4e4f01650bcd977f1531**。
- V1 後續發現 2004 Suttner CABG 研究已 **Retracted**（2011），保留 P0 source-integrity alert：**60cbe8ba4246a5871f19223429076f157229b60f**。
- V2 改稿 **b1fbe7666114cf2eedb826d1afcac464952d0ffb**；原創直式 SVG **8f83f9ff554b713328beb06e9265e1402d0367e7**。此處分數為另一次 AI 自查，**不是 V1 的重評**。

## V2 provisional non-blinded AI score

| Axis | Score | Basis |
| --- | ---: | --- |
| Core thesis /20 | 18 | 題目已移除「平均 SaO₂ 與事件 DO₂i 同時點」的假連結 |
| Prerequisites /20 | 19 | 氧合→攜氧容量→流量→輸送→耗氧及 Fick，與既有酸鹼文章分工 |
| Bedside decision /20 | 18 | 外科危險優先，後接 flow/Hb/VO₂；TRICS III 與 AABB 範圍保留 |
| Case & evidence /15 | 12 | 2025 真實 CPB 個案 + 2026 1,352 人術後 CVICU 資料分離；撤稿研究已排除；個案內部矛盾仍待核 |
| Figures /10 | 5 | 新增 440×840 原創 SVG（雙因果路徑、可閱讀字級），但尚無實際手機 Chromium 截圖與來源圖像原像素 QA |
| Readability /10 | 9 | 反事實與實測分離，部分長段待讀者測試 |
| Navigation/provenance /5 | 4 | 文獻來源清楚，未加入公開 site/pages.json，尚未完成 source page |
| **Total** | **85 / 100** | **HOLD**（未達 90，且 Figure Gate 未完成） |

## V2 hard gates

- **P0 resolved within V2 draft:** 2004 撤稿研究不再作為正面證據。這項修正不代表來源驗證系統已永久自動化。
- **P1 remains — 2025 case contradiction:** <280 for 8.5 min 與 <300 for <5 min 無法共存；CPB Hb narrative vs Table 3 取樣關係不明。圖不繪製事件持續時間，也不把平均 SaO₂ 當事件同步值。
- **P1 remains — original images:** 2025 Cureus Table 2/3 PDF 原始像素、2024 EACTS PBM Recommendation Table 11 caption/footnotes、Pocket 9E p32/p374 原頁圖像未完成目視。Library PDF 可檢索原文，但 raw bytes materialization 失敗；不把文字抽取冒稱原圖審查。
- **P1 remains — medical review:** 沒有獨立臨床醫師審閱；AI 自評 85 不能替代。
- **P1 remains — web engineering:** SVG 未經正式 renderer 375/390px 截圖；V2 未進網站白名單、CI、Cloudflare production 或 HTTPS，**不得稱已發布**。
- **P2 — trial scope:** 2026 Okamoto 是單中心 retrospective、Hb≥7.5 已接受輸血之選樣；SvO₂ 變化非臨床結果，探索性 69% 不可當 trigger。
- **P2 — CPB scope:** 2025 case 不能證明特定 DO₂i threshold 對一般術後 CO 的處方效果；術中 pump flow 與術後 CO 必須保持區分。

## Figure Gate manifest（private draft）

| Figure | Origin | Numerical provenance | Caption/footnote check | Rights | Mobile | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `oxygen-delivery-two-paths-v2.svg` | 本站原創，未複製原研究圖像 | 2025 Cureus case narrative DO₂i 260 / 275、Hb 7.9、介入後區間；CPB 平均 SaO₂ 98±0.5 明標為非同期 | 原始 PDF Table 2/3 視覺核對待辦；文字已核 | original-only | 440px 直式，**尚未實測** | **HOLD** |
| Pocket 9E p32/p374 | 私有教材原頁，未公開 | Fick / mixed venous oxygen saturation，原書抽取文字已核 | 原像素取得失敗 | private-link-only | n/a | **HOLD** |
| 2024 PBM Recommendation Table 11 | 指引原圖，不公開複製 | restrictive transfusion strategy | image caption/footnotes 待核 | link-only | n/a | **HOLD** |

## 人工介入紀錄

本輪對話中未觀察到使用者即時介入（**0 次**）；使用者實際人工耗時沒有測量，不得記為 0 分鐘。撤稿來源由 Agent 在 V1 凍結後自行查出、另檔記錄並於 V2 修正。這次失誤說明**首次成稿前的文獻撤稿狀態查核**仍未成為穩定的預防機制。

## 下一個最小修復

先逐像素核 2025 case Table 2/3 與 2024 PBM Table 11，並檢查 V2 SVG 在 375/390px 的真實渲染；若來源矛盾無法解決，保留為作者原始限制而非推論時間；必要時改用較可靠的真實個案。再做正式 source page、醫學審查、EPQC、CI、部署。**現在不修改 site/pages.json。**