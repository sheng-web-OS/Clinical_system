"""Read-only, fail-closed instruments for Clinical_system agent quality research.

No model execution, medical approval, deployment, owner-time inference or publication.
All verdicts describe the supplied evidence only. Private experiments only.
"""
import argparse
import hashlib
import json
import os
import re
from urllib.request import Request, urlopen
from pathlib import Path

SHA256 = re.compile(r"^[a-f0-9]{64}$")
GIT_SHA = re.compile(r"^[a-f0-9]{40}$")
INCIDENT = re.compile(r"^\|\s*(F-\d{3})(?:[^|]*)\|")
EVAL = re.compile(r"^##\s*(EVAL-\d+)\b")
STATUSES = {"PROVISIONAL", "VALIDATED", "INVALIDATED"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()



def validate_model_completion_response(raw, content_type):
    """Treat HTTP success as transport evidence, never as model-completion proof."""
    require(isinstance(raw, bytes) and raw and len(raw) <= 2000000,
            "model provider response missing/oversized")
    require(isinstance(content_type, str) and "application/json" in content_type.lower()
            and raw.lstrip().startswith(b"{"), "no verifiable model JSON despite HTTP success")
    try:
        obj = json.loads(raw)
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("malformed model response JSON") from exc
    require(isinstance(obj, dict) and isinstance(obj.get("model"), str)
            and obj["model"].strip(), "missing provider model identity")
    choices = obj.get("choices")
    require(isinstance(choices, list) and len(choices) == 1
            and isinstance(choices[0], dict), "missing or unexpected response choices")
    message = choices[0].get("message")
    require(isinstance(message, dict) and isinstance(message.get("content"), str)
            and message["content"].strip(), "missing actual model output")
    return {"model_returned": obj["model"], "answer": message["content"],
            "finish_reason": choices[0].get("finish_reason"),
            "usage": obj.get("usage"), "evidence_level": "MODEL_OUTPUT_SHAPE_ONLY",
            "clinical_validated": False, "release_approval": False}



def audit_generated_finding_quotes(article, answer):
    """Evidence locator only. Quote presence is NOT a soundness/quality verdict."""
    require(isinstance(article, str) and bool(article.strip())
            and isinstance(answer, str), "article and response text required")
    quotes = re.findall(r"原文\s*[：:]\s*「([^」]+)」", answer)
    compact = lambda s: "".join(s.split())
    source_no_whitespace = compact(article)
    audited = []
    for quote in quotes:
        present_verbatim = quote in article
        present_spaced = compact(quote) in source_no_whitespace
        audited.append({
            "quote": quote,
            "exact_contiguous_match": present_verbatim,
            "whitespace_insensitive_match": present_spaced,
            "qualification_needs_context_review": any(
                signal in quote for signal in ("不是所有", "並不是", "不代表", "不一定", "至少", "未必")
            ),
            "status": "QUOTE_LOCATED_NOT_INDEPENDENTLY_VALIDATED" if present_spaced
                      else "SOURCE_SPAN_NOT_LOCATED",
            "auto_edit_allowed": False,
        })
    return {
        "evidence_level": "MECHANICAL_SOURCE_ANCHOR_ONLY",
        "original_findings": len(quotes),
        "exact_quotes": sum(q["exact_contiguous_match"] for q in audited),
        "whitespace_matched_quotes": sum(q["whitespace_insensitive_match"] for q in audited),
        "needs_qualification_review": sum(q["qualification_needs_context_review"] for q in audited),
        "findings": audited,
        "medical_quality_verified": False,
        "public_edit_allowed": False,
        "limitations": "Source quote presence and negation flags cannot establish actionable defects; check adjacent paragraphs, source figures and medical validity independently.",
    }



def triage_revision_claims(article, answer):
    """High-specificity context-risk triage, NOT an automatic semantic verdict.

    Each candidate keeps an exact original-source neighborhood for independent
    review. Lexical cues are deliberately only reason-to-review flags; neither
    flagged nor unflagged content earns automatic approval or rejection.
    """
    require(isinstance(article, str) and article.strip()
            and isinstance(answer, str) and answer.strip(),
            "complete article and generated review required")
    sections = re.split(r"(?m)(?=^\s*\d{1,2}\.\s*原文\s*[：:])", answer)
    sections = [part for part in sections if re.search(r"^\s*\d{1,2}\.\s*原文", part)]
    raw_compact = [(char, index) for index, char in enumerate(article)
                   if not char.isspace()]
    compact_source = "".join(char for char, _ in raw_compact)
    triggers = (
        ("universal_scope", "不是所有", r"所有.{0,22}(?:都|必然|會|遵循)"),
        ("single_test_overreach", "並不是", r"單獨|單憑"),
        ("negated_implication", "不代表", r"沒有關係|不會影響|直接關係"),
        ("minimum_as_maximum", "至少", r"只需要|僅需|只有"),
    )
    results = []
    for section in sections:
        original = re.search(r"原文\s*[：:]\s*「([^」]+)」", section)
        critique = re.search(r"問題機制\s*[：:]\s*([^\n]+)", section)
        proposed = re.search(r"最小改法\s*[：:]\s*([^\n]+)", section)
        quote = original.group(1) if original else ""
        mechanism = critique.group(1) if critique else ""
        minimal_edit = proposed.group(1) if proposed else ""
        key = "".join(quote.split())
        offset = compact_source.find(key) if key else -1
        evidence_found = offset >= 0
        if evidence_found:
            left = raw_compact[offset][1]
            right = raw_compact[offset + len(key) - 1][1] + 1
            context = article[max(0, left - 700):min(len(article), right + 700)]
        else:
            left = None
            right = None
            context = None
        reversal = [name for name, source_literal, pattern in triggers
                    if source_literal in quote and re.search(pattern, mechanism)]
        result = {
            "number": len(results) + 1,
            "quoted_source_text": quote,
            "source_start_char": left,
            "source_end_char": right,
            "source_span_found_ignoring_whitespace": evidence_found,
            "exact_contiguous_quote": quote in article if quote else False,
            "critique": mechanism,
            "proposed_edit": minimal_edit,
            "source_context_excerpt": context,
            "risk_signals": reversal,
            "context_rebuttal_required": bool(reversal) or not evidence_found,
            "decision": "HOLD_FOR_CONTEXT_REVIEW" if reversal or not evidence_found
                        else "REVIEW_REQUIRED_NOT_CLEARED",
            "not_a_medical_or_teaching_truth_verdict": True,
        }
        results.append(result)
    return {
        "evidence_level": "LEXICAL_CONTEXT_CUE_ONLY",
        "finding_count": len(results),
        "located_count": sum(r["source_span_found_ignoring_whitespace"] for r in results),
        "scope_reversal_review_flags": sum(bool(r["risk_signals"]) for r in results),
        "context_rebuttal_required_count":
            sum(r["context_rebuttal_required"] for r in results),
        "unparseable_or_absent_findings": len(results) == 0,
        "findings": results,
        "automatic_accepts": 0,
        "automatic_rejections": 0,
        "public_edit_allowed": False,
        "medical_quality_verified": False,
        "limitations": "Flags are a post-hoc lexical triage signal, not a validated false-positive classifier; no unflagged finding is approved. Full source and clinical independent review remain necessary.",
    }



def anchored_file(root, relative, digest):
    require(isinstance(relative, str) and relative.startswith("content/")
            and not relative.startswith("content//"), "only public teaching-source paths permitted")
    require(isinstance(digest, str) and SHA256.fullmatch(digest), "missing source digest")
    root = Path(root).resolve()
    p = root / relative
    require(p.resolve().is_relative_to(root / "content") and p.is_file()
            and not p.is_symlink(), "missing, symlinked or out-of-scope source")
    raw = p.read_bytes()
    require(sha256(raw) == digest, "article/source changed since preregistration")
    return raw.decode("utf-8")


def prepare_packets(root, spec, out):
    """Freeze full-article input packets; deliberately does NOT run any AI trial."""
    require(type(spec.get("schema_version")) is int and spec["schema_version"] == 1 and spec.get("exposure") == "development",
            "only explicitly visible development cohorts supported")
    require(isinstance(spec.get("source_commit"), str)
            and GIT_SHA.fullmatch(spec["source_commit"]), "exact source commit required")
    arms = spec.get("arms")
    require(isinstance(arms, dict) and set(arms) == {"baseline", "lite"}
            and all(isinstance(x, str) and x.strip() for x in arms.values()),
            "explicit matched baseline/lite instructions required")
    require(arms["baseline"] != arms["lite"], "comparison arms identical")
    require(isinstance(spec.get("common_instruction"), str)
            and bool(spec["common_instruction"].strip()), "missing common instruction")
    trials = spec.get("trials")
    require(isinstance(trials, list) and len(trials) >= 3
            and all(isinstance(t, str) and t.strip() == t and t for t in trials)
            and len(set(trials)) == len(trials), "at least 3 distinct trials")
    cases = spec.get("cases")
    require(isinstance(cases, list) and len(cases) >= 2, "need real original articles and controls")
    packets, seen = [], set()
    for item in cases:
        require(isinstance(item, dict) and set(item) == {"id", "path", "sha256"},
                "case must include only id/path/sha256, never defect hints")
        ident = item["id"]
        require(isinstance(ident, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,64}", ident)
                and ident not in seen, "invalid/duplicate article ID")
        seen.add(ident)
        article = anchored_file(root, item["path"], item["sha256"])
        for trial in trials:
            for arm in ("baseline", "lite"):
                packet = {"schema_version": 1, "evidence_level": "DEVELOPMENT_ONLY",
                          "article_id": ident, "trial": trial, "arm": arm,
                          "source_commit": spec["source_commit"], "source_sha256": item["sha256"],
                          "instructions": spec["common_instruction"] + "\n" + arms[arm],
                          "original_full_markdown": article,
                          "output_contract": "Locate original actionable findings with verbatim evidence; preserve supported passages. Do not claim original figure or medical verification unless actually performed."}
                packets.append((f"{ident}-{trial}-{arm}.json", packet))
    out = Path(out)
    real_out, real_root = out.resolve(), Path(root).resolve()
    require(not real_out.is_relative_to(real_root)
            or real_out.is_relative_to(real_root / "experiments/autonomy-eval"),
            "packet output must stay outside repo or under private experiments/autonomy-eval")
    require(not out.exists(), "output already exists: immutable packet set, do not overwrite")
    out.mkdir(parents=True)
    fingerprints = {}
    for name, packet in packets:
        raw = (json.dumps(packet, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
        (out / name).write_bytes(raw)
        fingerprints[name] = sha256(raw)
    manifest = {"schema_version": 1, "evidence_level": "DEVELOPMENT_ONLY",
                "model_executions": 0, "clinical_validated": False,
                "source_commit": spec["source_commit"], "article_count": len(cases),
                "planned_reviews": len(packets), "task_sha256": fingerprints,
                "limitations": "Packet creation does not prove fresh contexts, fair budget, blinded grading or successful repair."}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def fetch_canonical_issue_133(token):
    """Read existing single-source failure ledger using only an authenticated GET."""
    require(isinstance(token, str) and bool(token.strip()),
            "GitHub read-only token needed to fetch private issue #133")
    request = Request("https://api.github.com/repos/sheng-web-OS/Clinical_system/issues/133",
                      headers={"Accept": "application/vnd.github+json",
                               "X-GitHub-Api-Version": "2022-11-28",
                               "Authorization": "Bearer " + token,
                               "User-Agent": "clinical-os-selective-experience"})
    with urlopen(request, timeout=15) as response:
        data = json.load(response)
    require(isinstance(data.get("body"), str), "issue #133 missing canonical body")
    return data["body"]


def select_experiences(issue_markdown, terms, statuses=None, limit=3):
    """Extract snippets from canonical issue #133; no parallel memory database."""
    require(isinstance(terms, list) and terms and
            all(isinstance(t, str) and len(t.strip()) >= 2 for t in terms),
            "nonempty task-specific terms required")
    statuses = statuses or {}
    lines = issue_markdown.splitlines()
    entries = []
    for i, line in enumerate(lines):
        m = INCIDENT.match(line) or EVAL.match(line)
        if m is None:
            continue
        ident = m.group(1)
        if INCIDENT.match(line):
            excerpt = line[:1800]
        else:
            last = next((j for j in range(i + 1, len(lines))
                         if re.match(r"^##\s", lines[j])), len(lines))
            excerpt = "\n".join(lines[i:min(last, i + 18)])[:1800]
        entry = statuses.get(ident, {"status": "PROVISIONAL"})
        require(isinstance(entry, dict) and entry.get("status") in STATUSES,
                "invalid incident memory state")
        if entry["status"] == "INVALIDATED":
            continue
        if entry["status"] == "VALIDATED":
            require(all(isinstance(entry.get(k), str) and entry[k].strip()
                        for k in ("verified_case", "review_evidence", "negative_control")),
                    "VALIDATED requires external evidence and a normal control")
        hits = [term for term in terms if term.casefold() in excerpt.casefold()]
        if hits:
            entries.append({"incident_id": ident, "status": entry["status"],
                            "matched_terms": hits, "source": "GitHub issue #133",
                            "evidence_excerpt": excerpt, "score": len(hits)})
    entries.sort(key=lambda x: (-x["score"], x["incident_id"]))
    # The real #133 pilot showed that a generic match like "PR" can displace
    # the true incident when a meaningful term has no lexical hit. A narrow
    # preview is permitted only with one complete exact-term candidate.
    # Otherwise demand the canonical issue as context; do not silently
    # certify retrieval completeness or fabricate semantic synonym matching.
    complete = [e for e in entries if len(e["matched_terms"]) == len(terms)]
    requires_full_issue_review = len(complete) != 1
    preview = entries[:limit] if requires_full_issue_review else complete
    return {"evidence_level": "ISSUE_TEXT_RETRIEVAL_ONLY",
            "selected": preview,
            "requires_full_issue_review": requires_full_issue_review,
            "memory_adequacy_verified": False,
            "limitations": "Exact-term overlap is not semantic recall or reviewer authentication; ambiguous/no matches require the full canonical issue, and even a unique match cannot certify medical completeness."}


def trace_failure(events):
    """Locate earliest independently declared failure; no invented root-cause diagnosis."""
    require(isinstance(events, list) and events, "missing execution trace")
    seen, failures = set(), []
    for event in events:
        require(isinstance(event, dict) and type(event.get("step")) is int
                and event["step"] >= 0 and event["step"] not in seen,
                "trace steps must be unique nonnegative integers")
        seen.add(event["step"])
        require(event.get("verdict") in ("CONFIRMED_FAILURE", "PASS", "UNKNOWN"),
                "unknown trace verdict")
        if event["verdict"] == "CONFIRMED_FAILURE":
            require(isinstance(event.get("evidence_ref"), str)
                    and event["evidence_ref"].strip()
                    and isinstance(event.get("reviewer_context"), str)
                    and event["reviewer_context"].strip()
                    and event.get("reviewer_context") != event.get("worker_context"),
                    "failure attribution needs evidence and separate reviewer")
            failures.append(event)
    if not failures:
        return {"root_cause": "NOT_ESTABLISHED", "first_failure_step": None,
                "evidence_level": "TRACE_ONLY_NOT_MEDICAL_REVIEW"}
    first = min(failures, key=lambda x: x["step"])
    return {"root_cause": "NOT_ESTABLISHED", "first_failure_step": first["step"],
            "evidence_ref": first["evidence_ref"],
            "failure_kind": first.get("kind", "UNSPECIFIED"),
            "evidence_level": "INDEPENDENTLY_DECLARED_TRACE_NOT_CAUSALLY_VERIFIED"}


def judge_order_calibration(grades):
    """Pairwise left/right swap check with opaque candidates. Does not grade medicine."""
    require(isinstance(grades, list) and grades, "no grades")
    grouped = {}
    for g in grades:
        require(isinstance(g, dict) and isinstance(g.get("item_id"), str)
                and g["item_id"].strip(), "missing item identity")
        order = g.get("candidate_order")
        require(isinstance(order, list) and len(order) == 2
                and all(isinstance(x, str) and x for x in order)
                and len(set(order)) == 2, "two different opaque candidates required")
        require(g.get("choice") in ("left", "right", "tie"), "invalid judgement")
        require(isinstance(g.get("reviewer_context"), str)
                and bool(g["reviewer_context"].strip()), "missing reviewer trace")
        grouped.setdefault(g["item_id"], []).append(g)
    results = []
    for ident, records in sorted(grouped.items()):
        require(len(records) <= 2, "no repeated cherry-picked grade")
        first = records[0]
        if len(records) != 2:
            results.append({"item_id": ident, "state": "INCOMPLETE", "winner": None})
            continue
        second = records[1]
        require(second["candidate_order"] == first["candidate_order"][::-1],
                "must exchange left/right on same candidate pair")
        require(first["reviewer_context"] != second["reviewer_context"],
                "reversed order requires a fresh reviewer context")
        def winner(g):
            return None if g["choice"] == "tie" else g["candidate_order"][0 if g["choice"] == "left" else 1]
        w1, w2 = winner(first), winner(second)
        stable = w1 == w2
        results.append({"item_id": ident, "state": "STABLE" if stable else "ORDER_SENSITIVE",
                        "winner": w1 if stable else None})
    return {"evidence_level": "ORDER_BIAS_SCREEN_ONLY",
            "medical_validation": False, "publication_approval": False,
            "pairs": results, "pairs_stable": sum(x["state"] == "STABLE" for x in results),
            "pairs_total": len(results),
            "status": "NEEDS_REVIEW" if any(x["state"] != "STABLE" for x in results) else "ORDER_STABLE_NOT_CLINICALLY_VALIDATED"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    cmd = parser.add_subparsers(dest="cmd", required=True)
    p = cmd.add_parser("prepare")
    p.add_argument("--root", required=True)
    p.add_argument("--spec", required=True)
    p.add_argument("--out", required=True)
    m = cmd.add_parser("memory")
    source = m.add_mutually_exclusive_group(required=True)
    source.add_argument("--issue-md")
    source.add_argument("--issue-133", action="store_true")
    m.add_argument("--terms", nargs="+", required=True)
    m.add_argument("--statuses")
    t = cmd.add_parser("trace")
    t.add_argument("--events", required=True)
    j = cmd.add_parser("judge")
    j.add_argument("--grades", required=True)
    q = cmd.add_parser("audit")
    q.add_argument("--article", required=True)
    q.add_argument("--response", required=True)
    c = cmd.add_parser("context")
    c.add_argument("--article", required=True)
    c.add_argument("--response", required=True)
    a = parser.parse_args()
    try:
        if a.cmd == "prepare":
            result = prepare_packets(a.root, json.loads(Path(a.spec).read_text()), a.out)
        elif a.cmd == "memory":
            issue_text = (fetch_canonical_issue_133(os.environ.get("GITHUB_TOKEN", ""))
                          if a.issue_133 else Path(a.issue_md).read_text())
            result = select_experiences(issue_text, a.terms,
                    json.loads(Path(a.statuses).read_text()) if a.statuses else None)
        elif a.cmd == "trace":
            result = trace_failure(json.loads(Path(a.events).read_text()))
        elif a.cmd == "audit":
            result = audit_generated_finding_quotes(Path(a.article).read_text(encoding="utf-8"),
                                                    Path(a.response).read_text(encoding="utf-8"))
        elif a.cmd == "context":
            result = triage_revision_claims(Path(a.article).read_text(encoding="utf-8"),
                                           Path(a.response).read_text(encoding="utf-8"))
        else:
            result = judge_order_calibration(json.loads(Path(a.grades).read_text()))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, TypeError, UnicodeError) as exc:
        parser.exit(2, "INVALID_EVIDENCE: " + str(exc) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
