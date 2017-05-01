from __future__ import print_function
from modules.amazon_parser import *

# get a list of dictionary items which represent each review object (including metadata like product id and user id) 
reviews = parserJSON('./library/amazon-review-data.json')
# get a dict with {user : sorted list (by productId) of their review objects, ...}
user_dict = get_reviewers(reviews)
# remove all reviewers who reviewed less than 3 products with ratings other than 1 or 5
user_dict = remove_lessthan3(user_dict)


# takes a dictionary of users and their products
# returns a dictionary of {group1 : [(userId1, [{R1}, {R2}, ...]), (userId2, [{R1}, {R2}, ...]) ...], ...}
# groups are represented as concatenated productId's of products in that group: "R1-R2-R3"
def group_users(users_dict):
   # get a tuple of... (memberId, list of reviews that a user left for products which match 'productIds')
   def get_entry(memberId, productId_list):
      reviews = [review for review in users_dict[memberId] if review["productId"] in productId_list]
      return ( memberId, reviews )
   # create a list of tuples of... (reviewer, list of the product ids reviewed)
   users = [(memberId, [(review["productId"], review["Rate"]) for review in reviews]) for memberId, reviews in users_dict.items()]# equal to the function of nested loop
   groups = {}
   for i in range(len(users)-1):
      ref_user = users[i]
      for j in range(i+1,len(users)):
         comp_user = users[j]
         common_products = set(ref_user[1]).intersection(set(comp_user[1]))#cmp current and it's next till end
         common_products = sorted([review[0] for review in common_products])#sort by
         if len(common_products) >= 3:
            key = "-".join(common_products)##intersection
            comp_entry = get_entry(comp_user[0], common_products)
            if key in groups:
               if comp_user[0] not in [entry[0] for entry in groups[key]]: # make sure user's not already in group
                  groups[key].append(comp_entry)
            else:
               ref_entry  = get_entry(ref_user[0] , common_products)
               groups[key] = [ref_entry, comp_entry]

   return groups
'''
with open("./library/groups_chia.txt", "w") as f:
    f.write(repr(group_users(user_dict)))
with open("./library/groups_prodct.txt", "w") as f:
    f.write(repr(get_products(user_dict)))
'''
