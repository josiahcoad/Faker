from spam_reviewers import *
from sklearn.cluster import KMeans
import numpy as np

training_data = construct_feature_vector()[0]
final_training_data = []
for value in training_data.values():
	final_training_data.append(value[1:])
X = np.array(final_training_data)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
predictions = kmeans.predict(X)
count_0 = 0
count_1 = 0
fake_reviewers = []
for i in range(len(predictions)):
	if final_training_data[i][0] < 3:
		predictions[i] = 1
	if predictions[i] == 0:
		count_0 += 1
	if predictions[i] == 1:
		count_1 += 1
	if predictions[i] == 0:
		fake_reviewers.append(training_data.keys()[i])

print fake_reviewers
