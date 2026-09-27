"""Silver-layer transformation logic, shared by the Databricks notebook and the unit tests."""
from pyspark.sql import Column, functions as F

MISSING_SENTINEL = -999   # NASA POWER's marker for missing values


def clean_numeric(col_name: str) -> Column:
    x = F.col(col_name).cast("double")
    return F.when(x <= MISSING_SENTINEL, None).otherwise(x)


def doy_to_date(year_col: str = "YEAR", doy_col: str = "DOY") -> Column:
    return F.expr(
        f"date_add(make_date(CAST({year_col} AS INT), 1, 1), CAST({doy_col} AS INT) - 1)"
    )


def weather_rules() -> dict:
    return {
        "unknown_district":     F.col("_known").isNull(),
        "missing_date":         F.col("date").isNull(),
        "rain_out_of_range":    ~F.col("precip_mm").between(0, 500),
        "temp_out_of_range":    ~F.col("tmax_c").between(-10, 55),
        "tmax_below_tmin":      F.col("tmax_c") < F.col("tmin_c"),
        "soil_wetness_invalid": ~F.col("root_soil_wetness").between(0, 1),
    }


def failed_rules(rules: dict) -> Column:
    return F.concat_ws(", ", *[F.when(cond, F.lit(name)) for name, cond in rules.items()])