#!/usr/bin/env python3
"""Repair PDF numeric pseudo-headings detected by the explicit source QA."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import json, re, sys, unicodedata
sys.path.insert(0,str(Path(__file__).resolve().parent))
import prepare_med3_exam_bank as base

OUT=base.OUT

def restore(row):
 raw=row["raw_text"]; found=list(base.OPT.finditer(raw))
 labels=[unicodedata.normalize("NFKC",m.group(1)) for m in found]
 row["stem_text"]=raw[:found[0].start()].strip() if found else raw
 row["options"]=[{"label":labels[i],"text":raw[m.end():(found[i+1].start() if i+1<len(found) else len(raw))].strip()}
                 for i,m in enumerate(found)]
 row["possible_visual_reference"]=bool(base.IMAGE.search(raw))
 row["topic_candidates_not_verified"]=[name for name,expr in base.TAGS.items() if re.search(expr,raw,re.I)]
 ans=row["answer"]
 note=ans["official_correction_note"]
 compact=re.sub(r"\s+","",note) if note else None
 ans["scoring"]=base.rule(ans["standard"],ans["correction_grid"],compact)
 return labels

def fix_paper(path):
 data=json.loads(path.read_text(encoding="utf8"))
 original=data["questions"]; cleaned=[]; merged=[]
 for row in original:
  number=row["number"];expected=len(cleaned)+1
  if number==expected:
   cleaned.append(row)
  elif cleaned:
   # A mistaken heading inside a previous question. Put its original
   # numbered prefix and remaining text back, then re-split A/B/C/D.
   cleaned[-1]["raw_text"] += "\n"+str(number)+"."+row["raw_text"]
   merged.append({"false_number":number,"merged_into":cleaned[-1]["number"]})
  else:
   raise ValueError(f"{path.name}: first question number was not 1")
 errors=[];found_nums=[q["number"] for q in cleaned]
 if found_nums!=list(range(1,81)):
  errors.append({"type":"question_sequence","found":found_nums})
 for row in cleaned:
  labels=restore(row)
  if labels!=list("ABCD"):
   errors.append({"type":"options","number":row["number"],"found":labels})
  if row["answer"]["scoring"]["needs_review"]:
   errors.append({"type":"answer_correction_review","number":row["number"],"note":row["answer"]["official_correction_note"]})
 data["questions"]=cleaned
 data["qa_errors"]=errors
 data["repair_log"]=merged
 data["quality_level"]="machine_structured_not_visually_verified"
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 return {"paper":data["paper"],"questions":len(cleaned),
         "corrected_questions":sum(q["answer"]["correction_grid"]=="#" for q in cleaned),
         "merged_numeric_false_headings":len(merged),"qa_errors":errors}

def main():
 paths=sorted(OUT.glob("????-s?-med3.json"))
 results=[fix_paper(p) for p in paths]
 question_count=sum(p["questions"] for p in results)
 error_count=sum(len(p["qa_errors"]) for p in results)
 tags=Counter()
 figures=0
 for path in paths:
  d=json.loads(path.read_text(encoding="utf8"))
  for row in d["questions"]:
   tags.update(row["topic_candidates_not_verified"])
   figures+=bool(row["possible_visual_reference"])
 report={"as_of_utc":datetime.now(timezone.utc).isoformat(),
   "papers":len(results),"expected_questions":800,"questions":question_count,
   "merged_numeric_false_headings":sum(p["merged_numeric_false_headings"] for p in results),
   "remaining_qa_error_count":error_count,
   "possible_figure_references_not_visually_checked":figures,
   "topic_keyword_candidates_multiple_matches_possible":dict(tags),
   "validation_level":"machine structured; source PDF visual audit and clinical semantic validation outstanding",
   "per_paper":results}
 (OUT/"qa-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 lines=["# 醫學（三）十梯逐題資料品質報告","",
    f'官方試題共 10 梯，逐題資料已整理 **{question_count}/800** 題。',
    f'已將 **{report["merged_numeric_false_headings"]}** 處誤判為題號的段落重新併回原題。',
    f'目前尚有 **{error_count}** 項機器結構／更正規則警示。',
    f'**{figures}** 題有可能涉及圖片或影像的文字提示，並不代表所有含圖題已被找出。',"",
    "重要：800 題僅表示題號序列與機器辨識的選項結構已檢查，**不代表題幹、圖像與答案已逐題視覺核對或醫學審稿**。","",
    "| 年份梯次 | 題數 | 更正題數 | 修復誤切 | 殘留 QA 警示 |",
    "|---|---:|---:|---:|---:|"]
 lines += [f'| {r["paper"]} | {r["questions"]} | {r["corrected_questions"]} | {r["merged_numeric_false_headings"]} | {len(r["qa_errors"])} |' for r in results]
 lines += ["","## 初步語詞匹配（非正式考頻、不可用於排名）","",
    "可多重命中、漏掉同義詞，亦可能將題目非考點的詞當成主題；只供後續語意分類抽樣。","",
    "| 候選 | 題數（可重複） |","|---|---:|"]
 lines += [f"| {k} | {v} |" for k,v in tags.most_common()]
 lines += ["","## 後續醫學審查","",
    "逐題核對官方試卷圖片／頁碼與更正給分；由臨床問題、必要前提、機轉、處置及現行證據重建真正考點，並評估既有小麻教材涵蓋度。",""]
 (OUT/"qa-report.md").write_text("\n".join(lines),encoding="utf8")
 print("Final question count",question_count,"/800; repaired",report["merged_numeric_false_headings"],"false headings; remaining errors",error_count)
 if question_count!=800 or error_count:
  raise SystemExit(2)

if __name__=="__main__": main()
