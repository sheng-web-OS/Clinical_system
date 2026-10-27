"""Incremental EPQC evidence gate; not an automated clinical/semantic truth judge."""
import argparse
import hashlib
import json
import re
from pathlib import Path

BASELINE = "audit/editorial-semantic-baseline.json"
REVIEWS = "audit/editorial-semantic-reviews.json"
ROLES = {"orientation", "definition", "causal_bridge", "case_evidence",
         "evidence_boundary", "decision", "counterfactual", "safety",
         "navigation", "source_context"}
AXES = tuple("ABCDEFG")
CONTINUITY_DIMS = ("concept", "causal", "decision", "narrative")


def is_teaching_page(row):
    s = row["source"]
    return row.get("kind") != "historical_original" and (
        row.get("kind") == "ai_integrated" or "/lessons/" in s
        or ("/exams/" in s and not s.endswith("/index.md"))
        or s == "content/clinical-os/acs.md")


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def reading_units(markdown):
    """Paragraphs + substantial list items; source figures have a separate gate."""
    units, buffer, occurrences = [], [], {}
    in_code = False
    in_comment = False
    skip_html = None
    begin = 1

    def emit():
        nonlocal buffer
        if not buffer:
            return
        raw = " ".join(x.strip() for x in buffer)
        buffer = []
        visible = re.sub(r"<[^>]*>", " ", raw)
        visible = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", visible)
        visible = re.sub(r"[\x60*_~]", "", visible)
        visible = re.sub(r"\s+", " ", visible).strip()
        if len(re.sub(r"\s+", "", visible)) < 26:
            return
        key = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:18]
        occurrences[key] = occurrences.get(key, 0) + 1
        units.append({"id": key + "-" + str(occurrences[key]),
                      "line": begin, "excerpt": visible[:145]})

    for line_no, line in enumerate(markdown.splitlines(), 1):
        s = line.strip()
        if re.match(r"^\s*(\x60{3}|~{3})", line):
            emit()
            in_code = not in_code
            continue
        if in_code:
            continue
        if in_comment:
            if "-->" in s:
                in_comment = False
            continue
        if s.startswith("<!--"):
            emit()
            in_comment = "-->" not in s
            continue
        if skip_html:
            if re.search(r"</\s*" + skip_html + r"\s*>", s, re.I):
                skip_html = None
            continue
        tag = re.match(r"^<(figure|svg|table|script|style|pre)\b", s, re.I)
        if tag:
            emit()
            skip_html = (None if re.search(r"</\s*" + tag.group(1) + r"\s*>", s, re.I)
                         else tag.group(1).lower())
            continue
        if (not s or re.match(r"^#{1,6}\s", s)
                or re.match(r"^(-{3,}|\*{3,}|_{3,})$", s)
                or s.startswith("|")
                or re.match(r"^\s*!\[[^]]*\]\(", s)
                or re.match(r"^</?[\w-]+(?:\s[^>]*)?>\s*$", s)):
            emit()
            continue
        if re.match(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", line):
            emit()
            begin = line_no
            buffer = [re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", "", line)]
            emit()
            continue
        if not buffer:
            begin = line_no
        buffer.append(s)
    emit()
    return units


def review_metadata_errors(review, source):
    errors = []
    scores = review.get("epqc_scores")
    if not isinstance(scores, dict) or set(scores) != set(AXES):
        return [source + ": EPQC requires A-G scores"]
    if any(type(scores[k]) is not int or scores[k] not in range(5) for k in AXES):
        return [source + ": EPQC axis scores must be integers 0-4"]
    if min(scores.values()) < 3 or sum(scores.values()) / 7 < 3.3:
        errors.append(source + ": EPQC below 3/axis or 3.3 mean")
    for field in ("core_reader_question", "new_understanding", "strongest_counterargument"):
        if not isinstance(review.get(field), str) or len(review[field].strip()) < 32:
            errors.append(source + ": missing specific " + field)
    if review.get("reviewer_context") not in ("independent_ai_pass", "human_editor"):
        errors.append(source + ": separate editorial context must be disclosed")
    if not isinstance(review.get("reviewer_reference"), str) or len(review["reviewer_reference"]) < 8:
        errors.append(source + ": missing reviewer run/reference")
    stops = review.get("hard_stops")
    required = {"unsafe_claim", "fabricated_evidence", "broken_causal_bridge",
                "internal_metadata", "unresolved_source_conflict",
                "broken_narrative_continuity"}
    if not isinstance(stops, dict) or set(stops) != required or any(type(stops[k]) is not bool for k in required):
        errors.append(source + ": missing/invalid EPQC hard-stop decisions")
    elif any(stops.values()):
        errors.append(source + ": unresolved EPQC hard stop")
    continuity = review.get("continuity_gate")
    if not isinstance(continuity, dict):
        errors.append(source + ": CONTINUITY_HOLD missing independent continuity verdict")
    else:
        if continuity.get("verdict") != "pass":
            errors.append(source + ": CONTINUITY_HOLD continuity not approved")
        if continuity.get("all_transitions_checked") is not True:
            errors.append(source + ": CONTINUITY_HOLD paragraph handoffs not fully checked")
        if continuity.get("unresolved_gaps") != []:
            errors.append(source + ": CONTINUITY_HOLD unresolved narrative gaps")
        checks = continuity.get("checks")
        if not isinstance(checks, dict) or set(checks) != set(CONTINUITY_DIMS):
            errors.append(source + ": CONTINUITY_HOLD requires four independent checks")
        else:
            for dim in CONTINUITY_DIMS:
                entry = checks[dim]
                if (not isinstance(entry, dict) or entry.get("verdict") != "pass"
                        or not isinstance(entry.get("evidence"), str)
                        or len(entry["evidence"].strip()) < 24):
                    errors.append(source + ": CONTINUITY_HOLD missing supported " + dim + " decision")
    return errors


def continuity_handoff_errors(continuity, units, source):
    """Confirm sample points at a *real* adjacent reader handoff; not a semantic grader."""
    if len(units) < 2 or not isinstance(continuity, dict):
        return []
    handoff = continuity.get("sample_handoff")
    neighbors = {(a["id"], b["id"]) for a, b in zip(units, units[1:])}
    if (not isinstance(handoff, dict)
            or (handoff.get("from_id"), handoff.get("to_id")) not in neighbors
            or any(not isinstance(handoff.get(k), str) or len(handoff[k].strip()) < 24
                   for k in ("reader_question", "bridge_justification"))):
        return [source + ": CONTINUITY_HOLD missing grounded adjacent handoff evidence"]
    return []


def validate_semantic_gate(root, pages):
    """Check review evidence and exact source fingerprints; legacy is NOT certified."""
    baseline = json.loads((root / BASELINE).read_text("utf-8"))
    registry = json.loads((root / REVIEWS).read_text("utf-8"))
    if baseline.get("schema_version") != 1 or registry.get("schema_version") != 1:
        return ["Invalid semantic review registry version"]
    frozen, reviews = baseline.get("legacy_blobs"), registry.get("reviews")
    if not isinstance(frozen, dict) or not isinstance(reviews, dict):
        return ["Invalid semantic review registry shape"]
    teaching = [p for p in pages if is_teaching_page(p)]
    sources = {p["source"] for p in teaching}
    errors = []
    if (set(frozen) | set(reviews)) - sources:
        errors.append("Semantic registry contains sources outside publication catalog")
    for page in teaching:
        path = page["source"]
        data = (root / path).read_bytes()
        blob = git_blob_sha(data)
        if blob == frozen.get(path):
            continue
        review = reviews.get(path)
        if not isinstance(review, dict):
            errors.append(path + ": SEMANTIC_HOLD new/changed article lacks paragraph review")
            continue
        if review.get("content_blob") != blob:
            errors.append(path + ": SEMANTIC_HOLD review stale after a content change")
            continue
        errors.extend(review_metadata_errors(review, path))
        units = reading_units(data.decode("utf-8"))
        errors.extend(continuity_handoff_errors(review.get("continuity_gate"), units, path))
        if not units:
            errors.append(path + ": SEMANTIC_HOLD no assessable teaching paragraphs")
            continue
        notes = review.get("paragraphs")
        if not isinstance(notes, dict):
            errors.append(path + ": SEMANTIC_HOLD missing paragraph decisions")
            continue
        expected = {u["id"] for u in units}
        missing, extras = expected - set(notes), set(notes) - expected
        if missing:
            errors.append(path + ": SEMANTIC_HOLD " + str(len(missing)) + " uncovered paragraphs")
        if extras:
            errors.append(path + ": SEMANTIC_HOLD " + str(len(extras)) + " stale paragraph IDs")
        gains = []
        for ident in expected & set(notes):
            item = notes[ident]
            if not isinstance(item, dict):
                errors.append(path + ": invalid paragraph review " + ident)
                continue
            if item.get("role") not in ROLES or item.get("verdict") != "keep":
                errors.append(path + ": paragraph verdict/role missing " + ident)
            gain, reason = item.get("reader_gain"), item.get("nonredundancy_reason")
            if (not isinstance(gain, str) or len(gain.strip()) < 18
                    or not isinstance(reason, str) or len(reason.strip()) < 18):
                errors.append(path + ": paragraph gain / nonredundancy not explained " + ident)
            else:
                gains.append(gain.strip())
        if len(gains) != len(set(gains)):
            errors.append(path + ": duplicate paragraph rationales")
    return errors


def packet(source, content):
    """Unapproved review skeleton. A different reviewer must supply judgments."""
    data = content.encode("utf-8")
    return {
        "content_blob": git_blob_sha(data),
        "reviewer_context": "UNREVIEWED", "reviewer_reference": "",
        "core_reader_question": "", "new_understanding": "",
        "strongest_counterargument": "",
        "epqc_scores": {k: None for k in AXES},
        "hard_stops": {k: None for k in (
            "unsafe_claim", "fabricated_evidence", "broken_causal_bridge",
            "internal_metadata", "unresolved_source_conflict",
            "broken_narrative_continuity")},
        "continuity_gate": {
            "verdict": "unreviewed", "all_transitions_checked": False,
            "unresolved_gaps": [],
            "checks": {k: {"verdict": "unreviewed", "evidence": ""}
                       for k in CONTINUITY_DIMS},
            "sample_handoff": {"from_id": "", "to_id": "",
                               "reader_question": "", "bridge_justification": ""},
        },
        "paragraphs": {u["id"]: {
            "role": "", "reader_gain": "", "nonredundancy_reason": "",
            "verdict": "review", "excerpt_for_editor": u["excerpt"],
            "line_for_editor": u["line"]
        } for u in reading_units(content)},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, help="content/.../article.md")
    args = parser.parse_args()
    p = Path(args.packet)
    if not p.is_file() or "content" not in p.parts or p.suffix != ".md":
        parser.error("Expected a repository content/ Markdown file")
    print(json.dumps(packet(str(p), p.read_text("utf-8")), ensure_ascii=False, indent=2))
