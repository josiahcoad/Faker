import math
from collections import defaultdict
def cosine_sim(string1, string2):
   count1 = defaultdict(int)
   count2 = defaultdict(int)
   for word in string1:
      count1[word.lower()] += 1
   for word in string2:
      count2[word.lower()] += 1
   dot_product = sum(count1.get(key, 0)*count2.get(key, 0) for key in count1)
   magnitude = math.sqrt(sum([val**2 for key, val in count1.items()])) * math.sqrt(sum([val**2 for key, val in count2.items()]))
   return dot_product/magnitude if magnitude else 0