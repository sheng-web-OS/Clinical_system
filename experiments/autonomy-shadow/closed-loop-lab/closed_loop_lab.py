#!/usr/bin/env python3
"""Clinical OS - isolated closed-loop executor contract, NOT production.

Research artifact pinned to PUBLIC Clinical_system PR #238 exact HEAD
 d8d70be13389879e32edfcae5b7b12db21d5acd1 (2026-10-30).
The program uses ONLY an in-memory synthetic GitHub backend and test-attested
execution contexts. It performs no network/connector calls and grants NO real
GitHub, billing, medical, publishing or scheduled-task authorization.

Hypothesis: bounded eligibility fallback + fenced CAS + post-write readback +
idempotent continuation can improve liveness without sacrificing safety.
"""
from __future__ import annotations
from dataclasses import dataclass, field, replace
from hashlib import sha256
from typing import Literal

PROTECTED = frozenset({224, 225, 234, 235})


class Hold(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class LostAcknowledgement(Exception):
    pass


def conflict(a: str, b: str) -> bool:
    if a == b:
        return True
    if a.startswith('path:') and b.startswith('path:'):
        x, y = a[5:], b[5:]
        return x.startswith(y + '/') or y.startswith(x + '/')
    return False


@dataclass(frozen=True)
class Identity:
    context: str
    run: str
    role: Literal['writer', 'qa']


@dataclass
class Task:
    id: str
    pr: int
    priority: int
    path: str
    # These are synthetically pre-authorized test paths, not actual PRs.
    start_head: str
    gate_id: str = 'repair'
    stage: str = 'READY'
    writer_context: str | None = None
    writer_run: str | None = None
    committed_head: str | None = None
    last_verified_head: str | None = None
    checkpoint_version: int = 0
    next_gate: str = 'repair'
    qa_context: str | None = None
    qa_run: str | None = None
    last_hold: str | None = None

    @property
    def resources(self) -> tuple[str, str]:
        return (f'pr:{self.pr}', f'path:{self.path}')

    @property
    def operation_id(self) -> str:
        # Deterministic task+input+gate intent, never a wall-clock/retry ID.
        return sha256(f'{self.id}\0{self.pr}\0{self.start_head}\0{self.gate_id}\0{self.path}\0synthetic-fix-v1'.encode()).hexdigest()


@dataclass
class Lease:
    task: str
    context: str
    run: str
    resources: tuple[str, ...]
    fence: int
    expires_at: int


@dataclass(frozen=True)
class Receipt:
    task: str
    pr: int
    previous_head: str
    new_head: str
    operation_id: str
    writer_context: str
    writer_run: str
    fence: int
    path: str


@dataclass
class Result:
    verdict: str
    task: str | None = None
    reason: str = ''
    checked: tuple[tuple[str, str], ...] = ()
    mutations: int = 0
    execution_authorized: bool = False  # NEVER platform authorization


class FakeGitHub:
    """Synthetic atomic CAS backend. NOT a model of authenticated GitHub API behavior."""
    def __init__(self, tasks: list[Task], *, mode='active'):
        self.tasks = {x.id: x for x in tasks}
        self.heads = {x.pr: x.start_head for x in tasks}
        self.leases: dict[str, Lease] = {}
        self.generation = 0
        self.receipts: dict[str, Receipt] = {}
        self.ci: dict[tuple[int, str], str] = {}
        self.qa_probes: dict[str, bool] = {}
        self.known_runs: set[Identity] = set()
        self.terminated: set[str] = set()
        self.mode = mode  # synthetic mode; real PR #238 is SHADOW
        self.trusted_control_plane = True
        self.write_count = 0
        self.checkpoint_write_count = 0
        self.failpoints: set[str] = set()
        self.read_count = 0
        self.delay_until: int | None = None

    def attest(self, identity: Identity):
        # Solely the test harness owns this authority.
        self.known_runs.add(identity)

    def attest_termination(self, run: str):
        # Solely test-harness-supplied trusted evidence; self-reported claims fail.
        self.terminated.add(run)

    def _assert_actor(self, who: Identity):
        if who not in self.known_runs:
            raise Hold('UNVERIFIED_PLATFORM_RUN')

    def _assert_scope(self, task: Task):
        if task.pr in PROTECTED:
            raise Hold('PROTECTED_EXPERIMENT_SCOPE')
        if not task.path or task.path == '.' or task.path.startswith('/') or '..' in task.path.split('/'):
            raise Hold('INVALID_RESOURCE_PATH')

    def _compatible(self, task: Task, lease: Lease) -> bool:
        return not any(conflict(a, b) for a in task.resources for b in lease.resources)

    def claim(self, task: Task, who: Identity, now: int, *, observed_generation: int) -> Lease:
        self._assert_actor(who)
        if who.role != 'writer':
            raise Hold('WRITER_ROLE_REQUIRED')
        self._assert_scope(task)
        if self.mode != 'active':
            raise Hold('SHADOW_NO_ACTION')
        if observed_generation != self.generation:
            raise Hold('STALE_LEASE_GENERATION')
        prior = self.receipts.get(task.operation_id)
        head = self.heads[task.pr]
        legitimate_replay = (prior is not None and prior.previous_head == task.start_head
                             and prior.path == task.path and prior.pr == task.pr
                             and prior.new_head == head)
        if head != task.start_head and head != task.committed_head and not legitimate_replay:
            raise Hold('HEAD_DRIFT_HOLD')
        removable = []
        for key, lease in self.leases.items():
            if key == task.id or not self._compatible(task, lease):
                if now < lease.expires_at:
                    raise Hold('ACTIVE_OWNER')
                if lease.run not in self.terminated:
                    raise Hold('EXPIRED_OWNER_REQUIRES_RECONCILIATION')
                removable.append(key)
        # All conflicts validated before changing lease table: fail-atomic claim.
        for key in removable:
            del self.leases[key]
        self.generation += 1
        claim = Lease(task.id, who.context, who.run, task.resources, self.generation, now + 20)
        self.leases[task.id] = claim
        return claim

    def assert_fence(self, claim: Lease, now: int) -> None:
        live = self.leases.get(claim.task)
        if live != claim:
            raise Hold('LEASE_FENCE_CHANGED')
        if now >= claim.expires_at:
            raise Hold('LEASE_EXPIRED')

    def release(self, claim: Lease):
        if self.leases.get(claim.task) != claim:
            raise Hold('LEASE_FENCE_CHANGED')
        del self.leases[claim.task]
        self.generation += 1

    def submit_fix(self, task: Task, claim: Lease, now: int) -> Receipt:
        self.assert_fence(claim, now)
        # Authorize the ACTUAL target at the final mutation boundary.
        if (claim.task != task.id or self.tasks.get(task.id) is not task
                or not set(task.resources).issubset(set(claim.resources))):
            raise Hold('CLAIM_TASK_SCOPE_MISMATCH')
        if 'RATE_LIMITED' in self.failpoints:
            self.delay_until = now + 30
            raise Hold('RATE_LIMITED')
        existing = self.receipts.get(task.operation_id)
        if existing is not None:
            if (existing.previous_head != task.start_head or
                self.heads[task.pr] != existing.new_head or
                existing.path != task.path or existing.pr != task.pr):
                raise Hold('RECEIPT_OR_HEAD_UNVERIFIED')
            return existing
        if self.heads[task.pr] != task.start_head:
            raise Hold('STALE_TARGET_HEAD')
        new_head = sha256((task.start_head + task.operation_id).encode()).hexdigest()[:40]
        receipt = Receipt(task.id, task.pr, task.start_head, new_head,
                          task.operation_id, claim.context, claim.run, claim.fence, task.path)
        # Atomic synthetic Git commit+receipt; ACK and checkpoint may be lost.
        self.heads[task.pr] = new_head
        self.receipts[task.operation_id] = receipt
        self.write_count += 1
        if 'ACK_LOST_ONCE' in self.failpoints:
            self.failpoints.remove('ACK_LOST_ONCE')
            raise LostAcknowledgement()
        return receipt

    def checkpoint(self, task: Task, *, version: int, next_stage: str,
                   head: str, writer: Receipt | None = None, qa: Identity | None = None):
        if task.checkpoint_version != version:
            raise Hold('STALE_CHECKPOINT_CAS')
        if head != self.heads[task.pr]:
            raise Hold('CHECKPOINT_HEAD_MISMATCH')
        # Simulated persistent checkpoint MUST enforce transitions itself;
        # a caller must never bypass QA through direct checkpoint invocation.
        if self.tasks.get(task.id) is not task:
            raise Hold('INVALID_CHECKPOINT_TRANSITION')
        transition = (task.stage, next_stage)
        if transition == ('READY', 'AWAITING_CI'):
            permitted = (writer is not None and qa is None
                         and writer.new_head == head)
        elif transition == ('AWAITING_CI', 'AWAITING_QA'):
            permitted = (writer is None and qa is None
                         and task.committed_head == head
                         and self.ci.get((task.pr, head)) == 'SUCCESS')
        elif transition in {('AWAITING_QA','VERIFIED_COMPLETE'),
                            ('AWAITING_QA','CHANGES_REQUESTED')}:
            permitted = (writer is None and qa is not None
                         and qa in self.known_runs and qa.role == 'qa'
                         and task.writer_context is not None
                         and task.writer_run is not None
                         and qa.context != task.writer_context
                         and qa.run != task.writer_run
                         and task.committed_head == head
                         and self.ci.get((task.pr, head)) == 'SUCCESS'
                         and self.qa_probes.get(task.id) is (next_stage == 'VERIFIED_COMPLETE'))
        else:
            permitted = False
        if not permitted:
            raise Hold('INVALID_CHECKPOINT_TRANSITION')
        if writer:
            if self.receipts.get(task.operation_id) != writer:
                raise Hold('UNVERIFIED_COMMIT_RECEIPT')
            task.committed_head = writer.new_head
            task.writer_context = writer.writer_context
            task.writer_run = writer.writer_run
        if qa:
            task.qa_context = qa.context
            task.qa_run = qa.run
        task.stage = next_stage
        task.next_gate = {'AWAITING_CI':'check-ci', 'AWAITING_QA':'independent-qa',
                          'VERIFIED_COMPLETE':'closed', 'CHANGES_REQUESTED':'repair-again'}.get(next_stage, task.next_gate)
        task.last_verified_head = head
        task.checkpoint_version += 1
        self.checkpoint_write_count += 1
        if 'CHECKPOINT_ACK_LOST_ONCE' in self.failpoints:
            self.failpoints.remove('CHECKPOINT_ACK_LOST_ONCE')
            raise LostAcknowledgement()


def writer_wake(db: FakeGitHub, who: Identity, now: int, *, max_scan=7) -> Result:
    """One scheduled synthetic writer wake: at most one useful next gate."""
    db._assert_actor(who)
    if who.role != 'writer':
        return Result('HOLD', reason='WRITER_ROLE_REQUIRED')
    if not db.trusted_control_plane:
        return Result('HOLD', reason='GLOBAL_CONTROL_PLANE_HOLD')
    if db.mode != 'active':
        return Result('HOLD', reason='SHADOW_NO_ACTION')
    if db.delay_until is not None and now < db.delay_until:
        return Result('HOLD', reason='RATE_LIMITED_BACKOFF')
    checked = []
    tasks = sorted(db.tasks.values(), key=lambda x: (-x.priority, x.id))
    for task in tasks[:max_scan]:
        try:
            db._assert_scope(task)
            db.read_count += 1
            if task.stage in {'VERIFIED_COMPLETE', 'AWAITING_QA'}:
                checked.append((task.id, 'WAITING_QA_OR_DONE'))
                continue
            if task.stage == 'AWAITING_CI':
                if task.committed_head != db.heads[task.pr]:
                    checked.append((task.id, 'CI_HEAD_DRIFT_HOLD'))
                    continue
                status = db.ci.get((task.pr, task.committed_head), 'PENDING')
                if status == 'PENDING':
                    checked.append((task.id, 'AWAITING_EXACT_HEAD_CI'))
                    continue
                if status != 'SUCCESS':
                    checked.append((task.id, 'CI_FAIL_HANDOFF'))
                    # No auto-repeat. A failed gate is task-local; let unrelated tasks advance.
                    continue
                before = task.checkpoint_version
                try:
                    db.checkpoint(task, version=before, next_stage='AWAITING_QA', head=db.heads[task.pr])
                except LostAcknowledgement:
                    # Read back before claiming failure or retrying.
                    if task.checkpoint_version != before + 1 or task.stage != 'AWAITING_QA':
                        return Result('HOLD',task.id,'CHECKPOINT_ACK_UNKNOWN',tuple(checked))
                checked.append((task.id, 'CI_ACCEPTED_NEEDS_QA'))
                return Result('GATE_ADVANCED',task.id,'AWAITING_INDEPENDENT_QA',tuple(checked))
            if task.stage == 'CHANGES_REQUESTED':
                checked.append((task.id, 'REVISED_REPAIR_PLAN_REQUIRED'))
                continue
            if task.stage != 'READY':
                checked.append((task.id, 'UNKNOWN_STAGE_HOLD'))
                continue
            # No speculative retry if checkpoint was lost after an acknowledged commit.
            gen = db.generation
            try:
                lease = db.claim(task, who, now, observed_generation=gen)
            except Hold as e:
                checked.append((task.id,e.reason))
                continue
            try:
                receipt = db.submit_fix(task,lease,now)
                before = task.checkpoint_version
                try:
                    db.checkpoint(task,version=before,next_stage='AWAITING_CI',head=receipt.new_head,writer=receipt)
                except LostAcknowledgement:
                    if task.checkpoint_version != before + 1 or task.stage != 'AWAITING_CI':
                        return Result('HOLD',task.id,'CHECKPOINT_ACK_UNKNOWN',tuple(checked))
                # The lease is released ONLY after exact commit/checkpoint readback.
                if db.heads[task.pr] != receipt.new_head or task.committed_head != receipt.new_head:
                    return Result('HOLD',task.id,'POSTWRITE_READBACK_MISMATCH',tuple(checked))
                db.release(lease)
                checked.append((task.id,'COMMIT_READBACK_VERIFIED'))
                return Result('GATE_ADVANCED',task.id,'AWAITING_EXACT_HEAD_CI',tuple(checked),
                              mutations=0 if receipt.writer_run != who.run else 1)
            except LostAcknowledgement:
                checked.append((task.id,'COMMIT_ACK_UNKNOWN'))
                # Cannot release or retry until exact HEAD+receipt/actor reconciliation.
                return Result('HOLD',task.id,'COMMIT_ACK_UNKNOWN',tuple(checked))
            except Hold as e:
                checked.append((task.id,e.reason))
                if e.reason in {'RECEIPT_OR_HEAD_UNVERIFIED', 'UNVERIFIED_COMMIT_RECEIPT',
                                'STALE_CHECKPOINT_CAS', 'CHECKPOINT_HEAD_MISMATCH',
                                'POSTWRITE_READBACK_MISMATCH'}:
                    return Result('HOLD',task.id,e.reason,tuple(checked))
                if e.reason == 'RATE_LIMITED':
                    try: db.release(lease)
                    except Hold: pass
                    return Result('HOLD',task.id,'RATE_LIMITED',tuple(checked))
                try: db.release(lease)
                except Hold: pass
                continue
        except Hold as e:
            checked.append((task.id, e.reason))
            continue
    return Result('NO_ACTION',reason='NO_SAFE_ACTIONABLE_GATE',checked=tuple(checked))


def qa_wake(db: FakeGitHub, who: Identity, now: int) -> Result:
    """Synthetic QA; skip task-local HOLD while preserving independent review."""
    db._assert_actor(who)
    if who.role != 'qa':
        return Result('HOLD', reason='QA_ROLE_REQUIRED')
    if not db.trusted_control_plane or db.mode != 'active':
        return Result('HOLD', reason='GLOBAL_OR_SHADOW_HOLD')
    first_block = None
    for task in sorted(db.tasks.values(), key=lambda x:(-x.priority,x.id)):
        if task.stage != 'AWAITING_QA':
            continue
        reason = None
        if task.writer_context is None or task.writer_run is None:
            reason = 'WRITER_PROVENANCE_MISSING'
        elif who.context == task.writer_context or who.run == task.writer_run:
            reason = 'REVIEW_NOT_INDEPENDENT'
        elif task.committed_head != db.heads[task.pr]:
            reason = 'REVIEW_STALE_HEAD'
        elif db.ci.get((task.pr, task.committed_head)) != 'SUCCESS':
            reason = 'CI_NOT_SUCCESS'
        elif db.qa_probes.get(task.id) is None:
            reason = 'QA_EVIDENCE_MISSING'
        if reason is not None:
            if first_block is None:
                first_block = Result('HOLD', task.id, reason)
            continue
        verdict = db.qa_probes[task.id]
        next_stage = 'VERIFIED_COMPLETE' if verdict else 'CHANGES_REQUESTED'
        before = task.checkpoint_version
        try:
            db.checkpoint(task, version=before, next_stage=next_stage,
                          head=task.committed_head, qa=who)
        except LostAcknowledgement:
            # A completed QA checkpoint can outlive a lost transport ACK.
            # Re-read the exact persisted transition before reporting success;
            # never retry the signing mutation or treat uncertainty as PASS.
            if (task.checkpoint_version != before + 1
                    or task.stage != next_stage
                    or task.last_verified_head != task.committed_head
                    or task.qa_context != who.context
                    or task.qa_run != who.run):
                return Result('HOLD', task.id, 'QA_CHECKPOINT_ACK_UNKNOWN')
        return Result('QA_ACCEPTED' if verdict else 'QA_REJECTED',task.id,next_stage)
    return first_block or Result('NO_ACTION',reason='NO_FROZEN_ARTIFACT_AWAITING_QA')


def example() -> dict:
    """A->B->QA synthetic sequence with a blocked higher-priority task."""
    a=Task('blocked-A',901,100,'synthetic/a.py','a'*40)
    b=Task('fix-B',902,90,'synthetic/b.py','b'*40)
    db=FakeGitHub([a,b]); writer_a=Identity('writer-slot','run-A','writer')
    writer_b=Identity('writer-slot','run-B','writer'); qa=Identity('qa-slot','run-Q','qa')
    for i in (writer_a,writer_b,qa): db.attest(i)
    db.leases[a.id]=Lease(a.id,'other-context','old-owner',a.resources,1,200)
    db.generation=1
    events=[]
    def snapshot(label,result):
        events.append({'run':label,'verdict':result.verdict,'task':result.task,
                       'reason':result.reason,'checked':list(result.checked),
                       'commits':db.write_count,'checkpoints':db.checkpoint_write_count})
    snapshot('Run A',writer_wake(db,writer_a,100))
    db.ci[(b.pr,b.committed_head)]='SUCCESS'
    snapshot('Run B',writer_wake(db,writer_b,101))
    db.qa_probes[b.id]=True
    snapshot('QA C',qa_wake(db,qa,102))
    snapshot('Run D no-change',writer_wake(db,writer_b,103))
    return {'simulation_only':True,'events':events,'task_B':replace(b).__dict__,
            'commits':db.write_count,'checkpoints':db.checkpoint_write_count}


if __name__ == '__main__':
    import json
    print(json.dumps(example(),ensure_ascii=False,indent=2))
