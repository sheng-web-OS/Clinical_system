#!/usr/bin/env python3
"""Process-separated, synthetic-only restart replay of closed_loop_lab.

Local JSON is an interchangeable test fixture standing in for the future
GitHub Issue/PR checkpoint. It is NOT a live GitHub store, lock, proof of
ChatGPT Work wake identity, or permission to deploy the dispatcher.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import tempfile
from closed_loop_lab import FakeGitHub, Identity, Task, Lease, Receipt, writer_wake, qa_wake

ACTORS = {
    'run-A': Identity('engineering-scheduled-slot', 'run-A', 'writer'),
    'run-B': Identity('engineering-scheduled-slot', 'run-B', 'writer'),
    'run-Q': Identity('independent-qa-scheduled-slot', 'run-Q', 'qa'),
}


def bootstrap() -> FakeGitHub:
    a=Task('blocked-high-priority',901,100,'synthetic/a.py','a'*40)
    b=Task('repair-unrelated-task',902,90,'synthetic/b.py','b'*40)
    db=FakeGitHub([a,b]); db.generation=1
    db.leases[a.id]=Lease(a.id,'other-writer','unobserved-active-run',a.resources,1,200)
    for actor in ACTORS.values(): db.attest(actor)
    return db


def encode(db: FakeGitHub) -> dict:
    return {'test_fixture_only':True,'mode':db.mode,'trusted_control_plane':db.trusted_control_plane,
            'generation':db.generation,'heads':{str(k):v for k,v in db.heads.items()},
            'tasks':[asdict(t) for t in db.tasks.values()],
            'leases':[asdict(l) for l in db.leases.values()],
            'receipts':[asdict(r) for r in db.receipts.values()],
            'ci':[{'pr':pr,'head':head,'status':v} for (pr,head),v in db.ci.items()],
            'qa_probes':db.qa_probes,'terminated':sorted(db.terminated),
            'write_count':db.write_count,'checkpoint_write_count':db.checkpoint_write_count,
            'read_count':db.read_count,'delay_until':db.delay_until}


def decode(v:dict) -> FakeGitHub:
    if v.get('test_fixture_only') is not True:
        raise ValueError('UNTRUSTED_OR_NOT_A_LAB_FIXTURE')
    tasks=[Task(**x) for x in v['tasks']]
    db=FakeGitHub(tasks,mode=v['mode'])
    db.trusted_control_plane=v['trusted_control_plane']
    db.generation=v['generation'];db.heads={int(k):h for k,h in v['heads'].items()}
    db.leases={x['task']:Lease(**{**x,'resources':tuple(x['resources'])}) for x in v['leases']}
    db.receipts={x['operation_id']:Receipt(**x) for x in v['receipts']}
    db.ci={(x['pr'],x['head']):x['status'] for x in v['ci']}
    db.qa_probes=v['qa_probes'];db.terminated=set(v['terminated'])
    db.write_count=v['write_count'];db.checkpoint_write_count=v['checkpoint_write_count']
    db.read_count=v['read_count'];db.delay_until=v['delay_until']
    for actor in ACTORS.values():db.attest(actor)
    return db


def store(path:Path,db:FakeGitHub):
    # Local-only atomic single-process handoff, NOT a cross-process CAS lock.
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.clinical-os-lab-')
    try:
        with os.fdopen(fd,'w',encoding='utf8') as f:
            json.dump(encode(db),f,sort_keys=True,indent=2)
            f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


def load(path:Path) -> FakeGitHub:
    return decode(json.loads(path.read_text(encoding='utf8')))


def execute(command:str,db:FakeGitHub):
    if command=='writer-A':
        result=writer_wake(db,ACTORS['run-A'],100)
    elif command=='mark-ci-success':
        task=db.tasks['repair-unrelated-task']
        if not task.committed_head:
            raise ValueError('NO_COMMIT_TO_TEST')
        db.ci[(task.pr,task.committed_head)]='SUCCESS'
        return {'event':'SYNTHETIC_CI_SUCCESS_INJECTED','exact_head':task.committed_head}
    elif command=='writer-B':
        result=writer_wake(db,ACTORS['run-B'],101)
    elif command=='qa-C':
        db.qa_probes['repair-unrelated-task']=True
        result=qa_wake(db,ACTORS['run-Q'],102)
    elif command=='writer-D':
        result=writer_wake(db,ACTORS['run-B'],103)
    elif command=='inspect':
        return {'stage':db.tasks['repair-unrelated-task'].stage,'commits':db.write_count,
                'checkpoints':db.checkpoint_write_count,'head':db.heads[902],
                'qa_run':db.tasks['repair-unrelated-task'].qa_run}
    else:
        raise ValueError('UNKNOWN_COMMAND')
    return {'verdict':result.verdict,'reason':result.reason,'task':result.task,
            'checked':result.checked,'commits':db.write_count,
            'checkpoints':db.checkpoint_write_count}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('command',choices=['init','writer-A','mark-ci-success','writer-B','qa-C','writer-D','inspect'])
    p.add_argument('fixture_path',type=Path)
    args=p.parse_args()
    if args.command=='init':
        db=bootstrap();out={'event':'SYNTHETIC_FIXTURE_INITIALIZED'}
    else:
        db=load(args.fixture_path);out=execute(args.command,db)
    if args.command!='inspect':store(args.fixture_path,db)
    print(json.dumps({'simulation_only':True,'command':args.command,**out},sort_keys=True))


if __name__=='__main__':
    main()
