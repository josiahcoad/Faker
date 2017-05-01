'''
Maximum number of reviews
It was observed that about 75 % of spammers write more than 3 reviews on any given day. Therefore, taking into account the number of reviews a user writes per day can help detect spammers since 90 % of legitimate reviewers never create more than one review on any given day.

Percentage of positive reviews
Approximately 85 % of spammers wrote more than 80 % of their reviews as positive reviews, thus a high percentage of positive reviews might be an indication of an untrustworthy reviewer.

Review length
The average review length may be an important indication of reviewers with questionable intentions since about 80 % of spammers have no reviews longer than 135 words while more than 92 % of reliable reviewers have an average review length of greater than 200 words.

Reviewer deviation
It was observed that spammers ratings tend to deviate from the average review rating at a far higher rate than legitimate reviewers, thus identifying user rating deviations may help in detection of dishonest reviewers.

Maximum content similarity
The presence of similar reviews for different products by the same reviewer has been shown to be a strong indication of a spammer. Mukherjee et al. [23] used cosine similarity; however, other more advanced similarity functions based upon word meanings versus the words themselves have shown promise 
'''



import time
from collections import defaultdict
from nltk.stem.porter import *

ps = PorterStemmer()

def parserJSON(path, numLines=None):
    numLines = numLines or len(open(path).read().split("\n")) - 1
    with open(path) as txt:
        reviews = [eval(next(txt)) for x in range(numLines)]
    return reviews

def cosine_sim(s1, s2):
    dict1 = defaultdict(lambda: int)
    dict2 = defaultdict(lambda: int)

    for word in re.split('\W+', s1):
        word = ps.stem(word)
        word = word.lower()
        dict1[word] += 1

    for word in re.split('\W+', s2):
        word = ps.stem(word)
        word = word.lower()
        dict2[word] += 1

    intersection = set(dict1.keys()) & set(dict2.keys())
    numerator = sum([dict1[x] * dict2[x] for x in intersection])

    denominator = math.sqrt(sum([dict1[x]**2 for x in dict1.values()])) + math.sqrt(sum([dict2[x]**2 for x in dict2.values()]))

    return float(numerator/denominator) if denominator else 0.0



reviews = parserJSON('../library/amazon-review-data.json')

reviewer_collection = defaultdict(lambda: defaultdict(int))

def maximum_reviews(reviews):
    reviews_per_day = defaultdict(lambda: defaultdict(float))
    avg_reviews_per_day = defaultdict(lambda: defaultdict(float))
    for i in range(len(reviews)):
        day = time.strftime('%Y%m%d', time.localtime(float(reviews[i]["Date"])))
        reviews_per_day[reviews[i]["memberId"]][day] += 1

    for key1 in reviews_per_day:
        for key2 in reviews_per_day[key1]:
            avg_reviews_per_day[key1] =  sum(reviews_per_day[key1].values())/len(reviews_per_day[key1].keys())
    count = 0
    for key in avg_reviews_per_day:
        if avg_reviews_per_day[key] > 3:
            count += 1
    return avg_reviews_per_day

def pos_reviews(reviews):
    sentiment_reviews = defaultdict(lambda: defaultdict(float))
    for i in range(len(reviews)):
        sentiment_reviews[reviews[i]["memberId"]][reviews[i]["reviewId"]] = reviews[i]["Rate"]
    positive_reviews = defaultdict(lambda: float)

    for key1 in sentiment_reviews:
        count_pos = 0
        for key2 in sentiment_reviews[key1]:
            if sentiment_reviews[key1][key2] > 3:
                count_pos += 1
        positive_reviews[key1] = float(count_pos)/float(len(sentiment_reviews[key1].keys()))
    return positive_reviews


def review_length(reviews):
    review_length_collection = defaultdict(lambda: defaultdict(float))
    for i in range(len(reviews)):
        review_length_collection[reviews[i]["memberId"]][reviews[i]["reviewId"]] = len(reviews[i]["reviewText"])
    avg_review_length_collection = defaultdict(lambda: float)
    for key1 in review_length_collection:
        for key2 in review_length_collection[key1]:
            avg_review_length_collection[key1] = float(sum(review_length_collection[key1].values()))/float(len(review_length_collection[key1].keys()))
    return avg_review_length_collection

def reviewer_deviation(reviews):
    product_rating = defaultdict(lambda: defaultdict(float))
    for i in range(len(reviews)):
        product_rating[reviews[i]["productId"]]["memberId"] = reviews[i]["Rate"]

    avg_product_rating = defaultdict(lambda: float)

    for key1 in product_rating:
        for key2 in product_rating[key1]:
            avg_product_rating[key1] = float(sum(product_rating[key1].values()))/float(len(product_rating[key1].keys()))

    deviation_member_rating = defaultdict(lambda: defaultdict(float))

    avg_deviation_member_rating = defaultdict(lambda: float)

    for i in range(len(reviews)):
        deviation_member_rating[reviews[i]["memberId"]][reviews[i]["productId"]] = reviews[i]["Rate"] - avg_product_rating[reviews[i]["productId"]]

    for key1 in deviation_member_rating:
        for key2 in deviation_member_rating[key1]:
            avg_deviation_member_rating[key1] = float(sum(deviation_member_rating[key1].values()))/float(len(deviation_member_rating[key1].keys()))

    # for key in avg_deviation_member_rating:
    #     if avg_deviation_member_rating[key] > 1.0:
            # print key

    return avg_deviation_member_rating

def content_similarity(reviews):
    pass


def construct_feature_vector():
    avg_reviews_per_day = maximum_reviews(reviews)
    positive_reviews = pos_reviews(reviews)
    avg_review_length_collection = review_length(reviews)
    avg_deviation_member_rating = reviewer_deviation(reviews)

    training_data = {} 

    for key in avg_reviews_per_day:
        if key not in training_data:
            training_data[key] = []
        if avg_reviews_per_day[key] > 3:
            training_data[key].append(5 * avg_reviews_per_day[key])
        else:
            training_data[key].append(0.5 * avg_reviews_per_day[key])

    for key in positive_reviews:
        if positive_reviews[key] > 0.8:
            training_data[key].append(3 * positive_reviews[key])
        else:
            training_data[key].append(0.2 * positive_reviews[key])

    for key in avg_review_length_collection:
        if avg_review_length_collection[key] < 135.0:
            training_data[key].append( 3 * (avg_review_length_collection[key] - 135.0 ))
        else:
            training_data[key].append( (avg_review_length_collection[key] - 135.0))

    for key in avg_deviation_member_rating:
        if avg_deviation_member_rating[key] > 1.0:
            training_data[key].append(10 * avg_deviation_member_rating[key] )
        else:
            training_data[key].append( avg_deviation_member_rating[key]  )

    return training_data


# reviewer_deviation(reviews)
    

    


# pos_reviews(reviews)

# maximum_reviews(reviews)

# review_length(reviews)


