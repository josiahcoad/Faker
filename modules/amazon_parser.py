from __future__ import print_function
from collections import defaultdict
# find out how many groups there that meet the following criteria
'''
members reviewed 3 or more of the same products (and no others?)
members reviewed with same star rating (either 5 or 1 star)
members posted within 4 days of eachother
2 or more members
'''

# score of spamicity could be based on the following
'''
>>1. earliness of reviews - Group Early Time Frame (GETF)
2. group deviation (diff between rating from group and non-group members) (GD)
>>>3. group content similarity (similarity between all reviews in the group) (GCS)
4. group member content similarity - for each member in the group, how similar are their own reviews? (GMCS)
>>5. time closeness of reviews - g time window (GTW)
size of group (normalized)
'''

'''
x, y axis of graphs?
how to determine dimensions for cosine similarity in reviews (length? sentiment? exact word use? syntax? mispelling?)
if groups are determined by the "only review these products" rule, than there wont be any two groups who
   share the same reviewers... right?
'''


# returns a list of reviews represented as dict objects.
# put in a number of lines to read from file
# or put in no number and it will read all
def parserJSON(path, numLines=None):
  numLines = numLines or len(open(path).read().split("\n")) - 1
  with open(path) as txt:
    reviews = [eval(next(txt)) for x in range(numLines)]
  print("Number of reviews:", len(reviews))
  return reviews


######
###reviews = parserJSON('./library/amazon-review-data.json',)
######


# create a dict with reviewer ID as key and a list of the reviewers reviews as the value
def get_reviewers(reviews):
   reviewers = {}
   for review in reviews:
      reviewerId = review["memberId"]
      if reviewerId not in reviewers:
         reviewers[reviewerId] = [review]
      else:
         reviewers[reviewerId].append(review)
   print("Number of reviewers:", len(reviewers))
   return reviewers


# filter out reviewers who didn't review more than three products and didn't leave a 1 or 5 star rating
# according to the paper, fraud reviewers will review at least three products to get their money's worth
# and they won't leave anything other than 1 or 5 star reviews.
def filter_reviewers(reviewers):
   final_reviewers = {}
   for reviewer in reviewers:
      if len(reviewers[reviewer]) >= 3:
         # if all(rating == 1 or rating == 5 for review["Rate"] in reviewers[reviewer):
         final_reviewers[reviewer] = reviewers[reviewer]
   print("Number of reviewers after filtering:", len(final_reviewers))
   return final_reviewers


# create a dict with product ID as the key and a list of the product's reviews as the value
def get_products(reviews):
   products = {}
   for review in reviews:
      productId = review["productId"]
      if productId not in products:
         products[productId] = [review]
      else:
         products[productId].append(review)
   return products


# - ADD COMMON-USED FUNCTION HERE

def normalizedVector(vector):
    total = 0
    for key in vector:
        total += vector[key] ** 2
    total = total ** 0.5
    for key in vector:
        vector[key] /= total
    return vector


#reviewers = get_reviewers(reviews)
#busiest = max(reviewers.keys(), key=(lambda key: len(reviewers[key])))

# print(len(reviewers[busiest]))
# busiest = {}
# for r in get_reviewers(reviews):
   # if
