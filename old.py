from textblob import TextBlob
# sort by sentiment polarity
dataList = sorted(dataList, key=lambda k: TextBlob(k["reviewText"]).sentiment.polarity)
# compare sorted sentiment list with star rating to see accuracy of sentiment analysis
for i in range(0, 10000, 1000):
   print(numpy.mean([int(entry["Rate"]) for entry in dataList[i:i+1000]]))


# create dictionary of most reviewed products (or can change productId to memberId)
products = {}
for entry in dataList:
   if entry["productId"] not in products:
      products[entry["productId"]] = 1
   else:
      products[entry["productId"]] += 1
# get k most reviewed products / active users
k = 10
mostReviewed = sorted(products.iterkeys(), key=(lambda occur: products[occur]), reverse=True)
for elem in mostReviewed[1:k+1]:
   print (elem, products[elem])

