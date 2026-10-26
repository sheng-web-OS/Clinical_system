#!/usr/bin/env python3
"""Ship original CC BY Silverman 2018 ECGs as build-local site assets.

The figure bytes come from the NCBI PubMed Central article repository, not
from a publisher hotlink at reader time and not from an AI ECG reconstruction.
Fail closed when the figures cannot be retrieved or recognized. Source and
figure attribution are presented in each corresponding article.

PMCID: PMC6166305, DOI: 10.1177/2324709618802870 (CC BY 4.0).
"""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import sys
import time

PMCID = "6166305"
DOI_FILE = "10.1177_2324709618802870"
ORIGIN = "https://pmc.ncbi.nlm.nih.gov/articles/instance/" + PMCID + "/bin/"
# Immutable successful Cloudflare Pages deployment containing ORIGINAL audited ECG bytes.
# The source was bundled by our prior checksum-pinned build; this is a historical
# artifact fallback for Cloudflare runners blocked by PMC anti-bot truncated output.
# Keep hash+pixel+JPEG validation below; never accept a lookalike or a 21KB response.
VERIFIED_DEPLOYMENT_ASSETS = "https://b4d47291.sheng-clinical-system.pages.dev/assets/"
FIGURES = {
    "silverman-2018-fig1.jpg": (ORIGIN + DOI_FILE + "-fig1.jpg", (753, 536)),
    "silverman-2018-fig2.jpg": (ORIGIN + DOI_FILE + "-fig2.jpg", (753, 341)),
    "silverman-2018-fig3.jpg": (ORIGIN + DOI_FILE + "-fig3.jpg", (753, 343)),
}
# Byte-identity pinned from the first successful GitHub Actions source retrieval.
# A changed image is not silently accepted as the same patient ECG.
EXPECTED_SHA256 = {
    "silverman-2018-fig1.jpg": "fe63862dbb8ccb02711d8caac7946102a103f9953c7d3504af3daccef9d2dbeb",
    "silverman-2018-fig2.jpg": "d1166b7000b5951081f0e268000b86c2f48d21882c03feb1c528dc3ad501686a",
    "silverman-2018-fig3.jpg": "04aeb13a3309f5b1b66949b325a1c2856c65abc71d1da64d525a6670a870d2e6"
}

def jpeg_dimensions(data):
    """Read actual SOF pixel dimensions without installing an imaging stack."""
    if not data.startswith(bytes.fromhex("ffd8")):
        return None
    index = 2
    while index + 9 < len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        while index < len(data) and data[index] == 0xFF:
            index += 1
        if index >= len(data):
            break
        marker = data[index]
        index += 1
        if marker in (0xD9, 0xDA):
            break
        if marker in range(0xD0, 0xD8) or marker == 0x01:
            continue
        if index + 2 > len(data):
            break
        length = int.from_bytes(data[index:index+2], "big")
        if length < 2 or index + length > len(data):
            break
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF) and length >= 7:
            height = int.from_bytes(data[index+3:index+5], "big")
            width = int.from_bytes(data[index+5:index+7], "big")
            return width, height
        index += length
    return None

def original_figure(uri):
    req = Request(uri, headers={
        "User-Agent": "Mozilla/5.0 (compatible; ClinicalOS-Figure-Archive/1.0; educational citation)",
        "Accept": "image/jpeg,image/*;q=0.9",
    })
    with urlopen(req, timeout=28) as response:
        return response.read(6_000_001)

def verified_original(image, filename, expected):
    if not 7000 < len(image) < 6_000_000 or not image.endswith(bytes.fromhex("ffd9")):
        raise ValueError("invalid or incomplete JPEG content: " + str(len(image)))
    actual = jpeg_dimensions(image)
    if actual != expected:
        raise ValueError(f"unverified original ECG dimensions: {actual} != {expected}")
    digest = hashlib.sha256(image).hexdigest()
    if digest != EXPECTED_SHA256[filename]:
        raise ValueError("original ECG source image checksum changed: " + digest)
    return actual, digest


def main():
    destination = Path(sys.argv[1]).resolve() / "assets"
    destination.mkdir(parents=True, exist_ok=True)
    cache = Path(__file__).resolve().parents[1] / ".figure-cache" / "silverman2018"
    cache.mkdir(parents=True, exist_ok=True)
    for filename, (uri, expected) in FIGURES.items():
        cached = cache / filename
        if cached.exists():
            try:
                image = cached.read_bytes()
                actual, digest = verified_original(image, filename, expected)
                (destination / filename).write_bytes(image)
                print(f"PASS {filename}: verified cached original ECG {actual}, sha256={digest}", flush=True)
                continue
            except (OSError, ValueError) as exc:
                print(f"Discarding invalid ECG cache {filename}: {exc}", flush=True)
                cached.unlink(missing_ok=True)

        errors = []
        # The immutable, previously published, byte-audited originals come first.
        # Direct PMC is a second chance; never bypass the hard-coded SHA-256 pins.
        for origin in (VERIFIED_DEPLOYMENT_ASSETS + filename, uri):
            for attempt in range(2):
                try:
                    image = original_figure(origin)
                    actual, digest = verified_original(image, filename, expected)
                    cached.write_bytes(image)
                    (destination / filename).write_bytes(image)
                    print(f"PASS {filename}: checksum-verified original ECG from {origin}; "
                          f"{actual[0]}x{actual[1]}, {len(image)} bytes, sha256={digest}", flush=True)
                    break
                except Exception as exc:
                    errors.append(f"{origin} attempt {attempt+1}: {type(exc).__name__}: {exc}")
                    if attempt < 1:
                        time.sleep(1)
            if (destination / filename).is_file():
                break
        else:
            raise RuntimeError(
                "Publication BLOCKED: actual ECG image unavailable: " + filename + "\n" +
                "\n".join(errors)
            )
    print("PASS: all 3 original Silverman 2018 ECGs bundled as local publication assets",flush=True)

if __name__ == "__main__":
    main()
