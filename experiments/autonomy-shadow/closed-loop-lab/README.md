# Clinical OS: Closed-loop autonomy lab (offline only)

**2026-10-30 — owner-directed synthetic research artifact. Submitted for isolated Draft review, never a production integration.**

## Problem and evidence boundary

Pinned design reference: `sheng-web-OS/Clinical_system`, Draft PR #238, exact HEAD
`d8d70be13389879e32edfcae5b7b12db21d5acd1`. Referenced modules:
`tools/dispatch_reconcile.py`, `tools/dispatch_runtime.py`, `tools/dispatch_selector.py`,
and `ops/dispatch.json`.

The project contract at Issue #241 is `QUEUED_HOLD` until the independent #240 closeout and original
#137 preregistered window ends **2026-11-01T06:20:15Z**. The first live no-nudge
Run A -> Run B -> independent QA is **NOT VERIFIED**.

These files use *synthetic task IDs* and an in-memory `FakeGitHub`. `local_replay.py`
serializes the fake state to **local JSON only** to demonstrate state transfer
across separate OS processes. The JSON is **not** a production ledger,
GitHub CAS/lease implementation, authenticated identity, real CI, GitHub event
wake-up, or a real repair. The fake `active` mode is an isolated lab setting:
real PR #238 remains Shadow. No network, paid API, medical artifact, or real
GitHub mutation is performed.

## Reproduce

```bash
cd clinical_os_closed_loop_lab
python -m unittest discover -s . -p 'test_*.py' -v
python closed_loop_lab.py

# Seven invocations = separate Python processes, same local synthetic file:
python local_replay.py init /tmp/clinical-os-synthetic.json
python local_replay.py writer-A /tmp/clinical-os-synthetic.json
python local_replay.py mark-ci-success /tmp/clinical-os-synthetic.json
python local_replay.py writer-B /tmp/clinical-os-synthetic.json
python local_replay.py qa-C /tmp/clinical-os-synthetic.json
python local_replay.py writer-D /tmp/clinical-os-synthetic.json
python local_replay.py inspect /tmp/clinical-os-synthetic.json
```

`mark-ci-success` **injects a synthetic CI PASS**. `qa-C` **injects a synthetic QA fixture**.
Their names are not evidence that real CI or independent clinical/engineering
review occurred.

## Closed-loop contract

1. Global control-plane invalid / real manifest Shadow -> no work.
2. Locally blocked highest priority -> scan a bounded next candidate; never
   overwrite the current owner or inherit authority from issue metadata.
3. Claim is fenced by generation, head, paths, and run ID; TTL expiry alone
   cannot transfer ownership. Test-harness **attested termination** enables
   a synthetic takeover after the expiry. Real provider attestation and live
   lease-ref CAS are unavailable in this lab.
4. One bounded synthetic code mutation, exact mock-head readback and
   per-task checkpoint. An ACK-lost commit is reconciled by immutable
   operation ID and receipt rather than resent. Actual GitHub may not offer
   atomic commit+receipt; deploy only after independent readback/recovery proof.
5. Later writer wake observes CI pinned to the exact mock head, advances only
   the checkpoint; it does not repeat the repair. CI failure is task-local.
6. Different, test-attested QA context checks the same mock head, CI and
   simulated QA verdict; only then may `VERIFIED_COMPLETE` occur.
7. Unchanged subsequent wake returns `NO_ACTION` and makes zero new commits.

## Safety and liveness fault tests

31 tests include: active/expired/conflicting leases, expired lease with/without
trusted terminal evidence, stale lease generation/fence/HEAD, ancestor lock,
protected preregistered cohort, spoofed run, ACK-lost commit, checkpoint
ACK-lost, wrong-head CI, CI failure not starving other jobs, API rate-limit
backoff, stale QA head, same-context self-review refusal, QA rejection, per-task
vs global HOLD, finite queue scans, and subprocess-separated Run A -> Run B ->
independent-QA-style fixture + no-op replay.

## Not yet proved / production integration gates

- **Actual GitHub authority**: read fresh protected `main` AGENTS, reviewed
  active manifest, permitted Issue/PR mapping and complete exact changed paths.
- **Live concurrency**: shared `runtime/dispatch-leases` ref, Git non-force
  expected-SHA CAS+readback, issuance of fencing generations and safe expiry
  reconciliation under overlapping actual writer sessions. An in-memory fake
  cannot prove that a concurrent external actor obeys the fence.
- **ACK uncertainty on GitHub**: committing an update and writing a separate
  receipt are not one atomic GitHub operation. Use commit ancestry/tree/path
  evidence on next wake; never blindly repeat a write after lost response.
- **Real version-bound CI and QA**: exact SHA job/logs and independent real
  automation task/run identities; GitHub login is insufficient.
- **No-nudge liveness**: scheduled Run A then a separate actual scheduled Run B
  then separate QA task/run without owner prompting or `run_now`.
- **Auditability**: no user private/patient info/credentials in PUBLIC PRs;
  no paid service, publication or medical approval by the dispatcher.
- **Invariant**: original Issue #137, #159, #224, #225, #234, #235 frozen
  until preregistered closure; all this work is `OWNER_DIRECTED_RESEARCH`
  and contributes **zero** to the original autonomous-success numerator.

## Recommended first post-freeze integration unit

Use existing Issue #241 and original #238 codepaths after its gates unlock.
Write an independent integration test for **claim collision after selection**:
A remains active/expired and un-reconciled, B independent and actionable,
`max_tasks_per_run=1`, two separate scheduled runs, no duplicate writes.
Fail if blocked A starves B, if the old owner is overwritten, if missing
reviewer identity is accepted, or if checkpoint cannot be read back. Do not
activate the dispatcher or merge/publish to get a green demonstration.
## GitHub source status

All four original Python code and test files have been uploaded individually and verified byte-for-byte against the original Git blobs. The isolated 31-test suite is also registered through `tests/test_closed_loop_lab_bridge.py`, so the existing `python -m unittest discover -s tests` GitHub CI can run it. Original local transcript JSON traces and the prior local result log are **not** committed, because they can be reproduced using the commands above; they are available in the user-provided research package. This remains a synthetic **Artifact / HOLD**, not an active Dispatcher or real cross-run proof.
