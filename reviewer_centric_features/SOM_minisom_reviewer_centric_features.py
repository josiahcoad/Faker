from __future__ import print_function
import numpy as np
from spam_reviewers import *
X = np.array(construct_feature_vector()[0].values())
mapping = construct_feature_vector()[1]

# Training the SOM
# We will use MiniSom 1.0
from minisom import MiniSom
som = MiniSom(x = 10, y = 10, input_len = 5, sigma = 1.0, learning_rate = 0.5)
som.random_weights_init(X)
som.train_random(data = X, num_iteration = 100000)


som_distance = som.distance_map().T

mappings = som.win_map(X)
print('size of the SOM map', len(mappings))
text_file = open("mappings_individual.txt", "w")
text_file.write("winning map is %s" % mappings)
text_file.close()

# List of fake review user IDs
faker_list = []
faker_id = []
for i in xrange(len(som_distance)):
	for j in xrange(len(som_distance[0])):
		if som_distance[i][j] > 0.8:
			fake_reviewers = mappings[(i,j)]
			for user in fake_reviewers:
				faker_id.append(user[0])
				faker_list.append(mapping[user[0]])
print('list of fake user IDs is\n', faker_list)

# Visualizing the results (SOM in a 2-D plot)
from pylab import bone, pcolor, colorbar, plot, show
bone() # creates a white window
pcolor(som.distance_map().T)
colorbar()
markers = ['o', 's']
colors = ['r', 'g']
show()