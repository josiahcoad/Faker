from modules.amazon_parser import *

# grouping users by the timestamp for each product

reviews = parserJSON('./library/amazon-review-data.json')
products = get_products(reviews)
reviewers = get_reviewers(reviews)
# print reviewers

def group_users(products):
	for product_id in products:
		products[product_id] = sorted(products[product_id], key=lambda k: k['Date'])
	return products

def group_products(users):
	user_dict = {}
	for user in users:
		if user not in user_dict:
			user_dict[user] = []
		for review in users[user]:
			user_dict[user].append(review["productId"])
	return user_dict

user_dict = group_products(reviewers)
# print len(user_dict)
# print len(reviewers)
group = {}
user_list = user_dict.keys()
for i in range(0,len(user_list)):
	count = 1
	for j in range(i,len(user_list)):
		intersection = list(set(user_dict[user_list[i]]).intersection(set(user_dict[user_list[j]])))
		if len(intersection) >= 3:
			group[count] = (user_list[i],user_list[j])
			count = count + 1
		
print len(group)

			

