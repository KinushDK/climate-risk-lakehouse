"""One representative point per Kenyan sub-county, tagged with its county."""
import geopandas as gpd

EQUAL_AREA = 6933   # projected CRS so areas and distances are in metres

subs = gpd.read_file("raw/geoBoundaries-KEN-ADM2_simplified.geojson").to_crs(4326)
counties = (gpd.read_file("raw/geoBoundaries-KEN-ADM1_simplified.geojson")
            .to_crs(EQUAL_AREA)[["shapeName", "geometry"]]
            .rename(columns={"shapeName": "county_name"}))

# a point guaranteed to fall inside each sub-county (a centroid can land outside odd shapes)
points = gpd.GeoDataFrame(
    subs[["shapeID", "shapeName"]],
    geometry=subs.representative_point(),
    crs=4326,
)
points["area_km2"] = (subs.to_crs(EQUAL_AREA).area / 1e6).round(1)

# attach county: nearest county polygon (distance 0 when inside);
# nearest, not "within", because the two files come from different sources and edges don't line up perfectly
joined = (gpd.sjoin_nearest(points.to_crs(EQUAL_AREA), counties, how="left")
          .drop(columns="index_right")
          .drop_duplicates("shapeID")
          .to_crs(4326))

out = (joined.assign(lat=joined.geometry.y.round(4), lon=joined.geometry.x.round(4))
             .rename(columns={"shapeID": "district_id", "shapeName": "district_name"})
             [["district_id", "district_name", "county_name", "lat", "lon", "area_km2"]])

out.to_csv("raw/districts.csv", index=False)

# sanity checks
print(f"Sub-counties: {len(out)}  (expected 290)")
print(f"Counties matched: {out.county_name.nunique()}  (expected 47)")
print(f"Missing county: {out.county_name.isna().sum()}")
print(f"Duplicate IDs: {out.district_id.duplicated().sum()}")
print(out.head())
