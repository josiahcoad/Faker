from modules.amazon_parser import *

reviews = parserJSON('./library/amazon-review-data.json', 100)

# sort dictionary reviews by len of reviews
reviewers = get_reviewers(reviews)
sorted_reviewers = sorted(reviewers.items(), len(reviewers[key]))
# busiest = max(reviewers.keys(), key=(lambda key: len(reviewers[key])))
# print(len(reviewers[busiest]))
