#!/usr/bin/env python3
"""Opt-in Mac user LaunchAgent for a bounded, read-only ALE Anki upload.

This installs only a local periodic runner. It cannot sync iPhone/AnkiWeb
or grant a cloud ChatGPT task permission to read an owner-private Sheet.
No OAuth or card content is stored in the launchd plist.
"""
import argparse
import os
import plistlib
import subprocess
import sys
from pathlib import Path

LABEL = "org.clinicalos.ale.anki-readonly-sync"
INTERVAL_SECONDS = 1800


def make_agent_config(wrapper: Path, logs: Path, interval: int = INTERVAL_SECONDS):
    if interval < 600 or interval > 86400:
        raise ValueError("interval must be between 600 and 86400 seconds")
    if not wrapper.is_absolute() or not logs.is_absolute():
        raise ValueError("wrapper and log directory must be absolute")
    return {
        "Label": LABEL,
        "ProgramArguments": ["/bin/bash", str(wrapper)],
        "RunAtLoad": True,
        "StartInterval": interval,
        "KeepAlive": False,
        "StandardOutPath": str(logs / "ale-autosync.out.log"),
        "StandardErrorPath": str(logs / "ale-autosync.err.log"),
        "ProcessType": "Background",
    }


def control(*args):
    result = subprocess.run(["/bin/launchctl", *args], capture_output=True, text=True)
    if result.returncode:
        # Avoid forwarding potentially private provider diagnostics.
        print("LAUNCHCTL_FAILED | action=" + args[0], file=sys.stderr)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "status", "uninstall"))
    args = parser.parse_args()
    if sys.platform != "darwin":
        parser.error("macOS user session only")
    home = Path.home()
    vault = home / "Library" / "Application Support" / "ClinicalOS-ALE"
    wrapper = (Path(__file__).resolve().parent / "ale_anki_unattended_run.sh").resolve()
    uploader = wrapper.parent / "ale_anki_drive_sync.py"
    plist = home / "Library" / "LaunchAgents" / (LABEL + ".plist")
    domain = "gui/" + str(os.getuid())
    service = domain + "/" + LABEL

    if args.action == "status":
        if not plist.is_file():
            print("ALE_AUTOSYNC_NOT_INSTALLED")
            return 0
        status = control("print", service)
        print("ALE_AUTOSYNC_LOADED" if status == 0 else "ALE_AUTOSYNC_PLIST_PRESENT_NOT_LOADED")
        return status

    if args.action == "uninstall":
        if not plist.exists():
            print("ALE_AUTOSYNC_ALREADY_ABSENT")
            return 0
        control("bootout", service)
        plist.unlink()
        print("ALE_AUTOSYNC_UNINSTALLED | OAuth and existing review data retained")
        return 0

    if plist.exists():
        print("ALE_AUTOSYNC_ALREADY_PRESENT | use status; uninstall first to reinstall")
        return 2
    if not wrapper.is_file() or not uploader.is_file():
        print("ALE_AUTOSYNC_SOURCE_MISSING", file=sys.stderr)
        return 2
    # Never schedule an older key-only uploader; require #261 full content readback.
    source = uploader.read_text(encoding="utf-8")
    if ("def _remote_event_index(" not in source
            or "Remote immutable review content differs; cursor NOT advanced" not in source):
        print("ALE_CONTENT_READBACK_GUARD_MISSING | integrate PR #261 before install", file=sys.stderr)
        return 2
    if not (vault / "venv" / "bin" / "python3").is_file():
        print("ALE_SETUP_MISSING | run the existing owner-local setup first")
        return 2
    logs = vault / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    logs.chmod(0o700)
    plist.parent.mkdir(parents=True, exist_ok=True)
    config = make_agent_config(wrapper, logs)
    # Exclusive creation; no rewrite of an unrelated or user-modified agent.
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(plist, flags, 0o600)
    with os.fdopen(fd, "wb") as stream:
        plistlib.dump(config, stream, sort_keys=True)
    if control("bootstrap", domain, str(plist)):
        print("ALE_AUTOSYNC_PLIST_CREATED_BUT_NOT_LOADED | check login GUI session")
        return 3
    print("ALE_AUTOSYNC_INSTALLED | 30-minute wake checks while Mac is awake")
    print("ALE_SYNC_REQUIRES | iPhone->AnkiWeb->Mac normal sync and Anki Desktop open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
