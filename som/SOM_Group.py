from __future__ import print_function
from SOM_Trianing import som
import sys
path = "/Users/josiahcoad/Desktop/Coding/Faker"
sys.path.insert(1,path)
import numpy as numpy
from group_analysis_jo import get_all_scores
from collections import defaultdict
from cosine_sim import cosine_sim
from numpy import mean as avg
import json
from group_analysis import *
from modules.amazon_parser import *
with open("./library/groups.txt") as f:
    groups = eval(f.read())


Final_Input = get_all_scores()
somCol = 10
somRow = 10
som = som(input,12,4,somCol,somRow)
ans =som.trainmodel()
print ('trained model is',ans)

#plot mayby distribution
#recalculate super group's indecators




