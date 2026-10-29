#!/usr/bin/env python3
"""E06: stateless three-arm clinical evaluation. No charge without explicit opt-in.

Usage:
  python tools/e06_runner.py --prepare
  python tools/e06_runner.py --dry-run
  E06_PAID_EVAL_APPROVED=yes OPENAI_API_KEY=... python tools/e06_runner.py --execute
Sources are only PUBLIC, published case reports; nothing from private patient records.
"""
import argparse
import hashlib
import json
import os
import random
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

CASES = {"K1": "PMC11978234", "K2": "PMC11284772", "K3": "PMC12598391"}
COMMON = (
    "Read the source case report, reconstruct the timeline and 2–4 case-specific "
    "clinical discussion questions with the key physiology, competing causes, "
    "what changes the decision, at least one counterfactual, remaining uncertainty "
    "and precise source positions. Do not invent patient facts. 繁體中文回答。"
)
EVIDENCE = ("Check original observations versus interpretation, relevant guidelines, "
            "source identity and scope. A case report does not establish treatment benefit.")
CLINOS = (EVIDENCE + " Apply causal intermediates, concept disambiguation, competing "
          "hypotheses, clinically meaningful decision reversals, and EPQC narrative "
          "continuity. Remove generic filler and mark unsupported claims.")
def digest(b):
    return hashlib.sha256(b).hexdigest()
def fetch_source(pmcid):
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    req = urllib.request.Request(url, headers={"User-Agent": "ClinicalSystem-E06/1.0"})
    with urllib.request.urlopen(req, timeout=45) as r:
        data = r.read()
    root = ET.fromstring(data)
    body = root.find(".//body")
    if body is None:
        raise RuntimeError(f"{pmcid}: original full text not available")
    result = " ".join(" ".join(body.itertext()).split())
    if not 2500 <= len(result) <= 150000:
        raise RuntimeError(f"{pmcid}: abnormal source length")
    return result.encode()
def prepare(home):
    d = home/"sources"
    d.mkdir(parents=True, exist_ok=True)
    index = {}
    for case, pmcid in CASES.items():
        f = d/f"{case}.txt"
        raw = f.read_bytes() if f.exists() else fetch_source(pmcid)
        if not f.exists():
            f.write_bytes(raw)
        index[case] = {"pmcid": pmcid, "sha256": digest(raw), "bytes": len(raw)}
    (d/"manifest.json").write_text(json.dumps(index, indent=2))
    print(json.dumps(index, indent=2))
def read_sources(home):
    d=home/"sources"
    if not (d/"manifest.json").exists():
        raise RuntimeError("Missing source snapshot: first use --prepare. No API invoked.")
    index=json.loads((d/"manifest.json").read_text())
    content={}
    for case,pmcid in CASES.items():
        raw=(d/f"{case}.txt").read_bytes()
        if index[case]["sha256"] != digest(raw) or index[case]["pmcid"] != pmcid:
            raise RuntimeError(f"Snapshot mismatch for {case}")
        content[case]=raw.decode()
    return index,content
def response(model, effort, dev, question, max_tokens):
    req=urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps({"model":model,"store":False,
              "reasoning":{"effort":effort},"max_output_tokens":max_tokens,
              "input":[{"role":"developer","content":dev},
                       {"role":"user","content":question}]}).encode(),
        method="POST",headers={"Content-Type":"application/json",
            "Authorization":"Bearer "+os.environ["OPENAI_API_KEY"]})
    with urllib.request.urlopen(req,timeout=360) as r:
        return json.loads(r.read())
def main():
    ap=argparse.ArgumentParser()
    x=ap.add_mutually_exclusive_group(required=True)
    x.add_argument("--prepare",action="store_true")
    x.add_argument("--dry-run",action="store_true")
    x.add_argument("--execute",action="store_true")
    ap.add_argument("--home",type=Path,default=Path(".local_e06"))
    ap.add_argument("--model",default="gpt-6.1-sol")
    ap.add_argument("--effort",default="high",choices=("medium","high"))
    ap.add_argument("--max-output-tokens",type=int,default=4000)
    ap.add_argument("--max-calls",type=int,default=9)
    args=ap.parse_args()
    if args.prepare:
        prepare(args.home);return
    index,source=read_sources(args.home)
    seed="E06-20261028-P1"
    jobs=[(case,arm) for case in CASES for arm in "ABC"]
    random.Random(seed).shuffle(jobs)
    if args.dry_run:
        print(json.dumps({"model":args.model,"effort":args.effort,
            "jobs":[x+y for x,y in jobs],
            "source_sha256":{x:y["sha256"] for x,y in index.items()},
            "model_calls":0},indent=2));return
    if os.environ.get("E06_PAID_EVAL_APPROVED") != "yes":
        raise RuntimeError("Paid model calls are NOT authorized. No API invoked.")
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY missing. No API invoked.")
    if not 1 <= args.max_calls <= 9:
        raise ValueError("--max-calls must be 1..9")
    # Verify and load the real Clinical OS contracts, not an abbreviated proxy.
    root=Path(__file__).resolve().parent.parent
    contracts={
      "docs/clinical-os-integration-20261021.md": "7680efef607ffe5dc14d984b639e4552312c02a8",
      "docs/editorial-prose-quality-contract.md": "be2fb5ff3e503e9a818ffd6db3606a5997fa4573",
      "docs/editorial-semantic-release-gate.md": "683797914e918078d2b81938f1d25956808aa6fd",
    }
    contract_bundle=[]
    for filename,expected_blob in contracts.items():
        b=(root/filename).read_bytes()
        blob=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\x00"+b).hexdigest()
        if blob!=expected_blob:
            raise RuntimeError(f"Contract drift: {filename}. No model calls made.")
        contract_bundle.append(f"# {filename}\n"+b.decode())
    clinos_contracts="\n\n".join(contract_bundle)
    folder=args.home/"outputs"
    folder.mkdir(parents=True,exist_ok=True)
    mapfile=args.home/"PRIVATE_unblind_map.json"
    mapping=json.loads(mapfile.read_text()) if mapfile.exists() else {}
    count=0
    for case,arm in jobs:
        opaque=digest(f"{seed}|{case}|{arm}".encode())[:14]
        mapping[opaque]={"case":case,"arm":arm}
        output=folder/f"{opaque}.json"
        if output.exists():
            continue
        if count >= args.max_calls:
            break
        dev=({"A":"Write a high-quality clinical CBD as you normally would.",
              "B":EVIDENCE,"C":CLINOS+"\n\n"+clinos_contracts}[arm])
        question=f"{case} original full text {index[case]['pmcid']}:\n"+source[case]+"\n\n"+COMMON
        started=time.time()
        raw=response(args.model,args.effort,dev,question,args.max_output_tokens)
        text="\n".join(c.get("text","") for item in raw.get("output",[])
             for c in item.get("content",[]) if c.get("type")=="output_text")
        record={"blind_id":opaque,"case":case,"source_sha256":index[case]["sha256"],
            "response_id":raw.get("id"),"model":raw.get("model"),
            "effort":args.effort,"status":raw.get("status"),"usage":raw.get("usage"),
            "elapsed_seconds":round(time.time()-started,2),"text":text}
        if not text or record["status"]!="completed":
            record["invalid_reason"]="Incomplete/empty response; cannot score."
        output.write_text(json.dumps(record,ensure_ascii=False,indent=2))
        count+=1
        print(f"{opaque}: {record['status']}",flush=True)
    mapfile.write_text(json.dumps(mapping,indent=2))
    print(f"Calls completed this run: {count}. INDEPENDENT REVIEW NOT RUN; NO VERDICT.")
if __name__=="__main__":
    try:
        main()
    except Exception as err:
        print(f"E06 safe stop: {type(err).__name__}: {err}",file=sys.stderr)
        sys.exit(2)
