from __future__ import print_function
from collections import defaultdict
from cosine_sim import cosine_sim
from numpy import mean as avg
from modules.amazon_parser import *

review_objects = parserJSON('./library/amazon-review-data.json')
<<<<<<< HEAD
products_dict  = get_products(review_objects) # create a dict with product ID as the key and a list of the product's reviews as the value
print("len products_dict", len(products_dict))
=======
products_dict = get_products(review_objects) # create a dict with product ID as the key and a list of the product's reviews as the value

>>>>>>> chia
MAX_USERS = 5 # found previously
MAX_PRODS = 7 # found previously


with open("./library/groups.txt") as f:
   groups = eval(f.read())

# takes a dictionary of groups which are organized by groupID as the key and a list of tuples as the value
# return a list of groups where each group is structured as: [(product, [reviews]), (product, [reviews])]
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

groups_by_products = organize_by_product(groups)

<<<<<<< HEAD
print("len groups_by_products", len(groups_by_products))
=======
>>>>>>> chia
# takes a dictionary of groups which are organized by groupID as the key and a list of tuples as the value
# return a list of groups where each group is structured as: [(reviewer, [reviews]), (reviewer, [reviews])]
def organize_by_user(groups_dict):
   return [groups_dict[key] for key in groups_dict]

groups_by_reviewers = organize_by_user(groups)
<<<<<<< HEAD
print("len groups_by_reviewers", len(groups_by_reviewers))
=======

>>>>>>> chia

def get_avg(Name):
    if(len(products_dict[Name])>0):
        count = 0
        sum = 0
        for i in range(len(products_dict[Name])):
            sum+= products_dict[Name][i]["Rate"]
            count+=1
        return float(sum/count)
    else:
        return 0

# Group Deviation (GD)
def GD(group):
    Deviation = []
    handle = set()
    for i in range(len(group)):
        cur_user = group[i]
        for item in cur_user[1]:
            if(item["productId"] not in handle):
                handle.add(item["productId"])
                if(item["Rate"]==5):
                    Deviation.append(abs(5-get_avg(item["productId"]))/4)
                elif(cur_user[1][1]["Rate"]==1):
                    Deviation.append(abs(get_avg(item["productId"])-1)/4)
    return max(Deviation)

# Group Member Content Similarity
def GMCS(group):
  MCS = []
  count = []
  for i in range(len(group)):
    cur_user = group[i]
    MCS.append(0)
    count.append(0)
    for x in range(len(cur_user[1])-1):#each review
      for y in range(x+1,len(cur_user[1])):
        MCS[i]+=cosine_sim(cur_user[1][x]["reviewText"], cur_user[1][y]["reviewText"])    
        count[i]+=1 
    MCS[i]/=count[i]
  Sum = 0
  for indi in MCS:
    Sum+=indi
  return float(Sum)/len(group)

# Group Size (GS) (number of users in group)
def GS(group_by_users):
    return float(len(group_by_users)) / MAX_USERS

# Group Size Ratio (GSR) (returns 1 if each product in the group were only reviewed by the group members)
def GSR(group_by_products):
  return avg ( [gsr(product, reviews) for product, reviews in group_by_products] )

def gsr(product, reviews):
  return float(len(reviews)) / len(products_dict[product])
# ------------------------

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

# Group Support Count (GSUP) (number of products in group)
def GSUP(group):
  return float(len(group)) / MAX_PRODS

# Sum Scores
def scores(gbp, gbr):
   return [GCS(gbp), GTW(gbp), GETF(gbp), GSUP(gbp), GS(gbr), GSR(gbp), GD(gbr), GMCS(gbr)]


def get_all_scores():
  all_scores = []
  for i in range(len(groups_by_reviewers)):
     all_scores.append(scores(groups_by_products[i], groups_by_reviewers[i]))
  return all_scores

<<<<<<< HEAD
# get_all_scores()
=======
>>>>>>> chia

# for s in all_scores:
#   print("GCS: %.5f, GTW: %.5f, GETF: %.5f, GSUP: %.5f, GS: %.5f, GSR: %.5f, GD: %.5f, GMCS %.5f"%(s))
# sorted(groups_score, key=lambda x: sum(x[1]), reverse=True)



# print sz of groups
# sz = defaultdict(int)
# for groupId, group in groups.items():
#    sz[len(group)] += 1
<<<<<<< HEAD
# print(sz)t)
# for groupId, group in groups.items():
#    sz[len(group)] += 1
=======
>>>>>>> chia
# print(sz)