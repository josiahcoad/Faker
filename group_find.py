from __future__ import print_function
from modules.amazon_parser import *

# get a list of dictionary items which represent each review object (including metadata like product id and user id) 
reviews = parserJSON('./library/amazon-review-data.json')
# get a list of tuples with user as first entry and a list of the review objects their part of as the second
reviewers_reviews_dict = get_reviewers(reviews)
reviewers_reviews = reviewers_reviews_dict.items()
# remove all reviewers who reviewed less than 3 products with ratings other than 1 or 5
reviewers_reviews = remove_lessthan3(reviewers_reviews)

# create a new list of tuples... with first entry being the reviewer 
# and second being a list of the product ids reviewed
reviewers_products = []
for reviewer, reviews in reviewers_reviews:
   reviewers_products.append( (reviewer, [review["productId"] for review in reviews]) )

# get a sorted list of reviews that a user left for products which match 'productIds'
def get_product_reviews(productIds, userId):
   return [review for review in reviewers_reviews_dict[userId] if review["productId"] in productIds]

# go through all eligible reviewers and see which of them have three or more products in common
# take a ref_user and compare his products against all the other users. If they have 3 or more products
# in common with the ref_user then add them to a list with ref_user.
# .. this part is O(n^2*avg(len(productsList)))... it takes more than 30 seconds

# a group is made from a collection of comparer_users who have three or more products in common with ref_user 
# a group is a list made of 2 or more tuples like this:
'''
[ (ref_user, list of their reviews which they share with the entire group),
  (compare_user1, list of their reviews which they share with the entire group),
  (compare_user2, list of their reviews which they share with the entire group),
  ... 
]
'''
# there are problems with this...
# consider the following scenerio where all three users have reviewed the same products
'''
U1 : A, B, C
U2 : A, B, C
U3 : A, B, C
'''
# then, by this algo, there will be two groups
'''
G1 - (A, B, C) : U1, U2, U3
G2 - (A, B, C) : U2, U3
'''
# there should, of course, only be G1 - (A, B, C) : U1, U2, U3
# we could just check to make sure there isn't already a group for (A, B, C) but there's got to be a smarter way
groups = []
for i in range(len(reviewers_products)-1):
   ref_user = reviewers_products[i]
   newgroup = [ref_user]
   for j in range(i+1, len(reviewers_products)):
      compare_user = reviewers_products[j]
      shared_products = set(ref_user[1]).intersection(set(compare_user[1]))
      if len(shared_products) >= 3:
         newgroup.append(compare_user)
   if len(newgroup) >= 2:
      group_products = sorted(list(set(ref_user[1]).intersection(*[set(user[1]) for user in newgroup])))
      newgroup = [( user[0], get_product_reviews(group_products, user[0]) ) for user in newgroup]
      groups.append(newgroup)
print(*groups[0], sep="\n\n")
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

         # "delete" that (reviewer, products) so that it isn't added to another group... not sure about this
         # reviewers_products[j] = ("", [])
# print("The max number of items shared in a group is: ", max([len(group[0][1]) for group in groups]))
