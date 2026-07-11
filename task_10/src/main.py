import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data_utils import load_data, clean_data, train_val_test_split, standardize
from metrics import mae, mse, rmse, r_squared, accuracy, precision, recall, f1_score, confusion_matrix, inertia, silhouette_score
from baselines import mean_baseline_predict, majority_baseline_predict
from linear_regression_gd import LinearRegressionGD
from logistic_regression_gd import LogisticRegressionGD
from kmeans import KMeans

FEATURE_COLS = ['PT08.S1(CO)', 'PT08.S2(NMHC)', 'PT08.S3(NOx)', 'PT08.S4(NO2)', 'PT08.S5(O3)', 'T', 'RH', 'AH']

def run_regression(df, output_dir):
    X = df[FEATURE_COLS].values
    y = df['CO(GT)'].values
    X_train, y_train, X_val, y_val, X_test, y_test = train_val_test_split(X, y)
    X_train, X_val, X_test = standardize(X_train, X_val, X_test)
    model = LinearRegressionGD(learning_rate=0.05, iterations=500)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    baseline_pred = mean_baseline_predict(y_train, len(y_test))
    metrics = {
        'model_mae': float(mae(y_test, y_pred)),
        'model_mse': float(mse(y_test, y_pred)),
        'model_rmse': float(rmse(y_test, y_pred)),
        'model_r2': float(r_squared(y_test, y_pred)),
        'baseline_mae': float(mae(y_test, baseline_pred)),
        'baseline_mse': float(mse(y_test, baseline_pred)),
        'baseline_rmse': float(rmse(y_test, baseline_pred)),
        'baseline_r2': float(r_squared(y_test, baseline_pred))
    }
    with open(f'{output_dir}/regression_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    pd.DataFrame({'actual': y_test, 'predicted': y_pred}).to_csv(f'{output_dir}/regression_predictions.csv', index=False)
    plt.figure()
    plt.plot(model.loss_history)
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.title('Regression Loss Curve')
    plt.savefig(f'{output_dir}/regression_loss_curve.png')
    plt.close()
    plt.figure()
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('Actual vs Predicted CO(GT)')
    plt.savefig(f'{output_dir}/actual_vs_predicted.png')
    plt.close()
    return metrics

def run_classification(df, output_dir):
    threshold = df['CO(GT)'].median()
    y = (df['CO(GT)'] > threshold).astype(int).values
    X = df[FEATURE_COLS].values
    X_train, y_train, X_val, y_val, X_test, y_test = train_val_test_split(X, y)
    X_train, X_val, X_test = standardize(X_train, X_val, X_test)
    model = LogisticRegressionGD(learning_rate=0.1, iterations=500)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    baseline_pred = majority_baseline_predict(y_train, len(y_test))
    cm = confusion_matrix(y_test, y_pred)
    metrics = {
        'model_accuracy': float(accuracy(y_test, y_pred)),
        'model_precision': float(precision(y_test, y_pred)),
        'model_recall': float(recall(y_test, y_pred)),
        'model_f1': float(f1_score(y_test, y_pred)),
        'baseline_accuracy': float(accuracy(y_test, baseline_pred)),
        'baseline_precision': float(precision(y_test, baseline_pred)),
        'baseline_recall': float(recall(y_test, baseline_pred)),
        'baseline_f1': float(f1_score(y_test, baseline_pred)),
        'confusion_matrix': cm.tolist()
    }
    with open(f'{output_dir}/classification_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    pd.DataFrame({'actual': y_test, 'predicted': y_pred}).to_csv(f'{output_dir}/classification_predictions.csv', index=False)
    plt.figure()
    plt.plot(model.loss_history)
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.title('Classification Loss Curve')
    plt.savefig(f'{output_dir}/classification_loss_curve.png')
    plt.close()
    plt.figure()
    plt.imshow(cm, cmap='Blues')
    plt.xticks([0, 1], ['Predicted Low', 'Predicted High'])
    plt.yticks([0, 1], ['Actual Low', 'Actual High'])
    for i in range(2):
        for j in range(2):
            plt.text(j, i, cm[i, j], ha='center', va='center')
    plt.title('Confusion Matrix')
    plt.savefig(f'{output_dir}/confusion_matrix.png')
    plt.close()
    return metrics

def run_clustering(df, output_dir):
    X = df[FEATURE_COLS].values
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    X_scaled = (X - mean) / std
    model = KMeans(n_clusters=3, iterations=100)
    labels = model.fit(X_scaled)
    inertia_value = inertia(X_scaled, labels, model.centroids)
    sample_size = min(500, len(X_scaled))
    rng = np.random.default_rng(42)
    sample_idx = rng.choice(len(X_scaled), sample_size, replace=False)
    silhouette_value = silhouette_score(X_scaled[sample_idx], labels[sample_idx])
    cluster_counts = {int(i): int(np.sum(labels == i)) for i in range(3)}
    metrics = {
        'inertia': float(inertia_value),
        'silhouette_score': float(silhouette_value),
        'cluster_counts': cluster_counts
    }
    with open(f'{output_dir}/clustering_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    pd.DataFrame({'cluster': labels}).to_csv(f'{output_dir}/clustering_assignments.csv', index=False)
    plt.figure()
    plt.scatter(df['T'], df['PT08.S1(CO)'], c=labels, cmap='viridis', alpha=0.5)
    plt.xlabel('Temperature')
    plt.ylabel('PT08.S1(CO) Sensor')
    plt.title('Cluster Visualization')
    plt.savefig(f'{output_dir}/clustering_plot.png')
    plt.close()
    return metrics

def main():
    data_path = sys.argv[1]
    output_dir = sys.argv[2]
    df = load_data(data_path)
    df = clean_data(df)
    regression_metrics = run_regression(df, output_dir)
    classification_metrics = run_classification(df, output_dir)
    clustering_metrics = run_clustering(df, output_dir)
    print('Regression:', regression_metrics)
    print('Classification:', classification_metrics)
    print('Clustering:', clustering_metrics)

if __name__ == '__main__':
    main()