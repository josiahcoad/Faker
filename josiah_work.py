from __future__ import print_function
from modules.amazon_parser import *

reviews = parserJSON('./library/amazon-review-data.json')

# get dictionary with each user as key and a list of their reviews as value
reviewers = get_reviewers(reviews)
# change dictionary into list of tuples
reviewers = reviewers.items()
# sort reviewers by the number of reviews they left
reviewers.sort(key=lambda x: len(x[1]))
# for each reviewer, sort their reviews by order of product ID
for r in reviewers:
   # r[0] is the reviewer id
   # r[1] is the list of their reviews
   r[1].sort(key=lambda review: review["productId"])


# create a list of tuples... with first entry being the reviewer 
# and second being a concatenated string of the product ids reviewed 

# this way, if two reviewers reviewed the same objects, they'll be adjacent
reviewers_short = []
for reviewer in reviewers:
   reviewers_short.append((reviewer[0], "".join([review["productId"] for review in reviewer[1]])))
# print(*reviewers_short, sep="\n\n")

# compare adjacent reviewers to see if any are the same
for i in range(len(reviewers_short)-1):
   if reviewers_short[i][1][:4] == reviewers_short[i+1][1][:4]:
      print(reviewers_short[i])





''' old code '''
# sorted_reviewers = sorted(reviewers.items(), len(reviewers[key]))
# busiest = max(reviewers.keys(), key=(lambda key: len(reviewers[key])))
# print(len(reviewers[busiest]))
