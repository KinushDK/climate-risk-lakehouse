from datetime import date

import pytest

pytest.importorskip("pyspark")   # skip these tests if Spark isn't installed locally

from climate_risk.transforms import clean_numeric, doy_to_date, failed_rules, weather_rules


def test_clean_numeric_turns_missing_marker_into_null(spark):
    df = spark.createDataFrame([("12.5",), ("-999",), ("0",)], "v string")
    result = [r.v for r in df.select(clean_numeric("v").alias("v")).collect()]
    assert result == [12.5, None, 0.0]


def test_doy_to_date_handles_leap_years(spark):
    df = spark.createDataFrame(
        [(1985, 1), (1988, 366), (2024, 60), (2023, 60)], "YEAR int, DOY int"
    )
    result = [r.d for r in df.select(doy_to_date().alias("d")).collect()]
    assert result == [date(1985, 1, 1), date(1988, 12, 31), date(2024, 2, 29), date(2023, 3, 1)]


def test_failed_rules_lists_every_broken_rule(spark):
    schema = ("_known boolean, date date, precip_mm double, "
              "tmax_c double, tmin_c double, root_soil_wetness double")
    rows = [
        (True, date(2020, 1, 1), 5.0, 30.0, 15.0, 0.5),    # valid
        (True, date(2020, 1, 1), -5.0, 20.0, 25.0, 0.5),   # negative rain AND tmax < tmin
        (True, date(2020, 1, 1), None, None, None, None),  # nulls are not failures
        (None, date(2020, 1, 1), 5.0, 30.0, 15.0, 0.5),    # district not in reference table
        (True, date(2020, 1, 1), 5.0, 60.0, 15.0, 1.4),    # impossible temp and soil wetness
    ]
    df = spark.createDataFrame(rows, schema)
    result = [r.f for r in df.select(failed_rules(weather_rules()).alias("f")).collect()]
    assert result == [
        "",
        "rain_out_of_range, tmax_below_tmin",
        "",
        "unknown_district",
        "temp_out_of_range, soil_wetness_invalid",
    ]