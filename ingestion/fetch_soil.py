"""Sample SoilGrids 2.0 soil properties at each sub-county point. """
from pathlib import Path

import pandas as pd
import rasterio
from rasterio.warp import transform

PROPERTIES = ["clay", "sand", "soc"]          # clay %, sand %, soil organic carbon
DEPTHS = ["0-5cm", "5-15cm", "15-30cm"]       # topsoil, where crop roots are
BASE = "/vsicurl/https://files.isric.org/soilgrids/latest/data"

districts = pd.read_csv("raw/districts.csv")
out_dir = Path("raw/soil")
out_dir.mkdir(parents=True, exist_ok=True)

rows = []
with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",   # don't list remote folders
                  GDAL_HTTP_MAX_RETRY=5, GDAL_HTTP_RETRY_DELAY=3):
    for prop in PROPERTIES:
        for depth in DEPTHS:
            layer = f"{prop}_{depth}_mean"
            with rasterio.open(f"{BASE}/{prop}/{layer}.vrt") as src:
                # SoilGrids uses its own map projection, so convert our lat/lon into it
                xs, ys = transform("EPSG:4326", src.crs,
                                   districts.lon.tolist(), districts.lat.tolist())
                values = [v[0] for v in src.sample(zip(xs, ys))]
                nodata = src.nodata
            for district_id, v in zip(districts.district_id, values):
                rows.append({
                    "district_id": district_id,
                    "property": prop,
                    "depth": depth,
                    "value_mapped": None if v == nodata else int(v),
                })
            print(f"{layer}: sampled {len(values)} points")

df = pd.DataFrame(rows)
df.to_csv(out_dir / "soil_points.csv", index=False)

# sanity checks (mapped units / 10 = clay %, sand %, SOC g/kg)
print(f"\nRows: {len(df)}  (expected {290 * 9})")
print(f"Missing values: {df.value_mapped.isna().sum()}")
print((df.assign(value=df.value_mapped / 10)
         .groupby("property").value.describe()[["min", "mean", "max"]].round(1)))