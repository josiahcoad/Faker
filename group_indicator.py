from modules.amazon_parser import *
from __future__ import print_function
from collections import defaultdict
from cosine_sim import cosine_sim
from numpy import mean as avg
with open("./library/groups.txt") as f:
   groups = eval(f.read())
