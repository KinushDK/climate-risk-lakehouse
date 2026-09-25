"""Download Kenya county (ADM1) and sub-county (ADM2) boundaries from geoBoundaries."""
from pathlib import Path
import requests

RAW = Path("raw")
RAW.mkdir(exist_ok=True)

for level in ["ADM1", "ADM2"]:
    meta = requests.get(
        f"https://www.geoboundaries.org/api/current/gbOpen/KEN/{level}/", timeout=60
    ).json()
    out = RAW / f"geoBoundaries-KEN-{level}_simplified.geojson"
    out.write_bytes(requests.get(meta["simplifiedGeometryGeoJSON"], timeout=120).content)
    print(f"{level}: {meta['admUnitCount']} units, licence: {meta['boundaryLicense']} -> {out}")