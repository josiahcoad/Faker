from __future__ import print_function
from collections import defaultdict
from cosine_sim import cosine_sim
from numpy import mean as avg
import json
from modules.amazon_parser import *
with open("./library/groups.txt") as f:
   groups = eval(f.read())

Final_Input = []
# takes a group which is organized by reviewer_reviews and translates it to product_reviews
def translate_group(group):
   reviews = []
   for user_reviews in group:
      reviews.extend(user_reviews[1])
   products_reviews = defaultdict(list)
   for review in reviews:
    products_reviews[review["productId"]].append(review)
   return products_reviews.items()


#products_reviews_traslated = translate_group(groups)


MAXTIME = 345600 # number of seconds in 4 days
def GTW(group):
   products_reviews = translate_group(group)
   timewindows = []
   for product_reviews in products_reviews:
      timestamps = [float(review["Date"]) for review in product_reviews[1]]
      timewindows.append(prod_TW(timestamps))
   return max(timewindows)

def prod_TW(timestamps):
   _range = max(timestamps)-min(timestamps)
   return 1-_range/MAXTIME if _range < MAXTIME else 0

def CS(reviews):
    cs = []
    for review in reviews:
        for review2 in reviews:
            cs.append(cosine_sim(review, review2))
    return avg(cs)
def GCS(group):
   products_reviews = translate_group(group)
   cs = []
   for product_reviews in products_reviews:
      reviews = [review["reviewText"] for review in product_reviews[1]]
      cs.append(CS(reviews))
   return max(cs)

reviews = parserJSON('./library/amazon-review-data.json')
product_dict = get_products(reviews)
def get_avg(Name):
    if(len(product_dict[Name])>0):
        count = 0
        sum = 0
        for i in range(len(product_dict[Name])):
            sum+= product_dict[Name][i]["Rate"]
            count+=1
    #    print ("Overall average:",float(sum),float(count))
    #    print (float(sum/count))
        return float(sum/count)
    else:
        return 0

def GD(group):
    Deviation = []
    handle = set()
    for i in range(len(group)):
        cur_user = group[i]
        print("People:",cur_user[0])
        for item in cur_user[1]:
            if(item["productId"] not in handle):
                handle.add(item["productId"])
                if(item["Rate"]==5):
                    Deviation.append(abs(5-get_avg(item["productId"]))/4)
                elif(cur_user[1][1]["Rate"]==1):
                    Deviation.append(abs(get_avg(item["productId"])-1)/4)
    return max(Deviation)

def GMCS(group):
	MCS = []
	count = []
	for i in range(len(group)):
		print ("Initial :",i,"~~",len(group))
		cur_user = group[i]
		MCS.append(0)
		count.append(0)
		for x in range(len(cur_user[1])-1):#each review
			for y in range(x+1,len(cur_user[1])):
				MCS[i]+=cosine_sim(cur_user[1][x]["reviewText"], cur_user[1][y]["reviewText"])		
				count[i]+=1	
		MCS[i]/=count[i]
		print ("MCS:",i,":",MCS[i])
	Sum = 0
	for indi in MCS:
		Sum+=indi
	return float(Sum)/len(group)


def GS(group):
    return len(group)

def GSR(group):
    handle = set()
    for i in range(len(group)):
        cur_user = group[i]
        for item in cur_user[1]:
            if(item["productId"] not in handle):
                handle.add(item["productId"])
    GSR = 0
    for product in handle:
        GSR+=len(group)/len(product_dict[product])
    return float(GSR)/len(handle)

print ( "GMCS of first group:",GSR(groups.items()[0][1]))


#print (len(groups.items()[1][1]))
#print(groups.items()[1][1])

#for groupId, groupU in groups.items():
#   print (groupId, groupU,'\n')
#print(sz)
