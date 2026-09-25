# Climate Resilience & Resource Allocation Platform

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