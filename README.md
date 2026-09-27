# Climate Resilience & Resource Allocation Platform
![tests](https://github.com/KinushDK/climate-risk-lakehouse/actions/workflows/tests.yml/badge.svg)

**Problem:** Field offices across 290 sub-counties in Kenya's 47 counties need to decide where drought-relief and agricultural-support resources go first. 
Rainfall, temperature and soil data exist but are scattered across raw files and APIs, so prioritisation is slow and hard to justify.

**Solution:** A Databricks lakehouse that ingests daily climate and soil data (1985–2025),
cleans and validates it through a Bronze/Silver/Gold pipeline, and produces a monthly,
explainable risk score and budget allocation per district.

**Stack:** Databricks · PySpark · SQL · Delta Lake · Unity Catalog · Auto Loader · Lakeflow Jobs · AI/BI Dashboards

## Status
🚧 In progress — Phase 0: setup complete

## Architecture
_Diagram coming soon._

## Data sources
- District boundaries: geoBoundaries gbOpen KEN ADM1/ADM2 (source: IEBC, OCHA ROSEA), licensed CC BY 3.0 IGO
- Weather: NASA POWER daily API
- Soil: ISRIC SoilGrids

## Project structure
- `ingestion/` — local scripts that download raw data
- `notebooks/` — Databricks pipeline (bronze → silver → gold)
- `config/` — scoring weights and thresholds
- `tests/` — unit tests for transformation logic
- `dashboards/` — exported AI/BI dashboard

## Results

The score was calibrated on the 2022 drought and validated on seasons it never saw:

| Season (Oct–Dec) | Sub-counties at Watch or above | Context |
|---|---|---|
| 2010 | 160 of 290 (55%) | Failed rains preceding the 2011 Horn of Africa drought |
| 2016 | 249 of 290 (86%) | Failed rains; national drought disaster declared early 2017 |
| 2019 | 4 of 290 (1%) | One of the wettest seasons on record |
| 2022 | 139 of 290 (48%) | Fifth consecutive failed season |

Without any location input, the highest-scoring counties in Dec 2022 were Marsabit, Samburu,
Tana River, Wajir and Mandera — Kenya's arid and semi-arid counties most affected by the drought.

## Limitations
- **Weather resolution:** NASA POWER data sits on a coarse grid (~50 km cells). The 290
  sub-counties fall into only 93 distinct cells, so neighbouring sub-counties often share identical weather and are differentiated only by soil properties.
  
- **Soil gaps:** SoilGrids has no data for built-up areas. 18 sub-counties (urban cores of   Nairobi, Mombasa, Kisumu and Nakuru, plus lakeshore Nyatike) 
  have soil values imputed from their county median and are flagged with `soil_imputed = true`.
  
- **Rainfall scoring:** plain z-scores understate droughts in arid areas, where rainfall varies widely year to year. Tier thresholds were calibrated on the 2022 drought and validated on
  2010 and 2016. Planned v2: replace z-scores with a gamma-fitted SPI.
  
 - **Population:** WorldPop's unconstrained estimates placed ~2.3M people in Mandera versus ~0.87M in the 2019 census. Sub-county populations are therefore calibrated to official
  KNBS 2019 county totals, using WorldPop only for the distribution within each county.