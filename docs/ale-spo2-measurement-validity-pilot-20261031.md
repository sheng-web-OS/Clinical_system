# ALE source-first Concept Family experiment 02｜SpO₂ measurement validity
2026-10-31 · owner-directed after #137 termination · research artifact / NOT PUBLISHED

**Question:** Can 謝小生, without a pre-tagged `impact` or `concept_id` supplied for this topic, read an already-published clinical narrative plus external evidence, identify a consequential missing *relation*, attempt falsification, and choose one useful revision rather than fill every possible medical detail?

## Source exposure & inspection limits

Existing project files actually inspected:
- `content/clinical-os/index.md`, the single canonical public knowledge atlas. Dyspnea portion separates oxygenation, ventilation, delivery and support; it describes SpO₂ as an estimate but **does not explicitly introduce reliability of the optical measurement as an inferential prerequisite**.
- `content/xiaoma-internal-medicine/lessons/2026-10-21-hypoxemia.md`, the full deep lesson. This ALREADY states SpO₂ is an optical estimate, limited by motion, poor perfusion and dyshemoglobins; explicitly mentions co-oximetry, COHb and methemoglobinemia later. **Do not classify those basic facts as missing**.
- `content/xiaoma-internal-medicine/lessons/2026-10-25-hypoxemia-mechanisms.md`, narrower gas-exchange topic, not the source of device accuracy standards.

External **public** references consulted as research evidence (not a standalone independent clinician review):
1. [CDC clinical CO poisoning guidance, updated Aug 21, 2026](https://www.cdc.gov/carbon-monoxide/hcp/clinical-guidance/index.html): conventional **two-wavelength** pulse oximetry is not accurate with COHb; appropriate laboratory co-oximetry confirms COHb in exposure-compatible presentation, while level depends on exposure/treatment timing and does not alone grade severity.
2. [FDA pulse oximeter basics](https://www.fda.gov/medical-devices/products-and-medical-procedures/pulse-oximeters): poor perfusion, skin pigmentation, nail polish, and other conditions influence accuracy. [FDA January 2025 pulse oximeter guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pulse-oximeters-medical-purposes-non-clinical-and-clinical-performance-testing-labeling-and) is a **DRAFT / not for implementation**, not a finalized universal clinical cutoff.
3. [PMID 19615844](https://pubmed.ncbi.nlm.nih.gov/19615844/), published CO poisoning case: traditional SpO₂ normal with COHb **28%** on pulse CO-oximetry; investigation found malfunctioning domestic water heater. The case supports a *diagnostic failure mode*, not pulse CO-oximeter validation as universal replacement.
4. [2026 open access methemoglobinemia report](https://pmc.ncbi.nlm.nih.gov/articles/PMC13417352/): SpO₂ approximately **85%**, PaO₂ **167 mmHg**, **calculated** arterial saturation 97.3%, laboratory co-oximetry methemoglobin 19%; clinical course cannot be collapsed into a fabricated combined case. Crucial distinction: blood-gas **calculated** saturation is not equivalent to a direct multi-wavelength hemoglobin-species measurement.
5. [Sjoding et al., NEJM 2020, PMID 33326721](https://pubmed.ncbi.nlm.nih.gov/33326721/) plus [published correction, Dec 2021](https://pubmed.ncbi.nlm.nih.gov/34936755/): retrospective paired measurements revealed potential occult hypoxemia in particular sampled groups; original authors' racial categories are not an individual optical pigment measurement.
6. [EquiOx, CHEST Critical Care online Aug 3, 2026](https://doi.org/10.1016/j.chstcc.2026.100305): prospective single-center ICU cohort (631 adults, 1,760 paired SpO₂/SaO₂ readings), **most were well oxygenated**; in this sample SpO₂ tended to *underestimate* SaO₂ and the degree of bias varied by measured pigment. This does **not** erase occult hypoxemia from other datasets or establish a universal direction of bias at low saturation.
7. [2026 study of 34 devices, PMID 42012940](https://pubmed.ncbi.nlm.nih.gov/42012940/): observed instrument-specific performance and variability. An optical bias claim must be bounded by device, population, saturation distribution and perfusion/measurement protocol.

## 1. Knowledge spine *before* source comparison

```text
Dyspnea
  ├── oxygenation: FiO₂ / PaO₂ / gas exchange
  ├── ventilation: V̇A / PaCO₂
  ├── carriage: Hb / SaO₂ / CaO₂
  └── delivery: cardiac output × CaO₂
            ↑
        SpO₂ is often used as a saturation proxy
```

This correctly prevents treating a normal SpO₂ as proof of ventilation or oxygen delivery. The **inferential path from monitor value to trustworthy saturation estimate**, including possible optical failure, is not explicit at the atlas level even though parts of it exist in the deep article.

## 2. Three competing research gaps, proposed *after reading* existing content and external references

| Candidate | Actual delta | Initial choice | Why |
| --- | --- | --- | --- |
| `oximetry_measurement_validity_bridge` | Connect *measurement reliability* as a typed prerequisite to any inference from SpO₂ → SaO₂ → oxygen content | **INVESTIGATE / PROPOSE RELATION** | A correct top-level relation could prevent a safety-relevant category error across respiratory, emergency, toxicology and ICU reasoning |
| `pigmentation_device_bias_domain` | Add a qualified study-specific accuracy caveat to source layer, with attention to conflicting bias direction and measurement protocol | **QUEUE / RESEARCH BOUNDARIES** | Important but does not support a single bedside correction formula; article and device-specific claims require editorial scoping |
| `new_co-poisoning_protocol` | Add complete CO poisoning treatment algorithm and hyperbaric thresholds to dyspnea atlas | **PRESERVE OUTSIDE SCOPE** | Not necessary for this concept identity test; would substantially broaden curriculum and require independent clinical guideline review |

These priorities were decided by **this ChatGPT research interaction** after reading source texts; they were NOT generated by the deterministic `ale_gap_triage` program from raw prose, and are not independent evidence of unattended agent autonomy.

## 3. Recursive Three Questions on the selected bridge

**Q0/Q1 — Observation and contradiction:** A normal displayed SpO₂ can coexist with substantial COHb, while low displayed SpO₂ can coexist with high PaO₂ under certain dyshemoglobins. Therefore neither the number alone nor normal oxygen tension necessarily proves an adequate functional Hb oxygen-carrying state. Previously existing article statements cover this, but a central atlas inference may allow readers to bypass the measurement-validity question.

**Q2 — Reconstruct a typed, limited Concept structure:**

```text
  measurement/spo2-optical-estimate
         │
         ├──[REQUIRES_VALIDATION_IN_CONTEXT]──>
         │      measurement/model-validity
         │        ├── sensor signal / perfusion / motion
         │        ├── hemoglobin species (COHb, MetHb)
         │        └── device / pigmentation / tested saturation range
         │
         └──[APPROXIMATES_IF_VALID]──> measurement/arterial-saturation
                    └──[CONTRIBUTES_TO]──> physiology/oxygen-content
                                                 └──[ALONG_WITH_CO]──> physiology/oxygen-delivery
```

`REQUIRES_VALIDATION_IN_CONTEXT` is **not** `is_a`, and does not assert every patient needs laboratory co-oximetry. Original saturation terms can mean functional versus fractional saturation depending on method, so definitions/measurement method must accompany the link. This is a **candidate relation repair**, not an automatic medically accepted ontology rewrite.

**Q3 — Falsification and counterexample cases:**
- *Case A, high/normal conventional SpO₂ with high COHb:* proves a clinically important situation in which interpreting the number as true oxygen-carrying capacity fails. Does **not** prove that CO poisoning is a common cause of any asymptomatic normal SpO₂.
- *Case B, low SpO₂ and high PaO₂ with laboratory MetHb:* falsifies the universal inference `low SpO₂ ⇒ inadequate pulmonary oxygen transfer`. Does **not** imply no oxygen-delivery problem exists; methemoglobin reduces usable Hb.
- *Device pigment counterexample:* different device/population studies show not all observed mean biases have one direction. Therefore `darker pigment always adds +X to displayed SpO₂` is unsupported. Do not propose a fixed correction by skin category.
- *Boundary:* in a conventional clinical setting with reliable waveform and no signal/hemoglobin interference, SpO₂ remains a clinically useful estimate; no need to downgrade all pulse oximetry to worthless or demand co-oximetry routinely.

**Recursive Q0:** When SpO₂ and the patient's presentation disagree, which *specific* assumption behind the optical estimate fails, and which *different* observation can discriminate it (exposure history, waveform/perfusion, Hb, PaO₂, measured multi-wavelength co-oximetry as indicated)? Do not repeat a predetermined 'test everyone' rule.

## 4. Concrete atlas candidate (DO NOT publish without clinical QA)

Proposed short replacement of the first SpO₂ phrase in the dyspnea section, **not applied to main**:

> SpO₂ 是脈搏血氧儀對動脈血氧飽和度的光學估計；先確認這個估計在當下是否可靠，再用它推論氧合。末梢灌流不足、訊號干擾、不同儀器與皮膚色素條件，或異常血紅素，都可能使數值失真。尤其一般雙波長血氧儀無法可靠排除 COHb；臨床狀況與讀值不符時，應針對可能失效的前提查證，而非讓漂亮的 SpO₂ 取代換氣、攜氧量與組織供氧評估。

This **adds a relation/decision boundary**, not another disease taxonomy branch. Keep the complete source critique and cases in the article/source layer; concise atlas remains readable rather than UpToDate-length.

## 5. Acceptance and limits

**Already delivered:** independently inspectable external source list and original-source distinction; negative cases in two opposite directions (normal-high vs low-high); actual contrast with canonical atlas versus deep lesson; one candidate typed Concept Family edge and a ready-for-review atlas paragraph.

**Still missing:** separate medical reviewer signoff, prospective unseen learner answer, persistent canonical graph adoption, automatic raw-text entity-relation extraction, generalizable evidence-based gap priority inference, unattended two-run agent follow-through. No Anki card created: no owner-private misconception has been observed.

**Best next test:** A genuinely held-out medical source on a *different measurement modality* (e.g. creatinine-based eGFR during rapidly evolving AKI) should be processed without a supplied `impact` label. Ask an independent reviewer whether the agent finds the missing assumption and avoids inappropriate `is_a` merges. Only then connect the protocol to private learner ALE and card-worthiness.

Links: #258 private learning; #260/#263/#268 recursive experimental Concept Family; #254 delivery-first. This artifact is owner-directed, outside terminated #137. No public site or Anki mutation.
