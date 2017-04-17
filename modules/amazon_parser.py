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


# takes a list of tuples (reviewer, reviews)
# filter out reviewers who did reviewed less than three products which have been rated 1 or 5 star
# according to the paper, fraud reviewers will review at least three products to get their money's worth
def remove_lessthan3(reviewers_reviews):
   final = []
   for reviewer, reviews in reviewers_reviews:
      reviews = list(filter(lambda review: review["Rate"] == 1 or review["Rate"] == 5, reviews))
      if len(reviews) >= 3:
            final.append( (reviewer, reviews) )
   print("Number of reviewers with 3+ reviews rated 1 or 5 star:", len(final))
   return final


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



'''Old Code'''
#reviewers = get_reviewers(reviews)
#busiest = max(reviewers.keys(), key=(lambda key: len(reviewers[key])))

# print(len(reviewers[busiest]))
# busiest = {}
# for r in get_reviewers(reviews):
   # if

# # takes a list of tuples of (reviewers, reviews)
# # returns the same list but any ratings which are between 1 and 5 are removed
# def remove_2though4_star_ratings(reviewers):
#   return [(r[0], [review for review in r[1] if review["Rate"] == 1 or review["Rate"] == 5]) for r in reviewers]
