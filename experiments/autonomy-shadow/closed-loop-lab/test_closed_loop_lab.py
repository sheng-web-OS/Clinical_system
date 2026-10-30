"""Deterministic fault injection for isolated contract only; no external IO."""
import unittest
from dataclasses import replace
from closed_loop_lab import (FakeGitHub, Identity, Task, Lease, Hold, PROTECTED,
                             writer_wake,qa_wake,example)


def fixture(*,mode='active'):
    a=Task('a-blocked',901,100,'docs/a.py','a'*40)
    b=Task('b-fix',902,90,'docs/b.py','b'*40)
    c=Task('c-followup',903,80,'other/c.py','c'*40)
    db=FakeGitHub([a,b,c],mode=mode)
    W=Identity('engineering-slot','writer-run-A','writer')
    W2=Identity('engineering-slot','writer-run-B','writer')
    Q=Identity('qa-slot','qa-run-C','qa')
    for who in (W,W2,Q):db.attest(who)
    return db,a,b,c,W,W2,Q


class ClosedLoopContracts(unittest.TestCase):
    def test_01_baseline_closed_loop_no_duplicate_commit(self):
        d,a,b,c,w,w2,q=fixture()
        d.tasks={a.id:a}; d.heads={a.pr:a.start_head}
        x=writer_wake(d,w,100)
        self.assertEqual(('GATE_ADVANCED',a.id,'AWAITING_EXACT_HEAD_CI'),(x.verdict,x.task,x.reason))
        self.assertEqual(1,d.write_count)
        self.assertEqual('NO_ACTION',writer_wake(d,w2,101).verdict)
        d.ci[(a.pr,a.committed_head)]='SUCCESS'
        self.assertEqual('AWAITING_INDEPENDENT_QA',writer_wake(d,w2,102).reason)
        d.qa_probes[a.id]=True
        self.assertEqual('QA_ACCEPTED',qa_wake(d,q,103).verdict)
        self.assertEqual('VERIFIED_COMPLETE',a.stage)
        self.assertEqual(1,d.write_count)

    def test_02_active_A_yields_to_B_within_same_wake(self):
        d,a,b,c,w,w2,q=fixture()
        d.leases[a.id]=Lease(a.id,'old','old-run',a.resources,1,200)
        d.generation=1
        r=writer_wake(d,w,100)
        self.assertEqual('b-fix',r.task)
        self.assertIn(('a-blocked','ACTIVE_OWNER'),r.checked)
        self.assertEqual(1,d.write_count)

    def test_03_expired_A_no_termination_remains_blocked_B_proceeds(self):
        d,a,b,c,w,w2,q=fixture()
        d.leases[a.id]=Lease(a.id,'old','old-run',a.resources,1,99)
        d.generation=1
        r=writer_wake(d,w,100)
        self.assertEqual('b-fix',r.task)
        self.assertIn(('a-blocked','EXPIRED_OWNER_REQUIRES_RECONCILIATION'),r.checked)

    def test_04_expired_A_trusted_termination_fences_old_writer(self):
        d,a,b,c,w,w2,q=fixture()
        stale=Lease(a.id,'old','old-run',a.resources,1,99)
        d.leases[a.id]=stale;d.generation=1
        d.attest_termination('old-run')
        r=writer_wake(d,w,100)
        self.assertEqual('a-blocked',r.task)
        with self.assertRaisesRegex(Hold,'LEASE_FENCE_CHANGED'):
            d.assert_fence(stale,100)

    def test_05_spoofed_platform_identity_fails(self):
        d,a,b,c,w,w2,q=fixture()
        fake=Identity('bad','forged','writer')
        with self.assertRaisesRegex(Hold,'UNVERIFIED_PLATFORM_RUN'):
            writer_wake(d,fake,100)

    def test_06_ack_lost_commit_requires_trusted_reconciliation(self):
        d,a,b,c,w,w2,q=fixture()
        d.failpoints.add('ACK_LOST_ONCE')
        r=writer_wake(d,w,100)
        self.assertEqual('COMMIT_ACK_UNKNOWN',r.reason)
        self.assertEqual(1,d.write_count)
        self.assertEqual('READY',a.stage)
        # Before expiry, other writer cannot replay A and can work on B.
        r2=writer_wake(d,w2,101)
        self.assertEqual('b-fix',r2.task)
        self.assertEqual(2,d.write_count)
        # After expiry, no auto takeover without attested old-run termination.
        c.stage='AWAITING_QA'  # prevent a third independent work unit in this fixture
        r3=writer_wake(d,w2,121)
        self.assertIn(('a-blocked','EXPIRED_OWNER_REQUIRES_RECONCILIATION'),r3.checked)
        self.assertEqual(2,d.write_count)
        d.attest_termination(w.run)
        r4=writer_wake(d,w2,122)
        self.assertEqual('a-blocked',r4.task)
        self.assertEqual(2,d.write_count)  # dedup by operation intent + readback
        self.assertEqual('AWAITING_CI',a.stage)
        self.assertEqual(w.run,a.writer_run)  # original commit author preserved

    def test_07_head_drift_fail_closed(self):
        d,a,b,c,w,w2,q=fixture()
        d.heads[a.pr]='0'*40
        r=writer_wake(d,w,100)
        self.assertEqual('b-fix',r.task)
        self.assertIn(('a-blocked','HEAD_DRIFT_HOLD'),r.checked)
        self.assertEqual(1,d.write_count)

    def test_08_rate_limit_backoff_never_busy_loops(self):
        d,a,b,c,w,w2,q=fixture()
        d.failpoints.add('RATE_LIMITED')
        r=writer_wake(d,w,100)
        self.assertEqual('RATE_LIMITED',r.reason)
        self.assertEqual(0,d.write_count)
        self.assertEqual('RATE_LIMITED_BACKOFF',writer_wake(d,w2,101).reason)
        self.assertEqual(0,d.write_count)
        d.failpoints.remove('RATE_LIMITED')
        self.assertEqual('GATE_ADVANCED',writer_wake(d,w2,131).verdict)

    def test_09_checkpoint_ack_lost_readback_no_replay(self):
        d,a,b,c,w,w2,q=fixture()
        d.tasks={a.id:a}; d.heads={a.pr:a.start_head}
        d.failpoints.add('CHECKPOINT_ACK_LOST_ONCE')
        self.assertEqual('GATE_ADVANCED',writer_wake(d,w,100).verdict)
        self.assertEqual(1,d.write_count)
        self.assertEqual('AWAITING_CI',a.stage)
        self.assertEqual('NO_ACTION',writer_wake(d,w2,101).verdict)
        self.assertEqual(1,d.write_count)

    def test_10_fake_ci_success_wrong_head_cannot_pass(self):
        d,a,b,c,w,w2,q=fixture()
        d.tasks={a.id:a}; d.heads={a.pr:a.start_head}
        writer_wake(d,w,100)
        d.ci[(a.pr,'0'*40)]='SUCCESS'
        self.assertEqual('NO_ACTION',writer_wake(d,w2,101).verdict)
        self.assertEqual('AWAITING_CI',a.stage)

    def test_11_self_review_rejected_separate_reviewer_passes(self):
        d,a,b,c,w,w2,q=fixture()
        d.tasks={a.id:a}; d.heads={a.pr:a.start_head}
        writer_wake(d,w,100)
        d.ci[(a.pr,a.committed_head)]='SUCCESS'
        writer_wake(d,w2,101)
        forged=Identity(w.context,'qa-run-same-context','qa')
        d.attest(forged)
        d.qa_probes[a.id]=True
        self.assertEqual('REVIEW_NOT_INDEPENDENT',qa_wake(d,forged,102).reason)
        self.assertEqual('QA_ACCEPTED',qa_wake(d,q,103).verdict)

    def test_12_qa_rejection_never_pretends_success(self):
        d,a,b,c,w,w2,q=fixture()
        d.tasks={a.id:a}; d.heads={a.pr:a.start_head}
        writer_wake(d,w,100)
        d.ci[(a.pr,a.committed_head)]='SUCCESS';writer_wake(d,w2,101)
        d.qa_probes[a.id]=False
        self.assertEqual('QA_REJECTED',qa_wake(d,q,102).verdict)
        self.assertEqual('CHANGES_REQUESTED',a.stage)

    def test_13_shadow_never_mutates(self):
        d,a,b,c,w,w2,q=fixture(mode='shadow')
        self.assertEqual('SHADOW_NO_ACTION',writer_wake(d,w,100).reason)
        self.assertEqual(0,d.write_count)

    def test_14_global_hold_does_not_fallback(self):
        d,a,b,c,w,w2,q=fixture()
        d.trusted_control_plane=False
        self.assertEqual('GLOBAL_CONTROL_PLANE_HOLD',writer_wake(d,w,100).reason)
        self.assertEqual(0,d.write_count)

    def test_15_protected_cohort_not_modified(self):
        d,a,b,c,w,w2,q=fixture()
        p=Task('experiment-protected',225,200,'experiments/x.py','f'*40)
        d.tasks[p.id]=p;d.heads[p.pr]=p.start_head
        r=writer_wake(d,w,100)
        self.assertIn((p.id,'PROTECTED_EXPERIMENT_SCOPE'),r.checked)
        self.assertEqual(0,len([v for v in d.receipts.values() if v.pr in PROTECTED]))

    def test_16_ancestor_lock_blocks_branch_but_unrelated_moves(self):
        d,a,b,c,w,w2,q=fixture()
        d.leases['other']=Lease('other','old','old-run',('path:docs',),1,200)
        d.generation=1
        r=writer_wake(d,w,100)
        self.assertEqual('c-followup',r.task)
        self.assertIn((a.id,'ACTIVE_OWNER'),r.checked)
        self.assertIn((b.id,'ACTIVE_OWNER'),r.checked)

    def test_17_no_repeated_checkpoint_when_no_ci(self):
        d,a,b,c,w,w2,q=fixture()
        d.tasks={a.id:a}; d.heads={a.pr:a.start_head}
        writer_wake(d,w,100)
        v=d.checkpoint_write_count
        writer_wake(d,w2,101)
        self.assertEqual(v,d.checkpoint_write_count)

    def test_18_wrong_stale_checkpoint_cas_rejected(self):
        d,a,b,c,w,w2,q=fixture()
        with self.assertRaisesRegex(Hold,'STALE_CHECKPOINT_CAS'):
            d.checkpoint(a,version=100,next_stage='AWAITING_QA',head=a.start_head)

    def test_19_bounded_fallback_stops_at_scan_limit(self):
        d,a,b,c,w,w2,q=fixture()
        d.leases[a.id]=Lease(a.id,'old','old-run',a.resources,1,200)
        d.generation=1
        r=writer_wake(d,w,100,max_scan=1)
        self.assertEqual('NO_ACTION',r.verdict)
        self.assertEqual(0,d.write_count)

    def test_20_ci_success_is_not_qa_acceptance(self):
        d,a,b,c,w,w2,q=fixture()
        d.tasks={a.id:a}; d.heads={a.pr:a.start_head}
        writer_wake(d,w,100)
        d.ci[(a.pr,a.committed_head)]='SUCCESS'
        r=writer_wake(d,w2,101)
        self.assertEqual('AWAITING_QA',a.stage)
        self.assertNotEqual('VERIFIED_COMPLETE',a.stage)

    def test_21_no_auth_by_return_value(self):
        r=example()
        self.assertTrue(r['simulation_only'])
        self.assertTrue(all(x['verdict'] != 'PLATFORM_AUTHORIZED' for x in r['events']))


if __name__ == '__main__':
    unittest.main(verbosity=2)

class AdditionalAdversarialContracts(unittest.TestCase):
    def test_22_claim_is_fail_atomic_if_multiple_conflicts(self):
        db,a,b,c,w,w2,q=fixture()
        expired=Lease('expired','x','old-terminated',('path:docs',),1,50)
        active=Lease('active','x','old-active',('pr:901',),2,200)
        db.leases={'expired':expired,'active':active};db.generation=2
        db.attest_termination('old-terminated')
        with self.assertRaisesRegex(Hold,'ACTIVE_OWNER'):
            db.claim(a,w,100,observed_generation=2)
        self.assertEqual({'expired':expired,'active':active},db.leases)
        self.assertEqual(2,db.generation)

    def test_23_stale_lease_generation_prevents_parallel_claim(self):
        db,a,b,c,w,w2,q=fixture()
        old_generation=db.generation
        db.claim(a,w,100,observed_generation=old_generation)
        with self.assertRaisesRegex(Hold,'STALE_LEASE_GENERATION'):
            db.claim(b,w2,100,observed_generation=old_generation)
        self.assertEqual(1,len(db.leases))

    def test_24_unrelated_job_progresses_after_exact_head_ci_failure(self):
        db,a,b,c,w,w2,q=fixture()
        writer_wake(db,w,100)
        db.ci[(a.pr,a.committed_head)]='FAILED'
        r=writer_wake(db,w2,101)
        self.assertEqual('b-fix',r.task)
        self.assertIn((a.id,'CI_FAIL_HANDOFF'),r.checked)
        self.assertEqual(2,db.write_count)

    def test_25_unknown_commit_receipt_holds_that_task_only(self):
        db,a,b,c,w,w2,q=fixture()
        db.failpoints.add('ACK_LOST_ONCE')
        writer_wake(db,w,100)
        db.attest_termination(w.run)
        prior=db.receipts[a.operation_id]
        # Deliberately corrupt receipt; readback must fail closed.
        db.receipts[a.operation_id]=replace(prior,path='different/unsafe.py')
        r=writer_wake(db,w2,121)
        self.assertEqual('b-fix',r.task)
        self.assertIn((a.id,'HEAD_DRIFT_HOLD'),r.checked)
        self.assertEqual(2,db.write_count)

    def test_26_qa_changed_head_rejects_former_ci(self):
        db,a,b,c,w,w2,q=fixture()
        db.tasks={a.id:a};db.heads={a.pr:a.start_head}
        writer_wake(db,w,100)
        db.ci[(a.pr,a.committed_head)]='SUCCESS'
        writer_wake(db,w2,101)
        db.heads[a.pr]='f'*40
        db.qa_probes[a.id]=True
        self.assertEqual('REVIEW_STALE_HEAD',qa_wake(db,q,102).reason)
        self.assertNotEqual('VERIFIED_COMPLETE',a.stage)

    def test_27_qa_rejection_without_new_repair_plan_cannot_repeat_fix(self):
        db,a,b,c,w,w2,q=fixture()
        db.tasks={a.id:a};db.heads={a.pr:a.start_head}
        writer_wake(db,w,100)
        db.ci[(a.pr,a.committed_head)]='SUCCESS'
        writer_wake(db,w2,101)
        db.qa_probes[a.id]=False
        qa_wake(db,q,102)
        self.assertEqual('NO_ACTION',writer_wake(db,w2,103).verdict)
        self.assertEqual(1,db.write_count)

    def test_28_claim_does_not_authorize_real_mutation(self):
        db,a,b,c,w,w2,q=fixture()
        claim=db.claim(a,w,100,observed_generation=db.generation)
        self.assertEqual(0,db.write_count)
        self.assertEqual(a.id,claim.task)
        self.assertNotEqual(db.mode,'production')
