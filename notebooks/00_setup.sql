-- Phase 0: create the lakehouse layers
CREATE SCHEMA IF NOT EXISTS workspace.climate_raw
  COMMENT 'Landing zone for raw downloaded files';
CREATE VOLUME IF NOT EXISTS workspace.climate_raw.landing
  COMMENT 'Raw CSV/JSON files uploaded from ingestion scripts';

CREATE SCHEMA IF NOT EXISTS workspace.climate_bronze
  COMMENT 'Raw data as ingested, with lineage columns';
CREATE SCHEMA IF NOT EXISTS workspace.climate_silver
  COMMENT 'Cleaned, typed and validated data';
CREATE SCHEMA IF NOT EXISTS workspace.climate_gold
  COMMENT 'Business-ready risk scores and allocations';

-- Subdirectories (districts, weather, soil, population) inside the landing volume
-- are auto-created when files are first written to them during ingestion.
-- To pre-create them, run this in a Python notebook or .py file:
--   base = "/Volumes/workspace/climate_raw/landing"
--   for folder in ["districts", "weather", "soil", "population"]:
--       dbutils.fs.mkdirs(f"{base}/{folder}")
--   display(dbutils.fs.ls(base))


SHOW SCHEMAS IN workspace LIKE 'climate*';