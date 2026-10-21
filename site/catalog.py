"""Explicit publication list shared by the compiler and output checks."""
import json
import hashlib
import re
from datetime import date
from pathlib import PurePosixPath


def load_pages(root):
    pages = json.loads((root / "site/pages.json").read_text("utf8"))
    if not isinstance(pages, list) or not pages:
        raise ValueError("Publication list must be a non-empty array")
    sources, outputs = set(), set()
    for row in pages:
        for key in ("source", "output", "title", "subtitle"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError("Missing publication field: " + key)
        source = PurePosixPath(row["source"])
        if (source.is_absolute() or ".." in source.parts or
                source.parts[0] != "content" or
                source.suffix != ".md"):
            raise ValueError("Public source must be reader-facing content/ Markdown; internal audit/ stays private")
        path = (root / row["source"]).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError("Missing or escaped publication source: " + row["source"])
        if path.relative_to(root.resolve()).parts[0] != "content":
            raise ValueError("Public source resolves into a private directory")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.html", row["output"]):
            raise ValueError("Output must be a flat HTML filename")
        if row["source"] in sources or row["output"] in outputs:
            raise ValueError("Duplicate publication source or output")
        sources.add(row["source"])
        outputs.add(row["output"])
        if "/lessons/" in row["source"]:
            date.fromisoformat(row.get("date", ""))
            if row.get("review") not in ("author_source_check", "independent_ai_review", "human_review"):
                raise ValueError("Lesson must disclose its actual review type")
        if row.get("kind") == "historical_original":
            date.fromisoformat(row.get("date", ""))
            if row.get("review") != "source_recovery_only":
                raise ValueError("Recovered original must disclose the source recovery review")
            fingerprint = row.get("source_sha256", "")
            if not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
                raise ValueError("Recovered original requires its source fingerprint")
            if hashlib.sha256(path.read_bytes()).hexdigest() != fingerprint:
                raise ValueError("Recovered original changed: " + row["source"])
    return pages



RELEASE_CHECKS = (
    "version_identity",
    "figures_and_tables",
    "clinical_evidence",
    "citation_and_rights",
    "reader_experience",
)


def load_public_pages(root, *, preview=False):
    """Return only explicitly approved, SHA-pinned articles.

    Publication receipts live in private audit/ and are NEVER included in
    dist/. An empty approved list is valid in PR preview mode only.
    """
    candidates = load_pages(root)
    manifest_path = root / "site/release.json"
    manifest = json.loads(manifest_path.read_text("utf8"))
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("approved"), list):
        raise ValueError("Invalid publication-release manifest")
    by_source = {row["source"]: row for row in candidates}
    approved = []
    seen = set()
    for entry in manifest["approved"]:
        if not isinstance(entry, dict):
            raise ValueError("Invalid publication approval entry")
        source = entry.get("source", "")
        receipt = entry.get("receipt", "")
        if not isinstance(source, str) or source not in by_source or source in seen:
            raise ValueError("Publication approval is missing, duplicated, or outside candidate inventory")
        seen.add(source)
        if not isinstance(receipt, str):
            raise ValueError("Publication receipt path must be a string")
        receipt_path = PurePosixPath(receipt)
        if (receipt_path.is_absolute() or ".." in receipt_path.parts
                or receipt_path.parts[:2] != ("audit", "publication")
                or receipt_path.suffix != ".json"):
            raise ValueError("Release receipt must be a private audit/publication JSON")
        receipt_file = (root / receipt).resolve()
        if (not receipt_file.is_relative_to((root / "audit/publication").resolve())
                or not receipt_file.is_file()):
            raise ValueError("Missing private publication receipt: " + receipt)
        record = json.loads(receipt_file.read_text("utf8"))
        actual_sha = hashlib.sha256((root / source).read_bytes()).hexdigest()
        if record.get("source") != source or record.get("source_sha256") != actual_sha:
            raise ValueError("Publication receipt source or content fingerprint mismatch: " + source)
        if record.get("decision") != "publish":
            raise ValueError("Publication requires a final publish decision: " + source)
        try:
            date.fromisoformat(record["approved_on"])
        except (KeyError, TypeError, ValueError):
            raise ValueError("Publication receipt is missing a valid approval date: " + source)
        checks = record.get("checks")
        if not isinstance(checks, dict):
            raise ValueError("Publication receipt missing evidence checks: " + source)
        for check in RELEASE_CHECKS:
            report = checks.get(check)
            if (not isinstance(report, dict) or report.get("status") != "pass"
                    or not isinstance(report.get("evidence"), str)
                    or not report["evidence"].strip()):
                raise ValueError("Publication evidence not passed: " + check + " for " + source)
        approved.append(by_source[source])
    if not approved and not preview:
        raise ValueError(
            "PUBLICATION BLOCKED: no lessons have complete, signed-off quality receipts. "
            "Keep the branch as a draft until one or more articles pass all release checks."
        )
    return approved
