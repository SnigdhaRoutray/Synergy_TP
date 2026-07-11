# Task 10: Baseline Machine Learning from Scratch (AirQualityUCI)

## Objective
This project implements a full baseline ML workflow — regression, classification,
and clustering — entirely from scratch in NumPy, without scikit-learn or any other
ready-made ML library.

## Dataset
UCI Machine Learning Repository: Air Quality Data Set (AirQualityUCI).

## Models implemented
- Linear Regression (gradient descent)
- Logistic Regression (gradient descent)
- KMeans clustering
- Mean baseline (regression)
- Majority-class baseline (classification)

## Outputs generated
- regression_metrics.json, classification_metrics.json, clustering_metrics.json
- regression_predictions.csv, classification_predictions.csv, clustering_assignments.csv
- regression_loss_curve.png, classification_loss_curve.png
- actual_vs_predicted.png, confusion_matrix.png, clustering_plot.png
- model_comparison.md, error_analysis.md

## How to run
```
python task_10/src/main.py task_10/data/AirQualityUCI.csv task_10/output
```
## What each output file contains
- **regression_metrics.json** - MAE, MSE, RMSE, R² for the model and the mean baseline
- **classification_metrics.json** - accuracy, precision, recall, F1, confusion matrix
- **clustering_metrics.json** - inertia, silhouette score, cluster sizes
- **regression_predictions.csv** - actual vs predicted CO(GT) on the test set
- **classification_predictions.csv** - actual vs predicted class on the test set
- **clustering_assignments.csv** - cluster number assigned to every row
- **regression_loss_curve.png** - training loss over gradient descent iterations
- **classification_loss_curve.png** - training loss over gradient descent iterations
- **actual_vs_predicted.png** - scatter plot of regression performance
- **confusion_matrix.png** - visual confusion matrix
- **clustering_plot.png** - 2D view of the clusters
- **model_comparison.md** - how each model did against its baseline
- **error_analysis.md** - where and why the models went wrong

## Confirmation
No scikit-learn or any other ready-made ML library was used anywhere in this project.
All models and metrics are implemented by hand in NumPy.