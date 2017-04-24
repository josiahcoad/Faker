from __future__ import print_function
from collections import defaultdict
from cosine_sim import cosine_sim
from numpy import mean as avg
from modules.amazon_parser import *

reviews = parserJSON('./library/amazon-review-data.json')
products_dict = get_products(reviews)

with open("./library/groups.txt") as f:
   groups = eval(f.read())

# takes a dictionary of groups which are organized by groupID as the key and a list of tuples as the value
# returns a list of a list of tuples where internal list is a group and each tuple inside that group is (product, [reviews])
def organize_by_product(groups_dict):
   group_list = []
   for groupId, group in groups_dict.items():
      reviews = []
      for user, user_reviews in group:
         reviews.extend(user_reviews)
      products_reviews = defaultdict(list)
      for review in reviews:
         products_reviews[review["productId"]].append(review)
      group_list.append( products_reviews.items() )
   return group_list

GTW_MAXTIME = 345600 # number of seconds in 4 days
def GTW(group):
   timewindows = []
   for product, reviews in group:
      timestamps = [float(review["Date"]) for review in reviews]
      timewindows.append(prod_TW(timestamps))
   return max(timewindows)

def prod_TW(timestamps):
   _range = max(timestamps)-min(timestamps)
   return 1-_range/GTW_MAXTIME if _range < GTW_MAXTIME else 0

def GCS(group):
   cs = []
   for product, reviews in group:
      reviews = [review["reviewText"] for review in reviews]
      cs.append(CS(reviews))
   return max(cs)

def CS(reviews):
   cs = []
   for review in reviews:
      for review2 in reviews:
         cs.append(cosine_sim(review, review2))
   return avg(cs)

# def GETF(group):
#    products_reviews = translate_group(group)
#    gtf = []
#    for product, reviews in products_reviews:
#       timestamps = [float(review["Date"]) for review in reviews]
#       earliest_time_for_product = min([float(review["Date"]) for review in products_dict[product]])
#       gtf.append(GTF(timestamps, earliest_time))
#    return max(gtf)

def GETF(group):
   return max([GTF(product, reviews) for product, reviews in group])

GTF_MAXTIME = 15552000 # seconds in 6 months
def GTF(product, reviews):
   earliest_product_review = min([float(review["Date"]) for review in products_dict[product]])
   latest_group_review = max([float(review["Date"]) for review in reviews])
   _range = latest_group_review-earliest_product_review
   return 1-_range/GTF_MAXTIME if _range < GTF_MAXTIME else 0
   
groups = organize_by_product(groups)
for group in groups:
   print(GETF(group))



# print sz of groups
# sz = defaultdict(int)
# for groupId, group in groups.items():
#    sz[len(group)] += 1
# print(sz)