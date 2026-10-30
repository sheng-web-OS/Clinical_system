#!/usr/bin/env python3
"""Fail-closed, stdlib-only metadata gate. NEVER executes a received package."""
import argparse
import datetime as dt
import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath

HEX = re.compile(r"^[0-9a-f]{64}$")
ID = re.compile(r"^[a-z0-9][a-z0-9._-]{2,79}$")
SUSPICIOUS = re.compile(r"(^|/)(\.env(\.|$)|id_rsa|id_ed25519|credentials|secrets?\.(json|ya?ml)|.*\.(pem|key|p12|pfx))$", re.I)
MAX_FILES = 500
MAX_TOTAL = 50 * 1024 * 1024
MAX_RATIO = 200


def result(decision, *reasons, **extra):
    return {"decision": decision, "reasons": list(reasons), **extra}


def preflight_zip(path):
    """Inspect ZIP metadata, not contents; safe result is NOT a malware/privacy clearance."""
    path = Path(path)
    try:
        with path.open("rb") as stream:
            raw_digest = hashlib.file_digest(stream, "sha256").hexdigest()
        with zipfile.ZipFile(path) as z:
            entries = z.infolist()
            if not entries or len(entries) > MAX_FILES:
                return result("QUARANTINE", "file_count_out_of_range")
            total = 0
            names = set()
            for info in entries:
                name = info.filename
                normalized = PurePosixPath(name)
                if (not name or "\\" in name or name.startswith("/")
                        or any(x in ("", ".", "..") for x in name.rstrip("/").split("/"))
                        or ":" in name or "\x00" in name):
                    return result("QUARANTINE", "unsafe_archive_path")
                key = str(normalized).casefold()
                if key in names:
                    return result("QUARANTINE", "duplicate_archive_path")
                names.add(key)
                mode = info.external_attr >> 16
                if stat.S_IFMT(mode) == stat.S_IFLNK:
                    return result("QUARANTINE", "symlink")
                if info.flag_bits & 1:
                    return result("QUARANTINE", "encrypted_entry")
                if SUSPICIOUS.search(name):
                    return result("QUARANTINE", "suspected_secret_filename")
                total += info.file_size
                if total > MAX_TOTAL or (info.file_size > 1024 * 1024
                    and info.file_size / max(1, info.compress_size) > MAX_RATIO):
                    return result("QUARANTINE", "archive_size_or_ratio")
            return result("METADATA_PREFLIGHT_ONLY", "no_execution_no_content_scan",
                          package_sha256=raw_digest, file_count=len(entries), uncompressed_bytes=total)
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError):
        return result("QUARANTINE", "unreadable_zip")


def decision(manifest, receipt=None, today=None):
    """Adoption is an advisory *shadow* status; no software is installed or deployed."""
    today = today or dt.date.today()
    if not isinstance(manifest, dict):
        return result("HOLD_INVALID", "manifest_not_object")
    required = ("candidate_id", "artifact_sha256", "source_url", "source_commit",
                "license_status", "privacy_status", "risk_tier", "reversible")
    if any(k not in manifest for k in required):
        return result("HOLD_INVALID", "missing_manifest_field")
    if (not isinstance(manifest["candidate_id"], str) or not ID.fullmatch(manifest["candidate_id"])
        or not isinstance(manifest["artifact_sha256"], str) or not HEX.fullmatch(manifest["artifact_sha256"])
        or not isinstance(manifest["source_commit"], str) or not re.fullmatch(r"[0-9a-f]{40,64}", manifest["source_commit"])
        or not isinstance(manifest["source_url"], str) or not manifest["source_url"].startswith("https://")
        or type(manifest["reversible"]) is not bool
        or manifest["risk_tier"] not in ("low", "medium", "high")):
        return result("HOLD_INVALID", "invalid_manifest_field")
    if manifest["license_status"] != "VERIFIED" or manifest["privacy_status"] != "PUBLIC_CLEARED":
        return result("QUARANTINE", "rights_or_privacy_not_cleared")
    if manifest["risk_tier"] != "low" or not manifest["reversible"]:
        return result("HOLD_RISK", "not_low_risk_reversible")
    if receipt is None:
        return result("PAUSE_SHADOW" if manifest.get("current_state") == "SHADOW_ADOPTED"
                      else "READY_FOR_ISOLATED_EVALUATION", "independent_receipt_missing")
    if not isinstance(receipt, dict):
        return result("HOLD_INVALID", "receipt_not_object")
    for key in ("candidate_id", "artifact_sha256", "prereg_sha256", "review_sha256",
                "evaluator_id", "reviewer_id", "security_review", "rights_review",
                "expires_on", "minimum_cases", "minimum_domains", "minimum_periods",
                "minimum_mean_gain", "maximum_cost_ratio", "cases"):
        if key not in receipt:
            return result("HOLD_EVIDENCE", "missing_evaluation_field")
    if (receipt["candidate_id"] != manifest["candidate_id"]
        or receipt["artifact_sha256"] != manifest["artifact_sha256"]):
        return result("QUARANTINE", "artifact_identity_mismatch")
    if (not isinstance(receipt["prereg_sha256"], str) or not HEX.fullmatch(receipt["prereg_sha256"])
        or not isinstance(receipt["review_sha256"], str) or not HEX.fullmatch(receipt["review_sha256"])):
        return result("HOLD_EVIDENCE", "missing_content_bound_evidence")
    if (not receipt["evaluator_id"] or not receipt["reviewer_id"]
        or receipt["evaluator_id"] == receipt["reviewer_id"]):
        return result("HOLD_EVIDENCE", "reviewer_not_distinct")
    if receipt["security_review"] != "PASS" or receipt["rights_review"] != "PASS":
        return result("PAUSE_SHADOW" if manifest.get("current_state") == "SHADOW_ADOPTED"
                      else "QUARANTINE", "review_gate_failed_or_pending")
    try:
        expiry = dt.date.fromisoformat(receipt["expires_on"])
        min_cases = receipt["minimum_cases"]
        min_domains = receipt["minimum_domains"]
        min_periods = receipt["minimum_periods"]
        gain_floor = receipt["minimum_mean_gain"]
        cost_ceiling = receipt["maximum_cost_ratio"]
        if (any(type(x) is not int or x < 2 for x in (min_cases, min_domains, min_periods))
            or any(type(x) not in (float, int) for x in (gain_floor, cost_ceiling))
            or not 0 < gain_floor <= 1 or not 1 <= cost_ceiling <= 10):
            return result("HOLD_EVIDENCE", "invalid_preregistered_thresholds")
    except (ValueError, TypeError):
        return result("HOLD_EVIDENCE", "invalid_preregistered_thresholds")
    adopted = manifest.get("current_state") == "SHADOW_ADOPTED"
    if expiry < today:
        return result("PAUSE_SHADOW" if adopted else "HOLD_EXPIRED", "evaluation_expired")
    cases = receipt["cases"]
    if not isinstance(cases, list) or len(cases) < min_cases:
        return result("HOLD_EVIDENCE", "insufficient_cases")
    ids, domains, periods = set(), set(), set()
    deltas, costs_base, costs_candidate = [], [], []
    for item in cases:
        if not isinstance(item, dict):
            return result("HOLD_EVIDENCE", "case_not_object")
        fields = ("id", "domain", "period", "split", "baseline_score", "candidate_score",
                  "baseline_cost", "candidate_cost", "severe_regression")
        if any(k not in item for k in fields):
            return result("HOLD_EVIDENCE", "missing_case_field")
        if (not isinstance(item["id"], str) or not item["id"] or item["id"] in ids
            or not isinstance(item["domain"], str) or not item["domain"]
            or not isinstance(item["period"], str) or not item["period"]
            or item["split"] != "unseen_holdout"
            or type(item["severe_regression"]) is not bool):
            return result("HOLD_EVIDENCE", "invalid_case_identity_or_holdout")
        ids.add(item["id"]); domains.add(item["domain"]); periods.add(item["period"])
        nums = [item[x] for x in ("baseline_score", "candidate_score", "baseline_cost", "candidate_cost")]
        if any(type(n) not in (float, int) for n in nums):
            return result("HOLD_EVIDENCE", "invalid_numeric_score")
        b, c, bc, cc = nums
        if not (0 <= b <= 1 and 0 <= c <= 1 and bc > 0 and cc >= 0):
            return result("HOLD_EVIDENCE", "invalid_numeric_range")
        if item["severe_regression"]:
            return result("PAUSE_SHADOW" if adopted else "REJECT", "severe_regression_hard_stop")
        deltas.append(c - b); costs_base.append(bc); costs_candidate.append(cc)
    if len(domains) < min_domains or len(periods) < min_periods:
        return result("HOLD_EVIDENCE", "insufficient_cross_domain_or_period_coverage")
    mean_gain = sum(deltas) / len(deltas)
    cost_ratio = sum(costs_candidate) / sum(costs_base)
    metrics = {"n": len(cases), "domains": len(domains), "periods": len(periods),
               "mean_paired_gain": round(mean_gain, 6), "cost_ratio": round(cost_ratio, 6),
               "independence": "DECLARED_NOT_AUTHENTICATED"}
    if mean_gain < gain_floor or cost_ratio > cost_ceiling:
        return result("RETIRE_SHADOW" if adopted else "REJECT", "no_predeclared_net_benefit", metrics=metrics)
    return result("CONTINUE_SHADOW" if adopted else "ADOPT_SHADOW_CANDIDATE",
                  "advisory_only_no_execution_or_production_authority", metrics=metrics)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("preflight", "decide"))
    p.add_argument("path", help="ZIP path for preflight, or manifest JSON path for decide")
    p.add_argument("--receipt", help="trusted-side evaluation JSON for decide")
    args = p.parse_args()
    try:
        if args.mode == "preflight":
            output = preflight_zip(args.path)
        else:
            manifest = json.loads(Path(args.path).read_text(encoding="utf-8"))
            receipt = json.loads(Path(args.receipt).read_text(encoding="utf-8")) if args.receipt else None
            output = decision(manifest, receipt)
    except (ValueError, OSError, TypeError):
        output = result("HOLD_INVALID", "unreadable_json_or_file")
    print(json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if output["decision"] in ("METADATA_PREFLIGHT_ONLY", "READY_FOR_ISOLATED_EVALUATION",
                                  "ADOPT_SHADOW_CANDIDATE", "CONTINUE_SHADOW") else 2


if __name__ == "__main__":
    raise SystemExit(main())
