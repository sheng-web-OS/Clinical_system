# Lab Medicine Pilot｜初稿來源稽核與發布閘門（2026-10-27）

## 狀態
Issue #180。兩篇新 AI 教材目前在私有 feature branch，**DRAFT / HOLD**；本紀錄是撰稿脈絡內的初步自我校核，**不等於獨立審查或正式 release receipt**。不修改 site/pages.json、不更動現有 09:00 任務。

## 已核對來源與存取層級
- NICE AKI NG148（直接讀取建議文字）：https://www.nice.org.uk/guidance/ng148/chapter/Recommendations 。成人 SCr 48h +26 µmol/L、7d +50%、尿量 <0.5 mL/kg/h >6h；尿液 dipstick；超音波不是所有 AKI 都需例行安排。
- KDIGO AKI 官方頁（已核讀）：https://kdigo.org/guidelines/acute-kidney-injury/ 。2026 AKI/AKD 仍是 public-review draft，未正式出版。
- UK Kidney Association hyperkalemia 官方頁（已核讀）：https://www.ukkidney.org/health-professionals/guidelines/treatment-acute-hyperkalaemia-adults-0 。已開啟 July 2026 官方 PDF 180 頁，目視核對印刷第 7、14、15 頁（viewer pages 6、13、14），包含假性高血鉀 Guideline 15.3 的成對 heparin plasma / clotted serum、16.2-16.6 的重要安全處置與 17.1-17.2 重測及血糖監測；**沒有完成完整 Appendix 原圖分岔與台灣院內劑量審核**，稿件因此不提供固定劑量。
- BMJ 2026 急性高血鉀診療可見 HTML（已核讀）：https://www.bmj.com/content/394/bmj-2026-100287 。ECG 不能敏感排除，高風險立即處置與確認需並行。
- AHRQ PSNet 2017 Hemolysis Holdup（真實案例及專家評論全文已核對）：https://psnet.ahrq.gov/web-mm/hemolysis-holdup 。72M，K 7.4（溶血）→重驗 8.4，等待期間惡化與 cardiac arrest；不能用 case report 外推一般發生率或治療效果。
- Kanjee/Lippi/Freed 2026 Mayo Clin Proc（PubMed abstract/出版商 highlights，未取得訂閱全文逐頁）：https://pubmed.ncbi.nlm.nih.gov/42134749/ 。體外溶血、EDTA clumping、heparin-line 與凝血採樣干擾。
- Shean 2025 IV fluid contamination（可見正文）：https://jlpm.amegroups.org/article/view/10562/html ；ADLM vascular-line phlebotomy 教學資料（可見網頁）：https://myadlm.org/science-and-research/clinical-chemistry/clinical-chemistry-trainee-council/pearls-of-laboratory-medicine-in-english/2016/collecting-blood-from-patients-with-vascular-lines 。
- 2026 BMP IV contamination rules study（僅 PubMed abstract）：https://pubmed.ncbi.nlm.nih.gov/42275628/ 。異常告警有真正病理/治療效應造成者，不能視為已驗證本院工具。
- Choosing Wisely Canada Using Labs Wisely（網頁）：https://choosingwiselycanada.org/hospitals/labs-test/ 。反對穩定患者無理由 routine daily CBC/chemistry；不能外推到不穩定病人。
- KDIGO 2027 CKD medication focused update 2026-10-15 起公開審查，尚未正式生效：https://kdigo.org/kdigo-2027-ckd-guideline-focused-update-public-review-open/
- 已讀到本庫 115 年第二次醫師二階醫學（三）Q26：2026-s2-med3-q26，答案欄為 B；內部 record 仍寫 machine_parsed_visual_and_medical_review_pending，**不能把程式擷取誤當已完成官方 PDF 原圖、答案更正的目視查核**。

## 自行計算核對（非獨立審稿）
- UO：170mL/8h/70kg = 0.304 mL/kg/h；SCr 1.0→1.7 mg/dL，已符合 AKI stage 1 的功能條件。
- 07:00 AG = 134 − (102+18) = 14 mmol/L；albumin 2.8 g/dL 校正粗估 14 + 2.5×1.2 = 17。不可把校正 AG 當病因確診。
- 修訂後自編 ABG 與 07:00 生化同步採檢；pH 7.33、PaCO2 35、計算 HCO3 約 18，Winter 1.5×18+8±2=33–37。這是近似對照，不可拿非同步結果宣稱已完全辨識混合障礙。
- ANC = 17.5×0.88 = 15.4 ×10³/µL；WBC 3×0.10=ANC0.3 ×10³/µL。
- glucose 210 與 Na 133：ESE 2014 指引採 +2.4 mmol/L per 100 mg/dL，校正 133+2.4×1.1=135.64；Katz 常見 +1.6 算式得到 134.76。正文現已並列兩個近似式、明示來源與 2014 勘誤；不可把估值當真實張力或診斷。
- 已明確區分生化檢體 hemolysis 與 CBC 不同管別／方法；採檢後改變可能和真正疾病變化並存。

## 獨立發布閘門／待辦
1. 逐段 reviewer **必須與寫作者分離**，覆蓋每段 reader gain、redundancy、推論界線、EPQC A–G 與危險反例；此文件不能自簽 independent_ai_pass。
2. 高風險來源補查：2026 UKKA 高血鉀原 PDF 未讀的完整 Appendix 算法／2026 KDIGO 草案 vs 正式；Q26 題圖／官方答案 PDF；以及若新增精確治療劑量必須正式逐項審。
3. 使用 repo tooling 實際完成 python site/semantic_gate.py --packet、獨立 receipt、python tools/validate.py、bash tools/build_site.sh；手機 360/375/390px 與相互連結，不能只用 Markdown 已寫入假稱驗收。
4. 所有新公開教材必須先過 site/pages.json allowlist 的編輯發布流程；目前不提交出版 manifest。
5. Pilot 後以未見病例驗證理解遷移、重大安全錯誤、編輯返工次數與使用者投入；AI 自評不是教學效果。

## 下一篇候選
SCr/BUN/eGFR、尿量、UA/urine sediment、時間滯後：AKI 功能訊號不等於腎小管損傷，對照 CKD 病程與藥物/灌流/阻塞。避免與已存在 acid-base、diuretics 重複。

**最終狀態：HOLD。早期文章版本已有 GitHub Actions build success，但最新版文章／來源審查仍需依 exact SHA 讀回，且無獨立醫學與逐段語義審查、正式發布或讀者學習成效的合格證據。**
