#!/usr/bin/env python3
"""Fetch unmodified Taiwan physician stage-II national exam PDFs from MoEx.

Run from repository root:
    pip install pypdf
    python tools/import_physician_stage2.py --extract --workers 4
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "archive/national-exam/physician-stage2-2022-2026"
MANIFEST = DATA / "manifest.json"
GOOD = {"downloaded_pdf", "existing_pdf"}

def get_pdf(url, destination):
    if destination.exists():
        buf = destination.read_bytes()
        if buf.startswith(b"%PDF-") and len(buf) > 700:
            return {"status": "existing_pdf", "bytes": len(buf), "sha256": hashlib.sha256(buf).hexdigest()}
    last_error = ""
    for attempt in range(3):
        try:
            request = Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; ClinicalOSMedicalEducation/1.0)",
                "Accept": "application/pdf,*/*"})
            with urlopen(request, timeout=40) as response:
                buf = response.read()
            if not buf.startswith(b"%PDF-") or len(buf) < 700:
                raise ValueError("response is not a valid PDF header or is too short")
            destination.parent.mkdir(parents=True, exist_ok=True)
            temp = destination.with_name(destination.name + ".part")
            temp.write_bytes(buf)
            temp.replace(destination)
            return {"status": "downloaded_pdf", "bytes": len(buf),
                    "sha256": hashlib.sha256(buf).hexdigest()}
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < 2:
                time.sleep(attempt + 1)
    return {"status": "failed", "error": last_error}

def extract_text(pdf, destination):
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf), strict=False)
        pages = [{"page": n + 1, "text": page.extract_text() or ""}
                 for n, page in enumerate(reader.pages)]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps({
            "pdf": str(pdf.relative_to(DATA)),
            "status": "machine_extracted_not_figure_complete_not_question_verified",
            "warning": "Figures/ECGs/tables may be missing; check official PDF.",
            "pages": pages}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {"status": "extracted_unverified", "pages": len(pages),
                "chars": sum(len(x["text"]) for x in pages)}
    except Exception as exc:
        return {"status": "extraction_failed", "error": f"{type(exc).__name__}: {exc}"}

def process(job, want_text):
    item, kind, url = job
    dest = DATA / "raw" / item["id"] / f"{kind}.pdf"
    result = {"paper_id": item["id"], "kind": kind, "official_url": url,
              "path": str(dest.relative_to(DATA))}
    result.update(get_pdf(url, dest))
    if want_text and result["status"] in GOOD:
        output = DATA / "extracted" / item["id"] / f"{kind}.json"
        result["extraction"] = extract_text(dest, output)
    return result

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--extract", action="store_true", help="Make page-text derivatives with pypdf")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--strict", action="store_true", help="Exit nonzero when a PDF fails")
    p.add_argument("--questions-only", action="store_true")
    args = p.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    jobs = []
    for item in manifest["items"]:
        jobs.append((item, "question", item["question_pdf"]))
        if not args.questions_only:
            jobs.append((item, "standard_answer", item["standard_answer_pdf"]))
            if item["correction_pdf"]:
                jobs.append((item, "corrected_answer", item["correction_pdf"]))
    results = []
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 8))) as pool:
        futures = [pool.submit(process, job, args.extract) for job in jobs]
        for f in as_completed(futures):
            r = f.result()
            results.append(r)
            print(f'{r["paper_id"]} {r["kind"]}: {r["status"]}', flush=True)
    results.sort(key=lambda r: (r["paper_id"], r["kind"]))
    ok = sum(r["status"] in GOOD for r in results)
    failed = len(results) - ok
    questions = sum(r["kind"] == "question" and r["status"] in GOOD for r in results)
    summary = {"dataset": manifest["dataset"],
               "generated_utc": datetime.now(timezone.utc).isoformat(),
               "requested_pdf_files": len(jobs), "verified_pdf_files": ok,
               "failed_pdf_files": failed, "verified_question_pdfs": questions,
               "complete": failed == 0, "files": results}
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "ingestion-report.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA / "INGESTION_STATUS.md").write_text(
        f'# 醫師二階考題來源檔下載狀態\n\n'
        f'紀錄時間（UTC）：{summary["generated_utc"]}\n\n'
        f'- 成功保存且驗證 PDF 標頭：**{ok}/{len(jobs)}**\n'
        f'- 原始考卷：**{questions}/40**\n'
        f'- 失敗檔案：**{failed}**\n'
        f'- 完整來源檔典藏：**{"完成" if failed == 0 else "尚未完成"}**\n\n'
        '詳見 ingestion-report.json（每份 PDF 的來源連結、SHA-256、下載錯誤）。\n\n'
        '注意：逐題結構化、影像確認、更正給分語意解析與主題標籤仍需另行驗證。\n',
        encoding="utf-8")
    print(f"Saved valid PDFs: {ok}/{len(jobs)}; failed={failed}; questions={questions}/40")
    return 2 if args.strict and failed else 0

if __name__ == "__main__":
    sys.exit(main())
