from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = yaml.safe_load((ROOT / "config" / "risk_weights.yml").read_text())


def test_risk_weights_sum_to_one():
    assert abs(sum(CONFIG["weights"].values()) - 1.0) < 1e-9


def test_risk_tiers_are_in_descending_order():
    t = CONFIG["tiers"]
    assert t["high"] > t["elevated"] > t["watch"] > 0


def test_census_file_covers_all_counties_and_matches_national_total():
    census = pd.read_csv(ROOT / "config" / "census_2019_county.csv")
    assert len(census) == 47
    assert census.county_name.is_unique
    assert census.population_2019.sum() == 47_564_296   # KNBS 2019, Table 2.2