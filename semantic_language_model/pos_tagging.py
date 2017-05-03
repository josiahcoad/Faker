import nltk
from nltk import *

# nltk.download('all')

def parserJSON(path, numLines=None):
  numLines = numLines or len(open(path).read().split("\n")) - 1
  with open(path) as txt:
    reviews = [eval(next(txt)) for x in range(numLines)]
  print("Number of reviews:", len(reviews))
  return reviews

def pos_tagging(reviews):
	tagged_review = []
	for review in reviews:
		reviewerId = review["memberId"]
		reviewText = review["reviewText"]
		text = word_tokenize(reviewText)
		tagged_review.append((reviewerId, nltk.pos_tag(text)))
	return tagged_review


reviews = parserJSON('../library/amazon-review-data.json')
print pos_tagging(reviews)
