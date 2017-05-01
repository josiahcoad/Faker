from spam_reviewers import *
from sklearn.cluster import KMeans
import numpy as np

training_data = construct_feature_vector()

X = np.array(training_data.values())
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
predictions = kmeans.predict(X)
count_0 = 0
count_1 = 0
for i in range(len(predictions)):
	if predictions[i] == 0:
		count_0 += 1
	if predictions[i] == 1:
		count_1 += 1
	print predictions[i], training_data.keys()[i], training_data.values()[i]

print count_1
print count_0

