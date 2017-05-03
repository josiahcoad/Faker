from semantic_similarity import *
from collections import defaultdict
import itertools

def parserJSON(path, numLines=None):
  numLines = numLines or len(open(path).read().split("\n")) - 1
  with open(path) as txt:
    reviews = [eval(next(txt)) for x in range(numLines)]
  print("Number of reviews:", len(reviews))
  return reviews

def getReviewsByReviewerId(reviews):
	reviewsById = defaultdict(list)
	for review in reviews:
		reviewerId = review["memberId"]
		reviewText = review["reviewText"]
		reviewsById[reviewerId].append(reviewText)
	return reviewsById

reviews = parserJSON('../library/amazon-review-data.json',10)
reviewsById = getReviewsByReviewerId(reviews)

for reviewers in reviewsById:
	reviewsForEachId = reviewsById[reviewers]
	combination_docs = list(itertools.combinations(reviewsForEachId, 2))
	for combination in combination_docs:
		s1 = combination[0]
		s2 = combination[1]
		print s1
		print "\n"
		print s2
		print reviewers, similarity(s1, s2, True)

