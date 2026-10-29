import argparse,hashlib,importlib.util,json
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument("--data-dir",type=Path,required=True)
parser.add_argument("--repo-root",type=Path,required=True)
args=parser.parse_args()
root=args.data_dir.resolve()
repo=args.repo_root.resolve()
gm=json.loads((root/"gold-and-mapping.json").read_text())
key=json.loads((root/"blinding-key.json").read_text())
grade_rows=json.loads((root/"blinded-grades.json").read_text())["grades"]
assert len(grade_rows)==len({r["record_id"] for r in grade_rows})==len(key)==144
assert set(key)=={r["record_id"] for r in grade_rows}
grades={r["record_id"]:r for r in grade_rows}
record_id_by_key={(v["arm"],v["trial"],v["case_id"]):rid for rid,v in key.items()}
ledger=json.loads((root/"execution-ledger.json").read_text())
spec=importlib.util.spec_from_file_location("eval_summary",repo/"tools/summarize_autonomy_eval.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
suite={"schema_version":1,"suite_id":"ab-development-20261027-24cases","exposure":"development","note":"20 prior visible seeds plus 4 synthetic transfer cases; proposed correction semantics, not applied article repairs or protected holdouts.","cases":list(gm["gold"].values())}
suite_bytes=(json.dumps(suite,ensure_ascii=False,indent=2)+"\n").encode()
(root/"evaluation-suite.json").write_bytes(suite_bytes)
digest=hashlib.sha256(suite_bytes).hexdigest()
summaries={};details={}
for arm in ["baseline","rules"]:
 run={"schema_version":1,"suite_id":suite["suite_id"],"suite_sha256":digest,"candidate_sha":"141958a3eca91995d6fa9fd7048a85e2035c37f4","run_id":f"ab-{arm}-20261027","arm":arm,"model":"same inherited model configuration; exact version not returned","trial_ids":["1","2","3"],"records":[],"task_cueing":"Several seed case descriptions explicitly name the failure; autonomous-discovery fields are development task classification only."}
 total_input=total_output=0;bycase={}
 for trial in range(1,4):
  name=f"{arm}-{trial}"
  task=json.loads((root/(name+"-task.json")).read_text())
  total_input+=len((root/(name+"-task.json")).read_text())
  response_path=root/(name+"-responses.json")
  assert hashlib.sha256(response_path.read_bytes()).hexdigest()==ledger["runs"][name]["response_sha256"],name
  data=json.loads(response_path.read_text())
  for response in data["responses"]:
   cid=gm["mapping"][str(trial)][response["id"]];gold=gm["gold"][cid]
   rid=record_id_by_key[(arm,trial,cid)];g=grades[rid]
   assert g["defect_flag_correct"]==(response["flagged"]==gold["defect_present"])
   assert not g.get("reference_dispute")
   final=(g["defect_flag_correct"] and g["correction_pass"] and not g["hard_failure"] and (g["location_correct"] is True if gold["defect_present"] else True))
   rec={"case_id":cid,"trial_id":str(trial),"flagged":response["flagged"],"located":bool(g["location_correct"]) if gold["defect_present"] else False,"repair_pass":g["correction_pass"] and bool(g["location_correct"]) if gold["defect_present"] else None,"first_pass":bool(final),"final_pass":bool(final),"hinted":False,"worker_context":ledger["runs"][name]["worker_context"],"reviewer_context":"/root/blinded_adjudication","trace_ref":name+"-responses.json#"+response["id"],"hard_failures":int(g["hard_failure"]),"attempts":1,"owner_minutes":None,"owner_interruptions":None}
   run["records"].append(rec)
   total_output+=sum(len(response[f]) for f in ["location","reason","correction"])
   bycase.setdefault(cid,[]).append(final)
 (root/(arm+"-actual-run.json")).write_text(json.dumps(run,ensure_ascii=False,indent=2)+"\n")
 summary=mod.summarize(suite,run,digest)
 summary["correction_measurement"]="independent AI assessment of proposed correction; no actual article edit performed"
 summary["human_learning"]="NOT_MEASURED"
 summary["task_cueing"]=run["task_cueing"]
 (root/(arm+"-summary.json")).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
 summaries[arm]=summary
 details[arm]={"unique_cases":len(bycase),"case_responses":len(run["records"]),"defective_case_responses":36,"normal_case_responses":36,"flag_correct":sum(grades[record_id_by_key[(arm,t,c)]]["defect_flag_correct"] for t in range(1,4) for c in gm["gold"]),"correction_proposals_acceptable":sum(grades[record_id_by_key[(arm,t,c)]]["correction_pass"] for t in range(1,4) for c in gm["gold"]),"all_three_acceptable_cases":sum(all(v) for v in bycase.values()),"task_json_characters":total_input,"response_field_characters":total_output}
result={"experiment_id":"ab-development-20261027","preregistration_commit":"8e35b59e2bb26d00a7191ccb6f715f73977126f3","candidate_sha":"141958a3eca91995d6fa9fd7048a85e2035c37f4","worker_contexts":6,"adjudication_contexts":1,"case_responses":144,"results":details,"inference":{"additional_discovery_gain_observed":False,"additional_correction_gain_observed":False,"equivalence_established":False,"human_time_savings_established":False,"actual_operational_autonomy_established":False,"interpretation":"Both prompt conditions saturated this small descriptive synthetic test set. No observed benefit from appending the entire SOP; cannot infer rules are unnecessary in harder real tasks."},"input_packet_character_ratio_rules_over_baseline":details["rules"]["task_json_characters"]/details["baseline"]["task_json_characters"],"response_field_character_ratio_rules_over_baseline":details["rules"]["response_field_characters"]/details["baseline"]["response_field_characters"],"cost_limit":"characters only; not API tokens, money, inference latency or owner minutes"}
result["test_set_limitation"]="Ceiling and explicit failure cueing; not an unhinted original-article review benchmark."
(root/"comparison-summary.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(result,ensure_ascii=False,indent=2))

