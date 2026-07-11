import numpy as np

def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def rmse(y_true, y_pred):
    return np.sqrt(mse(y_true, y_pred))

def r_squared(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - ss_res / ss_tot

def accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)

def precision(y_true, y_pred):
    tp = np.sum((y_pred == 1) & (y_true == 1))
    fp = np.sum((y_pred == 1) & (y_true == 0))
    if tp + fp == 0:
        return 0.0
    return tp / (tp + fp)

def recall(y_true, y_pred):
    tp = np.sum((y_pred == 1) & (y_true == 1))
    fn = np.sum((y_pred == 0) & (y_true == 1))
    if tp + fn == 0:
        return 0.0
    return tp / (tp + fn)

def f1_score(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    if p + r == 0:
        return 0.0
    return 2 * p * r / (p + r)

def confusion_matrix(y_true, y_pred):
    tp = np.sum((y_pred == 1) & (y_true == 1))
    tn = np.sum((y_pred == 0) & (y_true == 0))
    fp = np.sum((y_pred == 1) & (y_true == 0))
    fn = np.sum((y_pred == 0) & (y_true == 1))
    return np.array([[tn, fp], [fn, tp]])

def inertia(X, labels, centroids):
    total = 0.0
    for i in range(len(centroids)):
        points = X[labels == i]
        total += np.sum((points - centroids[i]) ** 2)
    return total

def silhouette_score(X, labels):
    n = len(X)
    scores = np.zeros(n)
    unique_labels = np.unique(labels)
    for i in range(n):
        same_cluster = X[labels == labels[i]]
        a = np.mean(np.linalg.norm(same_cluster - X[i], axis=1)) if len(same_cluster) > 1 else 0
        b = np.inf
        for label in unique_labels:
            if label == labels[i]:
                continue
            other_cluster = X[labels == label]
            dist = np.mean(np.linalg.norm(other_cluster - X[i], axis=1))
            if dist < b:
                b = dist
        if max(a, b) == 0:
            scores[i] = 0
        else:
            scores[i] = (b - a) / max(a, b)
    return np.mean(scores)