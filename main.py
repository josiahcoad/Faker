## write a function to normalize the given vector


import  amazon_parser as ap
from collections import defaultdict


reviews = ap.reviews #get review array from the input data

R = set()
D = defaultdict(lambda:0)


for r in reviews:
    D[ r["reviewId"] ] += 1

for key in D:
    if D[key] > 1:
        R.add(key)


print(len(reviews))

# f = open("revised-data.txt","r")
# fo = open("test.json","w+")
# repeatedID = set()
#
# for line in f.readlines():
#     flag = False
#     for ID in R:
#         if ID in line:
#             rid = ID
#             flag = True
#             if flag and rid not in repeatedID:
#                 fo.write(line)
#             repeatedID.add(ID)
#             break
#
#     if flag == False:
#         fo.write(line)
#
# f.close()
# fo.close()


#print(cnt)
#print(len(reviews))
#print(len(D))
