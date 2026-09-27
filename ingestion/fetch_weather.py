"""Download daily weather (1985-2025) for each Kenyan sub-county from NASA POWER. 
Resumable: skips sub-counties already downloaded. Re-run to retry any failures."""
import io
import time
from pathlib import Path

import pandas as pd
import requests

URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
PARAMS = {
    "parameters": "PRECTOTCORR,T2M_MAX,T2M_MIN,GWETROOT",
    "community": "AG",
    "start": "19850101",
    "end": "20251231",
    "format": "CSV",
}
OUT = Path("raw/weather")
OUT.mkdir(parents=True, exist_ok=True)


def fetch(lat, lon, attempts=4):
    """Call the API, retrying with exponential backoff (10s, 20s, 40s...)."""
    for i in range(attempts):
        try:
            r = requests.get(URL, params={**PARAMS, "latitude": lat, "longitude": lon}, timeout=300)
            r.raise_for_status()
            return r.text
        except requests.RequestException as e:
            wait = 10 * 2 ** i
            print(f"    attempt {i + 1} failed ({e}); retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError("all attempts failed")


districts = pd.read_csv("raw/districts.csv")
failed = []

for n, d in enumerate(districts.itertuples(), 1):
    target = OUT / f"{d.district_id}.csv"
    if target.exists():
        continue
    print(f"[{n}/{len(districts)}] {d.district_name} ({d.county_name})")
    try:
        text = fetch(d.lat, d.lon)
        body = text.split("-END HEADER-", 1)[-1].lstrip()   # drop NASA's metadata block
        df = pd.read_csv(io.StringIO(body))
        df.insert(0, "district_id", d.district_id)
        tmp = target.with_suffix(".tmp")
        df.to_csv(tmp, index=False)
        tmp.replace(target)          # write fully, then rename
    except Exception as e:
        print(f"    FAILED: {e}")
        failed.append(d.district_id)
    time.sleep(1)                    # be polite to the API

done = len(list(OUT.glob("*.csv")))
print(f"\nDone: {done}/{len(districts)} files. Failed this run: {len(failed)}")
if failed:
    print("Re-run the script to retry these:", failed)