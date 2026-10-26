#!/usr/bin/env python3
"""Fail-safe CI scope selector for pull requests with only private intake edits.

Only an exact path prefix can skip redundant site compilation. All PRs still
run unit tests, publication/source checks and corpus validation. Main pushes
and manually dispatched builds always perform the full site build.
"""
from pathlib import Path, PurePosixPath
import argparse

PRIVATE_INTAKE_PREFIX = "archive/xiaoma-reading/intake/"


def private_intake_path(name: str) -> bool:
    if not isinstance(name, str) or not name or "\n" in name or "\r" in name or "\\" in name:
        return False
    path = PurePosixPath(name)
    return (not path.is_absolute() and path.as_posix() == name
            and ".." not in path.parts and name.startswith(PRIVATE_INTAKE_PREFIX)
            and len(path.parts) > len(PurePosixPath(PRIVATE_INTAKE_PREFIX).parts))


def classify(paths: list[str]) -> str:
    """Permit the shorter path only when every changed file is private intake."""
    if paths and all(private_intake_path(name) for name in paths):
        return "private_intake"
    return "full_site"


def parse_nul_paths(data: bytes) -> list[str]:
    """Git diff -z avoids unsafe parsing of whitespace and Unicode paths."""
    if data and not data.endswith(b"\0"):
        raise ValueError("Non-NUL-terminated diff; do not allow an unsafe CI fast path")
    return [part.decode("utf-8") for part in data.split(b"\0") if part]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths0", required=True, type=Path)
    parser.add_argument("--github-output", required=True, type=Path)
    args = parser.parse_args()
    scope = classify(parse_nul_paths(args.paths0.read_bytes()))
    args.github_output.open("a", encoding="utf-8").write(
        f"full_build={'false' if scope == 'private_intake' else 'true'}\n"
        f"scope={scope}\n"
    )
    print(f"CI scope: {scope}; full site build = {scope != 'private_intake'}")


if __name__ == "__main__":
    main()
