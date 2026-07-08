# Task 9: Calibration Statistics, Correlation Analysis, and Feature Engineering

## Objective

The objective of this task is to analyze raw domain-style measurement data from Biochemistry, Electronics, and Mechanical experiments and convert it into statistically reliable, machine-learning-ready data. This involves calculating replicate-level statistics, analyzing calibration and correlation behavior between signal and controlled inputs, and engineering domain-valid derived features for a final ML-ready dataset.

---

## Folder Structure

```text
task_9/
│
├── README.md
├── data/
│   └── calibration_measurements.csv
├── output/
│   ├── replicate_summary.csv
│   ├── calibration_summary.csv
│   ├── correlation_summary.csv
│   ├── engineered_features.csv
│   ├── ml_ready_dataset.csv
│   ├── replicate_analysis.md
│   ├── correlation_limitations.md
│   ├── feature_dictionary.md
│   ├── feature_summary.md
│   ├── calibration_curve_biochem.png
│   ├── calibration_curve_electronics.png
│   ├── calibration_curve_mechanical.png
│   └── correlation_signal_input.png
└── src/
    ├── replicate_statistics.py
    ├── correlation_analysis.py
    ├── feature_engineering.py
    └── main.py
```

---

## Required Packages

* Python 3.x
* pandas
* numpy
* scipy
* matplotlib
* scikit-learn

Install the required packages using:

```bash
pip install -r task_9/requirements.txt
```

---

## Setup Instructions

1. Clone the repository.
2. Install the required packages.
3. Ensure the input CSV file is present at:

```text
task_9/data/calibration_measurements.csv
```

4. Run the program from the root directory of the repository.

---

## Run Command

```bash
python task_9/src/main.py task_9/data/calibration_measurements.csv task_9/output
```

---

## Expected Output Files

After successful execution, the following files will be generated inside the `task_9/output/` directory:

```text
task_9/output/
├── replicate_summary.csv
├── calibration_summary.csv
├── correlation_summary.csv
├── engineered_features.csv
├── ml_ready_dataset.csv
├── replicate_analysis.md
├── correlation_limitations.md
├── feature_dictionary.md
├── feature_summary.md
├── calibration_curve_biochem.png
├── calibration_curve_electronics.png
├── calibration_curve_mechanical.png
└── correlation_signal_input.png
```

---

## Implementation Logic

### Replicate Statistics

* Groups the dataset by domain, condition, input type, input value, input unit, and signal unit.
* Calculates mean, median, variance, standard deviation, standard error, confidence interval, coefficient of variation, minimum, and maximum for each group.
* Uses sample variance and sample standard deviation with degrees of freedom equal to n - 1.
* Marks standard deviation, standard error, and confidence interval as unreliable when a group has fewer than two valid replicate readings.
* Assigns a stability flag (stable, moderate, unstable) based on the coefficient of variation.
* Writes the summary to `replicate_summary.csv`.

### Correlation Analysis

* Calculates Pearson and Spearman correlation for five domain-specific relationships: Biochem signal vs concentration, Electronics signal vs load, Electronics signal vs temperature, Mechanical signal vs load, and Mechanical stress vs load.
* Fits a simple linear calibration line between input value and measured signal for each relationship.
* Calculates slope, intercept, R-squared, mean absolute error, and root mean squared error for each fit.
* Generates calibration curve plots (input value vs mean signal with confidence interval error bars) for Biochem, Electronics, and Mechanical.
* Generates a scatter plot of raw signal versus input value.
* Writes the results to `correlation_summary.csv`.

### Feature Engineering

* Calculates rolling average signal using a window size of 3, grouped by domain and condition, ordered by time step.
* Calculates normalized signal as signal divided by baseline signal.
* Calculates power as voltage multiplied by current, valid for Electronics only.
* Calculates error percentage as the difference between signal and expected signal, relative to expected signal.
* Calculates stress ratio as stress divided by reference stress, valid for Mechanical only.
* Leaves domain-invalid features blank instead of forcing a value of zero.
* Assigns an ml_ready flag based on required raw values, domain-applicable engineered features, and replicate stability.
* Writes the results to `engineered_features.csv` and `ml_ready_dataset.csv`.

---

## Summary generated

The program calculates:

* Replicate-level statistics for every measurement group
* Calibration slope, intercept, R-squared, MAE, and RMSE per relationship
* Pearson and Spearman correlation per relationship
* Rolling average, normalized signal, power, error percentage, and stress ratio
* Stability flag per replicate group
* ML-readiness flag per row