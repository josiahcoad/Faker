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
d = {"reviewId": "R17L2MXWXEZNEA", "verifiedPurchase": "false", "reviewText": "I travel internationally on a regular basis and have always had those really dorky white compression socks. They are so stretched out now that they aren\u2019t compressing anything ;) I was excited to try socks that not only had an important function but also looked good. Here\u2019s what it was like from opening the package at the departures gate for a 17 hour flight, to taking them off: - Open package, admire the paisley pattern - Try to stretch the foot hole a bit to get my foot in, realize that they are pretty strongly compressed. (That\u2019s good, right! That\u2019s the point of compression socks) - Make grimacing faces while pulling the socks on, much to the amusement of my fellow passengers in the departure gate, most of whom are putting on their dorky white socks - Get the sock on and wonder why on earth there are 2 extra inches of length in the foot. The rest of the sock fits well (from a length \u2013 toe to knee perspective), so are these designed for super long-footed people? - Figure that since they are now calling my flight, I will not worry about the extra inches of sock flopping around my heel and toe - Settling in to my seat for the 17 hour flight, get a slight twinge of worry as to why I\u2019m feeling rubbing on the top of my bare toes on both feet. Rubbing, as in\u2026blistery rubbing - Sleep for several hours courtesy of the drinks cart, and wake up to think \u2018my legs feel comfortably compressed but the top of my toes are feeling pretty raw\u2019 - Go back to sleep - Fast forward to hour 18, when I remove socks in the rental car at the arrival destination - Stare at toes in dismay. They have indeed been rubbed raw by the socks. Blisters on the top of each toe. So in sum \u2013 I\u2019m wondering if there\u2019s a slight miscalculation in the fit of these socks. They fit great in length from toe/ankle to knee. The amount of compression around the actual calf area is comfortable. BUT\u2026they are way too long in the foot. (I chose the size carefully based on my shoe size). And, they are way too tight in the foot and possibly because of the extra length, they didn\u2019t sit firmly on the foot. The rubbing and blisters ended up being problematic for the entire duration of my trip. I did wear them on the trip home (15 hours), because I needed compression socks. I got smart and put bandaids on top of my toes. No blisters. But I don\u2019t want to have to wear bandaids to prevent blisters. Hopefully they will \u2018break in\u2019 a bit and this won\u2019t be an ongoing problem. * I received the socks for evaluation and review", "memberId": "AI2VYX30JR9GE", "Rate": 4.0, "video": "0", "Date": "1467176400.0", "reviewTitle": "If it wasn't for the blisters...", "productId": "B01EX4UWS8"}

def removeNonAscii(s):
    return "".join(filter(lambda x: ord(x)<128, s))          


def _parserJSON(path, numLines=None):
   numLines = numLines or len(open(path).read().split("\n")) - 1
   with open(path, encoding='utf-8') as txt:
      reviews = [eval(next(txt)) for x in range(numLines)]
   return reviews


# take only first 10,0000 for ease
reviews = _parserJSON('./revised-data.txt', 100) # 90000
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

