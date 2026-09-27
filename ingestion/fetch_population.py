"""Sum WorldPop 2022 population (1 km, UN-adjusted) within each Kenyan sub-county."""
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
from rasterstats import zonal_stats

URL = ("https://worldpop-public-data.soton.ac.uk/GIS/Population/Global_2021_2022_1km_UNadj/"
       "unconstrained/2022/KEN/ken_ppp_2022_1km_UNadj.tif")
tif = Path("raw/ken_ppp_2022_1km_UNadj.tif")
if not tif.exists():
    tif.write_bytes(requests.get(URL, timeout=300).content)

subs = gpd.read_file("raw/geoBoundaries-KEN-ADM2_simplified.geojson").to_crs(4326)
stats = zonal_stats(list(subs.geometry), str(tif), stats=["sum"])

out = pd.DataFrame({
    "district_id": subs["shapeID"],
    "population": [round(s["sum"] or 0) for s in stats],
})
out_dir = Path("raw/population")
out_dir.mkdir(parents=True, exist_ok=True)
out.to_csv(out_dir / "population.csv", index=False)

print(f"Total population: {out.population.sum():,}")
print(f"Sub-counties with zero population: {(out.population == 0).sum()}")
print(out.merge(pd.read_csv("raw/districts.csv"), on="district_id")
         .sort_values("population", ascending=False)
         [["county_name", "district_name", "population"]].head(8).to_string(index=False))