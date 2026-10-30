"""Independent adversarial tests against the synthetic #248 contract, not production."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).parent))
from closed_loop_lab import FakeGitHub, Identity, Task, Hold, qa_wake


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

if __name__=='__main__': unittest.main()
