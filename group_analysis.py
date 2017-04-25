from __future__ import print_function
from collections import defaultdict
from cosine_sim import cosine_sim
from numpy import mean as avg
from modules.amazon_parser import *

review_objects = parserJSON('./library/amazon-review-data.json')
products_dict = get_products(review_objects)

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


def GTW(group):
   return max([prod_TW(reviews) for product, reviews in group])

def prod_TW(reviews):
   GTW_MAXTIME = 345600 # number of seconds in 4 days
   timestamps = [float(review["Date"]) for review in reviews]
   _range = max(timestamps)-min(timestamps)
   return 1-_range/GTW_MAXTIME if _range < GTW_MAXTIME else 0

def GCS(group):
   return max([CS(reviews) for product, reviews in group])

def CS(reviews):
   texts = [review["reviewText"] for review in reviews]
   return avg([cosine_sim(review1, review2) for review1 in texts for review2 in texts])

def GETF(group):
   return max([GTF(product, reviews) for product, reviews in group])

def GTF(product, reviews):
   GTF_MAXTIME = 15552000 # seconds in 6 months
   earliest_product_review = min([float(review["Date"]) for review in products_dict[product]])
   latest_group_review = max([float(review["Date"]) for review in reviews])
   _range = latest_group_review-earliest_product_review
   return 1-_range/GTF_MAXTIME if _range < GTF_MAXTIME else 0
   
def score(group):
   return GCS(group)+GTW(group)+GETF(group)

groups = organize_by_product(groups)
groups_score = sorted( [ ( group, score(group) ) for group in groups], key=lambda x: x[1], reverse=True)

print(groups_score[0][1])
with open("fake_team.txt", "w") as f:
   f.write(repr(groups_score[0]))


# print sz of groups
# sz = defaultdict(int)
# for groupId, group in groups.items():
#    sz[len(group)] += 1
# print(sz)