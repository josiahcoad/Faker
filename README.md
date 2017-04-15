# Faker

This project is targeting those fake reviews, rating, and comments on shopping websites (such as Amazon.com), forums or review APP. The approach is mainly based on the ML technique.


## Code Example
To import the API and initialize your dictionary, please add these two lines at the top of your .py file.
```python
from modules.amazon_parser import *
reviews = parserJSON('./library/amazon-review-data.json',)
```

## API Reference

```python
parserJSON(path, numLines=None) 
#which will return a dictionary according to the top-numLines, the default is all Lines.

get_reviewers(reviews) 
#parse in your review dictionary and return a dictionary with keys of all reviewerID.

get_products(reviews)
#parse in your review dictionary and return a dictionary with keys of all productID.

normalizedVector(vector)
#parse in a vecotr(type of dictionary) and return a normalized vector.
```
