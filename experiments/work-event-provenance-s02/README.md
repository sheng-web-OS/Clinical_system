# EVLOOP-S02 — Event/run provenance negative gate

Status: **Draft / HOLD / OWNER_DIRECTED_PARALLEL**. This is a standalone, public, synthetic, standard-library-only experiment, **not** a second GitHub-to-Work wake trial. Do not merge, activate, publish, or count as original #137/#159 autonomous performance.

## Problem

GitHub PR #240 proved that an ARM commit object was created, the PR branch HEAD later moved (after an explicit CAS repair), GitHub Actions saw a 'synchronize' event on the expected SHA, and the ChatGPT event-task platform recorded one 'no_update' run. Those observations **do not establish** that the GitHub delivery initiated the particular ChatGPT run. No event delivery identity, provider-attested event→run binding, or real repair receipt was exposed.

## Source-of-truth hierarchy

1. Git commit object: object exists; **does not mean** the branch moved.
2. Git branch/PR: expected head and PR activity are independently read back; **does not mean** Work was triggered.
3. Work task/run: the authenticated platform returns actual task and run records; **does not identify** the triggering delivery without a link.
4. Application processing: a platform-result receipt referring to an exact head and nonce may show that the run processed that state; **does not certify** why the run began.
5. Provider event→run attestation: requires an authenticated source record linking the delivery/event ID (or an equivalent unique event identity) to the exact ChatGPT task/run. A self-supplied 'binding' JSON or PR comment is not proof.

The verifier implements steps 1-4 as **consistency and negative checks only**. It does not authenticate records, make network calls or return PASS/VERIFIED. Platform causal attribution remains INCONCLUSIVE until a legitimate trusted adapter is available. GitHub webhook HMAC signatures for an owner-managed receiver cannot be repurposed to attest ChatGPT's managed webhook.

## Run

From this directory:

    python3 -m unittest discover -s . -p 'test_provenance_probe.py' -v
    python3 provenance_probe.py s01_observed.json

The tests exercise 24 fixed scenarios: real S01 inconclusive, forged bindings, time coincidence, wrong run/task/PR/head/delivery, stale latest_result, booleans masquerading as PR IDs, fake event IDs, and self-reported receipts. Engineering test success is **not** Work event provenance.

## Isolation and next gate

- Only files in this isolated new directory are in scope.
- No GitHub workflow changes, no active dispatcher, no new automation, no second ARM, no run_now, no original 72h study inputs, no medical/PHI or publication.
- #240 is INCONCLUSIVE pending independent QA failure/cleanup closeout; #241 quota/recovery remains QUEUED/HOLD until its own prerequisites.
- Independent QA must inspect the actual HEAD, diff and Python tests; an event→run PASS additionally requires trusted provider-native correlation that this code does not have.

Reference: #240, #241, https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt and https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
