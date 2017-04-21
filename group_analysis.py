from __future__ import print_function
from collections import defaultdict
from cosine_sim import cosine_sim
from numpy import mean as avg
with open("./library/groups.txt") as f:
   groups = eval(f.read())

# takes a group which is organized by reviewer_reviews and translates it to product_reviews
def translate_group(group):
   reviews = []
   for user_reviews in group:
      reviews.extend(user_reviews[1])
   products_reviews = defaultdict(list)
   for review in reviews:
      products_reviews[review["productId"]].append(review)
   return products_reviews.items()



MAXTIME = 345600 # number of seconds in 4 days
def GTW(group):
   products_reviews = translate_group(group)
   timewindows = []
   for product_reviews in products_reviews:
      timestamps = [float(review["Date"]) for review in product_reviews[1]]
      timewindows.append(prod_TW(timestamps))
   return max(timewindows)

def prod_TW(timestamps):
   _range = max(timestamps)-min(timestamps)
   return 1-_range/MAXTIME if _range < MAXTIME else 0

def GCS(group):
   products_reviews = translate_group(group)
   cs = []
   for product_reviews in products_reviews:
      reviews = [review["reviewText"] for review in product_reviews[1]]
      cs.append(CS(reviews))
   return max(cs)

def CS(reviews):
   cs = []
   for review in reviews:
      for review2 in reviews:
         cs.append(cosine_sim(review, review2))
   return avg(cs)

for groupId, group in groups.items():
   print(GCS(group))


# print sz of groups
sz = defaultdict(int)
for groupId, group in groups.items():
   sz[len(group)] += 1
print(sz)