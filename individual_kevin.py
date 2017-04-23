from modules.amazon_parser import *
from collections import defaultdict
from cosine_sim import cosine_sim

reviews = parserJSON('./library/amazon-review-data.json',)

"""
keys of reviews
`Rate`
`reviewText`
`video`
`verifiedPurchase`
`Date`
`productId`
`reviewId`
`memberId`
`reviewTitle`
"""

#rating for product p given by certain user 'm' and average given by other users.


####IRD####
def IRD():

    productRatingDictionary = defaultdict(lambda: {"review_counts": 0, "cumulative_score": 0}) #key is `productId` -> {"productId":{"review_counts": int, "cumulative_score": float}}
    customerToProductDictionary = defaultdict(lambda: []) #key is `memberId` -> {"memberId":[productA, productB, ...etc]}
    customerVectorDictionary = defaultdict(lambda: []) #key is `memberId` -> {"memberId":[feature1, feature2, etc...]}

    for review in reviews: #build up dictionaries
        if (review["productId"]!= "None" and review["memberId"]!= "None"):
            productRatingDictionary[ review["productId"] ]["cumulative_score"] += review["Rate"]
            productRatingDictionary[ review["productId"] ]["review_counts"] += 1
            customerToProductDictionary[ review["memberId"] ].append((review["productId"], review["Rate"])) #should further consider that reviewer has multiple ratings on the same product

    for key in customerToProductDictionary:
        for product in customerToProductDictionary[key]:
            UserID = key
            ProductID = product[0]
            UserRating = product[1]
            try:
                AvgProductRating = (productRatingDictionary[ product[0] ]["cumulative_score"] - UserRating)/(productRatingDictionary[ product[0] ]["review_counts"] - 1)
            except ZeroDivisionError:
                AvgProductRating = UserRating
            IRD = (UserRating - AvgProductRating) / 4
            #print(IRD)

        #customerVectorDictionary[]
        #print(customerToProductDictionary[key])

####ICS####

def ICS(reviews):
    customerToProductDictionary = defaultdict(lambda:defaultdict(lambda:[]))
    ICS_Dictionary = defaultdict(lambda:defaultdict(lambda:0))

    for review in reviews: #build up dictionaries
        if (review["productId"]!= "None" and review["memberId"]!= "None"):
            customerToProductDictionary[ review["memberId"] ][ review["productId"] ].append(review["reviewText"])

    for member in customerToProductDictionary:
        for productId in customerToProductDictionary[member]:
            temp = 0
            cnt = 0
            if len(customerToProductDictionary[member][productId]) > 1: #check if the same memeber review on a product repeatedly
                for i in customerToProductDictionary[member][productId]:
                    for j in customerToProductDictionary[member][productId]:
                        if i != j:
                            temp = cosine_sim(i, j)
                            cnt += 1
            if cnt != 0:
                ICS = 1.0* temp/cnt #take average
                ICS_Dictionary[member][productId] = ICS
    return ICS_Dictionary
