from __future__ import print_function
from modules.amazon_parser import *

reviews = parserJSON('./library/amazon-review-data.json',1000)
# get dictionary with each user as key and a list of their reviews as value
reviewers = get_reviewers(reviews)
# remove all reviewers who reviewed less than 3 products
reviewers = remove_lessthan3(reviewers)
# change dictionary into list of tuples
reviewers = reviewers.items()
# remove all review which have rates of anything other than 1 or 5
reviewers = remove_2though4_star_ratings(reviewers)

# create a list of tuples... with first entry being the reviewer 
# and second being a concatenated string of the product ids reviewed
reviewers_short = []
for reviewer in reviewers:
   reviewers_short.append( (reviewer[0], [review["productId"] for review in reviewer[1]]) )

# sort the list of reviewers_short by their concatenated productId's
# this way, if two reviewers reviewed the same products, they'll be adjacent
reviewers_short.sort(key=lambda review: review[1])


# compare adjacent reviewers to see if any are the same
for i in range(len(reviewers_short)-1):
   if reviewers_short[i][1][:3] == reviewers_short[i+1][1][:3]:
      print(reviewers_short[i][0], reviewers_short[i+1][0])



''' old code '''
# sorted_reviewers = sorted(reviewers.items(), len(reviewers[key]))
# busiest = max(reviewers.keys(), key=(lambda key: len(reviewers[key])))
# print(len(reviewers[busiest]))

# for each reviewer, sort their reviews by order of product ID
# for r in reviewers:
#    # r[0] is the reviewer id
#    # r[1] is the list of their reviews
#    r[1].sort(key=lambda review: review["productId"])

# print(*reviewers_short, sep="\n\n")
# # now sort reviewers by the number of reviews they left
# reviewers.sort(key=lambda x: len(x[1]))