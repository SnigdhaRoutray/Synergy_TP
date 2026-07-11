# Error Analysis

## Regression errors
The largest regression errors are likely to happen at extreme CO(GT) values (very
high pollution spikes) since a straight-line model has trouble matching sudden jumps
that don't follow a smooth linear pattern. Sensor drift and missing readings around
those spikes can also throw off predictions.

## Classification errors
Misclassifications are most likely to occur for values close to the median split point,
where "high" and "low" barely differ in real pollution level. A reading just barely
above the median can easily be predicted as "low," and vice versa, since the model has
no way to know the split was exactly at the median.

## Balanced or imbalanced
Because the classification label was created by splitting at the median, the two
classes should be close to balanced (about 50/50) in the training data. This makes
accuracy a fairer metric here than it would be for a naturally imbalanced target.

## Clustering alignment
The clusters found by KMeans are not guaranteed to line up with any real air-quality
category. They may instead reflect broader patterns like temperature and humidity
changes across seasons or times of day, since those features have a strong influence
on the distances KMeans uses.

## Limitations of the baseline models
1. Linear regression assumes a straight-line relationship between sensors and CO(GT),
   which may not capture more complex sensor behavior.
2. Logistic regression uses a single straight decision boundary, so it may struggle
   with rows where classes overlap heavily.
3. KMeans assumes clusters are round and similarly sized, and it is sensitive to the
   random starting points, so results can shift between runs.
4. Missing values were simply dropped rather than estimated, which removes real rows
   and may bias the data toward periods with fewer sensor faults.