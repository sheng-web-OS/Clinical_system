#!/usr/bin/env python3
"""Freeze verified CC BY DCM journal figures into this *build*, never hotlink to readers.

Failure to fetch or recognize a real image stops publication rather than leaving blank art.
Source texts and license/figure attribution live in the corresponding article.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
import sys
import time
import hashlib

IMAGES = {
    "dcm-pv.webp": "https://www.frontiersin.org/files/Articles/1212875/xml-images/fcvm-10-1212875-g002.webp",
    "dcm-secondary-mr.png": "https://www.mdpi.com/jcm/jcm-14-04518/article_deploy/html/images/jcm-14-04518-g001.png",
    "dcm-ischemic-cmr.webp": "https://www.frontiersin.org/files/Articles/523242/xml-images/fcvm-07-00097-g0003.webp",
}

# Original publisher Figure bytes archived unchanged from a successful audited build.
# SHA-256 prevents silently substituting another patient image or a partial download.
ARCHIVED_SHA256 = {
    "dcm-pv.webp": "2ca703dae92a7dff548c705fe2ce2dd7edbca618925aaec1affc939c9e71f718",
    "dcm-secondary-mr.png": "6f79230df9c1a360fd5b9d835cab54fa7dab9c122c3b393de2e21c00087f1bfe",
    "dcm-ischemic-cmr.webp": "76a422b4a054803b8d654012a1ad9d5c51fb7bcc383ed48c208248bb83fb15b6",
}
ARCHIVE = Path(__file__).resolve().parents[1] / "site/source-assets/dcm"

def is_image(data, suffix):
    if len(data) < 7000 or len(data) > 8_000_000:
        return False
    if suffix == ".webp":
        return data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    return data.startswith(b"\x89PNG\r\n\x1a\n")

def fetch(uri):
    req = Request(uri, headers={"User-Agent": "Mozilla/5.0 (compatible; ClinicalOSSourceFigureArchive/1.0)",
                                "Accept": "image/avif,image/webp,image/png,image/*;q=0.8"})
    with urlopen(req, timeout=28) as response:
        return response.read(8_000_001)

def main():
    directory = Path(sys.argv[1]).resolve() / "assets"
    directory.mkdir(parents=True, exist_ok=True)
    for name, origin in IMAGES.items():
        target = directory / name
        archived = ARCHIVE / name
        if archived.is_file():
            data = archived.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            if digest != ARCHIVED_SHA256[name] or not is_image(data, target.suffix):
                raise RuntimeError("Publication BLOCKED: archived original DCM figure modified: " + name)
            target.write_bytes(data)
            print(f"Verified DCM original archive {name}: {len(data)} bytes, sha256={digest}", flush=True)
            continue
        alternatives = [
            origin,
            "https://images.weserv.nl/?url=" + quote(origin.removeprefix("https://"), safe=""),
        ]
        failures = []
        for url in alternatives:
            for attempt in range(2):
                try:
                    raw = fetch(url)
                    if not is_image(raw, target.suffix):
                        raise ValueError(f"not valid {target.suffix}, bytes={len(raw)}")
                    target.write_bytes(raw)
                    print(f"Verified DCM figure {name}: {len(raw)} bytes")
                    break
                except Exception as exc:
                    failures.append(f"{url}: {type(exc).__name__}: {exc}")
                    time.sleep(1)
            if target.exists():
                break
        if not target.exists():
            raise RuntimeError(f"Journal figure missing; cancel publication: {name}\n" +
                               "\n".join(failures))
    print("PASS: 3 publisher figures embedded as local build assets")

if __name__ == "__main__":
    main()
