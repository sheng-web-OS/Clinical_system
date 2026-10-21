#!/usr/bin/env python3
"""Med(III) original-source question index; automated extraction, not medical review."""
import json, re, unicodedata
from pathlib import Path
from datetime import datetime, timezone

BASE=Path(__file__).resolve().parents[1]/"archive/national-exam/physician-stage2-2022-2026"
OUT=BASE/"structured"
HEAD=re.compile(r"(?m)^[ \t]*([1-9]|[1-7][0-9]|80)[.．、][ \t]*")
OPT=re.compile(r"(?m)^[ \t]*([ABCDＡＢＣＤ])[.．、][ \t]*")
REMARK=re.compile(r"第\s*(\d+)\s*題\s*(.*?)(?=第\s*\d+\s*題|$)",re.S)
IMAGE=re.compile(r"如圖|下圖|附圖|圖中|圖示|心電圖|(?:X光|X-ray|CT|MRI)影像",re.I)
TAGS={
 "cardiology":r"心肌梗塞|心臟衰竭|心衰竭|冠狀動脈|心律不整|心房顫動|心包填塞|心電圖|heart failure|syncope",
 "respiratory":r"缺氧|低血氧|呼吸衰竭|呼吸窘迫|肺炎|氣喘|肺栓塞|呼吸器|COPD|ARDS|hypoxia|hypoxemia",
 "renal_electrolyte":r"腎功能|腎衰竭|透析|腎絲球|低血鈉|高血鈉|低血鉀|高血鉀|酸中毒|creatinine|glomerul",
 "gastro_liver":r"肝硬化|肝炎|腹水|消化道出血|胰臟炎|黃疸|食道靜脈瘤|cirrhosis|pancreatitis|hepatitis",
 "endocrine":r"糖尿病|甲狀腺|腎上腺|低血糖|高血糖|骨鬆|痛風|diabetes|thyroid|osteoporosis|cortisol",
 "infection":r"抗生素|感染性|敗血症|結核|愛滋|菌血症|sepsis|bacteremia|tuberculosis|antibiotic|HIV",
 "neurology":r"中風|頭痛|癲癇|帕金森|巴金森|失智|偏頭痛|stroke|seizure|migraine",
 "hematology_oncology":r"貧血|白血病|淋巴瘤|腫瘤|癌症|化學治療|anemia|leukemia|lymphoma",
 "rheumatology":r"紅斑性狼瘡|類風濕|血管炎|自體免疫|vasculitis|rheumatoid arthritis|systemic lupus",
 "ethics_family":r"安寧|緩和醫療|醫學倫理|知情同意|守密|醫療法|DNR|醫病關係",
}

def pages(pid,kind):
 return json.loads((BASE/"extracted"/pid/(kind+".json")).read_text(encoding="utf8"))["pages"]

def answers(pp):
 s=unicodedata.normalize("NFKC","\n".join(x["text"] for x in pp))
 lines=[re.findall(r"[ABCD#]",m.group(1)) for line in s.splitlines()
        if (m:=re.fullmatch(r"[ \t]*答案[ \t]+([ABCD# \t]+)",line))]
 return [c for part in lines for c in part]

def notes(pp):
 s=unicodedata.normalize("NFKC","\n".join(x["text"] for x in pp))
 s=s.split("79 80")[-1]
 return {int(m.group(1)):re.sub(r"\s+"," ",m.group(2)).strip() for m in REMARK.finditer(s)}

def rule(original,mark,note):
 if original not in "ABCD":return {"type":"unavailable","accepted":[],"needs_review":True}
 if mark!="#":return {"type":"original_single","accepted":[original],"needs_review":False}
 if not note:return {"type":"correction_note_missing","accepted":[],"needs_review":True}
 if "除未作答者不給分外" in note or "其餘均給分" in note:
  return {"type":"all_attempted","accepted":[],"needs_review":False}
 if "一律給分" in note:return {"type":"all_responses","accepted":[],"needs_review":False}
 m=re.search(r"答\s*([ABCD或、,\s]+?)\s*者均給分",note)
 if m:
  accepted=[x for x in re.split("或|、|,|\\s+",m.group(1)) if x]
  if accepted and all(re.fullmatch("[ABCD]+",x) for x in accepted):
   return {"type":"explicit_accepted","accepted":accepted,"needs_review":False}
 return {"type":"correction_unparsed","accepted":[],"needs_review":True}

def build(p):
 pid=p["id"];pp=pages(pid,"question");parts=[];starts=[];offset=0
 for pg in pp:
  starts.append((offset,pg["page"]))
  t=pg["text"] or "";parts.append(t);offset+=len(t)+1
 content="\n".join(parts)
 marks=list(HEAD.finditer(content));numbers=[int(m.group(1)) for m in marks]
 std=answers(pages(pid,"standard_answer"))
 cor=answers(pages(pid,"corrected_answer")) if p["correction_pdf"] else []
 nmap=notes(pages(pid,"corrected_answer")) if p["correction_pdf"] else {}
 errors=[]
 if numbers!=list(range(1,81)):errors.append({"type":"question_sequence","found":numbers})
 if len(std)!=80:errors.append({"type":"standard_answers","count":len(std)})
 if cor and len(cor)!=80:errors.append({"type":"corrected_answers","count":len(cor)})
 qlist=[]
 for i,m in enumerate(marks):
  n=int(m.group(1));end=marks[i+1].start() if i+1<len(marks) else len(content)
  raw=content[m.end():end].strip();om=list(OPT.finditer(raw))
  letters=[unicodedata.normalize("NFKC",z.group(1)) for z in om]
  if letters!=list("ABCD"):errors.append({"type":"option_split","q":n,"found":letters})
  options=[{"label":letters[k],"text":raw[x.end():(om[k+1].start() if k+1<len(om) else len(raw))].strip()} for k,x in enumerate(om)]
  orig=std[n-1] if len(std)==80 else None
  c=cor[n-1] if len(cor)==80 else None
  grading=rule(orig,c,nmap.get(n))
  if grading["needs_review"]:errors.append({"type":"grading_review","q":n})
  page=next((pg for start,pg in reversed(starts) if m.start()>=start),1)
  qlist.append({"id":f"{pid}-q{n:02}","number":n,"official_pdf_page":page,
    "stem_text":raw[:om[0].start()].strip() if om else raw,"options":options,
    "raw_text":raw,"answer":{"standard":orig,"correction_grid":c,
       "official_correction_note":nmap.get(n),"scoring":grading},
    "possible_visual_reference":bool(IMAGE.search(raw)),
    "topic_candidates_not_verified":[key for key,rx in TAGS.items() if re.search(rx,raw,re.I)],
    "status":"machine_parsed_visual_and_medical_review_pending",
    "clinical_problem":None,"causal_mechanism":None,"decision_node":None,
    "linked_lessons":[],"source_question_pdf":p["question_pdf"],
    "source_answer_pdf":p["standard_answer_pdf"],"source_correction_pdf":p["correction_pdf"]})
 return {"paper":pid,"year":p["year"],"session":p["session"],"questions":qlist,
         "qa_errors":errors,"corrected_questions":sum(q["answer"]["correction_grid"]=="#" for q in qlist)}

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 manifest=json.loads((BASE/"manifest.json").read_text(encoding="utf8"))
 items=[p for p in manifest["items"] if p["subject_number"]==3]
 reports=[];counts={key:0 for key in TAGS}
 for p in items:
  o=build(p)
  (OUT/(p["id"]+".json")).write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
  reports.append({"paper":o["paper"],"year":o["year"],"session":o["session"],
                  "questions":len(o["questions"]),"corrections":o["corrected_questions"],
                  "qa_errors":o["qa_errors"]})
  for q in o["questions"]:
   for key in q["topic_candidates_not_verified"]:counts[key]+=1
  print(p["id"],len(o["questions"]),"QA:",len(o["qa_errors"]),flush=True)
 report={"generated_utc":datetime.now(timezone.utc).isoformat(),
         "papers":len(reports),"questions":sum(x["questions"] for x in reports),
         "expected_questions":len(items)*80,"qa_error_count":sum(len(x["qa_errors"]) for x in reports),
         "provisional_topic_keyword_hits_not_validated":counts,
         "warning":"Keyword matches are not question classifications. Every answer and visual must be confirmed against original PDF.",
         "per_paper":reports}
 (OUT/"qa-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 lines=["# 醫學（三）近五年國考逐題預處理報告","",f'共 {report["papers"]} 梯；擷取 {report["questions"]}/{report["expected_questions"]} 題；結構／給分解析警示 {report["qa_error_count"]} 項。',"",
        "**注意：僅為機器文字擷取與解析，尚未通過原 PDF 視覺審閱。關鍵字候選不是正式考頻。**","",
        "| 試卷 | 題數 | 更正題數 | QA 警示 |","|---|---:|---:|---:|"]
 lines += [f'| {x["paper"]} | {x["questions"]} | {x["corrections"]} | {len(x["qa_errors"])} |' for x in reports]
 lines += ["","## 關鍵字候選（可多重命中、非正式分類）","",
           "| 關鍵字主題 | 候選數 |","|---|---:|"]
 lines += [f"| {k} | {v} |" for k,v in sorted(counts.items(),key=lambda kv:-kv[1])]
 lines += ["","**品質門檻**：先完成題幹選項圖像核對、答案更正複核，再以臨床問題／前提／機轉／決策語意審稿，才可用於國考重要度排序。",""]
 (OUT/"qa-report.md").write_text("\n".join(lines),encoding="utf8")

if __name__=="__main__":main()
