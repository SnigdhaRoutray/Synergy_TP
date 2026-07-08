# Feature Engineering Summary

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

Number of rows not ready for machine learning: 0

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

Stable Groups: 21

Moderate Groups: 6

Unstable Groups: 0
