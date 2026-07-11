import pandas as pd
import numpy as np

def load_data(path):
    df = pd.read_csv(path, sep=';', decimal=',')
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    return df

def clean_data(df):
    df = df.replace(-200, np.nan)
    df = df.drop(columns=['NMHC(GT)'], errors='ignore')
    df = df.dropna()
    return df

def train_val_test_split(X, y, train_ratio=0.7, val_ratio=0.15, seed=42):
    n = len(X)
    rng = np.random.default_rng(seed)
    indices = rng.permutation(n)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    train_idx = indices[:train_end]
    val_idx = indices[train_end:val_end]
    test_idx = indices[val_end:]
    return X[train_idx], y[train_idx], X[val_idx], y[val_idx], X[test_idx], y[test_idx]

def standardize(X_train, X_val, X_test):
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    std[std == 0] = 1
    X_train_scaled = (X_train - mean) / std
    X_val_scaled = (X_val - mean) / std
    X_test_scaled = (X_test - mean) / std
    return X_train_scaled, X_val_scaled, X_test_scaled