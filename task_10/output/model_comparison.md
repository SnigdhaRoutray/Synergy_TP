# Model Comparison

## Regression
Target: CO(GT), the true carbon monoxide concentration. This is a valid continuous
target because it is a real, physically measured number that changes smoothly, not
a category.

The linear regression model clearly beats the baseline. RMSE dropped from 1.42 (baseline)
to 0.56 (model), and R² went from -0.0002 (baseline, essentially no explanatory power)
to 0.85 (model). This means the model explains about 85% of the variation in CO(GT)
using the sensor and weather readings, while the baseline (always guessing the average)
explains almost none of it. The scatter plot backs this up — predictions track the
actual values closely, with more spread only at the highest pollution spikes.

| Metric | Model | Baseline |
|---|---|---|
| MAE | 0.34 | 1.09 |
| MSE | 0.31 | 2.02 |
| RMSE | 0.56 | 1.42 |
| R² | 0.85 | -0.0002 |

## Classification
Target: "high CO" vs "low CO", created by splitting CO(GT) at its median value in the
training data. Rows above the median are labeled 1 (high), rows at or below are labeled 0 (low).

The logistic regression model strongly outperforms the baseline. Accuracy went from
50.5% (baseline, just guessing the majority class) to 91.4% (model). The baseline
scores 0 on precision, recall, and F1 because it always predicts one single class,
so it never predicts the other class at all. The model's precision (0.92) and recall
(0.90) are close to each other, meaning it isn't strongly biased toward false alarms
or missed detections — it's fairly balanced in both directions.

| Metric | Model | Baseline |
|---|---|---|
| Accuracy | 0.91 | 0.50 |
| Precision | 0.92 | 0.00 |
| Recall | 0.90 | 0.00 |
| F1 | 0.91 | 0.00 |

Confusion matrix: 488 true negatives, 38 false positives, 52 false negatives, 464 true positives.

## Which classification error is worse
A false negative (predicting "low CO" when it's actually "high CO") is more serious than
a false positive here, because it means a real pollution spike goes undetected. In an
air-quality warning system, missing a spike is worse than raising an unnecessary alert.
In this run there were 52 false negatives against 38 false positives — a small gap, but
worth watching if this model were used for actual alerts.

## Clustering
Features used: the five PT08 sensor voltages, temperature, relative humidity, and
absolute humidity, all standardized. The CO(GT) label (or any label) is deliberately
left out, because clustering is meant to find groups based on natural similarity in
the data, not to reproduce a label we already know.

The silhouette score came out at 0.28, which is moderate — the clusters exist and are
somewhat separated, but there's real overlap between them, not sharp, clean boundaries.
Cluster sizes are fairly balanced (1995, 2241, 2705 points), so no single cluster is
dominating. Looking at the plot, the split lines up closely with temperature rather
than any clear air-quality signal, which suggests the clusters are mostly capturing
weather patterns (like day/season temperature swings) rather than distinct pollution
regimes.

## Data leakage risks
1. Using CO(GT) as a feature in the classification task, since the label is derived
   directly from it.
2. Using NOx(GT) or NO2(GT) as regression features, since these are also lab-measured
   ground truth values that a cheap sensor system wouldn't normally have available.
3. Standardizing features using the full dataset's mean and standard deviation instead
   of only the training set's, which would let information from the test set leak into
   training.

## Is the dataset ready for stronger models
The regression and classification results here are already strong (R² of 0.85, accuracy
of 91%), so the linear/logistic baselines are doing a solid job — a more complex model
might squeeze out a bit more, especially at the high-pollution outliers the regression
model struggles with, but the improvement may not be dramatic. The clustering result
(silhouette 0.28) is weaker and might benefit more from trying a different number of
clusters or a different algorithm, since the current split seems to be picking up
weather rather than pollution structure.