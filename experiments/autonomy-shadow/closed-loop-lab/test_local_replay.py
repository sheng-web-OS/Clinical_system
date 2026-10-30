"""A/B/QA must be separate OS Python processes; local fixture only."""
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT=Path(__file__).resolve().parent


class ProcessSeparatedReplay(unittest.TestCase):
    def run_cli(self,cmd,state):
        p=subprocess.run([sys.executable,str(ROOT/'local_replay.py'),cmd,str(state)],
                         check=True,text=True,capture_output=True,timeout=8)
        return json.loads(p.stdout)

    def test_29_writer_runA_runB_independentQA_restart_and_noop(self):
        with TemporaryDirectory() as tmp:
            state=Path(tmp)/'local-only-synthetic-checkpoint.json'
            seq=[]
            for command in ['init','writer-A','mark-ci-success','writer-B','qa-C','writer-D','inspect']:
                seq.append(self.run_cli(command,state))
            self.assertEqual('repair-unrelated-task',seq[1]['task'])
            self.assertEqual('GATE_ADVANCED',seq[1]['verdict'])
            self.assertEqual('GATE_ADVANCED',seq[3]['verdict'])
            self.assertEqual('QA_ACCEPTED',seq[4]['verdict'])
            self.assertEqual('NO_ACTION',seq[5]['verdict'])
            self.assertEqual({'stage':'VERIFIED_COMPLETE','commits':1,
                              'checkpoints':3,'qa_run':'run-Q','head':seq[6]['head']},
                             {k:v for k,v in seq[6].items() if k in {'stage','commits','checkpoints','qa_run','head'}})

    def test_30_reject_nonfixture_state(self):
        from local_replay import decode
        with self.assertRaisesRegex(ValueError,'UNTRUSTED_OR_NOT_A_LAB_FIXTURE'):
            decode({'tasks':[]})

    def test_31_does_not_double_commit_on_replayed_writer_A(self):
        with TemporaryDirectory() as tmp:
            state=Path(tmp)/'local-only.json'
            self.run_cli('init',state)
            self.run_cli('writer-A',state)
            self.run_cli('writer-A',state)
            read=self.run_cli('inspect',state)
            self.assertEqual(1,read['commits'])
            self.assertEqual(1,read['checkpoints'])
