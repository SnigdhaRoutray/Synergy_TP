# Feature Dictionary

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
