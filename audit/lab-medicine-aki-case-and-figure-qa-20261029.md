# Lab Medicine 03｜2026-10-29 case / source / visual evidence audit (PRIVATE)

**Scope**: `content/xiaoma-internal-medicine/lessons/2026-10-27-lab-medicine-aki-creatinine-urine.md`, content SHA `c599ff19f7beb4f75a229fb9106e017690e24f0d` at drafting stage; content version changes require new exact-blob reviewer receipt. This is a writer-side fact check, **NOT independent clinical or EPQC approval, human peer review, publication permission, or evidence of reader learning**.

## Question–evidence fit before writing

Single article question: What do SCr/eGFR/AKI criteria actually measure; how can the same creatinine rise conceal competing perfusion, renal parenchymal and obstructive processes; what evidence could distinguish them? **PROCEED with constrained title** rather than promote it as diagnosis made by a formula. 2025 Chen case has full visit-to-CT-to-catheter-to-follow-up narrative and original tables/images. Core decision pivot: persistently worsening renal function after hydration and negative initial ultrasound, high persisting urinary obstruction risk -> CT showed bilateral severe hydronephrosis/hydroureter -> Tiemann-tip catheter exchange -> high urine output and later SCr decline. Do not infer a precise structural level of obstruction unreported by CT.

## Original case visually checked

Chen et al., Cureus 2025;17:e88144, DOI 10.7759/cureus.88144; [publisher-origin PDF](https://assets.cureus.com/uploads/case_report/pdf/378818/20250817-408465-h29q8a.pdf), [PMC page](https://pmc.ncbi.nlm.nih.gov/articles/PMC12358086/), PMID 40827146. Current web PDF read and screenshots **were actually inspected**:
- PDF page index 1 / printed page 2: Figure 1 and 2 renal US, captions specify 10.9 cm left / 10.6 cm right; no significant hydronephrosis at captured view.
- PDF page index 2 / printed page 3: Table 1, initial 2024-12-08 Na120 K4 Urea23 SCr375 μmol/L Hb132 Platelet90 CRP211, 12-10 SCr558 urea30.3 Hb108 Platelet91 bilirubin38; **12-12 SCr618 μmol/L** in same pre-insertion table.
- PDF page index 3 / printed page 4: Figure 3 CT coronal image and caption bilateral severe hydronephrosis/moderate bilateral hydroureter; Table 2 post Tiemann 2024-12-11 input1800 output6170 net−4370 mL. Daily I/O ≠ documentation that all 6 L left immediately.
- PDF page index 4 / printed page 5: Table 3 has **2024-12-12 SCr122 μmol/L**, 12-13 SCr85; 12-12 sodium141 and 12-13 sodium141; blood film 'No evidence of hemolysis' yet DAT **positive** and C4 <0.1 g/L. No grounds to describe *all* hemolytic/immune investigations as normal. Admission platelet already 90×10⁹/L; 12-10 value 91 must not be narrated as a new normal-to-low change.

**In-source contradictions / hard stops against precision**:
1. SCr 618 and 122 both dated **12/12** in Table 1 vs Table 3; cannot derive an exact timestamp-specific intervention-to-SCr response or decide typo.
2. Author calls admission 'Stage 1 AKI' while SCr375 μmol/L (~4.24 mg/dL) is above KDIGO 2012 Stage 3 absolute threshold of 353.6 μmol/L when acute; exact pre-admission baseline / staging prerequisites absent. Do not endorse stage 1 or independently certify stage 3 from missing baseline.
3. Narrative says urine ‘around 6 L immediately’; audited Table 2 gives only 6,170 mL/day. Do not equate with documented immediate drainage. CT does not reveal exact obstruction mechanism.
4. Author narrative says hemolytic tests unremarkable but Table3 has DAT positive; avoid assuming active hemolysis solely from DAT or assuming entire workup negative.
5. Author attributes anemia/platelet/bilirubin to urosepsis; there is not sufficient reported culture/verification to elevate this to a confirmed mechanism. HUS/TTP considered, not established.
6. No measured FENa, FEUrea, urine sediment, baseline SCr or exact hourly post-catheter urine trajectory for **Chen patient**; no invented values or overlays from companion patients.

**Other evidence separately sourced**:
- KDIGO 2012 AKI original PDF [official](https://kdigo.org/wp-content/uploads/2016/10/KDIGO-2012-AKI-Guideline-English.pdf) screenshots PDF indices 21 (printed19, Table2 definition and staging), 27 (printed25, Figure4), 28 (printed26, Figure5). This contrasts staging vs etiologic testing; original figures are linked but not reproduced.
- KDIGO AKI/AKD guideline web landing dated 2026-10-29: 2026 public review draft is being prepared for publication; not final.
- KDIGO CKD 2024 official landing online, and 2027 focused CKD medication update is in public consultation (do not conflate with AKI).
- NICE NG148 html text [official](https://www.nice.org.uk/guidance/ng148/chapter/Recommendations), section 1.4.2/1.4.4–1.4.6 and 1.5.1: urine dipstick and symptom-specific obstruction risk; 6h pyonephrosis, 24h uncertain AKI or obstruction risk; not blanket CT timing.
- [Obstructive uropathy review 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9846865/) for POD >200 ml/h×2 or >3L/day, requiring volume/electrolyte re-evaluation.
- [Jahnke et al. Braz J Nephrol 2022 open HTML](https://www.scielo.br/j/jbn/a/6K7JcmSpSgt3srPxR7WLRjv/?lang=en) own rhabdo+COVID case with CK4415/SCr4.8, first UA heme2+/RBC6/HPF/granular6/LPF; serial 1.9 on June13, 4.2 on June16 with tubular epithelial cells and muddy-brown casts. Do not concatenate as Chen patient, do not imply causality of treatment for mortality.
- [Kundavaram 2023 J Lab Physicians full HTML](https://jlabphy.org/bland-urine-sediment-in-a-child-with-acute-kidney-injury/) childhood bland initial UA SCr7.89 then biopsy-proven interstitial nephritis. Distinct case.
- [Varghese Kidney360 2022 cohort](https://pmc.ncbi.nlm.nih.gov/articles/PMC9136894/) 270 selected nephrology-inpatient suspected intrinsic AKI, 133 MBGC, 50/133 (38%) FENa<1%. Do **NOT** convert biopsy-positive subset 100% specificity to a universal rule.

## Editing and release status

Writer self-review: initial simulated A/B/C main case and treatment-direction language replaced with verified longitudinal patient and evidence discrimination; new contrasting literature is explicitly separate. The original author Table1/Table3 conflict is made visible in reader prose because it changes the defensibility of exact treatment timing. Original figures are link-only; no third-party pixel republishing. 113-1 Q29 official subject standard answer D retained from existing branch source QC; 115-2 Q28 retained with Moex official portal and prior branch verification but this current run did not fully reread its PDF.

**HOLD:** needs independent clinical reviewer (especially KDIGO stage 3 threshold and case source conflict), exact-blob independent paragraph EPQC reviewer, alternative case if reviewers judge date contradiction blocks reader trust, independent medical rights/figure and exam source review, this specific AKI page's 360/375/390 + desktop browser screenshots, no unmet P0/P1, current-head CI and publication authorization. Source file is currently outside `site/pages.json`, so CI green does not mean public article exists. Do not merge/deploy without gate.
