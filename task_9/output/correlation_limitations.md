# Calibration Curve and Correlation Analysis

## Does signal increase or decrease with input value?

For the strongest calibration relationship, the signal generally **increases** as the input value increases.

## Which domain shows the strongest signal-input relationship?

- Domain: Biochem
- Relationship: signal vs concentration
- Pearson Correlation: 0.9993
- Spearman Correlation: 0.9487
- R²: 0.9986

This relationship shows the strongest linear association in the dataset.

## Which domain shows the weakest or noisiest relationship?

- Domain: Mechanical
- Relationship: signal vs load
- Pearson Correlation: 0.9841
- Spearman Correlation: 0.9487
- R²: 0.9684

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
