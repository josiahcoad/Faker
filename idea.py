users = [("U1" , ['A', 'B', 'C', 'D', 'E', 'F']),   
         ("U2" , ['A', 'B', 'C']               ),
         ("U3" ,                ['D', 'E', 'F']),
         ("U4" ,           ['C', 'D', 'E']     ),
         ("U5" , ['A', 'B', 'C']               )]


print(get_review(users_dict, "U1", "A"))
# takes a list of tuples (userID : string, productId-list : list of strings)
# returns a dictionary of groups with the key as the concatenated productId
# and the value as a set of productsId's which are common to that group
def group_users(users):
   groups = {}
   for i in range(len(users)-1):
      ref_user = users[i]
      for j in range(i+1,len(users)):
         comp_user = users[j]
         common_products = list(set(ref_user[1]).intersection(set(comp_user[1])))
         if len(common_products) >= 3:
            key = "".join(sorted(common_products))
            if key in groups:
               groups[key].add(comp_user[0])
            else:
               groups[key] = set([ref_user[0], comp_user[0]])
   print(groups)

group_users(users)



'''for later''
# users_dict = {"U1": [{"productID": "A", "review" : "good"}, {"productID": "B", "review" : "bad"}]}

# # return a sorted list of products in productId_list that user has reviewed
# def get_review(users_dict, user, productId_list):
#    return sorted([review for review in users_dict[user] if review["productID"] in productId_list])
