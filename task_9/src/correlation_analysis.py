import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

def calculate_correlations(df):
    relationships = [
        ("Biochem", "signal vs concentration", "input_value", "signal"),
        ("Electronics", "signal vs load", "input_value", "signal"),
        ("Electronics", "signal vs temperature", "temperature_c", "signal"),
        ("Mechanical", "signal vs load", "input_value", "signal"),
        ("Mechanical", "stress vs load", "input_value", "stress_mpa"),
    ]

    results = []
    for domain, relationship, x_col, y_col in relationships:
        data = df[df["domain"] == domain][[x_col, y_col]].dropna()
        if len(data) < 2:
            continue

        pearson = pearsonr(data[x_col], data[y_col])[0]
        spearman = spearmanr(data[x_col], data[y_col])[0]

        fit_data = data.rename(columns={x_col: "input_value", y_col: "signal"})
        slope, intercept, r2, mae, rmse = calculate_fit_metrics(fit_data)

        results.append({
            "domain": domain,
            "relationship": relationship,
            "samples": len(data),
            "pearson_correlation": pearson,
            "spearman_correlation": spearman,
            "slope": slope,
            "intercept": intercept,
            "r_squared": r2,
            "mae": mae,
            "rmse": rmse
        })

    return pd.DataFrame(results)

def fit_calibration_line(df):
    x = df[["input_value"]]
    y = df["signal"]
    model = LinearRegression()
    model.fit(x, y)
    return model

def calculate_fit_metrics(df):
    if len(df) < 2:
        return np.nan, np.nan, np.nan, np.nan, np.nan
    model = fit_calibration_line(df)
    x = df[["input_value"]]
    y = df["signal"]
    predictions = model.predict(x)
    slope = model.coef_[0]
    intercept = model.intercept_
    r_squared = model.score(x, y)
    mae = mean_absolute_error(y, predictions)
    rmse = np.sqrt(mean_squared_error(y, predictions))
    return slope, intercept, r_squared, mae, rmse

def plot_calibration_curve(summary_df, domain, output_path):
    data = summary_df[summary_df["domain"] == domain]
    if len(data) == 0:
        return
    plt.figure(figsize=(6, 4))
    error = data["confidence_interval_upper"] - data["mean_signal"]
    plt.errorbar(
        data["input_value"],
        data["mean_signal"],
        yerr=error,
        fmt="o",
        capsize=5
    )
    plt.plot(
        data["input_value"],
        data["mean_signal"]
    )
    plt.xlabel("Input Value")
    plt.ylabel("Mean Signal")
    plt.title(domain + " Calibration Curve")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_signal_input_scatter(df, output_path):
    plt.figure(figsize=(7, 5))
    for domain in df["domain"].unique():
        temp = df[df["domain"] == domain]
        plt.scatter(
            temp["input_value"],
            temp["signal"],
            label=domain
        )
    plt.xlabel("Input Value")
    plt.ylabel("Signal")
    plt.title("Signal vs Input Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()