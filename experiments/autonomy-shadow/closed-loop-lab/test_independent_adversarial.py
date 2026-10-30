"""Independent adversarial tests against the synthetic #248 contract, not production."""
import copy
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).parent))
from closed_loop_lab import FakeGitHub, Identity, Task, Hold, writer_wake, qa_wake


def fixture():
    a = Task('task-a', 901, 100, 'docs/a.py', 'a'*40)
    b = Task('task-b', 902, 90, 'docs/b.py', 'b'*40)
    db = FakeGitHub([a, b])
    writer = Identity('writer-slot', 'writer-run-A', 'writer')
    reviewer = Identity('qa-slot', 'qa-run-Q', 'qa')
    db.attest(writer); db.attest(reviewer)
    return db, a, b, writer, reviewer

class IndependentAdversarialTests(unittest.TestCase):
    def test_01_lease_for_A_cannot_mutate_B(self):
        db,a,b,w,q=fixture()
        lease=db.claim(a,w,100,observed_generation=0)
        with self.assertRaisesRegex(Hold,'CLAIM_TASK_SCOPE_MISMATCH'):
            db.submit_fix(b,lease,100)
        self.assertEqual(b.start_head,db.heads[b.pr])
        self.assertEqual(0,db.write_count)

    def test_02_checkpoint_cannot_self_certify_without_CI_QA(self):
        db,a,b,w,q=fixture()
        with self.assertRaisesRegex(Hold,'INVALID_CHECKPOINT_TRANSITION'):
            db.checkpoint(a,version=0,next_stage='VERIFIED_COMPLETE',head=a.start_head)
        self.assertEqual('READY',a.stage)
        self.assertIsNone(a.qa_run)

    def test_03_unreviewable_A_does_not_starve_reviewable_B(self):
        db,a,b,w,q=fixture()
        for task in (a,b):
            task.stage='AWAITING_QA'
            task.committed_head=task.start_head
            db.ci[(task.pr,task.start_head)]='SUCCESS'
            db.qa_probes[task.id]=True
        a.writer_context='qa-slot';a.writer_run='earlier-writer'
        b.writer_context='writer-slot';b.writer_run='writer-run-A'
        result=qa_wake(db,q,100)
        self.assertEqual('QA_ACCEPTED',result.verdict)
        self.assertEqual(b.id,result.task)
        self.assertEqual('AWAITING_QA',a.stage)
        self.assertEqual('VERIFIED_COMPLETE',b.stage)

    def test_04_qa_identity_cannot_acquire_writer_lease(self):
        db,a,b,w,q=fixture()
        with self.assertRaisesRegex(Hold,'WRITER_ROLE_REQUIRED'):
            db.claim(a,q,100,observed_generation=0)
        self.assertEqual(0,len(db.leases))
        self.assertEqual(0,db.write_count)

    def _advance_to_qa(self, db, task, writer, now):
        self.assertEqual(task.id, writer_wake(db, writer, now).task)
        db.ci[(task.pr, task.committed_head)] = 'SUCCESS'
        self.assertEqual(task.id, writer_wake(db, writer, now + 1).task)
        self.assertEqual('AWAITING_QA', task.stage)
        db.qa_probes[task.id] = True

    def test_05_missing_writer_provenance_does_not_starve_B(self):
        for missing in ('writer_context', 'writer_run'):
            with self.subTest(missing=missing):
                db,a,b,w,q=fixture()
                self._advance_to_qa(db, a, w, 100)
                self._advance_to_qa(db, b, w, 102)
                setattr(a, missing, None)
                unchanged_a = copy.deepcopy(a)
                result = qa_wake(db, q, 104)
                self.assertEqual(('QA_ACCEPTED', b.id), (result.verdict, result.task))
                self.assertEqual(unchanged_a, a)
                self.assertEqual('VERIFIED_COMPLETE', b.stage)
                self.assertEqual(2, db.write_count)
                self.assertFalse(result.execution_authorized)

    def test_06_missing_writer_provenance_alone_returns_unchanged_hold(self):
        for missing in ('writer_context', 'writer_run'):
            with self.subTest(missing=missing):
                db,a,b,w,q=fixture()
                db.tasks = {a.id: a}
                db.heads = {a.pr: a.start_head}
                self._advance_to_qa(db, a, w, 100)
                setattr(a, missing, None)
                before = copy.deepcopy(db.__dict__)
                result = qa_wake(db, q, 102)
                self.assertEqual(('HOLD', a.id, 'WRITER_PROVENANCE_MISSING'),
                                 (result.verdict, result.task, result.reason))
                self.assertEqual(before, db.__dict__)

    def test_07_missing_writer_provenance_never_overrides_global_hold(self):
        db,a,b,w,q=fixture()
        self._advance_to_qa(db, a, w, 100)
        self._advance_to_qa(db, b, w, 102)
        a.writer_run = None
        db.trusted_control_plane = False
        before = copy.deepcopy(db.__dict__)
        result = qa_wake(db, q, 104)
        self.assertEqual('HOLD', result.verdict)
        self.assertEqual('GLOBAL_OR_SHADOW_HOLD', result.reason)
        self.assertEqual(before, db.__dict__)


    def test_08_qa_checkpoint_ack_lost_after_write_is_reconciled(self):
        # A real reviewer verdict persisted but the checkpoint response was lost.
        # Writer path already reconciles this; QA must do the same without double-signing.
        db, a, b, w, q = fixture()
        db.tasks = {a.id: a}
        db.heads = {a.pr: a.start_head}
        self._advance_to_qa(db, a, w, 100)
        before = a.checkpoint_version
        db.failpoints.add('CHECKPOINT_ACK_LOST_ONCE')
        result = qa_wake(db, q, 102)
        self.assertEqual(('QA_ACCEPTED', a.id, 'VERIFIED_COMPLETE'),
                         (result.verdict, result.task, result.reason))
        self.assertEqual(before + 1, a.checkpoint_version)
        self.assertEqual(1, db.write_count)
        self.assertEqual('VERIFIED_COMPLETE', a.stage)
        self.assertEqual(q.run, a.qa_run)
        self.assertEqual(0, len(db.failpoints))
        self.assertEqual('NO_ACTION', qa_wake(db, q, 103).verdict)

if __name__=='__main__': unittest.main()
