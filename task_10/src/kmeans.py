import numpy as np

class KMeans:
    def __init__(self, n_clusters=3, iterations=100, seed=42):
        self.n_clusters = n_clusters
        self.iterations = iterations
        self.seed = seed
        self.centroids = None

    def fit(self, X):
        rng = np.random.default_rng(self.seed)
        indices = rng.choice(len(X), self.n_clusters, replace=False)
        self.centroids = X[indices]
        labels = self.predict(X)
        for _ in range(self.iterations):
            labels = self.predict(X)
            new_centroids = np.array([
                X[labels == i].mean(axis=0) if np.any(labels == i) else self.centroids[i]
                for i in range(self.n_clusters)
            ])
            if np.allclose(new_centroids, self.centroids):
                self.centroids = new_centroids
                break
            self.centroids = new_centroids
        return labels

    def predict(self, X):
        distances = np.array([np.linalg.norm(X - c, axis=1) for c in self.centroids])
        return np.argmin(distances, axis=0)