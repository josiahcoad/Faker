from __future__ import print_function
from collections import defaultdict
from cosine_sim import cosine_sim
from numpy import mean as avg
from modules.amazon_parser import *


MAX_USERS_IN_GROUP = 5 # found previously
MAX_PRODS_IN_GROUP = 7 # found previously
SIX_MONTHS = 15552000 # seconds in 6 months, used in GETF
FOUR_DAYS = 345600 # number of seconds in 4 days


review_objects = parserJSON('./library/amazon-review-data-modified.json')

products_dict  = get_products(review_objects) # create a dict with product ID as the key and a list of the product's reviews as the value

with open("./library/groups_chia.txt") as f:
   groups = eval(f.read())

groups_by_products = organize_by_product(groups)

groups_by_reviewers = organize_by_user(groups)

# Group Deviation (GD)
def GD(group_by_products):
  return max([D(product, reviews) for product, reviews in group_by_products])

def D(product, reviews):
  group_prod_rate = reviews[0]["Rate"]
  avg_prod_rate = avg([review["Rate"] for review in products_dict[product]])
  return abs(group_prod_rate - avg_prod_rate) / 4.0

# Group Member Content Similarity (GMCS)
def GMCS(groups_by_reviewers):
  return sum([MS(reviews) for reviewer, reviews in groups_by_reviewers]) / len(groups_by_reviewers)

def MS(reviews):
  texts = [review["reviewText"] for review in reviews]
  return avg([cosine_sim(review1, review2) for review1 in texts for review2 in texts])

# Group Size (GS) (number of users in group)
def GS(group_by_users):
    return float(len(group_by_users)) / MAX_USERS_IN_GROUP

# Group Size Ratio (GSR) (returns 1 if each product in the group were only reviewed by the group members)
def GSR(group_by_products):
  return avg ( [gsr(product, reviews) for product, reviews in group_by_products] )

def gsr(product, reviews):
  return float(len(reviews)) / len(products_dict[product])
# ------------------------

def GTW(group):
   return max([prod_TW(reviews) for product, reviews in group])

def prod_TW(reviews):
   timestamps = [float(review["Date"]) for review in reviews]
   _range = max(timestamps)-min(timestamps)
   return 1-_range/FOUR_DAYS if _range <= FOUR_DAYS else 0

def GCS(group):
   return max([CS(reviews) for product, reviews in group])

def CS(reviews):
   texts = [review["reviewText"] for review in reviews]
   return avg([cosine_sim(review1, review2) for review1 in texts for review2 in texts])

def GETF(group):
   return max([GTF(product, reviews) for product, reviews in group])

def GTF(product, reviews):
   earliest_product_review = min([float(review["Date"]) for review in products_dict[product]])
   latest_group_review = max([float(review["Date"]) for review in reviews])
   _range = latest_group_review-earliest_product_review
   return 1-_range/SIX_MONTHS if _range <= SIX_MONTHS else 0

# Group Support Count (GSUP) (number of products in group)
def GSUP(group):
  return float(len(group)) / MAX_PRODS_IN_GROUP

# Sum Scores
def scores(gbp, gbr):
   return [GCS(gbp), GTW(gbp), GETF(gbp), GSUP(gbp), GS(gbr), GSR(gbp), GD(gbp), GMCS(gbr)]


def get_all_scores():
  all_scores = []
  for i in range(len(groups_by_reviewers)):
     all_scores.append(scores(groups_by_products[i], groups_by_reviewers[i]))
  return all_scores

# scores = [( i, sum(score) ) for i, score in enumerate(get_all_scores())]
# fakest_indexes = sorted(scores, lambda k: k[1], reverse=True)
# for top in fakest_indexes[:5]:
#   fakest_users = [reviewer for reviewer, review in groups_by_reviewers[fakest_index]]
#   print(fakest_users)
with open("scores.txt", "w") as file:
  file.write(repr(get_all_scores()))

# for s in all_scores:
#   print("GCS: %.5f, GTW: %.5f, GETF: %.5f, GSUP: %.5f, GS: %.5f, GSR: %.5f, GD: %.5f, GMCS %.5f"%(s))
# sorted(groups_score, key=lambda x: sum(x[1]), reverse=True)



# print sz of groups
# sz = defaultdict(int)
# for groupId, group in groups.items():
#    sz[len(group)] += 1
