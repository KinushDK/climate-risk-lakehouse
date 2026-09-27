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



SHOW SCHEMAS IN workspace LIKE 'climate*';