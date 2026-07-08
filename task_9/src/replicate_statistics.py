import pandas as pd
import numpy as np
from scipy.stats import t


def load_data(file_path: str):
    return pd.read_csv(file_path)


def calculate_replicate_statistics(df):
    group_columns = [
        "domain",
        "condition",
        "input_type",
        "input_value",
        "input_unit",
        "signal_unit"
    ]
    grouped = df.groupby(group_columns)
    summary_rows = []
    for name, group in grouped:
        signals = group["signal"].dropna()
        n = len(signals)
        mean_signal = signals.mean()
        median_signal = signals.median()
        minimum_signal = signals.min()
        maximum_signal = signals.max()
        if n >= 2:
            variance = signals.var(ddof=1)
            std = signals.std(ddof=1)
            se = std / np.sqrt(n)
            ci_lower, ci_upper = calculate_confidence_interval(mean_signal, std, n)
        else:
            variance = np.nan
            std = np.nan
            se = np.nan
            ci_lower = np.nan
            ci_upper = np.nan
        if mean_signal != 0 and not pd.isna(std):
            cv = std / mean_signal
        else:
            cv = np.nan
        stability = assign_stability_flag(cv)
        row = dict(zip(group_columns, name))
        row["replicate_count"] = n
        row["mean_signal"] = mean_signal
        row["median_signal"] = median_signal
        row["variance_signal"] = variance
        row["standard_deviation_signal"] = std
        row["standard_error_signal"] = se
        row["confidence_interval_lower"] = ci_lower
        row["confidence_interval_upper"] = ci_upper
        row["coefficient_of_variation"] = cv
        row["minimum_signal"] = minimum_signal
        row["maximum_signal"] = maximum_signal
        row["stability_flag"] = stability
        summary_rows.append(row)
    summary_df = pd.DataFrame(summary_rows)
    return summary_df


def calculate_confidence_interval(mean: float, std: float, n: int) -> tuple[float, float]:
    if n < 2 or pd.isna(std):
        return (np.nan, np.nan)
    standard_error = std / np.sqrt(n)
    t_value = t.ppf(0.975, df=n - 1)
    margin = t_value * standard_error
    lower = mean - margin
    upper = mean + margin
    return (lower, upper)


def assign_stability_flag(coefficient_of_variation: float) -> str:
    if pd.isna(coefficient_of_variation):
        return "unknown"
    if coefficient_of_variation <= 0.05:
        return "stable"
    elif coefficient_of_variation <= 0.15:
        return "moderate"
    else:
        return "unstable"


def round_numeric_columns(df, decimals=6):
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].round(decimals)
    return df


def save_replicate_summary(summary_df, output_path: str):
    summary_df = round_numeric_columns(summary_df)
    summary_df.to_csv(output_path, index=False)