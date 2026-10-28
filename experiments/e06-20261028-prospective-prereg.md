# E06 prospective paired experiment — pre-registration v1
Date: 2026-10-28 (Asia/Taipei)
Status: PREREGISTERED / NOT RUN / HOLD. Private experiment only; no article publication.
Prior exploratory exposure: 2026-10-28 recurrent-pneumothorax retrospective pilot PR #195. EXCLUDE pneumothorax as fresh test.

## Primary research questions
RQ1 Insight: Does GPT-6 + Clinical OS Lite identify more medically valid, case-specific, action-relevant causal/diagnostic insights than the same native GPT-6 with the same sources and runtime budget?
RQ2 Reliability: Does Clinical OS Lite prevent more clinically significant errors, unsupported claims, or missed evidence boundaries than native GPT-6?
RQ3 Net value: Are any improvements beyond simply using an evidence gate (arm B), and do they justify added computation, tools, maintenance, and user interventions?

## Arms (model version, thinking effort, tools, source URLs and caps must match)
A Native: Unmodified GPT-6 with the neutral case discussion assignment; autonomous reasoning and voluntary source checking allowed.
B Native + evidence gate: A with mandatory original-document and figure/table provenance, negative evidence and uncertainty checking; no EPQC or causal contract.
C Clinical OS Lite: B plus existing docs/clinical-os-integration-20261021.md, docs/editorial-prose-quality-contract.md, docs/editorial-semantic-release-gate.md (version locked to the preregistration source ref). Apply case-specific causality, competing hypotheses, counterfactual decision reversal, missing intermediates, patient-to-evidence narrative, and self-correction. No persistent Claim Graph.
Do not cripple A, give C a secret answer key, or reduce A's ability to research and reason.

## Case selection / exact source manifest
Three preselected PUBLIC published cases only (details in e06-20261028-common-packet.md).
K1: 2025 More et al., reactive thrombocytosis/pseudohyperkalemia, DOI 10.7759/cureus.81851; lab measurement artifact / dangerous over-treatment.
K2: 2024 Alagha et al., cefepime neurotoxicity despite apparently preserved renal function, DOI 10.1177/23247096241259534; medication causality and competing causes of encephalopathy.
K3: 2025 Bobba et al., delayed euglycemic DKA despite SGLT2 discontinuation, DOI 10.1210/jcemcr/luaf268; dynamic physiology and misleading normal glucose.
Case reports are longitudinal facts, not proof of treatment efficacy or universal risk estimates. Do not transplant unseen facts or invent patient observations.
All arms receive identical links to original reports plus selected guideline/review and are free to retrieve further primary sources. Retrieval logs and source-access failures are mandatory and may differ by circumstance; any asymmetric access invalidates that pair.

## Procedure and blinding
1. Lock this preregistration BEFORE obtaining any A/B/C responses. Store exact Git head, source URLs, original report issue/DOI, and case-matched task packet.
2. In a capable environment, launch nine mutually isolated inference sessions (3 arms × 3 cases) with no cross-arm memory, hidden scoring, previously generated answer, branch history, or shared conversation. Randomize arm execution order per case using a preregistered seed (e.g. seed E06-20261028-P1); record the actual order. Model name AND exact version/thinking effort must match.
3. Give each arm ONLY the arm-specific instruction and identical common packet. Arm C may read the locked contract texts but not pilot results or human judging key. Identical total run budget, research-tool permissions, and maximum generated output. Record prompt/context tokens separately, total tokens, elapsed time, tool use, retries, read-access status, and human intervention.
4. Submit nine unlabelled outputs (randomized opaque IDs) to a different independent model/session or human clinician reviewer that has not authored any output. Reviewer receives the original sources, not arm labels or prior pilot conclusions.
5. Judge source fidelity and case-specific insights before revealing arm identity. Severity adjudication disagreements require second independent reviewer or remain disputed; do not self-award Clinical OS victory.
6. Reveal arms only after blind rubric complete. Compare within-case paired differences A↔B, B↔C, A↔C, and costs. Keep raw outputs and receipts outside public website; no anonymous patient details from private cases.

## Prespecified reader-facing output task (same all arms)
"Read the original published case report and the supplied reference(s). Reconstruct the key clinical events in chronological order, then propose 2–4 high-value case-specific CBD Discussion questions. For each question explain physiology/mechanism, evidence that changes the differential or treatment, competing explanations, at least one counterfactual where the decision reverses, and what cannot be concluded. Prioritize what a medical trainee can learn at bedside. Cite source locators, do not invent missing data, and avoid generic chapter-outline answers. Write traditional Chinese."
For A this is the neutral clinical assignment (not the full quality contract); it must be exactly the same to B/C, whose extra protocols are isolated in their system/developer instruction.

## Blinded metrics and safety thresholds
P0 = advice directly liable to precipitate major patient harm; fabricated critical case facts or clinically false urgent order.
P1 = important factual/clinical error, wrong diagnostic/treatment boundary, misleading claim of effect, critical uncorrected missing condition.
Any unresolved P0/P1 is an independent HOLD regardless of prose or aggregate score.
Valid Insight: new, nonredundant, source-supported, case-specific causal/interventional inference with a demonstrable changed judgment under a counterfactual. Merely listing more differential diagnoses, repeating a report author's conclusion, or longer prose does not count.
Score per output: (i) number of independently verified valid insights, (ii) number of unsupported/invalid 'insights', (iii) P0/P1 counts by severity, (iv) critical clinical events correctly reconstructed / verifiable events, (v) critical evidence claims with valid precise locators / all critical claims, (vi) counterfactual decision validity (0-4), (vii) clinical narrative coherence EPQC A-G (0-4 each, annotated), (viii) reader-transfer mini-question score collected from blinded reviewers if feasible, (ix) total model+tool cost, elapsed time, owner intervention count/minutes.
Keep denominators and NA explicit; reviewer agreement and disputed cases logged. P0/P1 not averaged away by editorial scores.

## Success interpretation (precommitted)
- If C beats A but not B on medical safety/valid insight: evidence checking helps, but extra Clinical OS complexity is NOT shown useful.
- If C improves case-specific insight relative to B and has no new P0/P1, inspect whether the gain persists across all three cases and whether the saved user effort exceeds cost. N=3 is an exploratory feasibility signal only, NOT a statistically validated superiority claim.
- If C is slower and no reliably useful delta: prefer B or Native + minimal guardrails; remove redundant instructions.
- Any access failures, isolation failures, budget mismatch, unblinded reviewers, or incomplete outputs → INVALID / INCONCLUSIVE for the affected pairs. Never report a superiority percentage from invalid pairs.

## Current execution boundary
This chat cannot demonstrably launch independent GPT-6 inference contexts with synchronized model effort and equal budgets through available connectors. Creating this preregistration is NOT running an A/B. No nine outputs or blind judging exists yet. Do not populate results from the researcher's own same-thread rewordings. Follow up only in an agent environment that actually supports independent sessions (for example properly configured Work orchestration or external controlled eval harness); do not assume tools not connected are callable.
