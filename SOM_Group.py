from __future__ import print_function
from SOM_Trianing import som
import numpy as np
from group_analysis_jo import get_all_scores
from modules.amazon_parser import *
import collections

with open("./library/groups.txt") as f:
    groups = eval(f.read())


final_input = np.array(get_all_scores())
somCol = 10
somRow = 10
som = som(final_input,100,1.0,somCol,somRow)
ans = som.trainmodel()
print ('trained model is',ans)

text_file = open("Output.txt", "w")
text_file.write("Trained model is %s" % ans)
text_file.close()

# Calculate the Euclidean distance of each group to its winning neuron
for i in xrange(len(final_input)): # 'i' is the group number here (from 0 to the number of groups)
	dist_dict = collections.defaultdict()
	group_dict = collections.defaultdict(list)
	for ans_row_index in xrange(len(ans)):
		for ans_col_index in xrange(len(ans[0])):
			dist = 0.0
			#dist = np.linalg.norm(ans[ans_row_index][ans_col_index] - final_input[i])
			for ele_index in xrange(len(ans[0][0])):
				dist += (ans[ans_row_index][ans_col_index][ele_index] - final_input[i][ele_index])**2
			dist = dist**0.5
			dist_dict[(ans_row_index, ans_col_index, i)] = dist

	win_neuron = min(dist_dict, key = dist_dict.get)
	group_to_assign = win_neuron[2]

	group_dict[ans_row_index, ans_col_index] = group_to_assign

for key, value in group_dict.iteritems():
	print('The winning neuron is ', key, ' and the group associated with it is ', value)


#plot maybe distribution
#recalculate super group's indicators

#def Euclidean_distance(final_input, ans):
#	for






