import json, pprint, numpy

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


def _parserJSON(path, numLines=None):
   numLines = numLines or len(open(path).read().split("\n")) - 1
   with open(path, encoding='utf-8') as txt:
      reviews = [eval(next(txt)) for x in range(numLines)]
   return reviews


# take only first 10,0000 for ease
reviews = _parserJSON('./revised-data.txt', 1000) # 90000
print(reviews)
# for num, review in enumerate(reviews):
#    try:
#       print(review)
#    except Exception as e:
#       print(num, e)
reviewers = {}
print("Number of reviews:", len(reviews))
for review in reviews:
   reviewerId = review["memberId"]
   if reviewerId not in reviewers:
      reviewers[reviewerId] = [review]
   else:
      reviewers[reviewerId].append(review)

print("Number of reviewers:", len(reviewers))

products = {}
for review in reviews:
   productId = review["productId"]
   if productId not in products:
      products[productId] = [review]
   else:
      products[productId].append(review)

print("Number of products:", len(products))

