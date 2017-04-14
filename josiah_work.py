from amazon_parser import *

reviewers = get_reviewers(reviews)
busiest = max(reviewers.keys(), key=(lambda key: len(reviewers[key])))
print(len(reviewers[busiest]))