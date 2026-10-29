#!/usr/bin/env python3
"""Offline, synthetic-only first-pass evidence gap probe.

This probe inspects *file content*, not a caller-supplied source_state flag.
It is deliberately lexical (single synthetic figure), not a clinical or
provenance validator, and never calls a model, Google Drive, or GitHub.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

_FIGURE_RE = re.compile(r"\bFigure\s+(F[1-9][0-9]{0,2})\b", re.IGNORECASE)
_ALLOWED_HASH = re.compile(r"^[a-f0-9]{64}$")
_MAX_BYTES = 64 * 1024


class ProbeHold(Exception):
    """Unsafe or unresolvable fixture evidence."""


def _inside(root: Path, relative: str, suffix: str | None = None) -> Path:
    path = PurePosixPath(relative)
    if (path.is_absolute() or not path.parts or
            any(part in {"..", ".", ""} for part in path.parts)):
        raise ProbeHold("UNSAFE_PATH")
    target = root.joinpath(*path.parts)
    if target.is_symlink() or not target.resolve().is_relative_to(root.resolve()):
        raise ProbeHold("UNSAFE_PATH")
    if suffix and target.suffix != suffix:
        raise ProbeHold("UNSAFE_PATH")
    return target


def _read_text(path: Path) -> str:
    try:
        if not path.is_file() or path.stat().st_size > _MAX_BYTES:
            raise ProbeHold("SOURCE_UNREADABLE")
        return path.read_text(encoding="utf-8-sig")
    except (UnicodeError, OSError):
        raise ProbeHold("SOURCE_UNREADABLE") from None


def probe(root: Path, article: str, captions: str) -> dict:
    """Determine if one lexical Figure F# requires an approved source lookup.

    SKIP means an integrity-anchored local *synthetic* caption exists; it
    does not mean primary-source provenance or medical accuracy is verified.
    READ means no local caption or digest exists. Other uncertainty is HOLD.
    """
    def result(decision, reason, figure=None):
        return {"decision": decision, "reason": reason, "figure": figure,
                "model_calls": 0, "external_reads": 0,
                "clinical_provenance_verified": False, "autonomy_certified": False}

    try:
        root = root.resolve(strict=True)
        article_file = _inside(root, article, ".md")
        text = _read_text(article_file)
        refs = set(x.upper() for x in _FIGURE_RE.findall(text))
        if not refs:
            return result("SKIP", "NO_FIGURE_CUE")
        if len(refs) != 1:
            return result("HOLD", "MULTIPLE_FIGURES_UNSUPPORTED")
        figure = next(iter(refs))
        caption_dir = _inside(root, captions)
        caption = _inside(root, str(PurePosixPath(captions) / (figure + ".txt")), ".txt")
        digest = _inside(root, str(PurePosixPath(captions) / (figure + ".sha256")), ".sha256")
        if caption_dir.exists() and (not caption_dir.is_dir() or caption_dir.is_symlink()):
            raise ProbeHold("UNSAFE_PATH")
        if caption_dir.is_dir():
            alternatives = [p for p in caption_dir.glob(figure + "*")
                            if p.name not in {caption.name, digest.name}]
            if alternatives:
                return result("HOLD", "CONFLICTING_LOCAL_CANDIDATES", figure)
        if not caption.exists() and not digest.exists():
            return result("READ", "LOCAL_CAPTION_MISSING", figure)
        if not caption.is_file() or not digest.is_file():
            return result("HOLD", "INCOMPLETE_LOCAL_EVIDENCE", figure)
        body = _read_text(caption)
        anchor = _read_text(digest).strip().lower()
        if not _ALLOWED_HASH.fullmatch(anchor):
            return result("HOLD", "BAD_INTEGRITY_ANCHOR", figure)
        actual_hash = hashlib.sha256(caption.read_bytes()).hexdigest()
        if actual_hash != anchor:
            return result("HOLD", "LOCAL_INTEGRITY_MISMATCH", figure)
        if not re.search(r"^Figure\s+" + re.escape(figure) + r"\s*:\s*\S",
                         body, re.IGNORECASE | re.MULTILINE):
            return result("HOLD", "CAPTION_CUE_MISSING", figure)
        return result("SKIP", "LOCAL_CAPTION_INTEGRITY_MATCH", figure)
    except (ProbeHold, OSError) as error:
        label = str(error) if isinstance(error, ProbeHold) else "SOURCE_UNREADABLE"
        return result("HOLD", label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--article", required=True)
    parser.add_argument("--captions", required=True)
    args = parser.parse_args()
    result = probe(args.root, args.article, args.captions)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["decision"] != "HOLD" else 2


if __name__ == "__main__":
    sys.exit(main())
