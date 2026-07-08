import pandas as pd
import numpy as np


def add_rolling_average(df):
    df = df.sort_values(["domain", "condition", "time_step"])
    df["rolling_average_signal"] = (
        df.groupby(["domain", "condition"])["signal"]
        .rolling(window=3, min_periods=1)
        .mean()
        .reset_index(level=[0, 1], drop=True)
    )
    return df


def add_normalized_signal(df):
    df["normalized_signal"] = df["signal"] / df["baseline_signal"]
    df.loc[df["baseline_signal"].isna(), "normalized_signal"] = np.nan
    df.loc[df["baseline_signal"] == 0, "normalized_signal"] = np.nan
    return df


def add_power_feature(df):
    df["power_w"] = df["voltage_v"] * df["current_a"]
    df.loc[df["domain"] != "Electronics", "power_w"] = np.nan
    return df


def add_error_percent(df):
    df["error_percent"] = ((df["signal"] - df["expected_signal"]) / df["expected_signal"]) * 100
    df.loc[df["expected_signal"].isna(), "error_percent"] = np.nan
    df.loc[df["expected_signal"] == 0, "error_percent"] = np.nan
    return df


def add_stress_ratio(df):
    df["stress_ratio"] = df["stress_mpa"] / df["reference_stress_mpa"]
    df.loc[df["domain"] != "Mechanical", "stress_ratio"] = np.nan
    df.loc[df["reference_stress_mpa"].isna(), "stress_ratio"] = np.nan
    df.loc[df["reference_stress_mpa"] == 0, "stress_ratio"] = np.nan
    return df


def add_ml_readiness_flag(df):
    ml_ready = (
        df["signal"].notna()
        & df["expected_signal"].notna()
        & df["input_value"].notna()
        & df["domain"].notna()
        & df["condition"].notna()
    )
    if "normalized_signal" in df.columns:
        ml_ready &= df["normalized_signal"].notna()
    if "error_percent" in df.columns:
        ml_ready &= df["error_percent"].notna()
    if "power_w" in df.columns:
        is_electronics = df["domain"] == "Electronics"
        power_missing_where_required = is_electronics & df["power_w"].isna()
        ml_ready &= ~power_missing_where_required
    if "stress_ratio" in df.columns:
        is_mechanical = df["domain"] == "Mechanical"
        stress_missing_where_required = is_mechanical & df["stress_ratio"].isna()
        ml_ready &= ~stress_missing_where_required
    if "stability_flag" in df.columns:
        ml_ready &= df["stability_flag"] != "unstable"
    df["ml_ready"] = ml_ready
    return df


def round_numeric_columns(df, decimals=6):
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].round(decimals)
    return df


def save_engineered_features(df, output_path):
    df = round_numeric_columns(df)
    df.to_csv(output_path, index=False)