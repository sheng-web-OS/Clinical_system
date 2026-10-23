"""Publication gate for source Figure/Table provenance and reader-facing representation.

This verifies *evidence of review and actual rendered/reachable targets*, not medical
truth, copyright clearance, or instructional effectiveness.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re


VALID_MODES = {"illustrated", "source_link"}
VALID_STATES = {"represented", "no_relevant_visual"}
REVIEW_FILE = "audit/figure-gate.json"


def _blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = b"blob " + str(len(data)).encode("ascii") + b"\x00"
    return hashlib.sha1(header + data).hexdigest()


def _teaching_page(row: dict) -> bool:
    source = row["source"]
    if row.get("kind") == "historical_original":
        return False  # Immutable historical artifact; an edited integration is a new page.
    return ("/lessons/" in source or row.get("kind") == "ai_integrated")


def _require(value, what, source, min_len=1):
    if not isinstance(value, str) or len(value.strip()) < min_len:
        raise ValueError("Figure audit " + source + ": missing/inadequate " + what)
    return value.strip()


def _linked_file(text: str, from_file: str, target: str) -> bool:
    """Resolve explicit reader-visible links, not bare mentions of an audit file."""
    links = re.findall(r"\]\(([^)]+)\)", text)
    links += re.findall(r'href=["\x27]([^"\x27]+)["\x27]', text)
    base = PurePosixPath(from_file).parent
    for link in links:
        if link.startswith(("https:", "http:", "mailto:", "tel:", "#", "//")):
            continue
        candidate = link.split("#")[0].split("?")[0]
        # pathlib normalization doesn't remove ".."; resolve against the real root later.
        parts = list(base.parts)
        for piece in PurePosixPath(candidate).parts:
            if piece == "..":
                if parts: parts.pop()
            elif piece != ".":
                parts.append(piece)
        if PurePosixPath(*parts).as_posix() == target:
            return True
    return False


def validate_figure_gate(root: Path, pages: list) -> None:
    """Fail new/edited teaching pages without evidence, while pinning legacy pages."""
    entries = {r["source"]: r for r in pages if _teaching_page(r)}
    if not entries:
        return  # Directory/metadata-only or historical-only fixture has no new teaching output.
    path = root / REVIEW_FILE
    if not path.is_file():
        raise ValueError("Figure audit gate missing: " + REVIEW_FILE)
    try:
        record = json.loads(path.read_text(encoding="utf8"))
    except (ValueError, OSError) as exc:
        raise ValueError("Figure audit gate invalid JSON") from exc

    legacy = record.get("legacy_frozen")
    reviews = record.get("reviews")
    if not isinstance(legacy, dict) or not isinstance(reviews, dict):
        raise ValueError("Figure audit requires legacy_frozen and reviews maps")

    unknown = (set(legacy) | set(reviews)) - set(entries)
    if unknown:
        raise ValueError("Figure audit has unregistered teaching source: " + sorted(unknown)[0])
    if set(legacy) & set(reviews):
        raise ValueError("Figure audit duplicate legacy and reviewed entry")

    for source, row in entries.items():
        document = (root / source)
        if source in legacy:
            expected = _require(legacy[source], "legacy blob fingerprint", source)
            if not re.fullmatch(r"[0-9a-f]{40}", expected):
                raise ValueError("Figure audit invalid legacy blob fingerprint: " + source)
            if _blob_sha(document) != expected:
                raise ValueError("Figure audit LEGACY_CHANGED: " + source + " requires source Figure/Table review")
            continue
        if source not in reviews:
            raise ValueError("Figure audit MISSING: " + source + " cannot publish unreviewed teaching content")
        check = reviews[source]
        if not isinstance(check, dict):
            raise ValueError("Figure audit record must be an object: " + source)
        status = _require(check.get("status"), "status", source)
        if status not in VALID_STATES:
            raise ValueError("Figure audit HOLD: " + source + " has unsupported/incomplete status " + status)
        src_doc = _require(check.get("source_review"), "source_review", source)
        if src_doc == source or src_doc.startswith("/") or ".." in PurePosixPath(src_doc).parts:
            raise ValueError("Figure audit source review must be a separate safe source document: " + source)
        # Must be publicly navigable, so readers can independently locate evidence.
        if src_doc not in {r["source"] for r in pages}:
            raise ValueError("Figure audit source review not published: " + source)
        evidence_file = root / src_doc
        if not evidence_file.is_file():
            raise ValueError("Figure audit missing source review document: " + source)
        body, evidence = document.read_text("utf8"), evidence_file.read_text("utf8")
        if not _linked_file(body, source, src_doc):
            raise ValueError("Figure audit reader has no source review link: " + source)
        if status == "no_relevant_visual":
            if check.get("items"):
                raise ValueError("Figure audit no_relevant_visual must not disguise known figures: " + source)
            _require(check.get("examined_pages"), "examined_pages", source, 12)
            _require(check.get("rationale"), "rationale", source, 40)
            token = _require(check.get("source_token"), "source_token", source, 8)
            if token.casefold() not in evidence.casefold():
                raise ValueError("Figure audit no_relevant_visual source not verifiable: " + source)
            continue

        items = check.get("items")
        if not isinstance(items, list) or not items:
            raise ValueError("Figure audit no item represented: " + source)
        anchors = set()
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("Figure audit item must be an object: " + source)
            loc = _require(item.get("locator"), "original Figure/Table and exact page", source, 24)
            token = _require(item.get("source_token"), "matching source token", source, 8)
            _require(item.get("teaching_role"), "why this item changes reasoning", source, 32)
            _require(item.get("scope_limit"), "what it cannot establish", source, 25)
            if token.casefold() not in evidence.casefold():
                raise ValueError("Figure audit locator is absent from source review: " + source + " / " + loc)
            mode = _require(item.get("mode"), "representation mode", source)
            if mode not in VALID_MODES:
                raise ValueError("Figure audit unsupported representation mode: " + source)
            if mode == "illustrated":
                anchor = _require(item.get("anchor"), "visible figure id", source)
                if anchor in anchors:
                    raise ValueError("Figure audit duplicate reader figure id: " + source)
                anchors.add(anchor)
                pat = r'<figure\b(?=[^>]*\bid=["\x27]' + re.escape(anchor) + r'["\x27])[^>]*>(.*?)</figure>'
                match = re.search(pat, body, re.DOTALL | re.IGNORECASE)
                if not match or not re.search(r"<figcaption\b", match.group(1), re.I):
                    raise ValueError("Figure audit missing illustrated figure or caption: " + source + " #" + anchor)
                caption_text = re.sub(r"<[^>]+>", " ", match.group(1))
                caption_token = _require(item.get("caption_token"), "caption/source marker", source, 8)
                if caption_token.casefold() not in caption_text.casefold():
                    raise ValueError("Figure audit caption omits source identity: " + source + " #" + anchor)
            else:
                url = _require(item.get("url"), "direct original figure/table URL", source, 18)
                if not url.startswith("https://"):
                    raise ValueError("Figure audit source_link must be HTTPS: " + source)
                if url not in body:
                    raise ValueError("Figure audit original figure/table URL absent from reader: " + source)
                _require(item.get("why_link_instead"), "explanation for link rather than embedding", source, 35)


def audit_coverage(root: Path, pages: list) -> dict:
    """Read-only inventory for backlog reporting; never interpret as certification."""
    record = json.loads((root / REVIEW_FILE).read_text("utf8"))
    sources = [r["source"] for r in pages if _teaching_page(r)]
    return {"teaching_pages": len(sources),
            "source_reviewed": sum(s in record["reviews"] for s in sources),
            "legacy_pending": sum(s in record["legacy_frozen"] for s in sources)}
