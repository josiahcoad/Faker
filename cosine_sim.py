import math, re, string
from collections import defaultdict
from nltk.stem.porter import PorterStemmer

def purify(s):
   s = s.translate(None, string.punctuation)
   s = re.sub('(\s+)(a|an|and|but|the)(\s+)', ' ', s)
   s = [ps.stem(word.lower()) for word in re.split('\W+', s)]
   # print(s)
   return s


ps = PorterStemmer()
def cosine_sim(string1, string2):
   count1 = defaultdict(int)
   count2 = defaultdict(int)
   for word in purify(string1):
      count1[ps.stem(word.lower())] += 1
   for word in purify(string2):
      count2[ps.stem(word.lower())] += 1
   dot_product = sum(count1.get(key, 0)*count2.get(key, 0) for key in count1)
   magnitude = math.sqrt(sum([int(val)**2 for val in count1.values()])) * math.sqrt(sum([int(val)**2 for val in count2.values()]))
   return dot_product/magnitude if magnitude else 0

if __name__ == "__main__":
   R1 = "I have jumped!"
   R2 = "I will jump..."
   # R1 = "I am using this  product for  more than  3 weeks and  it is working great on me . I had lot of hair falls and used many products before to stop the hair fall but was in vain .I did not know what  to do , then I got  to know about this  product from my close  relative.  I bought this & after using it for few weeks , it started  to show results -  I was so happy that  my hair fall stopped and my hair became thick . Highly recommendable to everyone who has hairfall problem."
   # R2 = "supplement has done me nothing else but the good. Not only has it worked effectively for me but also for my friends. The results have been nothing less than tender skin, strong nails and hair. It also helps boost my energy which keeps me going strong the entire day. I indorse it."
   print (cosine_sim(R1, R2))