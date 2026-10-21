"""Only the specifically approved, credited DCM figures; fail closed on unavailable sources."""
from pathlib import Path
from urllib.request import Request, urlopen
import time

# Figure labels and source attribution are in the article's corresponding captions.
# Both Frontiers articles and the JCM article are CC BY; never fetch Pocket's PDF assets.
FIGURES = {
    "dcm-pv.webp": (
        "https://www.frontiersin.org/files/Articles/1212875/xml-images/fcvm-10-1212875-g002.webp",
        "webp",
    ),
    "dcm-secondary-mr.png": (
        "https://www.mdpi.com/jcm/jcm-14-04518/article_deploy/html/images/jcm-14-04518-g001.png",
        "png",
    ),
    "dcm-ischemic-cmr.webp": (
        "https://www.frontiersin.org/files/Articles/523242/xml-images/fcvm-07-00097-g0003.webp",
        "webp",
    ),
}

def stage_figures(dist):
    target = dist / "assets"
    target.mkdir(parents=True, exist_ok=True)
    for filename, (url, fmt) in FIGURES.items():
        last_exc = None
        for attempt in range(3):
            try:
                req = Request(url, headers={"User-Agent":"Mozilla/5.0 (compatible; ClinicalOS-education/1.0)", "Accept":"image/avif,image/webp,image/png,image/*;q=0.8,*/*;q=0.5"})
                with urlopen(req, timeout=25) as response:
                    contents = response.read(8_000_001)
                if len(contents) < 1024 or len(contents) > 8_000_000:
                    raise ValueError("unexpected figure size")
                if fmt == "png" and contents[:8] != b"\x89PNG\r\n\x1a\n":
                    raise ValueError("not a PNG image")
                if fmt == "webp" and not (contents[:4] == b"RIFF" and contents[8:12] == b"WEBP"):
                    raise ValueError("not a WebP image")
                (target / filename).write_bytes(contents)
                break
            except Exception as exc:
                last_exc = exc
                if attempt < 2:
                    time.sleep(1 + attempt)
        else:
            raise RuntimeError(f"DCM figure failed retrieval/format verification: {filename}: {last_exc}") from last_exc
    return sorted((Path("assets") / filename).as_posix() for filename in FIGURES)
