import sys
import os
import pandas as pd

from replicate_statistics import (
    load_data,
    calculate_replicate_statistics,
    save_replicate_summary
)

from correlation_analysis import (
    calculate_correlations,
    plot_calibration_curve,
    plot_signal_input_scatter
)

from feature_engineering import (
    add_rolling_average,
    add_normalized_signal,
    add_power_feature,
    add_error_percent,
    add_stress_ratio,
    add_ml_readiness_flag,
    save_engineered_features
)


def round_numeric_columns(df, decimals=6):
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].round(decimals)
    return df


def write_replicate_analysis(summary_df, output_folder):
    ci_width = summary_df["confidence_interval_upper"] - summary_df["confidence_interval_lower"]
    stable = summary_df.loc[summary_df["coefficient_of_variation"].idxmin()]
    noisy = summary_df.loc[summary_df["coefficient_of_variation"].idxmax()]
    widest = summary_df.loc[ci_width.idxmax()]
    investigate = summary_df[summary_df["stability_flag"] == "unstable"]
    report = f"""# Replicate Statistics and Measurement Reliability

## Which replicate group is most stable?

- Domain: {stable['domain']}
- Condition: {stable['condition']}
- Input Value: {stable['input_value']} {stable['input_unit']}
- Coefficient of Variation: {stable['coefficient_of_variation']:.4f}

This group has the lowest relative variation, indicating the highest measurement stability.

## Which replicate group is most noisy?

- Domain: {noisy['domain']}
- Condition: {noisy['condition']}
- Input Value: {noisy['input_value']} {noisy['input_unit']}
- Coefficient of Variation: {noisy['coefficient_of_variation']:.4f}

This group shows the greatest variability between repeated measurements.

## Which group has the widest confidence interval?

- Domain: {widest['domain']}
- Condition: {widest['condition']}
- Confidence Interval Width: {ci_width.max():.4f}

A wider confidence interval indicates greater uncertainty in the estimated mean.

## Which group has the highest coefficient of variation?

The highest coefficient of variation belongs to the {noisy['domain']} group under the {noisy['condition']} condition.

## Why is mean alone not enough for judging reliability?

The mean only describes the average value. Two replicate groups can have identical means but very different variability. Standard deviation, confidence interval and coefficient of variation are required to evaluate measurement reliability.

## Why does replicate count affect confidence interval width?

As replicate count increases, uncertainty decreases, making the confidence interval narrower. More repeated measurements produce a more reliable estimate of the true mean.

## Which readings should be investigated before using the data for machine learning?

"""
    if len(investigate) == 0:
        report += "No unstable replicate groups were detected using the selected stability thresholds.\n"
    else:
        report += "The following replicate groups should be investigated:\n\n"
        for _, row in investigate.iterrows():
            report += f"- {row['domain']} | {row['condition']} | {row['input_value']} {row['input_unit']} | CV = {row['coefficient_of_variation']:.4f}\n"
    with open(os.path.join(output_folder, "replicate_analysis.md"), "w") as f:
        f.write(report)


def write_correlation_limitations(correlation_df, output_folder):
    strongest = correlation_df.loc[correlation_df["pearson_correlation"].abs().idxmax()]
    weakest = correlation_df.loc[correlation_df["pearson_correlation"].abs().idxmin()]
    direction = "increases"
    if strongest["slope"] < 0:
        direction = "decreases"
    report = f"""# Calibration Curve and Correlation Analysis

## Does signal increase or decrease with input value?

For the strongest calibration relationship, the signal generally **{direction}** as the input value increases.

## Which domain shows the strongest signal-input relationship?

- Domain: {strongest['domain']}
- Relationship: {strongest['relationship']}
- Pearson Correlation: {strongest['pearson_correlation']:.4f}
- Spearman Correlation: {strongest['spearman_correlation']:.4f}
- R²: {strongest['r_squared']:.4f}

This relationship shows the strongest linear association in the dataset.

## Which domain shows the weakest or noisiest relationship?

- Domain: {weakest['domain']}
- Relationship: {weakest['relationship']}
- Pearson Correlation: {weakest['pearson_correlation']:.4f}
- Spearman Correlation: {weakest['spearman_correlation']:.4f}
- R²: {weakest['r_squared']:.4f}

This relationship is the weakest and may contain higher measurement noise or weaker dependence on the input variable.

## Does high correlation prove causation?

No. Correlation only measures how strongly two variables move together. It does not prove that one variable causes the other.

## Can correlation be trusted with small sample size?

Small sample sizes can produce unstable correlation values that may not represent the true relationship.

## Can correlation miss nonlinear relationships?

Yes. Pearson correlation mainly measures linear relationships. Strong nonlinear patterns may have low Pearson correlation.

## How can outliers affect correlation?

Outliers can significantly change the correlation coefficient, calibration slope, intercept, MAE and RMSE, leading to misleading conclusions.

## How can temperature, load, material type, or experimental condition act as confounding variables?

These variables may influence the measured signal independently of the controlled input, making observed correlations appear stronger or weaker than the true relationship.

## Why should mixed-domain correlation be avoided?

Biochemistry, Electronics and Mechanical measurements represent different physical systems with different units and behaviors. Combining them into a single correlation analysis would produce misleading results.
"""
    with open(os.path.join(output_folder, "correlation_limitations.md"), "w") as f:
        f.write(report)


def write_feature_dictionary(output_folder):
    report = """# Feature Dictionary

## rolling_average_signal

- Formula: Rolling mean of signal using a window size of 3
- Applies To: All domains
- Required Columns: signal, time_step
- Invalid When: Time order is missing or rolling window crosses unrelated conditions
- Usefulness: Reduces random measurement noise before machine learning

## normalized_signal

- Formula: signal / baseline_signal
- Applies To: All domains
- Required Columns: signal, baseline_signal
- Invalid When: baseline_signal is missing or zero
- Usefulness: Allows comparison of measurements collected under different baseline conditions

## power_w

- Formula: voltage_v × current_a
- Applies To: Electronics only
- Required Columns: voltage_v, current_a
- Invalid When: Used for Biochem or Mechanical rows
- Usefulness: Represents electrical power, an important Electronics feature

## error_percent

- Formula: ((signal - expected_signal) / expected_signal) × 100
- Applies To: All domains
- Required Columns: signal, expected_signal
- Invalid When: expected_signal is missing or zero
- Usefulness: Measures calibration accuracy

## stress_ratio

- Formula: stress_mpa / reference_stress_mpa
- Applies To: Mechanical only
- Required Columns: stress_mpa, reference_stress_mpa
- Invalid When: Used outside Mechanical or reference stress is zero
- Usefulness: Normalizes stress measurements between materials

## stability_flag

- Formula: Based on coefficient of variation
- Applies To: All replicate groups
- Required Columns: coefficient_of_variation
- Invalid When: Coefficient of variation cannot be calculated
- Usefulness: Indicates measurement reliability

## ml_ready

- Formula: Boolean flag based on required raw values, domain-applicable engineered features, and replicate stability
- Applies To: All domains
- Required Columns: signal, expected_signal, input_value, domain, condition, normalized_signal, error_percent, and (domain-dependent) power_w or stress_ratio
- Invalid When: Required raw values are missing, a domain-required engineered feature is blank, or the replicate group is unstable
- Usefulness: Identifies rows suitable for machine learning
"""
    with open(os.path.join(output_folder, "feature_dictionary.md"), "w") as f:
        f.write(report)


def write_feature_summary(df, output_folder):
    not_ready = len(df[df["ml_ready"] == False])
    stable = len(df[df["stability_flag"] == "stable"])
    moderate = len(df[df["stability_flag"] == "moderate"])
    unstable = len(df[df["stability_flag"] == "unstable"])
    report = f"""# Feature Engineering Summary

## Which features are general across all domains?

- rolling_average_signal
- normalized_signal
- error_percent
- stability_flag
- ml_ready

These features can be applied across all three domains whenever the required columns are available.

## Which features are domain-specific?

- power_w (Electronics)
- stress_ratio (Mechanical)

These features should only be calculated where they have physical meaning.

## Which rows are not ML-ready and why?

Number of rows not ready for machine learning: {not_ready}

Rows become non-ML-ready when required values are missing or when the replicate group is marked as unstable.

## Which engineered feature is most useful for Electronics?

power_w because it represents the electrical power calculated from voltage and current.

## Which engineered feature is most useful for Mechanical?

stress_ratio because it compares measured stress with the reference stress.

## Which engineered feature is most useful for Biochem?

normalized_signal because it removes baseline differences between measurements.

## Why should invalid domain features be left blank instead of forcing a value?

Blank values indicate that a feature is not applicable. Using zero would incorrectly imply a real measurement and could mislead machine learning models.

## How can feature engineering introduce misleading information?

Incorrect feature engineering can introduce noise, remove important information, create artificial relationships or even leak information from the target variable into the model.

## Stability Summary

Stable Groups: {stable}

Moderate Groups: {moderate}

Unstable Groups: {unstable}
"""
    with open(os.path.join(output_folder, "feature_summary.md"), "w") as f:
        f.write(report)


def main():
    input_file = sys.argv[1]
    output_folder = sys.argv[2]
    os.makedirs(output_folder, exist_ok=True)
    df = load_data(input_file)
    replicate_summary = calculate_replicate_statistics(df)
    save_replicate_summary(replicate_summary, os.path.join(output_folder, "replicate_summary.csv"))
    correlation_summary = calculate_correlations(df)
    correlation_summary = round_numeric_columns(correlation_summary)
    correlation_summary.to_csv(os.path.join(output_folder, "correlation_summary.csv"), index=False)
    fit_columns = correlation_summary[
        ["domain", "relationship", "slope", "intercept", "r_squared", "mae", "rmse"]
    ].rename(columns={
        "slope": "calibration_slope",
        "intercept": "calibration_intercept",
        "r_squared": "calibration_r_squared",
        "mae": "calibration_mae",
        "rmse": "calibration_rmse"
    })
    primary_fits = fit_columns[
        fit_columns["relationship"].isin(["signal vs concentration", "signal vs load"])
    ].drop(columns="relationship")
    calibration_summary = replicate_summary.merge(primary_fits, on="domain", how="left")
    calibration_summary = round_numeric_columns(calibration_summary)
    calibration_summary.to_csv(os.path.join(output_folder, "calibration_summary.csv"), index=False)
    plot_calibration_curve(calibration_summary, "Biochem", os.path.join(output_folder, "calibration_curve_biochem.png"))
    plot_calibration_curve(calibration_summary, "Electronics", os.path.join(output_folder, "calibration_curve_electronics.png"))
    plot_calibration_curve(calibration_summary, "Mechanical", os.path.join(output_folder, "calibration_curve_mechanical.png"))
    plot_signal_input_scatter(df, os.path.join(output_folder, "correlation_signal_input.png"))
    df = df.merge(
        replicate_summary[
            [
                "domain",
                "condition",
                "input_type",
                "input_value",
                "input_unit",
                "signal_unit",
                "stability_flag"
            ]
        ],
        on=[
            "domain",
            "condition",
            "input_type",
            "input_value",
            "input_unit",
            "signal_unit"
        ],
        how="left"
    )
    df = add_rolling_average(df)
    df = add_normalized_signal(df)
    df = add_power_feature(df)
    df = add_error_percent(df)
    df = add_stress_ratio(df)
    df = add_ml_readiness_flag(df)
    save_engineered_features(df, os.path.join(output_folder, "engineered_features.csv"))
    df = round_numeric_columns(df)
    df.to_csv(os.path.join(output_folder, "ml_ready_dataset.csv"), index=False)
    write_replicate_analysis(replicate_summary, output_folder)
    write_correlation_limitations(correlation_summary, output_folder)
    write_feature_dictionary(output_folder)
    write_feature_summary(df, output_folder)

if __name__ == "__main__":
    main()