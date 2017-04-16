from __future__ import print_function
from modules.amazon_parser import *

# get a list of dictionary items which represent each review object (including metadata like product id and user id) 
reviews = parserJSON('./library/amazon-review-data.json')
# get a list of tuples with user as first entry and a list of the review objects their part of as the second
reviewers_reviews = get_reviewers(reviews)
# remove all reviewers who reviewed less than 3 products with ratings other than 1 or 5
reviewers_reviews = remove_lessthan3(reviewers_reviews)

# create a new list of tuples... with first entry being the reviewer 
# and second being a list of the product ids reviewed
reviewers_products = []
for reviewer, reviews in reviewers_reviews:
   reviewers_products.append( (reviewer, [review["productId"] for review in reviews]) )

# go through all eligible reviewers and see if any of them have three or more products in common
# .. this part is O(n^2*avg(len(productsList)))... it takes more than 30 seconds
# a group is a list of lists. Each internal list (representing a group) has 2 or more tuples of (userid, list of reviews)
groups = []
for i in range(len(reviewers_products)-1):
   products = reviewers_products[i][1]
   newgroup = [reviewers_reviews[i]]
   for j in range(i+1, len(reviewers_products)):
      comp_products = reviewers_products[j][1]
      if len(set(products).intersection(set(comp_products))) >= 3:
         newgroup.append(reviewers_reviews[j])
         # maybe "delete" that (reviewer, products) so that it isn't added to another group??
         reviewers_products[j] = ("", [])
   if len(newgroup) >= 2:
      groups.append(newgroup)
print("Number of groups: ", len(groups))


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

# print(reviewers_products[i][0], reviewers_products[i+1][0])
# if reviewers_products[i][1][:3] == reviewers_products[i+1][1][:3]:

# # remove all review which have rates of anything other than 1 or 5
# reviewers = remove_2though4_star_ratings(reviewers)




# ''' from here on down... I'm not sure... '''
# # sort the list of reviewers_short by their list of productId's
# # this way, if two reviewers reviewed the same products, they'll be adjacent
# reviewers_products.sort(key=lambda review: review[1])

# # compare adjacent reviewers to see if have reviewed three or more of the same products
# groups = []
# for i in range(len(reviewers_products)-1):
#    review = reviewers_products[i]
#    newgroup = [review]
#    next_review = reviewers_products[i+1]
#    while review[1][:3] == next_review[1][:3] and i < len(reviewers_products)-1:
#       newgroup.append(next_review)
#       i += 1
#       next_review = reviewers_products[i+1]
#    if len(newgroup) >= 2:
#       groups.append(newgroup)
# print(*groups, sep="\n\n")
