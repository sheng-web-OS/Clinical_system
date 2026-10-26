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

IMAGES = {
    "dcm-pv.webp": "https://www.frontiersin.org/files/Articles/1212875/xml-images/fcvm-10-1212875-g002.webp",
    "dcm-secondary-mr.png": "https://mdpi-res.com/jcm/jcm-14-04518/article_deploy/html/images/jcm-14-04518-g001.png",
    "dcm-ischemic-cmr.webp": "https://www.frontiersin.org/files/Articles/523242/xml-images/fcvm-07-00097-g0003.webp",
}

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
