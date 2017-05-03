from __future__ import print_function
#from SOM_Trianing import som
import numpy as np
from group_analysis import *

from grouping import group_users
from modules.amazon_parser import *
with open("./library/groups_temp.txt") as f:
    groups = eval(f.read())

print("reached before X")
X = np.array(get_all_scores())

# Training the SOM
# We will use MiniSom 1.0
from minisom import MiniSom
som = MiniSom(x = 10, y = 10, input_len = 9, sigma = 1.0, learning_rate = 0.5)
som.random_weights_init(X)
som.train_random(data = X, num_iteration = 10)


som_distance = som.distance_map().T
#print('som map', som_distance)

print("reached before mappings")
# Detecting the fake groups and reviewers
mappings = som.win_map(X)
print('size of the SOM map', len(mappings))
text_file = open("mappings.txt", "w")
text_file.write("winning map is %s" % mappings)
text_file.close()

# List of fake review group IDs
faker_list = []
for i in xrange(len(som_distance)):
	for j in xrange(len(som_distance[0])):
		if som_distance[i][j] > 0.8:
			fake_groups = mappings[(i,j)]
			for group in fake_groups:
				fake_group_ID = group[0]
				faker_list.append(fake_group_ID)
print('list of fake group IDs is\n', faker_list)

for faker in faker_list:
	print(groups[faker])

'''
# List of fake reviewer IDs
# get the list of fake reviewers
fake_reviewers = group_users()
for g in faker_list:
	set(g[])
set()
'''

# Visualizing the results (SOM in a 2-D plot)
from pylab import bone, pcolor, colorbar, plot, show
bone() # creates a white window
pcolor(som.distance_map().T)
colorbar()
markers = ['o', 's']
colors = ['r', 'g']
show()