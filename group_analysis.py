from __future__ import print_function
from collections import defaultdict
from cosine_sim import cosine_sim
from numpy import mean as avg
import json
from modules.amazon_parser import *
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


#products_reviews_traslated = translate_group(groups)


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


def GD(group):
    reviews = parserJSON('./library/amazon-review-data.json')
    product_dict = get_products(reviews)
    


def CS(reviews):
   cs = []
   for review in reviews:
      for review2 in reviews:
         cs.append(cosine_sim(review, review2))
   return avg(cs)



Final_Input = []



i = 0
for groupId, group in groups.items():
    if i < 5:
        print (GTW(group))
        i+=1

print (len(groups.items()[1][1]))
print(groups.items()[1][1])

#for groupId, groupU in groups.items():
#   print (groupId, groupU,'\n')
#print(sz)
