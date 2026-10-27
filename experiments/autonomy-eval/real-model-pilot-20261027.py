"""One-shot real-article prompt A/B through GitHub Models. Public article only.

Exploratory 1 article × 2 conditions × 1 fresh API call each. No medical release,
model superiority, owner-time or protected holdout claims. Hard cap two requests.
"""
import hashlib
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
PATH = "content/xiaoma-reading/integrated/2026-10-21-dcm.md"
SOURCE_COMMIT = "c5898a22636b265da3bc99aec387c346e7f6c386"
GIT_BLOB = "f16eced854467e5c8e43a063ef5d34b93f0d1d15"
MODEL = "openai/gpt-4.1"
ENDPOINT = "https://models.github.ai/inference/chat/completions"
ARMS = (
    ("lite", "逐段核查讀者已知的前提、病例時間序列、機轉與證據界線，以及下一段或圖表是否真的改變臨床判斷。只提出可引用原句的必要修正，避免重複或額外杜撰。"),
    ("baseline", "依專業醫學教材審稿標準，找出真正需要更正的內部矛盾、敘事缺口或不恰當讀者語境。保留正確內容，不為修而修。"),
)
COMMON = ("以下是已公開的完整醫學教學文章。請審閱文內一致性、必要的概念和推理前提、"
          "段落間的臨床因果敘事與讀者語境。不能檢查的外部原圖、最新醫學來源請標記 pending，"
          "不要假稱完成。沒有真正缺陷時請回答無須修改。"
          "請輸出最多三項候選缺陷，每項包括原句、問題、最小修正與不確定性。")


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GitHub short-lived Models token unavailable")
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        raise RuntimeError("only same-owner pull_request event allowed")
    raw = (ROOT / PATH).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()
    if blob != GIT_BLOB:
        raise RuntimeError("source drift; abort before external inference")
    article = raw.decode("utf-8")
    report = {"status": "EXPLORATORY_NOT_CLINICALLY_VALIDATED", "study": "dcm-1x2x1-20261027",
              "source_commit": SOURCE_COMMIT, "source_git_blob": blob,
              "source_sha256": hashlib.sha256(raw).hexdigest(),
              "model_requested": MODEL, "max_model_calls": 2, "results": []}
    for arm, rules in ARMS:
        payload = {"model": MODEL, "messages": [
            {"role": "system", "content": "You are a careful medical-education editorial auditor. Do not infer external verification or publication authority."},
            {"role": "user", "content": COMMON + "\n" + rules + "\n完整原始文章：\n" + article}
        ], "temperature": 0.2, "max_tokens": 1250}
        request = Request(ENDPOINT, method="POST",
                          data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                          headers={"Authorization": "Bearer " + token,
                                   "Content-Type": "application/json",
                                   "Accept": "application/vnd.github+json",
                                   "X-GitHub-Api-Version": "2022-11-28",
                                   "User-Agent": "clinical-os-readonly-ab-eval"})
        print("BEGIN ARM", arm, "model", MODEL, "article_bytes", len(raw), flush=True)
        try:
            with urlopen(request, timeout=110) as response:
                data = json.load(response)
        except HTTPError as exc:
            print("PROVIDER_ERROR", exc.code, exc.read(500).decode("utf-8", errors="replace"), flush=True)
            raise SystemExit(2)
        except (URLError, TimeoutError) as exc:
            print("PROVIDER_UNAVAILABLE", type(exc).__name__, flush=True)
            raise SystemExit(2)
        answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not isinstance(answer, str) or not answer.strip():
            print("INVALID_MODEL_OUTPUT", arm, flush=True)
            raise SystemExit(2)
        row = {"arm": arm, "model_returned": data.get("model"),
               "finish_reason": data["choices"][0].get("finish_reason"),
               "usage": data.get("usage"), "answer": answer,
               "prompt_chars": len(payload["messages"][1]["content"])}
        report["results"].append(row)
        print("BEGIN MODEL OUTPUT", arm, flush=True)
        print(answer[:7500], flush=True)
        print("END MODEL OUTPUT", arm, flush=True)
    out = Path("real-article-model-pilot.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("COMPLETE", "2/2", "no clinical adjudication", flush=True)


if __name__ == "__main__":
    main()
