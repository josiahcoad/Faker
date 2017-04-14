
import  amazon_parser as ap
from collections import defaultdict

reviews = ap.reviews #get review array from the input data

R = set()

for r in reviews:
    R.add(r["reviewId"])


print(len(reviews))
print(len(R))
