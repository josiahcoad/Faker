from __future__ import print_function
from collections import defaultdict
from cosine_sim import cosine_sim
from numpy import mean as avg
from modules.amazon_parser import *
from collections import OrderedDict


MAX_USERS_IN_GROUP = 5 # found previously
MAX_PRODS_IN_GROUP = 7 # found previously
SIX_MONTHS = 15552000 # seconds in 6 months, used in GETF
FOUR_DAYS = 345600 # number of seconds in 4 days

fakegroup = {'FAKEGROUP': [
  ('U1', [{'Rate': 5, 'reviewId': 'U1', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'High Quality Organic and Made in the United States', 'Date': '1449885003', 'reviewText': "This fantastic shampoo is free of harsh chemicals and junk ingredients. It does a great job in making your hair full and nourished.", 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'},
   {'Rate': 5, 'reviewId': 'U1', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Cleanser with Anti-Aging Benefits', 'Date': '1449885003', 'reviewText': 'Your skin shows improvement on the first use of this facial cleanser. Its designed to cleanse, hydrate, and provide antioxidant power to protect your skin.', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}, 
   {'Rate': 5, 'reviewId': 'U1', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': '100 guaranteed', 'Date': '1449885003', 'reviewText': 'This all natural organic Vitamin C Serum is blended to reduce the signs of aging. Its gentle and effective, and it will start to renew your skin upon the first use.', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}, 
   {'Rate': 5, 'reviewId': 'U1', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Incredibly Soothing and Calming', 'Date': '1449885003', 'reviewText': 'This oil diffuser is terrific for aromatherapy. It will help lift your mood and cover stubborn odors. Its so much easier to fall asleep with it on.', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}, 
   {'Rate': 5, 'reviewId': 'U1', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': '100% Satisfaction Guarantee', 'Date': '1449885003.0', 'reviewText': 'This shampoo boasts all natural ingredients and is designed to prevent hair loss. The herbal ingredients definitely leave your hair super clean with a healthy shine!', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}, 
   {'Rate': 5, 'reviewId': 'U1', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': '100% Customer Satisfaction Guarantee', 'Date': '1449885003', 'reviewText': 'This essential oil is pure and all-natural. It&#8217;s often used in aromatherapy. Frankincense oil also is used to treat skin conditions such as acne and more.', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}, 
   {'Rate': 5, 'reviewId': 'U1', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Terrific Value 2013 Easy to Read', 'Date': '1449885003', 'reviewText': 'This monitor is very easy to use. It also has a very clear and large display for easy reading. ', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}]),
  ('U2', [{'Rate': 5, 'reviewId': 'U1', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'High Quality Organic and Made in the United States', 'Date': '1449885003', 'reviewText': "This fantastic shampoo is free of harsh chemicals and junk ingredients. It does a great job in making your hair full and nourished.", 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'},
   {'Rate': 5, 'reviewId': 'U2', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Cleanser with Anti-Aging Benefits', 'Date': '1449885003', 'reviewText': 'Your skin shows improvement on the first use of this facial cleanser. Its designed to cleanse, hydrate, and provide antioxidant power to protect your skin.', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}, 
   {'Rate': 5, 'reviewId': 'U2', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': '100 guaranteed', 'Date': '1449885003', 'reviewText': 'This all natural organic Vitamin C Serum is blended to reduce the signs of aging. Its gentle and effective, and it will start to renew your skin upon the first use.', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}, 
   {'Rate': 5, 'reviewId': 'U2', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Incredibly Soothing and Calming', 'Date': '1449885003', 'reviewText': 'This oil diffuser is terrific for aromatherapy. It will help lift your mood and cover stubborn odors. Its so much easier to fall asleep with it on.', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}, 
   {'Rate': 5, 'reviewId': 'U2', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': '100% Satisfaction Guarantee', 'Date': '1449885003.0', 'reviewText': 'This shampoo boasts all natural ingredients and is designed to prevent hair loss. The herbal ingredients definitely leave your hair super clean with a healthy shine!', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}, 
   {'Rate': 5, 'reviewId': 'U2', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': '100% Customer Satisfaction Guarantee', 'Date': '1449885003', 'reviewText': 'This essential oil is pure and all-natural. It&#8217;s often used in aromatherapy. Frankincense oil also is used to treat skin conditions such as acne and more.', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}, 
   {'Rate': 5, 'reviewId': 'U2', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Terrific Value 2013 Easy to Read', 'Date': '1449885003', 'reviewText': 'This monitor is very easy to use. It also has a very clear and large display for easy reading. ', 'memberId': 'AOEFYWCVQJEKT', 'productId': 'B0079R6BD2'}])
]}
  # ('U2', [{'Rate': 5, 'reviewId': 'R2XWL5YA6JYDS', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Deep Cleaning Shampoo', 'Date': '1454870952', 'reviewText': "Great concentration, I only needed one pump for my hair which is past my shoulders, second shampoo you do not need a full pump.  Deep cleaning, clean smelling, lathers very well.  Hair is squeaky clean after use so if you have longer hair you are going to want to use conditioner ;)  I'm a licensed Cosmetologist and I always try products before selling/recommending to my clients, this one has my approval.  My scalp and hair felt very clean, hold the style very well weather you're scrunching or iron curling/straightening.  I have even went to sleep with damp hair and woke up to just having to pick my hair out and my waves were prominent the next morn'n.  I wanted this mainly for my 20 year old son which is starting to recede.  He has started using it and he too likes it so far with hopes of this shampoo stopping his hair line from going back more or hopefully unclogging his scalp pores and letting his hair regrow.  I'll update this in 2-3 months if there is any difference he has seen.  If you're interested and I have not updated please comment and I'll be more than happy to update you :)I received this item at a Discount in return for my Honest Review.", 'memberId': 'A13SC93G2S92PD', 'productId': 'B0079R6BD2'}, {'Rate': 5, 'reviewId': 'R1ZXLP1YFVVKIW', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Super Clean Felling!!', 'Date': '1456605069', 'reviewText': "Lightly scented with a Orange fragrance.  Very concentrated start off small as you do not need very much of this at all, I'd say about 1/4 to 1/2 a pump is more than enough.  Be careful when you open/unlock the pump as it had some cleanser on the stalk once I opened mine, pump unlocked and came right up with full pressure.  My face felt really hydrated, clean and fresh after each use.  Don't get in eyes cuz ouch it hurts, just flush your eye/s with water and life is good again ;)  I would highly recommend this item.I received this item at a Discounted price in return for my Honest Review.", 'memberId': 'A13SC93G2S92PD', 'productId': 'B00VMYKCL0'}, {'Rate': 5, 'reviewId': 'R2FIAOHEWKVH9R', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Multi Use Serum', 'Date': '1455432489', 'reviewText': "I've been using this to help with my fine lines, no major difference as of yet but I know it takes time.  If I see any major results I'll up date this review.  I have had NO irritation burning, itching, redness of my skin after use of this product.  I comes with a nice dropper to help control how much you use, which you do not need much, start off small if you need more, add more.  It has a nice light scent of oranges.  The product is clean in color, I have already tried Vit C Serum that was orange in color and I felt as though it dyed my skin so I threw it out, personal opinion on that situation.  It is also a great moisturizer, and a quick fix to chapped lips.I received this item for Free in return for my Honest Review.", 'memberId': 'A13SC93G2S92PD', 'productId': 'B012Q4M3DO'}, {'Rate': 5, 'reviewId': 'R1KPO474ZE6W7H', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Awesome Mini Diffuser', 'Date': '1460087681', 'reviewText': "This is awesome it has a study mist until automatic shut off.  I have been using this for a few days in my room at night with some Peppermint Oil in it as it's sinus issue time for me and so far this has really helped!!  There are 2 settings one is a contentious feed (red light) and the other is a 30 seconds on and 30 seconds off (green light), both will automatically shut off.  When I'm talking about the 2 different lights I'm talking about the on/power light, not the whole system different colored lights.  The whole system power lights are amazing, depending on what mood you feel like you have a very wide assortments of colors, blues, greens, purples, pinks, reds, peach, clear etc.  The motor itself is a little loud not bad but louder than others I have used.  I do like that you can hear the water flowing a little bit, it's very soothing.  You can adjust the mist direction by turning the whole system or by putting the top cover on in the direction you want the flow to go.  Personally I have them in opposite directions at night, I have the main light off, but the mini power/on light either green or red I have pointing in the other direction so I can't see it and the flow blowing towards me.  If I'm not sleeping I turn the spout to mist out towards the center of the room.  The mist goes straight up and doesn't swarm down in a big downward cloud of mist like another one that I have does.I received this item for Free in return for my Honest Review.  I did NOT receive any money or any other compensation, these are my honest thoughts.", 'memberId': 'A13SC93G2S92PD', 'productId': 'B014SF6MBI'}, {'Rate': 5, 'reviewId': 'RQBP6PVBY1JME', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Small Amount Goes a Long Ways', 'Date': '1456280709', 'reviewText': "Another great Shampoo from Art Naturals, I'm really impressed with their products.  I am a license Cosmetologist and I would highly recommend this shampoo.  You only need the size of a dime for shoulder length hair for your shp, on your second shampoo you need less.  It's super concentrated so a little goes a long ways.  I'd suggest a dime size for short hair, quarter max for very long thick hair.  Since I've been using this I have noticed that my hair is easier to comb through, I do not need as much conditioner after use of this shp, and my daily hair loss is a lot less.  After I apply my conditioner in my hair I run through with a pick to evenly distribute it through out my hair, the amount of hair on my pick after is a lot less this is how I know I'm losing less ;)  My daughter has longer thicker hair and she noticed the same results as I stated above.I received this item at a Discount in return for my Honest Review.", 'memberId': 'A13SC93G2S92PD', 'productId': 'B016XANH32'}, {'Rate': 5, 'reviewId': 'R184FYRJJZJX64', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Great Scent', 'Date': '1456283078', 'reviewText': "If you love the scent of the wooded outdoors you'll love this scent it's very natural smelling.  I like using this in my diffuser, such a clean scent and it also is good for a persons mind set, helps with anxiety and depression also.  I've also taken this along for my massage, it helps with muscle and joint pain, massage person told me and has also done this, &quot;add a drop of oil to sink of hot water and soak a towel, wring out, then place the towel on your body to muscle aches, or on your face&quot;  I would highly recommend this product to help you with any or all.  It also makes a great antiseptic, disinfectant (you can clean your house with this also and you'll also get a great scent after use ;)I received this item at a Discounted rate in return for my Honest Review.", 'memberId': 'A13SC93G2S92PD', 'productId': 'B017AJKNQ4'}, {'Rate': 5, 'reviewId': 'RNDD3MVKBNOO5', 'video': '0', 'verifiedPurchase': 'false', 'reviewTitle': 'Mini Thermometer and Humidity Display', 'Date': '1470894716', 'reviewText': "I'm using this outside to see if the humidity is close to what the weather stations say and it is pretty close.  I have a covered front porch so it's not in any eliminates.  Both the temp and the humidity levels are really close to what my cellphone says, therefore to me this product is very good and accurate give or take one devices info.  It's small but not too small, the numbers are easy to read, there are buttons on the back to make F or C temp, and you can find out the max and min humidity levels also just by clicking the buttons on the back.  It comes with batteries pre-installed with the battery protector that needs to be pulled out before the batteries will work.  It comes with a built in stand (molded into the frame).  With all this being said I would recommend this to others.I received this Mini Thermometer and Humidity display  for free in return for my honest and unbiased review, I did not receive any money or any other compensation in return, these are my honest thoughts.", 'memberId': 'A13SC93G2S92PD', 'productId': 'B01F9FAOPG'}])])
# with open("./library/groups.txt") as f:
   # groups = eval(f.read())

review_objects = parserJSON('./library/amazon-review-data-modified.json')

products_dict  = get_products(review_objects) # create a dict with product ID as the key and a list of the product's reviews as the value


with open("./library/groups_temp.txt") as f:
   groups = eval(f.read())

'''
groups = fakegroup
'''
groups_by_products = organize_by_product(groups)
groups_by_reviewers = organize_by_user(groups)

# Group Deviation (GD)
def GD(group_by_products):
  return max([D(product, reviews) for product, reviews in group_by_products])

def D(product, reviews):
  group_prod_rate = reviews[0]["Rate"]
  avg_prod_rate = avg([review["Rate"] for review in products_dict[product]])
  return abs(group_prod_rate - avg_prod_rate) / 4.0

# Group Member Content Similarity (GMCS)
def GMCS(groups_by_reviewers):
  return sum([MS(reviews) for reviewer, reviews in groups_by_reviewers]) / len(groups_by_reviewers)

def MS(reviews):
  texts = [review["reviewText"] for review in reviews]
  return avg([cosine_sim(review1, review2) for review1 in texts for review2 in texts])

# Group Size (GS) (number of users in group)
def GS(group_by_users):
    return float(len(group_by_users)) / MAX_USERS_IN_GROUP

# Group Size Ratio (GSR) (returns 1 if each product in the group were only reviewed by the group members)
def GSR(group_by_products):
  return avg ( [gsr(product, reviews) for product, reviews in group_by_products] )

def gsr(product, reviews):
  return float(len(reviews)) / len(products_dict[product])
# ------------------------

def GTW(group):
   return max([prod_TW(reviews) for product, reviews in group])

def prod_TW(reviews):
   timestamps = [float(review["Date"]) for review in reviews]
   _range = max(timestamps)-min(timestamps)
   return 1-_range/FOUR_DAYS if _range <= FOUR_DAYS else 0

def GCS(group):
   return max([CS(reviews) for product, reviews in group])

def CS(reviews):
   texts = [review["reviewText"] for review in reviews]
   return avg([cosine_sim(review1, review2) for review1 in texts for review2 in texts])

def GETF(group):
   return max([GTF(product, reviews) for product, reviews in group])

def GTF(product, reviews):
   earliest_product_review = min([float(review["Date"]) for review in products_dict[product]])
   latest_group_review = max([float(review["Date"]) for review in reviews])
   _range = latest_group_review-earliest_product_review
   return 1-_range/SIX_MONTHS if _range <= SIX_MONTHS else 0

# Group Support Count (GSUP) (number of products in group)
def GSUP(group):
  return float(len(group)) / MAX_PRODS_IN_GROUP

# Sum Scores
def scores(gbp, gbr):
   return [GCS(gbp), GTW(gbp), GETF(gbp), GSUP(gbp), GS(gbr), GSR(gbp), GD(gbp), GMCS(gbr)]

def get_all_scores_final(index):
	return scores(groups_by_products[index], groups_by_reviewers[index])

def get_all_scores():
  all_scores = []
  for i in range(len(groups_by_reviewers)):
     l = [i] + scores(groups_by_products[i], groups_by_reviewers[i])
     all_scores.append(l)
  return all_scores


# scores = [( i, sum(score) ) for i, score in enumerate(get_all_scores())]
# fakest_indexes = sorted(scores, lambda k: k[1], reverse=True)
# for top in fakest_indexes[:5]:
#   fakest_users = [reviewer for reviewer, review in groups_by_reviewers[fakest_index]]
#   print(fakest_users)
# with open("scores.txt", "w") as file:
#   file.write(repr(get_all_scores()))

# for s in all_scores:
#   print("GCS: %.5f, GTW: %.5f, GETF: %.5f, GSUP: %.5f, GS: %.5f, GSR: %.5f, GD: %.5f, GMCS %.5f"%(s))
# sorted(groups_score, key=lambda x: sum(x[1]), reverse=True)



# print sz of groups
# sz = defaultdict(int)
# for groupId, group in groups.items():
#    sz[len(group)] += 1
