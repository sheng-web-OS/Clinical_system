#!/usr/bin/env python3
"""Fail closed if a public build contains obvious secrets or private agent controls.

This is a release-boundary regression check, NOT a complete secret-history,
personal-data, or clinical-safety audit. Never print matched secret values.
"""
from __future__ import annotations

import html
from pathlib import Path
import re
import sys


# Deliberately high-confidence signatures; ordinary medical prose and the
# public Cloudflare Web Analytics site identifier are not API credentials.
SECRET_PATTERNS = {
    "GitHub credential": re.compile(r"\b(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{30,})\b"),
    "OpenAI credential": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b"),
    "Slack credential": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "private key header": re.compile(r"-----BEGIN (?:OPENSSH|RSA|EC|DSA|ENCRYPTED )?PRIVATE KEY-----"),
    "API credential assignment": re.compile(
        r"\b(?:OPENAI_API_KEY|GITHUB_TOKEN|GH_TOKEN|CF_API_TOKEN|CLOUDFLARE_API_TOKEN)"
        r"\s*[:=]\s*[\"']?[A-Za-z0-9_-]{20,}\b", re.IGNORECASE
    ),
}
PRIVATE_MARKERS = (
    "This is the PRIVATE source-of-truth repository",
    "Clinical OS repository instructions",
    "docs/master-prompt-v5.1-architecture.md",
    "<!-- XIAOMA_PRIVATE_AGENT -->",
    "## Default agent behavior",
    "libfile_",
)
FORBIDDEN_NAMES = {".env", "AGENTS.md", "master-prompt.md", "id_rsa", "id_ed25519"}
FORBIDDEN_PARTS = {".git", ".github", "archive", "audit", "tools", "__pycache__"}


def scan_dist(dist: Path) -> list[str]:
    """Return sanitized findings: filenames and finding classes, not leaked values."""
    if not dist.is_dir():
        return ["missing public build directory"]
    errors: list[str] = []
    files = sorted(path for path in dist.rglob("*") if path.is_file() or path.is_symlink())
    if not files:
        return ["empty public build directory"]
    for path in files:
        name = path.relative_to(dist).as_posix()
        if path.is_symlink():
            errors.append(f"{name}: symlink forbidden in public build")
            continue
        if path.name in FORBIDDEN_NAMES or set(path.relative_to(dist).parts) & FORBIDDEN_PARTS:
            errors.append(f"{name}: private file/path in public build")
            continue
        content = path.read_bytes().decode("utf-8", errors="ignore")
        # Check encoded HTML entities too; otherwise a template can escape
        # obvious private content into a public HTML document unnoticed.
        versions = (content, html.unescape(content))
        for label, pattern in SECRET_PATTERNS.items():
            if any(pattern.search(version) for version in versions):
                errors.append(f"{name}: {label} detected")
        for marker in PRIVATE_MARKERS:
            if any(marker in version for version in versions):
                errors.append(f"{name}: private agent/source marker detected")
                break
    return errors


def main() -> int:
    dist = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "dist"
    findings = scan_dist(dist)
    if findings:
        for finding in findings:
            print("FAIL release-security: " + finding)
        return 1
    print("PASS release-security: public build contains no recognized secret or private-agent markers.")
    print("NOTE: use a separate private-repo/history scanner and account security review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
