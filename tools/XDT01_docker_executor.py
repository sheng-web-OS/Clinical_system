#!/usr/bin/env python3
"""Execute XDT-01 3xA/B/C on a private Docker host, one isolated case per run.

Docker is required for preflight AND live mode. No model call is made without
--live, a post-72h date check, explicit budget/operator flags and OPENAI_API_KEY.
This controller is NOT the independent examiner or independent reviewer.
"""
import argparse
import hashlib
import io
import json
import os
import pathlib
import pwd
import shutil
import subprocess
import sys
import zipfile
import uuid
import re
import secrets
from datetime import datetime, timezone
from collections import Counter

FROZEN_HEAD="03f29b980ba326ac0509299b9c94292d6a1a5d5a"
GATE=datetime(2026,11,1,6,20,15,tzinfo=timezone.utc)
MAX_CALLS=12
IMAGE="xdt01-python-3.13-git:isolated-v1"
ORIGINAL_ARCHIVE_SHA256="365685e3885754a50d5c81627ba376316c024a757207902f93eabe339eae4f69"
# This deployment's operator-owned state is independent of cwd, output workspace,
# and copies of this controller. No CLI/environment override is provided.
try:
    STATE_ROOT=pathlib.Path(pwd.getpwuid(os.getuid()).pw_dir)/("Documents/Codex/2026-10-31/"
                            "codex-xdt-01-docker-clinical-os/work/"
                            "private-xdt01-handoff-20261031/live-experiment-state")
except KeyError:
    # An unmapped container UID may import offline tests, but never invents a
    # new live ledger from HOME/cwd/workspace when no OS account is available.
    STATE_ROOT=None
RUNTIME_TOOLS=pathlib.Path(__file__).resolve().parent
RUNTIME_REPO=RUNTIME_TOOLS.parent

class Hold(Exception): pass

def require(cond,msg):
    if not cond: raise Hold(msg)

def staged_data(stage,expected_manifest_sha256,repo):
    """Read only a pinned cases-only manifest and its three complete task files."""
    from prepare_xdt01_rich_pilot import (read_pinned, exact_keys, validate_cases,
                                        unique_pairs, MAX_PACKET_BYTES, Hold as StageHold)
    stage=pathlib.Path(stage)
    require(stage.is_dir() and not stage.is_symlink(),"CASES_STAGE_INVALID")
    require(not stage.resolve().is_relative_to(repo) and
            not stage.resolve().is_relative_to(RUNTIME_REPO),"CASES_STAGE_INSIDE_PUBLIC_REPO")
    try:
        manifest=read_pinned(stage/"stage_manifest.json",expected_manifest_sha256,repo)
        exact_keys(manifest,{"status","schema_version","phase","source_class_claim",
                            "candidate_commit","skill_sha256","source_sha256",
                            "case_count","cases","model_calls"},"CASES_STAGE")
        require(manifest["status"]=="OFFLINE_CASES_ONLY_REVIEW_HOLD" and
                type(manifest["schema_version"]) is int and manifest["schema_version"]==1 and
                manifest["phase"]=="pilot" and manifest["source_class_claim"]=="synthetic" and
                manifest["candidate_commit"]==FROZEN_HEAD and
                type(manifest["case_count"]) is int and manifest["case_count"]==3 and
                type(manifest["model_calls"]) is int and manifest["model_calls"]==0,
                "CASES_STAGE_METADATA_INVALID")
        hex64=lambda value:isinstance(value,str) and re.fullmatch(r"[0-9a-f]{64}",value)
        source=manifest["source_sha256"]
        require(type(source) is dict and set(source)=={"cases"} and hex64(source["cases"]),
                "CASES_SOURCE_PIN_REQUIRED")
        require(hex64(manifest["skill_sha256"]),"SKILL_PIN_INVALID")
        skill=repo/"experiments/cross-domain-transfer/decision-skill-v0.md"
        require(skill.is_file() and not skill.is_symlink() and
                hashlib.sha256(skill.read_bytes()).hexdigest()==manifest["skill_sha256"],
                "FROZEN_SKILL_SHA_MISMATCH")
        rows=manifest["cases"]
        require(type(rows) is list and len(rows)==3,"THREE_CASES_REQUIRED")
        seen=set();digests=set();objects=[];raw_tasks=[]
        for row in rows:
            exact_keys(row,{"slot","sha256","bytes","evidence_count"},"CASES_STAGE_ENTRY")
            slot=row["slot"]
            require(type(slot) is str and slot in {"H01","H02","H03"} and slot not in seen,
                    "CASES_SLOT_INVALID")
            require(hex64(row["sha256"]) and row["sha256"] not in digests and
                    type(row["bytes"]) is int and 0<row["bytes"]<=MAX_PACKET_BYTES and
                    type(row["evidence_count"]) is int and 1<=row["evidence_count"]<=30,
                    "CASES_STAGE_ENTRY_INVALID")
            packet=stage/(slot+".txt")
            require(packet.is_file() and not packet.is_symlink(),"CASE_FILE_INVALID")
            with packet.open("rb") as stream:raw=stream.read(MAX_PACKET_BYTES+1)
            require(len(raw)==row["bytes"] and hashlib.sha256(raw).hexdigest()==row["sha256"],
                    "CASE_FILE_SHA_OR_SIZE_MISMATCH")
            obj=json.loads(raw.decode("utf-8"),object_pairs_hook=unique_pairs)
            exact_keys(obj,{"package_id","instructions","case"},"WORKER_OBJECT")
            require(type(obj["case"]) is dict and type(obj["case"].get("evidence")) is list and
                    len(obj["case"]["evidence"])==row["evidence_count"],"EVIDENCE_COUNT_MISMATCH")
            seen.add(slot);digests.add(row["sha256"]);objects.append(obj);raw_tasks.append(raw)
        require(all(obj["package_id"]==objects[0]["package_id"] and
                    obj["instructions"]==objects[0]["instructions"] for obj in objects),
                "GLOBAL_INSTRUCTIONS_OR_PACKAGE_MISMATCH")
        reconstructed={"schema_version":1,"phase":"pilot","source_class":"synthetic",
                       "package_id":objects[0]["package_id"],
                       "instructions":objects[0]["instructions"],
                       "cases":[obj["case"] for obj in objects]}
        complete=validate_cases(reconstructed)
        require(all(complete[obj["case"]["id"]]==raw for obj,raw in zip(objects,raw_tasks)),
                "CASE_PACKET_NOT_CANONICAL_OR_COMPLETE")
    except StageHold as error:
        raise Hold(str(error)) from None
    except (OSError,ValueError,TypeError,KeyError,UnicodeError):
        raise Hold("CASES_STAGE_FORMAT_INVALID") from None
    jobs=[]
    for raw in raw_tasks:
        for arm in ("A","B","C"):
            job={"job_id":"xdt-"+uuid.uuid4().hex,"arm":arm,
                 "task_sha256":hashlib.sha256(raw).hexdigest(),"candidate_commit":FROZEN_HEAD,
                 "skill_sha256":manifest["skill_sha256"] if arm=="C" else None}
            buffer=io.BytesIO()
            with zipfile.ZipFile(buffer,"w",compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("task.txt",raw)
                archive.writestr("job.json",json.dumps(job,sort_keys=True))
            jobs.append((job,buffer.getvalue()))
    secrets.SystemRandom().shuffle(jobs)
    return jobs,{"kind":"cases_only","stage_manifest_sha256":expected_manifest_sha256,
                 "cases_sha256":source["cases"]}

def data(archive):
    archive=pathlib.Path(archive)
    require(archive.is_file() and not archive.is_symlink(),"MASTER_ZIP_INVALID")
    with zipfile.ZipFile(archive) as z:
        filenames=z.namelist()
        workers=[f for f in filenames if f.startswith("workers/") and f.endswith(".zip")]
        require(len(workers)==9 and len(filenames)==12,"MASTER_SHAPE_INVALID")
        wrapper=z.read("run_one_worker.py")
        manifest=json.loads(z.read("examiner_job_manifest.json"))
        require(manifest.get("candidate_commit")==FROZEN_HEAD,"COMMIT_PIN_INVALID")
        info=[]
        for name in workers:
            raw=z.read(name)
            with zipfile.ZipFile(io.BytesIO(raw)) as w:
                require(set(w.namelist())=={"task.txt","job.json"} and len(w.namelist())==2,
                        "ONE_CASE_PER_JOB_REQUIRED")
                j=json.loads(w.read("job.json"))
                task=w.read("task.txt")
                require(hashlib.sha256(task).hexdigest()==j["task_sha256"],
                        "TASK_SHA_MISMATCH")
                require(j["candidate_commit"]==FROZEN_HEAD,"FROZEN_HEAD_INVALID")
                require(j["arm"] in ("A","B","C"),"ARM_INVALID")
                require(j["skill_sha256"] is None if j["arm"]!="C" else
                        isinstance(j["skill_sha256"],str),"SKILL_SCOPE_INVALID")
            info.append((j,raw))
        require(Counter(j["arm"] for j,_ in info)==
                Counter({"A":3,"B":3,"C":3}),"ARM_COUNT_WRONG")
        idx={x["job_id"]:x["order"] for x in manifest["jobs"]}
        require(len(idx)==9 and set(idx)=={j["job_id"] for j,_ in info},
                "MANIFEST_JOB_MISMATCH")
        info.sort(key=lambda row:idx[row[0]["job_id"]])
        return info,wrapper

def repo_verified(repo):
    repo=pathlib.Path(repo).resolve(strict=True)
    require(repo.is_dir(),"REPO_MISSING")
    try:
        v=subprocess.run(["git","-C",str(repo),"rev-parse","HEAD"],
                         capture_output=True,text=True,timeout=15)
        require(v.returncode==0 and v.stdout.strip()==FROZEN_HEAD,"EXACT_HEAD_MISMATCH")
        dirty=subprocess.run(["git","-C",str(repo),"status","--porcelain",
                              "--untracked-files=no"],capture_output=True,text=True,timeout=15)
        require(dirty.returncode==0 and not dirty.stdout.strip(),"TRACKED_CODE_DIRTY")
    except (OSError,subprocess.TimeoutExpired):
        raise Hold("GIT_UNAVAILABLE") from None
    return repo

def docker_cmd(job,packet,wrapper,repo,output,live,*,name=None,attempt_dir=None):
    mounts=[
        f"type=bind,src={packet},dst=/job/packet.zip,readonly",
        f"type=bind,src={wrapper},dst=/worker/run_one_worker.py,readonly",
        f"type=bind,src={repo},dst=/repo,readonly",
        f"type=bind,src={RUNTIME_TOOLS},dst=/runtime,readonly",
        f"type=bind,src={output},dst=/results",
    ]
    uid=os.geteuid() or 65532
    gid=os.getegid() if os.geteuid() else 65532
    cmd=["docker","run","--rm","--read-only","--cap-drop=ALL",
         "--security-opt=no-new-privileges","--pids-limit=64",
         "--memory=512m",f"--user={uid}:{gid}",
         "--network=bridge" if live else "--network=none",
         "--tmpfs=/tmp:rw,nosuid,nodev,size=32m","--workdir=/worker"]
    if name:cmd.extend(["--name",name])
    if live:
        require(attempt_dir is not None,"ATTEMPT_GRANT_REQUIRED")
        mounts.append(f"type=bind,src={attempt_dir},dst=/attempts")
    for bind in mounts:cmd.extend(["--mount",bind])
    if live:
        # Docker process receives the key via an environment-variable name,
        # never via argv, case files, GitHub, source text or result receipts.
        cmd.extend(["-e","OPENAI_API_KEY",
                    "-e","XDT01_PRIVATE_APPROVAL=YES"])
    cmd.extend([IMAGE,"python","/worker/run_one_worker.py",
                "--packet","/job/packet.zip","--repo","/repo",
                "--result-parent","/results"])
    if live:cmd.append("--live")
    return cmd

def write_private_once(path,value):
    fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as stream:
        json.dump(value,stream,sort_keys=True)
        stream.write("\n");stream.flush();os.fsync(stream.fileno())
    descriptor=os.open(path.parent,os.O_RDONLY)
    try:os.fsync(descriptor)
    finally:os.close(descriptor)

def experiment_identity(jobs):
    rows=sorted((job["task_sha256"],job["arm"],job["skill_sha256"] or "",
                 job["candidate_commit"]) for job,_ in jobs)
    groups={}
    for task,arm,_,_ in rows:groups.setdefault(task,[]).append(arm)
    require(len(groups)==3 and all(sorted(arms)==["A","B","C"]
                                  for arms in groups.values()),
            "MATCHED_TASK_ARMS_REQUIRED")
    return hashlib.sha256(json.dumps(rows,separators=(",",":")).encode()).hexdigest()

def claim_experiment(jobs,archive,state_root,*,source_pin=None):
    if source_pin is None:
        require(hashlib.sha256(pathlib.Path(archive).read_bytes()).hexdigest()==
                ORIGINAL_ARCHIVE_SHA256,"ORIGINAL_ARCHIVE_PIN_MISMATCH")
        source_pin={"kind":"original_archive","archive_sha256":ORIGINAL_ARCHIVE_SHA256}
    identity=experiment_identity(jobs)
    state_root=pathlib.Path(state_root)
    require(not state_root.is_symlink(),"STATE_ROOT_INVALID")
    state_root.mkdir(mode=0o700,parents=True,exist_ok=True)
    state_root.chmod(0o700)
    experiment=state_root/identity
    experiment.mkdir(mode=0o700,exist_ok=True)
    try:
        write_private_once(experiment/"claim.json",{
            "experiment_id":identity,"source_pin":source_pin,
            "status":"CLAIMED_NO_RETRY","max_calls":MAX_CALLS,
            "claimed_at_utc":datetime.now(timezone.utc).isoformat(),
            "reserved_calls":sum(2 if job["arm"]=="C" else 1 for job,_ in jobs),
        })
    except FileExistsError:
        raise Hold("EXPERIMENT_ALREADY_CLAIMED_NO_RETRY") from None
    grants={}
    for sequence,(job,_) in enumerate(jobs,1):
        grant_dir=experiment/("grant-%02d"%sequence)
        grant_dir.mkdir(mode=0o700)
        grant_file=grant_dir/"grant.json"
        write_private_once(grant_file,{
            "experiment_id":identity,"arm":job["arm"],
            "task_sha256":job["task_sha256"],
            "candidate_commit":job["candidate_commit"],
            "max_calls":2 if job["arm"]=="C" else 1,
        })
        if os.geteuid()==0:
            os.chown(grant_dir,65532,65532);os.chown(grant_file,65532,65532)
        grants[job["job_id"]]=grant_dir
    return experiment,grants

def stop_exact_container(name):
    """Return only sanitized state, with daemon loss distinct from absence."""
    for action in (["docker","stop","--time","5",name],
                   ["docker","rm","--force",name]):
        try:subprocess.run(action,capture_output=True,text=True,timeout=15)
        except (OSError,subprocess.TimeoutExpired):pass
    try:
        inspected=subprocess.run(["docker","inspect","--format",
                                  "{{.State.Running}}",name],
                                 capture_output=True,text=True,timeout=15)
        if inspected.returncode==0:
            return {"confirmed":inspected.stdout.strip()=="false",
                    "state":"STOPPED" if inspected.stdout.strip()=="false"
                    else "RUNNING_OR_UNKNOWN"}
        # A connection failure is NOT evidence that the named container is gone.
        diagnostic=inspected.stderr.lower()
        absent=("no such object" in diagnostic or
                "no such container" in diagnostic)
        daemon=subprocess.run(["docker","info","--format","{{.ServerVersion}}"],
                              capture_output=True,text=True,timeout=15)
        if absent and daemon.returncode==0:
            return {"confirmed":True,"state":"ABSENT"}
    except (OSError,subprocess.TimeoutExpired):pass
    return {"confirmed":False,"state":"UNCERTAIN_STOP"}

def launch(archive,repo,workspace,live,*,state_root=None,cases_stage=None,
           stage_manifest_sha256=None):
    require(shutil.which("docker") is not None,"DOCKER_RUNTIME_UNAVAILABLE")
    repo=repo_verified(repo)
    require((archive is None)!=(cases_stage is None),"EXACTLY_ONE_CASE_SOURCE_REQUIRED")
    require(cases_stage is not None or stage_manifest_sha256 is None,
            "STAGE_PIN_WITHOUT_STAGE")
    # cases-only is an engineering handoff, not proof of rubric custody/live consent.
    require(not (live and cases_stage is not None),"CASES_ONLY_OFFLINE_ONLY")
    if live:
        require(datetime.now(timezone.utc)>=GATE,"ORIGINAL_72H_STILL_OPEN")
        require(os.getenv("XDT01_PRIVATE_APPROVAL")=="YES","OWNER_LIVE_APPROVAL_REQUIRED")
        require(os.getenv("XDT01_BUDGET_EXTERNALLY_VERIFIED")=="YES",
                "PROJECT_HARD_LIMIT_NOT_VERIFIED")
        require(bool(os.getenv("OPENAI_API_KEY")),"PROVIDER_API_KEY_NOT_AVAILABLE")
    source_pin=None
    if cases_stage is not None:
        jobs,source_pin=staged_data(cases_stage,stage_manifest_sha256,repo)
    else:
        jobs,_original_wrapper=data(archive)
    wrapper=(pathlib.Path(__file__).parent/"run_one_worker.py").read_bytes()
    require((RUNTIME_TOOLS/"run_xdt01_skill_selection.py").is_file(),
            "PATCHED_RUNTIME_MISSING")
    requested=pathlib.Path(workspace).absolute()
    require(all(not parent.is_symlink() for parent in requested.parents),
            "WORKSPACE_SYMLINK_ANCESTOR_FORBIDDEN")
    root=requested.resolve(strict=False)
    require(not root.exists() and not root.is_symlink(),"NEW_PRIVATE_WORKSPACE_REQUIRED")
    require(not root.is_relative_to(repo),"WORKSPACE_CANNOT_BE_GITHUB_REPO")
    require(not root.is_relative_to(RUNTIME_REPO),"WORKSPACE_CANNOT_BE_RUNTIME_REPO")
    experiment=None;grants={}
    if live:
        require(state_root is not None or STATE_ROOT is not None,"OS_ACCOUNT_HOME_UNAVAILABLE")
        operator_state=pathlib.Path(state_root) if state_root is not None else STATE_ROOT
        require(not operator_state.resolve().is_relative_to(root.resolve()),
                "STATE_CANNOT_BE_ATTEMPT_WORKSPACE")
        experiment,grants=claim_experiment(jobs,archive,operator_state,source_pin=source_pin)
    root.mkdir(mode=0o700)
    root.chmod(0o700)
    code=root/"run_one_worker.py"
    code.write_bytes(wrapper);code.chmod(0o644)
    logs=root/"controller-ledger.jsonl"
    requests_reserved=0
    with logs.open("x",encoding="utf-8") as stream:
        os.chmod(logs,0o600)
        for i,(job,raw) in enumerate(jobs):
            limit=2 if job["arm"]=="C" else 1
            require(requests_reserved+limit<=MAX_CALLS,"TWELVE_CALL_CEILING")
            requests_reserved+=limit
            sub=root/("task-"+str(i+1).zfill(2))
            sub.mkdir(mode=0o700)
            packet=sub/"packet.zip"
            packet.write_bytes(raw);packet.chmod(0o644)
            result=sub/"results";result.mkdir(mode=0o700)
            # Match the nonroot operator UID so 0700/0600 receipts stay readable.
            # A root operator instead delegates this one bind to UID 65532.
            if os.geteuid()==0:os.chown(result,65532,65532)
            name="xdt01-"+uuid.uuid4().hex
            cmd=docker_cmd(job,packet,code,repo,result,live,name=name,
                           attempt_dir=grants.get(job["job_id"]))
            entry={"sequence":i+1,"arm":job["arm"],"state":"RESERVED_NO_RETRY",
                   "max_provider_calls":limit,"container_name":name}
            stream.write(json.dumps(entry)+"\n");stream.flush();os.fsync(stream.fileno())
            if experiment:
                write_private_once(experiment/("container-%02d.json"%(i+1)),entry)
            try:
                run=subprocess.run(cmd,capture_output=True,text=True,timeout=300,
                                   env=os.environ.copy() if live else
                                   {k:v for k,v in os.environ.items() if k not in
                                    {"OPENAI_API_KEY","XDT01_PRIVATE_APPROVAL"}})
            except BaseException:
                try:cleanup=stop_exact_container(name)
                except BaseException:
                    cleanup={"confirmed":False,"state":"UNCERTAIN_STOP"}
                failure={"sequence":i+1,"state":
                         "INTERRUPTED_STOP_CONFIRMED" if cleanup["confirmed"]
                         else "UNCERTAIN_STOP", "cleanup":cleanup,
                         "billing_status":"UNKNOWN_BILLED" if live else "NO_MODEL_CALLS"}
                stream.write(json.dumps(failure)+"\n");stream.flush();os.fsync(stream.fileno())
                if experiment:write_private_once(experiment/("interrupted-%02d.json"%(i+1)),failure)
                raise Hold("WORKER_INTERRUPTED_NO_RETRY" if cleanup["confirmed"]
                           else "UNCERTAIN_STOP_UNKNOWN_BILLED") from None
            # Never print stdout/stderr; they may contain runtime information.
            receipt=result/("result-"+job["job_id"])
            record=receipt/("first_pass.json" if live else "preflight.json")
            if run.returncode!=0 or not record.is_file():
                cleanup=stop_exact_container(name)
                failed={"sequence":i+1,"state":"FAILED_STOP_NO_RETRY"
                        if cleanup["confirmed"] else "UNCERTAIN_STOP",
                        "cleanup":cleanup,
                        "billing_status":"UNKNOWN_BILLED" if live else "NO_MODEL_CALLS"}
                stream.write(json.dumps(failed)+"\n")
                stream.flush();os.fsync(stream.fileno())
                if experiment:write_private_once(experiment/("failed-%02d.json"%(i+1)),failed)
                raise Hold("ISOLATED_WORKER_FAILED_STOP" if cleanup["confirmed"]
                           else "UNCERTAIN_STOP_UNKNOWN_BILLED")
            obj=json.loads(record.read_text())
            require(obj.get("task_sha256")==job["task_sha256"],"WRONG_TASK_RECEIPT")
            if live:
                require(obj.get("status")=="FIRST_PASS_UNSCORED","NO_FIRST_PASS_STOP")
                require(obj.get("provider_calls")==limit,"PROVIDER_CALL_COUNT_MISMATCH")
            else:
                require(obj.get("status")=="PREFLIGHT_ONLY_NO_MODEL_OUTCOME",
                        "OFFLINE_MODE_NOT_CONFIRMED")
            stream.write(json.dumps({"sequence":i+1,
                        "state":"FIRST_PASS_UNSCORED" if live else "PREFLIGHT_ONLY",
                        "provider_calls":limit if live else 0})+"\n")
            stream.flush();os.fsync(stream.fileno())
            if experiment:
                write_private_once(experiment/("completed-%02d.json"%(i+1)),{
                    "sequence":i+1,"state":"FIRST_PASS_UNSCORED",
                    "provider_calls":limit,"billing_status":"UNKNOWN_BILLED"})
    return {"status":"FIRST_PASSES_UNSCORED" if live else "DOCKER_PREFLIGHT_PASS",
            "jobs":9,"max_model_calls":12 if live else 0,
            "independent_judge":"NOT_VERIFIED"}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    source=p.add_mutually_exclusive_group(required=True)
    source.add_argument("--examiner-zip",type=pathlib.Path)
    source.add_argument("--cases-stage",type=pathlib.Path)
    p.add_argument("--stage-manifest-sha256")
    p.add_argument("--repo",type=pathlib.Path,required=True)
    p.add_argument("--workspace",type=pathlib.Path,required=True)
    p.add_argument("--live",action="store_true")
    args=p.parse_args()
    print(json.dumps(launch(args.examiner_zip,args.repo,args.workspace,args.live,
                           cases_stage=args.cases_stage,
                           stage_manifest_sha256=args.stage_manifest_sha256)))
if __name__=="__main__":
    try:main()
    except (Hold,OSError,ValueError,zipfile.BadZipFile,subprocess.TimeoutExpired) as e:
        print("HOLD_"+(str(e) if isinstance(e,Hold) else type(e).__name__),
              file=sys.stderr)
        sys.exit(2)
