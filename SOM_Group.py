from __future__ import print_function
from SOM_Trianing import som
import numpy as np
from group_analysis import get_all_scores
from modules.amazon_parser import *
with open("./library/groups_chia.txt") as f:
    groups = eval(f.read())


final_input = np.array(get_all_scores())
somCol = 10
somRow = 10
som = som(final_input,12,4,somCol,somRow)
ans =som.trainmodel()
print ('trained model is',ans)



#plot mayby distribution
#recalculate super group's indecators




